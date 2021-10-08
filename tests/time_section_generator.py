from fractions import Fraction

from pytest import mark

from beethoven.objects import Duration, TimeSection, TimeSignature
from beethoven.utils.duration import DurationLimit


@mark.parametrize(
    "time_signature,duration,first,last,length",
    [
        # Basic tests
        (
            "4/4",
            "W",
            (TimeSection(1, 1), Duration(4)),
            (TimeSection(1, 1), Duration(4)),
            1,
        ),
        (
            "4/4",
            "H",
            (TimeSection(1, 1), Duration(2)),
            (TimeSection(1, 3), Duration(2)),
            2,
        ),
        (
            "4/4",
            "Q",
            (TimeSection(1, 1), Duration(1)),
            (TimeSection(1, 4), Duration(1)),
            4,
        ),
        (
            "4/4",
            "E",
            (TimeSection(1, 1), Duration(Fraction(1, 2))),
            (TimeSection(1, 4, Fraction(1, 2)), Duration(Fraction(1, 2))),
            8,
        ),
        (
            "16/16",
            "S",
            (TimeSection(1, 1), Duration(Fraction(1, 4))),
            (TimeSection(1, 16), Duration(Fraction(1, 4))),
            16,
        ),
        # Tests with more complex time signatures
        (
            "3/4",
            "Q",
            (TimeSection(1, 1), Duration(1)),
            (TimeSection(1, 3), Duration(1)),
            3,
        ),
        (
            "3/2",
            "Q",
            (TimeSection(1, 1), Duration(1)),
            (TimeSection(1, 3, Fraction(1, 2)), Duration(1)),
            6,
        ),
        (
            "11/16",
            "S",
            (TimeSection(1, 1), Duration(Fraction(1, 4))),
            (TimeSection(1, 11), Duration(Fraction(1, 4))),
            11,
        ),
        # Tests with tuplets
        (
            "4/4",
            "1/3Q",
            (TimeSection(1, 1), Duration(Fraction(1, 3))),
            (TimeSection(1, 4, Fraction(2, 3)), Duration(Fraction(1, 3))),
            12,
        ),
        (
            "4/4",
            "1/5H",
            (TimeSection(1, 1), Duration(Fraction(2, 5))),
            (TimeSection(1, 4, Fraction(3, 5)), Duration(Fraction(2, 5))),
            10,
        ),
    ],
)
def test_time_section_generator(time_signature, duration, first, last, length):
    time_signature = TimeSignature.parse(time_signature)
    duration = Duration.parse(duration)

    generator = time_signature.time_section_generator(duration)
    time_sections = list(generator)

    assert time_sections[0] == first
    assert time_sections[-1] == last

    assert len(time_sections) == length


def test_time_section_generator_with_limit():
    time_signature = TimeSignature.parse("4/4")
    generator = time_signature.time_section_generator(
        Duration.parse("1Q"), limit=Duration.parse("3W")
    )
    time_sections = list(generator)

    assert time_sections[0] == (TimeSection(1, 1), Duration(1))
    assert time_sections[-1] == (TimeSection(3, 4), Duration(1))

    assert len(time_sections) == 12


def test_time_section_generator_with_offset():
    time_signature = TimeSignature.parse("4/4")
    generator = time_signature.time_section_generator(
        Duration.parse("Q"),
        limit=Duration.parse("3W"),
        offset=Duration.parse("W")
    )
    time_sections = list(generator)

    assert time_sections[0] == (TimeSection(2, 1), Duration(1))
    assert time_sections[-1] == (TimeSection(3, 4), Duration(1))

    assert len(time_sections) == 8


def test_time_section_generator_with_offset_over_limit():
    time_signature = TimeSignature.parse("4/4")
    generator = time_signature.time_section_generator(
        Duration.parse("Q"),
        limit=Duration.parse("3W"),
        offset=Duration.parse("4W")
    )
    time_sections = list(generator)

    assert time_sections == []


def test_time_section_generator_with_big_limit():
    time_signature = TimeSignature.parse("4/4")
    generator = time_signature.time_section_generator(
        Duration.parse("1Q"), limit=DurationLimit.NoLimit
    )
    time_sections = [next(generator) for _ in range(4000)]

    assert time_sections[0] == (TimeSection(1, 1), Duration(1))
    assert time_sections[-1] == (TimeSection(1000, 4), Duration(1))

    assert len(time_sections) == 4000


@mark.parametrize(
    "time_signature,time_section,duration",
    [
        ("2/2", TimeSection(1, 1), "0"),
        ("4/4", TimeSection(1, 1), "0"),
        ("8/8", TimeSection(1, 1), "0"),
        ("16/16", TimeSection(1, 1), "0"),
        ("4/4", TimeSection(1, 2), "Q"),
        ("4/4", TimeSection(1, 3), "H"),
        ("4/4", TimeSection(2, 1), "W"),
        ("4/4", TimeSection(2, 1), "4"),
        ("3/4", TimeSection(2, 1), "3"),
        ("3/4", TimeSection(1, 2), "Q"),
        ("5/8", TimeSection(1, 3), "Q"),
        ("3/4", TimeSection(1, 3), "H"),
        ("5/8", TimeSection(1, 5), "H"),
        ("15/16", TimeSection(2, 1), "15/4"),
        ("4/4", TimeSection(1, 1, Fraction(1, 2)), "E"),
        ("4/4", TimeSection(1, 2, Fraction(1, 4)), "5S"),
    ],
)
def test_time_section_to_duration(time_signature, time_section, duration):
    time_signature = TimeSignature.parse(time_signature)
    duration = Duration.parse(duration)

    assert time_section.as_duration(time_signature) == duration
