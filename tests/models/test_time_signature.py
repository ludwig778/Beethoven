from pytest import mark, raises

from beethoven.models import TimeSignature


@mark.parametrize(
    "beats_per_bar,beat_unit",
    [
        [4, 4],
        [5, 16],
    ],
)
def test_time_signature_model(beats_per_bar, beat_unit):
    assert TimeSignature(beats_per_bar=beats_per_bar, beat_unit=beat_unit)


@mark.parametrize("beat_unit", [0, 64])
def test_time_signature_model_raise_out_of_bound_beat_unit(beat_unit):
    with raises(
        ValueError, match=f"Invalid beat_unit: {beat_unit}, must be in range 1-32"
    ):
        TimeSignature(beats_per_bar=4, beat_unit=beat_unit)


@mark.parametrize("beat_unit", [3, 7])
def test_time_signature_model_raise_invalid_beat_unit(beat_unit):
    with raises(
        ValueError, match=f"Invalid beat_unit: {beat_unit}, must be a multiple of 2"
    ):
        TimeSignature(beats_per_bar=4, beat_unit=beat_unit)
