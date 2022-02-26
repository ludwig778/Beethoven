from fractions import Fraction

from pytest import mark

from beethoven.models import Duration


@mark.parametrize("value", [Fraction(1, 3), Fraction(2, 5)])
def test_duration_model(value):
    assert Duration(value=value)
