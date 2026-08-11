"""Tests for naming conventions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.naming import (
    shot_filename, input_frame_filename, prompt_filename,
    dialogue_filename, sfx_filename, contact_sheet_filename,
    approved_clip_filename, resolve_video_filename, sanitize
)


def test_shot_filename():
    assert shot_filename("E01_SH001", 1) == "E01_SH001_TAKE01.mp4"
    assert shot_filename("E01_SH008A", 3, ".webm") == "E01_SH008A_TAKE03.webm"


def test_input_frame_filename():
    assert input_frame_filename("E01_SH001") == "E01_SH001_input.png"


def test_prompt_filename():
    assert prompt_filename("E01_SH008A", "Guardian Reveal") == "E01_SH008A_Guardian_Reveal_WAN22MAX.txt"
    assert prompt_filename("E01_SH001") == "E01_SH001_WAN22MAX.txt"


def test_dialogue_filename():
    result = dialogue_filename("E01", "SC01", "REN", "001", 2)
    assert result == "E01_SC01_REN_001_TAKE02.wav"


def test_sfx_filename():
    result = sfx_filename("E01", "SC05", "SFX007", 1)
    assert result == "E01_SC05_SFX007_TAKE01.wav"


def test_contact_sheet():
    assert contact_sheet_filename("E01_SH008A") == "E01_SH008A_contact_sheet.png"


def test_approved_clip():
    assert approved_clip_filename("E01_SH001") == "E01_SH001_APPROVED.mp4"
    assert approved_clip_filename("E01_SH001", ".webm") == "E01_SH001_APPROVED.webm"


def test_resolve_video():
    assert resolve_video_filename(1, "E01_SH001") == "001_E01_SH001.mp4"
    assert resolve_video_filename(15, "E01_SH015") == "015_E01_SH015.mp4"


def test_sanitize():
    assert sanitize("Guardian Reveal") == "Guardian_Reveal"
    assert sanitize("test/bad:chars") == "test_bad_chars"


if __name__ == "__main__":
    tests = [v for k, v in list(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"  PASS: {t.__name__}")
    print(f"\nAll {len(tests)} naming tests passed")
