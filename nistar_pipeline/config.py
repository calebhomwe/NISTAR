"""Configuration loader for NISTAR pipeline."""

import os
from pathlib import Path
from typing import Any

import yaml


def get_project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def load_yaml(filename: str) -> dict[str, Any]:
    path = get_project_root() / "config" / filename
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_wan_config() -> dict[str, Any]:
    return load_yaml("wan22_max.yaml")


def load_style_lock() -> dict[str, Any]:
    return load_yaml("style_lock.yaml")


def load_character_refs() -> dict[str, Any]:
    return load_yaml("character_refs.yaml")


def load_voices() -> dict[str, Any]:
    return load_yaml("voices.yaml")


def load_audio_config() -> dict[str, Any]:
    return load_yaml("audio_generation.yaml")


def load_scene_overrides() -> dict[str, Any]:
    return load_yaml("scene_overrides.yaml")


def get_env(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


def get_elevenlabs_key() -> str:
    key = get_env("ELEVENLABS_API_KEY")
    if not key:
        from dotenv import load_dotenv
        load_dotenv(get_project_root() / ".env")
        key = os.environ.get("ELEVENLABS_API_KEY", "")
    return key
