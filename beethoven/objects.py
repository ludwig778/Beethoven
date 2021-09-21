from __future__ import annotations

from dataclasses import dataclass, field, replace
from fractions import Fraction
from typing import Any, Dict, Generator, List, Optional, Sequence, Tuple, Union

from beethoven.core.abstract import AbstractObject
from beethoven.exceptions import (
    BeatsPerBarCantBeZero,
    BeatUnitIsInvalid,
    BpmCantBeZero,
    ChordNameUnknown,
    InversionOutOfRange,
    ScaleIsNotDiatonic,
    ScaleNameUnknown,
    ScaleNotSet,
)
from beethoven.mappings import (
    chord_mapping,
    degree_mapping,
    interval_mapping,
    note_mapping,
    scale_mapping,
)
from beethoven.serializers import deserialize
from beethoven.utils.alterations import (
    get_alteration_as_int,
    get_alteration_from_int,
    get_interval_alteration_as_int,
    get_interval_alteration_from_int,
)
from beethoven.utils.duration import DurationLimit

default_durations = {
    "W": Fraction(4, 1),
    "H": Fraction(2, 1),
    "Q": Fraction(1, 1),
    "E": Fraction(1, 2),
    "S": Fraction(1, 4),
}


@dataclass
class Note:
    name: str
    alteration: int = 0
    octave: Optional[int] = None

    @property
    def index(self):
        semitones = note_mapping.get_semitones(self.name)

        if self.octave:
            return semitones + self.alteration + self.octave * 12

        return (semitones + self.alteration) % 12

    @classmethod
    def parse(cls, value: str) -> Note:
        parsed = deserialize("note", value)

        return cls.build(parsed)

    @classmethod
    def parse_list(cls, value: str) -> List[Note]:
        return [cls.parse(item) for item in value.split(",")]

    @classmethod
    def build(cls, parsed: dict) -> Note:
        name = parsed["name"]

        alteration = get_alteration_as_int(parsed.get("alteration"))

        if octave := parsed.get("octave"):
            octave = int(octave)

        return cls(name=name, alteration=alteration, octave=octave)

    def serialize(self) -> str:
        return (
            self.name
            + get_alteration_from_int(self.alteration)
            + str(self.octave or "")
        )

    @classmethod
    def add_interval(
        cls, note: Note, interval: Interval, reverse: bool = False
    ) -> Note:
        degree_diff = int(interval.name) - 1
        interval_st = (
            interval_mapping.get_semitones(interval.name) + interval.alteration
        )

        if reverse:
            degree_diff *= -1
            interval_st *= -1

        index_base_note = note_mapping.get_index(note.name)
        octave_diff, target_degree = divmod(degree_diff + index_base_note, 7)

        # get the target note name, and get semitones of base and target note
        base_st = note_mapping.get_semitones(note.name)
        dest_note = note_mapping.get_name_from_index(target_degree % 7)
        dest_st = note_mapping.get_semitones(dest_note)

        alteration = (
            base_st + interval_st + note.alteration - dest_st - (12 * octave_diff)
        )

        octave = None
        if note.octave is not None:
            octave = note.octave + octave_diff

        return cls(name=dest_note, alteration=alteration, octave=octave)

    def __add__(self, interval: Interval) -> Note:
        return Note.add_interval(self, interval)

    def __sub__(self, interval: Interval) -> Note:
        return Note.add_interval(self, interval, reverse=True)

    def __truediv__(self, note: Note) -> Interval:
        return Interval.get_notes_interval(self, note)


