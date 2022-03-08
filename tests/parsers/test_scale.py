from pytest import mark

from beethoven import parsers
from beethoven.models import Interval, Note, Scale


@mark.parametrize(
    "string,expected",
    [
        [
            "A_major",
            Scale(
                tonic=Note(name="A"),
                name="major",
                notes=[
                    Note(name="A"),
                    Note(name="B"),
                    Note(name="C", alteration=1),
                    Note(name="D"),
                    Note(name="E"),
                    Note(name="F", alteration=1),
                    Note(name="G", alteration=1),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="2"),
                    Interval(name="3"),
                    Interval(name="4"),
                    Interval(name="5"),
                    Interval(name="6"),
                    Interval(name="7"),
                ],
            ),
        ],
        [
            "B_pentatonic_minor",
            Scale(
                tonic=Note(name="B"),
                name="pentatonic_minor",
                notes=[
                    Note(name="B"),
                    Note(name="D"),
                    Note(name="E"),
                    Note(name="F", alteration=1),
                    Note(name="A"),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="3", alteration=-1),
                    Interval(name="4"),
                    Interval(name="5"),
                    Interval(name="7", alteration=-1),
                ],
            ),
        ],
        [
            "C4_lydian",
            Scale(
                tonic=Note(name="C", octave=4),
                name="lydian",
                notes=[
                    Note(name="C", octave=4),
                    Note(name="D", octave=4),
                    Note(name="E", octave=4),
                    Note(name="F", alteration=1, octave=4),
                    Note(name="G", octave=4),
                    Note(name="A", octave=4),
                    Note(name="B", octave=4),
                ],
                intervals=[
                    Interval(name="1"),
                    Interval(name="2"),
                    Interval(name="3"),
                    Interval(name="4", alteration=1),
                    Interval(name="5"),
                    Interval(name="6"),
                    Interval(name="7"),
                ],
            ),
        ],
    ],
)
def test_scale_parser(string, expected):
    assert parsers.scale.parse(string) == expected
