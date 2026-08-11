"""DaVinci Resolve export utilities."""

import json
import csv
import shutil
from pathlib import Path

from .config import get_project_root
from .models import Shot
from .manifests import load_shot_manifest
from .naming import resolve_video_filename, resolve_dialogue_filename
from .logging_utils import get_logger

logger = get_logger("resolve")


def export_for_resolve(episode: str = "episode_01"):
    root = get_project_root()
    shots = load_shot_manifest(episode)

    resolve_dir = root / "davinci" / episode
    video_dir = resolve_dir / "video"
    dialogue_dir = resolve_dir / "dialogue"
    sfx_dir = resolve_dir / "sfx"
    cue_dir = resolve_dir / "cue_sheets"
    guide_dir = resolve_dir / "edit_guides"

    for d in [video_dir, dialogue_dir, sfx_dir, cue_dir, guide_dir]:
        d.mkdir(parents=True, exist_ok=True)

    approved_clips = root / "wan" / "approved_clips"
    selected_audio = root / "audio" / "selected"

    missing = []
    exported_video = []
    exported_audio = []

    for i, shot in enumerate(shots, 1):
        clip_name = f"{shot.shot_id}_APPROVED.mp4"
        src = approved_clips / clip_name
        if src.exists():
            dst = video_dir / resolve_video_filename(i, shot.shot_id)
            shutil.copy2(src, dst)
            exported_video.append(dst.name)
            logger.info(f"Exported video: {dst.name}")
        else:
            missing.append(f"VIDEO: {clip_name}")

    audio_selected = root / "audio" / "selected"
    if audio_selected.exists():
        for i, wav in enumerate(sorted(audio_selected.glob("*.wav")), 1):
            dst = dialogue_dir / f"{i:03d}_{wav.name}"
            shutil.copy2(wav, dst)
            exported_audio.append(dst.name)

    _write_cue_sheet(shots, cue_dir, episode)
    _write_edit_guide(shots, guide_dir, episode)
    _write_missing_report(missing, resolve_dir)

    logger.info(f"Resolve export complete: {len(exported_video)} clips, {len(exported_audio)} audio")
    return {"video": exported_video, "audio": exported_audio, "missing": missing}


def _write_cue_sheet(shots: list[Shot], cue_dir: Path, episode: str):
    csv_path = cue_dir / f"{episode}_cue_sheet.csv"
    json_path = cue_dir / f"{episode}_cue_sheet.json"

    rows = []
    for i, shot in enumerate(shots, 1):
        rows.append({
            "order": i,
            "shot_id": shot.shot_id,
            "title": shot.title,
            "duration_target": shot.duration_target_seconds,
            "characters": "|".join(shot.characters),
            "status": shot.status,
        })

    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({"episode": episode, "cues": rows}, f, indent=2)


def _write_edit_guide(shots: list[Shot], guide_dir: Path, episode: str):
    path = guide_dir / f"{episode}_edit_guide.md"
    lines = [f"# {episode.upper()} — Edit Guide\n"]
    lines.append("## Shot Order\n")

    for i, shot in enumerate(shots, 1):
        lines.append(f"### {i}. {shot.shot_id} — {shot.title}")
        lines.append(f"- Duration: ~{shot.duration_target_seconds}s")
        lines.append(f"- Camera: {shot.camera}")
        lines.append(f"- Action: {shot.primary_action}")
        if shot.characters:
            lines.append(f"- Characters: {', '.join(shot.characters)}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def _write_missing_report(missing: list[str], resolve_dir: Path):
    path = resolve_dir / "MISSING_ASSETS.txt"
    if missing:
        path.write_text("MISSING ASSETS FOR RESOLVE EXPORT\n\n" + "\n".join(missing), encoding="utf-8")
    elif path.exists():
        path.unlink()
