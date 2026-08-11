"""Build animatic package — approved clips + placeholder stills + audio."""

import sys
import shutil
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest
from nistar_pipeline.config import get_project_root


def main():
    parser = argparse.ArgumentParser(description="Build animatic assembly package")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    shots = load_shot_manifest(args.episode)

    if not shots:
        print("No shots in manifest")
        return

    animatic_dir = root / "davinci" / args.episode / "video"
    animatic_dir.mkdir(parents=True, exist_ok=True)

    approved_dir = root / "wan" / "approved_clips"
    input_frames = root / "wan" / "input_frames"

    manifest_lines = ["# Animatic Assembly Manifest\n"]
    manifest_lines.append("| # | Shot | Source | Duration | Type |")
    manifest_lines.append("|---|------|--------|----------|------|")

    for i, shot in enumerate(shots, 1):
        approved_clip = approved_dir / f"{shot.shot_id}_APPROVED.mp4"
        input_still = input_frames / f"{shot.shot_id}_input.png"

        if approved_clip.exists():
            source = approved_clip
            stype = "VIDEO (approved)"
        elif input_still.exists():
            source = input_still
            stype = "STILL (placeholder)"
        else:
            source = None
            stype = "MISSING"

        if args.dry_run:
            manifest_lines.append(f"| {i} | {shot.shot_id} | {stype} | {shot.duration_target_seconds}s | {shot.title} |")
            continue

        if source:
            dest = animatic_dir / f"{i:03d}_{shot.shot_id}{source.suffix}"
            shutil.copy2(source, dest)

        manifest_lines.append(f"| {i} | {shot.shot_id} | {stype} | {shot.duration_target_seconds}s | {shot.title} |")

    # Audio
    audio_selected = root / "audio" / "selected"
    audio_list = list(audio_selected.glob("*.wav")) if audio_selected.exists() else []

    manifest_lines.append(f"\n## Audio: {len(audio_list)} selected clips")

    # Write manifest
    manifest_path = root / "davinci" / args.episode / "edit_guides" / "animatic_manifest.md"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text("\n".join(manifest_lines), encoding="utf-8")

    approved_count = sum(1 for s in shots if s.status == "approved")
    print(f"Animatic package: {animatic_dir}")
    print(f"  Approved clips: {approved_count}/{len(shots)}")
    print(f"  Still placeholders: {len(shots) - approved_count}")
    print(f"  Audio clips: {len(audio_list)}")
    print(f"  Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
