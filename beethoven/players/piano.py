from beethoven.sequencer.note import Note
from beethoven.sequencer.note_duration import Sixteenths, Whole
from beethoven.sequencer.players.base import BasePlayer


class Piano(BasePlayer):
    NOTE_DURATION = Sixteenths
    NOTE_RANGE = [Note("C2"), Note("C5")]

    def play_measure(self, **kwargs):
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            if part.check(bar=1, measure=1, submeasure=1):
                yield self.play(
                    part,
                    *self.chord_voicer,
                    duration=Whole,
                    velocity=76
                )
