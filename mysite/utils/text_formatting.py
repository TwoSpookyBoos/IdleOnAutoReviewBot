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

with open(__items_path, 'r') as f:
    ITEM_NAME_DICT = yaml.load(f, yaml.Loader)
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


stringToDecimal = {
    "QQQ": 1e21,
    "QQ": 1e18,
    "Q": 1e15,
    "T": 1e12,
    "B": 1e9,
    "M": 1e6,
    "K": 1e3,
    "": 1
}
def notateNumber(inputType: str, inputValue: float, decimals=2, matchString="B"):
    match inputType:
        case "Basic":
            if float(inputValue) >= 1e24:
                result = f"{inputValue:.{decimals}e}"
            elif float(inputValue) < 1e3:
                result = f"{inputValue:,}"
            else:
                for k, v in stringToDecimal.items():
                    if float(inputValue) >= v:
                        result = f"{inputValue / v:.{decimals}f}{k}"
                        break
        case "Match":
            result = f"{inputValue / stringToDecimal[matchString.upper()]:.{decimals}f}{matchString.upper()}"
            # if matchString.upper() in stringToDecimal:
            #
            # else:
            #     logger.debug(f"Unexpected matchString: {matchString}")
            #     result = f"{inputValue:,}"
        case _:
            result = f"{inputValue:,}"
    return result
