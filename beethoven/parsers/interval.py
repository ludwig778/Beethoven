from typing import List

from beethoven.models import Interval
from beethoven.utils.alterations import get_interval_alteration_int_from_str
from beethoven.utils.parser import parse_model_string


def parse(interval_string: str) -> Interval:
    parsed = parse_model_string("interval", interval_string)

    return construct(parsed)


def parse_list(intervals_string: str) -> List[Interval]:
    return [parse(interval_string) for interval_string in intervals_string.split(",")]


def construct(parsed: dict) -> Interval:
    return Interval(
        name=parsed["name"],
        alteration=get_interval_alteration_int_from_str(
            alteration=parsed.get("alteration", ""), interval=parsed["name"]
        ),
        octave=parsed.get("octave"),
    )
