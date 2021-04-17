from beethoven.prompt.base import BasePrompt
from beethoven.prompt.state import state
from beethoven.sequencer.grid import Grid


class HarmonyPrompt(BasePrompt):
    PROMPT_STR = "harmony> "

    def dispatch(self, text):
        from pprint import pprint
        try:
            state.jam_room.grid = Grid.parse(text)
            state.jam_room.play()
            pprint(state.jam_room.__dict__)

        except ValueError as exc:
            print(f"Error : {str(exc)}")
            return

        print("grid : ")

        pprint(state.jam_room.grid)
