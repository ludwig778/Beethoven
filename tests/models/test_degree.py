from pytest import mark, raises

from beethoven.models import Degree


@mark.parametrize(
    "name,alteration",
    [
        ["i", 0],
        ["vii", 1],
    ],
)
def test_degree_model(name, alteration):
    assert Degree(name=name, alteration=alteration)


def test_degree_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: VIII"):
        Degree(name="VIII")


@mark.parametrize("alteration", [-4, 4])
def test_degree_model_raise_invalid_alteration(alteration):
    with raises(
        ValueError, match=f"Invalid alteration: {alteration}, must be between -3 and 3"
    ):
        Degree(name="i", alteration=alteration)
