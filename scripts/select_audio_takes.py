"""Select preferred audio takes for final assembly."""

import sys
import shutil
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.config import get_project_root


def main():
    parser = argparse.ArgumentParser(description="Select audio takes")
    parser.add_argument("--line", required=True, help="Line ID pattern to match")
    parser.add_argument("--take", required=True, type=int, help="Take number to select")
    parser.add_argument("--type", choices=["dialogue", "sfx"], default="dialogue")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    source_dir = root / "audio" / args.type
    selected_dir = root / "audio" / "selected"
    selected_dir.mkdir(parents=True, exist_ok=True)

    # Find matching files
    pattern = f"*{args.line}*TAKE{args.take:02d}*"
    matches = list(source_dir.glob(pattern))

    if not matches:
        print(f"No files matching: {pattern}")
        print(f"  Searched: {source_dir}")
        # Show available
        all_takes = list(source_dir.glob(f"*{args.line}*"))
        if all_takes:
            print(f"  Available: {[f.name for f in all_takes]}")
        return

    for match in matches:
        dest = selected_dir / match.name
        if args.dry_run:
            print(f"[DRY-RUN] Would select: {match.name}")
        else:
            shutil.copy2(match, dest)
            print(f"Selected: {match.name} → audio/selected/")


if __name__ == "__main__":
    main()
