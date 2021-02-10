from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.players.mappings import metronome_mapping
from beethoven.sequencer.note_duration import Eighths
from beethoven.sequencer.note_duration import Whole, Quarter
from beethoven.sequencer.note_duration import *


class Metronome(BasePlayer):
    MAPPING = metronome_mapping
    NOTE_DURATION = Eighths

    def play_measure(self, **kwargs):
        print("GENERATING METRONOME")
        print(self.time_signature)
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            print(part)
            if part.check(1, 1, 1):
                yield self.play(part, "TICK")

            elif part.check(None, 1, 1):
                yield self.play(part, "ALT_TICK")

            else:
                yield self.play(part, "OFF_TICK")