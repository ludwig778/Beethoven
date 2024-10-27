from __future__ import annotations

import re
from copy import copy
from dataclasses import dataclass
from enum import Enum, auto
from functools import partial
from itertools import count
from typing import (Any, Callable, Dict, Generator, List,
                    Tuple, Type, Union)

from beethoven.models import (Bpm, Chord, ChordItem, Duration,
                              HarmonyItem, Note, Scale, TimeSection,
                              TimeSignature)
from beethoven.sequencer.registry import RegisteredPlayer
from beethoven.settings import PlayerSetting


class InvalidHarmonyChordItems(Exception):
    pass


class SequencerStrategy(Enum):
    bar = auto()
    part = auto()
    chord = auto()
    harmony = auto()
    free = auto()

@dataclass
class Mapping:
    mappings: Dict[str, Note | None]

    def get(self, name: str) -> Note | None:
        return self.mappings.get(name)
    
    def set_mapping(self, new_mapping: Dict[str, Note | None]) -> None:
        for name, note in new_mapping.items():
            if name in self.mappings:
                self.mappings[name] = note


@dataclass
class Message:
    note: Union[str, Note]
    player: BasePlayer
    velocity: int = 127
    duration: Duration = Duration()

    def __hash__(self):
        return hash(f"{self.player}:{self.note}")


class BasePlayer(RegisteredPlayer):
    is_percussion: bool = False
    mapping: Mapping | None = None

    part: Part | None = None

    def __init__(self, setting: PlayerSetting):
        self.setting = setting

        self.generator = None

    def play(self, *args, **kwargs):
        raise NotImplementedError()

    def setup(self, part: Part, strategy: Any | None = None, **kwargs):
        self.part = part
        self.strategy = strategy

        if self.generator is None:
            self.generator = self.play()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self.generator)
        except StopIteration:
            self.generator = None
            raise

    def get_message(
        self,
        note: Union[str, Note],
        duration: Duration = Duration(),
        velocity: int = 127,
        # cursor: Duration | None = None,
    ) -> Message | None:
        velocity = velocity
        duration = duration

        return Message(
            player=self,
            note=note,
            # note=note_midi_index,
            velocity=velocity,
            duration=duration,
        )


class PercussionPlayer(BasePlayer):
    is_percussion: bool = True

    def get_note(self, note_str: str, duration: Duration = Duration(), velocity: int = 127) -> Message | None:
        if self.mapping and (note := self.mapping.get(note_str)):
            return Message(
                player=self,
                note=note,
                # note=note_midi_index,
                velocity=velocity,
                duration=duration,
            )


class SystemPlayer(PercussionPlayer):
    def __init__(self, *args, callable: Callable | None = None, **kwargs):
        super(SystemPlayer, self).__init__(*args, **kwargs)

        self.callable: Callable = callable or self._none_callable
        self.generator = None

    def setup(self, part: "Part", strategy: Any | None = None, **kwargs):
        self.part = part
        self.strategy = strategy

        self.generator = self.play(part)

    def _none_callable(self, *args, **kwargs):
        pass

    def system_setup(self, callable: Callable | None = None):
        self.callable = callable or self._none_callable

    def play(self, part):
        for time_section, cursor in part.time_signature.generate_time_sections(
            Duration.parse("Q"),
            # sixteenth_duration,
            cursor_offset=part.start_cursor,
            base_time_section=part.start_time_section,
        ):
            if cursor >= part.intermediate_cursor:
                break
            # print("c", cursor, time_section)

            yield cursor, partial(self.callable, cursor, time_section, self)

        print("OUT")
        self.generator = None


class VoidPlayer(BasePlayer):
    pass


