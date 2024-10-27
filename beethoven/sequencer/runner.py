from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
from itertools import cycle
from pprint import pprint
from time import sleep
from typing import Dict, List, Protocol, Sequence, Tuple, TypeVar

from mido.backends.rtmidi import Output  # type: ignore[import]
from PySide6.QtCore import SignalInstance

from beethoven.adapters.midi import MidiAdapter, MidiMessage
from beethoven.models import (ChordItem, Duration, DurationItem,
                              HarmonyItem, TimeSection, TimeSignature)
from beethoven.sequencer.objects import BasePlayer, Message, Conductor, SequencerStrategy, Splitter, HarmonyItemSelector, SequencerStrategy, Part

# from beethoven.ui.constants import DEFAULT_TIME_SIGNATURE

Obj = TypeVar("Obj")


class NoteGeneratorProtocol(Protocol):
    def __init__(self, strategy: SequencerStrategy | None= None): ...
    def __iter__(self): ...
    def __next__(self): ...
    def setup(self, part: Part, strategy: SequencerStrategy | None= None, **kwargs): ...
    # def get_generators(self): ...


class Buffer:  # (NoteGenerator):
    def __init__(self, generators: Sequence[BasePlayer], *args, **kwargs):
        super(Buffer, self).__init__(*args, **kwargs)

        self.generators: Sequence[BasePlayer] = generators or []

        self.cursor: Duration
        self.limit_cursor: Duration

    def get_generators(self): return self.generators
    def set_generators(self, generators): self.generators = generators

    def setup(self, part: Part, strategy: SequencerStrategy | None = None, **kwargs):
        self.part = part
        # if strategy:
        #     self.strategy = strategy
        # self.propagate_part(**kwargs)
        self.cursor = part.start_cursor
        # self.limit_cursor = self.part.end_cursor
        self.limit_cursor = self.part.intermediate_cursor

    def get_messages(self):
        messages = []
        g: BasePlayer
        for g in self.generators:
            for timeline, message in g.play(self.part):
                if timeline >= self.part.intermediate_cursor:
                    break
                messages.append([timeline, message])
        return messages


