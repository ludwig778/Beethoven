from typing import Callable, List

from pyparsing import ParseException

from beethoven.objects import Chord, Degree, Interval, Note
from beethoven.parser import patterns
from beethoven.toolbox import (get_alteration_from_int,
                               get_interval_alteration_from_int)
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


def serialize_note(note: Note) -> str:
    return (
        note.name +
        get_alteration_from_int(note.alteration) +
        str(note.octave or "")
    )


def serialize_interval(interval: Interval) -> str:
    return (
        interval.name +
        get_interval_alteration_from_int(interval.name, interval.alteration)
    )


def serialize_degree(degree: Degree) -> str:
    return (
        get_alteration_from_int(degree.alteration) +
        degree.name
    )


def serialize_chord(chord: Chord) -> str:
    string = ""

    if chord.degree:
        string += serialize_degree(chord.degree)
    else:
        string += serialize_note(chord.root)

    string += "_" + chord.name

    if chord.inversion:
        string += f":i={chord.inversion}"

    if chord.base_note:
        string += f":b={serialize_note(chord.base_note)}"

    if chord.base_degree:
        string += f":s={serialize_degree(chord.base_degree)}"

    if chord.extensions:
        str_extensions = ",".join([
            serialize_interval(extension)
            for extension in chord.extensions
        ])
        string += f":e={str_extensions}"

    return string


def serialize_list(serializer: Callable, objs: List) -> str:
    return ",".join([
        serializer(obj)
        for obj in objs
    ])
