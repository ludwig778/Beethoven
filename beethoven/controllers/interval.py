from typing import List

from beethoven.helpers.interval import interval_alteration_to_int
from beethoven.helpers.parsers import parse_model_string
from beethoven.models import Interval


class IntervalController:
    @classmethod
    def parse(cls, interval_string: str) -> Interval:
        parsed = parse_model_string("interval", interval_string)

        return cls.construct(parsed)

    @classmethod
    def parse_list(cls, intervals_string: str) -> List[Interval]:
        return [
            cls.parse(interval_string)
            for interval_string in intervals_string.split(",")
        ]

    @classmethod
    def construct(cls, parsed: dict) -> Interval:
        return Interval(
            name=parsed["name"],
            alteration=interval_alteration_to_int(
                alteration=parsed.get("alteration", ""), interval=parsed.get("name")
            ),
            octave=parsed.get("octave"),
        )
