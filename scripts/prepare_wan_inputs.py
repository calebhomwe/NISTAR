"""Prepare input images for WAN 2.2 MAX — crop/resize to 832x480."""

import sys
import shutil
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest
from nistar_pipeline.config import load_wan_config, get_project_root
from nistar_pipeline.naming import input_frame_filename


def main():
    parser = argparse.ArgumentParser(description="Prepare WAN input frames")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--shot", help="Prepare single shot")
    parser.add_argument("--mode", choices=["crop", "letterbox"], default="crop")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    root = get_project_root()
    wan_cfg = load_wan_config()
    target_w = wan_cfg["generation"]["width"]
    target_h = wan_cfg["generation"]["height"]
    shots = load_shot_manifest(args.episode)

    if args.shot:
        shots = [s for s in shots if s.shot_id == args.shot]

    i2v_shots = [s for s in shots if s.generation_mode == "image_to_video"]
    print(f"Processing {len(i2v_shots)} image-to-video shots (target: {target_w}x{target_h})")

    try:
        from PIL import Image
    except ImportError:
        print("ERROR: Pillow not installed. Run: pip install Pillow")
        return

    output_dir = root / "wan" / "input_frames"
    output_dir.mkdir(parents=True, exist_ok=True)
    warnings = []

    for shot in i2v_shots:
        # Check approved stills first
        approved_dir = root / "stills" / "episode_01" / "approved"
        candidates = list(approved_dir.glob(f"{shot.shot_id}*"))

        if not candidates:
            # Check character reference as fallback
            for char in shot.characters:
                char_dir = root / "stills" / "characters" / char
                char_refs = list(char_dir.glob("*canonical*"))
                if char_refs:
                    candidates = char_refs[:1]
                    break

        if not candidates:
            warnings.append(f"  [MISSING] {shot.shot_id}: No input image found")
            continue

        src = candidates[0]
        out_name = input_frame_filename(shot.shot_id)
        out_path = output_dir / out_name

        if args.dry_run:
            print(f"  [DRY-RUN] {shot.shot_id}: Would process {src.name} → {out_name}")
            img = Image.open(src)
            w, h = img.size
            if w != target_w or h != target_h:
                print(f"    Source: {w}x{h} → needs {'crop' if args.mode == 'crop' else 'letterbox'}")
            continue

        img = Image.open(src)
        w, h = img.size

        if w == target_w and h == target_h:
            shutil.copy2(src, out_path)
            print(f"  [COPY] {shot.shot_id}: Already correct size")
            continue

        if args.mode == "crop":
            result = _smart_crop(img, target_w, target_h, shot)
        else:
            result = _letterbox(img, target_w, target_h)

        result.save(out_path, "PNG")
        print(f"  [{'CROP' if args.mode == 'crop' else 'LBOX'}] {shot.shot_id}: {w}x{h} → {target_w}x{target_h}")

        # Face-edge warning
        if shot.characters and w > 0:
            _check_face_position(img, shot, warnings)

    if warnings:
        print(f"\n{'='*40}")
        print("WARNINGS:")
        for w in warnings:
            print(w)


def _smart_crop(img, target_w, target_h, shot):
    """Crop to target aspect ratio, centered, preserving composition."""
    from PIL import Image

    w, h = img.size
    target_ratio = target_w / target_h
    current_ratio = w / h

    if current_ratio > target_ratio:
        # Too wide — crop sides
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        img = img.crop((left, 0, left + new_w, h))
    else:
        # Too tall — crop top/bottom
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        img = img.crop((0, top, w, top + new_h))

    return img.resize((target_w, target_h), Image.LANCZOS)


def _letterbox(img, target_w, target_h):
    """Letterbox to target size with black bars."""
    from PIL import Image

    ratio = min(target_w / img.width, target_h / img.height)
    new_size = (int(img.width * ratio), int(img.height * ratio))
    img = img.resize(new_size, Image.LANCZOS)

    result = Image.new("RGB", (target_w, target_h), (0, 0, 0))
    offset = ((target_w - new_size[0]) // 2, (target_h - new_size[1]) // 2)
    result.paste(img, offset)
    return result


def _check_face_position(img, shot, warnings):
    """Warn if characters present and face might be near edge."""
    w, h = img.size
    edge_zone = 0.1
    # Simple heuristic: if the image is portrait-oriented with characters,
    # warn about potential face cropping
    if h > w * 1.3 and shot.characters:
        warnings.append(
            f"  [FACE-EDGE] {shot.shot_id}: Portrait source with characters — "
            f"verify face not clipped after crop"
        )


if __name__ == "__main__":
    main()
