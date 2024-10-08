from pathlib import Path

from hartware_lib.adapters.filesystem import FileAdapter
from hartware_lib.serializers import NoSerializerMatch
from hartware_lib.serializers.dataclasses import DataClassExtraSerializer
from hartware_lib.serializers.main import deserialize, serialize
from pytest import fixture

from beethoven.settings import (AppSettings, MidiSettings, PlayerSetting,
                                PlayerSettings, TuningSetting, TuningSettings)

TEST_CONFIG_PATH = Path("tests/generated/config.json")

@fixture
def clean_default_settings_file():
    settings = AppSettings.get_default()

    AppSettings.delete(TEST_CONFIG_PATH)

    yield

    AppSettings.delete(TEST_CONFIG_PATH)


def test_settings_default_factory():
    settings = AppSettings.load_default()

    assert settings.test is True
    assert settings.debug is False

    #assert settings.config_file.path == Path("tests", "fixtures", "config.json")

    assert settings.midi.opened_outputs == [
        "Beethoven",
        "Beethoven:preview",
        "Beethoven:metronome",
    ]


def test_settings_default_factory_without_env_variables(monkeypatch):
    monkeypatch.delenv("BEETHOVEN_TEST")
    monkeypatch.delenv("BEETHOVEN_CONFIG_PATH")

    settings = AppSettings.load_default()

    assert settings.test is False
    assert settings.debug is False

    # assert settings.config_file.path == Path.home() / Path(".config", "beethoven", "config.json")


def test_settings_save_read_and_delete_cycle(clean_default_settings_file):
    settings = AppSettings.load_default()
    config_file = FileAdapter(path=TEST_CONFIG_PATH)

    settings.save(TEST_CONFIG_PATH)

    assert config_file.exists

    local_settings = AppSettings.load(TEST_CONFIG_PATH)

    assert local_settings
    assert local_settings == settings

    AppSettings.delete(TEST_CONFIG_PATH)

    assert not config_file.exists


def test_settings_save_and_read_with_env_variables_override(clean_default_settings_file, monkeypatch):
    settings = AppSettings.load_default()

    settings.save(TEST_CONFIG_PATH)

    monkeypatch.setenv("BEETHOVEN_TEST", "true")
    monkeypatch.setenv("BEETHOVEN_DEBUG", "true")

    settings = AppSettings.load()

    assert settings.test is True
    assert settings.debug is True


def test_settings_factory(clean_default_settings_file):
    settings = AppSettings.load_default()

    assert settings.debug is False
    assert settings == AppSettings.load()

    settings.debug = True

    settings.save(TEST_CONFIG_PATH)

    settings = AppSettings.load(TEST_CONFIG_PATH)

    assert settings.debug is True


def test_settings_serializers(clean_default_settings_file):
    settings = AppSettings.load_default()
    extra_serializers = DataClassExtraSerializer(
        AppSettings,
        TuningSettings,
        TuningSetting,
        MidiSettings,
        PlayerSettings,
        PlayerSetting
    )

    serialized = serialize(settings, extra_serializers=[extra_serializers])

    assert isinstance(serialized, str)

    deserialized = deserialize(serialized, extra_serializers=[extra_serializers])

    assert settings == deserialized