from copy import deepcopy
from itertools import product
from typing import List

from beethoven import controllers
from beethoven.constants.interval import octave
from beethoven.helpers.note import add_interval_to_note, get_notes_interval
from beethoven.indexes import chord_index
from beethoven.models import Chord, Degree, Note, Scale


def scale_product(tonics: List[Note], scale_names: List[str]):
    return [
        controllers.scale.parse(f"{str(tonic)}_{scale_name}")
        for tonic, scale_name in product(tonics, scale_names)
    ]


def get_scale_note_from_degree(scale: Scale, degree: Degree) -> Note:
    note = deepcopy(scale.notes[degree.index])
    note.alteration += degree.alteration

    return note


def get_diatonic_scale_chords(scale: Scale) -> List[Chord]:
    chords = []

    two_octave_notes = scale.notes + [
        add_interval_to_note(note, octave) for note in scale.notes
    ]

    for degree_index in range(7):
        root = two_octave_notes[degree_index]

        notes = []
        intervals = []
        for chord_indexx in [1, 3, 5, 7]:
            note = two_octave_notes[degree_index + chord_indexx - 1]

            notes.append(note)
            intervals.append(get_notes_interval(root, note))

        intervals_str = ",".join([str(i) for i in intervals])

        chord = Chord(
            root=root,
            name=chord_index.get_name_from_intervals(intervals_str),
            notes=notes,
            intervals=intervals,
        )
        chords.append(chord)

    return chords
