from typing import List, Protocol, Tuple

from beethoven.models import ChordItem, HarmonyItem, Note


class NotesContainer(Protocol):
    notes: List[Note]

    def __hash__(self) -> int:
        ...


SequencerItems = Tuple[HarmonyItem, ChordItem]
