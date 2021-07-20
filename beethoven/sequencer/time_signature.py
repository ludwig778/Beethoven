from dataclasses import dataclass
from typing import Generator

from beethoven.sequencer.note_duration import Quarter
from beethoven.sequencer.tempo import Tempo


@dataclass(eq=True)
class TimeContainer:
    bar: int
    measure: int
    submeasure: int
    divisor_index: int = 1
    divisor: int = 1

    def check(self, **kwargs) -> bool:
        """Simple cumlutalive check on kwargs values against object values."""
        checks = []
        for k, v in kwargs.items():
            self_value = getattr(self, k)
            if isinstance(v, int):
                checks.append(self_value == v)
            else:
                checks.append(self_value in v)

        return all(checks)

    def __lt__(self, other):
        if self.bar < other.bar:
            return True
        elif self.bar > other.bar:
            return False

        if self.measure < other.measure:
            return True
        elif self.measure > other.measure:
            return False

        if self.submeasure < other.submeasure:
            return True
        elif self.submeasure > other.submeasure:
            return False

        return (
            self.divisor_index / self.divisor <
            other.divisor_index / other.divisor
        )

    def __le__(self, other):
        return self.__class__ == other.__class__ and (
            self == other or self < other
        )


@dataclass
class TimeSignature:
    beat_unit: int = 4
    beats_per_bar: int = 4

    def duration(self, tempo: Tempo) -> float:
        """Compute the time span of the time signature regarding of the tempo."""
        reduction = self.beats_per_bar / 4

        quarter = Quarter.duration(bpm=tempo)

        return (self.beat_unit * quarter) / reduction

    def _get_time_container(
        self, count: int, divisor: int, beats_per_bar: int = None, beat_unit: int = None
    ) -> TimeContainer:
        """Compute a time container from a count variable according to time signature attributes."""

        raw_submeasure, divisor_index = divmod(count, divisor)
        raw_measure, submeasure = divmod(raw_submeasure, beats_per_bar or self.beats_per_bar)
        bar, measure = divmod(raw_measure, beat_unit or self.beat_unit)

        return TimeContainer(
            bar + 1,
            measure + 1,
            submeasure + 1,
            divisor_index + 1,
            divisor
        )

    def normalize_part(self, part: TimeContainer) -> TimeContainer:
        """Normalize a part to its relative x/4 time signature."""
        ratio = self.beats_per_bar / 4
        divisor = part.divisor

        raw_measure = ((part.bar - 1) * self.beat_unit) + (part.measure - 1)
        raw_submeasure = (raw_measure * self.beats_per_bar) + (part.submeasure - 1)
        count = ((part.divisor * raw_submeasure) - 1) + (part.divisor_index)

        while True:
            if divisor % 2:
                break

            divisor = int(divisor / 2)
            count = count / 2

        count = int(count / (ratio ** 2))

        return self._get_time_container(
            count,
            divisor,
            beats_per_bar=4,
            beat_unit=int(self.beat_unit / ratio)
        )

    # TODO: Clear up arguments
    def generator(self, note_duration, duration=None, go_on=False) -> Generator[TimeContainer, None, None]:
        reduction = self.beats_per_bar / 4

        divisor = note_duration.divisor
        reduc_ratio = self.beats_per_bar * reduction

        while not (divisor % 2 or reduc_ratio % 2):
            divisor //= 2
            reduc_ratio //= 2

        base_units = int(note_duration.base_units * reduc_ratio)

        # Get total duration
        if duration:
            last_section = self._get_time_container(
                int(duration.base_units * self.beats_per_bar * reduction * divisor / duration.divisor),
                divisor
            )
        elif go_on:
            last_section = None
        else:
            last_section = self._get_time_container(
                self.beat_unit * self.beats_per_bar * divisor,
                divisor
            )

        count = 0
        while 1:
            time_section = self._get_time_container(count, divisor)

            if last_section is not None and last_section <= time_section:
                return

            yield time_section

            count += base_units


def get_part_timestamp(time_signature: TimeSignature, tempo: Tempo, part: TimeContainer) -> float:
    """Compute part timestamp regarding of a given time signature and tempo."""
    reduction = time_signature.beats_per_bar / 4

    quarter = Quarter.duration(bpm=tempo) / reduction

    beats_per_bar = time_signature.beats_per_bar
    beat_unit = time_signature.beat_unit

    bar_part = (part.bar - 1) * beat_unit
    measure_part = part.measure - 1
    submeasure_part = (part.submeasure - 1) / beats_per_bar
    divisor_part = (1 / beats_per_bar) * ((part.divisor_index - 1) / part.divisor)

    return (bar_part + measure_part + submeasure_part + divisor_part) * quarter
