from pathlib import Path

from hartware_lib.adapters.directory import DirectoryAdapter
from pytest import fixture

from beethoven.adapters import get_adapters


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
