from __future__ import annotations

from copy import copy
from dataclasses import dataclass, field, replace
from fractions import Fraction
# from functools import lru_cache
from itertools import product
from typing import Any, Dict, Generator, List, Sequence, Tuple, Union
from uuid import UUID, uuid4

from pyparsing import ParseException

from beethoven import parser
from beethoven.constants import duration as duration_constants
from beethoven.indexes import (chord_index, degree_index, interval_index,
                               note_index, scale_index)
from beethoven.utils.alterations import (get_degree_alteration_int_from_str,
                                         get_degree_alteration_str_from_int,
                                         get_interval_alteration_int_from_str,
                                         get_interval_alteration_str_from_int,
                                         get_note_alteration_int_from_str,
                                         get_note_alteration_str_from_int)

# cache = lru_cache(maxsize=None)


def cache(f: Any) -> Any:
    def swrapper(*args: Any, **kwargs: Any) -> Any:
        return f(*args, **kwargs)
    return swrapper


@dataclass
class Degree:
    name: str
    alteration: int = 0

    def __post_init__(self) -> None:
        if not degree_index.is_valid(self.name):
            raise ValueError(f"Invalid name: {self.name}")

        if self.alteration < -3 or self.alteration > 3:
            raise ValueError(f"Invalid alteration: {self.alteration}, must be between -3 and 3")

    def __str__(self) -> str:
        return f"{get_degree_alteration_str_from_int(self.alteration)}{self.name}"

    def __hash__(self) -> int:
        return hash(self.name + str(self.alteration))

    @property
    def index(self) -> int:
        return degree_index.get_index(self.name)

    @classmethod
    @cache
    def parse(cls, string: str) -> Degree:
        parsed = parser.parse(parser.degree_pattern, string)

        return cls.build(**parsed)  # type: ignore[no-any-return]

    @classmethod
    def parse_list(cls, degrees_string: str) -> List[Degree]:
        return [cls.parse(degree_string) for degree_string in degrees_string.split(",")]

    @classmethod
    @cache
    def build(cls, name: str, alteration: str | None = None) -> Degree:
        return cls(
            name=name,
            alteration=get_degree_alteration_int_from_str(alteration) if alteration else 0,
        )

    def to_interval(self) -> Interval:
        return Interval(name=str(degree_index.get_index(self.name) + 1), alteration=self.alteration)

    def remove_alteration(self) -> Degree:
        return replace(self, alteration=0)


