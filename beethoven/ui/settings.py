from typing import Dict, List, Optional

from pydantic import BaseModel, validator

from beethoven.models import Note


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
    defaults: Dict[str, TuningSetting]
    user_defined: Dict[str, TuningSetting]

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


class AppSettings(BaseModel):
    tuning: TuningSettings
    midi: MidiSettings
    player: PlayerSettings


def get_default_settings():
    app_settings = AppSettings(
        tuning=TuningSettings(
            defaults={
                "E Standard": "E,A,D,G,B,E",
                "E Standard 4str": "E,A,D,G",
                "E Standard 5str": "E,A,D,G,C",
                "D Dropped": "D,A,D,G,B,E",
                "B Standard": "B,E,A,D,F#,B",
                "B Standard 7str": "B,E,A,D,G,B,E",
                "F# Standard 8str": "F#,B,E,A,D,G,B,E",
            },
            user_defined={},
        ),
        midi=MidiSettings(opened_outputs=[]),
        player=PlayerSettings(
            max_players=4,
            metronome=PlayerSetting(
                instrument_name="", output_name="", channel=0, enabled=True
            ),
            preview=PlayerSetting(
                instrument_name="", output_name="", channel=0, enabled=True
            ),
            players=[],
        ),
    )

    return app_settings


def get_settings():
    app_settings = AppSettings(
        tuning=TuningSettings(
            defaults={
                "E Standard": "E,A,D,G,B,E",
                "E Standard 4str": "E,A,D,G",
                "E Standard 5str": "E,A,D,G,C",
                "D Dropped": "D,A,D,G,B,E",
                "B Standard": "B,E,A,D,F#,B",
                "B Standard 7str": "B,E,A,D,G,B,E",
                "F# Standard 8str": "F#,B,E,A,D,G,B,E",
            },
            user_defined={
                "A Standard": "A,D,G,C,E,A",
            },
        ),
        midi=MidiSettings(opened_outputs=["Drums", "Piano", "Guitar", "Bass"]),
        player=PlayerSettings(
            max_players=4,
            metronome=PlayerSetting(
                instrument_name="Drums", output_name="Drums", channel=2, enabled=True
            ),
            preview=PlayerSetting(
                instrument_name="Guitar", output_name="Guitar", channel=2, enabled=True
            ),
            players=[
                PlayerSetting(
                    instrument_name="Guitar", output_name="e", channel=2, enabled=True
                )
            ],
        ),
    )

    return app_settings
