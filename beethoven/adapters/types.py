from dataclasses import dataclass

from beethoven.adapters.midi import MidiAdapter


@dataclass
class Adapters:
    midi: MidiAdapter

    # class Config:
    #     arbitrary_types_allowed = True
