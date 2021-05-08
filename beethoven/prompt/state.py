from beethoven.common.tuning import Tuning
from beethoven.players.drum import Drum
from beethoven.players.piano import Piano
from beethoven.sequencer.jam_room import JamRoom
from beethoven.sequencer.note_duration import Whole
from beethoven.sequencer.tempo import Tempo
from beethoven.sequencer.time_signature import TimeSignature
from beethoven.theory.scale import Scale


class State:
    DEFAULT_CONFIG = {
        "scale": Scale("C", "major"),
        "duration": Whole,
        "tempo": Tempo(60),
        "time_signature": TimeSignature(4, 4)
    }

    def __init__(self):
        self.jam_room = JamRoom()

        self.jam_room.players.add(Piano())
        self.jam_room.players.add(Drum())

        self.config = self.DEFAULT_CONFIG

        self.display_config = {
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
            ]
        }

    def load(self):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()


state = State()
