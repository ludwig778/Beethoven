from dataclasses import dataclass, field
from typing import List, Optional

from beethoven.sequencer.note_duration import NoteDuration
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.scale import Scale
from beethoven.theory.chord import Chord


@dataclass
class GridPart:
    scale: Scale
    chord: Chord
    time_signature: TimeSignature
    tempo: Tempo
    duration: Optional[NoteDuration] = None

    repeat: int = 1
    bypass: bool = False


@dataclass
class Grid:
    parts: List[GridPart] = field(default_factory=list)
