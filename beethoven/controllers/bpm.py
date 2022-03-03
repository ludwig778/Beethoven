from beethoven.models import Bpm
from beethoven.utils.parser import parse_model_string


class BpmController:
    @classmethod
    def parse(cls, string: str) -> Bpm:
        parsed = parse_model_string("bpm", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Bpm:
        return Bpm(value=parsed["value"])
