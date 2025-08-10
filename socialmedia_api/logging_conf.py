import logging
from logging.config import dictConfig

from socialmedia_api.config import DevConfig, config


def obfuscated(email: str, obfuscated_length: int) -> str:
    characters = email[:obfuscated_length]
    first, last = email.split("@")
    return characters + "*" * (len(first) - obfuscated_length) + "@" + last


class EmailObfuscationFilter(logging.Filter):
    """
    def filter(self, record: logging.LogRecord) -> bool:
        record.your_Variable = "123" # This variable will be available for the formatter
        return True # if True is return => we display, else no
    """

    def __init__(self, name: str = "", obfuscated_length: int = 2) -> None:
        super().__init__(name)
        self.obfuscated_length = obfuscated_length

    def filter(self, record: logging.LogRecord) -> bool:
        if "email" in record.__dict__:
            record.email = obfuscated(record.email, self.obfuscated_length)
        return True


def configure_logging() -> None:
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",  # Parameter of this functions
                    "uuid_length": 8 if isinstance(config, DevConfig) else 32,
                    "default_value": "-",
                },
                "email_obfuscation": {
                    "()": EmailObfuscationFilter,
                    "obfuscated_length": 2 if isinstance(config, DevConfig) else 0,
                },
            },
            "formatters": {
                "console": {
                    "class": "logging.Formatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "(%(correlation_id)s) %(name)s:%(lineno)d - %(message)s",
                },
                "file": {
                    "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "%(asctime)s %(msecs)03d %(levelname)-8s %(correlation_id)s %(name)s %(lineno)d %(message)s",
                },
            },
            "handlers": {
                "default": {
                    "class": "rich.logging.RichHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "rotating_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "level": "DEBUG",
                    "filename": "socialmedia_api.log",
                    "maxBytes": 1024 * 1024 * 1,  # 1MB
                    "backupCount": 5,
                    "encoding": "utf8",
                    "formatter": "file",
                    "filters": ["correlation_id", "email_obfuscation"],
                },
                "logtail": {
                    "class": "logtail.LogtailHandler",
                    "level": "DEBUG",
                    "formatter": "console",
                    "filters": ["correlation_id", "email_obfuscation"],
                    "source_token": "DzHn8we4N2MjJVgn1o7Rqwvp",
                },
            },
            "loggers": {
                "uvicorn": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "INFO",
                },
                "socialmedia_api": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "DEBUG" if isinstance(config, DevConfig) else "INFO",
                    "propagate": False,
                },
                "databases": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "WARNING",
                },
                "aiosqlite": {
                    "handlers": ["default", "rotating_file", "logtail"],
                    "level": "WARNING",
                },
            },
        }
    )
