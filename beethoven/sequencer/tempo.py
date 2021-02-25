class Tempo:
    DEFAULT_BPM = 120

    def __init__(self, bpm=None):
        self.set(bpm or self.DEFAULT_BPM)

    def set(self, bpm):
        self.value = bpm

    def base_time_unit(self):
        return 60 / self.value

    def __repr__(self):
        return f"<Tempo : {str(self)} bpm>"

    def __str__(self):
        return f"{self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self == other or self < other
