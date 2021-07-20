from dataclasses import dataclass, replace

from beethoven.sequencer.tempo import Tempo


@dataclass
class NoteDuration:
    name: str
    base_units: int
    divisor: int = 1

    def duration(self, bpm: Tempo) -> float:
        """Compute the duration with its attributes against a given tempo."""
        return (
            (self.base_units / self.divisor) *
            bpm.base_time_unit()
        )

    def __mul__(self, multiplier: int):
        obj = replace(self)
        obj.base_units *= multiplier

        return obj

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, self.__class__) and
            self.base_units / self.divisor == other.base_units / other.divisor
        )


@dataclass
class NoteDurationTuple:
    name: str
    divisor: int

    def __call__(self, note_duration: NoteDuration) -> NoteDuration:
        """Apply the instance attributes to a given NoteDuration to get a fraction of it."""
        return replace(
            note_duration,
            name=f"{note_duration.name} {self.name}",
            divisor=note_duration.divisor * self.divisor
        )


OneShot = NoteDuration("OneShot", 0)

Whole = NoteDuration("Whole", 4)
Half = NoteDuration("Half", 2)
Quarter = NoteDuration("Quarter", 1)
Eighths = NoteDuration("Eighths", 1, 2)
Sixteenths = NoteDuration("Sixteenths", 1, 4)

Triplet = NoteDurationTuple("Triplet", 3)
Quintuplet = NoteDurationTuple("Quintuplet", 5)
Septuplet = NoteDurationTuple("Septuplet", 7)
Octuplet = NoteDurationTuple("Octuplet", 8)
Nontuplet = NoteDurationTuple("Nontuplet", 9)
Decuplet = NoteDurationTuple("Decuplet", 10)
Undecuplet = NoteDurationTuple("Undecuplet", 11)
Dodecuplet = NoteDurationTuple("Dodecuplet", 12)
Tredecuplet = NoteDurationTuple("Tredecuplet", 13)
