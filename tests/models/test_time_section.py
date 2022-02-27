from fractions import Fraction

from pytest import mark

from beethoven.models import TimeSection


@mark.parametrize(
    "bar,measure,rest",
    [
        [1, 1, Fraction(0)],
        [4, 4, Fraction(1, 5)],
        [1, 1, 0],
    ],
)
def test_time_section_model(bar, measure, rest):
    assert TimeSection(bar=bar, measure=measure, rest=rest)
