from pytest import mark, raises

from beethoven.exceptions import CouldNotParse, MixedAlteration
from beethoven.objects import Interval, Note


@mark.parametrize(
    "string,note",
    [
        ("A", Note("A")),
        ("B#", Note("B", alteration=1)),
        ("Cbb", Note("C", alteration=-2)),
        ("D", Note("D", octave=None)),
        ("E4", Note("E", octave=4)),
        ("F#5", Note("F", alteration=1, octave=5)),
    ],
)
def test_note_parsing(string, note):
    assert Note.parse(string) == note


@mark.parametrize(
    "string,index",
    [
        ("A", 9),
        ("B#", 0),
        ("Cbb", 10),
        ("D", 2),
        ("E4", 52),
        ("F#5", 66),
        ("C0", 0),
    ],
)
def test_note_index_property(string, index):
    assert Note.parse(string).index == index


def test_note_parsing_exception():
    with raises(MixedAlteration):
        Note.parse("F#b")

    with raises(CouldNotParse, match="Couldn't parse string='empty' as Note"):
        Note.parse("empty")

    with raises(CouldNotParse, match="Couldn't parse string='' as Note"):
        Note.parse("")


@mark.parametrize(
    "base_note,interval,target_note",
    [
        ("A", "1", "A"),
        ("B#", "3", "D##"),
        ("C", "4", "F"),
        ("D", "6", "B"),
        ("E4", "8", "E5"),
        ("F#5", "9", "G#6"),
        ("G0", "13", "E2"),
    ],
)
def test_note_adding_interval(base_note, interval, target_note):
    base_note = Note.parse(base_note)
    interval = Interval.parse(interval)
    target_note = Note.parse(target_note)

    assert base_note + interval == target_note


@mark.parametrize(
    "base_note,interval,target_note",
    [
        ("A", "1", "A"),
        ("B#", "3", "G#"),
        ("C", "4", "G"),
        ("D", "6", "F"),
        ("E4", "8", "E3"),
        ("F#5", "9", "E4"),
        ("G4", "13", "Bb2"),
    ],
)
def test_note_adding_interval_reverse(base_note, interval, target_note):
    base_note = Note.parse(base_note)
    interval = Interval.parse(interval)
    target_note = Note.parse(target_note)

    assert base_note - interval == target_note