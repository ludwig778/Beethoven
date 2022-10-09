from enum import Enum, auto
from functools import lru_cache
from typing import Dict, List

from beethoven.helpers.note import remove_notes_octave
from beethoven.models import Note, Notes
from beethoven.types import NotesContainer


class NoteCheckerType(Enum):
    BY_MIDI_INDEX = auto()
    BY_BASE_NOTE = auto()


class NotesContainerChecker:
    def __init__(
        self,
        *args,
        notes_containers: List[NotesContainer],
        type_check: NoteCheckerType,
        **kwargs
    ):
        self.i = 0
        self.type_check = type_check
        self.notes_containers = notes_containers
        self.done = False

    @staticmethod
    @lru_cache
    def to_base_notes(notes_container: NotesContainer) -> Notes:
        return Notes(notes=remove_notes_octave(sorted(notes_container.notes)))

    @staticmethod
    @lru_cache
    def to_midi_index(notes_container: NotesContainer) -> List[int]:
        return [note.midi_index for note in notes_container.notes]

    @property
    def current(self) -> NotesContainer:
        return self.notes_containers[self.i]

    def check(self, indexed_notes: Dict[int, Note]) -> bool:
        if self.done:
            return False

        if self.type_check == NoteCheckerType.BY_BASE_NOTE:
            notes = Notes(notes=list(indexed_notes.values()))

            if self.to_midi_index(self.to_base_notes(notes)) != self.to_midi_index(
                self.current
            ):
                return False

        elif self.type_check == NoteCheckerType.BY_MIDI_INDEX:
            return False
        else:
            return False

        if self.i >= len(self.notes_containers) - 1:
            self.done = True
        else:
            self.i += 1

        return True
