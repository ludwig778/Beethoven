from pathlib import Path

from hartware_lib.adapters.file import FileAdapter

from beethoven.settings import get_settings
from beethoven.utils.settings import create_config_file


def test_settings_with_default_docker_env_variables():
    assert get_settings().dict() == {
        "test": True,
        "debug": False,
        "config": {"path": Path(".testing/beethoven/config.json")},
        "midi": {"default_output": "Beethoven Default Output"},
        "mongo_settings": {
            "database": "beethoven",
            "host": "mongodb",
            "password": "password123",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "user",
        },
        "local_store": {"path": Path(".testing/beethoven/store.json")},
    }


def test_settings_without_docker_env_variables(monkeypatch):
    monkeypatch.delenv("BEETHOVEN_TEST")
    monkeypatch.delenv("BEETHOVEN_MONGODB_USERNAME")
    monkeypatch.delenv("BEETHOVEN_MONGODB_PASSWORD")
    monkeypatch.delenv("BEETHOVEN_MONGODB_HOST")
    monkeypatch.delenv("BEETHOVEN_MONGODB_DATABASE")
    monkeypatch.delenv("BEETHOVEN_CONFIG_PATH")
    monkeypatch.delenv("BEETHOVEN_LOCAL_STORE_PATH")

    assert get_settings().dict() == {
        "test": False,
        "debug": False,
        "config": {"path": Path("/root/.config/beethoven/config.json")},
        "midi": {"default_output": "Beethoven Default Output"},
        "mongo_settings": {
            "database": "",
            "host": "",
            "password": "",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "",
        },
        "local_store": {"path": Path("/root/.config/beethoven/store.json")},
    }


def test_settings_with_only_env_variables(monkeypatch):
    monkeypatch.setenv("BEETHOVEN_TEST", "true")
    monkeypatch.setenv("BEETHOVEN_DEBUG", "false")
    monkeypatch.setenv("BEETHOVEN_MONGODB_USERNAME", "username")
    monkeypatch.setenv("BEETHOVEN_MONGODB_PASSWORD", "password")
    monkeypatch.setenv("BEETHOVEN_MONGODB_HOST", "host")
    monkeypatch.setenv("BEETHOVEN_MONGODB_DATABASE", "database")

    assert get_settings().dict() == {
        "test": True,
        "debug": False,
        "config": {"path": Path(".testing/beethoven/config.json")},
        "midi": {"default_output": "Beethoven Default Output"},
        "mongo_settings": {
            "database": "database",
            "host": "host",
            "password": "password",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "username",
        },
        "local_store": {"path": Path(".testing/beethoven/store.json")},
    }


def test_settings_create_config_file(monkeypatch):
    monkeypatch.setenv("BEETHOVEN_TEST", "true")
    monkeypatch.setenv("BEETHOVEN_DEBUG", "false")
    monkeypatch.setenv("BEETHOVEN_CONFIG_PATH", ".testing/beethoven/config.json")
    monkeypatch.setenv("BEETHOVEN_MONGODB_USERNAME", "username")
    monkeypatch.setenv("BEETHOVEN_MONGODB_PASSWORD", "password")
    monkeypatch.setenv("BEETHOVEN_MONGODB_HOST", "host")
    monkeypatch.setenv("BEETHOVEN_MONGODB_DATABASE", "database")
    monkeypatch.setenv("BEETHOVEN_LOCAL_STORE_PATH", ".testing/beethoven/store.json")

    settings = get_settings()

    create_config_file(settings)

    config_file = FileAdapter(file_path=Path(".testing/beethoven/config.json"))

    assert config_file.read_json() == {
        "local_store": {"path": ".testing/beethoven/store.json"},
        "midi": {"default_output": "Beethoven Default Output"},
        "mongo_settings": {
            "database": "database",
            "host": "host",
            "password": "password",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "username",
        },
    }


def test_settings_with_mixed_source(monkeypatch):
    config_file = FileAdapter(file_path=Path(".testing/beethoven/config.json"))
    config_file.create_parent_dir()

    config_file.write_json(
        {
            "local_store": {"path": ".testing/beethoven/store.json"},
            "midi": {"default_output": "Beethoven Default Output"},
            "mongo_settings": {
                "database": "beethoven",
                "host": "mongodb",
                "password": "password123",
                "port": 27017,
                "srv_mode": False,
                "timeout_ms": 2000,
                "username": "user",
            },
        }
    )

    monkeypatch.setenv("BEETHOVEN_TEST", "false")
    monkeypatch.setenv("BEETHOVEN_DEBUG", "true")
    monkeypatch.setenv("BEETHOVEN_CONFIG_PATH", ".testing/beethoven/config.json")
    monkeypatch.setenv("BEETHOVEN_MONGODB_USERNAME", "overrided")
    monkeypatch.setenv("BEETHOVEN_LOCAL_STORE_PATH", ".testing/beethoven/store2.json")

    assert get_settings().dict() == {
        "test": False,
        "debug": True,
        "config": {"path": Path(".testing/beethoven/config.json")},
        "midi": {"default_output": "Beethoven Default Output"},
        "mongo_settings": {
            "database": "beethoven",
            "host": "mongodb",
            "password": "password123",
            "port": 27017,
            "srv_mode": False,
            "timeout_ms": 2000,
            "username": "overrided",
        },
        "local_store": {"path": Path(".testing/beethoven/store2.json")},
    }
