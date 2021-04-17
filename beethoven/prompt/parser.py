from copy import copy

from beethoven.prompt.parsers import PARSER
from beethoven.sequencer.note_duration import (Eighths, Half, Quarter,
                                               Sixteenths, Whole)
from beethoven.sequencer.tempo import Tempo  # , default_tempo_factory
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.chord import Chord
from beethoven.theory.harmony import Harmony
from beethoven.theory.note import Note
from beethoven.theory.scale import Scale


def process_config(parsed_config, current_scale=None):
    parsed = {}
    scale_updated = False

    scale_name = None
    tonic_note = None
    if current_scale:
        scale_name = current_scale.name
        tonic_note = current_scale.tonic

    if scale_name := parsed_config.get("scale"):
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

    if not (chord := Harmony(current_scale).get(
            parsed_config.get("chord"),
            inversion=inversion,
            base_note=base_note,
            base_degree=base_degree
    )):
        chord = Chord.get_from_fullname(parsed_config.get("chord"), inversion=inversion, base_note=base_note)

    parsed["chord"] = chord

    return parsed


def prompt_harmony_list_parser(string):
    parsed_harmony_list = []
    config = {}

    current_scale = None

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

        if not config.get("progression"):
            continue

        for item in config.pop("progression"):
            config.update(process_chord_config(item, current_scale))

            parsed_harmony_list.append(copy(config))

            config.pop("scale", None)
            config.pop("duration", None)
            config.pop("tempo", None)
            config.pop("time_signature", None)

    return parsed_harmony_list
