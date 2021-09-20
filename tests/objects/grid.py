from pytest import mark

from beethoven.objects import Bpm, Chord, Duration, Grid, GridPart, Scale, TimeSignature


@mark.parametrize(
    "string,grid",
    [
        (
            "p=A_maj7,G_7",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("A_maj7"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=None,
                    ),
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("G_7"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=None,
                    ),
                ]
            ),
        ),
        (
            "sc=A p=A_dim7",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("A"),
                        chord=Chord.parse("A_dim7"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=None,
                    )
                ]
            ),
        ),
        (
            "bpm=90 ts=7/8 sc=A p=A",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("A"),
                        chord=Chord.parse("A"),
                        bpm=Bpm(90),
                        time_signature=TimeSignature(7, 8),
                        duration=None,
                    )
                ]
            ),
        ),
        (
            "p=A:d=W,B:d=1/3Q,C",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("A"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=Duration.parse("W"),
                    ),
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("B"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=Duration.parse("1/3Q"),
                    ),
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("C"),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=None,
                    ),
                ]
            ),
        ),
        (
            "p=I",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("C"),
                        chord=Chord.parse("I", scale=Scale.parse("C")),
                        bpm=Bpm(120),
                        time_signature=TimeSignature(4, 4),
                        duration=None,
                    )
                ]
            ),
        ),
        (
            "bpm=60 ts=3/2 sc=C_dorian p=I; bpm=80 ts=3/8 sc=D_lydian p=V",
            Grid(
                parts=[
                    GridPart(
                        scale=Scale.parse("C_dorian"),
                        chord=Chord.parse("I", scale=Scale.parse("C_dorian")),
                        bpm=Bpm(60),
                        time_signature=TimeSignature(3, 2),
                        duration=None,
                    ),
                    GridPart(
                        scale=Scale.parse("D_lydian"),
                        chord=Chord.parse("V", scale=Scale.parse("D_lydian")),
                        bpm=Bpm(80),
                        time_signature=TimeSignature(3, 8),
                        duration=None,
                    ),
                ]
            ),
        ),
    ],
)
def test_grid_parsing(string, grid):
    default_settings = {
        "scale": Scale.parse("C"),
        "time_signature": TimeSignature.parse("4/4"),
        "bpm": Bpm.parse("120"),
    }

    assert Grid.parse(string, default_settings=default_settings) == grid
