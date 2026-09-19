from functools import cached_property

from consts.consts_w1 import forge_upgrades_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class ForgeUpgrade:
    def __init__(self, index: int, info: dict, purchased: int):
        self.index: int = index
        self.name: str = info['UpgradeName']
        self.max_purchases: int = info['MaxPurchases']
        self.purchased: int = purchased

    @property
    def maxed(self) -> bool:
        return self.purchased >= self.max_purchases

    def get_advice(self) -> Advice:
        return Advice(
            label=self.name,
            picture_class='forge-upgrades',
            progression=self.purchased,
            goal=self.max_purchases,
        )


class ForgeUpgrades(dict[str, ForgeUpgrade]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_forge_upgrades = safe_loads(raw_data.get('ForgeLV', []))
        for index, info in forge_upgrades_dict.items():
            purchased = safer_convert(safer_index(raw_forge_upgrades, index, 0), 0)
            self[info['UpgradeName']] = ForgeUpgrade(index, info, purchased)

    @cached_property
    def total_purchased(self) -> int:
        return sum(upgrade.purchased for upgrade in self.values())

    @staticmethod
    def _ore_capacity_at(purchased: int) -> float:
        return (2 + 0.5 * (purchased - 1)) * purchased * 10

    @cached_property
    def ore_capacity(self) -> float:
        return self._ore_capacity_at(self['Ore Capacity Boost'].purchased)

    def get_ore_capacity_advice(self) -> Advice:
        upgrade = self['Ore Capacity Boost']
        return Advice(
            label=f"Forge Upgrade: {upgrade.name}: "
                  f"+{int(self.ore_capacity)}/{int(self._ore_capacity_at(upgrade.max_purchases))}",
            picture_class='forge-upgrades',
            progression=upgrade.purchased,
            goal=upgrade.max_purchases,
        )
