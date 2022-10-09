from fractions import Fraction

from pytest import mark

from beethoven.helpers.sequencer import (
    note_repeater,
    note_sequencer,
    sort_generator_outputs,
)
from beethoven.models import Duration


@mark.parametrize(
    "cycle,offset,cycles,expected",
    [
        (Duration(value=1), None, 11, (Duration(value=10), None)),
        (
            Duration(value=1),
            Duration(value=Fraction(1, 2)),
            11,
            (Duration(value=Fraction(21, 2)), None),
        ),
        (Duration(value=Fraction(1, 5)), None, 21, (Duration(value=4), None)),
        (
            Duration(value=Fraction(1, 3)),
            None,
            8,
            (Duration(value=Fraction(7, 3)), None),
        ),
    ],
)
def test_note_repeater(cycle, offset, cycles, expected):
    generator = note_repeater(cycle, [None], offset=offset)

    for _ in range(cycles):
        note_data = next(generator)

    assert note_data == expected


@mark.parametrize(
    "step,round_robin,cycles,expected",
    [
        (Duration(value=1), "+...+", 1, (Duration(value=0), None)),
        (Duration(value=1), "+...+", 2, (Duration(value=4), None)),
        (Duration(value=1), "+...+", 3, (Duration(value=5), None)),
        (Duration(value=Fraction(1, 5)), "+.+..", 1, (Duration(value=0), None)),
        (
            Duration(value=Fraction(1, 5)),
            "+.+..",
            2,
            (Duration(value=Fraction(2, 5)), None),
        ),
        (
            Duration(value=Fraction(1, 5)),
            "+.+..",
            6,
            (Duration(value=Fraction(12, 5)), None),
        ),
    ],
)
def test_note_sequencer(step, round_robin, cycles, expected):
    generator = note_sequencer(step, [None], round_robin)

    for _ in range(cycles):
        note_data = next(generator)

    assert note_data == expected


def test_sequencer_helper_sort_generator_outputs():
    def setup_generator(outputs):
        for output in outputs:
            yield output

    generators = {
        "kick": setup_generator(
            [
                (Duration(value=0), 0),
                (Duration(value=1), 0),
            ]
        ),
        "snare": setup_generator(
            [
                (Duration(value=2), 1),
            ]
        ),
        "hh": setup_generator(
            [
                (Duration(value=0), 2),
                (Duration(value=1), 2),
                (Duration(value=2), 2),
                (Duration(value=3), 2),
            ]
        ),
        "crash": setup_generator([]),
    }

    assert list(sort_generator_outputs(generators)) == [
        (Duration(value=0), 0),
        (Duration(value=0), 2),
        (Duration(value=1), 0),
        (Duration(value=1), 2),
        (Duration(value=2), 1),
        (Duration(value=2), 2),
        (Duration(value=3), 2),
    ]
