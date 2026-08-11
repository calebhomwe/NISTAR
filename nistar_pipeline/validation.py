"""Validation utilities for WAN inputs and pipeline state."""

from pathlib import Path
from typing import Optional

from .config import get_project_root, load_wan_config, load_character_refs
from .models import Shot


class ValidationResult:
    def __init__(self):
        self.errors: list[str] = []
        self.warnings: list[str] = []

    @property
    def ok(self) -> bool:
        return len(self.errors) == 0

    def error(self, msg: str):
        self.errors.append(msg)

    def warn(self, msg: str):
        self.warnings.append(msg)

    def summary(self) -> str:
        lines = []
        if self.errors:
            lines.append(f"ERRORS ({len(self.errors)}):")
            for e in self.errors:
                lines.append(f"  [ERROR] {e}")
        if self.warnings:
            lines.append(f"WARNINGS ({len(self.warnings)}):")
            for w in self.warnings:
                lines.append(f"  [WARN] {w}")
        if self.ok and not self.warnings:
            lines.append("ALL CHECKS PASSED")
        return "\n".join(lines)


def validate_shot_input(shot: Shot) -> ValidationResult:
    result = ValidationResult()
    root = get_project_root()
    wan_cfg = load_wan_config()

    if not shot.shot_id:
        result.error("Shot has no shot_id")
        return result

    if shot.generation_mode == "image_to_video":
        if not shot.input_image:
            result.error(f"{shot.shot_id}: No input_image specified")
        else:
            img_path = root / shot.input_image
            if not img_path.exists():
                result.error(f"{shot.shot_id}: Input image not found: {shot.input_image}")
            else:
                _check_image_dimensions(img_path, shot.shot_id, wan_cfg, result)

    if not shot.positive_prompt:
        result.error(f"{shot.shot_id}: No positive prompt")

    if not shot.negative_prompt:
        result.warn(f"{shot.shot_id}: No negative prompt (will use global)")

    if not shot.characters and shot.generation_mode == "image_to_video":
        result.warn(f"{shot.shot_id}: No characters listed")

    return result


def validate_all_shots(shots: list[Shot]) -> ValidationResult:
    result = ValidationResult()
    seen_ids = set()
    for shot in shots:
        if shot.shot_id in seen_ids:
            result.error(f"Duplicate shot_id: {shot.shot_id}")
        seen_ids.add(shot.shot_id)
        sr = validate_shot_input(shot)
        result.errors.extend(sr.errors)
        result.warnings.extend(sr.warnings)
    return result


def validate_character_refs() -> ValidationResult:
    result = ValidationResult()
    root = get_project_root()
    chars = load_character_refs().get("characters", {})

    for name, data in chars.items():
        ref = data.get("canonical_reference", "")
        if not ref:
            result.error(f"Character '{name}': No canonical reference path")
        else:
            if not (root / ref).exists():
                result.warn(f"Character '{name}': Reference image missing: {ref}")

    return result


def _check_image_dimensions(
    path: Path, shot_id: str, wan_cfg: dict, result: ValidationResult
):
    try:
        from PIL import Image
        img = Image.open(path)
        w, h = img.size
        target_w = wan_cfg.get("generation", {}).get("width", 832)
        target_h = wan_cfg.get("generation", {}).get("height", 480)
        if w != target_w or h != target_h:
            result.warn(
                f"{shot_id}: Image is {w}x{h}, target is {target_w}x{target_h} — will need crop/resize"
            )
    except ImportError:
        result.warn(f"{shot_id}: Pillow not installed, cannot check image dimensions")
    except Exception as e:
        result.warn(f"{shot_id}: Could not read image: {e}")
