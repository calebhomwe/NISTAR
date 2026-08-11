"""Tests for WAN manifest building and loading."""

import sys
import json
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import Shot
from nistar_pipeline.manifests import save_shot_manifest, load_shot_manifest


def test_round_trip(tmp_path=None):
    """Shots survive save/load cycle."""
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())

    shots = [
        Shot(
            shot_id="E01_SH001",
            scene="SC01_DREAM",
            title="Dream Highway",
            generation_mode="image_to_video",
            characters=["ren"],
            positive_prompt="test prompt",
            negative_prompt="test negative",
        ),
        Shot(
            shot_id="E01_SH002",
            scene="SC01_DREAM",
            title="The Void",
            generation_mode="image_to_video",
            characters=["ren"],
        ),
    ]

    # Monkey-patch project root for test
    import nistar_pipeline.manifests as m
    original_root = m.get_project_root
    m.get_project_root = lambda: tmp_path

    (tmp_path / "wan" / "manifests").mkdir(parents=True, exist_ok=True)
    save_shot_manifest(shots, "episode_01")

    loaded = load_shot_manifest("episode_01")
    assert len(loaded) == 2
    assert loaded[0].shot_id == "E01_SH001"
    assert loaded[0].title == "Dream Highway"
    assert loaded[0].characters == ["ren"]
    assert loaded[1].shot_id == "E01_SH002"

    m.get_project_root = original_root


def test_empty_manifest(tmp_path=None):
    """Empty episode returns empty list."""
    if tmp_path is None:
        tmp_path = Path(tempfile.mkdtemp())

    import nistar_pipeline.manifests as m
    original_root = m.get_project_root
    m.get_project_root = lambda: tmp_path

    result = load_shot_manifest("nonexistent")
    assert result == []

    m.get_project_root = original_root


def test_shot_to_dict():
    shot = Shot(
        shot_id="E01_SH008A",
        title="Guardian Reveal",
        characters=["guardian"],
        secondary_motion=["rain", "coat movement"],
    )
    d = shot.to_dict()
    assert d["shot_id"] == "E01_SH008A"
    assert d["characters"] == ["guardian"]
    assert "rain" in d["secondary_motion"]


if __name__ == "__main__":
    test_round_trip()
    print("  PASS: test_round_trip")
    test_empty_manifest()
    print("  PASS: test_empty_manifest")
    test_shot_to_dict()
    print("  PASS: test_shot_to_dict")
    print("\nAll WAN manifest tests passed")
