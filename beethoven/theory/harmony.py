from beethoven.theory.chord import Chord
from beethoven.theory.interval import AUGMENTED, DIMINISHED
from beethoven.theory.scale import Scale
from beethoven.utils.regex import HARMONY_PARSER


class HarmonySingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, scale=None):
        if scale is None:
            raise ValueError("Scale must be set")

        elif scale not in cls._INSTANCES:
            instance = super().__call__(scale)
            cls._INSTANCES[scale] = instance

        return cls._INSTANCES[scale]


class Harmony(metaclass=HarmonySingletonMeta):
    _DIRECTORY = {}
    _MAJOR_INTERVALS = {
        i: interval
        for i, interval in enumerate(Scale("A", "major").intervals, start=1)
    }
    _DEGREES = ("I", "II", "III", "IV", "V", "VI", "VII")
    _DEFAULT_DEGREES = "1,3,5,7"

    def __init__(self, scale):
        self._load_attributes(scale)

    def __repr__(self):
        return f"<Harmony {str(self)}>"

    def __str__(self):
        return str(self.scale)

    def _load_attributes(self, scale):
        if not len(scale.intervals) == 7:
            raise ValueError("Scale given to harmony must be diatonic")

        self.scale = scale
        self.degrees = []

        default_degrees = [1, 3, 5, 7]
        scale_notes = self.scale.notes

        for i, degree_name in enumerate(self._DEGREES):
            # TODO refactor with intervals for scale object instead of notes
            notes = list(map(lambda x: scale_notes[(x + i - 1) % 7], default_degrees))

            intervals = [
                notes[0] // note
                for note in notes
            ]

            chord_name = Chord.get_chord_name_from_intervals(intervals).short

            if "min" in chord_name or "dim" in chord_name:
                degree_name = degree_name.lower()

            self.degrees.append(degree_name)

    def get(self, *args, **kwargs):
        try:
            return self._get(*args, **kwargs)
        except ValueError:
            return

    def get_base_degree_interval(self, degree):
        note = self._parse_degree(degree)[0]

        return self.scale.notes[0] // note

    def _get(self, degree, inversion=None, base_note=None, base_degree=None, default_degrees=None, seventh=True, extensions=None):
        if not default_degrees:
            default_degrees = self._DEFAULT_DEGREES

        base_degree_interval = None
        note, alteration, index, chord_name = self._parse_degree(degree, seventh=seventh)

        if base_degree:
            base_degree_interval = self.get_base_degree_interval(base_degree)
            note += base_degree_interval

        if chord_name:
            chord = Chord(
                note,
                chord_name,
                inversion=inversion,
                base_note=base_note,
                extensions=extensions
            )

        else:
            scale = self.scale

            if base_degree_interval:
                scale = Scale(scale.tonic + base_degree_interval, str(scale.name))

            chord = scale.get_chord(
                index,
                default_degrees,
                alteration=alteration,
                inversion=inversion,
                base_note=base_note,
                extensions=extensions
            )

        return chord

    def _parse_degree(self, degree, seventh=True):
        matched = HARMONY_PARSER.match(degree)
        if not matched:
            raise ValueError("Degree could not be parsed")

        parsed = matched.groupdict()
        final_alteration = 0

        degree_name = parsed.get("degree_name")
        alteration = parsed.get("alteration")
        chord_name = parsed.get("chord_name")

        index = self._DEGREES.index(degree_name.upper())
        note = self.scale.notes[index]
        if degree_name not in self.degrees and not chord_name:
            if degree_name.isupper():
                chord_name = "maj"
            else:
                chord_name = "min"

            if seventh:
                chord_name += "7"

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

        return note, final_alteration, index, chord_name

    def to_dict(self):
        return {"scale": self.scale}
