import re
from pathlib import Path

import yaml
from flask import g

from config import app
from .logging import get_logger


logger = get_logger(__name__)


def pl(_list, suffix_singular: str = "", suffix_plural: str = "s") -> str:
    """Pluralize"""
    length = _list if isinstance(_list, int) else len(_list)
    return suffix_plural if length > 1 else suffix_singular


def letterToNumber(inputLetter: str) -> int:
    return "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ".index(inputLetter)


def numberToLetter(inputNumber: int) -> str:
    return "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"[inputNumber]


def kebab(string: str) -> str:
    """
    Converts any string to kebab-case format.
    Spaces turn to hyphens, non-word characters are removed.
    """
    return re.sub(r"[^\w-]", "", string.lower().replace(" ", "-"))


def is_username(data) -> bool:
    return isinstance(data, str) and len(data) < 16


def json_schema_valid(data) -> bool:
    return isinstance(data, str) and data.startswith("{") and data.endswith("}")


def format_character_name(name: str) -> str:
    name = name.strip().lower().replace(" ", "_")

    return name


__items_path = Path(app.static_folder) / 'items.yaml'
ITEM_NAME_DICT = yaml.load(open(__items_path), yaml.Loader)
ITEM_CODE_DICT = {v: k for k, v in ITEM_NAME_DICT.items()}


def _get_item_name(_dict, name):
    try:
        return _dict[name]
    except KeyError:
        logger.debug("Unknown item: %s", name)
        return f"Unknown-{name}"


def getItemDisplayName(codeName):
    return _get_item_name(ITEM_NAME_DICT, codeName)


def getItemCodeName(itemName):
    return  _get_item_name(ITEM_CODE_DICT, itemName)
