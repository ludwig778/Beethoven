from beethoven.sequencer.note_duration import Whole
from beethoven.sequencer.tempo import default_tempo_factory
from beethoven.sequencer.time_signature import default_time_signature_factory


class Grid:
    def __init__(self, parts=None, **kwargs):
        self.parts = []
        self.set_grid_config(**kwargs)
        self.set_parts(parts)

    def set_grid_config(self, time_signature=None, tempo=None, **kwargs):
        self.default_time_signature = time_signature or default_time_signature_factory()
        self.default_tempo = tempo or default_tempo_factory()

    def _generate_midi_file(self, timeline):
        pass

    def set_parts(self, parts):
        self.parts = []
        scale = chord = None

        for part in parts or []:
            if data := part.get("scale"):
                scale = data
            if data := part.get("chord"):
                chord = data

            part = GridPart(
                scale=scale,
                chord=chord,
                duration=part.get("duration", Whole),
                time_signature=part.get("time_signature", self.default_time_signature),
                tempo=part.get("tempo", self.default_tempo)
            )
            self.parts.append(part)


class GridPart:
    def __init__(self, scale=None, chord=None, duration=None, time_signature=None, tempo=None):
        self.scale = scale
        self.chord = chord
        self.duration = duration
        self.time_signature = time_signature
        self.tempo = tempo

    def __repr__(self):
        return f"<Grid Part : {self.scale}/{self.chord}/{self.duration}/{self.time_signature}/{self.tempo}>"
