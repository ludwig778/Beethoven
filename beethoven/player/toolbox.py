from dataclasses import replace
from itertools import product
from typing import List

from beethoven.models import Note, Scale


def get_scale_notes_within_range(low_range: Note, high_range: Note, scale: Scale) -> List[Note]:
    notes_by_index = {}

    if not (low_range.octave and high_range.octave):
        raise Exception("Invalid range")

    for octave, note in product(range(low_range.octave - 1, high_range.octave + 1), scale.notes):
        note = replace(note, octave=octave)
        notes_by_index[note.midi_index] = note

    low_range_index = low_range.midi_index
    high_range_index = high_range.midi_index

    notes = [
        note
        for index, note in sorted(notes_by_index.items(), key=lambda x: x[0])
        if low_range_index <= index <= high_range_index
    ]

    return notes
