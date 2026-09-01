from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.sushi_station import (
    sushi_upgrades,
    sushi_upgrade_shop_order,
    sushi_milestone_data,
    sushi_max_tier,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class SushiUpgrade:
    def __init__(self, index: int, info: dict, level: int):
        self.index = index
        self.name = info["Name"]
        self.description = info["Description"]
        self.max_level = info["Max Level"]
        self.value_per_level = info["Value Per Level"]
        self.level = level
        self.value = 0

    def calculate_bonus(self):
        # TODO: secondary "$"/"^" placeholder formulas not modeled
        self.value = self.level * self.value_per_level

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Sushi Station|#sushi-station}} - "
        max_value = self.max_level * self.value_per_level
        if "{" in self.description:
            value, displayed_max = self.value, max_value
        else:
            value, displayed_max = ValueToMulti(self.value), ValueToMulti(max_value)
        bonus = f"{round_and_trim(value)}/{round_and_trim(displayed_max)}"
        description = self.description.replace("{", bonus).replace("}", bonus)
        label += f"{self.name}:<br>{description}"
        return Advice(
            label=label,
            picture_class=f"sushi-upg-{self.index}",
            progression=self.level,
            goal=self.max_level,
        )


class SushiMilestoneBonus:
    def __init__(self, index: int, info: dict, unique_sushi_count: int):
        self.index = index
        self.name = info["Name"]
        self.description = info["Description"]
        self.value = info["Value"]
        self.unlocked = unique_sushi_count > index

    def get_advice(self) -> Advice:
        is_multi = "}" in self.description
        displayed_value = ValueToMulti(self.value) if is_multi else self.value
        placeholder = "}" if is_multi else "{"
        rendered = self.description.replace(placeholder, f"{round_and_trim(displayed_value)}")
        return Advice(
            label=f"Unique Sushi #{self.index + 1}: {rendered}",
            picture_class=f"sushi-{self.index}",
            progression=int(self.unlocked),
            goal=1,
        )

    @property
    def unlocked_value(self) -> float:
        return self.value if self.unlocked else 0


class SushiStation:
    def __init__(self, raw_data: dict):
        raw_sushi = safe_loads(raw_data.get("Sushi", []))
        if not raw_sushi:
            logger.warning("Sushi Station data not present.")

        upgrade_levels = safer_index(raw_sushi, 2, [])
        self.upgrades: dict[str, SushiUpgrade] = {}
        for index in sushi_upgrade_shop_order:
            info = sushi_upgrades[index]
            level = safer_index(upgrade_levels, index, 0)
            upgrade = SushiUpgrade(index, info, level)
            self.upgrades[upgrade.name] = upgrade

        # "UniqueSushi" in source: highest consecutive tier (from 0) that's been cooked
        tier_made = safer_index(raw_sushi, 5, [])
        unique_sushi = 0
        for tier in range(sushi_max_tier + 1):
            if safer_index(tier_made, tier, -1) < 0:
                break
            unique_sushi += 1
        self.unique_sushi = unique_sushi

        self.milestones: dict[str, SushiMilestoneBonus] = {}
        for index, info in enumerate(sushi_milestone_data):
            milestone = SushiMilestoneBonus(index, info, unique_sushi)
            self.milestones[milestone.name] = milestone

    def calculate_bonuses(self):
        for upgrade in self.upgrades.values():
            upgrade.calculate_bonus()

    def get_milestone_bonus_value(self, name: str) -> float:
        # "RoG_BonusQTY" in source
        return self.milestones[name].unlocked_value

    def get_unique_sushi_advice(self) -> Advice:
        highest_tier_icon = (
            f"sushi-{self.unique_sushi - 1}" if self.unique_sushi > 0 else "placeholder"
        )
        return Advice(
            label=f"Unique Sushi (consecutive tiers cooked): {self.unique_sushi}",
            picture_class=highest_tier_icon,
            progression=self.unique_sushi,
            goal=len(self.milestones),
        )