@dataclass
class Note:
    name: str
    alteration: int = 0
    octave: int | None = None

    def __hash__(self) -> int:
        return hash(self.name + str(self.alteration) + str(self.octave))

    def __str__(self) -> str:
        return f"{self.name}{get_note_alteration_str_from_int(self.alteration)}{self.octave if self.octave is not None else ''}"

    def __post_init__(self) -> None:
        if not note_index.is_valid(self.name):
            raise ValueError(f"Invalid name: {self.name}")

        if self.alteration < -4 or self.alteration > 4:
            raise ValueError(f"Invalid alteration: {self.alteration}, must be between -4 and 4")

        if self.octave is not None and (self.octave < 0 or self.octave > 10):
            raise ValueError(f"Invalid octave: {self.octave}, must be between 0 and 10")

    @property
    def index(self) -> int:
        return self.midi_index % 12

    @property
    def midi_index(self) -> int:
        if not self.octave:
            return (note_index.get_semitones(self.name) + self.alteration) % 12

        return 24 + note_index.get_semitones(self.name) + self.alteration + self.octave * 12

    # TODO: move to utils, setup a customized exception
    def check_octave_states(self, other: Note) -> None:
        """Check that both notes have or have not octaves"""

        # Apply a XOR function checking on None values
        if [self.octave is None, other.octave is None].count(False) == 1:
            raise Exception("Octaves must be present or absent in order to compare Notes")

    def __eq__(self, other: object) -> bool:
        """Check notes pitch equality, since we check on the midi_index property"""

        if not isinstance(other, Note):
            return NotImplemented

        self.check_octave_states(other)

        return self.midi_index == other.midi_index

    def __gt__(self, other: Note) -> bool:
        self.check_octave_states(other)

        return self.midi_index > other.midi_index

    def __ge__(self, other: Note) -> bool:
        self.check_octave_states(other)

        return self.midi_index >= other.midi_index

    @classmethod
    @cache
    def parse(cls, string: str) -> Note:
        parsed = parser.parse(parser.note_pattern, string)

        return cls.build(**parsed)  # type: ignore[no-any-return]

    @classmethod
    def parse_list(cls, notes_string: str) -> List[Note]:
        return [cls.parse(note_string) for note_string in notes_string.split(",")]

    @classmethod
    @cache
    def build(cls, name: str, alteration: str | None = None, octave: int | None = None) -> Note:
        return cls(
            name=name,
            alteration=get_note_alteration_int_from_str(alteration) if alteration else 0,
            octave=octave,
        )

    @classmethod
    def from_midi_index(cls, index: int) -> Note:
        octave, rest_index = divmod(index, 12)

        note = cls.parse("C" + str(octave))

        intervals = {
            0: "1",
            2: "2",
            4: "3",
            5: "4",
            7: "5",
            9: "6",
            11: "7",
        }

        for semitones, interval_name in intervals.items():
            if semitones >= rest_index:
                interval = Interval.parse(interval_name)
                interval.alteration = rest_index - semitones

                break

        return note.add_interval(interval)  # type: ignore[no-any-return]

    def add_interval(self, interval: Interval, reverse: bool = False) -> Note:
        degree_gap = int(interval.name) - 1
        semitone_gap = interval_index.get_semitones(interval.name) + interval.alteration

        if reverse:
            degree_gap *= -1
            semitone_gap *= -1

        origin_index = note_index.get_index(self.name)
        octave_gap, target_degree = divmod(degree_gap + origin_index, 7)

        origin_semitones = note_index.get_semitones(self.name)
        destination_note = note_index.get_name_from_index(target_degree % 7)
        destination_semitones = note_index.get_semitones(destination_note)

        destination_alteration = (
            origin_semitones + semitone_gap + self.alteration - destination_semitones - (12 * octave_gap)
        )

        destination_octave = None
        if self.octave is not None:
            destination_octave = self.octave + octave_gap

        return Note(
            name=destination_note,
            alteration=destination_alteration,
            octave=destination_octave,
        )

    def get_interval(self, note: Note) -> Interval:
        index_1 = note_index.get_index(self.name)
        index_2 = note_index.get_index(note.name)
        index_diff = index_2 - index_1

        semitones_1 = note_index.get_semitones(self.name)
        semitones_2 = note_index.get_semitones(note.name)

        octave_diff = 0
        if self.octave and note.octave:
            semitones_1 += self.octave * 12
            semitones_2 += note.octave * 12

            semitones_diff = semitones_2 - semitones_1

            octave_diff = note.octave - self.octave

            index_diff += octave_diff * 7
        else:
            semitones_diff = (semitones_2 - semitones_1) % 12
            index_diff %= 7

        name = interval_index.get_name_from_index(index_diff)
        semitones = interval_index.get_semitones(name)
        alteration = semitones_diff - semitones - self.alteration + note.alteration

        return Interval(name=name, alteration=alteration)

    def remove_octave(self) -> Note:
        return replace(self, octave=None)

    @staticmethod
    def remove_notes_octave(notes: List[Note]) -> List[Note]:
        return [note.remove_octave() for note in notes]


@dataclass
class NotesList:
    notes: List[Note]

    def __hash__(self) -> int:
        return hash("_".join(map(str, self.notes)))


@dataclass
class Interval:
    name: str
    alteration: int = 0

    def __post_init__(self) -> None:
        if not interval_index.is_valid(self.name):
            raise ValueError(f"Invalid name: {self.name}")

        if self.alteration < -3 or self.alteration > 3:
            raise ValueError(f"Invalid alteration: {self.alteration}, must be between -3 and 3")

    def __hash__(self) -> int:
        return hash(self.name + str(self.alteration))

    def __str__(self) -> str:
        alteration_str = get_interval_alteration_str_from_int(self.alteration, int(self.name))

        return f"{self.name}{alteration_str}"

    @property
    def semitones(self) -> int:
        return interval_index.get_semitones(self.name) + self.alteration

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Interval):
            return NotImplemented

        return self.semitones == other.semitones

    def __gt__(self, other: Interval) -> bool:
        return self.semitones > other.semitones

    def __ge__(self, other: Interval) -> bool:
        return self.semitones >= other.semitones

    def extension_str(self) -> str:
        return f"{get_degree_alteration_str_from_int(self.alteration)}{self.name}"

    @classmethod
    @cache
    def parse(cls, string: str) -> Interval:
        parsed = parser.parse(parser.interval_pattern, string)

        return cls.build(**parsed)  # type: ignore[no-any-return]

    @classmethod
    def parse_list(cls, intervals_string: str) -> List[Interval]:
        return [cls.parse(interval_string) for interval_string in intervals_string.split(",")]

    @classmethod
    @cache
    def build(
        cls,
        name: str,
        alteration: Optistr | None = None,
    ) -> Interval:
        return cls(
            name=name,
            alteration=get_interval_alteration_int_from_str(alteration=alteration, interval=int(name))
            if alteration
            else 0,
        )