@dataclass
class Part:
    scale: Scale
    chord: Chord
    time_signature: TimeSignature
    bpm: Bpm
    start_cursor: Duration
    intermediate_cursor: Duration
    end_cursor: Duration
    end_bar_cursor: Duration
    end_harmony_cursor: Duration
    global_cursor: Duration
    split_duration: Duration
    chord_duration: Duration
    section: Section
    # grid_starting: bool
    bar_starting: bool
    chord_starting: bool
    harmony_starting: bool
    # next_harmony_item_change: bool
    start_time_section: TimeSection

    def show(self):
        # print("scale                :", self.scale)
        # print("chord                :", self.chord)
        # print("time_signature       :", self.time_signature)
        # print("bpm                  :", self.bpm)
        print("start_cursor         :", self.start_cursor)
        print("end_cursor           :", self.end_cursor)
        print("intermediate_cursor  :", self.intermediate_cursor)
        print("end_bar_cursor       :", self.end_bar_cursor)
        print("end_harmony_cursor   :", self.end_harmony_cursor)
        print("global_cursor        :", self.global_cursor)
        print("split_duration       :", self.split_duration)
        print("chord_duration       :", self.chord_duration)
        print("section              :", self.section)
        print("bar_starting         :", self.bar_starting)
        print("chord_starting       :", self.chord_starting)
        print("harmony_starting     :", self.harmony_starting)
        # print("start_time_section   :", self.start_time_section)


@dataclass
class Section:
    symbol: str = "M"
    current: int = 1
    count: int = 1

    def __str__(self):
        return f"{self.symbol}={self.current}/{self.count}"


@dataclass
class Conductor:
    sections: list

    _section_index: int = 0
    _sub_section_index: int = 0

    _section_types: str = "CLMHS"

    @classmethod
    def build(cls, string: str = ""):
        sections: List[List[Union[str, int]]] = []

        for num, section_type in re.findall(
            rf"(?P<num>\d)?(?P<section_type>[{cls._section_types}])", string
        ):
            num = int(num) if num else 1

            if sections and sections[-1][0] == section_type:
                sections[-1][1] += num
            else:
                sections.append([section_type, num])

        if not sections:
            sections.append(["M", 1])

        return cls(sections=sections)

    @property
    def current(self):
        symbol, count = self.sections[self._section_index % len(self.sections)]

        return Section(symbol=symbol, current=self._sub_section_index + 1, count=count)

    def __iter__(self):
        return self

    def __next__(self):
        count = self.sections[self._section_index % len(self.sections)][1]

        section = self.current

        self._sub_section_index += 1
        if self._sub_section_index >= count:
            self._sub_section_index = 0
            self._section_index += 1

        return section


