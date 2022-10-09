from pytest import mark

from beethoven import controllers
from beethoven.models import Degree


@mark.parametrize(
    "string,expected",
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
def test_degree_parser(string, expected):
    assert controllers.degree.parse(string) == expected
