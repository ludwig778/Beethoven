from pathlib import Path

from hartware_lib.pydantic.field_types import BooleanFromString
from pydantic import BaseSettings, Field

from beethoven.utils.pydantic import use_env_variables_over_config_file

BASE_PATH: Path = Path.home() / ".config" / "beethoven"

DEFAULT_CONFIG_PATH: Path = BASE_PATH / "config.json"
DEFAULT_STORE_PATH: Path = BASE_PATH / "store.json"


class MongoSettings(BaseSettings):
    username: str = ""
    password: str = ""
    database: str = ""
    host: str = ""
    port: int = 27017
    srv_mode: BooleanFromString = Field(default=False)
    timeout_ms: int = 2000

    @property
    def is_valid(self):
        return all([self.username, self.password, self.database, self.host])

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_MONGODB_"


class MidiSettings(BaseSettings):
    default_output: str = "Beethoven Default Output"

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_MIDI_"


class LocalConfigSettings(BaseSettings):
    path: Path = DEFAULT_CONFIG_PATH

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_CONFIG_"


class LocalStoreSettings(BaseSettings):
    path: Path = DEFAULT_STORE_PATH

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_LOCAL_STORE_"
        customise_sources = use_env_variables_over_config_file


class AppSettings(BaseSettings):
    test: BooleanFromString = Field(default=False)
    debug: BooleanFromString = Field(default=False)

    midi: MidiSettings = Field(default_factory=MidiSettings)

    config: LocalConfigSettings = Field(default_factory=LocalConfigSettings)
    mongo_settings: MongoSettings = Field(default_factory=MongoSettings)
    local_store: LocalStoreSettings = Field(default_factory=LocalStoreSettings)

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_"


def get_settings() -> AppSettings:
    return AppSettings()
