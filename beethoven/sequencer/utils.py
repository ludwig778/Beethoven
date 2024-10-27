import logging
import sys
from contextlib import contextmanager
from dataclasses import replace
from itertools import product
from logging import Logger
from pathlib import Path
from typing import Callable, List

from beethoven.adapters.midi import MidiAdapter
from beethoven.models import (ChordItem, Degree, Duration, DurationItem,
                              HarmonyItem, Note, Scale, TimeSection)
from beethoven.sequencer.objects import BasePlayer
from beethoven.sequencer.registry import RegisteredPlayer
from beethoven.settings import PlayerSetting


# TODO: Set as an helper, maybe ?
def setup_players(midi_adapter: MidiAdapter, player_settings: List[PlayerSetting]) -> List[BasePlayer]:
    players = []

    for player_setting in player_settings:
        player_class = RegisteredPlayer.get_instrument_style(
            player_setting.instrument_name, player_setting.instrument_style
        )

        if not player_class:
            continue

        player = player_class(setting=player_setting)

        # if player_setting.output_name:
        #    player.setup_midi(
        #        output=midi_adapter.open_output(player_setting.output_name),
        #        channel=player_setting.channel,
        #    )

        players.append(player)

    return players



def system_tick_logger(logger: Logger, level: int = logging.INFO):
    def wrapper(cursor: Duration, time_section: TimeSection, player: BasePlayer):
        assert player.part, "Part must be set"
        logger.log(
            level,
            f"{float(cursor.value):<5}  "
            f"{player.part.time_signature.beats_per_bar}/{player.part.time_signature.beat_unit}  "
            f"{str(time_section):38s}   end: {float(player.part.end_cursor.value)}",
        )

    return wrapper


def get_scale_notes_within_range(low_range: Note, high_range: Note, scale: Scale) -> List[Note]:
    notes_by_index = {}

    if not (low_range.octave and high_range.octave):
        raise Exception("Invalid range")

    for octave, note in product(range(low_range.octave - 1, high_range.octave + 1), scale.notes):
        note = replace(note, octave=octave)
        notes_by_index[note.midi_index] = note

    low_range_index = low_range.midi_index
    high_range_index = high_range.midi_index

    notes = [
        note
        for index, note in sorted(notes_by_index.items(), key=lambda x: x[0])
        if low_range_index <= index <= high_range_index
    ]

    return notes
