from typing import List

from beethoven.controllers.interval import parse as interval_parse
from beethoven.helpers.note import add_interval_to_note
from beethoven.models import Note
from beethoven.parsers.parser import parse_model_string
from beethoven.utils.note import note_alteration_to_int


def parse(note_string: str) -> Note:
    parsed = parse_model_string("note", note_string)

    return construct(parsed)


def parse_list(notes_string: str) -> List[Note]:
    return [parse(note_string) for note_string in notes_string.split(",")]


def construct(parsed: dict) -> Note:
    return Note(
        name=parsed["name"],
        alteration=note_alteration_to_int(parsed.get("alteration", "")),
        octave=parsed.get("octave"),
    )


def from_midi_index(index: int) -> Note:
    octave, rest_index = divmod(index, 12)

    note = parse("C" + str(octave))

    intervals = {
        0: "1",
        2: "2",
        4: "3",
        5: "4",
        7: "5",
        9: "6",
        11: "7",
    }

    for semitones, interval_name in intervals.items():
        if semitones >= rest_index:
            interval = interval_parse(interval_name)
            interval.alteration = rest_index - semitones

            break

    note = add_interval_to_note(note, interval)

    return note
