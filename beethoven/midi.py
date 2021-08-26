from collections import defaultdict
from fractions import Fraction
from typing import Dict, Union

from mido import Message, MetaMessage, MidiFile, MidiTrack, open_output

from beethoven.core.settings import MIDI_OUTPUT_NAME, TEST
from beethoven.objects import Grid
from beethoven.player.base import Player
from beethoven.toolbox import get_base_time
from beethoven.utils.duration import NoLimit


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


midi = MidiRepository(
    virtual=TEST
)


def _get_messages(grid: Grid, players: Dict[int, Player]):
    timeline = Fraction()
    messages = defaultdict(list)

    for part_index, part in enumerate(grid):
        messages[timeline].append(('text', {"text": str(part_index)}))

        base_time = get_base_time(part.bpm)

        limit = (
            part.duration.value
            if part.duration
            else part.time_signature.as_duration.value
        ) * base_time

        for channel, player in players.items():
            player.setup(part)

            play_gen = player.play()

            while 1:
                notes, section, duration = next(play_gen)
                start = section.as_duration(part.time_signature).value * base_time

                if start >= limit:
                    break

                end = start + (duration.value * base_time)

                if end >= limit:
                    end = limit

                for note in notes:
                    messages[timeline + start].append(('note_on', {"note": note, "channel": channel}))
                    messages[timeline + end].append(('note_off', {"note": note, "channel": channel}))

        timeline += limit

    messages[timeline].append(('end_of_track', {}))

    return messages


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
                msg = MetaMessage(
                    instruction,
                    time=time,
                    **event_kwargs
                )
            else:
                msg = Message(
                    instruction,
                    time=time,
                    **event_kwargs
                )

            track.append(msg)

    return midi_file


def get_midi_file(grid: Grid, players: Dict[int, Player]):
    messages = _get_messages(grid, players)
    return _generate_midi_file(messages)


def play_midi_file(midi_file, repeat: Union[int, NoLimit] = 1):
    def _play(midi_file):
        for msg in midi_file.play(meta_messages=True):
            if msg.type == "text":
                yield int(msg.text)
                continue

            midi.send_msg(msg)

    if repeat is NoLimit:
        while 1:
            yield from _play(midi_file)

    elif repeat > 0:
        for _ in range(repeat):
            yield from _play(midi_file)

    return
