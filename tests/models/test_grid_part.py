from fractions import Fraction

from pytest import mark

from beethoven.models import Bpm, Chord, Duration, GridPart, Note, Scale, TimeSignature


@mark.parametrize(
    "scale,chord,bpm,time_signature,duration",
    [
        [
            Scale(tonic=Note(name="C"), name="major"),
            Chord(root=Note(name="D"), name="maj7"),
            Bpm(value=90),
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=Fraction(1)),
        ],
        [
            Scale(tonic=Note(name="E"), name="lydian"),
            Chord(root=Note(name="B"), name="min7"),
            Bpm(value=120),
            TimeSignature(beats_per_bar=5, beat_unit=8),
            Duration(value=Fraction(3, 2)),
        ],
    ],
)
def test_grid_part_model(scale, chord, bpm, time_signature, duration):
    assert GridPart(
        scale=scale,
        chord=chord,
        bpm=bpm,
        time_signature=time_signature,
        duration=duration,
    )
