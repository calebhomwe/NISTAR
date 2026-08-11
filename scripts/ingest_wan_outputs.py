"""Ingest WAN 2.2 MAX output clips — match to shots, record takes."""

import sys
import hashlib
import shutil
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest, save_shot_manifest, load_take_log, save_take_log
from nistar_pipeline.models import Take
from nistar_pipeline.config import get_project_root
from nistar_pipeline.naming import shot_filename


def main():
    parser = argparse.ArgumentParser(description="Ingest WAN output clips")
    parser.add_argument("--import-dir", help="Directory to scan for new clips")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    import_dir = Path(args.import_dir) if args.import_dir else root / "wan" / "output_clips"

    if not import_dir.exists():
        print(f"Import directory not found: {import_dir}")
        return

    clips = list(import_dir.glob("*.mp4")) + list(import_dir.glob("*.webm"))
    if not clips:
        print(f"No video files found in: {import_dir}")
        return

    shots = load_shot_manifest(args.episode)
    shot_ids = {s.shot_id for s in shots}

    print(f"Found {len(clips)} clips to process")
    ingested = 0

    for clip in sorted(clips):
        # Try to match filename to shot ID
        matched_id = _match_to_shot(clip.stem, shot_ids)
        if not matched_id:
            print(f"  [SKIP] Cannot match: {clip.name}")
            continue

        # Load existing takes
        takes = load_take_log(matched_id)
        next_take = len(takes) + 1

        # Get file info
        file_hash = _hash_file(clip)
        resolution, frame_count, duration = _get_video_info(clip)

        new_take = Take(
            shot_id=matched_id,
            take_number=next_take,
            filename=shot_filename(matched_id, next_take, clip.suffix),
            resolution=resolution,
            frame_count=frame_count,
            duration_seconds=duration,
            file_hash=file_hash,
        )

        if args.dry_run:
            print(f"  [DRY-RUN] {clip.name} → {matched_id} TAKE{next_take:02d}")
            print(f"    Resolution: {resolution}, Frames: {frame_count}, Duration: {duration:.1f}s")
            continue

        # Copy to shot directory
        dest_dir = root / "wan" / "output_clips" / matched_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / new_take.filename
        shutil.copy2(clip, dest)

        # Save take log
        takes.append(new_take)
        save_take_log(matched_id, takes)

        # Update manifest status
        for shot in shots:
            if shot.shot_id == matched_id and shot.status == "waiting_for_input":
                shot.status = "takes_available"

        print(f"  [OK] {clip.name} → {matched_id} TAKE{next_take:02d}")
        ingested += 1

    if not args.dry_run and ingested > 0:
        save_shot_manifest(shots, args.episode)

    print(f"\nIngested: {ingested} clips")


def _match_to_shot(stem: str, shot_ids: set) -> str:
    """Try to match a filename stem to a known shot ID."""
    stem_upper = stem.upper()
    for sid in sorted(shot_ids, key=len, reverse=True):
        if sid.upper() in stem_upper:
            return sid
    return ""


def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _get_video_info(path: Path) -> tuple:
    """Get resolution, frame count, duration. Returns defaults if ffprobe unavailable."""
    try:
        import subprocess
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(path)],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video":
                    w = stream.get("width", 0)
                    h = stream.get("height", 0)
                    frames = int(stream.get("nb_frames", 0))
                    duration = float(stream.get("duration", 0))
                    return f"{w}x{h}", frames, duration
    except Exception:
        pass

    # Fallback
    size_mb = path.stat().st_size / (1024 * 1024)
    return "unknown", 0, 0.0


if __name__ == "__main__":
    main()
