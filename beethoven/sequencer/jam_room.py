from beethoven.repository.midi import midi
from beethoven.sequencer.players.base import Players


class JamRoom:
    def __init__(self, grid=None, players=None, **kwargs):
        self.grid = grid
        self.players = Players(*(players or []))

    def play(self, callback=None, **kwargs):
        for grid_part_index in midi.play(self.grid, self.players, **kwargs):

            if callback:
                callback(grid_part_index)