@dataclass
class Interval:
    name: str
    alteration: int = 0

    @classmethod
    def parse(cls, value: str) -> Interval:
        parsed = deserialize("interval", value)

        return cls.build(parsed)

    @classmethod
    def parse_list(cls, value: str) -> List[Interval]:
        return [cls.parse(item) for item in value.split(",")]

    @classmethod
    def build(cls, parsed: dict) -> Interval:
        name = parsed["name"]

        alteration = 0
        if raw_alteration := parsed.get("alteration"):
            alteration = get_interval_alteration_as_int(name, raw_alteration)

        return Interval(name=name, alteration=alteration)

    def serialize(self) -> str:
        return self.name + get_interval_alteration_from_int(self.name, self.alteration)

    @staticmethod
    def serialize_list(intervals) -> str:
        return ",".join([interval.serialize() for interval in intervals])

    @classmethod
    def get_notes_interval(cls, note1: Note, note2: Note) -> Interval:
        index_1 = note_mapping.get_index(note1.name)
        index_2 = note_mapping.get_index(note2.name)
        index_diff = index_2 - index_1

        semitones_1 = note_mapping.get_semitones(note1.name)
        semitones_2 = note_mapping.get_semitones(note2.name)

        octave_diff = 0
        if note1.octave and note2.octave:
            semitones_1 += note1.octave * 12
            semitones_2 += note2.octave * 12

            semitones_diff = semitones_2 - semitones_1

            octave_diff = note2.octave - note1.octave

            index_diff += octave_diff * 7
        else:
            semitones_diff = (semitones_2 - semitones_1) % 12
            index_diff %= 7

        name = interval_mapping.get_name_from_index(index_diff)
        semitones = interval_mapping.get_semitones(name)
        alteration = semitones_diff - semitones - note1.alteration + note2.alteration

        return cls(name=name, alteration=alteration)


@dataclass
class Degree:
    name: str
    alteration: int = 0

    @classmethod
    def parse(cls, value: str) -> Degree:
        parsed = deserialize("degree", value)

        return cls.build(parsed)

    @classmethod
    def build(cls, parsed: dict) -> Degree:
        name = parsed["name"]

        alteration = 0
        if raw_alteration := parsed.get("alteration"):
            alteration = get_alteration_as_int(raw_alteration)

        return Degree(name=name, alteration=alteration)

    def serialize(self):
        return get_alteration_from_int(self.alteration) + self.name


