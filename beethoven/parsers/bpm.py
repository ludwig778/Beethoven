from beethoven.models import Bpm
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> Bpm:
    parsed = parse_model_string("bpm", string)

    return construct(parsed)


def construct(parsed: dict) -> Bpm:
    return Bpm(value=parsed["value"])
