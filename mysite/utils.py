import logging
import os
import re
import sys

from flask import g
from ua_parser import user_agent_parser
from werkzeug.user_agent import UserAgent
from werkzeug.utils import cached_property

from config import app


class ParsedUserAgent(UserAgent):
    @cached_property
    def _details(self):
        return user_agent_parser.Parse(self.string)

    @property
    def os_name(self):
        return self._details["os"]["family"]

    @property
    def browser_name(self):
        return self._details["user_agent"]["family"]

    @property
    def os_version(self):
        return ".".join(
            part
            for key in ("major", "minor", "patch")
            if (part := self._details["os"][key]) is not None
        )

    @property
    def browser_version(self):
        return ".".join(
            part
            for key in ("major", "minor", "patch")
            if (part := self._details["user_agent"][key]) is not None
        )

    @property
    def os(self):
        return f"{self.os_name} ({self.os_version})"

    @property
    def browser(self):
        return f"{self.browser_name} ({self.browser_version})"


def pl(_list: list, suffix_singular: str = "", suffix_plural: str = "s") -> str:
    """Pluralize"""
    return suffix_plural if len(_list) > 1 else suffix_singular


DEFAULT_FORMAT = (
    "%(asctime)s | %(name)s | %(funcName)s:%(lineno)d~ [%(levelname)s] %(message)s"
)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not _try_colorise(logger):
        _set_regular_logger(logger)

    return logger


def _try_colorise(logger):
    is_local_instance = os.environ.get("PYTHONANYWHERE_DOMAIN", None) is None
    if is_local_instance:
        import coloredlogs

        coloredlogs.DEFAULT_FIELD_STYLES["levelname"]["color"] = "white"
        coloredlogs.install(
            level="DEBUG", fmt=DEFAULT_FORMAT, stream=sys.stdout, logger=logger
        )
    return is_local_instance


def _set_regular_logger(logger: logging.Logger):
    formatter = logging.Formatter(DEFAULT_FORMAT)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)

    logger.addHandler(handler)


def browser_data_logger() -> logging.Logger:
    # create logger with 'spam_application'
    logger = logging.getLogger("browser_data")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(app.config["LOGS"] / "browser_data.log")
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    return logger


def letterToNumber(inputLetter: str) -> int:
    return "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(inputLetter)


def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "data"):
            return cls(*args, **kwargs)
        return g.data

    return getinstance


def kebab(string: str) -> str:
    """
    Converts any string to kebab-case format.
    Spaces turn to hyphens, non-word characters are removed.
    """
    return re.sub(r"[^\w-]", "", string.lower().replace(" ", "-"))
