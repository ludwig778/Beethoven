from pytest import mark

from beethoven import controllers
from beethoven.models import Bpm


@mark.parametrize(
    "string,expected",
    [["20", Bpm(value=20)], ["60", Bpm(value=60)], ["120", Bpm(value=120)]],
)
def test_bpm_parser(string, expected):
    assert controllers.bpm.parse(string) == expected
