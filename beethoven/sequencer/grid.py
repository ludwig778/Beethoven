

class Grid:

    def __init__(self, parts=None):
        self.set_parts(parts or [])

    def set_parts(self, parts):
        self.parts = parts

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if len(self.parts) != len(other.parts):
            return False

        for s, o in zip(self.parts, other.parts):
            if s != o:
                return False

        return True

    def __str__(self):
        return f"<Grid : {len(self.parts)} parts>"


class GridPart:

    def __init__(self, scale=None, chord=None, duration=None, time_signature=None, tempo=None, repeat=1, bypass=False):
        self.scale = scale
        self.chord = chord
        self.duration = duration
        self.time_signature = time_signature
        self.tempo = tempo

        self.repeat = repeat
        self.bypass = bypass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def to_dict(self):
        return self.__dict__

    def __repr__(self):
        string = "<GridPart : "
        string += f"{self.scale} / {self.chord} / {self.duration} / {self.time_signature} / {self.tempo.bpm}bpm"
        string += f" / {self.repeat}x" if self.repeat > 1 else ""
        string += " / bypassed" if self.bypass else ""
        string += ">"

        return string
