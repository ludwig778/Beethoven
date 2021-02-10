class NoteDuration:
    def __init__(self, name, base_units, divisor=1):
        self.name = name
        self.base_units = base_units
        self.divisor = divisor

    def duration(self, bpm):
        return (
            (self.base_units / self.divisor) *
            bpm.base_time_unit()
        )

    def __mul__(self, multiplier):
        obj = self.copy()
        obj.base_units *= multiplier

        return obj

    def __repr__(self):
        return f"<Note Duration : {self.name}>"

    def __eq__(self, other):
        return self.base_units / self.divisor == other.base_units / other.divisor

    def copy(self):
        return self.__class__(self.name, self.base_units, self.divisor)


class NoteDurationTuple:
    def __init__(self, name, divisor):
        self.name = name
        self.divisor = divisor

    def __call__(self, note_duration):
        obj = note_duration.copy()

        obj.name += " " + self.name
        obj.divisor *= self.divisor

        return obj


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
