from beethoven.common.tuning import E_STANDARD
from beethoven.display.fretboard import Fretboard
from beethoven.repository.midi import midi
from beethoven.sequencer.players.base import Players


class JamRoom:
    def __init__(self, grid=None, players=None, **kwargs):
        self.grid = grid
        self.players = Players(*(players or []))

    def play(self, **kwargs):
        for grid_part_index in midi.play(self.grid, self.players, **kwargs):
            grid_part = self.grid.parts[grid_part_index - 1]
            print()
            print("========", self.grid.parts[grid_part_index - 1])
            print()
            fretboard = Fretboard(
                E_STANDARD,
                config={
                    "tonic_color": "white",
                    "chord_color": "light_yellow",
                    "diatonic_color": {
                        2: "light_red",
                        3: "light_green",
                        4: "turquoise_2",
                        6: "light_magenta"
                    }
                }
            )
            print(fretboard.to_ascii(
                scale=grid_part.scale,
                chord=grid_part.chord
            ))
            print()
