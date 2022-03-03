from pytest import mark

from beethoven.helpers.note import add_interval_to_note, get_notes_interval
from beethoven.models import Interval, Note


@mark.parametrize(
    "note,interval,expected",
    [
        [Note(name="A"), Interval(name="3", alteration=-1), Note(name="C")],
        [Note(name="A", octave=3), Interval(name="8"), Note(name="A", octave=4)],
    ],
)
def test_note_helper_add_interval_to_note(note, interval, expected):
    assert add_interval_to_note(note, interval) == expected


@mark.parametrize(
    "note,interval,expected",
    [
        [
            Note(name="A"),
            Interval(name="3", alteration=-1),
            Note(name="F", alteration=1),
        ],
        [Note(name="A", octave=3), Interval(name="8"), Note(name="A", octave=2)],
    ],
)
def test_note_helper_add_interval_to_note_reversed(note, interval, expected):
    assert add_interval_to_note(note, interval, reverse=True) == expected


@mark.parametrize(
    "note1,note2,expected",
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
def test_note_helper_get_notes_interval(note1, note2, expected):
    assert get_notes_interval(note1, note2) == expected
