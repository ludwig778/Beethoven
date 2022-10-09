from typing import Any, Dict, Generator, List, Optional, Tuple

from beethoven.helpers.midi import get_on_off_messages
from beethoven.models.duration import Duration
from beethoven.sequencer.players.base import BasePlayer

NoteGenerator = Generator[Tuple[str, Any], None, None]
NoteGenerators = Dict[Any, NoteGenerator]


def note_repeater(cycle: Duration, messages, offset: Optional[Duration] = None):
    timeline = offset or Duration(value=0)

    while 1:
        for message in messages:
            yield timeline, message

        timeline += cycle


def note_sequencer(step: Duration, messages, round_robin: str):
    timeline = Duration(value=0)
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


def split_player_by_types(players: List[BasePlayer]) -> Tuple[List[BasePlayer], List[BasePlayer]]:
    regular = []
    time_signature_bound = []

    for player in players:
        if player.time_signature_bound:
            time_signature_bound.append(player)
        else:
            regular.append(player)

    return regular, time_signature_bound


def update_timeline_for_player(timeline_events, player, limit, offset) -> None:
    for note_timeline, note_data in player.play():
        duration = note_data.pop("duration")

        note_on, note_off = get_on_off_messages(
            note_index=note_data["note"],
            output=player.output,
            channel=player.channel,
            velocity=note_data["velocity"],
        )

        if note_timeline >= limit:
            break

        timeline_events[note_timeline + offset].append(note_on)

        note_timeline += duration

        if note_timeline > limit:
            remove = note_timeline - limit

            note_timeline -= remove

        timeline_events[note_timeline + offset].append(note_off)
