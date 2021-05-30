from prompt_toolkit.completion import WordCompleter

from beethoven.prompt.base import BasePrompt
from beethoven.prompt.compose import ComposePrompt
from beethoven.prompt.training import TrainingPrompt


class MainPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def _get_completer(self):
        return WordCompleter([
            "compose", "training", "help", "leave", "quit",
        ])

    def _help(self):
        print(" == Menu ==")
        print(" - Training")
        print(" - Compose")

    def dispatch(self, text):
        if text.lower() in ("c", "compose"):
            return ComposePrompt().loop()

        elif text.lower() in ("t", "training"):
            return TrainingPrompt().loop()
