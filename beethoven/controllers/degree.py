from typing import List

from beethoven.models import Degree
from beethoven.parsers.parser import parse_model_string
from beethoven.utils.alterations import get_degree_alteration_int_from_str


def parse(string: str) -> Degree:
    parsed = parse_model_string("degree", string)

    return construct(parsed)


def parse_list(degrees_string: str) -> List[Degree]:
    return [parse(degree_string) for degree_string in degrees_string.split(",")]


def construct(parsed: dict) -> Degree:
    return Degree(
        name=parsed["name"],
        alteration=get_degree_alteration_int_from_str(parsed.get("alteration", "")),
    )
