from pydantic import BaseModel

from beethoven.adapters.midi import MidiAdapter


class Adapters(BaseModel):
    midi: MidiAdapter

    class Config:
        arbitrary_types_allowed = True
