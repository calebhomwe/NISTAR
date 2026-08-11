"""Unpack the NISTAR E01 ElevenLabs Drop-In Package ZIP."""

import sys
import shutil
import zipfile
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.config import get_project_root


def main():
    parser = argparse.ArgumentParser(description="Unpack audio source package")
    parser.add_argument("--zip", help="Path to ZIP file (auto-detected if not given)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    dest = root / "source" / "original_audio_package"

    # Find ZIP
    zip_path = None
    if args.zip:
        zip_path = Path(args.zip)
    else:
        # Search common locations
        search_paths = [
            root,
            Path.home() / "Downloads",
            Path.home() / "Desktop",
        ]
        for loc in search_paths:
            candidates = list(loc.glob("*NISTAR*ElevenLabs*DropIn*.zip"))
            if candidates:
                zip_path = candidates[0]
                break

    if not zip_path or not zip_path.exists():
        print("ERROR: Cannot find NISTAR_E01_ElevenLabs_DropIn_Package.zip")
        print("Provide path with --zip or place in Downloads/Desktop")
        return

    print(f"Found package: {zip_path}")
    print(f"Destination: {dest}")

    if args.dry_run:
        with zipfile.ZipFile(zip_path) as zf:
            print(f"\nContents ({len(zf.namelist())} files):")
            for name in sorted(zf.namelist())[:20]:
                print(f"  {name}")
            if len(zf.namelist()) > 20:
                print(f"  ... and {len(zf.namelist()) - 20} more")
        return

    # Unpack
    dest.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(dest)

    # Count extracted files
    extracted = list(dest.rglob("*"))
    files = [f for f in extracted if f.is_file()]
    print(f"Extracted: {len(files)} files")

    # Copy to working directories
    _organize_audio_files(dest, root)


def _organize_audio_files(source_dir: Path, root: Path):
    """Sort extracted audio into dialogue/sfx working directories."""
    dialogue_dir = root / "source" / "dialogue"
    sfx_dir = root / "source" / "sfx_prompts"
    dialogue_dir.mkdir(parents=True, exist_ok=True)
    sfx_dir.mkdir(parents=True, exist_ok=True)

    audio_files = list(source_dir.rglob("*.wav")) + list(source_dir.rglob("*.mp3"))
    text_files = list(source_dir.rglob("*.txt")) + list(source_dir.rglob("*.json")) + list(source_dir.rglob("*.yaml"))

    for f in audio_files:
        shutil.copy2(f, dialogue_dir / f.name)

    for f in text_files:
        target = sfx_dir if "sfx" in f.name.lower() else dialogue_dir
        shutil.copy2(f, target / f.name)

    print(f"Organized: {len(audio_files)} audio, {len(text_files)} text files")


if __name__ == "__main__":
    main()
