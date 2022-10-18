import logging.config

from beethoven.settings import get_settings

settings = get_settings()


logging.config.dictConfig(
    {
        "version": 1,
        # "disable_existing_loggers": False,
        "formatters": {
            "standard": {"format": "%(asctime)s %(levelname)-8s %(name)-19s %(message)s"},
        },
        "handlers": {
            "default": {
                "level": logging.DEBUG,
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": logging.CRITICAL if settings.test else logging.DEBUG,
            },
        },
    }
)
