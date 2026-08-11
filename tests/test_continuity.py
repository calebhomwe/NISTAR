"""Tests for continuity checking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import Shot
from nistar_pipeline.continuity import (
    check_continuity_warnings, build_review_checklist,
    is_valid_rejection, REJECTION_REASONS
)


def test_unknown_character_warns():
    shot = Shot(
        shot_id="TEST_001",
        characters=["unknown_person"],
    )
    warnings = check_continuity_warnings(shot)
    assert any("not in character_refs" in w for w in warnings)


def test_vehicle_warning():
    shot = Shot(
        shot_id="TEST_002",
        characters=["ren"],
        vehicle="R34 GTR",
    )
    warnings = check_continuity_warnings(shot)
    assert any("R34" in w for w in warnings)


def test_checklist_has_character_items():
    shot = Shot(
        shot_id="TEST_003",
        characters=["ren"],
    )
    checklist = build_review_checklist(shot)
    assert any("identity" in item.lower() for item in checklist)
    assert any("hair" in item.lower() for item in checklist)


def test_checklist_has_vehicle_items():
    shot = Shot(
        shot_id="TEST_004",
        characters=["ren"],
        vehicle="R34",
    )
    checklist = build_review_checklist(shot)
    assert any("vehicle" in item.lower() for item in checklist)


def test_valid_rejections():
    assert is_valid_rejection("face_drift")
    assert is_valid_rejection("orange_purple_wash")
    assert not is_valid_rejection("invalid_reason")


def test_rejection_reasons_complete():
    assert len(REJECTION_REASONS) >= 15


if __name__ == "__main__":
    test_unknown_character_warns()
    print("  PASS: test_unknown_character_warns")
    test_vehicle_warning()
    print("  PASS: test_vehicle_warning")
    test_checklist_has_character_items()
    print("  PASS: test_checklist_has_character_items")
    test_checklist_has_vehicle_items()
    print("  PASS: test_checklist_has_vehicle_items")
    test_valid_rejections()
    print("  PASS: test_valid_rejections")
    test_rejection_reasons_complete()
    print("  PASS: test_rejection_reasons_complete")
    print("\nAll continuity tests passed")
