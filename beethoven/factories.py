from dataclasses import replace
from fractions import Fraction
from typing import List, Optional, Tuple

from beethoven.mappings import (chord_mapping, degree_mapping,
                                interval_mapping, note_mapping, scale_mapping)
from beethoven.objects import (Bpm, Chord, Degree, Duration, Grid, GridPart,
                               Interval, Note, Scale, TimeSignature)
from beethoven.serializers import (deserialize, serialize_interval,
                                   serialize_list, serialize_note)
from beethoven.utils.alterations import (get_alteration_as_int,
                                         get_interval_alteration_as_int)
from beethoven.utils.validation import check_if_diatonic

default_durations = {
    "W": Duration(Fraction(4, 1)),
    "H": Duration(Fraction(2, 1)),
    "Q": Duration(Fraction(1, 1)),
    "E": Duration(Fraction(1, 2)),
    "S": Duration(Fraction(1, 4))
}


def build_bpm(parsed: dict) -> Bpm:
    value = parsed.get("value")

    if not value:
        raise Exception("Bpm value can't be equal to 0")

    return Bpm(value=value)


def build_degree(parsed: dict) -> Degree:
    name = parsed.get("name")

    if name is None:
        raise Exception("Name must be set")

    alteration = 0
    if raw_alteration := parsed.get("alteration"):
        alteration = get_alteration_as_int(raw_alteration)

    return Degree(
        name=name,
        alteration=alteration
    )


def build_duration(parsed: dict) -> Duration:
    numerator = parsed.get("numerator", 1)
    denominator = parsed.get("denominator")

    if denominator == 0:
        raise Exception("Duration denominator can't be equal to 0")

    value = Fraction(
        numerator=numerator,
        denominator=denominator
    )

    if base_duration := parsed.get("base_duration"):
        if duration := default_durations.get(base_duration):
            value *= duration.value
        else:
            raise Exception(f"Duration base_duration {base_duration} couldn't be found")

    return Duration(value=value)


def build_time_signature(parsed: dict) -> TimeSignature:
    beats_per_bar = parsed.get("beats_per_bar", 4)
    beat_unit = parsed.get("beat_unit", 4)

    if beat_unit not in (1, 2, 4, 8, 16, 32):
        raise Exception("TimeSignature beat unit value {beat_unit} is invalid")
    elif beats_per_bar == 0:
        raise Exception("TimeSignature beat per bar value {beats_per_bar} can't be equal to 0")

    return TimeSignature(
        beats_per_bar=beats_per_bar,
        beat_unit=beat_unit
    )


def get_notes_interval(note1: Note, note2: Note) -> Interval:
    index_1 = note_mapping.get_index(note1.name)
    index_2 = note_mapping.get_index(note2.name)
    index_diff = index_2 - index_1

    semitones_1 = note_mapping.get_semitones(note1.name)
    semitones_2 = note_mapping.get_semitones(note2.name)

    octave_diff = 0
    if note1.octave and note2.octave:
        semitones_1 += note1.octave * 12
        semitones_2 += note2.octave * 12

        semitones_diff = semitones_2 - semitones_1

        octave_diff = note2.octave - note1.octave

        index_diff += (octave_diff * 7)
    else:
        semitones_diff = (semitones_2 - semitones_1) % 12
        index_diff %= 7

    name = interval_mapping.get_name_from_index(index_diff)
    semitones = interval_mapping.get_semitones(name)
    alteration = semitones_diff - semitones - note1.alteration + note2.alteration

    return Interval(
        name=name,
        alteration=alteration
    )


def build_interval(parsed: dict) -> Interval:
    name = parsed.get("name")
    if not name:
        raise Exception("LMAO")

    alteration = 0
    if raw_alteration := parsed.get("alteration"):
        alteration = get_interval_alteration_as_int(name, raw_alteration)

    return Interval(
        name=name,
        alteration=alteration
    )


