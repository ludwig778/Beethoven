from pytest import mark

from beethoven.controllers import NoteController
from beethoven.models import Note


@mark.parametrize(
    "string,expected",
    [
        ["A", Note(name="A")],
        ["B", Note(name="B")],
        ["C#", Note(name="C", alteration=1)],
        ["Db", Note(name="D", alteration=-1)],
        ["E###", Note(name="E", alteration=3)],
        ["Fbbb", Note(name="F", alteration=-3)],
        ["G#4", Note(name="G", alteration=1, octave=4)],
    ],
)
def test_note_controller_parse(string, expected):
    assert NoteController.parse(string) == expected


@mark.parametrize(
    "string,expected",
    [
        [
            "C,D,E,F,G,A,B",
            [
                Note(name="C"),
                Note(name="D"),
                Note(name="E"),
                Note(name="F"),
                Note(name="G"),
                Note(name="A"),
                Note(name="B"),
            ],
        ],
        [
            "A,B,C#,D,E,F#,G#",
            [
                Note(name="A"),
                Note(name="B"),
                Note(name="C", alteration=1),
                Note(name="D"),
                Note(name="E"),
                Note(name="F", alteration=1),
                Note(name="G", alteration=1),
            ],
        ],
        [
            "E4,F#4,G4,A4,B4,C5,D5",
            [
                Note(name="E", octave=4),
                Note(name="F", alteration=1, octave=4),
                Note(name="G", octave=4),
                Note(name="A", octave=4),
                Note(name="B", octave=4),
                Note(name="C", octave=5),
                Note(name="D", octave=5),
            ],
        ],
    ],
)
def test_note_controller_parse_list(string, expected):
    assert NoteController.parse_list(string) == expected