@dataclass
class Splitter:
    conductor: Conductor
    global_cursor: Duration = Duration()
    time_signature_range_cursor: Duration = Duration()
    bar_starting: bool = True
    previous_end_time_section: TimeSection = TimeSection()
    previous_part_harmony_item: HarmonyItem | None = None
    grid_starting: bool = True

    # @lru_cache(maxsize=None)
    def get_harmony_item_chords_durations(self, harmony_item: HarmonyItem) -> Dict[ChordItem, List[Duration]]:
        time_signature_duration = harmony_item.time_signature.get_duration()

        cursor = Duration()

        chords_data = []
        for chord_item in harmony_item.chord_items:
            duration = chord_item.duration_item.value

            if duration is None:
                duration = time_signature_duration

                if rest := cursor % time_signature_duration:
                    duration -= rest

            next_cursor = cursor + duration

            chords_data.append((chord_item, duration, cursor, next_cursor))
            # print(f"= {str(cursor):4} => {str(next_cursor):5} {str(duration):5}")

            cursor = next_cursor

        harmony_item_duration = cursor

        # print(f"harmony_item_duration: {harmony_item_duration}")
        # print()

        chord_items_data = {}  # defaultdict(list)
        for chord_item, duration, cursor, next_cursor in chords_data:
            num, rest = divmod(next_cursor, time_signature_duration)

            next_bar_cursor = time_signature_duration * (num + (1 if rest else 0))

            if next_bar_cursor > harmony_item_duration:
                next_bar_cursor = harmony_item_duration

            chord_items_data[chord_item] = [
                duration, cursor, next_cursor, next_bar_cursor, harmony_item_duration
            ]

        # pprint({id(k): v for k, v in chord_items_data.items()})
        return chord_items_data

    """
    def flatten(self, harmony_iterator: HarmonyItemSelector):
        harmony_iterator.harmony_index = 0
        harmony_iterator.chord_index = 0

        current_items = harmony_iterator.current_items
        origin_items = current_items
        next_items = harmony_iterator.get_next_items()

        parts = []
        while 1:
            parts.append(self.run(current_items, next_items))

            current_items = next_items
            next_items = harmony_iterator.next()

            if next_items == origin_items:
                return parts
    """

    def run(self, sequencer_items, next_sequencer_items):
        harmony_item, chord_item = sequencer_items
        time_signature_duration = harmony_item.time_signature.get_duration()
        next_harmony_change = harmony_item is not next_sequencer_items[0]

        duration = chord_item.duration_item.value

        (
            duration, cursor, next_cursor, next_bar_cursor, harmony_item_duration
        ) = self.get_harmony_item_chords_durations(harmony_item)[chord_item]

        split, next_time_signature_cursor = divmod(
            self.time_signature_range_cursor + duration,
            time_signature_duration,
        )
        if next_time_signature_cursor:
            split += 1

        chord_sum = Duration()
        split_range_cursor = self.time_signature_range_cursor
        remaining_duration = copy(duration)

        chord_starting = True

        chord = chord_item.as_chord(harmony_item.scale)

        for _ in range(split):
            if split_range_cursor + remaining_duration > time_signature_duration:
                split_duration = time_signature_duration - split_range_cursor
                remaining_duration -= split_duration
                end_bar_cursor = self.global_cursor + split_duration
                next_bar_starting = True
            else:
                split_duration = remaining_duration
                if split_range_cursor + remaining_duration == time_signature_duration:
                    next_bar_starting = True
                else:
                    next_bar_starting = False
                remaining_duration = Duration()
                end_bar_cursor = self.global_cursor + next_bar_cursor - cursor

            bar_offset = self.previous_end_time_section.bar - 1
            start_time_section = harmony_item.time_signature.get_time_section(
                self.time_signature_range_cursor + chord_sum, bar_offset=bar_offset
            )
            end_time_section = harmony_item.time_signature.get_time_section(
                self.time_signature_range_cursor + chord_sum + split_duration, bar_offset=bar_offset
            )

            harmony_starting = harmony_item != self.previous_part_harmony_item

            yield Part(
                scale=harmony_item.scale,
                chord=chord,
                time_signature=harmony_item.time_signature,
                bpm=harmony_item.bpm,
                start_cursor=self.global_cursor + chord_sum,
                intermediate_cursor=self.global_cursor + chord_sum + split_duration,
                end_cursor=self.global_cursor + duration,
                end_bar_cursor=end_bar_cursor,
                end_harmony_cursor=self.global_cursor + harmony_item_duration - cursor,
                global_cursor=self.global_cursor,
                split_duration=split_duration,
                chord_duration=duration,
                # next_harmony_item_change=next_harmony_change,
                section=self.conductor.current,
                bar_starting=self.bar_starting,
                chord_starting=chord_starting,
                harmony_starting=harmony_starting,
                start_time_section=start_time_section
            )

            chord_starting = False

            self.bar_starting = next_bar_starting
            self.previous_part_harmony_item = harmony_item

            if next_bar_starting:
                split_range_cursor = Duration()

            chord_sum += split_duration
            if next_bar_starting or next_harmony_change:
                next(self.conductor)

        self.global_cursor += duration
        self.time_signature_range_cursor = next_time_signature_cursor

        self.previous_end_time_section = end_time_section
        if next_harmony_change:
            self.bar_starting = True
            self.previous_end_time_section.to_next_bar()
            self.time_signature_range_cursor = Duration()


