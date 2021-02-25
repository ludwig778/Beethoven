from beethoven.sequencer.utils import get_all_notes


class Arpeggiator:

    def __init__(self, player):
        self.player = player

        self.last_note = None
        self.setup()

    def setup(self, notes=None, **kwargs):
        self.notes = notes or []

    def arpeggiator(self):
        return self._arpeggio_next()

    get = arpeggiator

    def _arpeggio_next(self):
        return get_all_notes(
            self.player.scale,
            self.player.NOTE_RANGE
        )
