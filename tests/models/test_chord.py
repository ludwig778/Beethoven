from pytest import mark, raises

from beethoven.models import Chord, Degree, Interval, Note
from tests.fixtures.scales import c_major


@mark.parametrize(
    "string,expected_obj,expected_notes,expected_intervals",
    [
        [
            "A",
            Chord(
                root=Note(name="A"),
                name="maj",
            ),
            [
                Note(name="A"),
                Note(name="C", alteration=1),
                Note(name="E"),
            ],
            [
                Interval(name="1"),
                Interval(name="3"),
                Interval(name="5"),
            ],
        ],
        [
            "B_min_maj7",
            Chord(
                root=Note(name="B"),
                name="min maj7",
            ),
            [
                Note(name="B"),
                Note(name="D"),
                Note(name="F", alteration=1),
                Note(name="A", alteration=1),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="5"),
                Interval(name="7"),
            ],
        ],
        [
            "C4_min6",
            Chord(
                root=Note(name="C", octave=4),
                name="min6",
            ),
            [
                Note(name="C", octave=4),
                Note(name="E", alteration=-1, octave=4),
                Note(name="G", octave=4),
                Note(name="A", octave=4),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="5"),
                Interval(name="6"),
            ],
        ],
        [
            "D4_min7:b=B",
            Chord(
                root=Note(name="D", octave=4),
                name="min7",
                base_note=Note(name="B"),
            ),
            [
                Note(name="B", octave=3),
                Note(name="D", octave=4),
                Note(name="F", octave=4),
                Note(name="A", octave=4),
                Note(name="C", octave=5),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
        [
            "E_7:e=9,11",
            Chord(
                root=Note(name="E"),
                name="7",
                extensions=[
                    Interval(name="9"),
                    Interval(name="11"),
                ],
            ),
            [
                Note(name="E"),
                Note(name="G", alteration=1),
                Note(name="B"),
                Note(name="D"),
                Note(name="F", alteration=1),
                Note(name="A"),
            ],
            [
                Interval(name="1"),
                Interval(name="3"),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
        [
            "F_maj:i=1",
            Chord(
                root=Note(name="F"),
                name="maj",
                inversion=1,
            ),
            [
                Note(name="A"),
                Note(name="C"),
                Note(name="F"),
            ],
            [
                Interval(name="1"),
                Interval(name="3"),
                Interval(name="5"),
            ],
        ],
        [
            "G#4_dim7:i=2:b=E:e=9m",
            Chord(
                root=Note(name="G", alteration=1, octave=4),
                name="dim7",
                inversion=2,
                base_note=Note(name="E"),
                extensions=[
                    Interval(name="9", alteration=-1),
                ],
            ),
            [
                Note(name="E", alteration=0, octave=4),
                Note(name="D", alteration=0, octave=5),
                Note(name="F", alteration=0, octave=5),
                Note(name="G", alteration=1, octave=5),
                Note(name="A", alteration=0, octave=5),
                Note(name="B", alteration=0, octave=5),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="5", alteration=-1),
                Interval(name="7", alteration=-2),
            ],
        ],
    ],
)
def test_chord_parsing(string, expected_obj, expected_notes, expected_intervals):
    chord = Chord.parse(string)

    assert chord == expected_obj
    assert chord.notes == expected_notes
    assert chord.intervals == expected_intervals


@mark.parametrize(
    "string,scale,expected_obj,expected_notes,expeceted_intervals",
    [
        [
            "I",
            c_major,
            Chord(
                root=Note(name="C"),
                name="maj7",
                degree=Degree(name="I"),
            ),
            [
                Note(name="C"),
                Note(name="E"),
                Note(name="G"),
                Note(name="B"),
            ],
            [
                Interval(name="1"),
                Interval(name="3"),
                Interval(name="5"),
                Interval(name="7"),
            ],
        ],
        [
            "bII",
            c_major,
            Chord(
                root=Note(name="D", alteration=-1),
                name="min7",
                degree=Degree(name="II", alteration=-1),
            ),
            [
                Note(name="D", alteration=-1),
                Note(name="F", alteration=-1),
                Note(name="A", alteration=-1),
                Note(name="C", alteration=-1),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
        [
            "V:s=V",
            c_major,
            Chord(
                root=Note(name="D"),
                name="7",
                degree=Degree(name="V"),
                base_degree=Degree(name="V"),
            ),
            [
                Note(name="D"),
                Note(name="F", alteration=1),
                Note(name="A"),
                Note(name="C"),
            ],
            [
                Interval(name="1"),
                Interval(name="3"),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
    ],
)
def test_chord_parsing_with_scale_context(
    string, scale, expected_obj, expected_notes, expeceted_intervals
):
    chord = Chord.parse_with_scale_context(string, scale)

    assert chord == expected_obj
    assert chord.notes == expected_notes
    assert chord.intervals == expeceted_intervals


def test_chord_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Chord(root=Note(name="C"), name="fake")
