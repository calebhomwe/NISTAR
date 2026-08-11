"""Validate the unpacked audio source package."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.config import get_project_root, load_voices


def main():
    root = get_project_root()
    source_dir = root / "source" / "original_audio_package"

    print("=" * 60)
    print("AUDIO SOURCE VALIDATION")
    print("=" * 60)

    if not source_dir.exists() or not list(source_dir.iterdir()):
        print("\n[ERROR] Audio package not unpacked yet.")
        print("Run: python scripts/unpack_audio_package.py")
        return

    # Count files
    all_files = list(source_dir.rglob("*"))
    files = [f for f in all_files if f.is_file()]
    audio = [f for f in files if f.suffix.lower() in (".wav", ".mp3", ".flac")]
    text = [f for f in files if f.suffix.lower() in (".txt", ".json", ".yaml", ".md")]

    print(f"\nTotal files: {len(files)}")
    print(f"  Audio: {len(audio)}")
    print(f"  Text/config: {len(text)}")
    print(f"  Other: {len(files) - len(audio) - len(text)}")

    # Check voice config
    voices = load_voices().get("voices", {})
    configured = sum(1 for v in voices.values() if v.get("voice_id"))
    print(f"\nVoice configuration:")
    print(f"  Characters defined: {len(voices)}")
    print(f"  Voice IDs set: {configured}/{len(voices)}")
    if configured < len(voices):
        missing = [k for k, v in voices.items() if not v.get("voice_id")]
        print(f"  Missing IDs: {', '.join(missing)}")

    # Check .env
    env_path = root / ".env"
    if env_path.exists():
        content = env_path.read_text()
        if "ELEVENLABS_API_KEY=" in content and content.split("ELEVENLABS_API_KEY=")[1].strip():
            print("\n[OK] ElevenLabs API key configured")
        else:
            print("\n[WARN] .env exists but API key is empty")
    else:
        print("\n[WARN] No .env file — create from .env.example and add your key")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
