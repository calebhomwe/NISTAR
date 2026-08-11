"""Export WAN 2.2 MAX prompt files for all shots in the manifest."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest
from nistar_pipeline.wan import export_prompt_file, build_full_positive, build_full_negative
from nistar_pipeline.config import load_wan_config


def main():
    parser = argparse.ArgumentParser(description="Export WAN 2.2 MAX prompt files")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--shot", help="Export single shot by ID")
    parser.add_argument("--output-dir", help="Override output directory")
    parser.add_argument("--dry-run", action="store_true", help="Print without writing")
    args = parser.parse_args()

    shots = load_shot_manifest(args.episode)
    if not shots:
        print(f"No shots found for {args.episode}. Run build_wan_manifest.py first.")
        return

    root = Path(__file__).resolve().parent.parent
    output_dir = Path(args.output_dir) if args.output_dir else root / "wan" / "prompts" / args.episode

    if args.shot:
        shots = [s for s in shots if s.shot_id == args.shot]
        if not shots:
            print(f"Shot {args.shot} not found")
            return

    wan_cfg = load_wan_config()
    gen = wan_cfg.get("generation", {})

    exported = []
    combined_md = [f"# WAN 2.2 MAX Prompt Book — {args.episode.upper()}\n"]
    combined_json = []

    for shot in shots:
        if args.dry_run:
            print(f"\n{'='*60}")
            print(f"[DRY-RUN] Shot: {shot.shot_id} — {shot.title}")
            print(f"  Mode: {shot.generation_mode}")
            print(f"  Input: {shot.input_image}")
            print(f"  Width: {gen.get('width', 832)} | Height: {gen.get('height', 480)}")
            print(f"  Frames: {gen.get('frames', 81)} | Steps: {gen.get('steps', 20)}")
            print(f"  Seed: {shot.seed or 'BLANK'}")
            print(f"  Positive: {build_full_positive(shot)[:120]}...")
            print(f"  Status: {shot.status}")
            continue

        path = export_prompt_file(shot, output_dir)
        exported.append(path)

        combined_md.append(f"\n## {shot.shot_id} — {shot.title}\n")
        combined_md.append(f"- Mode: {shot.generation_mode}")
        combined_md.append(f"- Camera: {shot.camera}")
        combined_md.append(f"- Action: {shot.primary_action}")
        combined_md.append(f"- Seed: {shot.seed or 'blank'}\n")

        combined_json.append({
            "shot_id": shot.shot_id,
            "title": shot.title,
            "mode": shot.generation_mode,
            "input_image": shot.input_image,
            "width": gen.get("width", 832),
            "height": gen.get("height", 480),
            "frames": gen.get("frames", 81),
            "steps": gen.get("steps", 20),
            "seed": shot.seed,
            "positive_prompt": build_full_positive(shot),
            "negative_prompt": build_full_negative(shot),
        })

    if not args.dry_run:
        # Write combined markdown
        md_path = output_dir / f"{args.episode}_prompt_book.md"
        md_path.write_text("\n".join(combined_md), encoding="utf-8")

        # Write combined JSON
        json_path = output_dir / f"{args.episode}_prompts.json"
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(combined_json, f, indent=2, ensure_ascii=False)

        # Write CSV
        csv_path = output_dir / f"{args.episode}_prompts.csv"
        import csv
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["shot_id", "title", "mode", "seed", "positive_prompt", "negative_prompt"])
            writer.writeheader()
            for entry in combined_json:
                writer.writerow({k: entry[k] for k in ["shot_id", "title", "mode", "seed", "positive_prompt", "negative_prompt"]})

        print(f"\nExported {len(exported)} prompt files to: {output_dir}")
        print(f"  Prompt book: {md_path.name}")
        print(f"  JSON manifest: {json_path.name}")
        print(f"  CSV manifest: {csv_path.name}")


if __name__ == "__main__":
    main()
