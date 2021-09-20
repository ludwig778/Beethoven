from pyparsing import ParseException

from beethoven.exceptions import CouldNotParse, ParserNotFound
from beethoven.parser import patterns
from beethoven.utils.parser import parse


def deserialize(obj_name: str, string: str) -> dict:
    pattern = getattr(patterns, obj_name + "_pattern", None)

    if not pattern:
        raise ParserNotFound(obj_name)
    try:
        return parse(pattern, string)
    except ParseException:
        raise CouldNotParse(string, obj_name)
