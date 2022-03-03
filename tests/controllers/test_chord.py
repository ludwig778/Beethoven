from pytest import mark

from beethoven.controllers import ChordController
from beethoven.models import Chord, Interval, Note
from beethoven.models.degree import Degree
from tests.fixtures.scales import c_major


@mark.parametrize(
    "string,expected",
    [
        [
            "A",
            Chord(
                root=Note(name="A"),
                name="maj",
                notes=[
                    Note(name="A"),
                    Note(name="C", alteration=1),
                    Note(name="E"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
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
            "D4_min7:b=B",
            Chord(
                root=Note(name="D", octave=4),
                name="min7",
                notes=[
                    Note(name="B", octave=3),
                    Note(name="D", octave=4),
                    Note(name="F", octave=4),
                    Note(name="A", octave=4),
                    Note(name="C", octave=5),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
                base_note=Note(name="B", octave=3),
            ),
        ],
        [
            "E_7:e=9,11",
            Chord(
                root=Note(name="E"),
                name="7",
                notes=[
                    Note(name="E"),
                    Note(name="G", alteration=1),
                    Note(name="B"),
                    Note(name="D"),
                    Note(name="F", alteration=1),
                    Note(name="A"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
                extensions=[
                    Interval(name="9"),
                    Interval(name="11"),
                ],
            ),
        ],
        [
            "F_maj:i=1",
            Chord(
                root=Note(name="F"),
                name="maj",
                notes=[
                    Note(name="A"),
                    Note(name="C"),
                    Note(name="F"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
                ],
                inversion=1,
            ),
        ],
        [
            "G#4_dim7:i=2:b=E:e=9m",
            Chord(
                root=Note(name="G", alteration=1, octave=4),
                name="dim7",
                notes=[
                    Note(name="E", alteration=0, octave=4),
                    Note(name="D", alteration=0, octave=5),
                    Note(name="F", alteration=0, octave=5),
                    Note(name="G", alteration=1, octave=5),
                    Note(name="A", alteration=0, octave=5),
                    Note(name="B", alteration=0, octave=5),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="5", alteration=-1),
                    Interval(name="7", alteration=-2),
                ],
                inversion=2,
                base_note=Note(name="E", octave=4),
                extensions=[
                    Interval(name="9", alteration=-1),
                ],
            ),
        ],
    ],
)
def test_chord_controller_parse(string, expected):
    assert ChordController.parse(string) == expected


@mark.parametrize(
    "string,scale,expected",
    [
        [
            "I",
            c_major,
            Chord(
                root=Note(name="C"),
                name="maj7",
                notes=[
                    Note(name="C"),
                    Note(name="E"),
                    Note(name="G"),
                    Note(name="B"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
                    Interval(name="7"),
                ],
                degree=Degree(name="I"),
            ),
        ],
        [
            "bII",
            c_major,
            Chord(
                root=Note(name="D", alteration=-1),
                name="min7",
                notes=[
                    Note(name="D", alteration=-1),
                    Note(name="F", alteration=-1),
                    Note(name="A", alteration=-1),
                    Note(name="C", alteration=-1),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
                degree=Degree(name="II", alteration=-1),
            ),
        ],
        [
            "V:s=V",
            c_major,
            Chord(
                root=Note(name="D"),
                name="7",
                notes=[
                    Note(name="D"),
                    Note(name="F", alteration=1),
                    Note(name="A"),
                    Note(name="C"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3"),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
                degree=Degree(name="V"),
                base_degree=Degree(name="V"),
            ),
        ],
    ],
)
def test_chord_controller_parse_with_scale_context(string, scale, expected):
    assert ChordController.parse_with_scale_context(string, scale) == expected
