from math import ceil, floor

from consts.consts_autoreview import ValueToMulti
from consts.consts_w4 import (
    cooking_close_enough,
    cooking_meal_dict,
    max_cooking_ribbon,
    max_cooking_tables,
    max_meal_count,
    max_meal_plate_level,
)
from models.advice.advice import Advice
from models.master_classes.grimoire import GrimoireUpgrade
from models.w6.sneaking import Emporium
from models.w7.spelunk import SpelunkCave
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_convert, safer_index
from utils.text_formatting import pl

logger = get_logger(__name__)


class Meal:
    def __init__(self, index: int, info: dict, level: int, mastery: int):
        self.name: str = info["Name"]
        self.index: int = index
        self.level: int = level
        self.mastery: int = mastery
        self.base_value: float = info["BaseValue"]
        self.effect: str = info["Effect"]
        self.image: str = info["Image"]
        self.world: int = info["World"]
        self.ribbon_tier: int = 0
        self.ribbon_multi: float = 1
        # "BonusMultiCook" in source: meal mastery. Last updated in v2.531.0
        self.mastery_multi: float = 1 + mastery / (mastery + 5)
        self.value: float = level * self.base_value
        self.description: str = self.effect

    def calculate_value(self, meal_multi: float, ribbon_multi: float):
        self.ribbon_multi = ribbon_multi
        self.value = (
            float(self.value) * meal_multi * self.mastery_multi * self.ribbon_multi
        )
        if "{" in self.effect:
            self.description = self.effect.replace("{", f"{self.value:,.3f}")
        elif "}" in self.effect:
            self.description = self.effect.replace("}", f"{self.value:,.3f}")

    def get_advice(self) -> Advice:
        return Advice(
            label=f"{self.name}: {self.description}"
            f"<br>Tier {self.ribbon_tier} Ribbon = {self.ribbon_multi:.3f}x multi",
            picture_class=self.image,
            progression=self.level,
            goal=max_meal_plate_level,
            resource=f"meal-ribbon-{self.ribbon_tier}",
            informational=True,
        )

    def get_bonus_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"{{{{ Meal|#cooking }}}} - {self.name}: "
            f"{self.description}{additional_text}",
            picture_class=self.image,
            progression=self.level,
            goal=max_meal_plate_level,
        )


