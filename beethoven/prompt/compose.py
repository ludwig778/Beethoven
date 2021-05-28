from prompt_toolkit.completion import WordCompleter

from beethoven.prompt.base import BasePrompt
from beethoven.prompt.display import display
from beethoven.prompt.state import state
from beethoven.sequencer.grid import Grid


class ComposePrompt(BasePrompt):
    PROMPT_STR = "compose> "

    def _get_completer(self):
        return WordCompleter([])

    def dispatch(self, text):
        try:
            state.jam_room.grid = Grid.parse(text, full_config=state.config)
            state.jam_room.play(callback=display)

        except ValueError as exc:
            print(f"Error : {str(exc)}")
            return
