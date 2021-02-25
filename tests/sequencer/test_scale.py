from pytest import mark, raises

from beethoven.sequencer.note import Note
from beethoven.sequencer.scale import Scale


@mark.parametrize("root_note,scale_name,result_notes", [
    ("A4", "major",       "A4,B4,C#5,D5,E5,F#5,G#5"),
    ("B4", "minor",       "B4,C#5,D5,E5,F#5,G5,A5"),
    ("D4", "phrygian #6", "D4,Eb4,F4,G4,A4,B4,C5"),
    ("F4", "whole tone",  "F4,G4,A4,B4,Db5,Eb5")
])
def test_scale(root_note, scale_name, result_notes):
    scale = Scale(root_note, scale_name)

    assert scale.notes == Note.to_list(result_notes)


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