def add_interval_to_note(note: Note, interval: Interval, reverse: bool = False) -> Note:
    degree_diff = int(interval.name) - 1
    interval_st = interval_mapping.get_semitones(interval.name) + interval.alteration

    if reverse:
        degree_diff *= - 1
        interval_st *= - 1

    index_base_note = note_mapping.get_index(note.name)
    octave_diff, target_degree = divmod(degree_diff + index_base_note, 7)

    # get the target note name, and get semitones of base and target note
    base_st = note_mapping.get_semitones(note.name)
    dest_note = note_mapping.get_name_from_index(target_degree % 7)
    dest_st = note_mapping.get_semitones(dest_note)

    alteration = base_st + interval_st + note.alteration - dest_st - (12 * octave_diff)

    octave = None
    if note.octave is not None:
        octave = note.octave + octave_diff

    return Note(
        name=dest_note,
        alteration=alteration,
        octave=octave
    )


def build_note(parsed: dict) -> Note:
    name = parsed.get("name")

    if not name:
        raise Exception("LMAO")

    alteration = get_alteration_as_int(parsed.get("alteration"))

    if octave := parsed.get("octave"):
        octave = int(octave)

    return Note(
        name=name,
        alteration=alteration,
        octave=octave
    )


def build_scale(parsed: dict) -> Scale:
    raw_tonic = parsed.get("tonic")
    assert raw_tonic, "LMAO"
    #    raise Exception("LMAOOOO")

    tonic = build_note(raw_tonic)

    if name := parsed.get("name"):
        name = name.replace("_", " ").strip()
    else:
        name = "ionian"

    if raw_intervals := scale_mapping.get_intervals(name):
        intervals = [
            build_interval(deserialize("interval", interval))
            for interval in raw_intervals.split(",")
        ]
    else:
        raise Exception(f"Scale named {name} does not exist")

    notes = [
        add_interval_to_note(tonic, interval)
        for interval in intervals
    ]

    return Scale(
        tonic=tonic,
        name=name,
        notes=notes,
        intervals=intervals
    )


def _parse_degrees(raw_degree, raw_base_degree, scale):
    degree = build_degree(raw_degree)
    degree_index = degree_mapping.get_index(degree.name)
    degree_alteration = degree.alteration
    diatonic_degree_index = degree_index

    base_degree = None
    if raw_base_degree:
        base_degree = build_degree(raw_base_degree)
        base_degree_index = degree_mapping.get_index(base_degree.name)

        diatonic_degree_index = degree_index + base_degree_index
        degree_alteration += base_degree.alteration

    add_octave = False
    if diatonic_degree_index >= 7:
        diatonic_degree_index %= 7
        add_octave = True

    root = scale.notes[diatonic_degree_index]

    if add_octave:
        octave = build_interval(deserialize("interval", "8"))
        root = add_interval_to_note(root, octave)

    if degree_alteration:
        root = replace(root, alteration=root.alteration + degree_alteration)

    return root, degree, degree_index, base_degree


def _apply_inversion(inversion: int, notes: List[Note]) -> List[Note]:
    if inversion == 0:
        return notes
    elif inversion < 0 or inversion > len(notes) - 1:
        raise Exception("Inversion is out of range")

    octave = build_interval(deserialize("interval", "8"))

    return notes[inversion:] + [
        add_interval_to_note(note, octave)
        for note in notes[:inversion]
    ]


def _parse_base_note(raw_base_note: dict, first_note: Note) -> Note:
    base_note = build_note(raw_base_note)

    if first_note.octave:

        base_note_octave = base_note.octave
        if not base_note_octave:
            base_note_octave = first_note.octave

        if base_note_octave > first_note.octave:
            base_note_octave = first_note.octave

        if base_note_octave == first_note.octave and (
            note_mapping.get_index(first_note.name) <
            note_mapping.get_index(base_note.name)
        ):
            base_note_octave -= 1

        base_note = replace(base_note, octave=base_note_octave)

    return base_note


