from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, validator

from beethoven.indexes import chord_index
from beethoven.models.degree import Degree
from beethoven.models.interval import Interval
from beethoven.models.note import Note


class Chord(BaseModel):
    root: Note
    name: str

    notes: List[Note] = Field(default_factory=list)
    intervals: List[Interval] = Field(default_factory=list)

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = Field(default_factory=list)

    degree: Optional[Degree] = Field(default=None, repr=False)
    base_degree: Optional[Degree] = Field(default=None, repr=False)

    def __hash__(self):
        return hash(
            f"{self.root}_{self.name}" f":notes={[str(note) for note in self.notes]}"
        )

    def __str__(self):
        return f"{self.degree or self.root} {self.name}"

    @validator("name")
    def name_must_be_valid(cls, name):
        if chord_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")
