from pytest import mark

from beethoven.controllers import ChordController
from beethoven.models import Chord, Interval, Note, interval


@mark.parametrize(
    "string,expected",
    [
        [
            "A_maj7",
            Chord(
                root=Note(name="A"),
                name="maj7",
                notes=[
                    Note(name="A"),
                    Note(name="C", alteration=1),
                    Note(name="E"),
                    Note(name="G", alteration=1),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
                    Interval(name="7"),
                ],
            ),
        ],
        [
            "B_sus4",
            Chord(
                root=Note(name="B"),
                name="sus4",
                notes=[
                    Note(name="B"),
                    Note(name="E"),
                    Note(name="F", alteration=1),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="4"),
                    Interval(name="5"),
                ],
            ),
        ],
        [
            "C4_min6",
            Chord(
                root=Note(name="C", octave=4),
                name="min6",
                notes=[
                    Note(name="C", octave=4),
                    Note(name="E", alteration=-1, octave=4),
                    Note(name="G", octave=4),
                    Note(name="A", octave=4),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="5"),
                    Interval(name="6"),
                ],
            ),
        ],
        [
            "D5_min7",
            Chord(
                root=Note(name="D", octave=5),
                name="min7",
                notes=[
                    Note(name="D", octave=5),
                    Note(name="F", octave=5),
                    Note(name="A", octave=5),
                    Note(name="C", octave=6),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
            ),
        ],
    ],
)
def test_chord_controller_parse(string, expected):
    assert ChordController.parse(string) == expected
