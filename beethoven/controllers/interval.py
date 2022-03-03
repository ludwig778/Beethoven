from typing import List

from beethoven.models import Interval
from beethoven.utils.alterations import get_interval_alteration_int_from_str
from beethoven.utils.parser import parse_model_string


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
            alteration=get_interval_alteration_int_from_str(
                alteration=parsed.get("alteration", ""), interval=parsed["name"]
            ),
            octave=parsed.get("octave"),
        )