@dataclass
class Chord:
    root: Note
    name: str

    inversion: int | None = None
    base_note: Note | None = None
    extensions: List[Interval] | None = None

    degree: Degree | None = None
    base_degree: Degree | None = None

    def __post_init__(self) -> None:
        if not chord_index.is_valid(self.name):
            raise ValueError(f"Invalid name: {self.name}")

    def __hash__(self) -> int:
        return hash(
            f"{self.root}_{self.name}:"
            f"{self.inversion}:{self.base_note}:{self.degree}:{self.base_degree}:"
            f"{'.'.join(map(str, self.extensions)) if self.extensions else self.extensions}"
        )

    def __str__(self) -> str:
        return f"{self.degree or self.root} {self.name}"

    @classmethod
    @cache
    def parse(cls, string: str) -> Chord:
        parsed = parser.parse(parser.chord_pattern, string)

        return cls.build(**parsed)

    @classmethod
    @cache
    def parse_with_scale_context(cls, string: str, scale: Scale) -> Chord:
        parsed = parser.parse(parser.chord_pattern, string)

        return cls.build(**parsed, scale=scale)

    @classmethod
    def build(
        cls,
        root: Union[Note, Dict[str, Any]] | None = None,
        name: str | None = None,
        inversion: int | None = None,
        base_note: Union[Note, Dict[str, Any]] | None = None,
        extensions: Sequence[Union[Interval, Dict[str, Any]]] | None = None,
        degree: Union[Degree, Dict[str, Any]] | None = None,
        base_degree: Union[Degree, Dict[str, Any]] | None = None,
        scale: Scale | None = None,
    ) -> Chord:
        if name and "_" in name:
            name = name.replace("_", " ")

        if root and degree:
            raise Exception("Only a Note or a Degree can be set as root")

        if isinstance(root, dict):
            root = Note.build(**root)
        if isinstance(degree, dict):
            degree.pop("octave", None)
            degree = Degree.build(**degree)
        if isinstance(base_degree, dict):
            base_degree = Degree.build(**base_degree)

        if not root and degree:
            if not scale:
                raise Exception("Scale must be set")

            root = scale.get_note_from_degree(degree)

            if not name:
                chords = scale.get_diatonic_chords()
                name = chords[degree.index].name

            if base_degree:
                root = root.add_interval(base_degree.to_interval())
        elif not root:
            raise Exception("Root note or degree need to be set")

        if isinstance(base_note, dict):
            base_note = Note.build(**base_note)

        _extensions: List[Interval] | None = None
        if extensions is not None:
            _extensions = [
                extension if isinstance(extension, Interval) else Interval.build(**extension)
                for extension in extensions
            ]

        return cls(
            name=name or "maj",
            root=root,
            degree=degree,
            inversion=inversion,
            extensions=_extensions,
            base_note=base_note,
            base_degree=base_degree,
        )

    @property
    def intervals(self) -> List[Interval]:
        intervals_string = chord_index.get_intervals(self.name or "maj")
        intervals = Interval.parse_list(intervals_string)

        return intervals

    @property
    def notes(self) -> List[Note]:
        notes = [self.root.add_interval(interval) for interval in self.intervals]

        if self.inversion:
            notes = notes[self.inversion :] + [
                note.add_interval(Interval(name="8")) for note in notes[: self.inversion]
            ]

        if self.base_note:
            base_note = copy(self.base_note)

            if self.root.octave and not base_note.octave:
                if notes[0].octave:
                    base_note.octave = notes[0].octave

                    if base_note > notes[0]:
                        base_note.octave -= 1

            elif base_note.octave and not notes[0].octave:
                last_note = base_note
                for note in notes:
                    note.octave = base_note.octave

                    if note < last_note:
                        note.octave += 1

                    last_note = note

            notes.insert(0, base_note)

        if self.extensions:
            notes += [self.root.add_interval(interval) for interval in self.extensions]

        if self.extensions and self.root.octave:
            notes = sorted(notes)

        return notes

    @staticmethod
    def chord_product(roots: List[Note], chord_names: List[str]) -> List[Chord]:
        return [
            Chord.parse(f"{str(root)}_{chord_name}") for root, chord_name in product(roots, chord_names)
        ]

    def set_root_octave(self, octave: int) -> Chord:
        return replace(self, root=replace(self.root, octave=octave))


