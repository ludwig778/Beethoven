from copy import copy

from beethoven.theory.interval import Interval
from beethoven.theory.mappings import note_mappings
from beethoven.utils.regex import THEORY_NOTE_PARSER
from beethoven.utils.settings import NameContainer


class NoteNameContainer(NameContainer):
    @property
    def anglosaxon(self):
        return self.names[0]

    system = anglosaxon

    @property
    def solfege(self):
        return self.names[1]


class NoteSingletonMeta(type):
    _INSTANCES = {}

    def __call__(cls, note_name=None):
        if note_name is None:
            raise ValueError("Note name must be set")

        elif note_name not in cls._INSTANCES:
            instance = super().__call__(note_name)
            cls._INSTANCES[note_name] = instance

        return copy(cls._INSTANCES[note_name])


class Note(metaclass=NoteSingletonMeta):
    _INTERVAL = Interval
    _DIRECTORY = {}
    _SYSTEM_DIRECTORY = {}

    def __init__(self, note_name):
        self._load_attributes(note_name)

    def __repr__(self):
        return f"<Note {self.name}>"

    def _get_theory_note_name(self):
        return f"{self.note_name}{self._get_alteration_symbols()}"

    @classmethod
    def to_list(cls, notes_str):
        return [cls(n) for n in notes_str.split(",")]

    @property
    def name(self):
        return self._get_theory_note_name()

    def __eq__(self, other):
        return self.name == other.name

    def __gt__(self, other):
        return (
            (self._SYSTEM_DIRECTORY[self.note_name.system][1] + self.alteration) >
            (self._SYSTEM_DIRECTORY[other.note_name.system][1] + other.alteration)
        )

    def _get_alteration_symbols(self):
        if self.alteration > 0:
            return "#" * self.alteration

        return "b" * abs(self.alteration)

    @property
    def semitones(self):
        return (self.index + self.alteration) % 12

    def __hash__(self):
        return id(self.name)

    @classmethod
    def load(cls, mappings):
        for index, *note_names in mappings:
            name_instance = NoteNameContainer(note_names)

            cls._SYSTEM_DIRECTORY[name_instance.anglosaxon] = (name_instance, index)

            for note_name in note_names:
                cls._DIRECTORY[note_name] = (name_instance, index)

            cls._DIRECTORY[name_instance.solfege] = (name_instance, index)

    def _load_attributes(self, note_name):
        matched = THEORY_NOTE_PARSER.match(note_name)
        if not matched:
            raise ValueError("Note name does not exists")

        parsed = matched.groupdict()

        note_name = parsed.get("note_name")
        alteration = parsed.get("alteration")

        sharps = alteration.count("#")
        flats = alteration.count("b")

        if flats and sharps:
            raise ValueError("Note name shouldn't contain sharps AND flats")

        data = self._DIRECTORY.get(note_name.capitalize())

        self.note_name, self.index = data
        self.alteration = sharps - flats

    def __add__(self, interval):
        return self.add_interval(interval)

    def __sub__(self, interval):
        return self.add_interval(interval, reverse=True)

    def __floordiv__(self, other):
        return self._get_interval_between_notes(self, other)

    def add_interval(self, interval, **kwargs):
        note_name, alteration, _ = self._add_interval_to_note(self, interval, **kwargs)

        note = self.__class__(note_name)
        note.alteration = alteration

        return note

    @classmethod
    def _add_interval_to_note(cls, note, interval, reverse=False):
        if not isinstance(interval, cls._INTERVAL):
            interval = cls._INTERVAL(interval)

        if reverse:
            degree_diff = - int(interval.name.numeric) + 1
            interval_st = - interval.index - interval.alteration
        else:
            degree_diff = int(interval.name.numeric) - 1
            interval_st = interval.index + interval.alteration

        # get the current note index
        for index, note_name in enumerate(list(cls._SYSTEM_DIRECTORY.keys()) * 2):
            if note_name == note.note_name.system:
                index_base_note = index
                break

        # combine interval degree difference and the base note
        target_degree = degree_diff + index_base_note

        # get the target note name, and get semitones of base and target note
        base_st = (list(cls._SYSTEM_DIRECTORY.values()) * 3)[index_base_note][1]
        dest_note, dest_st = (list(cls._SYSTEM_DIRECTORY.items()) * 3)[target_degree][1]

        # get the final alteration
        final_alteration = ((base_st - dest_st + note.alteration) % 12) + interval_st
        if final_alteration >= 12 or final_alteration <= -12:
            final_alteration = final_alteration % 12

        # necessary in some edge cases on close alterations, where single b's can lead to eleven #'s
        if final_alteration >= 6:
            final_alteration -= 12
        # necessary when removing octave interval or anything bigger than 6 half tones
        elif final_alteration <= -6:
            final_alteration += 12

        return dest_note.system, final_alteration, (degree_diff + index_base_note) // 7

    @classmethod
    def _get_interval_between_notes(cls, note1, note2):
        c_index = cls._SYSTEM_DIRECTORY["C"][1]
        self_index = cls._SYSTEM_DIRECTORY[note1.note_name.system][1]
        other_index = cls._SYSTEM_DIRECTORY[note2.note_name.system][1]

        l1 = (self_index - c_index) % 12
        l2 = (other_index - c_index) % 12

        d1 = Interval.get_interval_degree(l1)
        d2 = Interval.get_interval_degree(l2)

        degree = (d2 - d1) % 7
        interval_st = Interval.get_interval_semitones(degree)
        ll = interval_st

        alt_count = ((l2 - l1) + (note2.alteration - note1.alteration) % 12) - ll
        if alt_count >= 6:
            alt_count -= 12
        if alt_count <= -6:
            alt_count += 12

        symbol = cls._INTERVAL._get_alteration_symbols(degree + 1, alt_count)

        return cls._INTERVAL(f"{degree + 1}{symbol}")

    def to_dict(self):
        return {"note_name": self.name}


Note.load(note_mappings)
