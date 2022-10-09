from typing import Dict, List, Optional

from beethoven.indexes.models import ChordData, IntervalData, NoteData, ScaleData
from beethoven.indexes.notations import (
    ChordNotationEnum,
    IntervalNotationEnum,
    NoteNotationEnum,
)


class NoteIndex:
    directory: Dict[str, NoteData]
    index_directory: Dict[int, NoteData]

    def __init__(self, notes_data) -> None:
        self.directory = {}
        self.index_directory = {}

        for note_data in notes_data:
            for name in note_data.names:
                self.directory[name] = note_data

            self.index_directory[note_data.index] = note_data

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name].names

    def get_index(self, name: str) -> int:
        return self.directory[name].index

    def get_semitones(self, name: str) -> int:
        return self.directory[name].semitones

    def get_name_from_index(
        self, index: int, notation: NoteNotationEnum = NoteNotationEnum.ALPHABETIC
    ) -> str:
        if notation == NoteNotationEnum.ALPHABETIC:
            return self.index_directory[index].alphabetic_name
        else:  # notation == NoteNotationEnum.SYLLABIC:
            return self.index_directory[index].syllabic_name

    def get_note_data_by_name(self, name) -> NoteData:
        return self.directory[name]


class IntervalIndex:
    directory: Dict[str, IntervalData]
    index_directory: Dict[int, IntervalData]

    def __init__(self, intervals_data) -> None:
        self.directory = {}
        self.index_directory = {}

        for interval_data in intervals_data:
            for name in interval_data.names:
                self.directory[name] = interval_data

            self.index_directory[interval_data.index] = interval_data

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name].names

    def get_index(self, name: str) -> int:
        return self.directory[name].index

    def get_semitones(self, name: str) -> int:
        return self.directory[name].semitones

    def get_name_from_index(
        self, index: int, notation: IntervalNotationEnum = IntervalNotationEnum.SHORT
    ) -> str:
        if notation == IntervalNotationEnum.SHORT:
            return self.index_directory[index].short_name
        else:  # notation == IntervalNotationEnum.LONG:
            return self.index_directory[index].long_name


class ChordIndex:
    directory: Dict[str, ChordData]
    interval_directory: Dict[str, ChordData]
    label_directory: Dict[str, List[ChordData]]

    def __init__(self, chords_data) -> None:
        self.directory = {}
        self.interval_directory = {}
        self.label_directory = {}

        for chord_data in chords_data:
            for name in chord_data.names:
                self.directory[name] = chord_data

            self.interval_directory[chord_data.intervals_string] = chord_data

            for label in chord_data.labels:
                if not self.label_directory.get(label):
                    self.label_directory[label] = []

                self.label_directory[label].append(chord_data)

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name].names

    def get_intervals(self, name: str) -> str:
        return self.directory[name].intervals_string

    def get_name_from_intervals(
        self, intervals: str, notation: ChordNotationEnum = ChordNotationEnum.SHORT
    ) -> str:
        if notation == ChordNotationEnum.SHORT:
            return self.interval_directory[intervals].short_name
        elif notation == ChordNotationEnum.FULL:
            return self.interval_directory[intervals].full_name
        else:  # notation == ChordNotationEnum.SYMBOL:
            return self.interval_directory[intervals].symbol

    def get_chords_label_data(self) -> Dict[str, List[ChordData]]:
        return self.label_directory

    def get_chords_by_label_data(
        self, labels: Optional[List[str]] = None
    ) -> List[ChordData]:
        filtered_chords = []

        for label, chords_data in self.label_directory.items():
            if not labels or label in labels:
                filtered_chords += chords_data

        return filtered_chords


class ScaleIndex:
    directory: Dict[str, ScaleData]
    label_directory: Dict[str, List[ScaleData]]

    def __init__(self, scales_data) -> None:
        self.directory = {}
        self.label_directory = {}

        for scale_data in scales_data:
            for name in scale_data.names:
                self.directory[name] = scale_data

            for label in scale_data.labels:
                if not self.label_directory.get(label):
                    self.label_directory[label] = []

                self.label_directory[label].append(scale_data)

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name].names

    def get_intervals(self, name: str) -> str:
        return self.directory[name].intervals_string

    def get_scales_label_data(self) -> Dict[str, List[ScaleData]]:
        return self.label_directory

    def get_scales_by_label_data(
        self, labels: Optional[List[str]] = None
    ) -> List[ScaleData]:
        filtered_scales = []

        for label, scales_data in self.label_directory.items():
            if not labels or label in labels:
                filtered_scales += scales_data

        return filtered_scales


class DegreeIndex:
    directory: List[str]

    def __init__(self, degrees_data) -> None:
        self.directory = degrees_data

    def is_valid(self, name: str) -> bool:
        return name.lower() in self.directory

    def get_name(self, index: int) -> str:
        return self.directory[index]

    def get_index(self, name: str) -> int:
        return self.directory.index(name.lower())
