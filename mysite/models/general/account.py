import copy

from consts.consts_autoreview import lowest_accepted_version
from consts.w1.stamps import stamp_types
from consts.consts_w7 import coral_reef_bonuses, legend_talents_bonuses
from models.custom_exceptions import VeryOldDataException
from models.advice.advice import Advice
from models.w1.stamps import Stamps
from models.w6.emperor import Emperor
from models.w6.beanstalk import Beanstalk
from models.w6.sneaking import Sneaking
from models.w7.spelunk import Spelunk
from utils.safer_data_handling import safe_loads, safer_get
from utils.text_formatting import InputType
from flask import g


def session_singleton(cls):
    def getinstance(*args, **kwargs):
        if not hasattr(g, "account"):
            return cls(*args, **kwargs)
        return g.account

    return getinstance

@session_singleton
class Account:

    def __init__(self, json_data, source_string: InputType):
        self.raw_data = safe_loads(json_data)
        self.version = safer_get(self.raw_data, 'DoOnceREAL', 0.00)
        if self.version < lowest_accepted_version:
            raise VeryOldDataException(self.version)
        self.data_source = source_string.value
        self.alerts_Advices = {
            'General': [],
            'World 1': [],
            'World 2': [],
            'World 3': [],
            'World 4': [],
            'World 5': [],
            'The Caverns Below': [],
            'World 6': []
        }
        #General
        self.inventory = {
            'Characters Missing Bags': {},
            'Account Wide Inventory': {},
            'Account Wide Inventory Slots Owned': 0,
            'Account Wide Inventory Slots Max': 0,
        }
        self.gemshop = {
            'Purchases': {},
            'Bundle Data Present': None,
            'Bundles': {}
        }
        self.storage = {
            'Used Chests': [],
            'Used Chests Slots': 0,
            'Missing Chests': [],
            'Missing Chests Slots': 0,
            'Other Storage': {},
            'Other Slots Owned': 0,
            'Other Slots Max': 0,
            'Total Slots Owned': 0,
            'Total Slots Max': 0
        }
        #W1
        self.stamps: Stamps = Stamps()
        self.stamp_totals: dict[str, int] = {"Total": 0, **{stamp_type: 0 for stamp_type in stamp_types}}
        self.basketball = {
            'Upgrades': {}
        }
        self.darts = {
            'Upgrades': {}
        }
        # W6
        self.sneaking: Sneaking = Sneaking(self.raw_data)
        self.beanstalk: Beanstalk = Beanstalk(self.raw_data)
        self.emperor: Emperor = Emperor(self.raw_data)
        # W7
        self.spelunk = Spelunk(self.raw_data)
        self.coral_reef = {
            'Town Corals': 0,
            'Reef Corals': copy.deepcopy(coral_reef_bonuses)
        }
        self.legend_talents = {
            'Talents': copy.deepcopy(legend_talents_bonuses)
        }
        self.advice_for_money = {
            'Upgrades': {},
        }

    def add_alert_list(
        self, group_name: str, advice_list: list[Advice | None] | set[Advice | None]
    ):
        advice_list = [item for item in advice_list if item is not None]
        self.alerts_Advices[group_name].extend(advice_list)

    def get_current_max_talent(self, name: str) -> int:
        """
        Get the max level of characters talents from their current preset set.

        :param name: talent name.
        :returns: Max talent level or 0.
        """
        if name == "Generational Gemstones":
            return max(
                [
                    talent_level + char.total_bonus_talent_levels
                    for char in self.wws
                    if (talent_level := char.current_preset_talents.get("432", 0)) > 0
                ],
                default=0,
            )
        return 0
