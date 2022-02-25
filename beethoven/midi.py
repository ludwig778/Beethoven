from dataclasses import dataclass, field
from fractions import Fraction
from typing import Any, Dict, Union

from mido import Message, MetaMessage, MidiFile, MidiTrack, open_output

from beethoven.objects import Duration, Grid
from beethoven.player.base import Player
from beethoven.settings import MIDI_OUTPUT_NAME, TEST
from beethoven.utils.duration import DurationLimit


class MidiRepository:
    def __init__(self, virtual=False):
        self.virtual = virtual
        self.output = None

        if not virtual:
            self.output = open_output(MIDI_OUTPUT_NAME, virtual=True)

    def send_msg(self, msg):
        if self.virtual:
            return

        self.output.send(msg)

    def shutdown(self):
        if self.virtual:
            return

        self.output.panic()


midi = MidiRepository(virtual=TEST)


@dataclass
class Messages:
    values: Dict[Fraction, Any] = field(default_factory=dict)

    def add(self, time, values):
        if not self.values.get(time):
            self.values[time] = []

        self.values[time].append(values)


def _get_messages(grid: Grid, players: Dict[int, Player]):
    timeline = Duration(0)
    messages = Messages()

    for part_index, part in enumerate(grid):
        messages.add(timeline, ("text", {"text": str(part_index)}))

        base_time = part.bpm.base_time

        limit = part.duration * base_time

        for channel, player in players.items():
            player.setup(part)

            play_gen = player.play()

            while 1:
                notes, section, duration = next(play_gen)
                start = section.as_duration(part.time_signature) * base_time

                if start >= limit:
                    break

                end = start + (duration * base_time)

                if end >= limit:
                    end = limit

                for note in notes:
                    messages.add(
                        timeline + start,
                        ("note_on", {"note": note, "channel": channel}),
                    )
                    messages.add(
                        timeline + end, ("note_off", {"note": note, "channel": channel})
                    )

        timeline += limit

    messages.add(timeline, ("end_of_track", {}))

    return messages.values


def _generate_midi_file(messages):
    midi_file = MidiFile(type=1)
    track = MidiTrack()
    midi_file.tracks.append(track)

    sorted_timestamps = sorted(messages.keys())
    for start_time, events in sorted(messages.items(), key=lambda x: x[0]):
        for i, event in enumerate(events, start=1):
            instruction, event_kwargs = event

            current_time_index = sorted_timestamps.index(start_time)
            time = 0

            if i == 1:
                previous_time = sorted_timestamps[current_time_index - 1]
                if len(sorted_timestamps) == 1:
                    time = previous_time * 1000
                if current_time_index != 0:
                    time = (start_time - previous_time) * 1000

                # Approximative fix to mido time offset
                time *= Fraction(95864, 100000)

            if instruction not in ("note_on", "note_off"):
                msg = MetaMessage(instruction, time=time, **event_kwargs)
            else:
                msg = Message(instruction, time=time, **event_kwargs)

            track.append(msg)

    return midi_file


def get_midi_file(grid: Grid, players: Dict[int, Player]):
    messages = _get_messages(grid, players)
    return _generate_midi_file(messages)


def play_midi_file(midi_file, repeat: Union[int, DurationLimit] = 1):
    def _play(midi_file):
        for msg in midi_file.play(meta_messages=True):
            if msg.type == "text":
                yield int(msg.text)
                continue

            midi.send_msg(msg)

    if repeat is DurationLimit.NoLimit:
        while 1:
            yield from _play(midi_file)

    elif isinstance(repeat, int) and repeat > 0:
        for _ in range(repeat):
            yield from _play(midi_file)

    return
