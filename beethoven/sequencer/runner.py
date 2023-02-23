from collections import defaultdict
from time import sleep
from typing import Callable, Dict, List, Optional

from pydantic import BaseModel, Field

from beethoven.adapters.midi import MidiAdapter
from beethoven.helpers.midi import get_on_off_messages
from beethoven.helpers.sequencer import SequencerSorter
from beethoven.models import Bpm, Duration, TimeSection
from beethoven.sequencer.players import BasePlayer, SystemPlayer
from beethoven.ui.constants import DEFAULT_TIME_SIGNATURE
from beethoven.ui.models import ChordItem, HarmonyItem


class SequencerParams(BaseModel):
    harmony_items: List[HarmonyItem] = Field(default_factory=list)
    players: List[BasePlayer] = Field(default_factory=list)

    first_harmony_item: Optional[HarmonyItem] = None
    first_chord_item: Optional[ChordItem] = None

    selected_harmony_items: List[HarmonyItem] = Field(default_factory=list)
    selected_chord_items: List[ChordItem] = Field(default_factory=list)

    continuous: bool = False
    preview: bool = False

    on_tick: Optional[Callable] = None
    on_time_signature_change: Optional[Callable] = None
    on_harmony_item_change: Optional[Callable] = None
    on_chord_item_change: Optional[Callable] = None
    on_grid_end: Optional[Callable] = None

    class Config:
        arbitrary_types_allowed = True

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def clear_first_items(self):
        return self.set_first_items()

    def set_first_items(
        self,
        first_harmony_item: Optional[HarmonyItem] = None,
        first_chord_item: Optional[ChordItem] = None,
    ):
        self.first_harmony_item = first_harmony_item
        self.first_chord_item = first_chord_item

        return self

    def set_players(self, players: Optional[List[BasePlayer]] = None):
        self.players = players or []

        return self

    def clear_ranges(self):
        self.selected_harmony_items = []
        self.selected_chord_items = []

        return self

    def set_ranges(
        self,
        selected_harmony_items: Optional[List[HarmonyItem]] = None,
        selected_chord_items: Optional[List[ChordItem]] = None,
    ):
        self.selected_harmony_items = selected_harmony_items or []
        self.selected_chord_items = selected_chord_items or []

        return self

    def clear_options(self):
        return self.set_options()

    def set_options(
        self,
        continuous: bool = False,
        preview: bool = False,
    ):
        self.continuous = continuous
        self.preview = preview

        return self


