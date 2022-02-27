from pytest import mark, raises

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


def test_interval_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: 0"):
        Interval(name="0")


@mark.parametrize("alteration", [-4, 4])
def test_interval_model_raise_invalid_alteration(alteration):
    with raises(
        ValueError, match=f"Invalid alteration: {alteration}, must be between -3 and 3"
    ):
        Interval(name="1", alteration=alteration)
