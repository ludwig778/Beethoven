from typing import List, Protocol

from beethoven.models import GridPart, Note

GridParts = List[GridPart]


class NotesContainer(Protocol):
    notes: List[Note]

    def __hash__(self):
        ...
