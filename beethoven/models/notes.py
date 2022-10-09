from typing import List, Optional, Union

from pydantic import BaseModel

from beethoven.models.chord import Chord
from beethoven.models.note import Note
from beethoven.models.scale import Scale


class Notes(BaseModel):
    notes: List[Note]
    object: Optional[Union[Scale, Chord]]

    def __hash__(self):
        return hash("_".join(map(str, self.notes)))
