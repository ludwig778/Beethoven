from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, validator

from beethoven.indexes import scale_index
from beethoven.models.interval import Interval
from beethoven.models.note import Note


class Scale(BaseModel):
    tonic: Note
    name: str

    # TODO: Remove default factories, should be provided by the controller
    notes: List[Note] = Field(default_factory=list)
    intervals: List[Interval] = Field(default_factory=list)

    @validator("name")
    def name_must_be_valid(cls, name):
        if scale_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")
