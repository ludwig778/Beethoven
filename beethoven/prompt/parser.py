from copy import copy

from beethoven.models import GridPart
from beethoven.prompt.parsers import COMPOSE_PARSER, SECTION_PARSER
from beethoven.prompt.state import state
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
            extensions=extensions,
            strict=state.prompt_config.get("strict")
    )):
        chord = Chord.get_from_fullname(
            parsed_config.get("chord"),
            inversion=inversion,
            base_note=base_note,
            extensions=extensions
        )

    parsed["chord"] = chord

    return parsed


def expand_harmony_string(string, extra_config=None):
    harmony_list = []
    extra_config = extra_config or {}

    harmony_strings = (
        COMPOSE_PARSER
        .parseString(string)
        .get("harmony_strings")
    ) or []

    for sub_config in harmony_strings:

        section_parsed = SECTION_PARSER.parseString(sub_config)

        bypass = section_parsed.pop("bypass", False)
        repeat = section_parsed.pop("repeat", 1)
        command = section_parsed.pop("command", None)
        progression = section_parsed.pop("progression", [])

        section_extra_config = {
            **section_parsed,
            **extra_config
        }

        if command:
            if obj := GridPart.get(command):
                next_grid = expand_harmony_string(obj.text, section_extra_config)
            else:
                next_grid = expand_harmony_string(f"p={command}", section_extra_config)

            harmony_list += next_grid * repeat
        else:
            harmony_list += [
                {
                    "progression": progression,
                    "bypass": bypass,
                    **dict(section_parsed),
                    **extra_config
                }
            ] * repeat

    return harmony_list


def handle_global_commands(string):
    interrupt = False

    parsed = COMPOSE_PARSER.parseString(string)

    if value := parsed.get("register"):
        text = "; ".join(parsed.get("harmony_strings"))

        if obj := GridPart.get(value):
            print("updated")
            obj.update(text=text)

        else:
            print("created")
            obj = GridPart.create(value, text=text)

        state.grid_parts[obj.name] = obj
        interrupt = True

    elif value := parsed.get("delete"):
        if obj := GridPart.get(value):
            obj.delete()
            print("deleted")
            state.grid_parts.pop(value, None)

        interrupt = True

    elif parsed.get("settings"):

        print("Scale            :", state.config.get("scale"))
        print("Tempo            :", state.config.get("tempo"))
        print("Duration         :", state.config.get("duration"))
        print("Time signature   :", state.config.get("time_signature"))

        if state.config.get("last_progression"):
            print("Last progression :", state.config.get("last_progression").asList())

        interrupt = True

    elif parsed.get("info") is not None:
        values = parsed.get("info")

        if not values:
            for obj in sorted(GridPart.list(), key=lambda o: o.name):
                print(f"{obj.name:23s}: {obj.text}")

        else:
            for value in values:
                if obj := GridPart.get(value):
                    print("  ", obj.text)

                else:
                    print("no infos")

        interrupt = True

    return interrupt


def prompt_harmony_list_parser(string, full_config=None):
    parsed_harmony_list = []
    config = copy(full_config) if full_config else {}
    last_progression = config.pop("last_progression", None)

    if handle_global_commands(string):
        return

    harmony_list = expand_harmony_string(string)

    current_scale = config.get("scale")

    for section_parsed in harmony_list:
        config = {
            **config,
            **process_config(
                section_parsed,
                current_scale
            )
        }

        if config.get("scale"):
            current_scale = config["scale"]
        elif not current_scale:
            continue

        progression = (
            config.pop("progression", None) or last_progression or []
        )

        if full_config:
            full_config.update(config)

        if section_parsed.pop("bypass", False):
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
