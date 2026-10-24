from functools import cached_property
from math import ceil, floor

from consts.consts_autoreview import ValueToMulti
from consts.consts_w1 import forge_upgrades_dict
from consts.w1.forge import (
    bar_ore_costs,
    base_ore_capacity,
    godshard_card_ore_capacity_per_star,
    max_ore_capacity,
    skill_mastery_ore_capacity,
    skill_mastery_smithing_levels,
    vitamin_d_ore_capacity,
)
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
        self.vitamin_d_complete: bool = False
        self.skill_mastery_unlocked: bool = False
        self.total_smithing_levels: int = 0
        self.total_ore_capacity: int = 0

    @property
    def skill_mastery_active(self) -> bool:
        return (
            self.skill_mastery_unlocked
            and self.total_smithing_levels >= skill_mastery_smithing_levels
        )

    def calculate_ore_capacity(
        self,
        *,
        arcade_bonus: float,
        godshard_stars: int,
        forge_stamp: float,
        bribe: float,
        vault_beeg_forge: float,
        majik_beeg_forge: float,
        vitamin_d_complete: bool,
        skill_mastery_unlocked: bool,
        total_smithing_levels: int,
    ):
        self.vitamin_d_complete = vitamin_d_complete
        self.skill_mastery_unlocked = skill_mastery_unlocked
        self.total_smithing_levels = total_smithing_levels
        group_a = ValueToMulti(
            arcade_bonus + godshard_card_ore_capacity_per_star * (godshard_stars + 1)
        )
        group_b = ValueToMulti(forge_stamp)
        group_c = ValueToMulti(bribe + vault_beeg_forge)
        group_d = ValueToMulti(
            vitamin_d_ore_capacity * vitamin_d_complete
            + skill_mastery_ore_capacity * self.skill_mastery_active
        )
        self.total_ore_capacity = ceil(min(
            max_ore_capacity,
            (base_ore_capacity + self.ore_capacity)
            * group_a * group_b * group_c * group_d * majik_beeg_forge,
        ))

    def get_vitamin_d_advice(self) -> Advice:
        value = vitamin_d_ore_capacity * self.vitamin_d_complete
        return Advice(
            label=f"{{{{ Achievements|#achievements }}}} - Vitamin D-licious: "
                  f"+{value}/{vitamin_d_ore_capacity}%",
            picture_class='vitamin-d-licious',
            progression=int(self.vitamin_d_complete),
            goal=1,
        )

    def get_skill_mastery_advice(self) -> Advice:
        value = (
            skill_mastery_ore_capacity * self.skill_mastery_active
            * self.skill_mastery_unlocked
        )
        return Advice(
            label=f"{{{{ Rift|#rift }}}} - Skill Mastery at "
                  f"{skill_mastery_smithing_levels} Smithing: "
                  f"+{value}/{skill_mastery_ore_capacity}%",
            picture_class='smithing',
            progression=self.total_smithing_levels,
            goal=skill_mastery_smithing_levels,
        )

    def get_total_capacity_advice(self) -> Advice:
        return Advice(
            label=f"Total Capacity: {self.total_ore_capacity:,}",
            picture_class='empty-forge-slot',
        )

    def get_bar_advice(self) -> list[Advice]:
        advices = []
        for bar_name, ore_cost in bar_ore_costs.items():
            leftover = self.total_ore_capacity % ore_cost
            next_bar = ore_cost - leftover if leftover > 0 else ore_cost
            advices.append(Advice(
                label=f"{floor(self.total_ore_capacity / ore_cost):,} {bar_name}s."
                      f"<br>{next_bar:,} cap to next bar",
                picture_class=bar_name,
                progression=ore_cost - next_bar,
                goal=ore_cost,
            ))
        return advices

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
