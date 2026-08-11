"""Select an approved take for a shot."""

import sys
import shutil
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest, save_shot_manifest, load_take_log, save_take_log
from nistar_pipeline.config import get_project_root
from nistar_pipeline.naming import approved_clip_filename


def main():
    parser = argparse.ArgumentParser(description="Select a WAN take as approved")
    parser.add_argument("--shot", required=True, help="Shot ID (e.g. E01_SH008A)")
    parser.add_argument("--take", required=True, type=int, help="Take number to approve")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--note", default="", help="Optional note")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    takes = load_take_log(args.shot)

    if not takes:
        print(f"No takes found for {args.shot}")
        return

    selected = None
    for t in takes:
        if t.take_number == args.take:
            selected = t
            break

    if not selected:
        print(f"Take {args.take} not found for {args.shot}")
        print(f"Available takes: {[t.take_number for t in takes]}")
        return

    src = root / "wan" / "output_clips" / args.shot / selected.filename
    if not src.exists():
        print(f"Take file not found: {src}")
        return

    approved_dir = root / "wan" / "approved_clips"
    approved_name = approved_clip_filename(args.shot, src.suffix)
    dest = approved_dir / approved_name

    if args.dry_run:
        print(f"[DRY-RUN] Would approve: {args.shot} TAKE{args.take:02d}")
        print(f"  Source: {src}")
        print(f"  Dest: {dest}")
        return

    # Mark selected
    for t in takes:
        t.selected = (t.take_number == args.take)
    save_take_log(args.shot, takes)

    # Copy to approved
    approved_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)

    # Update manifest
    shots = load_shot_manifest(args.episode)
    for shot in shots:
        if shot.shot_id == args.shot:
            shot.status = "approved"
            shot.approved_take = approved_name
            shot.notes = args.note if args.note else shot.notes
            break
    save_shot_manifest(shots, args.episode)

    print(f"APPROVED: {args.shot} TAKE{args.take:02d}")
    print(f"  → {dest}")
    if args.note:
        print(f"  Note: {args.note}")


if __name__ == "__main__":
    main()
