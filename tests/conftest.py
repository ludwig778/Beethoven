from pathlib import Path

from hartware_lib.adapters.directory import DirectoryAdapter
from pytest import fixture


@fixture(scope="function", autouse=True)
def clean_test_directory_():
    test_directory = DirectoryAdapter(dir_path=Path(".testing"))
    test_directory.create()

    yield

    test_directory.delete()
