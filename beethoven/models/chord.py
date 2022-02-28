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

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = Field(default_factory=list)

    # TODO: Remove default factories, should be provided by the controller
    notes: List[Note] = Field(default_factory=list)
    intervals: List[Interval] = Field(default_factory=list)

    degree: Optional[Degree] = Field(default=None, repr=False)
    base_degree: Optional[Degree] = Field(default=None, repr=False)

    @validator("name")
    def name_must_be_valid(cls, name):
        if chord_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")
