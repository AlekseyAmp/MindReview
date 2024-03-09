import logging

from pydantic import BaseModel


class Settings(BaseModel):
    LOGGING_CONFIG: dict = {
        "version": 1,
        "disable_existing_loggers": True,
        "formatters": {
            "standard": {
                "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            },
        },
        "handlers": {
            "default": {
                "level": "INFO",
                "formatter": "standard",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "": {
                "level": "INFO",
                "handlers": ["default"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["default"]
            },
            "uvicorn.access": {
                "level": "INFO",
                "handlers": ["default"]
            }
        }
    }


logging.config.dictConfig(Settings().LOGGING_CONFIG)
logger = logging.getLogger(__name__)
