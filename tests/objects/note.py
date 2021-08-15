from pytest import mark, raises

from beethoven.factories import add_interval_to_note
from beethoven.objects import Note
from beethoven.utils.factory import factory


@mark.parametrize("string,note", [
    ("A",   Note("A")),
    ("B#",  Note("B", alteration=1)),
    ("Cbb", Note("C", alteration=-2)),
    ("D",   Note("D", octave=None)),
    ("E4",  Note("E", octave=4)),
    ("F#5", Note("F", alteration=1, octave=5)),
])
def test_note_parsing(string, note):
    assert factory("note", string) == note


def test_note_parsing_exception():
    with raises(Exception, match="Mixed alteration"):
        factory("note", "F#b")

    with raises(Exception, match="Couldn't parse string='empty' as Note"):
        factory("note", "empty")


@mark.parametrize("base_note,interval,target_note", [
    ("A",   "1",  "A"),
    ("B#",  "3",  "D##"),
    ("C",   "4",  "F"),
    ("D",   "6",  "B"),
    ("E4",  "8",  "E5"),
    ("F#5", "9",  "G#6"),
    ("G0", "13",  "E2"),
])
def test_note_adding_interval(base_note, interval, target_note):
    base_note = factory("note", base_note)
    interval = factory("interval", interval)
    target_note = factory("note", target_note)

    assert add_interval_to_note(base_note, interval) == target_note


@mark.parametrize("base_note,interval,target_note", [
    ("A",   "1",  "A"),
    ("B#",  "3",  "G#"),
    ("C",   "4",  "G"),
    ("D",   "6",  "F"),
    ("E4",  "8",  "E3"),
    ("F#5", "9",  "E4"),
    ("G4",  "13",  "Bb2"),
])
def test_note_adding_interval_reverse(base_note, interval, target_note):
    base_note = factory("note", base_note)
    interval = factory("interval", interval)
    target_note = factory("note", target_note)

    assert add_interval_to_note(base_note, interval, reverse=True) == target_note
