from hartware_lib.adapters.file import FileAdapter

from beethoven.settings import AppSettings
from beethoven.utils.json import PathEncoder


def create_config_file(settings: AppSettings) -> None:
    config_file = FileAdapter(file_path=settings.config.path)
    config_file.create_parent_dir()

    config_file.save_json(
        settings.dict(exclude={"config", "test", "debug"}), cls=PathEncoder
    )
