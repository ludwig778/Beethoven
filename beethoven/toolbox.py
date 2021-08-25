from dataclasses import replace
from fractions import Fraction
from itertools import product
from typing import Generator, List, Tuple, Union

from beethoven import factories
from beethoven.mappings import note_mapping
from beethoven.objects import (Bpm, Chord, Duration, Interval, Note, Scale,
                               TimeSection, TimeSignature)
from beethoven.serializers import deserialize
from beethoven.utils.duration import NoLimit


def get_parser(obj_name):
    def parser(string, **kwargs):
        parsed = deserialize(obj_name, string)
        obj = getattr(factories, "build_" + obj_name)(parsed, **kwargs)

        return obj
    return parser


def get_list_parser(obj_name):
    def list_parser(string):
        parse_func = get_parser(obj_name)
        return [
            parse_func(sub_string)
            for sub_string in string.split(",")
        ]
    return list_parser


def get_chords_from_scale(self, degrees: List[int] = None) -> List[Chord]:
    return factories.get_chords_from_scale(self, degrees=degrees)


def add_interval_to_note(note: Note, interval: Interval) -> Note:
    return factories.add_interval_to_note(note, interval)


def substract_interval_to_note(note: Note, interval: Interval) -> Note:
    return factories.add_interval_to_note(note, interval, reverse=True)


def get_notes_intervals(note1: Note, note2: Note) -> Interval:
    return factories.get_notes_interval(note1, note2)


def multiply_duration(duration: Duration, multiplier: int) -> Duration:
    return replace(duration, value=duration.value * multiplier)


def get_base_time(bpm: Bpm) -> Fraction:
    return Fraction(60, bpm.value)


def get_timespan(duration: Duration, bpm: Bpm) -> Fraction:
    return duration.value * bpm.base_time


def time_signature_as_duration(time_signature: TimeSignature) -> Duration:
    reduction = Fraction(time_signature.beat_unit, 4)

    return Duration(Fraction(time_signature.beats_per_bar, reduction))


def get_note_index(note: Note) -> int:
    return (
        note_mapping.get_semitones(note.name)
        + note.alteration
        + (note.octave or 0) * 12
    )


def get_time_section(time_signature: TimeSignature, timeline: Fraction) -> TimeSection:
    reduction = Fraction(time_signature.beat_unit, 4)

    bar, raw_measure = divmod(timeline, time_signature.as_duration.value)
    measure, fraction = divmod(raw_measure * reduction, 1)

    return TimeSection(
        bar=bar + 1,
        measure=measure + 1,
        fraction=fraction
    )


def time_section_generator(
    time_signature: TimeSignature,
    duration: Duration,
    limit: Union[Duration, NoLimit, None] = None
) -> Generator[Tuple[TimeSection, Duration], None, None]:

    time_signature_duration = time_signature.as_duration

    if limit is NoLimit:
        limit = None
    elif not limit:
        limit = time_signature_duration

    timeline = Fraction(0)
    while 1:
        next_timeline = timeline + duration.value

        if limit and next_timeline >= limit.value:
            duration = Duration(limit.value - timeline)

            yield get_time_section(time_signature, timeline), duration
            break

        yield get_time_section(time_signature, timeline), duration

        timeline = next_timeline


def time_section_to_duration(time_section: TimeSection, time_signature: TimeSignature) -> Duration:
    total = Fraction()
    reduction = Fraction(time_signature.beat_unit, 4)
    time_signature_duration = time_signature.as_duration

    if time_section.bar > 1:
        total += time_signature_duration.value * (time_section.bar - 1)

    if time_section.measure > 1:
        total += (time_section.measure - 1) / reduction

    if time_section.fraction:
        total += time_section.fraction

    return Duration(total)


def get_scale_notes_within_range(low_range: Note, high_range: Note, scale: Scale) -> List[Note]:
    notes_by_index = {}

    for octave, note in product(
        range(low_range.octave - 1, high_range.octave + 1),
        scale.notes
    ):
        note = replace(note, octave=octave)
        notes_by_index[note.index] = note

    low_range_index = low_range.index
    high_range_index = high_range.index

    notes = [
        note
        for index, note in sorted(notes_by_index.items(), key=lambda x: x[0])
        if low_range_index <= index <= high_range_index
    ]

    return notes
