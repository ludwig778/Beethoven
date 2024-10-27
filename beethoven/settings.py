from __future__ import annotations

from dataclasses import dataclass, field
from os import environ
from pathlib import Path
from typing import Dict, List

from hartware_lib.adapters.filesystem import FileAdapter
from hartware_lib.serializers.dataclasses import DataClassExtraSerializer
from hartware_lib.serializers.main import deserialize, serialize

from beethoven.models import Note

HOME_PATH = Path.home()
BEETHOVEN_CONFIG_PATH = (
    Path(environ["BEETHOVEN_CONFIG_PATH"])
    if "BEETHOVEN_CONFIG_PATH" in environ
    else (HOME_PATH / Path(".config", "beethoven", "config.json"))
)


@dataclass
class TuningSetting:
    notes: List[Note]

    @classmethod
    def build(cls, notes: List[Note]) -> TuningSetting:
        if all([isinstance(n, Note) for n in notes]):
            raise AssertionError("Tuning must been given Notes")

        if len(notes) < 4 or len(notes) > 8:
            raise AssertionError("Tuning must have between 4 and 8 strings")

        return cls(notes=notes)

    # def dict(self, *args, **kwargs) -> Dict[str, Note]:
    #     return ",".join(map(str, self.notes))

    @classmethod
    def build_from_str(cls, notes_str: str) -> TuningSetting:
        return cls(notes=Note.parse_list(notes_str))


@dataclass
class TuningSettings:
    user_defined: Dict[str, TuningSetting] = field(default_factory=dict)

    @property
    def defaults(self) -> Dict[str, TuningSetting]:
        return {
            "E Standard": TuningSetting.build_from_str("E,A,D,G,B,E"),
            "E Standard 4str": TuningSetting.build_from_str("E,A,D,G"),
            "E Standard 5str": TuningSetting.build_from_str("E,A,D,G,C"),
            "D Dropped": TuningSetting.build_from_str("D,A,D,G,B,E"),
            "B Standard": TuningSetting.build_from_str("B,E,A,D,F#,B"),
            "B Standard 7str": TuningSetting.build_from_str("B,E,A,D,G,B,E"),
            "F# Standard 8str": TuningSetting.build_from_str("F#,B,E,A,D,G,B,E"),
        }

    # @validator("defaults", "user_defined", pre=True)
    # def setup_tuning_objects(cls, tunings):
    # TODO REMOVE COMMENTS
    # @classmethod
    # def build(cls, tunings: List[TuningSetting]) -> TuningSettings:
    #     return {
    #         tuning: TuningSetting.from_str(tuning_setting)
    #         if isinstance(tuning_setting, str)
    #         else tuning_setting
    #         for tuning, tuning_setting in tunings.items()
    #     }

    @property
    def tunings(self) -> Dict[str, TuningSetting]:
        return {**self.defaults, **self.user_defined}


@dataclass
class MidiSettings:
    selected_input: str | None = None
    opened_outputs: List[str] = field(default_factory=list)


@dataclass
class PlayerSetting:
    instrument_name: str | None = None
    instrument_style: str | None = None
    output_name: str | None = None
    channel: int = 0
    mapping: str = ""
    enabled: bool = False


@dataclass
class PlayerSettings:
    max_players: int

    metronome: PlayerSetting
    preview: PlayerSetting
    players: List[PlayerSetting]


@dataclass
class AppSettings:
    tunings: TuningSettings
    midi: MidiSettings
    player: PlayerSettings

    test: bool = False
    debug: bool = False

    _prefix = "beethoven"

    @classmethod
    def get_default(cls) -> AppSettings:
        return cls(
            tunings=TuningSettings(),
            midi=MidiSettings(opened_outputs=["Beethoven", "Beethoven:preview", "Beethoven:metronome"]),
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

    @classmethod
    def load(cls, config_file: Path = BEETHOVEN_CONFIG_PATH) -> AppSettings:
        # NOTE to pass pytest env variable, to remove
        if isinstance(config_file, str):
            config_file = Path(config_file)

        settings_file = FileAdapter(path=config_file)

        settings = None
        if settings_file.exists:
            try:
                settings = deserialize(settings_file.read(), extra_serializers=[
                    DataClassExtraSerializer(
                        AppSettings,
                        TuningSettings,
                        TuningSetting,
                        MidiSettings,
                        PlayerSettings,
                        PlayerSetting
                    )
                ])
            except Exception as exc:
                print(exc)

        if not settings:
            settings = cls.get_default()

        if "BEETHOVEN_DEBUG" in environ:
            settings.debug = environ["BEETHOVEN_DEBUG"].lower() in ("1", "true", "yes")
        if "BEETHOVEN_TEST" in environ:
            settings.test = environ["BEETHOVEN_TEST"].lower() in ("1", "true", "yes")

        return settings

    @classmethod
    def load_default(cls) -> AppSettings:
        settings = cls.get_default()

        if "BEETHOVEN_DEBUG" in environ:
            settings.debug = environ["BEETHOVEN_DEBUG"].lower() in ("1", "true", "yes")
        if "BEETHOVEN_TEST" in environ:
            settings.test = environ["BEETHOVEN_TEST"].lower() in ("1", "true", "yes")

        return settings

    def serialize(self) -> str:
        return serialize(
            self, indent=4, extra_serializers=[DataClassExtraSerializer()]
        )

    def save(self, config_file: Path = BEETHOVEN_CONFIG_PATH) -> Path:
        settings_file = FileAdapter(path=config_file)

        if not settings_file.directory.exists:
            settings_file.directory.create()

        settings_file.write(self.serialize())

        return config_file

    @staticmethod
    def delete(config_file: Path = BEETHOVEN_CONFIG_PATH) -> None:
        if config_file:
            settings_file = FileAdapter(path=config_file)

            if settings_file.exists:
                settings_file.delete()
