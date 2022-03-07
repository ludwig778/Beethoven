from typing import Optional

from beethoven.constants.interval import octave
from beethoven.helpers.degree import get_interval_from_degree
from beethoven.helpers.note import add_interval_to_note
from beethoven.helpers.scale import (
    get_diatonic_scale_chords,
    get_scale_note_from_degree,
)
from beethoven.indexes import chord_index
from beethoven.models import Chord, Scale
from beethoven.parsers.degree import construct as degree_construct
from beethoven.parsers.interval import construct as interval_construct
from beethoven.parsers.interval import parse_list as interval_list_parser
from beethoven.parsers.note import construct as note_construct
from beethoven.utils.parser import parse_model_string


def parse(string: str) -> Chord:
    parsed = parse_model_string("chord", string)

    return construct(parsed)


def parse_with_scale_context(string: str, scale: Scale) -> Chord:
    parsed = parse_model_string("chord", string)

    return construct(parsed, scale=scale)


def construct(parsed: dict, scale: Optional[Scale] = None) -> Chord:
    name = parsed.get("name")
    root = degree = base_degree = None

    if parsed_root := parsed.get("root"):
        root = note_construct(parsed_root)

    elif parsed_degree := parsed.get("degree"):
        if not scale:
            raise Exception("Scale must be set")

        degree = degree_construct(parsed_degree)
        root = get_scale_note_from_degree(scale=scale, degree=degree)

        if not name:
            chords = get_diatonic_scale_chords(scale=scale)
            name = chords[degree.index].name

        if parsed_base_degree := parsed.get("base_degree"):
            base_degree = degree_construct(parsed_base_degree)
            root = add_interval_to_note(root, get_interval_from_degree(base_degree))

    if not root:
        raise Exception(f"Failed to get root note: {parsed=}")

    intervals_string = chord_index.get_intervals(name or "maj")
    intervals = interval_list_parser(intervals_string)

    notes = [add_interval_to_note(root, interval) for interval in intervals]

    if inversion := parsed.get("inversion"):
        notes = notes[inversion:] + [
            add_interval_to_note(note, octave) for note in notes[:inversion]
        ]

    base_note = None
    if base_note_parsed := parsed.get("base_note"):
        base_note = note_construct(base_note_parsed)

        if root.octave and not base_note.octave:
            base_note = note_construct(base_note_parsed)

            if notes[0].octave:
                base_note.octave = notes[0].octave

                if base_note > notes[0]:
                    base_note.octave -= 1

        notes.insert(0, base_note)

    extensions = []
    if extensions_parsed := parsed.get("extensions"):
        extensions = [
            interval_construct(extension_parsed)
            for extension_parsed in extensions_parsed
        ]
        notes += [add_interval_to_note(root, interval) for interval in extensions]

    # Only sort notes when chord root have an octave set
    if extensions and root.octave:
        first_note = notes[0]
        notes = sorted(notes)  # type: ignore
        first_note_index = notes.index(first_note)
        notes = notes[first_note_index:] + notes[:first_note_index]

    return Chord(
        root=root,
        name=name or "maj",
        notes=notes,
        intervals=intervals,
        inversion=inversion,
        extensions=extensions,
        base_note=base_note,
        degree=degree,
        base_degree=base_degree,
    )
