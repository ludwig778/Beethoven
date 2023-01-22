from fractions import Fraction

from pytest import mark, raises

from beethoven.constants.duration import (
    eighth_value,
    half_value,
    quarter_value,
    sixteenth_value,
    whole_value,
)
from beethoven.models import Duration, TimeSection, TimeSignature


@mark.parametrize(
    "string,expected_obj",
    [
        ["4/4", TimeSignature(beats_per_bar=4, beat_unit=4)],
        ["3/2", TimeSignature(beats_per_bar=3, beat_unit=2)],
        ["7/8", TimeSignature(beats_per_bar=7, beat_unit=8)],
        ["5/16", TimeSignature(beats_per_bar=5, beat_unit=16)],
    ],
)
def test_time_signature_parsing(string, expected_obj):
    assert TimeSignature.parse(string) == expected_obj


@mark.parametrize("beat_unit", [0, 64])
def test_time_signature_model_raise_out_of_bound_beat_unit(beat_unit):
    with raises(
        ValueError, match=f"Invalid beat_unit: {beat_unit}, must be in range 1-32"
    ):
        TimeSignature(beats_per_bar=4, beat_unit=beat_unit)


@mark.parametrize("beat_unit", [3, 7])
def test_time_signature_model_raise_invalid_beat_unit(beat_unit):
    with raises(
        ValueError, match=f"Invalid beat_unit: {beat_unit}, must be a multiple of 2"
    ):
        TimeSignature(beats_per_bar=4, beat_unit=beat_unit)


def test_time_section_helper_time_section_generator_first_values():
    generator = TimeSignature(beats_per_bar=4, beat_unit=4).generate_time_sections(
        Duration(value=whole_value)
    )

    assert next(generator) == (TimeSection(bar=1, measure=1, rest=0), Duration(value=0))


@mark.parametrize(
    "time_signature,step,count,expected_time_section",
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
    time_signature, step, count, expected_time_section
):
    generator = time_signature.generate_time_sections(step)

    for _ in range(count + 1):
        time_section = next(generator)

    assert time_section == expected_time_section
