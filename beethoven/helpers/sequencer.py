from typing import Any, Dict, Generator, List, Tuple

from beethoven.helpers.midi import get_on_off_messages

# from beethoven.sequencer.players.base import BasePlayer, PercussionPlayer
from beethoven.types import Player

NoteGenerator = Generator[Tuple[str, Any], None, None]
NoteGenerators = Dict[Any, NoteGenerator]


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


def split_player_by_types(players: List[Player]) -> Tuple[List[Player], List[Player]]:
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
