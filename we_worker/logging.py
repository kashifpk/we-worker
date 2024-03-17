from logging.config import dictConfig

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "fmt": "%(levelprefix)s %(asctime)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",

        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "rich.logging.RichHandler"
        },
    },
    "loggers": {
        # "gde": {"handlers": ["default"], "level": "DEBUG"},
        "we_worker": {"handlers": ["default"], "level": "DEBUG"},
    }
}


def configure_logging():
    dictConfig(log_config)