def build_chord(parsed: dict, scale: Optional[Scale] = None) -> Chord:
    if name := parsed.get("name"):
        name = name.replace("_", " ")

    degree = None
    base_degree = None
    if raw_degree := parsed.get("degree"):
        if not scale:
            raise Exception("Scale must be set when using degree on chord")

        check_if_diatonic(scale)

        root, degree, degree_index, base_degree = _parse_degrees(
            raw_degree,
            parsed.get("base_degree"),
            scale
        )

        if not name:
            name = get_chords_from_scale(scale)[degree_index].name

    elif raw_root := parsed.get("root"):
        root = build_note(raw_root)

    if not name:
        name = "maj"

    if raw_intervals := chord_mapping.get_intervals(name):
        intervals = [
            build_interval(deserialize("interval", interval))
            for interval in raw_intervals.split(",")
        ]
    else:
        raise Exception(f"Chord named {name} does not exist")

    notes = [
        add_interval_to_note(root, interval)
        for interval in intervals
    ]

    if inversion := parsed.get("inversion"):
        notes = _apply_inversion(inversion, notes)

    if extensions := parsed.get("extensions"):
        extensions = [
            build_interval(deserialize("interval", extension))
            for extension in extensions.split(",")
        ]

        for extension in extensions:
            notes.append(add_interval_to_note(root, extension))

    base_note = None
    if raw_base_note := parsed.get("base_note"):
        base_note = _parse_base_note(raw_base_note, notes[0])

        notes.insert(0, base_note)

    return Chord(
        root=root,
        name=name,
        inversion=inversion,
        extensions=extensions,
        base_note=base_note,
        notes=notes,
        intervals=intervals,
        degree=degree,
        base_degree=base_degree
    )


def get_chords_from_scale(scale: Scale, degrees: List[int] = None) -> List[Chord]:
    check_if_diatonic(scale)

    degrees = degrees or [1, 3, 5, 7]
    has_octave = bool(scale.tonic.octave)

    scale_notes = scale.notes
    if has_octave:
        scale_notes = [replace(note, octave=None) for note in scale_notes]

    chords = []
    for i in range(7):
        notes = [
            scale_notes[(degree + i - 1) % 7]
            for degree in degrees
        ]
        intervals = [
            get_notes_interval(notes[0], note)
            for note in notes
        ]

        intervals_str = serialize_list(serialize_interval, intervals)
        chord_name = chord_mapping.get_name_from_intervals(intervals_str)

        chord = build_chord(
            deserialize(
                "chord",
                serialize_note(scale.notes[i]) + "_" + chord_name
            )
        )
        chords.append(chord)

    return chords


def build_grid(parsed: dict, default_settings: Optional[dict] = None) -> Grid:
    scale = None
    bpm = None
    time_signature = None
    duration = None
    chords: List[Tuple[Chord, Optional[Duration]]] = []

    if default_settings:
        scale = default_settings.get("scale", scale)
        bpm = default_settings.get("bpm", bpm)
        time_signature = default_settings.get("time_signature", time_signature)
        duration = default_settings.get("duration", duration)
        chords = default_settings.get("chords", chords)

    parts = []
    for grid_part in parsed.get("grid_parts") or []:

        if data := grid_part.get("scale"):
            scale = build_scale(data)

        if data := grid_part.get("bpm"):
            bpm = build_bpm(data)

        if data := grid_part.get("time_signature"):
            time_signature = build_time_signature(data)

        if data := grid_part.get("duration"):
            duration = build_duration(data)

        if data := grid_part.get("chords"):
            chords = []

            for chord_data in data:
                chord = build_chord(chord_data, scale=scale)

                duration = None
                if duration_data := chord_data.pop("duration", None):
                    duration = build_duration(duration_data)

                chords.append((chord, duration))

        repeat = grid_part.get("repeat", 1)

        if not bpm:
            raise Exception("Bpm must be set")

        if not time_signature:
            raise Exception("TimeSignature must be set")

        if not scale:
            raise Exception("Scale must be set")

        for chord, chord_duration in chords:

            for _ in range(repeat):
                parts.append(GridPart(
                    scale=scale,
                    chord=chord,
                    bpm=bpm,
                    time_signature=time_signature,
                    duration=chord_duration or duration
                ))

    return Grid(parts)
