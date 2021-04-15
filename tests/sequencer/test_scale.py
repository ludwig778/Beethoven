from pytest import mark, raises

from beethoven.sequencer.chord import Chord
from beethoven.sequencer.note import Note
from beethoven.sequencer.scale import Scale


@mark.parametrize("root_note,scale_name,result_notes", [
    ("A4", "major",       "A4,B4,C#5,D5,E5,F#5,G#5"),
    ("B4", "minor",       "B4,C#5,D5,E5,F#5,G5,A5"),
    ("D4", "phrygian #6", "D4,Eb4,F4,G4,A4,B4,C5"),
    ("F4", "whole tone",  "F4,G4,A4,B4,Db5,Eb5")
])
def test_scale_instanciation(root_note, scale_name, result_notes):
    scale = Scale(root_note, scale_name)

    assert scale.notes == Note.to_list(result_notes)


def test_scale_repr():
    assert repr(Scale("A4", "major")) == "<Scale A4 ionian>"


@mark.parametrize("scale_name", ["foo", "bar"])
def test_scale_with_wrong_scale_name(scale_name):
    with raises(ValueError, match="Scale name does not exists"):
        Scale("A4", scale_name)


@mark.parametrize("name,alt_name", [
    ('ionian',        'major'),
    ('aeolian',       'minor'),
    ('melodic minor', 'ascending melodic minor'),
])
def test_scale_notation_on_initialization(name, alt_name):
    root_note = "A4"

    notation1 = Scale(root_note, name)
    notation2 = Scale(root_note, alt_name)

    assert notation1 == notation2
    assert str(notation1) == str(notation2)


@mark.parametrize("start_degree_name,chord_basic,chord_seventh", [
    (1, Chord("B4",  "min"), Chord("B4",  "min7")),
    (2, Chord("C#5", "min"), Chord("C#5", "min7")),
    (3, Chord("D5",  "maj"), Chord("D5",  "maj7")),
    (4, Chord("E5",  "maj"), Chord("E5",  "7")),
    (6, Chord("G#5", "dim"), Chord("G#5", "min7b5")),
])
def test_scale_get_chords(start_degree_name, chord_basic, chord_seventh):
    scale = Scale("A4", "major")

    assert scale.get_chord(start_degree_name, "1,3,5") == chord_basic
    assert scale.get_chord(start_degree_name, "1,3,5,7") == chord_seventh


@mark.parametrize("start_degree_name,alteration,chord_basic,chord_seventh", [
    (1, 0,  Chord("B4",   "min"), Chord("B4",   "min7")),
    (1, 1,  Chord("B#4",  "min"), Chord("B#4",  "min7")),
    (1, 2,  Chord("B##4", "min"), Chord("B##4", "min7")),
    (1, -2, Chord("Bbb4", "min"), Chord("Bbb4", "min7")),
])
def test_scale_get_chord_with_alteration(start_degree_name, alteration, chord_basic, chord_seventh):
    scale = Scale("A4", "major")

    assert scale.get_chord(start_degree_name, "1,3,5", alteration=alteration) == chord_basic
    assert scale.get_chord(start_degree_name, "1,3,5,7", alteration=alteration) == chord_seventh
