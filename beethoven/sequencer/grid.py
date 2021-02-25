from copy import copy

from beethoven.prompt.parser import prompt_harmony_list_parser
from beethoven.sequencer.note_duration import Whole
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature


class Grid:
    DEFAULT_TIME_SIGNATURE = TimeSignature(4, 4)
    DEFAULT_TEMPO = Tempo(60)
    DEFAULT_DURATION = Whole

    def __init__(self, time_signature=None, tempo=None, duration=None, parts=None, **kwargs):
        self.default_time_signature = time_signature or self.DEFAULT_TIME_SIGNATURE
        self.default_tempo = tempo or self.DEFAULT_TEMPO
        self.default_duration = duration or self.DEFAULT_DURATION

        self.parts = []
        if parts:
            self.set_parts(*parts)

    def set_parts(self, *parts):
        self.parts = []

        last_part = None
        for part in parts:
            if last_part:
                last_part = copy(last_part.to_dict())
                last_part.pop("duration", None)

                part = {**last_part, **part}

            part.setdefault("time_signature", self.default_time_signature)
            part.setdefault("tempo", self.default_tempo)

            grid_part = GridPart(**part)
            self.parts.append(grid_part)

            last_part = grid_part

    @classmethod
    def parse(cls, string, **kwargs):
        return cls(parts=prompt_harmony_list_parser(string), **kwargs)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"<Grid : {len(self.parts)} parts>"


class GridPart:

    def __init__(self, scale=None, chord=None, duration=None, time_signature=None, tempo=None):
        self.scale = scale
        self.chord = chord
        self.duration = duration
        self.time_signature = time_signature
        self.tempo = tempo

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        return (
            f"<GridPart : "
            f"{self.scale} / {self.chord} / {self.duration} / {self.time_signature} / {self.tempo}>"
        )
