from pytest import mark

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
