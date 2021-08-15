from pytest import mark

from beethoven.objects import Bpm, Grid, GridPart, TimeSignature
from beethoven.utils.factory import factory


@mark.parametrize("string,grid", [
    (
        "p=A_maj7,G_7",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "A_maj7"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=None
                ),
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "G_7"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=None
                )
            ]
        )
    ),
    (
        "sc=A p=A_dim7",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "A"),
                    chord=factory("chord", "A_dim7"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=None
                )
            ]
        )
    ),
    (
        "bpm=90 ts=7/8 sc=A p=A",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "A"),
                    chord=factory("chord", "A"),
                    bpm=Bpm(90),
                    time_signature=TimeSignature(7, 8),
                    duration=None
                )
            ]
        )
    ),
    (
        "p=A:d=W,B:d=1/3Q,C",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "A"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=factory("duration", "W"),
                ),
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "B"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=factory("duration", "1/3Q"),
                ),
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "C"),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=None
                )
            ]
        )
    ),
    (
        "p=I",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "C"),
                    chord=factory("chord", "I", scale=factory("scale", "C")),
                    bpm=Bpm(120),
                    time_signature=TimeSignature(4, 4),
                    duration=None
                )
            ]
        )
    ),
    (
        "bpm=60 ts=3/2 sc=C_dorian p=I; bpm=80 ts=3/8 sc=D_lydian p=V",
        Grid(
            parts=[
                GridPart(
                    scale=factory("scale", "C_dorian"),
                    chord=factory("chord", "I", scale=factory("scale", "C_dorian")),
                    bpm=Bpm(60),
                    time_signature=TimeSignature(3, 2),
                    duration=None
                ),
                GridPart(
                    scale=factory("scale", "D_lydian"),
                    chord=factory("chord", "V", scale=factory("scale", "D_lydian")),
                    bpm=Bpm(80),
                    time_signature=TimeSignature(3, 8),
                    duration=None
                )
            ]
        )
    )
])
def test_grid_parsing(string, grid):
    default_settings = {
        "scale": factory("scale", "C"),
        "time_signature": factory("time_signature", "4/4"),
        "bpm": factory("bpm", "120")
    }

    assert factory("grid", string, default_settings=default_settings) == grid
