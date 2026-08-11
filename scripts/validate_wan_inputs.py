"""Validate all WAN inputs — stills, prompts, character refs, dimensions."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest
from nistar_pipeline.validation import validate_all_shots, validate_character_refs
from nistar_pipeline.config import get_project_root, load_wan_config


def main():
    parser = argparse.ArgumentParser(description="Validate WAN inputs")
    parser.add_argument("--episode", default="episode_01")
    args = parser.parse_args()

    root = get_project_root()
    print("=" * 60)
    print("NISTAR WAN INPUT VALIDATION")
    print("=" * 60)

    # 1. Check manifest exists
    shots = load_shot_manifest(args.episode)
    if not shots:
        print("\n[ERROR] No shot manifest found. Run build_wan_manifest.py first.")
        return

    print(f"\nManifest: {len(shots)} shots loaded")

    # 2. Validate all shots
    print("\n--- Shot Validation ---")
    result = validate_all_shots(shots)
    print(result.summary())

    # 3. Character refs
    print("\n--- Character Reference Validation ---")
    char_result = validate_character_refs()
    print(char_result.summary())

    # 4. Check input frames directory
    print("\n--- Input Frames Check ---")
    input_dir = root / "wan" / "input_frames"
    i2v_shots = [s for s in shots if s.generation_mode == "image_to_video"]
    existing = set(f.stem for f in input_dir.glob("*.png")) if input_dir.exists() else set()

    missing_frames = []
    for shot in i2v_shots:
        expected = f"{shot.shot_id}_input"
        if expected not in existing:
            missing_frames.append(shot.shot_id)

    if missing_frames:
        print(f"  [WARN] {len(missing_frames)} shots missing input frames:")
        for sid in missing_frames:
            print(f"    - {sid}")
    else:
        print(f"  ALL {len(i2v_shots)} input frames present")

    # 5. Check prompt files
    print("\n--- Prompt Files Check ---")
    prompt_dir = root / "wan" / "prompts" / args.episode
    existing_prompts = set(f.stem.split("_WAN22MAX")[0] for f in prompt_dir.glob("*_WAN22MAX.txt")) if prompt_dir.exists() else set()

    missing_prompts = []
    for shot in shots:
        # The prompt filename uses shot_id + title, check if any file starts with shot_id
        found = any(shot.shot_id in p for p in existing_prompts)
        if not found:
            missing_prompts.append(shot.shot_id)

    if missing_prompts:
        print(f"  [WARN] {len(missing_prompts)} shots missing prompt files:")
        for sid in missing_prompts[:5]:
            print(f"    - {sid}")
        if len(missing_prompts) > 5:
            print(f"    ... and {len(missing_prompts) - 5} more")
        print("  Run export_wan_prompts.py to generate them.")
    else:
        print(f"  ALL {len(shots)} prompt files present")

    # 6. Check for duplicates
    print("\n--- Duplicate Check ---")
    ids = [s.shot_id for s in shots]
    dupes = [x for x in ids if ids.count(x) > 1]
    if dupes:
        print(f"  [ERROR] Duplicate shot IDs: {set(dupes)}")
    else:
        print("  No duplicates found")

    # 7. Summary
    total_errors = len(result.errors) + len(char_result.errors)
    total_warnings = len(result.warnings) + len(char_result.warnings) + len(missing_frames) + len(missing_prompts)
    print(f"\n{'='*60}")
    print(f"SUMMARY: {total_errors} errors, {total_warnings} warnings")
    if total_errors == 0:
        print("Ready for generation (resolve warnings for best results)")
    else:
        print("FIX ERRORS before generating")


if __name__ == "__main__":
    main()
