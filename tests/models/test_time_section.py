from fractions import Fraction

from pytest import mark

from beethoven.models import TimeSection


@mark.parametrize(
    "bar,measure,fraction",
    [
        [1, 1, Fraction(0)],
        [4, 4, Fraction(1, 5)],
    ],
)
def test_time_section_model(bar, measure, fraction):
    assert TimeSection(bar=bar, measure=measure, fraction=fraction)
