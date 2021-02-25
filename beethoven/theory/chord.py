from collections import defaultdict

from beethoven.theory.interval import Interval
from beethoven.theory.mappings import chord_mappings
from beethoven.theory.note import Note
from beethoven.utils.regex import CHORD_PARSER
from beethoven.utils.settings import NameContainer


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

    def __call__(cls, root_note=None, chord_name=None, inversion=None, base_note=None):
        if root_note is None and chord_name is None:
            raise ValueError("Chord name and root note must be set")

        elif base_note and not isinstance(base_note, Note):
            base_note = Note(base_note)

        args = frozenset([root_note, chord_name, inversion, base_note])
        if args not in cls._INSTANCES:
            instance = super().__call__(root_note, chord_name, inversion, base_note)
            cls._INSTANCES[args] = instance

        return cls._INSTANCES[args]


class Chord(metaclass=ChordSingletonMeta):
    _DIRECTORY = {}
    _REVERSE_DIRECTORY = defaultdict(list)

    def __init__(self, root, name, inversion, base_note):
        self._load_attributes(root, name, inversion, base_note)

    def __repr__(self):
        return f"<Chord {str(self)}>"

    def __str__(self):
        string = f"{self.root.name}{self.name}"

        if self.base_note:
            string += f"/{self.base_note.name}"

        return string

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.root == other.root and
            self.notes == other.notes and
            self.base_note == other.base_note and
            self.inversion == other.inversion
        )

    @classmethod
    def get_from_fullname(cls, name, **kwargs):
        matched = CHORD_PARSER.match(name)
        if not matched:
            return

        parsed = matched.groupdict()

        note_name = parsed.get("note_name")
        alteration = parsed.get("alteration")
        chord_name = parsed.get("chord_name")

        try:
            return Chord(note_name + alteration, chord_name, **kwargs)
        except ValueError:
            return

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

    def _load_attributes(self, root_note, chord_name, inversion, base_note):
        if not isinstance(root_note, Note):
            root_note = Note(root_note)

        if not (data := self._DIRECTORY.get(chord_name)):
            raise ValueError("Chord name does not exists")

        self.name, self.intervals = data

        if inversion and (inversion < 0 or inversion >= len(self.intervals)):
            raise ValueError("Chord inversion out of range")

        self.root = root_note
        self.inversion = inversion or 0
        self.base_note = None
        if base_note and base_note != root_note:
            self.base_note = base_note

        self.notes = []
        if base_note:
            self.notes.append(base_note)

        base_chord_notes = [self.root] + [
            self.root + interval
            for interval in self.intervals[1:]
        ]
        self.notes += base_chord_notes[self.inversion:] + base_chord_notes[:self.inversion]

    def to_dict(self):
        return {
            "chord_name": self.name.short,
            "root_note": self.root,
            "base_note": self.base_note,
            "inversion": self.inversion
        }


Chord.load(chord_mappings)
