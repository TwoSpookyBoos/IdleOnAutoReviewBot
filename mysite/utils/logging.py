import os
import sys
import uuid

from flask import request
from ua_parser import user_agent_parser
from werkzeug.user_agent import UserAgent
from werkzeug.utils import cached_property

from config import app
import logging


DEFAULT_FORMAT = (
    "%(asctime)s | %(name)s | %(funcName)s:%(lineno)d~ [%(levelname)s] %(message)s"
)


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


def get_logger(name: str) -> logging.Logger:
    logger_ = logging.getLogger(name)
    logger_.setLevel(logging.DEBUG)

    if not _try_colorise(logger_):
        _set_regular_logger(logger_)

    return logger_


def browser_data_logger() -> logging.Logger:
    logger = logging.getLogger("browser_data")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(message)s")

    handler = logging.FileHandler(app.config["LOGS"] / "browser_data.log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def name_for_logging(name_or_data, headerData, default=str(uuid.uuid4())[:8]) -> str:
    if isinstance(name_or_data, str) and name_or_data:
        name = name_or_data
    elif isinstance(name_or_data, dict) and headerData and headerData.first_name:
        name = headerData.first_name.lower()
    else:
        name = default

    return name


__user_agent_logger = browser_data_logger()


def log_browser_data(player):
    ua_string = request.headers.get("User-Agent")
    user_agent = ParsedUserAgent(ua_string)
    __user_agent_logger.info("%s | %s - %s", player, user_agent.os, user_agent.browser)

def unknown_item_logger() -> logging.Logger:
    logger = logging.getLogger("unknown_items")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s | %(message)s")

    handler = logging.FileHandler(app.config["LOGS"] / "unknown_items.log")
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


__unknown_item_logger = unknown_item_logger()

def log_unknown_item(itemCodeName: str):
    __unknown_item_logger.info(f"Unknown Item: {itemCodeName}")


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
