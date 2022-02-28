from __future__ import annotations

from pydantic import BaseModel

from beethoven.models.bpm import Bpm
from beethoven.models.chord import Chord
from beethoven.models.duration import Duration
from beethoven.models.scale import Scale
from beethoven.models.time_signature import TimeSignature


class GridPart(BaseModel):
    scale: Scale
    chord: Chord

    bpm: Bpm
    time_signature: TimeSignature
    duration: Duration
