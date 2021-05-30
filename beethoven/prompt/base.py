from enum import Enum, auto

from prompt_toolkit import PromptSession, prompt
from prompt_toolkit.history import FileHistory
from pyparsing import ParseFatalException


class PromptSignal(Enum):
    LEAVE = auto()
    QUIT = auto()


class BasePrompt:
    PROMPT_STR = None
    BOTTOM_TOOLBAR = None

    def __init__(self):
        self.session = PromptSession(
            message=self.PROMPT_STR,
            completer=self._get_completer(),
            bottom_toolbar=self.BOTTOM_TOOLBAR,
            history=FileHistory(".beethoven_history"),
            enable_suspend=True
        )

    def prompt(self, text):
        return prompt(text)

    def _get_completer(self):
        raise NotImplementedError

    def _help(self):
        raise NotImplementedError

    def loop(self):
        while True:
            try:
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

    def _handle(self):
        text = self.session.prompt()

        if text in ("q", "quit"):
            return PromptSignal.QUIT
        elif text in ("l", "leave"):
            return PromptSignal.LEAVE
        elif text in ("h", "help"):
            self._help()

        if text:
            try:
                if signal := self.dispatch(text):
                    if signal in (PromptSignal.QUIT, PromptSignal.LEAVE):
                        return signal
            except ParseFatalException as exc:
                offset = len(self.session.message) + exc.loc
                print(f"{' ' * offset}^ {exc.msg}")

    def dispatch(self):
        raise NotImplementedError()
