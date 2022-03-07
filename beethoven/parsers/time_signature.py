from beethoven.models import TimeSignature
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> TimeSignature:
    parsed = parse_model_string("time_signature", string)

    return construct(parsed)


def construct(parsed: dict) -> TimeSignature:
    return TimeSignature(
        beats_per_bar=parsed["beats_per_bar"], beat_unit=parsed["beat_unit"]
    )
