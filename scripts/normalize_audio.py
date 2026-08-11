"""Normalize generated audio to real PCM WAV.

ElevenLabs returns MP3 data even when a WAV Accept header is sent, so files
land as MP3 bytes with a .wav extension. This script rewrites any such file
as a true PCM WAV (16-bit, 44.1 kHz) in place using ffmpeg.

Idempotent: files that are already RIFF/WAVE are skipped. Run it after any
generation batch (dialogue, SFX, retakes) to guarantee real WAV for DaVinci.

Usage:
    python scripts/normalize_audio.py                 # all audio dirs
    python scripts/normalize_audio.py --lang jp       # only the JP track
    python scripts/normalize_audio.py --dir audio/sfx # a specific dir
    python scripts/normalize_audio.py --dry-run
"""

import sys
import shutil
import argparse
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from nistar_pipeline.config import get_project_root


def find_ffmpeg() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    # common WinGet install location
    winget = Path.home() / "AppData/Local/Microsoft/WinGet/Links/ffmpeg.exe"
    if winget.exists():
        return str(winget)
    raise FileNotFoundError("ffmpeg not found on PATH or in WinGet Links")


def is_real_wav(path: Path) -> bool:
    with open(path, "rb") as f:
        head = f.read(12)
    return head[:4] == b"RIFF" and head[8:12] == b"WAVE"


def normalize_dir(directory: Path, ffmpeg: str, dry_run: bool) -> tuple:
    converted = skipped = failed = 0
    for f in sorted(directory.glob("*.wav")):
        if is_real_wav(f):
            skipped += 1
            continue
        if dry_run:
            print(f"  [DRY-RUN] would transcode: {f.name}")
            converted += 1
            continue
        tmp = f.with_suffix(".__tmp.wav")
        try:
            r = subprocess.run(
                [ffmpeg, "-y", "-i", str(f), "-c:a", "pcm_s16le", "-ar", "44100",
                 str(tmp), "-loglevel", "error"],
                capture_output=True, timeout=60,
            )
            if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
                shutil.move(str(tmp), str(f))
                converted += 1
            else:
                tmp.unlink(missing_ok=True)
                failed += 1
                print(f"  FAIL: {f.name} ({r.stderr.decode('utf-8', 'ignore')[:80]})")
        except Exception as e:
            tmp.unlink(missing_ok=True)
            failed += 1
            print(f"  FAIL: {f.name} ({e})")
    return converted, skipped, failed


def main():
    ap = argparse.ArgumentParser(description="Normalize audio to real PCM WAV")
    ap.add_argument("--lang", choices=["en", "jp"], help="Only this dialogue track")
    ap.add_argument("--dir", help="Only this directory (relative to project root)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = get_project_root()
    if args.dir:
        dirs = [root / args.dir]
    elif args.lang == "jp":
        dirs = [root / "audio" / "dialogue_jp"]
    elif args.lang == "en":
        dirs = [root / "audio" / "dialogue"]
    else:
        dirs = [root / "audio" / "dialogue", root / "audio" / "dialogue_jp",
                root / "audio" / "sfx", root / "audio" / "selected"]

    ffmpeg = find_ffmpeg()
    tc = ts = tf = 0
    for d in dirs:
        if not d.exists():
            continue
        print(f"Normalizing {d.relative_to(root)} ...")
        c, s, fl = normalize_dir(d, ffmpeg, args.dry_run)
        print(f"  converted={c} already-wav={s} failed={fl}")
        tc += c; ts += s; tf += fl

    print(f"\nTotal: converted={tc} already-wav={ts} failed={tf}")


if __name__ == "__main__":
    main()
