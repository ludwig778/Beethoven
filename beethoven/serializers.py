from pyparsing import ParseException

from beethoven.parser import patterns
from beethoven.utils.casing import to_pascal_case
from beethoven.utils.parser import parse


def deserialize(obj_name: str, string: str) -> dict:
    pattern = getattr(patterns, obj_name + "_pattern", None)

    if not pattern:
        raise Exception(f"Couldn't find parser for {to_pascal_case(obj_name)}")
    try:
        return parse(pattern, string)
    except ParseException:
        raise Exception(f"Couldn't parse {string=} as {to_pascal_case(obj_name)}")
