from beethoven.repository.midi import midi
from beethoven.sequencer.players.base import Players


class JamRoom:
    def __init__(self, grid=None, players=None, **kwargs):
        self.grid = grid
        self.players = Players(*(players or []))

    def play(self, **kwargs):
        return midi.play(self.grid, self.players, **kwargs)
