"""Generate dialogue audio via ElevenLabs API."""

import sys
import re
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.audio import AudioGenerator
from nistar_pipeline.models import DialogueLine
from nistar_pipeline.config import get_project_root, load_audio_config


def main():
    parser = argparse.ArgumentParser(description="Generate dialogue via ElevenLabs")
    parser.add_argument("--scene", help="Generate single scene")
    parser.add_argument("--character", help="Generate single character")
    parser.add_argument("--line", help="Generate single line by ID")
    parser.add_argument("--lang", default="en", choices=["en", "jp"],
                        help="Language track: en (default) or jp (Japanese dub)")
    parser.add_argument("--dry-run", action="store_true", help="Print without calling API")
    args = parser.parse_args()

    root = get_project_root()
    audio_cfg = load_audio_config()

    lines = _load_dialogue_lines(root, args.lang)
    if not lines:
        print("No dialogue lines found. Check source/dialogue/ for script files.")
        print("Expected: JSON or YAML files with dialogue entries.")
        return

    # Filter
    if args.scene:
        lines = [l for l in lines if l.scene == args.scene]
    if args.character:
        lines = [l for l in lines if l.character.lower() == args.character.lower()]
    if args.line:
        lines = [l for l in lines if l.line_id == args.line]

    if not lines:
        print("No matching lines found with given filters")
        return

    # Mark critical lines
    critical_ids = set(audio_cfg.get("critical_lines", []))
    for line in lines:
        if line.line_id in critical_ids:
            line.is_critical = True

    print(f"Generating {len(lines)} dialogue lines [{args.lang.upper()}]")
    critical_count = sum(1 for l in lines if l.is_critical)
    if critical_count:
        print(f"  ({critical_count} critical lines — extra takes)")

    generator = AudioGenerator(dry_run=args.dry_run, lang=args.lang)
    total_generated = 0

    for line in lines:
        outputs = generator.generate_dialogue(line)
        total_generated += len(outputs)

    print(f"\nDone. Generated {total_generated} audio files.")
    if args.dry_run:
        print("(Dry run — no API calls made)")


_EMOTION_RE = re.compile(r"\[[^\]]*\]")

# Master file (one entry per line, carries scene) preferred over per-scene files
_MASTER_FILE = "NISTAR_E01_PRIDE_TEXT_TO_DIALOGUE_API.json"
_MASTER_FILE_JP = "NISTAR_E01_PRIDE_JP_API.json"


def _strip_emotion(text: str) -> tuple:
    """Remove bracketed stage directions so they are not spoken aloud.

    eleven_multilingual_v2 reads '[quietly]' literally, so we pull the
    bracketed tags out into the emotion field and clean the spoken text.
    """
    tags = _EMOTION_RE.findall(text or "")
    clean = _EMOTION_RE.sub("", text or "")
    clean = re.sub(r"\s+", " ", clean).strip()
    emotion = ", ".join(t.strip("[] ") for t in tags)
    return clean, emotion


def _entry_to_line(entry: dict, scene_hint: str = "") -> DialogueLine:
    line_id = entry.get("line_id", "")
    speaker = entry.get("speaker_id") or entry.get("character") or ""
    scene = entry.get("scene") or scene_hint
    text, emotion = _strip_emotion(entry.get("text", ""))
    episode = line_id.split("_")[0] if line_id[:1] == "E" else "E01"
    return DialogueLine(
        line_id=line_id,
        episode=episode,
        scene=scene,
        character=speaker,
        text=text,
        emotion=emotion,
    )


def _load_dialogue_lines(root, lang="en") -> list:
    """Load dialogue lines from the NISTAR package JSON for the given language.

    Prefers the single master API file (one entry per line, with scene) so
    the per-scene files don't produce duplicates. Falls back to per-scene
    JSON files if the master is absent.
    """
    if lang == "jp":
        dlg = root / "source" / "dialogue_jp"
        master_name = _MASTER_FILE_JP
    else:
        dlg = root / "source" / "dialogue"
        master_name = _MASTER_FILE
    lines = []

    master = dlg / master_name
    if master.exists():
        try:
            data = json.load(open(master, encoding="utf-8"))
            for e in data:
                if e.get("text"):
                    lines.append(_entry_to_line(e))
            if lines:
                return lines
        except Exception as ex:
            print(f"Warning: could not parse master file: {ex}")

    for f in sorted(dlg.glob("*.json")):
        if f.name == master_name or "API" in f.name:
            continue
        try:
            data = json.load(open(f, encoding="utf-8"))
            if isinstance(data, list):
                for e in data:
                    if e.get("text"):
                        lines.append(_entry_to_line(e, scene_hint=f.stem))
        except Exception as ex:
            print(f"Warning: could not parse {f.name}: {ex}")

    return lines


if __name__ == "__main__":
    main()
