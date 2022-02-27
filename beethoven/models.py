from __future__ import annotations

from fractions import Fraction
from typing import List, Optional, Sequence, Union

from pydantic import BaseModel, Field, validator

from beethoven.indexes import (
    chord_index,
    degree_index,
    interval_index,
    note_index,
    scale_index,
)


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


class Interval(BaseModel):
    name: str
    alteration: int = 0

    @validator("name")
    def name_must_be_valid(cls, name):
        if interval_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")


class Degree(BaseModel):
    name: str
    alteration: int = 0

    @validator("name")
    def name_must_be_valid(cls, name):
        if degree_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")


class Chord(BaseModel):
    root: Note
    name: str

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = Field(default_factory=list)

    notes: List[Note] = Field(default_factory=list)
    intervals: List[Interval] = Field(default_factory=list)

    degree: Optional[Degree] = Field(default=None, repr=False)
    base_degree: Optional[Degree] = Field(default=None, repr=False)

    @validator("name")
    def name_must_be_valid(cls, name):
        if chord_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")


class Scale(BaseModel):
    tonic: "Note"
    name: str

    notes: List["Note"] = Field(default_factory=list)
    intervals: List["Interval"] = Field(default_factory=list)

    @validator("name")
    def name_must_be_valid(cls, name):
        if scale_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")


class Bpm(BaseModel):
    value: int

    @validator("value")
    def value_must_be_within_range(cls, value):
        if 0 < value <= 600:
            return value

        raise ValueError(f"Invalid value: {value}, must be between 0 and 600")


class TimeSignature(BaseModel):
    beats_per_bar: int
    beat_unit: int

    # TODO check beat unit multiple of 2


class TimeSection(BaseModel):
    bar: int
    measure: int
    fraction: Fraction

    class Config:
        arbitrary_types_allowed = True

    # TODO cast int to fraction


class Duration(BaseModel):
    value: Fraction

    class Config:
        arbitrary_types_allowed = True

    # TODO cast int to fraction


class GridPart(BaseModel):
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Duration


class Grid(BaseModel):
    parts: Sequence[Union[Grid, GridPart]] = Field(default_factory=list)
