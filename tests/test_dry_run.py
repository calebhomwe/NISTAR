"""Integration test — full dry-run pipeline without API calls."""

import sys
import tempfile
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.models import Shot
from nistar_pipeline.manifests import save_shot_manifest, load_shot_manifest
from nistar_pipeline.wan import export_prompt_file, build_full_positive, build_full_negative, detect_comfyui
from nistar_pipeline.validation import validate_shot_input


def test_full_dry_run():
    """Full pipeline dry run — manifest → prompts → validation."""
    tmp = Path(tempfile.mkdtemp())
    real_root = Path(__file__).resolve().parent.parent

    # Copy config to tmp so load_yaml works
    import shutil
    (tmp / "config").mkdir(parents=True, exist_ok=True)
    for cfg in (real_root / "config").glob("*.yaml"):
        shutil.copy2(cfg, tmp / "config" / cfg.name)

    # Monkey-patch
    import nistar_pipeline.manifests as m
    import nistar_pipeline.config as c
    import nistar_pipeline.wan as w
    orig_root_m = m.get_project_root
    orig_root_c = c.get_project_root
    orig_root_w = w.get_project_root if hasattr(w, 'get_project_root') else None
    m.get_project_root = lambda: tmp
    c.get_project_root = lambda: tmp

    # Create manifest
    shots = [
        Shot(
            shot_id="E01_TEST001",
            scene="SC01",
            title="Test Shot",
            generation_mode="text_to_video",
            positive_prompt="A test scene for validation",
            negative_prompt="bad quality",
            characters=["ren"],
        ),
    ]
    (tmp / "wan" / "manifests").mkdir(parents=True, exist_ok=True)
    save_shot_manifest(shots, "episode_01")

    # Load back
    loaded = load_shot_manifest("episode_01")
    assert len(loaded) == 1
    assert loaded[0].shot_id == "E01_TEST001"

    # Export prompt
    prompt_dir = tmp / "wan" / "prompts" / "episode_01"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    path = export_prompt_file(loaded[0], prompt_dir)
    assert path.exists()
    content = path.read_text()
    assert "TEXT TO VIDEO" in content
    assert "WAN 2.2 MAX" in content
    assert "test scene" in content.lower()

    # Build full prompts
    pos = build_full_positive(loaded[0])
    neg = build_full_negative(loaded[0])
    assert "seinen" in pos.lower()
    assert "photorealistic" in neg.lower()

    # Validate
    result = validate_shot_input(loaded[0])
    assert result.ok  # t2v doesn't need input image

    # Restore
    m.get_project_root = orig_root_m
    c.get_project_root = orig_root_c


def test_comfyui_detection():
    """ComfyUI detection should not crash."""
    result = detect_comfyui()
    # May or may not be running — just ensure no exception
    assert result is None or isinstance(result, str)


if __name__ == "__main__":
    test_full_dry_run()
    print("  PASS: test_full_dry_run")
    test_comfyui_detection()
    print("  PASS: test_comfyui_detection")
    print("\nAll dry-run integration tests passed")
