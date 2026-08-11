"""Build contact sheets from WAN output takes for visual comparison."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_take_log
from nistar_pipeline.config import get_project_root
from nistar_pipeline.naming import contact_sheet_filename


def main():
    parser = argparse.ArgumentParser(description="Build contact sheet from takes")
    parser.add_argument("--shot", required=True, help="Shot ID")
    parser.add_argument("--frames", type=int, default=6, help="Frames to extract per take")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    takes = load_take_log(args.shot)

    if not takes:
        print(f"No takes for {args.shot}")
        return

    clips_dir = root / "wan" / "output_clips" / args.shot
    output_dir = root / "wan" / "contact_sheets"
    output_dir.mkdir(parents=True, exist_ok=True)

    out_name = contact_sheet_filename(args.shot)

    if args.dry_run:
        print(f"[DRY-RUN] Would build contact sheet for {args.shot}")
        print(f"  Takes: {len(takes)}")
        print(f"  Frames per take: {args.frames}")
        print(f"  Output: {output_dir / out_name}")
        return

    try:
        from PIL import Image
        import subprocess
    except ImportError:
        print("ERROR: Pillow required. pip install Pillow")
        return

    rows = []
    for take in takes:
        clip_path = clips_dir / take.filename
        if not clip_path.exists():
            continue

        frames = _extract_frames(clip_path, args.frames)
        if frames:
            rows.append((take, frames))

    if not rows:
        print("No frames extracted")
        return

    # Build grid
    frame_w, frame_h = rows[0][1][0].size
    cols = args.frames
    grid_w = frame_w * cols + (cols - 1) * 4
    grid_h = (frame_h + 30) * len(rows)

    sheet = Image.new("RGB", (grid_w, grid_h), (20, 20, 30))

    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(sheet)

    for row_idx, (take, frames) in enumerate(rows):
        y = row_idx * (frame_h + 30)
        label = f"TAKE {take.take_number:02d}" + (" [SELECTED]" if take.selected else "")
        draw.text((4, y + 2), label, fill=(200, 200, 200))

        for col_idx, frame in enumerate(frames):
            x = col_idx * (frame_w + 4)
            sheet.paste(frame, (x, y + 20))

    sheet.save(output_dir / out_name)
    print(f"Contact sheet: {output_dir / out_name}")


def _extract_frames(clip_path: Path, count: int) -> list:
    """Extract evenly-spaced frames from a video clip."""
    try:
        import subprocess
        import tempfile
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmpdir:
            subprocess.run(
                ["ffmpeg", "-i", str(clip_path), "-vf", f"select=not(mod(n\\,{max(1, 81//count)}))",
                 "-vsync", "vfr", "-frames:v", str(count),
                 str(Path(tmpdir) / "frame_%03d.png")],
                capture_output=True, timeout=30
            )
            frames = []
            for f in sorted(Path(tmpdir).glob("frame_*.png")):
                frames.append(Image.open(f).copy())
            return frames
    except Exception:
        return []


if __name__ == "__main__":
    main()
