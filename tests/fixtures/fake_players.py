from beethoven.sequencer.note import Note
from beethoven.sequencer.note_duration import Half, Whole
from beethoven.sequencer.players.base import BasePlayer


class FakePlayer1(BasePlayer):
    NOTE_DURATION = Whole
    NOTE_RANGE = [Note("C3"), Note("C5")]

    def play_measure(self, **kwargs):
        for self.part in self.time_signature.generator(self.NOTE_DURATION):
            yield self.play(
                *self.chord_voicer.get()[0:2],
                duration=Whole,
                velocity=127
            )


class FakePlayer2(BasePlayer):
    NOTE_DURATION = Half
    NOTE_RANGE = [Note("D3"), Note("C5")]

    def play_measure(self, **kwargs):
        for self.part in self.time_signature.generator(self.NOTE_DURATION):
            yield self.play(
                self.arpeggiator.get()[0],
                duration=Half,
                velocity=63
            )