class Sequencer:
    continuous_duration_ratio = 2

    def __init__(self, midi_adapter: MidiAdapter):
        self.midi_adapter = midi_adapter

        self.params = SequencerParams()

        self.current_harmony_item: Optional[HarmonyItem] = None
        self.current_chord_item: Optional[ChordItem] = None

        self._system_player = SystemPlayer()

        self.reset()

    def setup(self, params: SequencerParams):
        self.params = params

    def get_players(self):
        return [*self.params.players, self._system_player]

    def reset(self):
        self.global_cursor = Duration()
        self.previous_time_signature = None

    def get_harmony_items(self):
        next_harmony_item_index = 0

        if self.params.first_harmony_item:
            if self.params.first_harmony_item in self.params.harmony_items:
                next_harmony_item_index = self.params.first_harmony_item.get_index_from(
                    self.params.harmony_items
                )

            self.params.first_harmony_item = None

        while 1:
            self.current_harmony_item = self.params.harmony_items[
                next_harmony_item_index
            ]

            if (
                self.params.selected_harmony_items
                and self.current_harmony_item.is_in(self.params.selected_harmony_items)
                or not self.params.selected_harmony_items
            ):
                yield self.current_harmony_item

            if self.params.preview:
                break

            current_harmony_item_index = self.current_harmony_item.get_index_from(
                self.params.harmony_items
            )
            next_harmony_item_index = current_harmony_item_index + 1

            if next_harmony_item_index >= len(self.params.harmony_items):
                next_harmony_item_index = 0

    def get_chords_items(self):
        next_chord_item_index = 0

        if not self.current_harmony_item:
            return

        if self.params.first_chord_item:
            if self.params.first_chord_item in self.current_harmony_item.chord_items:
                next_chord_item_index = self.params.first_chord_item.get_index_from(
                    self.current_harmony_item.chord_items
                )

            self.params.first_chord_item = None

        while 1:
            self.current_chord_item = self.current_harmony_item.chord_items[
                next_chord_item_index
            ]

            if (
                self.params.selected_chord_items
                and self.current_chord_item.is_in(self.params.selected_chord_items)
                or not self.params.selected_chord_items
            ):
                yield self.current_chord_item

            if self.params.preview:
                break

            current_chord_item_index = self.current_chord_item.get_index_from(
                self.current_harmony_item.chord_items
            )
            next_chord_item_index = current_chord_item_index + 1

            if next_chord_item_index >= len(self.current_harmony_item.chord_items):
                break

    def run(self):  # noqa: C901
        previous_harmony_end_time_section = TimeSection()

        sequencer_sorter = SequencerSorter(players=self.get_players())

        self._system_player.system_setup(callable=self.params.on_tick)

        for harmony_item in self.get_harmony_items():
            if self.params.on_harmony_item_change:
                self.params.on_harmony_item_change(harmony_item)

            if self.params.continuous:
                harmony_time_signature = DEFAULT_TIME_SIGNATURE
                harmony_time_signature_duration = (
                    harmony_time_signature.get_duration() * self.continuous_duration_ratio
                )
            else:
                harmony_time_signature = harmony_item.time_signature
                harmony_time_signature_duration = harmony_time_signature.get_duration()

            chord_sum = Duration()
            bar_offset = previous_harmony_end_time_section.bar - 1

            for player in self.get_players():
                player.reset()

            for chord_item in self.get_chords_items():
                if self.params.on_chord_item_change:
                    self.params.on_chord_item_change(chord_item, harmony_item)

                if self.params.continuous:
                    chord_duration = harmony_time_signature_duration
                elif chord_duration := chord_item.duration_item.value:
                    pass
                elif chord_sum.value:
                    chord_duration = harmony_time_signature_duration - (
                        chord_sum % harmony_time_signature_duration
                    )
                else:
                    chord_duration = harmony_time_signature_duration

                chord_sum += chord_duration

                start_chord_time_section = harmony_time_signature.get_time_section(
                    chord_sum - chord_duration, bar_offset=bar_offset
                )
                end_chord_time_section = harmony_time_signature.get_time_section(
                    chord_sum, bar_offset=bar_offset
                )
                start_cursor = self.global_cursor + chord_sum - chord_duration
                end_cursor = self.global_cursor + chord_sum

                if self.previous_time_signature != harmony_item.time_signature:
                    if self.params.on_time_signature_change:
                        self.params.on_time_signature_change(
                            self.previous_time_signature, harmony_item.time_signature
                        )

                    self.previous_time_signature = harmony_item.time_signature

                sequencer_sorter.setup(
                    scale=harmony_item.scale,
                    chord=chord_item.as_chord(harmony_item.scale),
                    time_signature=harmony_time_signature,
                    start_cursor=start_cursor,
                    end_cursor=end_cursor,
                    start_time_section=start_chord_time_section,
                )

                last_cursor = start_cursor

                for cursor, msg in self.sort_sequencer_sorter_messages(
                    sequencer_sorter
                ):
                    if cursor > last_cursor:
                        self.sleep_for_gap(last_cursor, cursor, bpm=harmony_item.bpm)

                    if callable(msg):
                        msg()
                    else:
                        self.midi_adapter.send_message(msg)

                    last_cursor = cursor

                if last_cursor < end_cursor:
                    self.sleep_for_gap(last_cursor, end_cursor, bpm=harmony_item.bpm)

            self.global_cursor = end_cursor

            previous_harmony_end_time_section = end_chord_time_section

            if self.params.on_grid_end:
                self.params.on_grid_end()

    @staticmethod
    def sort_sequencer_sorter_messages(sequencer_sorter: SequencerSorter):
        values: Dict[str, list] = defaultdict(list)

        for cursor, msg in sequencer_sorter:
            for value_cursor in list(values.keys()):
                if value_cursor < cursor:
                    for msg in values.pop(value_cursor):
                        yield value_cursor, msg

            if callable(msg):
                yield cursor, msg
            else:
                player = msg["player"]
                duration = msg["duration"]

                note_on, note_off = get_on_off_messages(
                    note_index=msg["note"],
                    output=player.output,
                    channel=player.channel,
                    velocity=msg["velocity"],
                )

                yield cursor, note_on

                if duration == Duration():
                    yield cursor, note_off
                else:
                    values[cursor + duration].append(note_off)

        for value_cursor in sorted(list(values.keys())):
            for msg in values.pop(value_cursor):
                yield value_cursor, msg

    @staticmethod
    def sleep_for_gap(cursor, end_cursor, bpm: Bpm):
        sleep(float((end_cursor - cursor).value * 60 / bpm.value))
