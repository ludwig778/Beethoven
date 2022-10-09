from typing import List

from pydantic import BaseModel


class NoteData(BaseModel):
    index: int
    semitones: int
    alphabetic_name: str
    syllabic_name: str

    @property
    def names(self):
        return [self.alphabetic_name, self.syllabic_name]


class IntervalData(BaseModel):
    index: int
    semitones: int
    short_name: str
    long_name: str

    @property
    def names(self):
        return [self.short_name, self.long_name]


class ChordData(BaseModel):
    intervals_string: str
    labels: List[str]
    short_name: str
    full_name: str
    symbol: str

    @property
    def names(self):
        return [self.short_name, self.full_name, self.symbol]


class ScaleData(BaseModel):
    intervals_string: str
    labels: List[str]
    names: List[str]


IndexDataModels = (NoteData, IntervalData, ChordData, ScaleData)
