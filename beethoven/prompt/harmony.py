from beethoven.prompt.base import BasePrompt
from beethoven.prompt.state import state
from beethoven.sequencer.grid import Grid


class HarmonyPrompt(BasePrompt):
    PROMPT_STR = "harmony> "

    def dispatch(self, text):
        try:
            state.jam_room.grid = Grid.parse(text, full_config=state.config)
            state.jam_room.play()

        except ValueError as exc:
            print(f"Error : {str(exc)}")
            return
