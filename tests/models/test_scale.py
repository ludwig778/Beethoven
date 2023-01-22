from pytest import mark, raises

from beethoven.models import Interval, Note, Scale
from tests.fixtures.chords import c_major_7th_chords
from tests.fixtures.scales import a_minor, a_minor_pentatonic, c_major


@mark.parametrize(
    "string,expected_obj,expected_notes,expected_intervals",
    [
        [
            "A_major",
            Scale(tonic=Note(name="A"), name="major"),
            [
                Note(name="A"),
                Note(name="B"),
                Note(name="C", alteration=1),
                Note(name="D"),
                Note(name="E"),
                Note(name="F", alteration=1),
                Note(name="G", alteration=1),
            ],
            [
                Interval(name="1"),
                Interval(name="2"),
                Interval(name="3"),
                Interval(name="4"),
                Interval(name="5"),
                Interval(name="6"),
                Interval(name="7"),
            ],
        ],
        [
            "B_pentatonic_minor",
            Scale(tonic=Note(name="B"), name="pentatonic minor"),
            [
                Note(name="B"),
                Note(name="D"),
                Note(name="E"),
                Note(name="F", alteration=1),
                Note(name="A"),
            ],
            [
                Interval(name="1"),
                Interval(name="3", alteration=-1),
                Interval(name="4"),
                Interval(name="5"),
                Interval(name="7", alteration=-1),
            ],
        ],
        [
            "C4_lydian",
            Scale(tonic=Note(name="C", octave=4), name="lydian"),
            [
                Note(name="C", octave=4),
                Note(name="D", octave=4),
                Note(name="E", octave=4),
                Note(name="F", alteration=1, octave=4),
                Note(name="G", octave=4),
                Note(name="A", octave=4),
                Note(name="B", octave=4),
            ],
            [
                Interval(name="1"),
                Interval(name="2"),
                Interval(name="3"),
                Interval(name="4", alteration=1),
                Interval(name="5"),
                Interval(name="6"),
                Interval(name="7"),
            ],
        ],
    ],
)
def test_scale_parsing(string, expected_obj, expected_notes, expected_intervals):
    scale = Scale.parse(string)

    assert scale == expected_obj
    assert scale.notes == expected_notes
    assert scale.intervals == expected_intervals


def test_scale_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: fake"):
        Scale(tonic=Note(name="C"), name="fake")


def test_scale_model_is_diatonic():
    assert a_minor.is_diatonic
    assert not a_minor_pentatonic.is_diatonic


def test_scale_get_diatonic_chords():
    assert c_major.get_diatonic_chords() == c_major_7th_chords
