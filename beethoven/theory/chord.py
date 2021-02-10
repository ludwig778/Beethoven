from collections import defaultdict

from beethoven.settings import NameContainer
from beethoven.theory.interval import Interval
from beethoven.theory.mappings import chord_mappings
from beethoven.theory.note import Note


class ChordNameContainer(NameContainer):
    @property
    def short(self):
        return self.names[0]

    @property
    def extended(self):
        return self.names[1]

    @property
    def symbol(self):
        return self.names[2]


class ChordSingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, root_note, chord_name):
        args = frozenset([root_note, chord_name])
        if args not in cls._INSTANCES:
            instance = super().__call__(root_note, chord_name)
            cls._INSTANCES[args] = instance
        return cls._INSTANCES[args]


class Chord(metaclass=ChordSingletonMeta):
    _DIRECTORY = {}
    _REVERSE_DIRECTORY = defaultdict(list)

    def __init__(self, root, name):
        self._load_attributes(root, name)

    def __repr__(self):
        return f"<Chord {self.root.name}{self.name}>"

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.root == other.root and
            self.notes == other.notes
        )

    @classmethod
    def load(cls, mappings):
        for mapping in mappings:
            interval_names, *names = mapping
            names_instance = ChordNameContainer(names)

            intervals = []
            for interval_name in interval_names.split(","):
                intervals.append(Interval(interval_name))

            for name in names:
                cls._DIRECTORY[name] = (names_instance, intervals)

            cls._REVERSE_DIRECTORY[interval_names] = names_instance

    @classmethod
    def get_chord_name_from_intervals(cls, intervals):
        return cls._REVERSE_DIRECTORY.get(",".join([i.shortname for i in intervals]))

    def _load_attributes(self, root_note, chord_name):
        if not isinstance(root_note, Note):
            root_note = Note(root_note)

        self.root = root_note

        if not (data := self._DIRECTORY.get(chord_name)):
            raise ValueError("Chord name does not exists")

        self.name, self.intervals = data

        self.notes = [self.root] + [
            self.root + interval
            for interval in self.intervals[1:]
        ]


Chord.load(chord_mappings)
