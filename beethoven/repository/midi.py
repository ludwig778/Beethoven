from collections import defaultdict
from os import environ

import mido


class MidiRepository:
    DEFAULT_OUTPUT_NAME = "DEFAULT_OUTPUT"

    def __init__(self, output_name=None, virtual=False):
        self.output = None
        self.virtual = virtual

        if not virtual:
            self.output = mido.open_output(output_name or self.DEFAULT_OUTPUT_NAME, virtual=True)

    def play(self, grid, players, repeat=None):
        midi_file = self._generate_midi_file(grid, players)

        yield from self._play_midi_file(midi_file, repeat=repeat)

    @staticmethod
    def _get_messages(grid, players):  # noqa: C901
        global_time = 0.0

        last_time_signature = None
        last_time_ts_updated = 0.0

        messages = defaultdict(list)

        for grid_part_index, grid_part in enumerate(grid.parts, start=1):
            print("GRID", grid_part_index)
            messages[global_time].append(('text', {"text": str(grid_part_index)}))

            tempo = grid_part.tempo
            time_signature = grid_part.time_signature
            duration = grid_part.duration

            if last_time_signature is None:
                last_time_signature = time_signature

            if last_time_signature != time_signature:
                last_time_ts_updated = global_time

            if duration:
                limit_time = global_time + duration.duration(tempo)
            else:
                time_signature_duration = time_signature.duration(tempo)
                multi_signature_offset_num = (global_time - last_time_ts_updated + .0001) // time_signature_duration
                limit_time = (
                    last_time_ts_updated +
                    time_signature_duration * (multi_signature_offset_num + 1)
                )

            for channel, player in players.items():
                player.prepare(**grid_part.__dict__)

                for notes_attrs in player.play_measure() or []:
                    part = notes_attrs["part"]
                    velocity = notes_attrs["velocity"]
                    note_duration = notes_attrs["duration"].duration(tempo)

                    offset_time = part.start_offset(time_signature, tempo)
                    part_time = global_time + offset_time

                    if duration:
                        grid_part_duration = duration.duration(tempo)

                        if note_duration > grid_part_duration:
                            note_duration = grid_part_duration

                    if part_time + note_duration > limit_time:
                        note_duration = limit_time - part_time

                    if part_time >= limit_time:
                        continue

                    for note in notes_attrs.get("notes"):
                        messages[part_time].append(('note_on', {
                            'note': note.index,
                            'velocity': velocity,
                            'channel': channel
                        }))
                        messages[part_time + note_duration].append(('note_off', {
                            'note': note.index,
                            'velocity': 127,
                            'channel': channel
                        }))

            global_time = limit_time

            last_time_signature = time_signature

        messages[global_time].append(('end_of_track', {}))

        return messages

    def _generate_midi_file(self, grid, players):
        messages = self._get_messages(grid, players)

        midi_file = mido.MidiFile(type=1)
        track = mido.MidiTrack()
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

                if instruction not in ("note_on", "note_off"):
                    msg = mido.MetaMessage(
                        instruction,
                        time=time,
                        **event_kwargs
                    )
                else:
                    msg = mido.Message(
                        instruction,
                        time=time,
                        **event_kwargs
                    )

                track.append(msg)

        return midi_file

    def _send_msg(self, msg):
        if self.virtual:
            return

        self.output.send(msg)

    def _shutdown(self):
        if self.virtual:
            return

        self.output.panic()

    def _play_midi_file(self, midi_file, repeat=None, go_on=False):
        def _play(midi_file):
            for msg in midi_file.play(meta_messages=True):
                if msg.type == "text":
                    yield int(msg.text)
                    continue

                self._send_msg(msg)

        try:
            if go_on:
                while 1:
                    yield from _play(midi_file)
            elif repeat and repeat > 1:
                for _ in range(repeat):
                    yield from _play(midi_file)
            else:
                yield from _play(midi_file)

        except KeyboardInterrupt:
            self._shutdown()

        return


midi = MidiRepository(
    virtual=environ.get("TEST", "").lower() in ("true", "1")
)
