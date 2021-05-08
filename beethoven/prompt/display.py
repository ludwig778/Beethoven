from beethoven.common.tuning import E_STANDARD
from beethoven.display.fretboard import Fretboard
from beethoven.prompt.state import state


class PromptDisplay:
    DISPLAY_ORDER = (
        "global",
        "fretboard",
    )

    def __call__(self, grid_part_index):
        state.grid_part_index = grid_part_index
        state.grid_part = state.jam_room.grid.parts[state.grid_part_index - 1]

        for display_label in self.DISPLAY_ORDER:
            if func := getattr(self, f"print_{display_label}"):
                func()

    def print_fretboard(self):
        print("FRETBOARDS")

        for fretboard_config in state.prompt_config.get("fretboards"):
            tuning = fretboard_config.get("tuning", E_STANDARD)

            print(f"{tuning}\n")

            fretboard = Fretboard(
                tuning,
                config=fretboard_config
            )
            print(fretboard.to_ascii(
                scale=state.grid_part.scale,
                chord=state.grid_part.chord
            ))
            print("\n")

    def print_global(self):
        print("GLOBAL")

        print(state.grid_part)


display = PromptDisplay()
