from beethoven.theory.interval import AUGMENTED, DIMINISHED
from beethoven.utils.regex import HARMONY_PARSER

from .chord import Chord
from .scale import Scale

DEFAULT_DEGREES = "1,3,5,7"


class HarmonySingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, scale):
        if scale not in cls._INSTANCES:
            instance = super().__call__(scale)
            cls._INSTANCES[scale] = instance
        return cls._INSTANCES[scale]


class Harmony(metaclass=HarmonySingletonMeta):
    _DIRECTORY = {}
    _MAJOR_INTERVALS = {
        i: interval
        for i, interval in enumerate(Scale("A", "major").intervals, start=1)
    }
    _MAJOR_DEGREES = ("I", "II", "III", "IV", "V", "VI", "VII")

    def __init__(self, scale):
        self._load_attributes(scale)

    def __repr__(self):
        return f"<Harmony {self.scale.name}>"

    def _load_attributes(self, scale):
        scale_intervals = scale.intervals

        if not len(scale_intervals) == 7:
            raise ValueError("Scale given to harmony must be diatonic")

        self.scale = scale
        self.degrees = []

        for interval, major_interval, degree in zip(scale_intervals, self._MAJOR_INTERVALS.values(), self._MAJOR_DEGREES):
            diff_alteration = interval.alteration + major_interval.alteration

            if diff_alteration == -1:
                degree = degree.lower()
            elif diff_alteration > 0:
                degree += "a" * diff_alteration
            elif diff_alteration < -1:
                degree += "d" * abs(diff_alteration + 1)

            self.degrees.append(degree)

    def get(self, degree):
        parsed = HARMONY_PARSER.match(degree).groupdict()
        final_alteration = 0

        degree_name = parsed.get("degree_name")
        alteration = parsed.get("alteration")
        chord_name = parsed.get("chord_name")

        if not degree_name:
            raise ValueError("Degree could not be parsed")

        if (degree_name + alteration) in self.degrees:
            index = self.degrees.index(degree_name + alteration)

            note = self.scale.notes[index]
        elif degree_name.isupper():
            index = self._MAJOR_DEGREES.index(degree_name)

            note = self.scale.notes[index]
            if not chord_name:
                if "7" in DEFAULT_DEGREES:
                    chord_name = "maj7"
                else:
                    chord_name = "maj"
        else:
            index = self._MAJOR_DEGREES.index(degree_name.upper())

            note = self.scale.notes[index]
            note += DIMINISHED

            final_alteration -= 1
            if not chord_name:
                if "7" in DEFAULT_DEGREES:
                    chord_name = "min7"
                else:
                    chord_name = "min"

        flats = alteration.count("b")
        sharps = alteration.count("#")
        if flats:
            final_alteration -= flats
            for _ in range(flats):
                note += DIMINISHED
        elif sharps:
            final_alteration += sharps
            for _ in range(sharps):
                note += AUGMENTED

        if chord_name:
            chord = Chord(note, chord_name)
        else:
            chord = self.scale.get_chord(index, DEFAULT_DEGREES, alteration=final_alteration)

        return chord
