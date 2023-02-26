from collections import defaultdict
from dataclasses import dataclass, field
from time import sleep
from typing import Callable, Dict, List, Optional, Tuple

from beethoven.adapters.midi import MidiAdapter
from beethoven.helpers.midi import get_on_off_messages
from beethoven.helpers.sequencer import SequencerSorter
from beethoven.models import Bpm, ChordItem, Duration, HarmonyItem, TimeSection
from beethoven.sequencer.players import BasePlayer, SystemPlayer
from beethoven.types import SequencerItems
from beethoven.ui.constants import DEFAULT_TIME_SIGNATURE


@dataclass
class SequencerItemIterator:
    current_items: SequencerItems
    next_items: SequencerItems
    next_items_updater: Callable[[HarmonyItem, ChordItem], SequencerItems]

    @classmethod
    def setup(cls, current_items, next_items_updater):
        next_items = next_items_updater(*current_items)

        return cls(
            current_items=current_items,
            next_items=next_items,
            next_items_updater=next_items_updater,
        )

    def reset(self, new_current_items: SequencerItems):
        self.current_items = new_current_items
        self.next_items = self.next_items_updater(*self.current_items)

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[SequencerItems, SequencerItems]:
        self.current_items = self.next_items
        self.next_items = self.next_items_updater(*self.next_items)

        return self.current_items, self.next_items

    def run(self):
        yield self.current_items, self.next_items

        yield from self


@dataclass
class SequencerParams:
    item_iterator: SequencerItemIterator
    players: List[BasePlayer] = field(default_factory=list)

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

    def set_players(self, players: Optional[List[BasePlayer]] = None):
        self.players = players or []

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

        self._system_player = SystemPlayer()

        self.reset()

    def setup(self, params: SequencerParams):
        self.params = params

    def get_players(self):
        return [*self.params.players, self._system_player]

    def reset(self):
        self.global_cursor = Duration()
        self.previous_time_signature = None

        self.previous_harmony_end_time_section = TimeSection()
        self.previous_harmony_item = None

    def run(self):  # noqa: C901
        self.previous_harmony_end_time_section.to_next_bar()

        sequencer_sorter = SequencerSorter(players=self.get_players())

        self._system_player.system_setup(callable=self.params.on_tick)

        for [harmony_item, chord_item], _ in self.params.item_iterator.run():
            if self.params.on_harmony_item_change:
                self.params.on_harmony_item_change(harmony_item)

            if self.params.continuous or self.params.preview:
                harmony_time_signature = DEFAULT_TIME_SIGNATURE
                harmony_time_signature_duration = (
                    harmony_time_signature.get_duration()
                    * self.continuous_duration_ratio
                )
            else:
                harmony_time_signature = harmony_item.time_signature
                harmony_time_signature_duration = harmony_time_signature.get_duration()

            chord_sum = Duration()
            if harmony_item != self.previous_harmony_item:
                chord_sum = Duration()

            bar_offset = self.previous_harmony_end_time_section.bar - 1

            for player in self.get_players():
                player.reset()

            if self.params.on_chord_item_change:
                self.params.on_chord_item_change(harmony_item, chord_item)

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

            self.previous_harmony_end_time_section = end_chord_time_section
            self.previous_harmony_item = harmony_item

            sequencer_sorter.setup(
                scale=harmony_item.scale,
                chord=chord_item.as_chord(harmony_item.scale),
                time_signature=harmony_time_signature,
                start_cursor=start_cursor,
                end_cursor=end_cursor,
                start_time_section=start_chord_time_section,
            )

            last_cursor = start_cursor

            for cursor, msg in self.sort_sequencer_sorter_messages(sequencer_sorter):
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

            if self.params.preview:
                self.params.preview = False

                break

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
