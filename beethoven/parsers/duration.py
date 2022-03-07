from fractions import Fraction

from beethoven.constants.duration import durations
from beethoven.models import Duration
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> Duration:
    parsed = parse_model_string("duration", string)

    return construct(parsed)


def construct(parsed: dict) -> Duration:
    value = Fraction(1)
    if base_duration := parsed.get("base_duration"):
        value = durations[base_duration]

    if numerator := parsed.get("numerator"):
        value *= numerator

    if denominator := parsed.get("denominator"):
        value /= denominator

    return Duration(value=value)
