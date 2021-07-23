from dataclasses import dataclass

from beethoven.repository.midi import midi
from beethoven.sequencer.grid import Grid
from beethoven.sequencer.players.base import Players


@dataclass
class JamRoom:
    grid: Grid = Grid()
    players: Players = Players()

    def play(self, callback=None, **kwargs) -> None:
        for grid_part_index in midi.play(self.grid, self.players, **kwargs):

            if callback:
                callback(grid_part_index)

    def quiet(self) -> None:
        midi._shutdown()
