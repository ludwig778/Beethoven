from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, validator

from beethoven.indexes import note_index


class Note(BaseModel):
    name: str
    alteration: int = 0
    octave: Optional[int] = None

    @validator("name")
    def name_must_be_valid(cls, name):
        if note_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")

    @validator("octave")
    def octave_must_be_valid(cls, octave):
        if octave is None or 0 <= octave <= 10:
            return octave

        raise ValueError(f"Invalid octave: {octave}, must be between 0 and 10")

    @property
    def midi_index(self) -> int:
        return (
            note_index.get_semitones(self.name)
            + self.alteration
            + (self.octave or 0) * 12
        )

    def check_octave_states(self, other: Note) -> None:
        """Check that both notes have or have not octaves"""

        # Apply a XOR function checking on None values
        if [self.octave is None, other.octave is None].count(False) == 1:
            raise Exception(
                "Octaves must be present or absent in order to compare Notes"
            )

    def __eq__(self, other: object) -> bool:
        """Check notes pitch equality, since we check on the midi_index property"""

        if not isinstance(other, Note):
            return NotImplemented

        self.check_octave_states(other)

        return self.midi_index == other.midi_index

    def __gt__(self, other: Note) -> bool:
        self.check_octave_states(other)

        return self.midi_index > other.midi_index

    def __ge__(self, other: Note) -> bool:
        self.check_octave_states(other)

        return self.midi_index >= other.midi_index
