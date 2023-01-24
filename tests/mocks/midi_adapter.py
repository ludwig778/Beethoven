from mido.backends.rtmidi import Output

from beethoven.adapters.midi import MidiAdapter


class MockedInput(Output):
    def __init__(self, name, **kwargs):
        self.name = name

    def closed(self):
        return False

    def close(self, *args, **kwargs):
        pass


class MockedOutput(Output):
    def __init__(self, name, **kwargs):
        self.name = name

    def closed(self):
        return False

    def close(self, *args, **kwargs):
        pass


class MockedMidiAdapter(MidiAdapter):
    @property
    def available_inputs(self):
        return ["test_input_1", "test_input_2"]
