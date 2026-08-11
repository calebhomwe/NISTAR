"""Generate sound effects via ElevenLabs API."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.audio import AudioGenerator
from nistar_pipeline.models import SFXEntry
from nistar_pipeline.config import get_project_root


def main():
    parser = argparse.ArgumentParser(description="Generate SFX via ElevenLabs")
    parser.add_argument("--scene", help="Generate SFX for single scene")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    sfx_path = root / "source" / "sfx_prompts"

    entries = _load_sfx_entries(sfx_path)
    if not entries:
        print("No SFX entries found. Add prompts to source/sfx_prompts/")
        print("Expected: JSON file with sfx entries")
        _create_example_sfx(sfx_path)
        return

    if args.scene:
        entries = [e for e in entries if e.scene == args.scene]

    print(f"Generating {len(entries)} SFX entries")

    generator = AudioGenerator(dry_run=args.dry_run)
    total = 0

    for entry in entries:
        outputs = generator.generate_sfx(entry)
        total += len(outputs)

    print(f"\nDone. Generated {total} SFX files.")
    if args.dry_run:
        print("(Dry run — no API calls made)")


def _load_sfx_entries(sfx_path: Path) -> list:
    entries = []
    for f in sfx_path.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, list):
                for entry in data:
                    entries.append(SFXEntry(**entry))
            elif isinstance(data, dict) and "sfx" in data:
                for entry in data["sfx"]:
                    entries.append(SFXEntry(**entry))
        except Exception as e:
            print(f"Warning: Could not parse {f.name}: {e}")
    return entries


def _create_example_sfx(sfx_path: Path):
    """Create an example SFX prompts file."""
    sfx_path.mkdir(parents=True, exist_ok=True)
    example = {
        "sfx": [
            {"sfx_id": "SFX001", "episode": "E01", "scene": "SC01", "description": "Car engine revving, turbo whistle, low rumble", "duration_seconds": 4},
            {"sfx_id": "SFX002", "episode": "E01", "scene": "SC02", "description": "Metal crunching, glass shattering, car crash impact", "duration_seconds": 3},
            {"sfx_id": "SFX003", "episode": "E01", "scene": "SC03", "description": "Heavy rain on concrete, distant thunder", "duration_seconds": 5},
            {"sfx_id": "SFX004", "episode": "E01", "scene": "SC04", "description": "Television static hiss, energy drink can rolling on floor", "duration_seconds": 3},
            {"sfx_id": "SFX005", "episode": "E01", "scene": "SC05", "description": "Garage door opening mechanical, fluorescent light buzz and flicker", "duration_seconds": 4},
            {"sfx_id": "SFX006", "episode": "E01", "scene": "SC05", "description": "Fuel warning beep, dashboard electronics", "duration_seconds": 2},
            {"sfx_id": "SFX007", "episode": "E01", "scene": "SC05", "description": "Semi-truck horn blasting, air brake hiss, rain on windscreen", "duration_seconds": 4},
            {"sfx_id": "SFX008", "episode": "E01", "scene": "SC06", "description": "Tyre screech on wet concrete, drift slide, car stopping", "duration_seconds": 3},
            {"sfx_id": "SFX009", "episode": "E01", "scene": "SC06", "description": "Small puppy whimpering quietly", "duration_seconds": 3},
            {"sfx_id": "SFX010", "episode": "E01", "scene": "SC07", "description": "Wallet landing on wet pavement, small splash", "duration_seconds": 2},
        ]
    }
    out = sfx_path / "episode_01_sfx.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(example, f, indent=2)
    print(f"Created example: {out}")


if __name__ == "__main__":
    main()