@dataclass
class Sequencer:
    continuous_duration_ratio = 2

    harmony_iterator: HarmonyItemSelector
    players: List[BasePlayer] = field(default_factory=list)

    continuous: bool = False
    preview: bool = False

    def __init__(
        self,
        midi_adapter: MidiAdapter,
        harmony_iterator: HarmonyItemSelector,
        players: List[BasePlayer],
        preview: bool,
        items_change: SignalInstance
    ):
        self.midi_adapter = midi_adapter
        self.harmony_iterator = harmony_iterator
        self.players = players
        self.preview = preview
        self.items_change = items_change

        self._cached_midi_outputs: Dict[str, Output] = {}

        self.reset()

    def set_players(self, players):
        self.players = players

    def set_harmony_iterator(self, harmony_iterator):
        self.harmony_iterator = harmony_iterator

    def get_midi_output(self, output_name):
        if output_name and output_name not in self._cached_midi_outputs:
            self._cached_midi_outputs[output_name] = self.midi_adapter.open_output(output_name)

        return self._cached_midi_outputs[output_name]

    def reset(self):
        self.global_cursor = Duration()
        self.previous_time_signature = None

        self.previous_harmony_end_time_section = TimeSection()
        self.previous_harmony_item = None

    def run(self):  # noqa: C901
        conductor = Conductor.build("MCL")
        splitter = Splitter(conductor=conductor)

        v = 0
        print("RUN")
        players = self.players

        if v:
            print(self.players)

        buffer = Buffer(generators=players)
        if v:
            print("(", players, ")")

        if v:
            print("RERUN")
        # print("RERUN")
        # print("RERUN")
        # print(self.params.harmony_iterator)
        message: Message
        last_cursor = Duration()

        # for sequencer_items, next_sequencer_items in self.params.harmony_iterator.run():

        print(f"{self.preview = }")
        print(f"{self.continuous = }")
        preview_iterator: cycle[Tuple[Tuple[HarmonyItem, ChordItem], Tuple[HarmonyItem, ChordItem]]]
        if self.preview or self.continuous:
            sequencer_items = self.harmony_iterator.current_items
            # next_sequencer_items = self.harmony_iterator.get_next_items()

            harmony_item, chord_item = sequencer_items

            harmony_item = replace(harmony_item)
            harmony_item.time_signature = TimeSignature.parse("4/4")
            harmony_item.chord_items = [chord_item]
            chord_item.duration_item = DurationItem(base_duration=Duration.parse("4"))

            preview_iterator = cycle([
                ((harmony_item, chord_item), (harmony_item, chord_item))
            ])

        i = 0
        # while 1:
        print(self.preview)
        for sequencer_items, next_sequencer_items in preview_iterator or self.harmony_iterator.run():
            harmony_item, chord_item = sequencer_items
            if not self.preview:
                self.items_change.emit(harmony_item, chord_item)

            # pprint(harmony_item)
            print("Sequencer = ", harmony_item.scale.to_log_string(), " - ", chord_item.root)

            sequencer_items = (harmony_item, chord_item)

            # harmony_item, chord_item = sequencer_items
            if v:
                print("=" * 55)
            if v:
                print("#", i)
            #  if self.params.on_harmony_item_change:
            #      self.params.on_harmony_item_change(harmony_item)

            # if self.params.on_chord_item_change:
            #     self.params.on_chord_item_change(harmony_item, chord_item)

            for part in splitter.run(sequencer_items, next_sequencer_items):
                if v:
                    print("-" * 33)

                # print("START", part.start_cursor)
                # print("INTER", part.intermediate_cursor)
                # print("END  ", part.end_cursor)
                # print("scale", part.scale)
                # print("chord", part.chord)

                if v:
                    pprint(part)
                # pprint(part)

                if v:
                    print()
                buffer.setup(part)

                events = defaultdict(list)
                messages = buffer.get_messages()
                for cursor, message in messages:
                    """
                    if not callable(message):
                        print(f"{str(cursor.value):6}, {str(message.note):4}, {str(message.duration.value)}")
                    """

                    if cursor >= part.end_cursor:
                        break

                    if isinstance(message, Message):
                        note_on, note_off = MidiMessage.get_tuple_from_message(
                            message=message,
                            output=self.get_midi_output(message.player.setting.output_name),
                        )

                        events[cursor].append(note_on)
                        events[cursor + message.duration].append(note_off)
                    elif callable(message):
                        events[cursor].append(message)

                end_cursor = part.end_cursor
                end_cursor = part.intermediate_cursor
                ratio = 1
                midi_messages: List[MidiMessage]
                """
                pprint(events)
                print("++++", last_cursor, end_cursor)
                """
                if v:
                    pprint(list(events.keys()))
                for cursor, midi_messages in sorted(events.items(), key=lambda x: x[0]):
                    if cursor > last_cursor:
                        if v:
                            print("SLEEP", last_cursor, cursor, float((cursor - last_cursor).value) * ratio * 60)  # / part.bpm.value)
                        sleep(float((cursor - last_cursor).value) * ratio * 60 / part.bpm.value)
                        # sleep_for_gap(last_cursor, cursor, bpm=part.bpm)
                    # print("out sleep")

                    for midi_message in midi_messages:
                        # print(message)
                        print("-", cursor, midi_message.origin.note, midi_message.type)

                        if callable(midi_message):
                            midi_message()

                            continue
                        else:
                            midi_message.fix_note_midi_index()

                        if (
                            not midi_message.output or
                            not midi_message.origin.player.setting.enabled or
                            not midi_message.note
                        ):
                            # print(
                            #     "ddddd",
                            #     bool(message.output),
                            #     message.origin.player.setting.enabled,
                            #     message.fix_note_midi_index(),
                            # )
                            # print("OUT", message.origin.player)
                            continue
                        # else:
                        elif midi_message.note:
                            if midi_message.type == "note_on":
                                # print("MSG", message.note)
                                self.midi_adapter.send_message(midi_message)
                            else:
                                if midi_message.opener:
                                    midi_message.note = midi_message.opener.note
                                if midi_message.note:
                                    self.midi_adapter.send_message(midi_message)
                            # print("======", datetime.now(), cursor, last_cursor, end_cursor)
                            # if message.type == "note_on":
                            #     print("MSG", message.note)

                    last_cursor = cursor

                # print("----", cursor, last_cursor, end_cursor)
                if last_cursor < end_cursor:
                    print("end sleep", part.start_cursor, end_cursor, last_cursor, float((end_cursor - last_cursor).value) * ratio * 60)  # / part.bpm.value)
                    # sleep(float((end_cursor - last_cursor).value) * ratio * 60 / part.bpm.value)
                print("end", part.start_cursor, part.intermediate_cursor, part.end_harmony_cursor)
                # sleep_for_gap(last_cursor, end_cursor, bpm=part.bpm)

            # if self.preview:
            #     i += 1
            #     if i > 20:
            #         break
            i += 1
            if self.preview:
                if i > 3:
                    break

        print("Sequencer::Run grid ended")
