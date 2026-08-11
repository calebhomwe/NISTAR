"""Estimate total generation time and VRAM requirements."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest
from nistar_pipeline.config import load_wan_config


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Estimate generation load")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--discovery-passes", type=int, default=None)
    args = parser.parse_args()

    wan_cfg = load_wan_config()
    gen = wan_cfg["generation"]
    workflow = wan_cfg["workflow"]

    shots = load_shot_manifest(args.episode)
    if not shots:
        print("No shots in manifest")
        return

    passes = args.discovery_passes or workflow.get("discovery_passes", 3)
    i2v_shots = [s for s in shots if s.generation_mode == "image_to_video"]
    t2v_shots = [s for s in shots if s.generation_mode == "text_to_video"]

    # Timing estimates for RTX 4080 16GB with Q8 14B model
    i2v_time_per_gen = 8.0  # minutes per 81-frame i2v generation
    t2v_time_per_gen = 10.0  # minutes per 81-frame t2v generation

    total_i2v = len(i2v_shots) * passes
    total_t2v = len(t2v_shots) * passes
    total_gens = total_i2v + total_t2v

    total_minutes = (total_i2v * i2v_time_per_gen) + (total_t2v * t2v_time_per_gen)
    total_hours = total_minutes / 60

    pending = [s for s in shots if s.status in ("waiting_for_input", "takes_available")]
    approved = [s for s in shots if s.status == "approved"]

    print("=" * 60)
    print("NISTAR — Generation Load Estimate")
    print("=" * 60)
    print(f"\nModel: WAN 2.2 MAX 14B Q8")
    print(f"Resolution: {gen['width']}x{gen['height']}")
    print(f"Frames: {gen['frames']} | Steps: {gen['steps']}")
    print(f"Discovery passes: {passes}")
    print(f"\nShots:")
    print(f"  Image-to-video: {len(i2v_shots)}")
    print(f"  Text-to-video:  {len(t2v_shots)}")
    print(f"  Total:          {len(shots)}")
    print(f"\nStatus:")
    print(f"  Pending:  {len(pending)}")
    print(f"  Approved: {len(approved)}")
    print(f"\nGeneration estimate ({passes} passes):")
    print(f"  Total generations: {total_gens}")
    print(f"  Estimated time:    {total_minutes:.0f} min ({total_hours:.1f} hours)")
    print(f"  VRAM required:     ~14-16 GB (Q8 model)")
    print(f"\nNote: Estimates assume RTX 4080 16GB. Actual times vary.")
    print(f"GPU will be fully occupied during generation.")


if __name__ == "__main__":
    main()
