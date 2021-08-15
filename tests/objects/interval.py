from pytest import mark

from beethoven.factories import get_notes_interval
from beethoven.objects import Interval
from beethoven.utils.factory import factory


@mark.parametrize("string,interval", [
    ("1",   Interval("1")),
    ("3",   Interval("3")),
    ("3M",  Interval("3")),
    ("5",   Interval("5")),
    ("8",   Interval("8")),
    ("3m",  Interval("3", alteration=-1)),
    ("3d",  Interval("3", alteration=-2)),
    ("4d",  Interval("4", alteration=-1)),
    ("4a",  Interval("4", alteration=1)),
    ("4aa", Interval("4", alteration=2)),
])
def test_interval_parsing(string, interval):
    assert factory("interval", string) == interval


@mark.parametrize("note1,note2,interval", [
    ("A",  "A",   "1"),
    ("A",  "A#",  "1a"),
    ("A",  "B",   "2"),
    ("A",  "C",   "3m"),
    ("B",  "E",   "4"),
    ("C",  "Gb",  "5d"),
    ("C",  "G",   "5"),
    ("C#", "A",   "6m"),
    ("C#", "A#",  "6"),
    ("D",  "Cb",  "7d"),
    ("D",  "C",   "7m"),
    ("D",  "C#",  "7"),
    ("E2", "E3",  "8"),
    ("F3", "D#5", "13a"),
    ("G4", "G6",  "15"),
])
def test_get_notes_interval(note1, note2, interval):
    note1 = factory("note", note1)
    note2 = factory("note", note2)
    interval = factory("interval", interval)

    assert get_notes_interval(note1, note2) == interval


"""
def test_interval_parsing_exception():
    assert factories.interval.parse("F#b") is None
    assert factories.interval.parse("empty") is None
"""
