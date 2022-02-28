from pytest import mark

from beethoven.controllers import TimeSignatureController
from beethoven.models import TimeSignature


@mark.parametrize(
    "string,expected",
    [
        ["4/4", TimeSignature(beats_per_bar=4, beat_unit=4)],
        ["3/2", TimeSignature(beats_per_bar=3, beat_unit=2)],
        ["7/8", TimeSignature(beats_per_bar=7, beat_unit=8)],
        ["5/16", TimeSignature(beats_per_bar=5, beat_unit=16)],
    ],
)
def test_time_signature_controller_parse(string, expected):
    assert TimeSignatureController.parse(string) == expected
