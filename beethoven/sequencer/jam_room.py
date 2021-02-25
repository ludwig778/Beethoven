from collections import defaultdict

from beethoven.repository.midi import midi
from beethoven.sequencer.players.base import Players


class JamRoom:
    def __init__(self, grid=None, players=None, **kwargs):
        self.grid = grid
        self.players = Players(*(players or []))

        self.timeline = {}
        self.length = 0.0

        self.setup()

    def setup(self):
        self.timeline, self.length = self._get_timeline(self.grid, self.players)

    @staticmethod
    def _get_timeline(grid, players):  # noqa: C901
        global_time = 0.0

        last_time_signature = None
        last_time_ts_updated = 0.0

        timeline = defaultdict(list)

        for grid_part in grid.parts:
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
                multi_signature_offset_num = (global_time - last_time_ts_updated) // time_signature_duration
                limit_time = (
                    last_time_ts_updated +
                    time_signature_duration * (multi_signature_offset_num + 1)
                )

            for channel, player in players.items():
                player.prepare(**grid_part.__dict__)

                for note in player.play_measure():
                    part = note.pop("part")

                    note["channel"] = channel

                    offset_time = part.start_offset(time_signature, tempo)
                    part_time = global_time + offset_time

                    note_duration = note["duration"].duration(tempo)
                    if duration:
                        grid_part_duration = duration.duration(tempo)

                        if note_duration > grid_part_duration:
                            note_duration = grid_part_duration

                    if part_time + note_duration > limit_time:
                        note_duration = limit_time - part_time

                    note["duration"] = note_duration

                    if part_time < limit_time:
                        timeline[part_time].append(note)

            global_time = limit_time

            last_time_signature = time_signature

        return timeline, global_time

    def play(self, **kwargs):
        return midi.play(self.timeline, self.length, **kwargs)
