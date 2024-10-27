from pathlib import Path

from hartware_lib.adapters.filesystem import DirectoryAdapter, FileAdapter
from pytest import fixture

from beethoven.adapters.factory import get_adapters
from tests.mocks.midi_adapter import (MockedInput, MockedMidiAdapter,
                                      MockedOutput)


@fixture
def adapters():
    adapters = get_adapters()

    yield adapters

    adapters.midi.close_all_outputs()


@fixture(scope="function")
def mock_midi_adapter(monkeypatch):
    monkeypatch.setattr("beethoven.adapters.midi.open_input", MockedInput)
    monkeypatch.setattr("beethoven.adapters.midi.open_output", MockedOutput)
    monkeypatch.setattr("beethoven.adapters.factory.MidiAdapter", MockedMidiAdapter)


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(path=Path(".testing"))
    test_directory.create()

    yield

    test_directory.delete()


@fixture(scope="session")
def fixtures_folder():
    return FileAdapter(path=Path("tests", "fixtures", "data"))
