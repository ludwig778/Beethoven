from pytest import mark

from beethoven import parsers
from beethoven.models import Bpm


@mark.parametrize(
    "string,expected",
    [["20", Bpm(value=20)], ["60", Bpm(value=60)], ["120", Bpm(value=120)]],
)
def test_bpm_parser(string, expected):
    assert parsers.bpm.parse(string) == expected
