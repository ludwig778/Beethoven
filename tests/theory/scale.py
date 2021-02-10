from pytest import mark, raises

from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


def to_list(notes):
    return [Note(n) for n in notes.split(",")]


@mark.parametrize("root_note,scale_name,result_notes", [
    ("A", "major",            "A,B,C#,D,E,F#,G#"),
    ("B", "minor",            "B,C#,D,E,F#,G,A"),
    ("D", "phrygian #6",      "D,Eb,F,G,A,B,C"),
    ("F", "whole tone scale", "F,G,A,B,Db,Eb")
])
def test_scale(root_note, scale_name, result_notes):
    scale = Scale(root_note, scale_name)

    assert scale.notes == to_list(result_notes)


@mark.parametrize("scale_name", ["foo", "bar"])
def test_scale_with_wrong_scale_name(scale_name):
    with raises(ValueError, match="Scale name does not exists"):
        Scale("A", scale_name)


@mark.parametrize("name,alt_name", [
    ('ionian', 'major'),
    ('aeolian', 'minor'),
    ('melodic minor', 'ascending melodic minor'),
])
def test_scale_notation_on_initialization(name, alt_name):
    root_note = "A"

    notation1 = Scale(root_note, name)
    notation2 = Scale(root_note, alt_name)

    assert notation1 == notation2
    assert str(notation1) == str(notation2)
