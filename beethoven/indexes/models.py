from dataclasses import dataclass
from typing import List


@dataclass
class NoteData:
    index: int
    semitones: int
    alphabetic_name: str
    syllabic_name: str

    @property
    def names(self) -> List[str]:
        return [self.alphabetic_name, self.syllabic_name]


@dataclass
class IntervalData:
    index: int
    semitones: int
    short_name: str
    long_name: str

    @property
    def names(self) -> List[str]:
        return [self.short_name, self.long_name]


@dataclass
class ChordData:
    intervals_string: str
    labels: List[str]
    short_name: str
    full_name: str
    symbol: str

    @property
    def names(self) -> List[str]:
        return [self.short_name, self.full_name, self.symbol]


@dataclass
class ScaleData:
    intervals_string: str
    labels: List[str]
    names: List[str]


IndexDataModels = (NoteData, IntervalData, ChordData, ScaleData)
