from beethoven.sequencer.note import Note
from beethoven.sequencer.note_duration import Sixteenths, Whole
from beethoven.sequencer.players.base import BasePlayer


class Piano(BasePlayer):
    NOTE_DURATION = Sixteenths
    NOTE_RANGE = [Note("C2"), Note("C5")]
    NORMALIZE_TS = True

    def play_measure(self, **kwargs):
        for self.part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            if self.check(bar=1, measure=1, submeasure=1):
                yield self.play(
                    *self.chord_voicer.get(),
                    duration=Whole,
                    velocity=76
                )
