from pytest import mark

from beethoven.sequencer.chord import Chord
from beethoven.sequencer.note import Note


@mark.parametrize("start_note,chord_name,expected_notes", [
    ("A4", "maj",      "A4,C#5,E5"),
    ("B5", "min",      "B5,D6,F#6"),
    ("G4", "dim7",     "G4,Bb4,Db5,Fb5"),
    ("C4", "7",        "C4,E4,G4,Bb4"),
    ("D4", "min maj7", "D4,F4,A4,C#5")
])
def test_interval_check_display(start_note, chord_name, expected_notes):
    assert Chord(start_note, chord_name).notes == [Note(note_name) for note_name in expected_notes.split(",")]
