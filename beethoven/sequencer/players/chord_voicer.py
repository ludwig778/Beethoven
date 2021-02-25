from beethoven.sequencer.utils import adapt_chord_to_sequencer


class ChordVoicer:

    def __init__(self, player):
        self.player = player

        self.setup()

    def setup(self, notes=None, **kwargs):
        self.notes = notes or []

    def chord_voicer(self):
        return self._chord_voicing_next()

    get = chord_voicer

    def _chord_voicing_next(self):
        return adapt_chord_to_sequencer(
            self.player.chord,
            self.player.NOTE_RANGE
        )
