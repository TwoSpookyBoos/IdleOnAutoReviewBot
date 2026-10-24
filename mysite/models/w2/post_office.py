from functools import cached_property

from consts.idleon.lava_func import lava_func
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class PostOfficeBox:
    def __init__(self, info: dict, level: int | None):
        self.name: str = info["Name"]
        self.tab: str = info["Tab"]
        self.max_level: int = info["Max Level"]
        self.level: int = level or 0
        # Boxes missing from the save get no bonus at all
        self.bonus_1_value: float = self._bonus(info, 1, level)
        self.bonus_2_value: float = self._bonus(info, 2, level)
        self.bonus_3_value: float = self._bonus(info, 3, level)

    @staticmethod
    def _bonus(info: dict, slot: int, level: int | None) -> float:
        if level is None:
            return 0
        # Bonuses 2 and 3 only start counting past their min level
        min_count = info.get(f"{slot}_minCount", 0)
        if level < min_count:
            return 0
        return lava_func(
            info[f"{slot}_funcType"],
            level - min_count,
            info[f"{slot}_x1"],
            info[f"{slot}_x2"],
        )


class PostOffice:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        self.completing_orders: int = safer_convert(raw_data.get('CYDeliveryBoxComplete', 0), 0)
        self.streak_bonuses: int = safer_convert(raw_data.get('CYDeliveryBoxStreak', 0), 0)
        self.miscellaneous: int = safer_convert(raw_data.get('CYDeliveryBoxMisc', 0), 0)
        self.upgrade_vault: int = safer_convert(safer_index(raw_optlacc, 347, 0), 0)

    @cached_property
    def total_boxes_earned(self) -> int:
        return self.completing_orders + self.streak_bonuses + self.miscellaneous + self.upgrade_vault
