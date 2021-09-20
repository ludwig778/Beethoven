from pytest import fixture, mark

from beethoven.prompt import MainPrompt, PromptContext, session


@fixture(scope="function")
def prompt_redirect(monkeypatch):
    class PromptRedirector:
        def __init__(self):
            self.inputs = []
            self.outputs = []
            self.n = 0

        def set_inputs(self, inputs):
            self.inputs = inputs

        def add_output(self, output):
            self.outputs.append(output)

        def __next__(self):
            if self.n >= len(self.inputs):
                raise EOFError()

            value = self.inputs[self.n]
            self.n += 1

            return value

    redirect = PromptRedirector()

    monkeypatch.setattr(session, "prompt", redirect.__next__)
    monkeypatch.setattr("beethoven.prompt.print_formatted_text", redirect.add_output)

    yield redirect


@mark.parametrize(
    "inputs,outputs",
    [
        (["leave"], ["leaving MainPrompt"]),
        (["quit"], ["quitting"]),
        (["train", "leave"], ["going to train", "leaving TrainingPrompt"]),
        (
            ["train", "leave", "compose", "quit"],
            [
                "going to train",
                "leaving TrainingPrompt",
                "going to compose",
                "quitting",
            ],
        ),
        (["compose", "sc=A_major bpm=33 ts=4/4 p=I"], ["going to compose"]),
        (
            ["compose", "invalid_grid"],
            ["going to compose", "Couldn't parse string='invalid_grid' as Grid"],
        ),
    ],
)
def test_prompt_browsing_responses(inputs, outputs, prompt_redirect):
    prompt_redirect.set_inputs(inputs)
    MainPrompt().loop(PromptContext())

    assert prompt_redirect.outputs == outputs
