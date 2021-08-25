from pytest import mark

from beethoven.objects import Bpm


@mark.parametrize("string,bpm", [
    ("60",  Bpm(60)),
    ("120", Bpm(120)),
])
def test_bpm_parsing(string, bpm):
    assert Bpm.parse(string) == bpm
