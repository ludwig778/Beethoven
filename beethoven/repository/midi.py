from collections import defaultdict

import mido


class MidiRepository:
    DEFAULT_OUTPUT_NAME = "DEFAULT_OUTPUT"

    def __init__(self, output_name=None, virtual=False):
        self.output = None
        self.virtual = virtual

        if not virtual:
            self.output = mido.open_output(output_name or self.DEFAULT_OUTPUT_NAME, virtual=True)

    def play(self, timeline, length, repeat=None):
        messages = self._get_messages(timeline, length)
        midi_file = self._generate_midi_file(messages)

        return self._play_midi_file(midi_file, repeat=repeat)

    def _get_messages(self, timeline, global_time):
        messages = defaultdict(list)

        for start_time, players_notes in sorted(timeline.items(), key=lambda x: x[0]):
            for player_notes in players_notes:
                velocity = player_notes['velocity']
                channel = player_notes['channel']
                duration = player_notes['duration']

                for note in player_notes['notes']:

                    messages[start_time].append([
                        'note_on', note.index, velocity, channel
                    ])
                    messages[start_time + duration].append([
                        'note_off', note.index, 127, channel
                    ])

        messages[global_time].append(['end_of_track', 0, 0, 0])

        return messages

    def _generate_midi_file(self, messages):
        midi_file = mido.MidiFile(type=1)
        track = mido.MidiTrack()
        midi_file.tracks.append(track)

        sorted_timestamps = sorted(messages.keys())
        for start_time, events in sorted(messages.items(), key=lambda x: x[0]):

            for i, event in enumerate(events, start=1):
                instruction = event[0]
                note = event[1]
                velocity = event[2]
                channel = event[3]

                current_time_index = sorted_timestamps.index(start_time)
                if i == 1 and current_time_index != 0:
                    previous_time = sorted_timestamps[current_time_index - 1]
                    time = (start_time - previous_time) * 1000
                else:
                    time = 0

                if instruction == "end_of_track":
                    msg = mido.MetaMessage(
                        instruction,
                        time=time
                    )
                else:
                    msg = mido.Message(
                        instruction,
                        note=note,
                        velocity=velocity,
                        channel=channel,
                        time=time
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

    def _play_midi_file(self, midi_file, repeat=None):
        try:
            if repeat and repeat > 1:
                for _ in range(repeat):
                    for msg in midi_file.play():
                        self._send_msg(msg)
            else:
                for msg in midi_file.play():
                    self._send_msg(msg)
        except KeyboardInterrupt:
            self._shutdown()


midi = MidiRepository(virtual=True)
