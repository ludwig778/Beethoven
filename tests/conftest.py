from pathlib import Path

from hartware_lib.adapters.directory import DirectoryAdapter
from mido.backends.rtmidi import Output
from pytest import fixture

from beethoven.adapters import get_adapters


@fixture(scope="function", autouse=True)
def mock_open_midi_output(monkeypatch):
    def void(self, *args, **kwargs):
        pass

    class MockedOutput(Output):
        def __init__(self, name, **kwargs):
            self.name = name

        send = void
        _send = void
        panic = void
        close = void

    monkeypatch.setattr("beethoven.adapters.midi.Output", MockedOutput)
    monkeypatch.setattr("beethoven.adapters.midi.open_output", MockedOutput)


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(dir_path=Path(".testing"))
    test_directory.create()

    yield

    test_directory.delete()


@fixture
def adapters():
    adapters = get_adapters()

    yield adapters

    adapters.midi.close_all_outputs()
