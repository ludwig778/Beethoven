from pytest import mark

from beethoven.models import Bpm


@mark.parametrize("value", [60, 120])
def test_bpm_model(value):
    assert Bpm(value=value)
