from functools import cached_property

from utils.safer_data_handling import safe_loads, safer_convert, safer_index


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
