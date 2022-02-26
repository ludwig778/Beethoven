from pytest import mark

from beethoven.models import Interval


@mark.parametrize(
    "name,alteration",
    [
        ["1", 0],
        ["7", 1],
    ],
)
def test_interval_model(name, alteration):
    assert Interval(name=name, alteration=alteration)
