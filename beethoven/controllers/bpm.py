from beethoven.helpers.parsers import parse_model_string
from beethoven.models import Bpm


class BpmController:
    @classmethod
    def parse(cls, string: str) -> Bpm:
        parsed = parse_model_string("bpm", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Bpm:
        return Bpm(value=parsed["value"])
