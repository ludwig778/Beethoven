from typing import List, Protocol

from beethoven.models import GridPart


class NotesContainer(Protocol):
    @property
    def notes(self):
        ...

    def __hash__(self):
        return hash(":".join([str(hash(note)) for note in self.notes]))


GridParts = List[GridPart]
