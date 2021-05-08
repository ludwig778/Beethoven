from copy import copy

from beethoven.prompt.parsers import PARSER
from beethoven.sequencer.note_duration import (Eighths, Half, Quarter,
                                               Sixteenths, Whole)
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.interval import Interval
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


def process_config(parsed_config, current_scale=None):
    parsed = {}
    scale_updated = False

    scale_name = None
    tonic_note = None
    if current_scale:
        scale_name = str(current_scale.name)
        tonic_note = current_scale.tonic

    if scale_name_value := parsed_config.get("scale"):
        scale_name = scale_name_value
        scale_updated = True

    if tonic_name := parsed_config.get("note"):
        tonic_note = Note(tonic_name)
        scale_updated = True

    if scale_updated and scale_name and tonic_note:
        parsed["scale"] = Scale(tonic_note, scale_name)
    elif not current_scale:
        return parsed

    if progression := parsed_config.get("progression"):
        parsed["progression"] = progression

    if time_signature := parsed_config.get("time_signature"):
        parsed["time_signature"] = TimeSignature(*time_signature)

    if tempo := parsed_config.get("tempo"):
        parsed["tempo"] = Tempo(tempo)

    return parsed


def process_chord_config(parsed_config, current_scale=None):
    parsed = {}

    # GET CHORD DURATION
    if duration := parsed_config.get("duration"):
        chord_duration = {
            "W": Whole,
            "H": Half,
            "Q": Quarter,
            "E": Eighths,
            "S": Sixteenths,
        }[duration]

        if chord_duration and (duration_count := parsed_config.get("duration_count")):
            chord_duration *= int(duration_count)

        if chord_duration:
            parsed["duration"] = chord_duration

    if inversion := parsed_config.get("inversion"):
        pass

    # GET BASE NOTE OR INVERSION
    base_note = None
    base_degree = None
    if base := parsed_config.get("base"):
        try:
            base_note = Note(base)
        except (ValueError, AttributeError):
            # base_degree_interval = harmony.get_base_degree_interval(raw_data)
            base_degree = base

    if extensions := parsed_config.get("extensions"):
        extensions = {Interval(e) for e in extensions}

    if not (chord := Harmony(current_scale).get(
            parsed_config.get("chord"),
            inversion=inversion,
            base_note=base_note,
            base_degree=base_degree,
            extensions=extensions
    )):
        chord = Chord.get_from_fullname(
            parsed_config.get("chord"),
            inversion=inversion,
            base_note=base_note,
            extensions=extensions
        )

    parsed["chord"] = chord

    return parsed


def prompt_harmony_list_parser(string, full_config=None):
    parsed_harmony_list = []
    config = full_config or {}

    current_scale = config.get("scale")

    for sub_config in PARSER.parseString(string).get("harmony_list"):

        if not sub_config:
            continue

        config = process_config(
            sub_config,
            current_scale
        )

        if config.get("scale"):
            current_scale = config["scale"]
        elif not current_scale:
            continue

        progression = (
            config.pop("progression", None) or
            full_config and full_config.get("last_progression") or []
        )

        if not progression:
            if full_config is not None:
                full_config.update(config)
            continue

        for item in progression:
            config.update(process_chord_config(item, current_scale))

            parsed_harmony_list.append(copy(config))

            if full_config is not None:
                full_config.update(config)

            config.pop("scale", None)
            config.pop("duration", None)
            config.pop("tempo", None)
            config.pop("time_signature", None)

        if full_config is not None:
            full_config.update({"last_progression": progression})

    return parsed_harmony_list