@dataclass
class Chord:
    root: Note
    name: str

    inversion: Optional[int] = None
    base_note: Optional[Note] = None
    extensions: List[Interval] = field(default_factory=list)

    notes: List[Note] = field(default_factory=list)
    intervals: List[Interval] = field(default_factory=list)

    degree: Optional[Degree] = field(default=None, repr=False)
    base_degree: Optional[Degree] = field(default=None, repr=False)

    @classmethod
    def parse(cls, value: str, **kwargs: Any) -> Chord:
        parsed = deserialize("chord", value)

        return cls.build(parsed, **kwargs)

    @classmethod
    def build(cls, parsed: dict, scale: Optional["Scale"] = None) -> Chord:
        if name := parsed.get("name"):
            name = name.replace("_", " ")

        degree = None
        base_degree = None
        if raw_degree := parsed.get("degree"):
            if not scale:
                raise ScaleNotSet("Scale must be set when using degree on chord")

            if not scale.is_diatonic:
                raise ScaleIsNotDiatonic(scale)

            root, degree, degree_index, base_degree = cls._parse_degrees(
                raw_degree, parsed.get("base_degree"), scale
            )

            if not name:
                name = scale.get_chords()[degree_index].name

        elif raw_root := parsed.get("root"):
            root = Note.build(raw_root)

        if not name:
            name = "maj"

        if raw_intervals := chord_mapping.get_intervals(name):
            intervals = Interval.parse_list(raw_intervals)
        else:
            raise ChordNameUnknown(name)

        notes = [root + interval for interval in intervals]

        if inversion := parsed.get("inversion"):
            notes = cls._apply_inversion(inversion, notes)

        if extensions := parsed.get("extensions"):
            extensions = Interval.parse_list(extensions)

            for extension in extensions:
                notes.append(root + extension)

        base_note = None
        if raw_base_note := parsed.get("base_note"):
            base_note = cls._parse_base_note(raw_base_note, notes[0])

            notes.insert(0, base_note)

        return cls(
            root=root,
            name=name,
            inversion=inversion,
            extensions=extensions,
            base_note=base_note,
            notes=notes,
            intervals=intervals,
            degree=degree,
            base_degree=base_degree,
        )

    @staticmethod
    def _parse_degrees(raw_degree, raw_base_degree, scale):
        degree = Degree.build(raw_degree)
        degree_index = degree_mapping.get_index(degree.name)
        degree_alteration = degree.alteration
        diatonic_degree_index = degree_index

        base_degree = None
        if raw_base_degree:
            base_degree = Degree.build(raw_base_degree)
            base_degree_index = degree_mapping.get_index(base_degree.name)

            diatonic_degree_index = degree_index + base_degree_index
            degree_alteration += base_degree.alteration

        add_octave = False
        if diatonic_degree_index >= 7:
            diatonic_degree_index %= 7
            add_octave = True

        root = scale.notes[diatonic_degree_index]

        if add_octave:
            root += Interval.parse("8")

        if degree_alteration:
            root = replace(root, alteration=root.alteration + degree_alteration)

        return root, degree, degree_index, base_degree

    @staticmethod
    def _apply_inversion(inversion: int, notes: List[Note]) -> List[Note]:
        if inversion == 0:
            return notes
        elif inversion < 0 or inversion > len(notes) - 1:
            raise InversionOutOfRange()

        octave = Interval.parse("8")

        return notes[inversion:] + [note + octave for note in notes[:inversion]]

    @staticmethod
    def _parse_base_note(raw_base_note: dict, first_note: Note) -> Note:
        base_note = Note.build(raw_base_note)

        if first_note.octave:

            base_note_octave = base_note.octave
            if not base_note_octave:
                base_note_octave = first_note.octave

            if base_note_octave > first_note.octave:
                base_note_octave = first_note.octave

            if base_note_octave == first_note.octave and (
                note_mapping.get_index(first_note.name)
                < note_mapping.get_index(base_note.name)
            ):
                base_note_octave -= 1

            base_note = replace(base_note, octave=base_note_octave)

        return base_note

    def serialize(self):
        string = ""

        if self.degree:
            string += self.degree.serialize()
        else:
            string += self.root.serialize()

        string += "_" + self.name

        if self.inversion:
            string += ":i=" + str(self.inversion)

        if self.base_note:
            string += ":b=" + self.base_note.serialize()

        if self.base_degree:
            string += ":s=" + self.base_degree.serialize()

        if self.extensions:
            string += ":e=" + Interval.serialize_list(self.extensions)

        return string

    @classmethod
    def serialize_list(cls, chords):
        return ",".join([chord.serialize() for chord in chords])


@dataclass
class Scale:
    tonic: "Note"
    name: str

    notes: List["Note"] = field(default_factory=list)
    intervals: List["Interval"] = field(default_factory=list)

    @classmethod
    def parse(cls, value: str) -> Scale:
        parsed = deserialize("scale", value)

        return cls.build(parsed)

    @classmethod
    def build(cls, parsed: Dict) -> Scale:
        raw_tonic = parsed["tonic"]

        tonic = Note.build(raw_tonic)

        if name := parsed.get("name"):
            name = name.replace("_", " ").strip()
        else:
            name = "ionian"

        if raw_intervals := scale_mapping.get_intervals(name):
            intervals = Interval.parse_list(raw_intervals)
        else:
            raise ScaleNameUnknown(name)

        notes = [tonic + interval for interval in intervals]

        return cls(tonic=tonic, name=name, notes=notes, intervals=intervals)

    def get_chords(self, degrees: List[int] = None) -> List["Chord"]:
        if not self.is_diatonic:
            raise ScaleIsNotDiatonic(self)

        degrees = degrees or [1, 3, 5, 7]
        has_octave = bool(self.tonic.octave)

        scale_notes = self.notes
        if has_octave:
            scale_notes = [replace(note, octave=None) for note in scale_notes]

        chords = []
        for i in range(7):
            notes = [scale_notes[(degree + i - 1) % 7] for degree in degrees]
            intervals = [notes[0] / note for note in notes]

            intervals_str = Interval.serialize_list(intervals)
            chord_name = chord_mapping.get_name_from_intervals(intervals_str)

            chord = Chord.parse(self.notes[i].serialize() + "_" + chord_name)
            chords.append(chord)

        return chords

    @property
    def is_diatonic(self) -> bool:
        return len(self.notes) == 7

    def serialize(self):
        return f"{self.tonic.serialize()}_{self.name}"


