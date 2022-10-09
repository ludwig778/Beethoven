from beethoven.controllers.interval import parse_list as interval_list_parser
from beethoven.controllers.note import construct as note_construct
from beethoven.helpers.note import add_interval_to_note
from beethoven.indexes import scale_index
from beethoven.models import Scale
from beethoven.parsers.parser import parse_model_string


def parse(string: str) -> Scale:
    parsed = parse_model_string("scale", string)

    return construct(parsed)


def construct(parsed: dict) -> Scale:
    tonic = note_construct(parsed["tonic"])

    name = parsed["name"].replace("_", " ")

    intervals_string = scale_index.get_intervals(name)
    intervals = interval_list_parser(intervals_string)

    notes = [add_interval_to_note(tonic, interval) for interval in intervals]

    return Scale(tonic=tonic, name=name, notes=notes, intervals=intervals)
