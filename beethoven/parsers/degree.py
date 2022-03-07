from beethoven.models import Degree
from beethoven.utils.alterations import get_degree_alteration_int_from_str
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> Degree:
    parsed = parse_model_string("degree", string)

    return construct(parsed)


def construct(parsed: dict) -> Degree:
    return Degree(
        name=parsed["name"],
        alteration=get_degree_alteration_int_from_str(parsed.get("alteration", "")),
    )
