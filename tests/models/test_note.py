from pytest import mark, raises

from beethoven.models import Interval, Note


@mark.parametrize(
    "string,expected_obj",
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
def test_note_parsing(string, expected_obj):
    assert Note.parse(string) == expected_obj


@mark.parametrize(
    "string,expected_obj",
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
def test_note_list_parsing(string, expected_obj):
    assert Note.parse_list(string) == expected_obj


def test_note_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: H"):
        Note(name="H")


@mark.parametrize("alteration", [-5, 5])
def test_note_model_raise_invalid_alteration(alteration):
    with raises(ValueError, match=f"Invalid alteration: {alteration}, must be between -4 and 4"):
        Note(name="C", alteration=alteration)


@mark.parametrize("octave", [-1, 11])
def test_note_model_raise_invalid_octave(octave):
    with raises(ValueError, match=f"Invalid octave: {octave}, must be between 0 and 10"):
        Note(name="C", octave=octave)


def test_note_model_greater_equality_methods():
    assert Note(name="C") == Note(name="C")
    assert Note(name="C", alteration=1) == Note(name="C", alteration=1)
    assert Note(name="C", alteration=1, octave=4) == Note(name="C", alteration=1, octave=4)

    assert Note(name="C") != Note(name="C", alteration=1)

    # Check enharmonic notes
    assert Note(name="C") == Note(name="D", alteration=-2)


def test_note_model_greater_equality_methods_raise_octave_state_discrepancy():
    with raises(Exception, match="Octaves must be present or absent in order to compare Notes"):
        Note(name="C") == Note(name="C", octave=1)


def test_note_model_greater_than_method():
    assert Note(name="C") < Note(name="B")
    assert Note(name="C", octave=1) > Note(name="B", octave=0)
    assert Note(name="C", octave=1) < Note(name="B", octave=1)

    assert Note(name="C") <= Note(name="D")
    assert Note(name="C") <= Note(name="B")


@mark.parametrize(
    "note,interval,expected_note",
    [
        [Note(name="A"), Interval(name="3", alteration=-1), Note(name="C")],
        [Note(name="A", octave=3), Interval(name="8"), Note(name="A", octave=4)],
    ],
)
def test_note_add_interval(note, interval, expected_note):
    assert note.add_interval(interval) == expected_note


@mark.parametrize(
    "note,interval,expected_note",
    [
        [
            Note(name="A"),
            Interval(name="3", alteration=-1),
            Note(name="F", alteration=1),
        ],
        [Note(name="A", octave=3), Interval(name="8"), Note(name="A", octave=2)],
    ],
)
def test_note_add_interval_reversed(note, interval, expected_note):
    assert note.add_interval(interval, reverse=True) == expected_note


@mark.parametrize(
    "note1,note2,expected_interval",
    [
        [Note(name="A"), Note(name="E"), Interval(name="5")],
        [
            Note(name="C", alteration=-2),
            Note(name="G"),
            Interval(name="5", alteration=2),
        ],
        [
            Note(name="C", alteration=-1),
            Note(name="G", alteration=1),
            Interval(name="5", alteration=2),
        ],
        [Note(name="A", octave=2), Note(name="A", octave=3), Interval(name="8")],
        [Note(name="A", octave=2), Note(name="A", octave=4), Interval(name="15")],
    ],
)
def test_note_get_interval(note1, note2, expected_interval):
    assert note1.get_interval(note2) == expected_interval


@mark.parametrize(
    "note,expected_note",
    [
        (Note(name="A"), Note(name="A")),
        (Note(name="C", octave=4), Note(name="C")),
        (Note(name="E", octave=3), Note(name="E")),
    ],
)
def test_note_remove_octave(note, expected_note):
    assert note.remove_octave() == expected_note


def test_note_remove_notes_octave():
    assert Note.remove_notes_octave(
        [
            Note(name="A"),
            Note(name="C", octave=4),
            Note(name="E", octave=3),
        ]
    ) == [
        Note(name="A"),
        Note(name="C"),
        Note(name="E"),
    ]
