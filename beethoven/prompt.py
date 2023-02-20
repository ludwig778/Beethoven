from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.history import FileHistory

from beethoven.models import Grid


class PromptStatus(Enum):
    RUNNING: int = auto()
    LEAVE: int = auto()
    QUIT: int = auto()


@dataclass
class PromptContext:
    command: str = ""
    args: Dict = field(default_factory=dict)
    state: PromptStatus = PromptStatus.RUNNING


session: PromptSession = PromptSession(
    history=FileHistory(".beethoven_history"), enable_suspend=True
)


class BasePrompt:
    def dispatch(self, string, context):
        raise NotImplementedError()

    def help(self):
        raise NotImplementedError()

    def loop(self, context):
        i = 0
        while True:
            try:
                i += 1
                if i > 2:
                    return
                string = session.prompt()

                if string in ("h", "help"):
                    print_formatted_text("help")
                    self.help()
                elif string in ("l", "leave"):
                    print_formatted_text(f"leaving {self.__class__.__name__}")
                    context.state = PromptStatus.LEAVE
                elif string in ("q", "quit"):
                    print_formatted_text("quitting")
                    context.state = PromptStatus.QUIT
                else:
                    self.dispatch(string, context)

                if context.state == PromptStatus.LEAVE:
                    context.state = PromptStatus.RUNNING
                    break
                if context.state == PromptStatus.QUIT:
                    context.state = PromptStatus.QUIT
                    break
            except EOFError:
                context.state = PromptStatus.QUIT
                break
            except KeyboardInterrupt:
                pass


class MainPrompt(BasePrompt):
    def dispatch(self, string, context):
        if string in (
            "c",
            "compose",
        ):
            print_formatted_text("going to compose")
            ComposePrompt().loop(context)
        elif string in (
            "t",
            "train",
        ):
            print_formatted_text("going to train")
            TrainingPrompt().loop(context)


class ComposePrompt(BasePrompt):
    def dispatch(self, string, context):
        try:
            _ = Grid.parse(string)
        except Exception as exc:
            print_formatted_text(str(exc))


class TrainingPrompt(BasePrompt):
    def dispatch(self, string, context):
        print_formatted_text()
        print_formatted_text("in training prompt")
