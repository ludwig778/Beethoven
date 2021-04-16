from enum import Enum, auto

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory

from beethoven.sequencer.grid import Grid
from beethoven.sequencer.jam_room import JamRoom

print("\nNEW PROMPT\n")

class PromptSignal(Enum):
    LEAVE = auto()
    QUIT = auto()

class BasePrompt:
    PROMPT_STR = None
    BOTTOM_TOOLBAR = None

    def __init__(self):
        self.session = PromptSession(
            message=self.PROMPT_STR,
            bottom_toolbar=self.BOTTOM_TOOLBAR,
            history=FileHistory(".beethoven_history"),
            enable_suspend=True
        )

    def loop(self):
        try:
            while True:
                signal = self._handle()
                if signal == PromptSignal.LEAVE:
                    break
                if signal == PromptSignal.QUIT:
                    return PromptSignal.QUIT
        except EOFError:
            print("EOF : quitting...")
            return PromptSignal.QUIT
        except KeyboardInterrupt:
            pass

    def _pre_handle(self):
        text = self.session.prompt()

        if text in ("q", "quit"):
            return PromptSignal.QUIT, text
        elif text in ("l", "leave"):
            return PromptSignal.LEAVE, text

        return None, text

    def _handle(self):
        signal, text = self._pre_handle()
        if signal:
            return signal

        if text:
            if signal := self.dispatch(text):
                return signal

    def dispatch(self):
        raise NotImplementedError()



class MainPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def dispatch(self, text):
        if text == "s":
            if HarmonyPrompt().loop() == PromptSignal.QUIT:
                return PromptSignal.QUIT

        print("text is : ", text)


class HarmonyPrompt(BasePrompt):
    PROMPT_STR = "harmony> "

    def dispatch(self, text):
        try:
            grid = Grid.parse(text)
            jam_room = JamRoom(grid=grid)
            jam_room.play()

        except ValueError as exc:
            print(f"Error : {str(exc)}")
            return


        print("grid : ")
        from pprint import pprint

        pprint(grid)


main_prompt = MainPrompt()
main_prompt.loop()
