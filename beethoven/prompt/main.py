from beethoven.prompt.base import BasePrompt, PromptSignal
from beethoven.prompt.harmony import HarmonyPrompt


class MainPrompt(BasePrompt):
    PROMPT_STR = ">>> "

    def dispatch(self, text):
        if text == "s":
            if HarmonyPrompt().loop() == PromptSignal.QUIT:
                return PromptSignal.QUIT

        print("text is : ", text)
