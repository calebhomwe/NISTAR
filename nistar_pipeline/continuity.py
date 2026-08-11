"""Continuity checking for character and vehicle consistency."""

from pathlib import Path
from typing import Optional

from .config import get_project_root, load_character_refs
from .models import Shot, Take
from .logging_utils import get_logger

logger = get_logger("continuity")

REJECTION_REASONS = [
    "face_drift",
    "hair_drift",
    "outfit_change",
    "age_change",
    "vehicle_model_change",
    "warped_vehicle",
    "melted_wheels",
    "extra_fingers",
    "unstable_eyes",
    "excessive_mouth",
    "random_camera",
    "colour_shift",
    "cgi_drift",
    "photorealistic_drift",
    "painterly_drift",
    "excessive_glow",
    "orange_purple_wash",
    "text_watermark",
]


def check_continuity_warnings(shot: Shot) -> list[str]:
    warnings = []
    chars = load_character_refs().get("characters", {})

    for char_name in shot.characters:
        char_data = chars.get(char_name.lower())
        if not char_data:
            warnings.append(f"Character '{char_name}' not in character_refs.yaml")
            continue

        ref_path = char_data.get("canonical_reference", "")
        if ref_path and not (get_project_root() / ref_path).exists():
            warnings.append(f"Missing canonical reference for {char_name}: {ref_path}")

    if shot.vehicle and "r34" in shot.vehicle.lower():
        warnings.append("R34 shots: verify body lines, wheel count, spoiler shape match reference")

    return warnings


def build_review_checklist(shot: Shot) -> list[str]:
    checklist = []

    if shot.characters:
        checklist.append("[ ] Character identity matches reference")
        checklist.append("[ ] Hair colour and style consistent")
        checklist.append("[ ] Outfit matches shot description")
        checklist.append("[ ] Eye colour correct")
        checklist.append("[ ] No age regression/progression")

    if shot.vehicle:
        checklist.append("[ ] Vehicle model consistent")
        checklist.append("[ ] No body deformation")
        checklist.append("[ ] Correct wheel count and shape")

    checklist.append("[ ] Single camera movement only")
    checklist.append("[ ] No excessive mouth animation")
    checklist.append("[ ] Colour within style bible range")
    checklist.append("[ ] No text/watermark/logo")
    checklist.append("[ ] No CGI/photorealistic drift")
    checklist.append("[ ] No orange-purple wash")

    return checklist


def is_valid_rejection(reason: str) -> bool:
    return reason in REJECTION_REASONS
