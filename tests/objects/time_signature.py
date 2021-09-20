from pytest import mark, raises

from beethoven.objects import TimeSignature
from beethoven.exceptions import BeatsPerBarCantBeZero, BeatUnitIsInvalid


@mark.parametrize(
    "string,time_signature",
    [
        ("4/4", TimeSignature(4, 4)),
        ("3/2", TimeSignature(3, 2)),
        ("12/8", TimeSignature(12, 8)),
        ("15/16", TimeSignature(15, 16)),
    ],
)
def test_time_signature_parsing(string, time_signature):
    assert TimeSignature.parse(string) == time_signature


def test_time_signature_parsing_exception():
    with raises(BeatUnitIsInvalid):
        TimeSignature.parse("4/0")

    with raises(BeatUnitIsInvalid):
        TimeSignature.parse("4/5")

    with raises(BeatsPerBarCantBeZero):
        TimeSignature.parse("0/4")


def test_time_signature_serialize():
    string = "15/16"

    assert TimeSignature.parse(string).serialize() == string
