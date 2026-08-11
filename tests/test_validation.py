"""Tests for validation utilities."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import Shot
from nistar_pipeline.validation import validate_shot_input, validate_all_shots, ValidationResult


def test_missing_shot_id():
    shot = Shot(shot_id="")
    result = validate_shot_input(shot)
    assert not result.ok
    assert any("no shot_id" in e for e in result.errors)


def test_i2v_missing_image():
    shot = Shot(
        shot_id="E01_SH001",
        generation_mode="image_to_video",
        input_image="",
        positive_prompt="test",
    )
    result = validate_shot_input(shot)
    assert not result.ok
    assert any("No input_image" in e for e in result.errors)


def test_missing_prompt():
    shot = Shot(
        shot_id="E01_SH001",
        generation_mode="text_to_video",
        positive_prompt="",
    )
    result = validate_shot_input(shot)
    assert not result.ok
    assert any("No positive prompt" in e for e in result.errors)


def test_valid_t2v_shot():
    shot = Shot(
        shot_id="E01_SH001",
        generation_mode="text_to_video",
        positive_prompt="A car driving",
        negative_prompt="bad quality",
    )
    result = validate_shot_input(shot)
    assert result.ok


def test_duplicate_ids():
    shots = [
        Shot(shot_id="E01_SH001", generation_mode="text_to_video", positive_prompt="test"),
        Shot(shot_id="E01_SH001", generation_mode="text_to_video", positive_prompt="test2"),
    ]
    result = validate_all_shots(shots)
    assert not result.ok
    assert any("Duplicate" in e for e in result.errors)


def test_validation_result_summary():
    r = ValidationResult()
    assert r.ok
    assert "PASSED" in r.summary()

    r.error("something broke")
    assert not r.ok
    assert "ERROR" in r.summary()


if __name__ == "__main__":
    test_missing_shot_id()
    print("  PASS: test_missing_shot_id")
    test_i2v_missing_image()
    print("  PASS: test_i2v_missing_image")
    test_missing_prompt()
    print("  PASS: test_missing_prompt")
    test_valid_t2v_shot()
    print("  PASS: test_valid_t2v_shot")
    test_duplicate_ids()
    print("  PASS: test_duplicate_ids")
    test_validation_result_summary()
    print("  PASS: test_validation_result_summary")
    print("\nAll validation tests passed")
