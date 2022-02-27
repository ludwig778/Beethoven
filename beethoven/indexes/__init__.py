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

note_index = NoteIndex(note_index_data)
interval_index = IntervalIndex(interval_index_data)
chord_index = ChordIndex(chord_index_data)
scale_index = ScaleIndex(scale_index_data)
degree_index = DegreeIndex(degree_index_data)