@dataclass
class Scale:
    tonic: Note
    name: str

    def __post_init__(self) -> None:
        if not scale_index.is_valid(self.name):
            raise ValueError(f"Invalid name: {self.name}")

    def __hash__(self) -> int:
        return hash(f"{self.tonic}_{self.name}")

    def __str__(self) -> str:
        return f"{self.tonic} {self.name}"

    @property
    def is_diatonic(self) -> bool:
        return len(self.notes) == 7

    def to_log_string(self) -> str:
        return f"{self.tonic} {self.name}"

    @classmethod
    @cache
    def parse(cls, string: str) -> Scale:
        parsed = parser.parse(parser.scale_pattern, string)

        return cls.build(**parsed)

    @classmethod
    def build(cls, tonic: Union[Dict[str, Any], Note], name: str) -> Scale:
        return cls(
            tonic=Note.build(**tonic) if isinstance(tonic, dict) else tonic,
            name=name.replace("_", " "),
        )

    @property
    def intervals(self) -> List[Interval]:
        intervals_string = scale_index.get_intervals(self.name)
        intervals = Interval.parse_list(intervals_string)

        return intervals

    @property
    def notes(self) -> List[Note]:
        return [self.tonic.add_interval(interval) for interval in self.intervals]

    @staticmethod
    def scale_product(tonics: List[Note], scale_names: List[str]) -> List[Scale]:
        return [
            Scale.parse(f"{str(tonic)}_{scale_name}")
            for tonic, scale_name in product(tonics, scale_names)
        ]

    def get_note_from_degree(self, degree: Degree) -> Note:
        note = self.notes[degree.index]

        return replace(note, alteration=note.alteration + degree.alteration)

    def get_diatonic_chords(self) -> List[Chord]:
        chords = []

        two_octave_notes = self.notes + [note.add_interval(Interval(name="8")) for note in self.notes]

        for degree_num in range(7):
            root = two_octave_notes[degree_num]

            notes = []
            intervals = []
            for chord_degree in [1, 3, 5, 7]:
                note = two_octave_notes[degree_num + chord_degree - 1]

                notes.append(note)
                intervals.append(root.get_interval(note))

            intervals_str = ",".join([str(i) for i in intervals])

            chord = Chord(root=root, name=chord_index.get_name_from_intervals(intervals_str))
            chords.append(chord)

        return chords


@dataclass
class Bpm:
    value: int

    def __str__(self) -> str:
        return str(self.value)

    def __post_init__(self) -> None:
        if self.value <= 0 or self.value > 600:
            raise ValueError(f"Invalid value: {self.value}, must be between 0 and 600")

    @classmethod
    @cache
    def parse(cls, string: str) -> Bpm:
        parsed = parser.parse(parser.bpm_pattern, string)

        return cls(**parsed)

    @classmethod
    @cache
    def _build(cls, value: int) -> Bpm:
        return cls(value=value)


