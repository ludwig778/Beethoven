from typing import Union

from pyparsing import ParseException

from beethoven.models import Degree, Note


def parse_root_note_or_degree(string: str) -> Union[Note, Degree]:
    try:
        return Note.parse(string)
    except ParseException:
        pass

    try:
        return Degree.parse(string)
    except ParseException:
        pass

    raise Exception('Couldn\'t parse note or degree from: "{string}"')
