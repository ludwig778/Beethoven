from typing import List

from beethoven.helpers.note import note_alteration_to_int
from beethoven.helpers.parsers import parse_model_string
from beethoven.models import Note


class NoteController:
    @classmethod
    def parse(cls, note_string: str) -> Note:
        parsed = parse_model_string("note", note_string)

        return cls.construct(parsed)

    @classmethod
    def parse_list(cls, notes_string: str) -> List[Note]:
        return [cls.parse(note_string) for note_string in notes_string.split(",")]

    @classmethod
    def construct(cls, parsed: dict) -> Note:
        return Note(
            name=parsed["name"],
            alteration=note_alteration_to_int(parsed.get("alteration", "")),
            octave=parsed.get("octave"),
        )
