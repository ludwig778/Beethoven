from beethoven.players.mappings import drum_mapping
from beethoven.sequencer.note_duration import OneShot, Sixteenths
from beethoven.sequencer.players.base import BasePlayer


class Drum(BasePlayer):
    CACHED = True
    MAPPING = drum_mapping
    NOTE_DURATION = Sixteenths
    NORMALIZE_TS = True

    def play_measure(self, **kwargs):
        for self.part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            if self.check(measure=(1, 2, 5), submeasure=1):
                yield self.play("KICK", duration=OneShot, velocity=55)

            if self.check(measure=(2, 4, 6), submeasure=1):
                yield self.play("SNARE", duration=OneShot)

            if self.check(measure=4, submeasure=4):
                yield self.play("OPEN_HH", duration=OneShot)
            else:
                yield self.play("CLOSE_HH", duration=OneShot)