@dataclass
class Bpm(AbstractObject):
    value: int

    @classmethod
    def parse(cls, value: str) -> "Bpm":
        parsed = deserialize("bpm", value)

        return cls.build(parsed)

    @classmethod
    def build(cls, parsed: dict) -> "Bpm":
        value = parsed.get("value")

        if not value:
            raise BpmCantBeZero()

        return cls(value=value)

    def serialize(self):
        return str(self.value)

    @property
    def base_time(self) -> Fraction:
        return Duration(Fraction(60, self.value))


@dataclass
class TimeSignature:
    beats_per_bar: int
    beat_unit: int

    @classmethod
    def parse(cls, value: str) -> TimeSignature:
        parsed = deserialize("time_signature", value)

        return cls.build(parsed)

    @classmethod
    def build(cls, parsed: dict) -> TimeSignature:
        beats_per_bar = parsed.get("beats_per_bar", 4)
        beat_unit = parsed.get("beat_unit", 4)

        if beat_unit not in (1, 2, 4, 8, 16, 32):
            raise BeatUnitIsInvalid(beat_unit)
        elif beats_per_bar == 0:
            raise BeatsPerBarCantBeZero(beats_per_bar)

        return cls(beats_per_bar=beats_per_bar, beat_unit=beat_unit)

    def serialize(self) -> str:
        return f"{self.beats_per_bar}/{self.beat_unit}"

    @property
    def as_duration(self) -> Duration:
        reduction = Fraction(self.beat_unit, 4)

        return Duration(Fraction(self.beats_per_bar, reduction))

    def get_time_section(self, timeline: Fraction) -> TimeSection:
        reduction = Fraction(self.beat_unit, 4)

        bar, raw_measure = divmod(timeline, self.as_duration.value)
        measure, fraction = divmod(raw_measure * reduction, 1)

        return TimeSection(bar=bar + 1, measure=measure + 1, fraction=fraction)

    def time_section_generator(
        self,
        duration: Duration,
        limit: Union[Duration, DurationLimit] = DurationLimit.TimeSignatureBound,
    ) -> Generator[Tuple[TimeSection, Duration], None, None]:

        self_duration = self.as_duration

        if limit is DurationLimit.NoLimit:
            _limit = None
        elif limit is DurationLimit.TimeSignatureBound:
            _limit = self_duration
        else:
            _limit = limit

        timeline = Fraction(0)
        while 1:
            next_timeline = timeline + duration.value

            if _limit and next_timeline >= _limit.value:
                duration = Duration(_limit.value - timeline)

                yield self.get_time_section(timeline), duration
                break

            yield self.get_time_section(timeline), duration

            timeline = next_timeline


@dataclass
class TimeSection:
    bar: int
    measure: int
    fraction: Fraction = Fraction()

    def as_duration(self, time_signature: TimeSignature) -> Duration:
        total = Fraction()
        reduction = Fraction(time_signature.beat_unit, 4)
        time_signature_duration = time_signature.as_duration

        if self.bar > 1:
            total += time_signature_duration.value * (self.bar - 1)

        if self.measure > 1:
            total += (self.measure - 1) / reduction

        if self.fraction:
            total += self.fraction

        return Duration(total)