class Meals(dict[str, Meal]):
    def __init__(self, raw_data: dict, version: float):
        super().__init__()
        # Level, then 3 more per-plate lists
        raw_meals = safe_loads(
            raw_data.get("Meals", [[0] * max_meal_count for _ in range(4)])
        )
        if len(raw_meals[0]) < max_meal_count:
            logger.warning(
                f"Data's meal levels list shorter than expected: "
                f"{len(raw_meals[0])} < {max_meal_count}"
            )
            while len(raw_meals[0]) < max_meal_count:
                raw_meals[0].append(0)
        # CookMaster[0] in source: meal mastery. Last updated in v2.531.0
        raw_mastery = safer_index(safe_loads(raw_data.get("CookMaster", [])), 0, [])
        for index, info in cooking_meal_dict.items():
            self[info["Name"]] = Meal(
                index,
                info,
                parse_number(raw_meals[0][index], 0),
                parse_number(safer_index(raw_mastery, index, 0), 0),
            )

        self.nyan_stacks: int = 0

        raw_ribbons = safe_loads(raw_data.get("Ribbon", []))
        if not raw_ribbons:
            expected = ", as expected" if version < 236 else ""
            logger.warning(f"Meal Ribbons data not present{expected}")
        for meal in self.values():
            try:
                # Ribbon shelf occupies first 28 indexes
                meal.ribbon_tier = safer_convert(raw_ribbons[meal.index + 28], 0)
            except IndexError:
                meal.ribbon_tier = 0
                if raw_ribbons:
                    logger.exception(f"Could not retrieve Ribbon for {meal.name}")

    @property
    def nyanborgir_value(self) -> float:
        return self["Nyanborgir"].value * self.nyan_stacks

    def get_nyanborgir_advice(self) -> Advice:
        return self["Nyanborgir"].get_bonus_advice(
            f"<br>After {self.nyan_stacks} Summoning Level stack{pl(self.nyan_stacks)}:"
            f" {self.nyanborgir_value:,.3f}%"
        )

    @property
    def total_levels(self) -> int:
        return sum(meal.level for meal in self.values())

    @property
    def unlocked_count(self) -> int:
        return sum(meal.level > 0 for meal in self.values())

    @property
    def unlocked_by_world(self) -> dict[int, int]:
        counts = {world: 0 for world in range(9)}
        for meal in self.values():
            counts[meal.world] += meal.level > 0
        return counts

    def unlocked_below(self, level: int) -> int:
        return sum(0 < meal.level < level for meal in self.values())

    def below(self, level: int) -> int:
        return sum(meal.level < level for meal in self.values())

    def calculate_values(
        self,
        black_diamond_value: float,
        shiny_meal_levels: float,
        summoning_multi: float,
        wickerlight_multi: float,
        emperor_set: float,
        cloud_73: bool,
        jelly_rog_60: float,
        max_summoning_level: int,
    ):
        meal_multi = (
            ValueToMulti(black_diamond_value + shiny_meal_levels)
            * summoning_multi
            * wickerlight_multi
        )
        # Nyanborgir stacks once per 50 Summoning levels
        self.nyan_stacks = ceil((max_summoning_level + 1) / 50)
        # _customBlock_Summoning > "RibbonBonus". Last updated in v2.531.0
        # 1 + (floor(5t + floor(t/2)*(4 + 6.5*floor(t/5))) + floor(t/4)*EMPEROR_SET/4
        #   + floor(t/10)*CloudBonus(73) + floor(t/20)*JellyRoG(60)) / 100
        ribbon_multi_table = [
            ValueToMulti(
                floor((5 * tier) + (floor(tier / 2) * (4 + 6.5 * floor(tier / 5))))
                + (floor(tier / 4) * (emperor_set / 4))
                + (floor(tier / 10) * cloud_73)
                + (floor(tier / 20) * jelly_rog_60)
            )
            for tier in range(0, max_cooking_ribbon + 1)
        ]
        for meal in self.values():
            ribbon_multi = ribbon_multi_table[
                min(len(ribbon_multi_table) - 1, meal.ribbon_tier)
            ]
            meal.calculate_value(meal_multi, ribbon_multi)


