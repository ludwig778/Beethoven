from __future__ import annotations

from fractions import Fraction
from typing import List, Optional, Sequence, Union

from pydantic import BaseModel, Field


class Note(BaseModel):
    name: str
    alteration: int = 0
    octave: Optional[int] = None


class Interval(BaseModel):
    name: str
    alteration: int = 0


class Degree(BaseModel):
    name: str
    alteration: int = 0


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


class Scale(BaseModel):
    tonic: "Note"
    name: str

    notes: List["Note"] = Field(default_factory=list)
    intervals: List["Interval"] = Field(default_factory=list)


class Bpm(BaseModel):
    value: int


class TimeSignature(BaseModel):
    beats_per_bar: int
    beat_unit: int


class TimeSection(BaseModel):
    bar: int
    measure: int
    fraction: Fraction

    class Config:
        arbitrary_types_allowed = True


class Duration(BaseModel):
    value: Fraction

    class Config:
        arbitrary_types_allowed = True


class GridPart(BaseModel):
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Duration


class Grid(BaseModel):
    parts: Sequence[Union[Grid, GridPart]] = Field(default_factory=list)
