from __future__ import annotations

from copy import copy, deepcopy
from fractions import Fraction
from itertools import product
from typing import Dict, Generator, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, Field, validator

from beethoven import parser
from beethoven.constants import duration
from beethoven.indexes import (
    chord_index,
    degree_index,
    interval_index,
    note_index,
    scale_index,
)
from beethoven.utils.alterations import (
    get_degree_alteration_int_from_str,
    get_degree_alteration_str_from_int,
    get_interval_alteration_int_from_str,
    get_interval_alteration_str_from_int,
    get_note_alteration_str_from_int,
)
from beethoven.utils.note import note_alteration_to_int


class Degree(BaseModel):
    name: str
    alteration: int = 0

    def __str__(self):
        return f"{get_degree_alteration_str_from_int(self.alteration)}{self.name}"

    def __hash__(self):
        return hash(self.name + str(self.alteration))

    @validator("name")
    def name_must_be_valid(cls, name):
        if degree_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")

    @property
    def index(self):
        return degree_index.get_index(self.name)

    @classmethod
    def parse(cls, string: str) -> Degree:
        parsed = parser.parse(parser.degree_pattern, string)

        return cls.build(**parsed)

    @classmethod
    def parse_list(cls, degrees_string: str) -> List[Degree]:
        return [cls.parse(degree_string) for degree_string in degrees_string.split(",")]

    @staticmethod
    def build(name: str, alteration: Optional[int] = None) -> Degree:
        return Degree(
            name=name,
            alteration=get_degree_alteration_int_from_str(str(alteration or "")),
        )

    def to_interval(self) -> Interval:
        return Interval(
            name=degree_index.get_index(self.name) + 1, alteration=self.alteration
        )


