from prompt_toolkit.completion import WordCompleter

from beethoven.prompt.base import BasePrompt


class TrainingPrompt(BasePrompt):
    PROMPT_STR = "training> "

    def _get_completer(self):
        return WordCompleter([])

    def dispatch(self, text):
        print("test is ", text)
