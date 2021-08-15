from dataclasses import dataclass, field
from fractions import Fraction
from typing import Generator, List, Optional, Sequence

from beethoven.core.abstract import AbstractGridComponent, AbstractObject


@dataclass
class Note:
    name: str
    alteration: int = 0
    octave: Optional[int] = None


@dataclass
class Interval:
    name: str
    alteration: int = 0


@dataclass
class Degree:
    name: str
    alteration: int = 0


@dataclass
class Chord:
    root: Note
    name: str

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = field(default_factory=list)

    notes: List[Note] = field(default_factory=list)
    intervals: List[Interval] = field(default_factory=list)

    degree: Optional[Degree] = field(default=None, repr=False)
    base_degree: Optional[Degree] = field(default=None, repr=False)


@dataclass
class Scale:
    tonic: Note
    name: str

    notes: List[Note] = field(default_factory=list)
    intervals: List[Interval] = field(default_factory=list)


@dataclass
class Bpm(AbstractObject):
    value: int


@dataclass
class TimeSignature:
    beats_per_bar: int
    beat_unit: int


@dataclass
class Duration:
    value: Fraction


@dataclass
class GridPart(AbstractGridComponent):
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Optional[Duration]

    def __iter__(self) -> Generator[AbstractGridComponent, None, None]:
        yield self


@dataclass
class Grid(AbstractGridComponent):
    parts: Sequence[AbstractGridComponent] = field(default_factory=list)

    def __iter__(self) -> Generator[AbstractGridComponent, None, None]:
        for part in self.parts:
            yield from part
