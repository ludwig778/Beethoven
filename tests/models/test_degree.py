from pytest import mark, raises

from beethoven.models import Degree


@mark.parametrize(
    "string,expected_obj",
    [
        ["i", Degree(name="i")],
        ["v", Degree(name="v")],
        ["vii", Degree(name="vii")],
        ["#i", Degree(name="i", alteration=1)],
        ["biii", Degree(name="iii", alteration=-1)],
        ["###iii", Degree(name="iii", alteration=3)],
        ["bbbiii", Degree(name="iii", alteration=-3)],
    ],
)
def test_degree_parsing(string, expected_obj):
    assert Degree.parse(string) == expected_obj


def test_degree_model_raise_invalid_name():
    with raises(ValueError, match="Invalid name: VIII"):
        Degree(name="VIII")


@mark.parametrize("alteration", [-4, 4])
def test_degree_model_raise_invalid_alteration(alteration):
    with raises(ValueError, match=f"Invalid alteration: {alteration}, must be between -3 and 3"):
        Degree(name="i", alteration=alteration)


@mark.parametrize(
    "name,index",
    [
        ["i", 0],
        ["vii", 6],
    ],
)
def test_degree_model_index_property(name, index):
    assert Degree(name=name).index == index
