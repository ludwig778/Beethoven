from pytest import mark

from beethoven.objects import Bpm
from beethoven.utils.factory import factory


@mark.parametrize("string,bpm", [
    ("60",  Bpm(60)),
    ("120", Bpm(120)),
])
def test_bpm_parsing(string, bpm):
    assert factory("bpm", string) == bpm
