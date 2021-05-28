from prompt_toolkit.completion import WordCompleter

from beethoven.prompt.base import BasePrompt, PromptSignal
from beethoven.prompt.compose import ComposePrompt


class MainPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def _get_completer(self):
        return WordCompleter([
            "compose", "leave", "quit",
        ])

    def dispatch(self, text):
        if text.lower() in ("c", "compose"):
            if ComposePrompt().loop() == PromptSignal.QUIT:
                return PromptSignal.QUIT

        print("text is : ", text)
