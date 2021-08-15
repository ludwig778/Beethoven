from typing import Dict, List, Tuple

from beethoven.core.mappings import (chord_mappings, degree_mappings,
                                     interval_mappings, note_mappings,
                                     scale_mappings)
from beethoven.utils.deepget import deepget
from beethoven.utils.name_container import NameContainer


class ChordMapping:
    directory: Dict[str, Tuple[NameContainer, str]]
    reverse_directory: Dict[str, str]

    def __init__(self) -> None:
        self.directory = {}
        self.reverse_directory = {}

        for intervals, *names in chord_mappings:
            name_container = NameContainer(names)

            for name in names:
                self.directory[name] = (name_container, intervals)

            self.reverse_directory[intervals] = names[0]

    def get_names(self, name: str) -> NameContainer:
        return deepget(self.directory, f"{name}.0")

    def get_intervals(self, name: str) -> str:
        return deepget(self.directory, f"{name}.1")

    def get_name_from_intervals(self, intervals: str) -> str:
        name = self.reverse_directory.get(intervals)

        if not name:
            raise Exception(f"Chord intervals lookup unknown {intervals=}")

        return name


class DegreeMapping:
    directory: List[str]

    def __init__(self) -> None:
        self.directory = degree_mappings

    def get_name(self, index: int) -> str:
        return self.directory[index]

    def get_index(self, name: str) -> int:
        return self.directory.index(name.lower())


class IntervalMapping:
    directory: Dict[str, Tuple[NameContainer, int, int]]
    reverse_directory: Dict[int, str]

    def __init__(self) -> None:
        self.directory = {}
        self.reverse_directory = {}

        for index, semitones, *names in interval_mappings:
            name_container = NameContainer(names)

            for name in names:
                self.directory[name] = (name_container, index, semitones)

            self.reverse_directory[index] = names[0]

    def get_names(self, name: str) -> NameContainer:
        return deepget(self.directory, f"{name}.0")

    def get_index(self, name: str) -> int:
        return deepget(self.directory, f"{name}.1")

    def get_semitones(self, name: str) -> int:
        return deepget(self.directory, f"{name}.2")

    def get_name_from_index(self, index: int) -> str:
        name = self.reverse_directory.get(index)

        if not name:
            raise Exception(f"Interval index lookup unknown {index=}")

        return name


class NoteMapping:
    directory: Dict[str, Tuple[NameContainer, int, int]]
    index_directory: Dict[int, str]

    def __init__(self) -> None:
        self.directory = {}
        self.index_directory = {}

        for index, semitones, *names in note_mappings:
            name_container = NameContainer(names)

            for name in names:
                self.directory[name] = (name_container, index, semitones)

            self.index_directory[index] = names[0]

    def get_names(self, name: str) -> NameContainer:
        return deepget(self.directory, f"{name}.0")

    def get_index(self, name: str) -> int:
        return deepget(self.directory, f"{name}.1")

    def get_semitones(self, name: str) -> int:
        return deepget(self.directory, f"{name}.2")

    def get_name_from_index(self, index: int) -> str:
        name = self.index_directory.get(index)

        if not name:
            raise Exception(f"Note index lookup unknown {index=}")

        return name


class ScaleMapping:
    directory: Dict[str, Tuple[NameContainer, str]]
    modes_directory: Dict[str, List[str]]

    def __init__(self) -> None:
        self.directory = {}
        self.modes_directory = {}

        for intervals, mode, *names in scale_mappings:
            name_container = NameContainer(names)

            for name in names:
                self.directory[name] = (name_container, intervals)

            if mode:
                if not self.modes_directory.get(mode):
                    self.modes_directory[mode] = []

                self.modes_directory[mode].append(names[0])

    def get_names(self, name: str) -> NameContainer:
        return deepget(self.directory, f"{name}.0")

    def get_intervals(self, name: str) -> str:
        return deepget(self.directory, f"{name}.1")


note_mapping = NoteMapping()
interval_mapping = IntervalMapping()
chord_mapping = ChordMapping()
scale_mapping = ScaleMapping()
degree_mapping = DegreeMapping()
