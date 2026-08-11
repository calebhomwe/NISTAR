"""ElevenLabs audio generation utilities."""

import time
import hashlib
from pathlib import Path
from typing import Optional

from .config import get_project_root, get_elevenlabs_key, load_audio_config, load_voices
from .models import DialogueLine, SFXEntry
from .naming import dialogue_filename, sfx_filename
from .logging_utils import get_logger

logger = get_logger("audio")


class AudioGenerator:
    def __init__(self, dry_run: bool = False, lang: str = "en"):
        self.dry_run = dry_run
        self.lang = lang
        self.root = get_project_root()
        self.config = load_audio_config()
        if lang == "jp":
            from .config import load_yaml
            self.voices = load_yaml("voices_jp.yaml").get("voices", {})
        else:
            self.voices = load_voices().get("voices", {})
        self.api_key = get_elevenlabs_key() if not dry_run else "DRY_RUN"

    def _dialogue_dir(self) -> str:
        base = self.config["output"]["dialogue_dir"]
        return f"{base}_jp" if self.lang == "jp" else base

    def generate_dialogue(self, line: DialogueLine) -> list[Path]:
        voice_cfg = self.voices.get(line.character.lower(), {})
        voice_id = voice_cfg.get("voice_id", "")
        takes = self.config["generation"]["critical_takes"] if line.is_critical else self.config["generation"]["normal_takes"]

        outputs = []
        for take_num in range(1, takes + 1):
            filename = dialogue_filename(
                line.episode, line.scene, line.character, line.line_id, take_num
            )
            out_path = self.root / self._dialogue_dir() / filename

            if self.dry_run:
                logger.info(f"[DRY-RUN] Would generate: {filename}")
                logger.info(f"  Voice: {voice_cfg.get('name', line.character)}")
                logger.info(f"  Text: {line.text[:80]}...")
                logger.info(f"  Model: {voice_cfg.get('model_id', 'eleven_multilingual_v2')}")
                outputs.append(out_path)
                continue

            if not voice_id:
                logger.error(f"No voice_id for character: {line.character}")
                break

            if not self.api_key:
                logger.error("No ELEVENLABS_API_KEY set")
                break

            audio_data = self._call_elevenlabs(voice_id, voice_cfg, line.text)
            if audio_data:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(audio_data)
                outputs.append(out_path)
                logger.info(f"Generated: {filename}")
            else:
                logger.error(f"Failed to generate: {filename}")

        return outputs

    def generate_sfx(self, entry: SFXEntry) -> list[Path]:
        takes = self.config["sfx"]["takes"]
        outputs = []

        for take_num in range(1, takes + 1):
            filename = sfx_filename(entry.episode, entry.scene, entry.sfx_id, take_num)
            out_path = self.root / self.config["output"]["sfx_dir"] / filename

            if self.dry_run:
                logger.info(f"[DRY-RUN] Would generate SFX: {filename}")
                logger.info(f"  Description: {entry.description}")
                logger.info(f"  Duration: {entry.duration_seconds}s")
                outputs.append(out_path)
                continue

            if not self.api_key:
                logger.error("No ELEVENLABS_API_KEY set")
                break

            audio_data = self._call_elevenlabs_sfx(entry.description, entry.duration_seconds)
            if audio_data:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(audio_data)
                outputs.append(out_path)
                logger.info(f"Generated SFX: {filename}")

        return outputs

    def _call_elevenlabs(self, voice_id: str, voice_cfg: dict, text: str) -> Optional[bytes]:
        import requests

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/wav",
        }
        payload = {
            "text": text,
            "model_id": voice_cfg.get("model_id", "eleven_multilingual_v2"),
            "voice_settings": {
                "stability": voice_cfg.get("stability", 0.5),
                "similarity_boost": voice_cfg.get("similarity_boost", 0.75),
                "style": voice_cfg.get("style", 0.0),
                "use_speaker_boost": voice_cfg.get("use_speaker_boost", True),
            },
        }

        for attempt in range(self.config["generation"]["retry_max"]):
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return resp.content
                elif resp.status_code == 429:
                    pause = self.config["generation"]["rate_limit_pause_seconds"]
                    logger.warning(f"Rate limited, waiting {pause}s...")
                    time.sleep(pause)
                else:
                    logger.error(f"API error {resp.status_code}: {resp.text[:200]}")
                    break
            except Exception as e:
                logger.error(f"Request failed: {e}")
                time.sleep(self.config["generation"]["retry_delay_seconds"])

        return None

    def _call_elevenlabs_sfx(self, description: str, duration: float) -> Optional[bytes]:
        import requests

        url = "https://api.elevenlabs.io/v1/sound-generation"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json",
            "Accept": "audio/wav",
        }
        payload = {
            "text": description,
            "duration_seconds": duration,
        }

        for attempt in range(self.config["generation"]["retry_max"]):
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=60)
                if resp.status_code == 200:
                    return resp.content
                elif resp.status_code == 429:
                    pause = self.config["generation"]["rate_limit_pause_seconds"]
                    logger.warning(f"Rate limited, waiting {pause}s...")
                    time.sleep(pause)
                else:
                    logger.error(f"SFX API error {resp.status_code}: {resp.text[:200]}")
                    break
            except Exception as e:
                logger.error(f"SFX request failed: {e}")
                time.sleep(self.config["generation"]["retry_delay_seconds"])

        return None
