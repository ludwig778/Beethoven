from copy import copy

from beethoven.sequencer.mappings import standard_midi_mapping
from beethoven.theory.note import Interval
from beethoven.theory.note import Note as BaseNote
from beethoven.theory.note import NoteNameContainer, NoteSingletonMeta
from beethoven.utils.regex import SEQUENCER_NOTE_PARSER


class NotePitchSingletonMeta(NoteSingletonMeta):
    _INSTANCES = {}

    def __call__(cls, note_name=None):
        if note_name is None:
            raise ValueError("Note name must be set")

        elif note_name not in cls._INSTANCES:
            instance = super().__call__(note_name)
            cls._INSTANCES[note_name] = instance

        return copy(cls._INSTANCES[note_name])


class Note(BaseNote, metaclass=NotePitchSingletonMeta):
    _INTERVAL = Interval
    _DIRECTORY = {}

    def __init__(self, note_name):
        self._load_attributes(note_name)

    @property
    def name(self):
        return f"{self.note_name}{self._get_alteration_symbols()}{self.octave}"

    @classmethod
    def load(cls, mappings):
        for index, octave, *note_names in mappings:
            name_instance = NoteNameContainer(note_names)

            for note_name in note_names:
                cls._DIRECTORY[note_name + str(octave)] = (name_instance, index)

    def __lt__(self, other):
        return (
            (self.index + self.alteration) <
            (other.index + other.alteration)
        )

    def __le__(self, other):
        return self < other or self == other

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return id(self.name)

    def get_theory_self(self):
        return BaseNote(self._get_theory_note_name())

    @classmethod
    def cast_from_theory(cls, note, octave=0, inversion=None):
        return cls(f"{note.name}{octave}")

    def _load_attributes(self, note_name):
        matched = SEQUENCER_NOTE_PARSER.match(note_name)

        if not matched:
            raise ValueError("Note could not be parsed")

        parsed = matched.groupdict()

        note_name = parsed.get("note_name")
        octave = int(parsed.get("octave"))
        alteration = parsed.get("alteration")

        sharps = alteration.count("#")
        flats = alteration.count("b")

        if flats and sharps:
            raise ValueError("Note name shouldn't contain sharps AND flats")

        data = self._DIRECTORY.get(note_name.capitalize() + str(octave))

        self.note_name, self.index = data
        self.octave = octave
        self.alteration = sharps - flats
        self.index += self.alteration

    def add_interval(self, interval, **kwargs):
        note_name, alteration, octave_offset = self._add_interval_to_note(self, interval, **kwargs)

        octave_str = str(self.octave + octave_offset)

        note = self.__class__(note_name + octave_str)
        note.alteration = alteration
        note.index += alteration

        return note


Note.load(standard_midi_mapping)

note_mapping = {
    note_name: Note(note_name)
    for note_name in Note._DIRECTORY.keys()
}
