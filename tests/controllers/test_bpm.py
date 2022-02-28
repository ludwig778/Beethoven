from pytest import mark

from beethoven.controllers import BpmController
from beethoven.models import Bpm


@mark.parametrize(
    "string,expected",
    [["20", Bpm(value=20)], ["60", Bpm(value=60)], ["120", Bpm(value=120)]],
)
def test_bpm_controller_parse(string, expected):
    assert BpmController.parse(string) == expected
