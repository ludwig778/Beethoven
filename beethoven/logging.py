import logging.config

from beethoven.settings import BEETHOVEN_CONFIG_PATH, AppSettings

settings = AppSettings.load()


logging.config.dictConfig(
    {
        "version": 1,
        # "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s %(levelname)-8s %(name)-20s %(funcName)-32s %(message)s"
            },
        },
        "handlers": {
            "console": {
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "standard",
                "filename": BEETHOVEN_CONFIG_PATH.parent / "beethoven.log",
                "maxBytes": 1000000,
                "backupCount": 3,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console", "file"],
                "level": logging.DEBUG if settings.debug else logging.INFO,
            },
        },
    }
)
