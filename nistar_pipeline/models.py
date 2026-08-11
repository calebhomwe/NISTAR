"""Data models for NISTAR pipeline."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Shot:
    shot_id: str
    scene: str = ""
    title: str = ""
    duration_target_seconds: float = 4.0
    generation_mode: str = "image_to_video"
    input_image: str = ""
    characters: list[str] = field(default_factory=list)
    environment: str = ""
    vehicle: str = ""
    camera: str = ""
    primary_action: str = ""
    secondary_motion: list[str] = field(default_factory=list)
    lighting: str = ""
    colour_script: str = ""
    positive_prompt: str = ""
    negative_prompt: str = ""
    seed: Optional[int] = None
    status: str = "waiting_for_input"
    approved_take: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "shot_id": self.shot_id,
            "scene": self.scene,
            "title": self.title,
            "duration_target_seconds": self.duration_target_seconds,
            "generation_mode": self.generation_mode,
            "input_image": self.input_image,
            "characters": self.characters,
            "environment": self.environment,
            "vehicle": self.vehicle,
            "camera": self.camera,
            "primary_action": self.primary_action,
            "secondary_motion": self.secondary_motion,
            "lighting": self.lighting,
            "colour_script": self.colour_script,
            "positive_prompt": self.positive_prompt,
            "negative_prompt": self.negative_prompt,
            "seed": self.seed,
            "status": self.status,
            "approved_take": self.approved_take,
            "notes": self.notes,
        }


@dataclass
class Take:
    shot_id: str
    take_number: int
    filename: str
    resolution: str = ""
    frame_count: int = 0
    duration_seconds: float = 0.0
    file_hash: str = ""
    seed: Optional[int] = None
    selected: bool = False
    rejection_reason: str = ""


@dataclass
class DialogueLine:
    line_id: str
    episode: str
    scene: str
    character: str
    text: str
    emotion: str = ""
    is_critical: bool = False
    takes_generated: int = 0
    selected_take: Optional[int] = None


@dataclass
class SFXEntry:
    sfx_id: str
    episode: str
    scene: str
    description: str
    duration_seconds: float = 4.0
    takes_generated: int = 0
    selected_take: Optional[int] = None
