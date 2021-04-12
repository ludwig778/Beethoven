from copy import copy

from beethoven.sequencer.note_duration import (Eighths, Half, Quarter,
                                               Sixteenths, Whole)
from beethoven.sequencer.tempo import Tempo  # , default_tempo_factory
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale
from beethoven.utils.regex import PROMPT_ENTRY_PARSERS


def parse_global_config_string(config_str, current_scale=None):
    parsed = {}
    scale_updated = False

    scale_name = None
    tonic_note = None
    if current_scale:
        scale_name = current_scale.name
        tonic_note = current_scale.tonic

    if match_scale := PROMPT_ENTRY_PARSERS["scale"].search(config_str):
        scale_name = match_scale.groupdict().get("scale")
        scale_updated = True

    if match_tonic := PROMPT_ENTRY_PARSERS["note"].search(config_str):
        tonic_note = Note(match_tonic.groupdict().get("note"))
        scale_updated = True

    if scale_updated and scale_name and tonic_note:
        parsed["scale"] = Scale(tonic_note, scale_name)
    elif not current_scale:
        return parsed

    if match := PROMPT_ENTRY_PARSERS["progression"].search(config_str):
        parsed["progression"] = match.groupdict().get("progression").replace("_", " ")

    if match := PROMPT_ENTRY_PARSERS["time_signature"].search(config_str):
        parsed["time_signature"] = TimeSignature(*map(int, match.groupdict().get("time_signature").split("/")))

    if match := PROMPT_ENTRY_PARSERS["tempo"].search(config_str):
        parsed["tempo"] = Tempo(int(match.groupdict().get("tempo")))

    return parsed


def parse_chord_config_string(config_str, current_scale=None):
    parsed = {}

    # GET CHORD DURATION
    splitted = config_str.rsplit(":", 1)
    chord_duration = None
    if len(splitted) == 2:
        config_str, raw_duration = splitted
        chord_duration = {
            "W": Whole,
            "H": Half,
            "Q": Quarter,
            "E": Eighths,
            "S": Sixteenths,
        }[raw_duration[-1]]

        if len(raw_duration) == 2 and raw_duration[0].isdigit():
            chord_duration *= int(raw_duration[0])

        if chord_duration:
            parsed["duration"] = chord_duration

    # GET BASE NOTE OR INVERSION
    splitted = config_str.rsplit("/", 1)
    inversion = None
    base_note = None
    base_degree = None
    raw_data = None
    if len(splitted) == 2:
        config_str, raw_data = splitted
        if raw_data.isdigit():
            inversion = int(raw_data)
        else:
            try:
                base_note = Note(raw_data)
            except (ValueError, AttributeError):
                # base_degree_interval = harmony.get_base_degree_interval(raw_data)
                base_degree = raw_data

    if not (chord := Harmony(current_scale).get(
            config_str,
            inversion=inversion,
            base_note=base_note,
            base_degree=base_degree
    )):
        chord = Chord.get_from_fullname(config_str, inversion=inversion, base_note=base_note)

    parsed["chord"] = chord

    return parsed


def prompt_harmony_list_parser(string):
    parsed_harmony_list = []
    config = {}

    current_scale = None

    for sub_string in string.split(";"):
        if not sub_string:
            continue

        config = parse_global_config_string(
            sub_string,
            current_scale
        )

        if config.get("scale"):
            current_scale = config["scale"]
        elif not current_scale:
            continue

        if not config.get("progression"):
            continue

        for item in config.pop("progression").split(","):
            config.update(parse_chord_config_string(item, current_scale))

            parsed_harmony_list.append(copy(config))

            config.pop("scale", None)
            config.pop("duration", None)

    return parsed_harmony_list
