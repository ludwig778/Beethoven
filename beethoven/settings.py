import json
from pathlib import Path
from typing import Dict, List, Optional

from hartware_lib.adapters.file import FileAdapter
from hartware_lib.pydantic.field_types import BooleanFromString
from pydantic import BaseModel, BaseSettings, Field, validator

from beethoven.models import Note
from beethoven.utils.pydantic import use_env_variables_over_config_file


class TuningSetting(BaseModel):
    notes: List[Note]

    @validator("notes")
    def check_notes_count(cls, notes):
        if 4 <= len(notes) <= 8:
            return notes

        raise AssertionError("Tuning must have between 4 and 8 strings")

    def dict(self, *args, **kwargs):
        return ",".join(map(str, self.notes))

    @classmethod
    def from_str(cls, notes):
        return cls(notes=Note.parse_list(notes))


class TuningSettings(BaseModel):
    defaults: Dict[str, TuningSetting] = {
        "E Standard": TuningSetting.from_str("E,A,D,G,B,E"),
        "E Standard 4str": TuningSetting.from_str("E,A,D,G"),
        "E Standard 5str": TuningSetting.from_str("E,A,D,G,C"),
        "D Dropped": TuningSetting.from_str("D,A,D,G,B,E"),
        "B Standard": TuningSetting.from_str("B,E,A,D,F#,B"),
        "B Standard 7str": TuningSetting.from_str("B,E,A,D,G,B,E"),
        "F# Standard 8str": TuningSetting.from_str("F#,B,E,A,D,G,B,E"),
    }
    user_defined: Dict[str, TuningSetting] = {}

    @validator("defaults", "user_defined", pre=True)
    def setup_tuning_objects(cls, tunings):
        return {
            tuning: TuningSetting.from_str(tuning_setting)
            if isinstance(tuning_setting, str)
            else tuning_setting
            for tuning, tuning_setting in tunings.items()
        }

    @property
    def tunings(self):
        return {**self.defaults, **self.user_defined}


class MidiSettings(BaseModel):
    selected_input: Optional[str] = None
    opened_outputs: List[str]


class PlayerSetting(BaseModel):
    instrument_name: Optional[str] = None
    instrument_style: Optional[str] = None
    output_name: Optional[str] = None
    channel: int = 0
    enabled: bool = True


class PlayerSettings(BaseModel):
    max_players: int

    metronome: PlayerSetting
    preview: PlayerSetting
    players: List[PlayerSetting]


class SettingsConfigFile(BaseSettings):
    path: Path = Path.home() / Path(".config", "beethoven", "config.json")

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_CONFIG_"


class AppSettings(BaseSettings):
    test: BooleanFromString = Field(default=False)  # type: ignore
    debug: BooleanFromString = Field(default=False)  # type: ignore

    config_file: SettingsConfigFile = Field(default_factory=SettingsConfigFile)

    tuning: TuningSettings
    midi: MidiSettings
    player: PlayerSettings

    class Config:
        case_sensitive = False
        env_prefix = "BEETHOVEN_"
        customise_sources = use_env_variables_over_config_file


def get_local_settings() -> Optional[AppSettings]:
    settings_config_file = SettingsConfigFile()

    settings_file = FileAdapter(file_path=settings_config_file.path)

    if settings_file.exists():
        return AppSettings(
            config_file=settings_config_file, **settings_file.read_json()
        )

    return None


def get_default_settings():
    app_settings = AppSettings(
        tuning=TuningSettings(),
        midi=MidiSettings(
            opened_outputs=["Beethoven", "Beethoven:preview", "Beethoven:metronome"]
        ),
        player=PlayerSettings(
            max_players=4,
            metronome=PlayerSetting(
                instrument_name="Metronome",
                output_name="Beethoven:metronome",
                channel=0,
                enabled=True,
            ),
            preview=PlayerSetting(
                instrument_name="Piano",
                output_name="Beethoven:preview",
                channel=0,
                enabled=True,
            ),
            players=[],
        ),
    )

    return app_settings


def get_settings() -> AppSettings:
    return get_local_settings() or get_default_settings()


def setup_settings():
    local_settings = get_local_settings()

    if local_settings:
        return local_settings

    settings = get_default_settings()

    save_settings(settings)

    return settings


def serialize_settings(settings: AppSettings) -> str:
    settings_dict = settings.dict(exclude={"config_file"})

    return json.dumps(settings_dict, indent=2)


def save_settings(settings: AppSettings):
    settings_file = FileAdapter(file_path=settings.config_file.path)

    if not settings_file.file_path.parent.exists():
        settings_file.create_parent_dir()

    serialized_settings = serialize_settings(settings)

    settings_file.save(serialized_settings)


def delete_settings(settings: AppSettings):
    if settings.config_file.path:
        settings_file = FileAdapter(file_path=settings.config_file.path)

        if settings_file.exists():
            settings_file.delete()
