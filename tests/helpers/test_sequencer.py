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
        (Duration.parse("1"), None, 11, (Duration.parse("10"), None)),
        (
            Duration.parse("1"),
            Duration.parse("1/2"),
            11,
            (Duration.parse("21/2"), None),
        ),
        (Duration.parse("1/5"), None, 21, (Duration.parse("4"), None)),
        (
            Duration.parse("1/3"),
            None,
            8,
            (Duration.parse("7/3"), None),
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
        (Duration.parse("1"), "+...+", 1, (Duration.parse("0"), None)),
        (Duration.parse("1"), "+...+", 2, (Duration.parse("4"), None)),
        (Duration.parse("1"), "+...+", 3, (Duration.parse("5"), None)),
        (Duration.parse("1/5"), "+.+..", 1, (Duration.parse("0"), None)),
        (
            Duration.parse("1/5"),
            "+.+..",
            2,
            (Duration.parse("2/5"), None),
        ),
        (
            Duration.parse("1/5"),
            "+.+..",
            6,
            (Duration.parse("12/5"), None),
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
                (Duration.parse("0"), 0),
                (Duration.parse("1"), 0),
            ]
        ),
        "snare": setup_generator(
            [
                (Duration.parse("2"), 1),
            ]
        ),
        "hh": setup_generator(
            [
                (Duration.parse("0"), 2),
                (Duration.parse("1"), 2),
                (Duration.parse("2"), 2),
                (Duration.parse("3"), 2),
            ]
        ),
        "crash": setup_generator([]),
    }

    assert list(sort_generator_outputs(generators)) == [
        (Duration.parse("0"), 0),
        (Duration.parse("0"), 2),
        (Duration.parse("1"), 0),
        (Duration.parse("1"), 2),
        (Duration.parse("2"), 1),
        (Duration.parse("2"), 2),
        (Duration.parse("3"), 2),
    ]
