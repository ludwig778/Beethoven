from fractions import Fraction
from typing import List, Optional, Union

from pydantic import BaseModel

from beethoven.ui.constants import REVERSED_BASE_DURATIONS
from beethoven.utils.degree_or_note import parse_root_note_or_degree
from beethoven.models import Bpm, Chord, Degree, Duration, Note, Scale, TimeSignature


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
    root: Union[Note, Degree]
    name: str
    duration_item: DurationItem

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
            "duration_item": self.duration_item,
        }


class HarmonyItem(BaseModel):
    scale: Scale
    chord_items: List[ChordItem]
    bpm: Bpm
    time_signature: TimeSignature

    @classmethod
    def from_dict(cls, data):
        return cls(
            scale=Scale.parse(data["scale"]),
            chord_items=[ChordItem.from_dict(item) for item in data["chord_items"]],
            bpm=data["bpm"],
            time_signature=data["time_signature"],
        )

    def dict(self, *args, **kwargs):
        # print(2, self, args, kwargs)
        # pp({
        #    "scale": str(self.scale),
        #    "chord_items": [
        #        chord_item.dict()
        #        for chord_item in self.chord_items
        #    ]
        # })
        return {
            "scale": str(self.scale).replace(" ", "_"),
            "chord_items": [chord_item.dict() for chord_item in self.chord_items],
            "bpm": self.bpm,
            "time_signature": self.time_signature,
        }
