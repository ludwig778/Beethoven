from pathlib import Path

from hartware_lib.adapters.directory import DirectoryAdapter
from pytest import fixture

from beethoven.adapters.factory import get_adapters
from beethoven.adapters.local_file import LocalFileAdapter
from tests.mocks.midi_adapter import MockedOutput, MockedMidiAdapter


@fixture(scope="function")
def mock_midi_adapter(monkeypatch):
    monkeypatch.setattr("beethoven.adapters.midi.open_output", MockedOutput)
    monkeypatch.setattr("beethoven.adapters.midi.MidiAdapter", MockedMidiAdapter)


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(dir_path=Path(".testing"))
    test_directory.create_dir()

    yield

    test_directory.delete_dir()


@fixture(scope="session")
def local_file_adapter():
    return LocalFileAdapter(dir_path=Path("tests", "fixtures", "data"))


@fixture
def adapters():
    adapters = get_adapters()

    yield adapters

    adapters.midi.close_all_outputs()
