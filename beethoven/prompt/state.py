from os import environ

from beethoven.common.tuning import Tuning
from beethoven.models import GridPart
from beethoven.players.drum import Drum
from beethoven.players.piano import Piano
from beethoven.sequencer.jam_room import JamRoom
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.scale import Scale

DEFAULT_CONFIG = {
    "scale": Scale("C", "major"),
    "duration": None,
    "tempo": Tempo(60),
    "time_signature": TimeSignature(4, 4)
}

DEFAULT_PROMPT_CONFIG = {
    "strict": True
}


class State:

    def __init__(self, prompt_config=None):
        self.jam_room = JamRoom()

        self.grid_parts = {
            gp.name: gp
            for gp in GridPart.list()
        }

        self.jam_room.players.add(Piano())
        self.jam_room.players.add(Drum())

        self.config = DEFAULT_CONFIG

        self.prompt_config = {**DEFAULT_PROMPT_CONFIG, **(prompt_config or {})}

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()


if environ.get("TEST"):
    state = State()
else:
    state = State(prompt_config={
        "strict": False,
        "fretboards": [
            {
                "tuning": Tuning.from_notes_str("E,A,D,G,B,E"),
                "tonic_color": "white",
                "chord_color": "yellow",
                "diatonic_color": {
                    2: "light_red",
                    3: "light_green",
                    4: "turquoise_2",
                    6: "magenta"
                }
            }
        ]}
    )
