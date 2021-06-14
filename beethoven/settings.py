from json import dump, load
from os import environ
from pathlib import Path
from sys import exit

from beethoven.utils.validator import check_boolean

PREFIX = "BEETHOVEN"

TEST = environ.get(f"{PREFIX}_TEST", False)


CONFIG = {
    "prefix": PREFIX,
    "create_file": not TEST,
    "config": {
        "MONGODB": [
            ("username", None,        None),
            ("password", None,        None),
            ("host",     None,        None),
            ("port",     27017,       int),
            ("database", "beethoven", None),
            ("srv_mode", False,       check_boolean)
        ]
    }
}


class Settings:
    def __init__(self, prefix=None, create_file=None, config=None):
        self.prefix = prefix
        self.create_file = create_file
        self.config = config

        self.parsed = {}

        self.load()

    def get_default(self):
        return {
            field: default
            for prefix, config in self.config.items()
            for field, default, _ in config
        }

    def load(self):
        self.load_from_file()
        self.load_from_env()

    def load_from_file(self):
        config_dir = Path.home() / ".config" / self.prefix.lower()
        config_file = config_dir / "config.json"

        if config_file.is_file():
            with config_file.open() as fd:
                self.parsed.update(load(fd))
        else:
            if not self.create_file:
                return

            config_dir.mkdir(parents=True, exist_ok=True)

            config_file.touch()
            with config_file.open(mode="w") as fd:
                dump(self.get_default(), fd, indent=4)
                print(f"Tracker : Template configuration set at {config_file}")

    def load_from_env(self):
        for prefix, config in self.config.items():
            for field_name, default, transform in config:
                env_name = f"{self.prefix}_{prefix}_{field_name}".upper()
                attr = environ.get(env_name, default)

                if attr is None and not self.parsed.get(field_name):
                    print(f"Tracker : {field_name} must be set")
                    exit(1)

                if attr:
                    if transform:
                        attr = transform(attr)

                    self.parsed[field_name] = attr


settings = Settings(**CONFIG)

MONGO_CONFIG = settings.parsed
