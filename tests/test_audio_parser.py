"""Tests for audio pipeline."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import DialogueLine, SFXEntry
from nistar_pipeline.audio import AudioGenerator


def test_dry_run_dialogue():
    """Dry run should not call API."""
    gen = AudioGenerator(dry_run=True)
    line = DialogueLine(
        line_id="TEST_001",
        episode="E01",
        scene="SC01",
        character="ren",
        text="I always make it.",
    )
    outputs = gen.generate_dialogue(line)
    assert len(outputs) == 3  # normal_takes default


def test_dry_run_critical():
    """Critical lines get more takes."""
    gen = AudioGenerator(dry_run=True)
    line = DialogueLine(
        line_id="TEST_002",
        episode="E01",
        scene="SC01",
        character="ren",
        text="Critical line.",
        is_critical=True,
    )
    outputs = gen.generate_dialogue(line)
    assert len(outputs) == 5  # critical_takes default


def test_dry_run_sfx():
    """SFX dry run."""
    gen = AudioGenerator(dry_run=True)
    entry = SFXEntry(
        sfx_id="SFX001",
        episode="E01",
        scene="SC01",
        description="Car engine revving",
        duration_seconds=4,
    )
    outputs = gen.generate_sfx(entry)
    assert len(outputs) == 3


if __name__ == "__main__":
    test_dry_run_dialogue()
    print("  PASS: test_dry_run_dialogue")
    test_dry_run_critical()
    print("  PASS: test_dry_run_critical")
    test_dry_run_sfx()
    print("  PASS: test_dry_run_sfx")
    print("\nAll audio parser tests passed")
