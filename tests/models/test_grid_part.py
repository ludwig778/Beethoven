from fractions import Fraction

from pytest import mark

from beethoven.models import Bpm, Chord, Duration, GridPart, Note, Scale, TimeSignature


@mark.parametrize(
    "part_attributes",
    [
        {
            "scale": Scale(tonic=Note(name="C"), name="major"),
            "chord": Chord(root=Note(name="D"), name="maj7"),
            "bpm": Bpm(value=90),
            "time_signature": TimeSignature(beats_per_bar=4, beat_unit=4),
            "duration": Duration(value=Fraction(1)),
        },
        {
            "scale": Scale(tonic=Note(name="E"), name="lydian"),
            "chord": Chord(root=Note(name="B"), name="min7"),
            "bpm": Bpm(value=120),
            "time_signature": TimeSignature(beats_per_bar=5, beat_unit=8),
            "duration": Duration(value=Fraction(3, 2)),
        },
    ],
)
def test_grid_part_model(part_attributes):
    assert GridPart(**part_attributes)
