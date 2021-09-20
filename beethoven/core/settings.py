from dataclasses import dataclass
from os import environ
from typing import Any

TEST: bool = str(environ.get("BEETHOVEN_TEST")) in ("true", "yes", "1")

MIDI_OUTPUT_NAME = environ.get("BEETHOVEN_MIDI_OUTPUT_NAME", "BEETHOVEN_MIDI_OUTPUT")


def get_or_raise(data: Any, key: str, error_msg: str):
    value = data.get(key)

    assert value, error_msg

    return value


@dataclass
class MongoConfig:
    host: str = get_or_raise(
        environ, "BEETHOVEN_MONGODB_HOST", "Mongo host must be set"
    )
    port: int = int(environ.get("BEETHOVEN_MONGODB_PORT", 27017))

    database: str = environ.get("BEETHOVEN_MONGODB_DATABASE", "beethoven")
    username: str = get_or_raise(
        environ, "BEETHOVEN_MONGODB_USERNAME", "Mongo username must be set"
    )
    password: str = get_or_raise(
        environ, "BEETHOVEN_MONGODB_PASSWORD", "Mongo password must be set"
    )
    srv_mode: bool = environ.get("BEETHOVEN_MONGODB_SRV_MODE") in ("true", "yes", "1")

    if TEST:
        database += "_test"

    @property
    def uri(self) -> str:
        partial_uri = (
            f"{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

        if self.srv_mode:
            return f"mongodb+srv://{partial_uri}?retryWrites=true&w=majority"

        return f"mongodb://{partial_uri}?authSource=admin"


mongo_config = MongoConfig()
