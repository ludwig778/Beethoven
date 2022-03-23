from typing import Dict

from beethoven.adapters.midi import Output
from beethoven.models import Duration, GridPart
from beethoven.sequencer.players.meta import PlayerRegistry


class BasePlayer(metaclass=PlayerRegistry):
    time_signature_bound: bool = False

    def __init__(self, output: Output, channel: int):
        self.output = output
        self.channel = channel

    def setup(self, grid_part: GridPart):
        self.grid_part = grid_part

    def play_note(
        self, note_index: int, duration: Duration, velocity: int = 127
    ) -> Dict:
        return {"note": note_index, "velocity": velocity, "duration": duration}


class PercussionPlayer(BasePlayer):
    time_signature_bound: bool = True

    def __init__(self, *args, time_signature_bound: bool = False, **kwargs):
        super().__init__(*args, **kwargs)

        if time_signature_bound:
            self.time_signature_bound: bool = True
