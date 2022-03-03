from beethoven.models import Degree
from beethoven.utils.alterations import get_degree_alteration_int_from_str
from beethoven.utils.parser import parse_model_string


class DegreeController:
    @classmethod
    def parse(cls, string: str) -> Degree:
        parsed = parse_model_string("degree", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Degree:
        return Degree(
            name=parsed["name"],
            alteration=get_degree_alteration_int_from_str(parsed.get("alteration", "")),
        )
