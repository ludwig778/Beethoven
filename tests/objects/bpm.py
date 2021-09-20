from pytest import mark, raises

from beethoven.exceptions import BpmCantBeZero
from beethoven.objects import Bpm


@mark.parametrize(
    "string,bpm",
    [
        ("60", Bpm(60)),
        ("120", Bpm(120)),
    ],
)
def test_bpm_parsing(string, bpm):
    assert Bpm.parse(string) == bpm


def test_bpm_parsing_exception():
    with raises(BpmCantBeZero, match="Value can't be equal to 0"):
        Bpm.parse("0")


def test_bpm_parsing_serialize():
    string = "30"

    assert Bpm.parse(string).serialize() == string