class Cooking:
    def __init__(self, raw_data: dict, meals: Meals):
        self._meals: Meals = meals
        # Some tables have 10 fields, others 11
        empty_cooking = [[0] * 11 for _ in range(max_cooking_tables)]
        raw_tables = safe_loads(raw_data.get("Cooking", empty_cooking))
        for table in raw_tables:
            if isinstance(table, list):
                while len(table) < 11:
                    table.append(0)
        self.tables: list = raw_tables
        self.tables_owned: int = sum(1 for table in self.tables if table[0] == 2)
        self.max_plate_level: int = 30
        self.max_total_meal_levels: int = max_meal_count * max_meal_plate_level
        self.missing_plate_upgrades: list[Advice] = []

    @property
    def total_meal_levels(self) -> int:
        return self._meals.total_levels

    @property
    def meals_unlocked(self) -> int:
        return self._meals.unlocked_count

    @property
    def meals_unlocked_by_world(self) -> dict[int, int]:
        return self._meals.unlocked_by_world

    @property
    def unlocked_meals_under_11(self) -> int:
        return self._meals.unlocked_below(11)

    @property
    def unlocked_meals_under_30(self) -> int:
        return self._meals.unlocked_below(30)

    @property
    def meals_under_11(self) -> int:
        return self._meals.below(11)

    @property
    def meals_under_30(self) -> int:
        return self._meals.below(30)

    @property
    def current_remaining_meals(self) -> int:
        return self.max_total_meal_levels - self._meals.total_levels

    @property
    def max_remaining_meals(self) -> int:
        return (max_meal_count * max_meal_plate_level) - self._meals.total_levels

    @property
    def close_enough(self) -> bool:
        # Few enough levels left that cooking speed stops mattering
        return self.max_remaining_meals < cooking_close_enough

    @property
    def nmlb_days(self) -> int:
        return sum(
            ceil((max_meal_plate_level - meal.level) / 3)
            for meal in self._meals.values()
        )

    def calculate_max_plate_level(
        self,
        causticolumn_level: int,
        eldritch_unlocked: bool,
        emporium: dict[str, Emporium],
        supreme_head_chef: GrimoireUpgrade,
        lunarheim: SpelunkCave,
    ):
        missing = self.missing_plate_upgrades
        artifact = "{{ Artifact|#sailing }}"
        emporium_link = "{{ Jade Emporium|#sneaking }}"

        # Sailing Artifact tiers, https://idleon.wiki/wiki/Sailing#Artifacts
        self.max_plate_level += 10 * int(causticolumn_level)
        if causticolumn_level < 1:
            missing.append(
                _plate_advice(f"{artifact}: Base Causticolumn", "causticolumn")
            )
        if causticolumn_level < 2:
            missing.append(
                _plate_advice(f"{artifact}: Ancient Causticolumn", "causticolumn")
            )
        if causticolumn_level < 3:
            if eldritch_unlocked:
                missing.append(
                    _plate_advice(f"{artifact}: Eldritch Causticolumn", "causticolumn")
                )
            else:
                missing.append(
                    _plate_advice(
                        f"{artifact}: Eldritch Causticolumn. Eldritch Artifacts are "
                        "unlocked by completing {{ Rift|#rift }} 30",
                        "eldritch-artifact",
                    )
                )
        if causticolumn_level < 4:
            if emporium["Sovereign Artifacts"].obtained:
                missing.append(
                    _plate_advice(f"{artifact}: Sovereign Causticolumn", "causticolumn")
                )
            else:
                missing.append(
                    _plate_advice(
                        f"{artifact}: Sovereign Causticolumn. Sovereign Artifacts "
                        f"unlock from {emporium_link}",
                        "sovereign-artifacts",
                    )
                )
        if causticolumn_level < 5:
            # TODO: Verify if player has upgrade from first Spelunking Cave
            missing.append(
                _plate_advice(
                    f"{artifact}: Omnipotent Causticolumn. Omnipotent Artifacts unlock "
                    "from the first Spelunking Cave",
                    "causticolumn",
                )
            )
        if causticolumn_level < 6:
            # TODO: Verify if player has upgrade from Research
            missing.append(
                _plate_advice(
                    f"{artifact}: Transcendent Causticolumn. Transcendent Artifacts "
                    "unlock from Research",
                    "causticolumn",
                )
            )

        # Jade Emporium
        for upgrade_name, image in (
            ("Papa Blob's Quality Guarantee", "papa-blob-s-quality-guarantee"),
            (
                "Chef Geustloaf's Cutting Edge Philosophy",
                "chef-geustloaf-s-cutting-edge-philosophy",
            ),
        ):
            if emporium[upgrade_name].obtained:
                self.max_plate_level += 10
            else:
                missing.append(
                    _plate_advice(
                        f'Purchase "{upgrade_name}" from {emporium_link}', image
                    )
                )

        # Grimoire
        self.max_plate_level += supreme_head_chef.level
        if supreme_head_chef.level < supreme_head_chef.max_level:
            missing.append(
                _plate_advice(
                    'Upgrade "Supreme Head Chef Status" within '
                    "{{ The Grimoire|#the-grimoire }}",
                    supreme_head_chef.image,
                    supreme_head_chef.level,
                    supreme_head_chef.max_level,
                )
            )

        # Spelunking
        if lunarheim.bonus_obtained:
            self.max_plate_level += 30
        else:
            missing.append(lunarheim.get_unlock_advice())


def _plate_advice(
    label: str, picture_class: str, progression: int = 0, goal: int = 1
) -> Advice:
    return Advice(
        label=label, picture_class=picture_class, progression=progression, goal=goal
    )
