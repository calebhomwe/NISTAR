"""Export approved assets for DaVinci Resolve."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.resolve_export import export_for_resolve


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Export for DaVinci Resolve")
    parser.add_argument("--episode", default="episode_01")
    args = parser.parse_args()

    result = export_for_resolve(args.episode)
    print(f"\nExport complete:")
    print(f"  Video: {len(result['video'])} clips")
    print(f"  Audio: {len(result['audio'])} clips")
    if result['missing']:
        print(f"  Missing: {len(result['missing'])} assets")
        for m in result['missing']:
            print(f"    - {m}")


if __name__ == "__main__":
    main()
