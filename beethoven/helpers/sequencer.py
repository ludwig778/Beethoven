import logging
from logging import Logger
from typing import Any, Dict, Generator, Tuple

from beethoven.models import (Chord, ChordItem,  # Scale,; TimeSignature,
                              Duration, HarmonyItem, Note, TimeSection)
# from beethoven.sequencer.players import BasePlayer
from beethoven.ui.exceptions import PlayerStopPlaying  # , SystemPlayer

# from beethoven.ui.exceptions import PlayerStopPlaying

NoteGenerator = Generator[Tuple[str, Any], None, None]
NoteGenerators = Dict[Any, NoteGenerator]


def one_time_play(timeline, messages):
    for message in messages:
        yield timeline, message

    return StopIteration()


def note_repeater(cycle: Duration, messages, offset: Duration | None = None):
    timeline = offset or Duration()

    while 1:
        for message in messages:
            yield timeline, message

        timeline += cycle


def note_sequencer(step: Duration, messages, round_robin: str):
    timeline = Duration()
    i = 0

    while 1:
        if round_robin[i % len(round_robin)] == "+":
            for message in messages:
                yield timeline, message

        timeline += step
        i += 1


def sort_generator_outputs(generators: NoteGenerators) -> NoteGenerator:
    values: Dict[str, Any] = {}

    for name, generator in generators.items():
        try:
            values[name] = next(generator)
        except StopIteration:
            pass

    while values:
        key, item = sorted(values.items(), key=lambda x: x[1][0])[0]

        yield item

        try:
            values[key] = next(generators[key])
        except StopIteration:
            del values[key]


class BaseSorter:
    def __init__(self, generators: NoteGenerators | None = None, refeed_enabled: bool = False):
        self.generators = generators or {}

        self.refeed_enabled = refeed_enabled

        self.start_cursor: Duration
        self.end_cursor: Duration
        self.values: Dict[str, Any] = {}

    def clear(self):
        self.values = {}

    def refeed(self, key, item):
        self.values[key + "_refeed"] = item

    def __iter__(self):
        return self

    def __next__(self):
        if not self.values:
            raise StopIteration()

        key, [cursor, data] = sorted(self.values.items(), key=lambda x: x[1][0])[0]

        try:
            self.values[key] = next(self.generators[key])
        except (StopIteration, KeyError, PlayerStopPlaying):
            del self.values[key]

        if self.refeed_enabled and cursor >= self.end_cursor:
            self.refeed(key, [cursor, data])

            raise StopIteration()

        return (cursor, data)


class NoteSorter(BaseSorter):
    def __init__(self, **generators):
        super(NoteSorter, self).__init__()  # **kwargs)

        self.values: Dict[str, Any] = {}

        self.generators = generators
        for name, generator in self.generators.items():
            # print("#######", name, generator)
            try:
                self.values[name] = next(generator)
            except StopIteration:
                pass


"""


class SequencerSorter(BaseSorter):
    def __init__(self, players: List[BasePlayer]):
        super(SequencerSorter, self).__init__(refeed_enabled=True)

        self.players = players
        self.values: Dict[str, Any] = {}

    def setup(
        self,
        scale: Scale,
        chord: Chord,
        time_signature: TimeSignature,
        start_cursor: Duration,
        end_cursor: Duration,
        start_time_section: TimeSection,
    ):
        self.start_cursor = start_cursor
        self.end_cursor = end_cursor

        self.generators = {}

        for player in self.players:
            player_name = player.__class__.__name__

            time_signature_changed = getattr(player, "time_signature", None) != time_signature
            player.setup(
                scale,
                chord,
                time_signature,
                start_cursor,
                end_cursor,
                start_time_section,
            )
            generator = player.play_wrapper()

            if isinstance(player, SystemPlayer) and time_signature_changed:
                for gen_name in list(self.values.keys()):
                    if player_name in gen_name:
                        del self.values[gen_name]

            self.generators[player_name] = generator

            if player_name not in self.values:
                self.values[player_name] = next(generator)
"""


def get_chord_from_items(
    harmony_item: HarmonyItem, chord_item: ChordItem
) -> Tuple[Chord, Duration | None]:
    chord_data: Dict = {"root" if isinstance(chord_item.root, Note) else "degree": chord_item.root}

    return (
        Chord.build(name=chord_item.name, scale=harmony_item.scale, **chord_data),
        chord_item.duration_item.value,
    )
