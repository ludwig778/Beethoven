from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.players.mappings import drum_mapping
from beethoven.sequencer.note_duration import Eighths
from beethoven.sequencer.note_duration import Whole, Quarter
from beethoven.sequencer.note_duration import *


class Piano(BasePlayer):
    NOTE_DURATION = Sixteenths

    def play_measure(self, **kwargs):
        print("GENERATING PIANO")
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            #yield self.play(part, *self.chord.notes, velocity=76)

            if part.check(1, 1):
                yield self.play(part, *self.chord.notes, duration=Whole, velocity=76)