@dataclass(order=True)
class Duration:
    value: Fraction

    def __init__(self, value: Union[Fraction, int]):
        if isinstance(value, int):
            value = Fraction(value)

        self.value = value

    @classmethod
    def parse(cls, value: str) -> Duration:
        parsed = deserialize("duration", value)

        return cls.build(parsed)

    @classmethod
    def build(cls, parsed: dict) -> Duration:
        numerator = parsed.get("numerator", 1)
        denominator = parsed.get("denominator")

        if denominator == 0:
            raise Exception("Duration denominator can't be equal to 0")

        value = Fraction(numerator=numerator, denominator=denominator)

        if base_duration := parsed.get("base_duration"):
            if duration := default_durations.get(base_duration):
                value *= duration
            else:
                raise Exception(
                    f"Duration base_duration {base_duration} couldn't be found"
                )

        return cls(value=value)

    def __add__(self, other):
        return replace(self, value=self.value + other.value)

    def __sub__(self, other):
        return replace(self, value=self.value - other.value)

    def __mul__(self, other):
        return replace(self, value=self.value * other.value)

    def __mod__(self, other):
        return replace(self, value=self.value % other.value)


@dataclass
class GridPart:
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Optional[Duration]

    def __iter__(self) -> Generator[GridPart, None, None]:
        yield self


@dataclass
class Grid:
    parts: Sequence[Union[Grid, GridPart]] = field(default_factory=list)

    def __iter__(self) -> Generator[Union[GridPart], None, None]:
        for part in self.parts:
            yield from part

    @classmethod
    def parse(cls, value: str, default_settings: Optional[dict] = None) -> Grid:
        parsed = deserialize("grid", value)

        return cls.build(parsed, default_settings=default_settings)

    @classmethod
    def build(cls, parsed: dict, default_settings: Optional[dict] = None) -> Grid:  # noqa: C901
        scale = None
        bpm = None
        time_signature = None
        duration = None
        chords: List[Tuple[Chord, Optional[Duration]]] = []

        last_time_signature = None
        time_signature_total_duration = Duration.parse("0")

        if default_settings:
            scale = default_settings.get("scale", scale)
            bpm = default_settings.get("bpm", bpm)
            time_signature = default_settings.get("time_signature", time_signature)
            duration = default_settings.get("duration", duration)
            chords = default_settings.get("chords", chords)

        parts = []
        for grid_part in parsed.get("grid_parts") or []:

            if data := grid_part.get("scale") or {}:
                scale = Scale.build(data)

            if data := grid_part.get("bpm"):
                bpm = Bpm.build(data)

            if data := grid_part.get("time_signature"):
                time_signature = TimeSignature.build(data)

            if data := grid_part.get("duration"):
                duration = Duration.build(data)

            if data := grid_part.get("chords"):
                chords = []

                for chord_data in data:
                    chord = Chord.build(chord_data, scale=scale)

                    duration = None
                    if duration_data := chord_data.pop("duration", None):
                        duration = Duration.build(duration_data)

                    chords.append((chord, duration))

            if not bpm:
                raise Exception("Bpm must be set")

            if not time_signature:
                raise Exception("TimeSignature must be set")

            if not scale:
                raise Exception("Scale must be set")

            if last_time_signature != time_signature:
                time_signature_total_duration = Duration.parse("0")

            repeat = grid_part.get("repeat", 1)

            for _ in range(repeat):

                for chord, chord_duration in chords:

                    part_duration = chord_duration or duration
                    if not part_duration:
                        if time_signature_total_duration.value:
                            part_duration = (
                                time_signature.as_duration - (
                                    time_signature_total_duration % time_signature.as_duration
                                )
                            )
                        else:
                            part_duration = time_signature.as_duration

                    parts.append(
                        GridPart(
                            scale=scale,
                            chord=chord,
                            bpm=bpm,
                            time_signature=time_signature,
                            duration=part_duration
                        )
                    )

                    time_signature_total_duration += part_duration

        return cls(parts)
