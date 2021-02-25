from beethoven.players.mappings import metronome_mapping
from beethoven.sequencer.note_duration import Eighths
from beethoven.sequencer.players.base import BasePlayer


class Metronome(BasePlayer):
    CACHED = True
    MAPPING = metronome_mapping
    NOTE_DURATION = Eighths

    def play_measure(self, **kwargs):
        for part in self.time_signature.gen(self.NOTE_DURATION, self.duration):
            if part.check(measure=1, submeasure=1, divisor_index=1):
                yield self.play(part, "TICK")

            elif part.check(submeasure=1, divisor_index=1):
                yield self.play(part, "ALT_TICK")

            else:
                yield self.play(part, "OFF_TICK")
