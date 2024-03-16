from pathlib import Path

from config import app
from utils import get_logger

import yaml


logger = get_logger(__name__)

items_path = Path(app.static_folder) / 'items.yaml'
ITEM_NAME_DICT = yaml.load(open(items_path), yaml.Loader)
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
