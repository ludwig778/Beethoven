from fractions import Fraction

from beethoven.constants.duration import durations
from beethoven.helpers.parsers import parse_model_string
from beethoven.models import Duration


class DurationController:
    @classmethod
    def parse(cls, string: str) -> Duration:
        parsed = parse_model_string("duration", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Duration:
        value = Fraction(1)
        if base_duration := parsed.get("base_duration"):
            value = durations.get(base_duration)

        if numerator := parsed.get("numerator"):
            value *= numerator

        if denominator := parsed.get("denominator"):
            value /= denominator

        return Duration(value=value)
