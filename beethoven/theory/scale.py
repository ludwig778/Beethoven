from collections import defaultdict

from beethoven.theory.chord import Chord
from beethoven.theory.interval import AUGMENTED, DIMINISHED, Interval
from beethoven.theory.mappings import scale_mappings
from beethoven.theory.note import Note
from beethoven.utils.name_container import NameContainer


class ScaleNameContainer(NameContainer):
    pass


class ScaleSingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, tonic=None, scale_name=None):
        if tonic is None and scale_name is None:
            raise ValueError("Scale name and tonic note must be set")

        args = frozenset([tonic, scale_name])
        if args not in cls._INSTANCES:
            instance = super().__call__(tonic, scale_name)
            cls._INSTANCES[args] = instance

        return cls._INSTANCES[args]


class Scale(metaclass=ScaleSingletonMeta):
    _DIRECTORY = {}
    _MODES_DIRECTORY = defaultdict(list)

    def __init__(self, tonic, name):
        self._load_attributes(tonic, name)

    def __repr__(self):
        return f"<Scale {str(self)}>"

    def __str__(self):
        return f"{self.tonic.name} {self.name}"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.name == other.name and
            self.tonic == other.tonic and
            self.notes == other.notes
        )

    def __hash__(self):
        return id(self.name)

    @classmethod
    def load(cls, mappings):
        for mapping in mappings:
            interval_names, mode_name, *names = mapping
            names_instance = ScaleNameContainer(names)

            intervals = [
                Interval(interval_name)
                for interval_name in interval_names.split(",")
            ]

            for name in names:
                cls._DIRECTORY[name] = (names_instance, mode_name, intervals)

            if mode_name:
                cls._MODES_DIRECTORY[mode_name].append(names[0])

    def _load_attributes(self, tonic, scale_name):
        if not isinstance(tonic, Note):
            tonic = Note(tonic)

        self.tonic = tonic

        if not (data := self._DIRECTORY.get(scale_name)):
            raise ValueError("Scale name does not exists")

        self.name, self.mode, self.intervals = data

        self.notes = [self.tonic] + [
            self.tonic + interval
            for interval in self.intervals[1:]
        ]

        self.mode_index = None
        if self.mode:
            self.mode_index = self._MODES_DIRECTORY[self.mode].index(str(self.name))

    def get_chord(self, start_degree, degrees, alteration=0, inversion=None, base_note=None, extensions=None):
        degrees = degrees.split(",")
        notes = []

        for degree in degrees:
            note = self.notes[(start_degree + int(degree) - 1) % 7]
            # TODO
            # make DIMINISHED and AUGMENTED multipliable to avoid the range loop
            if alteration < 0:
                for _ in range(abs(alteration)):
                    note += DIMINISHED
            elif alteration > 0:
                for _ in range(alteration):
                    note += AUGMENTED
            notes.append(note)

        first_note = notes[0]
        intervals = []
        for note in notes:
            intervals.append(first_note // note)

        chord_name = Chord.get_chord_name_from_intervals(intervals)

        return Chord(
            first_note,
            chord_name.short,
            inversion=inversion,
            base_note=base_note,
            extensions=extensions
        )

    def switch_mode(self, index):
        if not len(self.notes) == 7:
            raise ValueError("Scale doesnt have modes")

        mode_name = self._MODES_DIRECTORY[self.mode][(self.mode_index + index) % 7]

        return Scale(self.tonic, mode_name)

    def to_dict(self):
        return {"tonic": self.tonic, "scale_name": str(self.name)}


Scale.load(scale_mappings)
