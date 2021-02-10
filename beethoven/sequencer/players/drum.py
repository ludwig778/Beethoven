from beethoven.sequencer.players.base import BasePlayer
from beethoven.sequencer.players.mappings import drum_mapping
from beethoven.sequencer.note_duration import Eighths
from beethoven.sequencer.note_duration import Whole, Quarter
from beethoven.sequencer.note_duration import *


class Drum(BasePlayer):
    MAPPING = drum_mapping
    NOTE_DURATION = Sixteenths

    def play_measure(self, **kwargs):
        print("GENERATING DRUM")
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            """
            print(part)
            if part.check(1, 1, 1):
                yield self.play(part, "KICK", duration=OneShot, velocity=55)
            if part.check(4, 4, 4):
                yield self.play(part, "KICK", duration=OneShot, velocity=55)
            if part.check((2, 4), 1, 1):
                yield self.play(part, "SNARE")

            if part.check(4, 4):
                yield self.play(part, "OPEN_HH")
            #else:
            """
            yield self.play(part, "CLOSE_HH", duration=OneShot)


