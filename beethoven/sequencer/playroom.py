from collections import defaultdict
from fractions import Fraction
from time import sleep
from typing import Any, Callable, List, Optional

from pydantic import BaseModel

from beethoven.adapters.midi import MidiAdapter, MidiMessage, Output
from beethoven.helpers.grid import (
    fix_grid_parts_durations,
    get_ordered_grid_parts_by_time_signature,
)
from beethoven.helpers.player import split_player_by_types
from beethoven.helpers.sequencer import update_timeline_for_player
from beethoven.models import Duration, Grid, GridPart
from beethoven.sequencer.players.base import BasePlayer, PercussionPlayer


class Piano(BasePlayer):
    def play(self):
        timeline = Duration(value=0)

        duration = Duration(value=4)

        while True:
            for note in self.grid_part.chord.notes:
                yield timeline, self.play_note(note.midi_index, duration=duration)

            timeline += duration


class Drum(PercussionPlayer):
    def play(self):
        pass


class Metronome(PercussionPlayer):
    def play(self):
        timeline = Duration(value=0)

        while True:
            yield timeline, self.play_note(23, duration=Duration(value=0))

            timeline += Duration(value=1)


class PlayerSettings(BaseModel):
    player: BasePlayer
    output: Output
    channel: int

    class Config:
        arbitrary_types_allowed = True


def play_grid(
    midi_adapter: MidiAdapter,
    players: List[BasePlayer],
    grid: Grid,
    on_grid_part_change: Optional[Callable] = None,
) -> None:
    grid = fix_grid_parts_durations(grid)
    grid_part_by_time_signatures = get_ordered_grid_parts_by_time_signature(grid)

    regular_players, percussion_players = split_player_by_types(players)

    timeline = Duration(value=0)

    timeline_events: Any = defaultdict(list)

    total_durations = Duration(value=0)

    for _, grid_parts in grid_part_by_time_signatures:
        total_duration: Duration = sum(
            [grid_part.duration for grid_part in grid_parts if grid_part.duration],
            start=Duration(value=0),
        )
        total_durations += total_duration

        for player in percussion_players:
            player.setup(grid_parts[0])

            update_timeline_for_player(
                timeline_events, player, limit=total_duration, offset=timeline
            )

        for grid_part in grid_parts:
            timeline_events[timeline].insert(0, grid_part)

            for player in regular_players:
                player.setup(grid_part)

                update_timeline_for_player(
                    timeline_events, player, limit=grid_part.duration, offset=timeline
                )

            timeline += grid_part.duration

    last_time_cursor = Duration(value=0)

    current_bpm = grid.parts[0].bpm

    for time_cursor, events in sorted(timeline_events.items(), key=lambda x: x[0]):
        sleep_time = time_cursor - last_time_cursor

        if sleep_time.value != Fraction(0):
            sleep_time *= Fraction(60, current_bpm.value)

            sleep(float(sleep_time.value))

        for event in events:
            if isinstance(event, GridPart):
                if event.bpm and event.bpm != current_bpm:
                    current_bpm = event.bpm

                if on_grid_part_change:
                    on_grid_part_change(event)

            elif isinstance(event, MidiMessage):
                midi_adapter.send_message(event)

        last_time_cursor = time_cursor

    # TODO CHECK IF USED
    if True:
        sleep_time = total_durations - last_time_cursor

        if sleep_time.value != Fraction(0):
            sleep_time *= Fraction(60, current_bpm.value)

            sleep(float(sleep_time.value))

    return
