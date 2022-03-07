from beethoven.helpers.note import add_interval_to_note
from beethoven.indexes import scale_index
from beethoven.models import Scale
from beethoven.parsers.interval import parse_list as interval_list_parser
from beethoven.parsers.note import construct as note_construct
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> Scale:
    parsed = parse_model_string("scale", string)

    return construct(parsed)


def construct(parsed: dict) -> Scale:
    tonic = note_construct(parsed["tonic"])

    intervals_string = scale_index.get_intervals(parsed["name"])
    intervals = interval_list_parser(intervals_string)

    notes = [add_interval_to_note(tonic, interval) for interval in intervals]

    return Scale(tonic=tonic, name=parsed["name"], notes=notes, intervals=intervals)
