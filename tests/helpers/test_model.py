from pytest import mark

from beethoven.helpers.model import update_model
from beethoven.models import Degree, Interval, Note


@mark.parametrize(
    "origin,update_kwargs,expected",
    [
        [Note(name="C"), {"octave": 2}, Note(name="C", octave=2)],
        [Degree(name="II"), {"alteration": 1}, Degree(name="II", alteration=1)],
        [Interval(name="2", alteration=-1), {"alteration": 0}, Interval(name="2")],
    ],
)
def test_model_helper_update_model(origin, update_kwargs, expected):
    assert update_model(origin, **update_kwargs) == expected
