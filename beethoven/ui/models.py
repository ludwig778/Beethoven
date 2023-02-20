from __future__ import annotations

from fractions import Fraction
from typing import Callable, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from beethoven.models import (
    Bpm,
    Chord,
    Degree,
    Duration,
    Grid,
    Note,
    Scale,
    TimeSignature,
)
from beethoven.ui.constants import REVERSED_BASE_DURATIONS
from beethoven.utils.degree_or_note import parse_root_note_or_degree


class DurationItem(BaseModel):
    numerator: int = 1
    denominator: int = 1
    base_duration: Optional[Duration] = None

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    @property
    def value(self) -> Optional[Duration]:
        if not self.base_duration:
            return None

        return self.base_duration * self.fraction

    def to_string(self):
        if not self.base_duration:
            return ""

        return (
            str(self.numerator) if self.numerator > 1 else ""
        ) + REVERSED_BASE_DURATIONS[self.base_duration][0].upper()


class ChordItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    root: Union[Note, Degree]
    name: str
    duration_item: DurationItem

    def __hash__(self):
        return int(self.id)

    def get_index_from(self, chord_items: List[ChordItem]):
        for i, chord_item in enumerate(chord_items):
            if chord_item.id == self.id:
                return i

        raise KeyError(f"ChordItem {self.id} is not in list")

    def is_in(self, chord_items: List[ChordItem]):
        for chord_item in chord_items:
            if chord_item.id == self.id:
                return True

        return False

    def __str__(self):
        chord_name = str(self.root)

        if self.name:
            chord_name += " " + self.name.replace("_", " ")

        return chord_name

    def as_chord(self, scale: Scale):
        chord_str = f"{self.root}4"

        if self.name:
            chord_str += f"_{self.name.replace(' ', '_')}"

        return Chord.parse_with_scale_context(chord_str, scale=scale)

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name"),
            root=parse_root_note_or_degree(data["root"]),
            duration_item=data["duration_item"],
        )

    def dict(self, *args, **kwargs):
        return {
            "name": self.name,
            "root": str(self.root),
            "duration_item": self.duration_item.dict(),
        }


class HarmonyItem(BaseModel):
    id: UUID = Field(default_factory=uuid4)

    scale: Scale
    chord_items: List[ChordItem]
    bpm: Bpm
    time_signature: TimeSignature

    def __hash__(self):
        return int(self.id)

    def get_index_from(self, harmony_items: List[HarmonyItem]):
        for i, harmony_item in enumerate(harmony_items):
            if harmony_item.id == self.id:
                return i

        raise KeyError(f"HarmonyItem {harmony_item.id} is not in list")

    def is_in(self, harmony_items: List[HarmonyItem]):
        for harmony_item in harmony_items:
            if harmony_item.id == self.id:
                return True

        return False

    @classmethod
    def from_dict(cls, data):
        return cls(
            scale=Scale.parse(data["scale"]),
            chord_items=[ChordItem.from_dict(item) for item in data["chord_items"]],
            bpm=data["bpm"],
            time_signature=data["time_signature"],
        )

    def dict(self, *args, **kwargs):
        return {
            "scale": str(self.scale).replace(" ", "_"),
            "chord_items": [chord_item.dict() for chord_item in self.chord_items],
            "bpm": self.bpm,
            "time_signature": self.time_signature,
        }


class SequencerItem(BaseModel):
    grid: Grid
    is_preview: bool = False
    on_grid_part_change: Optional[Callable] = None
    on_grid_part_end: Optional[Callable] = None
