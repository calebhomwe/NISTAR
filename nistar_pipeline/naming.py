"""Deterministic naming conventions for all pipeline outputs."""

import re
from pathlib import Path


def sanitize(name: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]", "_", name).strip("_")


def shot_filename(shot_id: str, take: int, ext: str = ".mp4") -> str:
    return f"{shot_id}_TAKE{take:02d}{ext}"


def input_frame_filename(shot_id: str) -> str:
    return f"{shot_id}_input.png"


def prompt_filename(shot_id: str, title: str = "") -> str:
    slug = sanitize(title) if title else ""
    if slug:
        return f"{shot_id}_{slug}_WAN22MAX.txt"
    return f"{shot_id}_WAN22MAX.txt"


def dialogue_filename(
    episode: str, scene: str, character: str, line_id: str, take: int
) -> str:
    return f"{episode}_{scene}_{character}_{line_id}_TAKE{take:02d}.wav"


def sfx_filename(episode: str, scene: str, sfx_id: str, take: int) -> str:
    return f"{episode}_{scene}_{sfx_id}_TAKE{take:02d}.wav"


def contact_sheet_filename(shot_id: str) -> str:
    return f"{shot_id}_contact_sheet.png"


def approved_clip_filename(shot_id: str, ext: str = ".mp4") -> str:
    return f"{shot_id}_APPROVED{ext}"


def resolve_video_filename(index: int, shot_id: str) -> str:
    return f"{index:03d}_{shot_id}.mp4"


def resolve_dialogue_filename(index: int, line_id: str) -> str:
    return f"{index:03d}_{line_id}.wav"
