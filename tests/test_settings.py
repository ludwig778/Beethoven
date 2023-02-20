from pathlib import Path

from hartware_lib.adapters.file import FileAdapter
from pytest import fixture

from beethoven.settings import (
    delete_settings,
    get_default_settings,
    get_local_settings,
    get_settings,
    save_settings,
)


@fixture
def clean_default_settings_file():
    settings = get_default_settings()

    delete_settings(settings)

    yield

    delete_settings(settings)


def test_settings_default_factory():
    settings = get_default_settings()

    assert settings.test is True
    assert settings.debug is False

    assert settings.config_file.path == Path("tests", "fixtures", "config.json")

    assert settings.midi.opened_outputs == [
        "Beethoven",
        "Beethoven:preview",
        "Beethoven:metronome",
    ]


def test_settings_default_factory_without_env_variables(monkeypatch):
    monkeypatch.delenv("BEETHOVEN_TEST")
    monkeypatch.delenv("BEETHOVEN_CONFIG_PATH")

    settings = get_default_settings()

    assert settings.test is False
    assert settings.debug is False

    assert settings.config_file.path == Path.home() / Path(
        ".config", "beethoven", "config.json"
    )


def test_settings_save_read_and_delete_cycle(clean_default_settings_file):
    assert not get_local_settings()

    settings = get_default_settings()
    config_file = FileAdapter(file_path=settings.config_file.path)

    save_settings(settings)

    assert config_file.exists()

    local_settings = get_local_settings()

    assert local_settings
    assert local_settings == settings

    delete_settings(settings)

    assert not config_file.exists()


def test_settings_save_and_read_with_env_variables_override(
    clean_default_settings_file, monkeypatch
):
    settings = get_default_settings()

    save_settings(settings)

    monkeypatch.setenv("BEETHOVEN_TEST", "true")
    monkeypatch.setenv("BEETHOVEN_DEBUG", "true")

    settings = get_settings()

    assert settings.test is True
    assert settings.debug is True


def test_settings_factory(clean_default_settings_file):
    settings = get_default_settings()

    assert settings.debug is False
    assert settings == get_settings()

    settings.debug = True

    save_settings(settings)

    settings = get_settings()

    assert settings.debug is True
