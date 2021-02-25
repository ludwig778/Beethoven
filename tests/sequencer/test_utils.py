from pytest import mark

from beethoven.sequencer.chord import Chord
from beethoven.sequencer.note import Note
from beethoven.sequencer.utils import adapt_chord_to_sequencer, get_all_notes
from beethoven.theory.scale import Scale


@mark.parametrize("chord,note_range,expected", [
    (Chord("C1", "maj"),  "C3,C6", "C3,E3,G3"),
    (Chord("C2", "maj"),  "C3,C6", "C3,E3,G3"),
    (Chord("C3", "maj"),  "C4,C6", "C4,E4,G4"),
    (Chord("C4", "maj"),  "C4,C6", "C4,E4,G4"),
    (Chord("C5", "maj"),  "C4,C6", "C5,E5,G5"),
    (Chord("C6", "maj"),  "C5,F6", "C6,E6"),
    (Chord("A4", "maj7"), "C4,C6", "A4,C#5,E5,G#5"),
    (Chord("A4", "maj7"), "C4,E5", "A4,C#5,E5"),
])
def test_adapt_chord_to_sequencer(chord, note_range, expected):
    assert (
        adapt_chord_to_sequencer(
            chord,
            Note.to_list(note_range)
        ) == Note.to_list(expected)
    )


@mark.parametrize("scale,note_range,expected", [
    (Scale("C3", "major"), "C3,C4", "C3,D3,E3,F3,G3,A3,B3,C4"),
    (Scale("C3", "major"), "E3,E4", "E3,F3,G3,A3,B3,C4,D4,E4"),
    (Scale("C3", "major"), "C3,C5", "C3,D3,E3,F3,G3,A3,B3,C4,D4,E4,F4,G4,A4,B4,C5"),
])
def test_get_all_notes(scale, note_range, expected):
    assert (
        get_all_notes(
            scale,
            Note.to_list(note_range)
        ) == Note.to_list(expected)
    )
