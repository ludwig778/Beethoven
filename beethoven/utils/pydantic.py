from typing import Tuple

from pydantic.env_settings import SettingsSourceCallable


def use_env_variables_over_config_file(
    init_settings: SettingsSourceCallable,
    env_settings: SettingsSourceCallable,
    file_secret_settings: SettingsSourceCallable,
) -> Tuple[SettingsSourceCallable, ...]:
    return env_settings, init_settings, file_secret_settings
