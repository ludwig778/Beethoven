from typing import Protocol


class NotesContainer(Protocol):
    @property
    def notes(self):
        ...
