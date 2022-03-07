from fractions import Fraction

from pytest import mark

from beethoven import parsers
from beethoven.constants.duration import whole_value
from beethoven.helpers.model import update_model
from beethoven.models import Bpm, Degree, Duration, Grid, GridPart, TimeSignature
from tests.fixtures.chords import a_min7, c4_maj, c_maj7, d_min7, e_min7, g_7
from tests.fixtures.scales import a_minor, c_major, d_lydian


@mark.parametrize(
    "string,expected",
    [
        ["", Grid()],
        [
            "bpm=90 ts=3/4 p=C4",
            Grid(
                parts=[
                    GridPart(
                        bpm=Bpm(value=90),
                        time_signature=TimeSignature(beats_per_bar=3, beat_unit=4),
                        scale=c_major,
                        chord=c4_maj,
                        duration=None,
                    )
                ]
            ),
        ],
        [
            "p=II,V,I",
            Grid(
                parts=[
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(d_min7, degree=Degree(name="II")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(g_7, degree=Degree(name="V")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(c_maj7, degree=Degree(name="I")),
                        duration=None,
                    ),
                ]
            ),
        ],
        [
            "p=II:d=1/3Q,V:d=3/5E,I:d=W",
            Grid(
                parts=[
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(d_min7, degree=Degree(name="II")),
                        duration=Duration(value=Fraction(1, 3)),
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(g_7, degree=Degree(name="V")),
                        duration=Duration(value=Fraction(3, 10)),
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(c_maj7, degree=Degree(name="I")),
                        duration=Duration(value=whole_value),
                    ),
                ]
            ),
        ],
        [
            "sc=A_minor p=I;sc=D_lydian p=II_min7",
            Grid(
                parts=[
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=a_minor,
                        chord=update_model(a_min7, degree=Degree(name="I")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=d_lydian,
                        chord=update_model(e_min7, degree=Degree(name="II")),
                        duration=None,
                    ),
                ]
            ),
        ],
        [
            "p=II,V r=2",
            Grid(
                parts=[
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(d_min7, degree=Degree(name="II")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(g_7, degree=Degree(name="V")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(d_min7, degree=Degree(name="II")),
                        duration=None,
                    ),
                    GridPart(
                        bpm=Bpm(value=120),
                        time_signature=TimeSignature(beats_per_bar=4, beat_unit=4),
                        scale=c_major,
                        chord=update_model(g_7, degree=Degree(name="V")),
                        duration=None,
                    ),
                ]
            ),
        ],
    ],
)
def test_grid_parser(string, expected):
    assert parsers.grid.parse(string) == expected
