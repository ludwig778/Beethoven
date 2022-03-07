from fractions import Fraction

from pytest import mark

from beethoven import parsers
from beethoven.models import Duration


@mark.parametrize(
    "string,expected",
    [
        ["1", Duration(value=1)],
        ["2", Duration(value=2)],
        ["1/2", Duration(value=Fraction(1, 2))],
        ["3/5", Duration(value=Fraction(3, 5))],
        ["W", Duration(value=4)],
        ["H", Duration(value=2)],
        ["Q", Duration(value=1)],
        ["E", Duration(value=Fraction(1, 2))],
        ["S", Duration(value=Fraction(1, 4))],
        ["1/4Q", Duration(value=Fraction(1, 4))],
        ["1/5E", Duration(value=Fraction(1, 10))],
        ["2/3S", Duration(value=Fraction(1, 6))],
    ],
)
def test_duration_parser(string, expected):
    assert parsers.duration.parse(string) == expected
