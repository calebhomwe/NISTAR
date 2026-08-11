"""Manifest loading and saving for shots, audio, and takes."""

import json
import csv
from pathlib import Path
from typing import Optional

from .config import get_project_root
from .models import Shot, Take, DialogueLine


def load_shot_manifest(episode: str = "episode_01") -> list[Shot]:
    root = get_project_root()
    path = root / "wan" / "manifests" / f"{episode}_shots.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Shot(**s) for s in data.get("shots", [])]


def save_shot_manifest(shots: list[Shot], episode: str = "episode_01"):
    root = get_project_root()
    path = root / "wan" / "manifests" / f"{episode}_shots.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"episode": episode, "shot_count": len(shots), "shots": [s.to_dict() for s in shots]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def save_shot_manifest_csv(shots: list[Shot], episode: str = "episode_01"):
    root = get_project_root()
    path = root / "wan" / "manifests" / f"{episode}_shots.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "shot_id", "scene", "title", "generation_mode", "status",
        "characters", "camera", "primary_action", "seed", "approved_take"
    ]
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in shots:
            row = s.to_dict()
            row["characters"] = "|".join(row["characters"])
            writer.writerow({k: row.get(k, "") for k in fields})


def save_shot_manifest_md(shots: list[Shot], episode: str = "episode_01"):
    root = get_project_root()
    path = root / "wan" / "manifests" / f"{episode}_shots.md"
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [f"# {episode.upper()} — Shot Manifest\n"]
    lines.append(f"Total shots: {len(shots)}\n")
    lines.append("| # | Shot ID | Title | Mode | Status | Characters |")
    lines.append("|---|---------|-------|------|--------|------------|")

    for i, s in enumerate(shots, 1):
        chars = ", ".join(s.characters) if s.characters else "-"
        lines.append(f"| {i} | {s.shot_id} | {s.title} | {s.generation_mode} | {s.status} | {chars} |")

    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def load_take_log(shot_id: str) -> list[Take]:
    root = get_project_root()
    path = root / "wan" / "logs" / f"{shot_id}_takes.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Take(**t) for t in data.get("takes", [])]


def save_take_log(shot_id: str, takes: list[Take]):
    root = get_project_root()
    path = root / "wan" / "logs" / f"{shot_id}_takes.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"shot_id": shot_id, "takes": [vars(t) for t in takes]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def update_shot_status(shots: list[Shot], shot_id: str, status: str, take: Optional[str] = None):
    for s in shots:
        if s.shot_id == shot_id:
            s.status = status
            if take:
                s.approved_take = take
            break
