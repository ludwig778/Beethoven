from pytest import mark

from beethoven.objects import Degree


@mark.parametrize(
    "string,degree",
    [
        ("I", Degree(name="I", alteration=0)),
        ("bii", Degree(name="ii", alteration=-1)),
        ("III", Degree(name="III", alteration=0)),
        ("#v", Degree(name="v", alteration=1)),
    ],
)
def test_degree_parsing(string, degree):
    assert Degree.parse(string) == degree
