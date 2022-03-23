from typing import List, Protocol, runtime_checkable

from beethoven.models import GridPart


class NotesContainer(Protocol):
    @property
    def notes(self):
        ...


@runtime_checkable
class Player(Protocol):
    time_signature_bound: bool

    def setup(self, grid_part: GridPart):
        ...

    def play(self):
        ...


GridParts = List[GridPart]
