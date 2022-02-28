from beethoven.controllers.interval import IntervalController
from beethoven.controllers.note import NoteController
from beethoven.helpers.note import add_interval_to_note
from beethoven.helpers.parsers import parse_model_string
from beethoven.indexes import chord_index
from beethoven.models import Chord, interval


class ChordController:
    @classmethod
    def parse(cls, string: str) -> Chord:
        parsed = parse_model_string("chord", string)

        return cls.construct(parsed)

    @classmethod
    def construct(cls, parsed: dict) -> Chord:
        root = NoteController.construct(parsed["root"])

        intervals_string = chord_index.get_intervals(parsed["name"])
        intervals = IntervalController.parse_list(intervals_string)

        notes = [add_interval_to_note(root, interval) for interval in intervals]

        return Chord(root=root, name=parsed["name"], notes=notes, intervals=intervals)
