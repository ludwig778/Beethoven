from dataclasses import dataclass
from os import environ

TEST: bool = str(environ.get("BEETHOVEN_TEST")) in ("true", "yes", "1")

MIDI_OUTPUT_NAME = environ.get("BEETHOVEN_MIDI_OUTPUT_NAME", "BEETHOVEN_MIDI_OUTPUT")


@dataclass
class MongoConfig:
    host: str = environ.get("BEETHOVEN_MONGODB_HOST")
    port: int = environ.get("BEETHOVEN_MONGODB_PORT", 27017)

    database: str = environ.get("BEETHOVEN_MONGODB_DATABASE", "beethoven")
    username: str = environ.get("BEETHOVEN_MONGODB_USERNAME")
    password: str = environ.get("BEETHOVEN_MONGODB_PASSWORD")

    srv_mode: bool = environ.get("BEETHOVEN_MONGODB_SRV_MODE")

    def __post_init__(self):
        self.port = int(self.port)
        self.srv_mode = str(self.srv_mode) in ("true", "yes", "1")

        assert self.host, "Mongo host must be set"
        assert self.database, "Mongo database must be set"
        assert self.username, "Mongo username must be set"
        assert self.password, "Mongo password must be set"

        if TEST:
            self.database += "_test"

    @property
    def uri(self) -> str:
        partial_uri = f"{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"

        if self.srv_mode:
            return f"mongodb+srv://{partial_uri}?retryWrites=true&w=majority"

        return f"mongodb://{partial_uri}?authSource=admin"


mongo_config = MongoConfig()