class Note(BaseModel):
    name: str
    alteration: int = 0
    octave: Optional[int] = None

    def __hash__(self):
        return hash(self.name + str(self.alteration) + str(self.octave))

    def __str__(self):
        return f"{self.name}{get_note_alteration_str_from_int(self.alteration)}{self.octave or ''}"

    @validator("name")
    def name_must_be_valid(cls, name):
        if note_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -4 <= alteration <= 4:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -4 and 4")

    @validator("octave")
    def octave_must_be_valid(cls, octave):
        if octave is None or 0 <= octave <= 10:
            return octave

        raise ValueError(f"Invalid octave: {octave}, must be between 0 and 10")

    @property
    def midi_index(self) -> int:
        if not self.octave:
            return (note_index.get_semitones(self.name) + self.alteration) % 12

        return note_index.get_semitones(self.name) + self.alteration + self.octave * 12

    # TODO: move to utils, setup a customized exception
    def check_octave_states(self, other: Note) -> None:
        """Check that both notes have or have not octaves"""

        # Apply a XOR function checking on None values
        if [self.octave is None, other.octave is None].count(False) == 1:
            raise Exception(
                "Octaves must be present or absent in order to compare Notes"
            )

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
    def parse(cls, string: str) -> Note:
        parsed = parser.parse(parser.note_pattern, string)

        return cls.build(**parsed)

    @classmethod
    def parse_list(cls, notes_string: str) -> List[Note]:
        return [cls.parse(note_string) for note_string in notes_string.split(",")]

    @staticmethod
    def build(**parsed: Dict) -> Note:
        return Note(
            name=parsed["name"],
            alteration=note_alteration_to_int(str(parsed.get("alteration", ""))),
            octave=parsed.get("octave"),
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

        return note.add_interval(interval)

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
            origin_semitones
            + semitone_gap
            + self.alteration
            - destination_semitones
            - (12 * octave_gap)
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
        note = deepcopy(self)
        note.octave = None

        return note

    @staticmethod
    def remove_notes_octave(notes: List[Note]) -> List[Note]:
        return [note.remove_octave() for note in notes]


class NotesList(BaseModel):
    notes: List[Note]

    def __hash__(self):
        return hash("_".join(map(str, self.notes)))


class Interval(BaseModel):
    name: str
    alteration: int = 0

    @validator("name")
    def name_must_be_valid(cls, name):
        if interval_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @validator("alteration")
    def alteration_must_be_valid(cls, alteration):
        if -3 <= alteration <= 3:
            return alteration

        raise ValueError(f"Invalid alteration: {alteration}, must be between -3 and 3")

    def __str__(self):
        alteration_str = get_interval_alteration_str_from_int(
            self.alteration, int(self.name)
        )

        return f"{self.name}{alteration_str}"

    @classmethod
    def parse(cls, string: str) -> Interval:
        parsed = parser.parse(parser.interval_pattern, string)

        return cls.build(**parsed)

    @classmethod
    def parse_list(cls, intervals_string: str) -> List[Interval]:
        return [
            cls.parse(interval_string)
            for interval_string in intervals_string.split(",")
        ]

    @staticmethod
    def build(
        name: str,
        alteration: str = "",
        octave: Optional[int] = None,
    ) -> Interval:
        return Interval(
            name=name,
            alteration=get_interval_alteration_int_from_str(
                alteration=alteration, interval=int(name)
            ),
            octave=octave,
        )


class Chord(BaseModel):
    root: Note
    name: str

    # notes: List[Note] = Field(default_factory=list)
    # intervals: List[Interval] = Field(default_factory=list)

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = Field(default_factory=list)

    degree: Optional[Degree] = Field(default=None, repr=False)
    base_degree: Optional[Degree] = Field(default=None, repr=False)

    def __hash__(self):
        return hash(
            f"{self.root}_{self.name}:"
            f"{self.inversion}:{self.base_note}:{self.degree}:{self.base_degree}:"
            f"{'.'.join(map(str, self.extensions))}"
        )

    def __str__(self):
        return f"{self.degree or self.root} {self.name}"

    @validator("name")
    def name_must_be_valid(cls, name):
        if chord_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @classmethod
    def parse(cls, string: str) -> Chord:
        parsed = parser.parse(parser.chord_pattern, string)

        return cls.build(**parsed)

    @classmethod
    def parse_with_scale_context(
        cls, string: str, scale: Optional[Scale] = None
    ) -> Chord:
        parsed = parser.parse(parser.chord_pattern, string)

        return cls.build(**parsed, scale=scale)

    @staticmethod
    def build(
        name: Optional[str] = None, scale: Optional[Scale] = None, **parsed: Dict
    ) -> Chord:
        if name and "_" in name:
            name = name.replace("_", " ")

        root = degree = base_degree = None

        if parsed_root := parsed.get("root"):
            root = (
                parsed_root
                if isinstance(parsed_root, Note)
                else Note.build(**parsed_root)
            )

        elif parsed_degree := parsed.get("degree"):
            if not scale:
                raise Exception("Scale must be set")

            parsed_degree.pop("octave", None)

            degree = Degree.build(**parsed_degree)
            root = scale.get_note_from_degree(degree)

            if not name:
                chords = scale.get_diatonic_chords()
                name = chords[degree.index].name

            if parsed_base_degree := parsed.get("base_degree"):
                base_degree = Degree.build(**parsed_base_degree)
                root = root.add_interval(base_degree.to_interval())

        if not root:
            raise Exception(f"Failed to get root note: {parsed=}")

        # intervals_string = chord_index.get_intervals(name or "maj")
        # intervals = Interval.parse_list(intervals_string)

        # notes = [root.add_interval(interval) for interval in intervals]

        inversion = parsed.get("inversion")
        # if inversion := parsed.get("inversion"):
        #    notes = notes[inversion:] + [
        #        note.add_interval(octave) for note in notes[:inversion]
        #    ]

        base_note = None
        if base_note_parsed := parsed.get("base_note"):
            base_note = (
                base_note_parsed
                if isinstance(base_note_parsed, Note)
                else Note.build(**base_note_parsed)
            )

        extensions = []
        if extensions_parsed := parsed.get("extensions"):
            extensions = [
                Interval.build(**extension_parsed)
                for extension_parsed in extensions_parsed
            ]

        return Chord(
            root=root,
            name=name or "maj",
            inversion=inversion,
            extensions=extensions,
            base_note=base_note,
            degree=degree,
            base_degree=base_degree,
        )

    @property
    def intervals(self):
        intervals_string = chord_index.get_intervals(self.name or "maj")
        intervals = Interval.parse_list(intervals_string)

        return intervals

    @property
    def notes(self):
        notes = [self.root.add_interval(interval) for interval in self.intervals]

        if self.inversion:
            notes = notes[self.inversion:] + [
                note.add_interval(octave) for note in notes[:self.inversion]
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

        # TODO CHECK THAT
        if self.extensions and self.root.octave:
            # print("OK" * 123)
            # first_note = notes[0]
            notes = sorted(notes)  # type: ignore
            # first_note_index = notes.index(first_note)
            # notes = notes[first_note_index:] + notes[:first_note_index]

        return notes

    """
    def get_notes(self):
        intervals_string = chord_index.get_intervals(name or "maj")
        intervals = Interval.parse_list(intervals_string)

        notes = [self.root.add_interval(interval) for interval in intervals]

        if inversion := parsed.get("inversion"):
            notes = notes[inversion:] + [
                note.add_interval(octave) for note in notes[:inversion]
            ]

        base_note = None
        if base_note_parsed := parsed.get("base_note"):
            base_note = Note.build(base_note_parsed)

            if root.octave and not base_note.octave:
                base_note = Note.build(base_note_parsed)

                if notes[0].octave:
                    base_note.octave = notes[0].octave

                    if base_note > notes[0]:
                        base_note.octave -= 1

            notes.insert(0, base_note)

        extensions = []
        if extensions_parsed := parsed.get("extensions"):
            extensions = [
                Interval.build(extension_parsed)
                for extension_parsed in extensions_parsed
            ]
            notes += [root.add_interval(interval) for interval in extensions]

        # Only sort notes when chord root have an octave set
        if extensions and root.octave:
            first_note = notes[0]
            notes = sorted(notes)  # type: ignore
            first_note_index = notes.index(first_note)
            notes = notes[first_note_index:] + notes[:first_note_index]
    """

    @staticmethod
    def chord_product(roots: List[Note], chord_names: List[str]):
        return [
            Chord.parse(f"{str(root)}_{chord_name}")
            for root, chord_name in product(roots, chord_names)
        ]


octave = Interval(name="8")


class Scale(BaseModel):
    tonic: Note
    name: str

    # notes: List[Note] = Field(default_factory=list)
    # intervals: List[Interval] = Field(default_factory=list)

    def __hash__(self):
        return hash(f"{self.tonic}_{self.name}")

    def __str__(self):
        return f"{self.tonic} {self.name}"

    @validator("name")
    def name_must_be_valid(cls, name):
        if scale_index.is_valid(name):
            return name

        raise ValueError(f"Invalid name: {name}")

    @property
    def is_diatonic(self):
        return len(self.notes) == 7

    @classmethod
    def parse(cls, string: str) -> Scale:
        parsed = parser.parse(parser.scale_pattern, string)

        return cls.build(**parsed)

    @staticmethod
    def build(tonic: Union[Dict, Note], name: str) -> Scale:
        return Scale(
            tonic=Note.build(**tonic) if isinstance(tonic, dict) else tonic,
            name=name.replace("_", " ")
        )

    @property
    def intervals(self):
        intervals_string = scale_index.get_intervals(self.name)
        intervals = Interval.parse_list(intervals_string)

        return intervals

    @property
    def notes(self):
        return [self.tonic.add_interval(interval) for interval in self.intervals]

    @staticmethod
    def scale_product(tonics: List[Note], scale_names: List[str]):
        return [
            Scale.parse(f"{str(tonic)}_{scale_name}")
            for tonic, scale_name in product(tonics, scale_names)
        ]

    def get_note_from_degree(self, degree: Degree) -> Note:
        note = deepcopy(self.notes[degree.index])
        note.alteration += degree.alteration

        return note

    def get_diatonic_chords(self) -> List[Chord]:
        chords = []

        two_octave_notes = self.notes + [
            note.add_interval(octave) for note in self.notes
        ]

        for degree_num in range(7):
            root = two_octave_notes[degree_num]

            notes = []
            intervals = []
            for chord_degree in [1, 3, 5, 7]:
                note = two_octave_notes[degree_num + chord_degree - 1]

                notes.append(note)
                intervals.append(root.get_interval(note))

            intervals_str = ",".join([str(i) for i in intervals])

            chord = Chord(
                root=root,
                name=chord_index.get_name_from_intervals(intervals_str),
                notes=notes,
                intervals=intervals,
            )
            chords.append(chord)

        return chords


class Bpm(BaseModel):
    value: int

    @validator("value")
    def value_must_be_within_range(cls, value):
        if 0 < value <= 600:
            return value

        raise ValueError(f"Invalid value: {value}, must be between 0 and 600")

    @classmethod
    def parse(cls, string: str) -> Bpm:
        parsed = parser.parse(parser.bpm_pattern, string)

        return cls.build(**parsed)

    @staticmethod
    def build(value: int) -> Bpm:
        return Bpm(value=value)


class TimeSignature(BaseModel):
    beats_per_bar: int
    beat_unit: int

    @validator("beat_unit")
    def beat_unit_must_be_within_range(cls, beat_unit):
        if 1 <= beat_unit <= 32:
            return beat_unit

        raise ValueError(f"Invalid beat_unit: {beat_unit}, must be in range 1-32")

    @validator("beat_unit")
    def beat_unit_must_be_a_multiple_of_2(cls, beat_unit):
        if beat_unit in (1, 2, 4, 8, 16, 32):
            return beat_unit

        raise ValueError(f"Invalid beat_unit: {beat_unit}, must be a multiple of 2")

    @classmethod
    def parse(cls, string: str) -> TimeSignature:
        parsed = parser.parse(parser.time_signature_pattern, string)

        return cls.build(**parsed)

    @staticmethod
    def build(beats_per_bar: int, beat_unit: int) -> TimeSignature:
        return TimeSignature(beats_per_bar=beats_per_bar, beat_unit=beat_unit)

    def get_duration(self) -> Duration:
        return Duration(value=Fraction(self.beats_per_bar * 4, self.beat_unit))

    def generate_time_sections(
        self, step: Duration
    ) -> Generator[Tuple[TimeSection, Duration], None, None]:
        cursor = Duration(value=Fraction(0))
        reduction = Fraction(self.beat_unit, 4)

        bar = measure = 0
        rest = Fraction(0)

        while True:
            yield TimeSection(bar=bar + 1, measure=measure + 1, rest=rest), cursor

            cursor += step

            bar, measure_rest = divmod(cursor.value * reduction, self.beats_per_bar)
            measure, rest = divmod(measure_rest * reduction, 1)


class Duration(BaseModel):
    value: Fraction

    @validator("value", pre=True)
    def cast_int_to_fraction(cls, value):
        if isinstance(value, int):
            value = Fraction(value)

        return value

    class Config:
        arbitrary_types_allowed = True

    def __hash__(self):
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

    def __mod__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value % other.value)

    def __floordiv__(self, other: object) -> Duration:
        if not isinstance(other, Duration):
            return NotImplemented

        return Duration(value=self.value // other.value)

    @classmethod
    def parse(cls, string: str) -> Duration:
        parsed = parser.parse(parser.duration_pattern, string)

        return cls.build(**parsed)

    @staticmethod
    def build(
        base_duration: Optional[str] = None,
        numerator: Optional[int] = None,
        denominator: Optional[int] = None,
    ) -> Duration:
        if base_duration:
            value = duration.base_values[base_duration]
        else:
            value = Fraction(1)

        if numerator:
            value *= numerator

        if denominator:
            value /= denominator

        return Duration(value=value)


class TimeSection(BaseModel):
    bar: int
    measure: int
    rest: Fraction

    @validator("rest", pre=True)
    def cast_int_to_fraction(cls, rest):
        if isinstance(rest, int):
            rest = Fraction(rest)

        return rest

    class Config:
        arbitrary_types_allowed = True


class GridPart(BaseModel):
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Optional[Duration]


class Grid(BaseModel):
    parts: Sequence[GridPart] = Field(default_factory=list)

    @classmethod
    def parse(cls, string: str) -> Grid:
        parsed = parser.parse(parser.grid_pattern, string)

        return cls.build(**parsed)

    @staticmethod
    def build(grid_sections: List[Dict]) -> Grid:
        parts = []

        bpm = Bpm(value=120)
        time_signature = TimeSignature(beats_per_bar=4, beat_unit=4)
        scale = Scale.parse("C_major")

        for parsed_grid_section in grid_sections:
            if not parsed_grid_section:
                continue

            if parsed_bpm := parsed_grid_section.get("bpm"):
                bpm = Bpm.build(**parsed_bpm)

            if parsed_time_signature := parsed_grid_section.get("time_signature"):
                time_signature = TimeSignature.build(**parsed_time_signature)

            if parsed_scale := parsed_grid_section.get("scale"):
                scale = Scale.build(**parsed_scale)

            parsed_chords = parsed_grid_section.get("chords")

            if not parsed_chords:
                continue

            grid_section_parts = []
            for parsed_chord in parsed_chords:
                chord = Chord.build(scale=scale, **parsed_chord)

                duration = None
                if parsed_duration := parsed_chord.get("duration"):
                    duration = Duration.build(**parsed_duration)

                grid_section_parts.append(
                    GridPart(
                        bpm=bpm,
                        time_signature=time_signature,
                        scale=scale,
                        chord=chord,
                        duration=duration,
                    )
                )

            parts += grid_section_parts * int(parsed_grid_section.get("repeat") or 1)

        return Grid(parts=parts)
