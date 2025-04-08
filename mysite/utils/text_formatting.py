import enum
import re
from pathlib import Path

import yaml

from config import app
from .logging import get_logger, log_unknown_item


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
    return (
        isinstance(data, str)
        and (
            len(data) < 16
            or 'idleonefficiency.com' in data.lower()
            or 'idleontoolbox.com' in data.lower()
            # or 'idleonleaderboards.com in data.lower()
        )
    )


def json_schema_valid(data) -> bool:
    return isinstance(data, str) and data.startswith("{") and data.endswith("}")


class InputType(enum.Enum):
    """What did the user send to us? His username, one of the links to public profiles, or a data JSON?"""
    ALL = 'all'
    IE = 'IE'
    IT = 'IT'
    LB = 'LB'
    JSON = 'JSON'


pattern = re.compile(rf"""
^                                                                # line start
(?:                                                              # non-capturing group 1 open
    (?P<{InputType.ALL.value}>[\w ]+)                            # match plain username
    |                                                            # or
    .*?                                                          # skip prefix if any
    (?:                                                          # non-capturing group 2 open
        [?&]profile=(?P<{InputType.IT.value}>[\w.]+)             # match IT  https://idleontoolbox.com/?profile=<username>
        |                                                        # or
        (?P<{InputType.IE.value}>[\w.]+)\.idleonefficiency\.com  # match IE  https://<username>.idleonefficiency.com/
        |                                                        # or
        profiles/(?P<{InputType.LB.value}>[\w.]+)                # match LB  https://idleonleaderboards.com/profiles/<username>
    )                                                            # non-capturing group 2 close
    .*                                                           # skip whatever follows
)                                                                # non-capturing group 1 close
$                                                                # line end
""", re.VERBOSE)

def format_character_name(name: str) -> tuple[str, InputType]:
    groups = pattern.match(name).groupdict()
    input_type, formatted_name = next((InputType(k), v) for k, v in groups.items() if v)
    # logger.debug(f"{name = }, {formatted_name = }")
    return formatted_name, input_type


__items_path = Path(app.static_folder) / 'items.yaml'
__fake_items_path = Path(app.static_folder) / 'fake_items.yaml'

with open(__items_path, 'r') as f:
    ITEM_NAME_DICT = yaml.load(f, yaml.Loader)
    ITEM_CODE_DICT = {v: k for k, v in ITEM_NAME_DICT.items()}

with open(__fake_items_path) as f2:
    FAKE_ITEM_NAME_DICT = yaml.load(f2, yaml.Loader)
    FAKE_ITEM_CODE_DICT = {v: k for k, v in FAKE_ITEM_NAME_DICT.items()}

ITEM_NAME_DICT.update(FAKE_ITEM_NAME_DICT)
ITEM_CODE_DICT.update(FAKE_ITEM_CODE_DICT)


def _get_item_name(_dict, name):
    if name and name != 'null':
        try:
            return _dict[name]
        except KeyError:
            logger.debug(f"Unknown item: '{name}'")
            log_unknown_item(name)
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
    # "QQQ": 1e21,
    # "QQ": 1e18,
    "Q": 1e15,
    "T": 1e12,
    "B": 1e9,
    "M": 1e6,
    "K": 1e3,
    "": 1
}
def notateNumber(inputType: str, inputValue: float, decimals=2, overrideCharacter="", matchString=None):
    """
    :param inputType: 'Basic' or 'Match'
    :param inputValue: The Value needing to be notated
    :param decimals: The number of decimals to show after
    :param overrideCharacter: Single character string to override the default matching. Must be present in stringToDecimal dictionary.
    :param matchString: The entire value to match to
    :return:
    """
    match inputType:
        case "Basic":
            if float(abs(inputValue)) >= 1e18:
                result = f"{inputValue:.{decimals}e}"
            elif float(abs(inputValue)) < 1e3:
                result = f"{inputValue:.{decimals}f}"
            else:
                for k, v in stringToDecimal.items():
                    if float(abs(inputValue)) >= v:
                        result = f"{inputValue / v:.{decimals}f}{k}"
                        break
        case "Match":
            if not overrideCharacter and isinstance(matchString, str):
                if 'e+' in matchString:
                    overrideCharacter = matchString.split('e+')[-1]
                elif matchString[-1].isalpha():
                    overrideCharacter = matchString[-1]
                else:
                    overrideCharacter = ''
            if overrideCharacter and overrideCharacter.isalpha():
                result = f"{inputValue / stringToDecimal[overrideCharacter.upper()]:.{decimals}f}{overrideCharacter.upper()}"
            elif overrideCharacter and overrideCharacter.isdigit():
                result = f"{inputValue / float(f'1e{overrideCharacter}'):.{decimals}f}e+{overrideCharacter}"
            else:
                result = notateNumber('Basic', inputValue, decimals)
            # if matchString.upper() in stringToDecimal:
            #
            # else:
            #     logger.debug(f"Unexpected matchString: {matchString}")
            #     result = f"{inputValue:,}"

        case _:
            result = f"{inputValue:,}"
    return result
