from typing import Union

from pyparsing import ParseException

from beethoven.controllers.degree import parse as degree_parse
from beethoven.controllers.note import parse as note_parse
from beethoven.models import Degree, Note


def parse_root_note_or_degree(string: str) -> Union[Note, Degree]:
    try:
        return note_parse(string)
    except ParseException:
        pass

    try:
        return degree_parse(string)
    except ParseException:
        pass

    raise Exception('Couldn\'t parse note or degree from: "{string}"')
