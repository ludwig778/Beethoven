from beethoven.sequencer.chord import Chord
from beethoven.sequencer.interval import OCTAVE
from beethoven.sequencer.note import Note
from beethoven.sequencer.scale import Scale
from beethoven.theory.chord import Chord as TheoryChord


def adapt_chord_to_sequencer(chord, range):
    low_range, high_range = range

    if isinstance(chord, TheoryChord):
        chord_data = chord.to_dict()
        root = chord_data.pop("root_note")

        chord = Chord(root_note=Note.cast_from_theory(root), **chord_data)

    if chord.root < low_range:
        while chord.root < low_range:
            chord.root += OCTAVE

    chord = Chord(chord.root, chord.name.short, chord.inversion, chord.base_note)

    return [
        note
        for note in chord.notes
        if note <= high_range
    ]


def get_all_notes(scale, note_range):
    low_range, high_range = note_range

    return [
        note
        for octave in range(low_range.octave, high_range.octave + 1)
        for note in Scale(f"C{octave}", str(scale.name)).notes
        if (note >= low_range and note <= high_range)
    ]
