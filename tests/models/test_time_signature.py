from pytest import mark

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
