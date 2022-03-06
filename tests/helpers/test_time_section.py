from fractions import Fraction

from pytest import mark

from beethoven.constants.duration import (
    eighth_value,
    half_value,
    quarter_value,
    sixteenth_value,
    whole_value,
)
from beethoven.helpers.time_section import time_section_generator
from beethoven.models import Duration, TimeSection, TimeSignature


def test_time_section_helper_time_section_generator_first_values():
    generator = time_section_generator(
        TimeSignature(beats_per_bar=4, beat_unit=4), Duration(value=whole_value)
    )

    assert next(generator) == (TimeSection(bar=1, measure=1, rest=0), Duration(value=0))


@mark.parametrize(
    "time_signature,step,count,expected",
    [
        # Check constants duration values
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=2, measure=1, rest=0), Duration(value=4)),
        ],
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=half_value),
            1,
            (TimeSection(bar=1, measure=3, rest=0), Duration(value=2)),
        ],
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=quarter_value),
            1,
            (TimeSection(bar=1, measure=2, rest=0), Duration(value=1)),
        ],
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=eighth_value),
            1,
            (
                TimeSection(bar=1, measure=1, rest=Fraction(1, 2)),
                Duration(value=Fraction(1, 2)),
            ),
        ],
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=sixteenth_value),
            1,
            (
                TimeSection(bar=1, measure=1, rest=Fraction(1, 4)),
                Duration(value=Fraction(1, 4)),
            ),
        ],
        # Time Signature Check
        [
            TimeSignature(beats_per_bar=2, beat_unit=2),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=2, measure=1, rest=0), Duration(value=4)),
        ],
        [
            TimeSignature(beats_per_bar=8, beat_unit=8),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=2, measure=1, rest=0), Duration(value=4)),
        ],
        [
            TimeSignature(beats_per_bar=16, beat_unit=16),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=2, measure=1, rest=0), Duration(value=4)),
        ],
        # Check Duration divided values
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=quarter_value * Fraction(2, 5)),
            2,
            (
                TimeSection(bar=1, measure=1, rest=Fraction(4, 5)),
                Duration(value=Fraction(4, 5)),
            ),
        ],
        [
            TimeSignature(beats_per_bar=4, beat_unit=4),
            Duration(value=quarter_value * Fraction(3, 5)),
            3,
            (
                TimeSection(bar=1, measure=2, rest=Fraction(4, 5)),
                Duration(value=Fraction(9, 5)),
            ),
        ],
        # Check duration overlaps
        [
            TimeSignature(beats_per_bar=5, beat_unit=4),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=1, measure=5, rest=0), Duration(value=4)),
        ],
        [
            TimeSignature(beats_per_bar=3, beat_unit=4),
            Duration(value=whole_value),
            1,
            (TimeSection(bar=2, measure=2, rest=0), Duration(value=4)),
        ],
    ],
)
def test_time_section_helper_time_section_generator(
    time_signature, step, count, expected
):
    generator = time_section_generator(time_signature, step)

    for _ in range(count + 1):
        time_section = next(generator)

    assert time_section == expected
