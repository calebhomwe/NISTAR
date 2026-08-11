"""Generate review reports for WAN output clips."""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from nistar_pipeline.manifests import load_shot_manifest, load_take_log
from nistar_pipeline.continuity import check_continuity_warnings, build_review_checklist, REJECTION_REASONS
from nistar_pipeline.config import get_project_root


def main():
    parser = argparse.ArgumentParser(description="Review WAN output clips")
    parser.add_argument("--episode", default="episode_01")
    parser.add_argument("--shot", help="Review single shot")
    parser.add_argument("--format", choices=["md", "html"], default="md")
    args = parser.parse_args()

    root = get_project_root()
    shots = load_shot_manifest(args.episode)

    if args.shot:
        shots = [s for s in shots if s.shot_id == args.shot]

    if args.format == "md":
        report = _build_md_report(shots, root)
        out_path = root / "wan" / "logs" / f"review_report_{args.episode}.md"
    else:
        report = _build_html_report(shots, root)
        out_path = root / "wan" / "logs" / f"review_report_{args.episode}.html"

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(f"Review report: {out_path}")


def _build_md_report(shots, root) -> str:
    lines = ["# WAN 2.2 MAX — Review Report\n"]

    for shot in shots:
        takes = load_take_log(shot.shot_id)
        warnings = check_continuity_warnings(shot)
        checklist = build_review_checklist(shot)

        lines.append(f"\n## {shot.shot_id} — {shot.title}")
        lines.append(f"**Status:** {shot.status}")
        lines.append(f"**Mode:** {shot.generation_mode}")
        lines.append(f"**Input:** `{shot.input_image}`")
        lines.append(f"**Seed:** {shot.seed or 'not locked'}")
        lines.append(f"**Camera:** {shot.camera}")
        lines.append(f"**Action:** {shot.primary_action}")

        if takes:
            lines.append(f"\n### Takes ({len(takes)})")
            lines.append("| # | Filename | Resolution | Frames | Duration | Selected |")
            lines.append("|---|----------|-----------|--------|----------|----------|")
            for t in takes:
                sel = "**YES**" if t.selected else ""
                lines.append(f"| {t.take_number} | {t.filename} | {t.resolution} | {t.frame_count} | {t.duration_seconds:.1f}s | {sel} |")
        else:
            lines.append("\n*No takes generated yet*")

        if warnings:
            lines.append("\n### Continuity Warnings")
            for w in warnings:
                lines.append(f"- {w}")

        lines.append("\n### Review Checklist")
        for item in checklist:
            lines.append(item)

        lines.append("\n### Rejection Criteria")
        lines.append("Reject this take if any of:")
        for r in REJECTION_REASONS[:8]:
            lines.append(f"- {r.replace('_', ' ')}")

        lines.append("")

    return "\n".join(lines)


def _build_html_report(shots, root) -> str:
    html = ["<html><head><style>"]
    html.append("body{font-family:system-ui;max-width:900px;margin:2em auto;background:#1a1a2e;color:#eee;}")
    html.append(".shot{border:1px solid #333;padding:1em;margin:1em 0;border-radius:8px;}")
    html.append(".status{display:inline-block;padding:2px 8px;border-radius:4px;font-size:0.8em;}")
    html.append(".waiting{background:#663;}.takes_available{background:#363;}.approved{background:#3a6;}")
    html.append("table{border-collapse:collapse;width:100%;}th,td{border:1px solid #444;padding:4px 8px;text-align:left;}")
    html.append("</style></head><body>")
    html.append("<h1>WAN 2.2 MAX Review Report</h1>")

    for shot in shots:
        takes = load_take_log(shot.shot_id)
        warnings = check_continuity_warnings(shot)

        html.append(f'<div class="shot">')
        html.append(f'<h2>{shot.shot_id} — {shot.title}</h2>')
        html.append(f'<span class="status {shot.status}">{shot.status}</span>')
        html.append(f'<p><b>Mode:</b> {shot.generation_mode} | <b>Seed:</b> {shot.seed or "unlocked"}</p>')
        html.append(f'<p><b>Camera:</b> {shot.camera}</p>')
        html.append(f'<p><b>Action:</b> {shot.primary_action}</p>')

        if takes:
            html.append("<table><tr><th>#</th><th>File</th><th>Res</th><th>Dur</th><th>Sel</th></tr>")
            for t in takes:
                sel = "YES" if t.selected else ""
                html.append(f"<tr><td>{t.take_number}</td><td>{t.filename}</td><td>{t.resolution}</td><td>{t.duration_seconds:.1f}s</td><td>{sel}</td></tr>")
            html.append("</table>")

        if warnings:
            html.append("<h4>Warnings</h4><ul>")
            for w in warnings:
                html.append(f"<li>{w}</li>")
            html.append("</ul>")

        html.append("</div>")

    html.append("</body></html>")
    return "\n".join(html)


if __name__ == "__main__":
    main()
