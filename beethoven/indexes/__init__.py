from pydantic import BaseModel

from beethoven.indexes.data import (
    chord_index_data,
    degree_index_data,
    interval_index_data,
    note_index_data,
    scale_index_data,
)
from beethoven.indexes.objects import (
    ChordIndex,
    DegreeIndex,
    IntervalIndex,
    NoteIndex,
    ScaleIndex,
)


class Indexes(BaseModel):
    notes: NoteIndex
    intervals: IntervalIndex
    chords: ChordIndex
    scales: ScaleIndex
    degrees: DegreeIndex

    class Config:
        arbitrary_types_allowed = True


def get_indexes() -> Indexes:
    return Indexes(
        notes=NoteIndex(note_index_data),
        intervals=IntervalIndex(interval_index_data),
        chords=ChordIndex(chord_index_data),
        scales=ScaleIndex(scale_index_data),
        degrees=DegreeIndex(degree_index_data),
    )
