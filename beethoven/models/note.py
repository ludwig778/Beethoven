from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, validator

from beethoven.indexes import note_index
from beethoven.utils.alterations import get_note_alteration_str_from_int


class Note(BaseModel):
    name: str
    alteration: int = 0
    octave: Optional[int] = None

    def __hash__(self):
        return hash(self.name + str(self.alteration) + str(self.octave))

    def __str__(self):
        return f"{self.name}{get_note_alteration_str_from_int(self.alteration)}{self.octave or ''}"

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
        if not self.octave:
            return (note_index.get_semitones(self.name) + self.alteration) % 12

        return note_index.get_semitones(self.name) + self.alteration + self.octave * 12

    # TODO: move to utils, setup a customized exception
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


class Notes(BaseModel):
    notes: List[Note]
    label: Optional[str]

    def __hash__(self):
        return hash("_".join(map(str, self.notes)))
