from beethoven.indexes.data import (
    chords_index_data,
    degrees_index_data,
    intervals_index_data,
    notes_index_data,
    scales_index_data,
)
from beethoven.indexes.objects import ChordIndex, DegreeIndex, IntervalIndex, NoteIndex, ScaleIndex

note_index = NoteIndex(notes_index_data)
interval_index = IntervalIndex(intervals_index_data)
chord_index = ChordIndex(chords_index_data)
scale_index = ScaleIndex(scales_index_data)
degree_index = DegreeIndex(degrees_index_data)