@dataclass
class HarmonyItemSelector:
    harmony_items: List[HarmonyItem]
    harmony_index: int = 0
    chord_index: int = 0

    chord_looping: bool = False

    def set_chord_looping(self, chord_looping):
        self.chord_looping = chord_looping

    @property
    def current_harmony_item(self) -> HarmonyItem:
        return self.harmony_items[self.harmony_index]

    @property
    def current_chord_item(self) -> ChordItem:
        return self.current_harmony_item.chord_items[self.chord_index]

    @property
    def current_items(self) -> Tuple[HarmonyItem, ChordItem]:
        harmony_item = self.harmony_items[self.harmony_index]
        return harmony_item, harmony_item.chord_items[self.chord_index]

    @property
    def current_indexes(self) -> Tuple[int, int]:
        return self.harmony_index, self.chord_index

    def set(self, harmony_item: HarmonyItem, chord_item: ChordItem):
        try:
            self.harmony_index = self.harmony_items.index(harmony_item)
            self.chord_index = harmony_item.chord_items.index(chord_item)
        except ValueError:
            raise InvalidHarmonyChordItems()

    def reset(self):
        self.harmony_index = 0
        self.chord_index = 0

    def insert(self, item: Union[HarmonyItem, ChordItem]):
        if isinstance(item, HarmonyItem):
            self.harmony_items.insert(self.harmony_index + 1, item)
        elif isinstance(item, ChordItem):
            self.current_harmony_item.chord_items.insert(self.chord_index + 1, item)
        else:
            raise Exception(f"Check this : {item = }")

    def delete(self, item_type: Union[Type[HarmonyItem], Type[ChordItem]]):
        if item_type is HarmonyItem:
            if len(self.harmony_items) == 1:
                return

            del self.harmony_items[self.harmony_index]

            if self.harmony_index == len(self.harmony_items):
                self.harmony_index -= 1
        elif item_type is ChordItem:
            if len(self.current_harmony_item.chord_items) == 1:
                return

            del self.current_harmony_item.chord_items[self.chord_index]

            if self.chord_index == len(self.current_harmony_item.chord_items):
                self.chord_index -= 1
        else:
            raise Exception(f"Check this : {item_type = }")

    def get_next_items(self) -> Tuple[Tuple[HarmonyItem, ChordItem], Tuple[int, int]]:
        harmony_index = self.harmony_index
        harmony_item = self.harmony_items[harmony_index]

        try:
            chord_index = self.chord_index + 1
            chord_item = harmony_item.chord_items[chord_index]
        except IndexError:
            try:
                if not self.chord_looping:
                    harmony_index = self.harmony_index + 1
                    harmony_item = self.harmony_items[harmony_index]

                chord_index = 0
                chord_item = harmony_item.chord_items[chord_index]
            except IndexError:
                harmony_index, chord_index = 0, 0
                harmony_item = self.harmony_items[harmony_index]
                chord_item = harmony_item.chord_items[chord_index]

        return (harmony_item, chord_item), (harmony_index, chord_index)

    def next(self) -> Tuple[HarmonyItem, ChordItem]:
        items, indexes = self.get_next_items()

        self.harmony_index, self.chord_index = indexes

        return items

    def get_previous_items(self) -> Tuple[Tuple[HarmonyItem, ChordItem], Tuple[int, int]]:
        harmony_index = self.harmony_index
        harmony_item = self.harmony_items[harmony_index]

        chord_index = self.chord_index - 1

        if self.chord_looping and chord_index < 0:
            chord_index = len(harmony_item.chord_items) - 1
            chord_item = harmony_item.chord_items[chord_index]
        elif chord_index < 0:
            harmony_index = self.harmony_index - 1
            if harmony_index < 0:
                harmony_index = len(self.harmony_items) - 1
                harmony_item = self.harmony_items[harmony_index]
                chord_index = len(harmony_item.chord_items) - 1
                chord_item = harmony_item.chord_items[chord_index]
            else:
                harmony_item = self.harmony_items[harmony_index]
                chord_index = len(harmony_item.chord_items) - 1
                chord_item = harmony_item.chord_items[chord_index]
        else:
            chord_item = harmony_item.chord_items[chord_index]

        return (harmony_item, chord_item), (harmony_index, chord_index)

    def previous(self) -> Tuple[HarmonyItem, ChordItem]:
        items, indexes = self.get_previous_items()

        self.harmony_index, self.chord_index = indexes

        return items

    def run_for(self, full_round: int = 1):
        count = 0
        for h in self.harmony_items:
            for c in h.chord_items:
                count += 1

        for i in range(full_round):
            for j in range(count):
                if i or j:
                    self.next()

                yield self.current_items, self.get_next_items()

    def run(self):
        for i in count(0):
            if i:
                self.next()

            yield self.current_items, self.get_next_items()


OptionalMessage = Message | None

MessageGenerator = Generator[Tuple[Duration, Message], None, None]
OptionalMessageGenerator = Generator[Tuple[Duration, OptionalMessage], None, None]

MessageGeneratorClass = Callable[..., MessageGenerator]
OptionalMessageGeneratorClass = Callable[..., OptionalMessageGenerator]
