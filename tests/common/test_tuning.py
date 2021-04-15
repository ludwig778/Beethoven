from pytest import mark

from beethoven.common.tuning import Tuning
from beethoven.theory.note import Note


@mark.parametrize("tuning_args,expected_repr", [
    ((Note("A"),),                 "<Tuning 1 strings>"),
    (Note.to_list("A,B,C"),       "<Tuning 3 strings>"),
    (Note.to_list("E,A,D,G,B,E"), "<Tuning 6 strings>"),
])
def test_tuning_instanciation(tuning_args, expected_repr):
    tuning = Tuning(*tuning_args)

    assert repr(tuning) == expected_repr