@dataclass
class Duration:
    value: Fraction = Fraction(0)

    @staticmethod
    def get_base_duration_string(base_duration: Duration, short: bool = True) -> str:
        return {
            Duration.parse("4"): ("whole", "w"),
            Duration.parse("2"): ("half", "h"),
            Duration.parse("1"): ("quarter", "q"),
            Duration.parse("1/2"): ("eighth", "e"),
            Duration.parse("1/4"): ("sixteenth", "s"),
        }[base_duration][int(short)]

    def __hash__(self) -> int:
        return hash(self.value)

    def __add__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value + other.value)

    def __iadd__(self, other: object) -> Duration:
        return Duration.__add__(self, other)

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented

        return self.value > other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Duration):
            return NotImplemented

        return self.value == other.value or self.value > other.value

    def __mul__(self, other: Union[Fraction, int]) -> Duration:
        return Duration(value=self.value * other)

    def __sub__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value - other.value)

    def __neg__(self) -> Duration:
        return Duration(value=self.value * -1)

    def __mod__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value % other.value)

    def __floordiv__(self, other: object) -> Duration:
        if isinstance(other, int):
            return Duration(value=Fraction(self.value // other))

        elif not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=Fraction(self.value // other.value))

    def __truediv__(self, other: object) -> Duration:
        if isinstance(other, int):
            return Duration(value=Fraction(self.value / other))

        elif not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=Fraction(self.value / other.value))

    def __divmod__(self, other: object) -> Tuple[int, Duration]:
        if not isinstance(other, Duration):
            return NotImplemented

        return self.value // other.value, self % other

    def __bool__(self) -> bool:
        return bool(self.value)

    def __str__(self) -> str:
        return str(float(self.value))

    def __repr__(self) -> str:
        return str(self)

    @classmethod
    @cache
    def parse(cls, string: str) -> Duration:
        return cls.build(**parser.parse(parser.duration_pattern, string))  # type: ignore[no-any-return]

    @classmethod
    @cache
    def build(
        cls,
        base_duration: str | None = None,
        numerator: int | None = None,
        denominator: int | None = None,
    ) -> Duration:
        if base_duration is None:
            value = Fraction(1)
        else:
            value = duration_constants.base_values[base_duration]

        if numerator is not None:
            value *= numerator

        if denominator is not None:
            value /= denominator

        return cls(value=value)


@dataclass
class TimeSignature:
    beats_per_bar: int
    beat_unit: int

    def __str__(self) -> str:
        return f"{self.beats_per_bar}/{self.beat_unit}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __post_init__(self) -> None:
        if self.beat_unit < 1 or self.beat_unit > 32:
            raise ValueError(f"Invalid beat_unit: {self.beat_unit}, must be in range 1-32")

        if self.beat_unit not in (1, 2, 4, 8, 16, 32):
            raise ValueError(f"Invalid beat_unit: {self.beat_unit}, must be a multiple of 2")

    @classmethod
    @cache
    def parse(cls, string: str) -> TimeSignature:
        parsed = parser.parse(parser.time_signature_pattern, string)

        return cls(**parsed)

    """
    @classmethod
    @cache
    def _build(cls, beats_per_bar: int, beat_unit: int) -> TimeSignature:
        return cls(beats_per_bar=beats_per_bar, beat_unit=beat_unit)
    """

    @cache
    def get_duration(self) -> Duration:
        return Duration(value=Fraction(self.beats_per_bar * 4, self.beat_unit))

    def get_time_section(self, cursor: Duration, bar_offset: int = 0) -> TimeSection:
        reduction = Fraction(self.beat_unit, 4)

        bar, measure_rest = divmod(cursor.value * reduction, self.beats_per_bar)
        measure, rest = divmod(measure_rest * reduction, 1)

        return TimeSection(bar=bar_offset + bar + 1, measure=measure + 1, rest=rest)

    def generate_time_sections(
        self,
        step: Duration,
        cursor_offset: Duration = Duration(),
        base_time_section: TimeSection | None = None,
    ) -> Generator[Tuple[TimeSection, Duration], None, None]:
        cursor = Duration()

        bar_offset = 0
        if base_time_section:
            bar_offset = base_time_section.bar - 1

        while True:
            time_section = self.get_time_section(cursor, bar_offset=bar_offset)

            yield time_section, cursor + cursor_offset

            cursor += step


@dataclass
class TimeSection:
    bar: int = 1
    measure: int = 1
    rest: Fraction = Fraction()

    """
    def __post_init__(self):
        if isinstance(self.rest, int):
            self.rest = Fraction(self.rest)
    """

    def to_next_bar(self) -> None:
        if self.measure > 1 or self.rest != Fraction():
            self.bar += 1
            self.measure = 1
            self.rest = Fraction()

    def __str__(self) -> str:
        return f"{self.bar}:{self.measure}:{float(self.rest)}"


@dataclass
class DurationItem:
    numerator: int = 1
    denominator: int = 1
    base_duration: Duration | None = None

    @property
    def fraction(self) -> Fraction:
        return Fraction(self.numerator, self.denominator)

    @property
    def value(self) -> Duration | None:
        if not self.base_duration:
            return None

        return self.base_duration * self.fraction

    def to_string(self) -> str:
        if not self.base_duration:
            return ""

        return (str(self.numerator) if self.numerator > 1 else "") + Duration.get_base_duration_string(
            self.base_duration
        ).upper()

    def to_log_string(self) -> str:
        return (
            f"{self.numerator}/{self.denominator}"
            f"{Duration.get_base_duration_string(self.base_duration).upper() if self.base_duration else ''}"
        )

    def dict(self) -> Dict[str, Any]:
        return {
            "numerator": self.numerator,
            "denominator": self.denominator,
            "base_duration": self.base_duration,
        }


@dataclass
class ChordItem:
    root: Union[Note, Degree]
    name: str

    duration_item: DurationItem

    inversion: int = 0
    base_note: Note | None = None
    extensions: List[Interval] | None = None

    id: UUID = field(default_factory=uuid4)

    def __hash__(self) -> int:
        return int(self.id)

    @staticmethod
    def parse_root_note_or_degree(string: str) -> Note | Degree:
        try:
            return Note.parse(string)  # type: ignore[no-any-return]
        except ParseException:
            pass

        try:
            return Degree.parse(string)  # type: ignore[no-any-return]
        except ParseException:
            pass

        raise Exception('Couldn\'t parse note or degree from: "{string}"')

    def to_simple_string(self) -> str:
        chord_name = str(self.root)

        if self.name:
            chord_name += " " + self.name.replace("_", " ")

        if self.inversion:
            chord_name += f"{self.inversion}".translate(str.maketrans("123", "₁₂₃"))

        if self.base_note:
            chord_name += f" /{self.base_note}"

        if self.extensions:
            chord_name += " " + ",".join(map(Interval.extension_str, self.extensions))

        return chord_name

    def to_log_string(self) -> str:
        return (
            f"id={self.id} root={self.root} "
            f"name={self.name} duration_item={self.duration_item.to_log_string()} "
            f"inversion={self.inversion} base_note={self.base_note} "
            "extensions="
            + (
                ",".join([f"{extension.extension_str()}" for extension in self.extensions])
                if self.extensions
                else ""
            )
        )

    def as_chord(self, scale: Scale) -> Chord:
        chord_str = f"{self.root}4"

        if self.name:
            chord_str += f"_{self.name.replace(' ', '_')}"

        root_note = None
        root_degree = None

        if isinstance(self.root, Note):
            root_note = self.root
        else:
            root_degree = self.root

        return Chord.build(
            root=root_note,
            degree=root_degree,
            name=self.name,
            inversion=self.inversion,
            base_note=self.base_note,
            extensions=self.extensions,
            scale=scale,
        )

    """
   @classmethod
    def _build(cls, name: str, root: str, duration_item: DurationItem) -> ChordItem:
        return cls(
            name=name,
            root=cls.parse_root_note_or_degree(root),
            duration_item=duration_item,
        )
    """

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            "name": self.name,
            "root": str(self.root),
            "duration_item": self.duration_item.dict(),
            "inversion": self.inversion,
            "base_note": self.base_note,
            "extensions": [str(extension) for extension in self.extensions] if self.extensions else None,
        }


@dataclass
class HarmonyItem:
    scale: Scale
    chord_items: List[ChordItem]
    bpm: Bpm
    time_signature: TimeSignature

    id: UUID = field(default_factory=uuid4)

    def __hash__(self) -> int:
        return int(self.id)

    """
    @classmethod
    def _build(
        cls,
        scale: Union[Scale, str],
        chord_items: List[Union[ChordItem, Dict[str, Any]]],
        bpm: Union[Bpm, str],
        time_signature: Union[TimeSignature, str],
    ) -> HarmonyItem:
        if isinstance(scale, str):
            scale = Scale.parse(scale)

        _chord_items: List[ChordItem] = [
            chord_item if isinstance(chord_item, ChordItem) else ChordItem.build(**chord_item)
            for chord_item in chord_items
        ]

        if isinstance(bpm, str):
            bpm = Bpm.parse(bpm)

        if isinstance(time_signature, str):
            time_signature = TimeSignature.parse(time_signature)

        return cls(
            scale=scale,
            chord_items=_chord_items,
            bpm=bpm,
            time_signature=time_signature,
        )
    """

    def to_log_string(self) -> str:
        return (
            f"id={self.id} scale={self.scale} "
            f"bpm={self.bpm} time_signature={self.time_signature} "
            "chord_items=" + ";".join([chord_item.to_log_string() for chord_item in self.chord_items])
        )

    def dict(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        return {
            "scale": str(self.scale).replace(" ", "_"),
            "chord_items": [chord_item.dict() for chord_item in self.chord_items],
            "bpm": self.bpm,
            "time_signature": self.time_signature,
        }


@dataclass
class HarmonyItemsIterator:
    items: List[HarmonyItem]
