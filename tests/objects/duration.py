from fractions import Fraction

from pytest import mark

from beethoven.objects import Duration


@mark.parametrize(
    "string,duration",
    [
        ("4", Duration(Fraction(4))),
        ("4/3", Duration(Fraction(4, 3))),
        ("1/3", Duration(Fraction(1, 3))),
        ("W", Duration(Fraction(4, 1))),
        ("2Q", Duration(Fraction(2, 1))),
        ("1/3W", Duration(Fraction(4, 3))),
        ("1/5Q", Duration(Fraction(1, 5))),
    ],
)
def test_duration_parsing(string, duration):
    assert Duration.parse(string) == duration
