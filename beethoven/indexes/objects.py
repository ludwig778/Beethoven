from typing import Dict, List, Tuple


class NoteIndex:
    directory: Dict[str, Tuple[List[str], int, int]]
    index_directory: Dict[int, str]

    def __init__(self, note_mappings) -> None:
        self.directory = {}
        self.index_directory = {}

        for index, semitones, *names in note_mappings:
            name_container = list(names)

            for name in names:
                self.directory[name] = (name_container, index, semitones)

            self.index_directory[index] = names[0]

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name][0]

    def get_index(self, name: str) -> int:
        return self.directory[name][1]

    def get_semitones(self, name: str) -> int:
        return self.directory[name][2]

    def get_name_from_index(self, index: int) -> str:
        return self.index_directory[index]


class IntervalIndex:
    directory: Dict[str, Tuple[List[str], int, int]]
    reverse_directory: Dict[int, str]

    def __init__(self, interval_mappings) -> None:
        self.directory = {}
        self.reverse_directory = {}

        for index, semitones, *names in interval_mappings:
            name_container = list(names)

            for name in names:
                self.directory[name] = (name_container, index, semitones)

            self.reverse_directory[index] = names[0]

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name][0]

    def get_index(self, name: str) -> int:
        return self.directory[name][1]

    def get_semitones(self, name: str) -> int:
        return self.directory[name][2]

    def get_name_from_index(self, index: int) -> str:
        return self.reverse_directory[index]


class ChordIndex:
    directory: Dict[str, Tuple[List[str], str]]
    reverse_directory: Dict[str, str]

    def __init__(self, chord_mappings) -> None:
        self.directory = {}
        self.reverse_directory = {}

        for intervals, *names in chord_mappings:
            name_container = list(names)

            for name in names:
                self.directory[name] = (name_container, intervals)

            self.reverse_directory[intervals] = names[0]

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name][0]

    def get_intervals(self, name: str) -> str:
        return self.directory[name][1]

    def get_name_from_intervals(self, intervals: str) -> str:
        return self.reverse_directory[intervals]


class ScaleIndex:
    directory: Dict[str, Tuple[List[str], str]]
    modes_directory: Dict[str, List[str]]

    def __init__(self, scale_mappings) -> None:
        self.directory = {}
        self.modes_directory = {}

        for intervals, mode, *names in scale_mappings:
            name_container = list(names)

            for name in names:
                self.directory[name] = (name_container, intervals)

            if mode:
                if not self.modes_directory.get(mode):
                    self.modes_directory[mode] = []

                self.modes_directory[mode].append(names[0])

    def is_valid(self, name: str) -> bool:
        return name in self.directory

    def get_names(self, name: str) -> List[str]:
        return self.directory[name][0]

    def get_intervals(self, name: str) -> str:
        return self.directory[name][1]


class DegreeIndex:
    directory: List[str]

    def __init__(self, degree_mappings) -> None:
        self.directory = degree_mappings

    def is_valid(self, name: str) -> bool:
        return name.lower() in self.directory

    def get_name(self, index: int) -> str:
        return self.directory[index]

    def get_index(self, name: str) -> int:
        return self.directory.index(name.lower())
