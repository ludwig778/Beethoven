from abc import ABC, abstractmethod

from beethoven.objects import Duration, GridPart
from beethoven.toolbox import time_section_generator
from beethoven.utils.duration import NoLimit


class Player(ABC):
    def __init__(self):
        self.default_duration = Duration.parse("Q")

    def setup(self, grid_part: GridPart):
        self._skip = 0

        self.scale = grid_part.scale
        self.chord = grid_part.chord
        self.duration = grid_part.duration or self.default_duration
        self.time_signature = grid_part.time_signature

    def skip(self, step):
        assert isinstance(step, int), "Step must be an integer"
        assert step > 0, "Step must be a positive integer"

        self._skip = step

    def check(self):
        if self._skip:
            self._skip -= 1
            return True

        return False

    def play(self):
        for section, duration in time_section_generator(
            self.time_signature,
            self.duration,
            limit=NoLimit,
        ):
            if self.check():
                continue

            yield from self.get_notes(section, duration)

    @abstractmethod
    def get_notes(self, section, duration):
        pass
