"""WAN 2.2 MAX integration — prompt pack, ComfyUI, and external endpoint."""

import json
import hashlib
import shutil
from pathlib import Path
from typing import Optional

from .config import get_project_root, load_wan_config
from .models import Shot
from .naming import prompt_filename, input_frame_filename, shot_filename
from .logging_utils import get_logger

logger = get_logger("wan")

GLOBAL_POSITIVE = (
    "Original mature psychological seinen anime production keyframe, "
    "hand-drawn 2D television anime look, realistic adult proportions, "
    "sharp angular face construction, restrained psychological expression, "
    "moderately thick clean outer ink lines, thinner facial linework, "
    "tapered hair strokes, smaller mature eyes, heavy upper eyelids, "
    "visible lower eyelid lines, flat iris colour, minimal eye highlights, "
    "base colour plus one hard-edged cel-shadow tone, modern clean compositing, "
    "controlled mature colour palette, readable skin tones, navy, slate blue, "
    "faded cyan, deep green, burgundy, violet and restrained warm practical light, "
    "cinematic framing, realistic physical weight, subtle hand-drawn imperfection, "
    "consistent character identity, consistent clothing, premium modern seinen thriller"
)

GLOBAL_NEGATIVE = (
    "photorealistic live action, digital painting, painterly concept art, "
    "glossy CGI, western 3D animation, plastic skin, airbrushed skin, "
    "soft gradient shading, excessive bloom, orange and purple colour wash, "
    "oversaturated neon, rainbow cyberpunk, chibi, cute anime, childish face, "
    "giant eyes, sparkling eyes, goofy shonen expression, exaggerated anatomy, "
    "changing face, changing hairstyle, changing clothing, unstable identity, "
    "face melting, warped eyes, bad hands, extra fingers, deformed vehicle, "
    "changing car model, melted wheels, excessive motion blur, multiple camera moves, "
    "uncontrolled camera orbit, random symbols, subtitles, text, logo, watermark"
)


def build_full_positive(shot: Shot) -> str:
    parts = [shot.positive_prompt.rstrip(", ")]
    parts.append(GLOBAL_POSITIVE)
    return ", ".join(parts)


def build_full_negative(shot: Shot) -> str:
    if shot.negative_prompt:
        return shot.negative_prompt + ", " + GLOBAL_NEGATIVE
    return GLOBAL_NEGATIVE


def export_prompt_file(shot: Shot, output_dir: Path) -> Path:
    wan_cfg = load_wan_config()
    gen = wan_cfg.get("generation", {})

    fname = prompt_filename(shot.shot_id, shot.title)
    out_path = output_dir / fname

    content = f"""MODE: {"IMAGE TO VIDEO" if shot.generation_mode == "image_to_video" else "TEXT TO VIDEO"}
MODEL: WAN 2.2 MAX 14B Q8
WIDTH: {gen.get('width', 832)}
HEIGHT: {gen.get('height', 480)}
FRAMES: {gen.get('frames', 81)}
STEPS: {gen.get('steps', 20)}
BATCH: {gen.get('batch_size', 1)}
SPEED LORA: {"ON" if gen.get('speed_lora') else "OFF"}
SEED: {shot.seed if shot.seed else "BLANK FOR DISCOVERY"}

INPUT IMAGE:
{shot.input_image if shot.generation_mode == "image_to_video" else "N/A (text-to-video)"}

POSITIVE PROMPT:
{build_full_positive(shot)}

NEGATIVE PROMPT:
{build_full_negative(shot)}

MOTION PRIORITY:
- Primary: {shot.primary_action}
- Secondary: {', '.join(shot.secondary_motion) if shot.secondary_motion else 'none'}

CAMERA:
{shot.camera}

LIGHTING:
{shot.lighting}

COLOUR SCRIPT:
{shot.colour_script}

REJECT IF:
- Face drift or identity change
- Hair/outfit change
- Vehicle deformation
- Multiple camera moves
- Excessive mouth animation
- CGI/photorealistic drift
- Orange-purple colour wash
- Text/watermark appears
"""

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(content, encoding="utf-8")
    logger.info(f"Exported prompt: {fname}")
    return out_path


def detect_comfyui() -> Optional[str]:
    import urllib.request
    try:
        resp = urllib.request.urlopen("http://127.0.0.1:8188/system_stats", timeout=3)
        if resp.status == 200:
            logger.info("ComfyUI detected at http://127.0.0.1:8188")
            return "http://127.0.0.1:8188"
    except Exception:
        pass

    common_dirs = [
        Path(r"C:\AI\ComfyUI"),
        Path.home() / "ComfyUI",
        Path(r"D:\ComfyUI"),
    ]
    for d in common_dirs:
        if (d / "main.py").exists():
            logger.info(f"ComfyUI installation found at {d} (not running)")
            return None
    return None


def submit_to_comfyui(shot: Shot, comfyui_url: str) -> Optional[str]:
    """Submit a shot to ComfyUI API. Returns prompt_id or None."""
    import requests

    wan_cfg = load_wan_config()
    gen = wan_cfg.get("generation", {})

    workflow = _build_comfyui_workflow(shot, gen)
    payload = {"prompt": workflow}

    try:
        resp = requests.post(f"{comfyui_url}/prompt", json=payload, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            prompt_id = data.get("prompt_id", "")
            logger.info(f"Submitted {shot.shot_id} to ComfyUI: {prompt_id}")
            return prompt_id
        else:
            logger.error(f"ComfyUI submission failed: {resp.status_code}")
    except Exception as e:
        logger.error(f"ComfyUI connection error: {e}")

    return None


def _build_comfyui_workflow(shot: Shot, gen: dict) -> dict:
    """Build a minimal ComfyUI workflow dict for WAN 2.2 I2V/T2V."""
    return {
        "_meta": {
            "title": f"NISTAR_{shot.shot_id}",
            "model": "WAN 2.2 MAX 14B Q8",
            "mode": shot.generation_mode,
        },
        "settings": {
            "width": gen.get("width", 832),
            "height": gen.get("height", 480),
            "frames": gen.get("frames", 81),
            "steps": gen.get("steps", 20),
            "seed": shot.seed,
            "positive": build_full_positive(shot),
            "negative": build_full_negative(shot),
            "input_image": shot.input_image if shot.generation_mode == "image_to_video" else None,
        },
    }
