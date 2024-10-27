from enum import Enum, auto
from typing import List

from beethoven.models import Note
from beethoven.types import NotesContainer


class NoteCheckerType(Enum):
    BY_MIDI_INDEX = auto()
    BY_BASE_NOTE = auto()


class NotesContainerChecker:
    def __init__(self, notes_containers: List[NotesContainer], type_check: NoteCheckerType):
        self.i = 0
        self.type_check = type_check
        self.notes_containers = notes_containers
        self.done = False

    @staticmethod
    def to_base_notes(notes: List[Note]) -> List[Note]:
        return Note.remove_notes_octave(notes)

    @staticmethod
    def to_midi_index(notes: List[Note]) -> List[int]:
        return [note.midi_index for note in notes]

    @property
    def current(self) -> NotesContainer:
        return self.notes_containers[self.i]

    def check(self, notes_container: NotesContainer) -> bool:
        if self.done:
            return False

        if self.type_check == NoteCheckerType.BY_BASE_NOTE:
            print(notes_container)
            print([
                self.to_midi_index(self.to_base_notes(notes_container.values())),
                self.to_midi_index(self.to_base_notes(self.current.notes))
            ])
            print(self.to_base_notes(notes_container.values()))
            print(self.current.notes)
            print()
            if (
                sorted(self.to_midi_index(self.to_base_notes(notes_container.values()))) !=
                sorted(self.to_midi_index(self.to_base_notes(self.current.notes)))
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
