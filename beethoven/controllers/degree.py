from beethoven.helpers.degree import degree_alteration_to_int
from beethoven.helpers.parsers import parse_model_string
from beethoven.models import Degree


class DegreeController:
    @classmethod
    def parse(cls, string: str) -> Degree:
        parsed = parse_model_string("degree", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Degree:
        return Degree(
            name=parsed["name"],
            alteration=degree_alteration_to_int(parsed.get("alteration", "")),
        )
