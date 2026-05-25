from locale import currency
from math import floor

from consts.consts_autoreview import ValueToMulti
from consts.consts_w7 import zenith_market_upgrade_data
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index, safer_math_pow

logger = get_logger(__name__)


class ZenithMarketUpgrade:
    def __init__(self, info: dict, level: int, index: int):
        self.name = info["Name"]
        self.description_template = info["Description Template"]
        self.level = level
        self.max_level = info["Max Level"]
        self.base_price = info["Base Price"]
        self.price_mult_per_level = info["Price Mult per Level"]
        self.bonus_per_level = info["Bonus per Level"]
        self.price = floor(self.level + self.base_price * safer_math_pow(self.price_mult_per_level, self.level))
        self.value = 0

    def calculate_bonus(self):
        self.value = self.level * self.bonus_per_level

    def get_advice(self):
        description = self.description_template
        if "}" in description:
            description = description.replace("}", str(ValueToMulti(self.value)))
        elif "{" in description:
            description = description.replace("{", str(self.value))
        return Advice(
            label=f"{self.name}:<br>{description}",
            picture_class="zenith-market",
            resource="zenith-cluster",
            progression=self.level,
            goal=self.max_level,
        )



class ZenithMarket(dict[str, ZenithMarketUpgrade]):
    def __init__(self, raw_data: dict):
        raw_spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        if not raw_spelunk_info:
            logger.warning("Zenith Market data not present.")
        market_upgrade_levels: list[int] = safer_index(raw_spelunk_info, 45, [])
        for index, info in enumerate(zenith_market_upgrade_data):
            level = safer_index(market_upgrade_levels, index, 0)
            upgrade = ZenithMarketUpgrade(info, level, index)
            self[upgrade.name] = upgrade

    def calculate_bonuses(self):
        for upgrade in self.values():
            upgrade.calculate_bonus()
