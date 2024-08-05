import re
from pathlib import Path

import yaml

from config import app
from .logging import get_logger


logger = get_logger(__name__)
numeralList = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

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
    if name:
        try:
            return _dict[name]
        except KeyError:
            logger.debug(f"Unknown item: '{name}'")
            return f"Unknown-'{name}'"
    else:
        #Don't need a logger message if the unknown item is an empty string
        return f"Unknown-'{name}'"


def getItemDisplayName(codeName):
    return _get_item_name(ITEM_NAME_DICT, codeName)


def getItemCodeName(itemName):
    if itemName != "":
        return _get_item_name(ITEM_CODE_DICT, itemName)

def numeralToNumber(numeral: str):
    if numeral in numeralList:
        return numeralList.index(numeral)+1

def notateNumber(type: str, input: float, decimals=2, matchString="B"):
    match type:
        case "Basic":
            if float(input) >= 1e24:
                result = f"{input:.{decimals}e}"
            elif float(input) >= 1e21:
                result = f"{input / 1e21:.{decimals}f}QQQ"
            elif float(input) >= 1e18:
                result = f"{input / 1e18:.{decimals}f}QQ"
            elif float(input) >= 1e15:
                result = f"{input / 1e15:.{decimals}f}Q"
            elif float(input) >= 1e12:
                result = f"{input / 1e12:.{decimals}f}T"
            elif float(input) >= 1e9:
                result = f"{input/1e9:.{decimals}f}B"
            elif float(input) >= 1e6:
                result = f"{input/1e6:.{decimals}f}M"
            # I'm not personally a fan of reducing to K, but helps Mobile not get scuffed
            elif float(input) >= 1e3:
                result = f"{input/1e3:.{decimals}f}K"
            else:
                result = f"{input:,}"
        case "Match":
            if matchString == "QQQ":
                result = f"{input / 1e21:.{decimals}f}QQQ"
            elif matchString == "QQ":
                result = f"{input / 1e18:.{decimals}f}QQ"
            elif matchString == "Q":
                result = f"{input / 1e15:.{decimals}f}Q"
            elif matchString == "T":
                result = f"{input / 1e12:.{decimals}f}T"
            elif matchString == "B":
                result = f"{input / 1e9:.{decimals}f}B"
            elif matchString == "M":
                result = f"{input / 1e6:.{decimals}f}M"
            elif matchString == "K":
                result = f"{input / 1e3:.{decimals}f}K"
            else:
                logger.debug(f"Unexpected matchString: {matchString}")
                result = f"{input:,}"
        case _:
            result = f"{input:,}"
    return result
