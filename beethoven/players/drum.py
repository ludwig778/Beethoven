from beethoven.players.mappings import drum_mapping
from beethoven.sequencer.note_duration import OneShot, Sixteenths
from beethoven.sequencer.players.base import BasePlayer


class Drum(BasePlayer):
    CACHED = True
    MAPPING = drum_mapping
    NOTE_DURATION = Sixteenths

    def play_measure(self, **kwargs):
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            if part.check((1, 3), 1, 1):
                yield self.play(part, "KICK", duration=OneShot, velocity=55)
            if part.check(4, 4, 1):
                yield self.play(part, "KICK", duration=OneShot, velocity=55)
            if part.check((1, 3), 2):
                yield self.play(part, "KICK", duration=OneShot, velocity=55)
            if part.check((2, 4), 1, 1):
                yield self.play(part, "SNARE", duration=OneShot)

            if part.check(4, 4):
                yield self.play(part, "OPEN_HH", duration=OneShot)
            else:
                yield self.play(part, "CLOSE_HH", duration=OneShot)
