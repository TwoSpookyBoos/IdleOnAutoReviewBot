from math import ceil, floor
from functools import cached_property

from consts.consts_autoreview import MultiToValue, ValueToMulti, EmojiType
from consts.general.common import percent_break_point
from consts.general.talents import dank_rank_talent_index
from consts.idleon.lava_func import lava_func
from consts.idleon.w6.farming import (
    market_info,
    exotic_market_info,
    crop_depot_list,
    landrank_list,
    seed_dict,
)
from consts.w6.farming import (
    max_land_rank_level,
    max_farming_crops,
    crop_dict,
    max_farming_value,
    crop_evo_breakpoint_list,
)

from models.advice.advice import Advice
from models.caverns.caves.the_lamp import LampWish
from models.general.achievements import Achievements
from models.master_classes.grimoire import Grimoire
from models.w1.star_signs import StarSigns
from models.w1.upgrade_vault import Vault
from models.w2.ballot import Ballot, BallotBuff
from models.w2.killroy import SkullShop
from models.w4.cooking import Meals
from models.w4.lab import LabBonus, LabJewel
from models.w4.rift import RiftBonus
from models.w6.sneaking import Emporium

from utils.number_formatting import parse_number, round_and_trim
from utils.safer_data_handling import safe_loads, safer_index, safer_math_pow
from utils.text_formatting import pl
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger

logger = get_logger(__name__)


class Crops(dict[int, float]):
    def __init__(self) -> None:
        self.count_per_seed = {seed_name: 0 for seed_name in seed_dict.keys()}
        self.count_per_seed["Unknown"] = 0
        self.stack = {
            "Evolution Gmo": 0,  # 200
            "Speed Gmo": 0,  # 1,000
            "Exp Gmo": 0,  # 2,500
            "Value Gmo": 0,  # 10,000
            "Super Gmo": 0,  # 100,000
        }
        self.unlocked = 0

    def add_crop(self, index: int, amount: float):
        self[index] = amount
        self._count_by_seed(index)
        self._count_stack(amount)

    def _count_by_seed(self, index: int):
        seed_name, _ = self._get_seed_index(index)
        self.count_per_seed[seed_name] += 1

    def _count_stack(self, amount: float):
        if amount >= 200:
            self.stack["Evolution Gmo"] += 1
        if amount >= 1000:
            self.stack["Speed Gmo"] += 1
        if amount >= 2500:
            self.stack["Exp Gmo"] += 1
        if amount >= 10000:
            self.stack["Value Gmo"] += 1
        if amount >= 100000:
            self.stack["Super Gmo"] += 1

    def get_discovery_advice(self, link_to_section: bool = False) -> Advice:
        return Advice(
            label=f"Total Crops Discovered: {self.unlocked}/{max_farming_crops}",
            picture_class="crop-depot",
            progression=self.unlocked,
            goal=max_farming_crops,
        )

    def get_crop_unlock_advice(self, crop_index: int) -> Advice | None:
        if crop_index in self:
            return None
        seed_name, seed_index = self._get_seed_index(crop_index)
        crop_info = crop_dict[crop_index]
        return Advice(
            label=f"Unlock: {crop_info['Name']} ({seed_name} #{seed_index})",
            picture_class=crop_info.get("Image", crop_info["Name"]),
            progression=self.count_per_seed[seed_name],
            goal=seed_index,
        )

    def _get_seed_index(self, crop_index: int) -> tuple[str, int]:
        for seed_name, info in seed_dict.items():
            if info["CropIndexStart"] <= crop_index <= info["CropIndexEnd"]:
                return seed_name, crop_index - info["CropIndexStart"] + 1
        return "Unknown", crop_index

    def get_unlock_advice(self, total_count: int):
        shortby = total_count - self.unlocked
        return Advice(
            label=f"Unlock {shortby} more crop type{pl(shortby)}",
            picture_class="crop-depot",
            progression=self.unlocked,
            goal=total_count,
        )

    def get_stack_progress_advice(self, name: str, target_value: int) -> Advice:
        match name:
            case "Evolution Gmo":
                count = 200
            case "Speed Gmo":
                count = 1000
            case "Exp Gmo":
                count = 2500
            case "Value Gmo":
                count = 10000
            case "Super Gmo":
                count = 100000
            case _:
                return None
        return Advice(
            label=f"Stacks for {name} ({count} crops)",
            picture_class="night-market",
            progression=self.stack[name],
            goal=target_value,
        )

    def evo_chance(self, crop_index: int) -> float:
        # "NextCropChance" in source. Last update v2.48 Giftmas Event
        seed_name, seed_num = self._get_seed_index(crop_index)
        try:
            info = seed_dict[seed_name]
            if crop_index == info["CropIndexStart"]:
                # First crop of seed always available
                return 1
            return info["EvoBase"] * safer_math_pow(
                info["EvoCoefficient"], seed_num - 1
            )
        except:
            logger.exception(
                f"Evo chance of {seed_name}#{seed_num}(#{crop_index}) not calculated"
            )
            return 0.3

    def get_crop_evo_advice(
        self, crop_index: int, needed_evo: float, complete_percent: float
    ) -> Advice:
        crop_info = crop_dict[crop_index]
        crop_name = crop_info["Name"]
        return Advice(
            label=f"{crop_name} chance<br>{needed_evo:.3g} for 100% chance",
            picture_class=crop_info.get("Image", crop_name),
            progression=f"{min(complete_percent, 1):.2%}",
            goal="100%" if complete_percent < 1 else "",
        )


class Depot:
    def __init__(self, info: dict):
        self.name = info["Name"]
        self._template = info["Bonus"]
        self._image = info["Image"]
        self._scaling_type = info["funcType"]
        self._scaling_coefficient = info["x1"]
        self.unlocked = False
        self._base_value = 0
        self._next_base_value = 0
        self.value: float = 0.0
        self.value_increase = 0.0
        self.max_value = 0.0
        self._require_emporium = info["EmporiumUnlockName"]
        self.unlocked = False

    def calculate_bonus(
        self, multi: float, crop_count: int, emporium: dict[str, Emporium]
    ):
        self.unlocked = emporium[self._require_emporium].obtained
        if self.name == "Highlighter":
            bonus_count = max(0, crop_count - 100)
            max_bonus_count = max_farming_crops - 100
        elif self.name == "Fancy Pen":
            bonus_count = max(0, crop_count - 200)
            max_bonus_count = max_farming_crops - 200
        else:
            bonus_count = crop_count
            max_bonus_count = max_farming_crops
        self._crop_count = crop_count
        self.value = (
            lava_func(self._scaling_type, bonus_count, self._scaling_coefficient, 0)
            * multi
        )
        if crop_count < max_farming_crops:
            self.value_increase = (
                lava_func(
                    self._scaling_type, bonus_count + 1, self._scaling_coefficient, 0
                )
                * multi
                - self.value
            )
            self.max_value = (
                lava_func(
                    self._scaling_type, max_bonus_count, self._scaling_coefficient, 0
                )
                * multi
            )
        else:
            self.value_increase = None
            self.max_value = None

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Farming Crop Depot|#farming }} - "
        label += f"{self.name}:<br>"
        is_multi = "}" in self._template
        progress = f"{_display_value(is_multi, self.value)}"
        # Show X/Y if bonus not maxed
        if self.max_value is not None:
            progress += f"/{_display_value(is_multi, self.max_value)}"
        label += self._template.replace("{", progress).replace("}", progress)
        if not link_to_section and self.max_value is not None:
            # Bonus not maxed and showed in section, add scaling info
            s_value = f"{self._scaling_coefficient}"
            scaling = self._template.replace("{", s_value).replace("}", s_value)
            label += f"<br>{scaling} per crop discovered"
            if self._scaling_type == "pow":
                label += ", multiplicative"
                if self.value_increase is not None:
                    display_increase = round_and_trim(
                        ValueToMulti(self.value_increase) - 1, 3
                    )
                    label += f"<br>Next crop would increase total by {display_increase}"
            else:
                label += ", additive"
            if not self.unlocked:
                label += "<br>Unlock via {{ Jade Emporium|#sneaking }}"
        if link_to_section:
            # Bonus show not in section, add note why there is progress but bonus 0
            if self.name == "Highlighter" and self.value == 0.0:
                label += "<br>Note: Value only increases after 100 crops found"
            elif self.name == "Fancy Pen" and self.value == 0.0:
                label += "<br>Note: Value only increases after 200 crops found"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=self._crop_count,
            goal=max_farming_crops,
        )


def _display_value(is_multi: bool, value: int | float):
    return round_and_trim(ValueToMulti(value) if is_multi else value)


class MarketUpgrade:
    def __init__(self, level: int, info: dict, is_day: bool):
        self.name = info["Name"]
        self._template = info["Description"]
        self.level = level
        self.max_level = info["MaxLevel"]
        self._value_per_level = info["BonusPerLevel"]
        # Bonus value from level only, no stack influence
        self.value = self.level * self._value_per_level
        self.max_value = self.max_level * self._value_per_level
        # Count of crop stack that influence on bonus
        self._stack = None
        # Bonus value with stack influence and ValueToMulti apply
        self._stack_value = None
        self._base_cost = info["BaseCost"]
        self._cost_imcrement = info["CostIncrement"]
        self.is_day = is_day
        self._crop_index_start = info["UpgradeCropIndexStart"]
        self._crop_index_scale = info["UpgradeCropIndexScale"]

    @cached_property
    def as_multi(self) -> float:
        """Return bonus as multi that ready to use"""
        if self._stack_value is None:
            return ValueToMulti(self.value)
        else:
            return self._stack_value

    def calculate_bonus(self, stack: dict[str, int], stack_multi: float):
        if self.name in stack:
            self._stack = stack[self.name]
            if self.name == "Evolution Gmo":
                self._stack_value = stack_multi * safer_math_pow(
                    ValueToMulti(self.value), self._stack
                )
            else:
                self._stack_value = stack_multi * ValueToMulti(self.value * self._stack)

    def get_bonus_advice(self, show_cost: bool = False):
        label = f"{self.name}:<br>"
        is_multi = "}" in self._template
        progress = f"{_display_value(is_multi, self.value)}"
        resource = ""
        if self.level < self.max_level:
            progress += f"/{_display_value(is_multi, self.max_value)}"
            if show_cost:
                if self.is_day:
                    resource = _get_crop_image(self._get_upgrade_crop_index())
                else:
                    resource = "magic-bean"
        label += self._template.replace("{", progress).replace("}", progress)
        if self._stack is not None:
            label += f"<br>{self._stack} stacks = {self._stack_value:,.2g}x"
        return Advice(
            label=label,
            picture_class="day-market" if self.is_day else "night-market",
            progression=self.level,
            goal=self.max_level,
            resource=resource,
        )

    def _get_upgrade_crop_index(self):
        # "MarketCostType" in source. Last updated v2.48 Giftmas Event
        if self.name == "Land Plots":
            return floor(
                self._crop_index_start
                + self._crop_index_scale
                * (
                    self.level
                    + self._crop_index_scale * floor(self.level / 3)
                    + floor(self.level / 4)
                )
            )
        else:
            return floor(self._crop_index_start + self._crop_index_scale * self.level)

    def _get_cost(self, cost_multi: float, to_level: int | None = None) -> float:
        total_cost = 0
        if to_level is None:
            to_level = self.level + 1
        for level in range(self.level, to_level):
            total_cost += (
                floor(self._base_cost * safer_math_pow(self._cost_imcrement, level))
                * cost_multi
            )
        return floor(total_cost) if 1e8 > total_cost else total_cost

    def get_target_bonus(
        self, target_level: int, cost_multi: float
    ) -> tuple[float | None, Advice] | None:
        if self.level == self.max_level:
            return None
        target_level = min(self.max_level, target_level)
        label = f"{self.name}:<br>"
        is_multi = "}" in self._template
        progress = f"{_display_value(is_multi, self.value)}"
        target_value = target_level * self._value_per_level
        progress += f"/{_display_value(is_multi, target_value)}"
        label += self._template.replace("{", progress).replace("}", progress)
        if self.is_day:
            upgrade_cost = None
            resource = _get_crop_image(self._get_upgrade_crop_index())
        else:
            upgrade_cost = self._get_cost(cost_multi, target_level)
            label += f"<br>Total cost: {upgrade_cost:,}"
            resource = "magic-bean"
        return upgrade_cost, Advice(
            label=label,
            picture_class="day-market" if self.is_day else "night-market",
            progression=self.level,
            goal=target_level,
            resource=resource,
        )


def _get_crop_image(crop_index: int) -> str:
    crop_info = crop_dict[crop_index]
    return crop_info.get("Image", crop_info["Name"])


class ExoticMarketUpgrade:
    def __init__(self, level: int, info: dict):
        self.level = level
        self.name = info["Name"]
        self._template = info["Description"]
        self._crop_index = info["CostCropIndex"]
        self._coefficient = info["Coefficient"]
        self._scaling_type = info["ScalingType"]
        self.value = 0
        self._max_value = None

    def calculate_bonus(self):
        # "ExoticBonusQTY" in source. Last update 2.48 Giftmas Event
        match self._scaling_type:
            case 1:
                self.value = self._coefficient * self.level / (self.level + 1000)
                self._max_value = self._coefficient
            case 0:
                self.value = self._coefficient * self.level
            case _:
                logger.warning(
                    f"Unknown scaling type ({self._scaling_type})"
                    f" of exotic upgrade '{self.name}'"
                )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Exotic Market|#farming }} - "
        label += f"{self.name}:<br>"
        is_multi = "}" in self._template
        value = f"{_display_value(is_multi, self.value)}"
        if self._max_value is not None:
            value += f"/{_display_value(is_multi, self._max_value)}"
        bonus = (
            self._template.replace("{", value).replace("}", value).replace("$", value)
        )
        if not link_to_section:
            label += f"Level {self.level}: {bonus}"
            if self._max_value is not None:
                current_percent = self.value / self._max_value
                progress = f"{current_percent:.2%}"
                goal = "100%"
                for percent in percent_break_point:
                    if current_percent < percent:
                        next_level, next_bonus = self._get_percent_info(percent)
                        label += (
                            f"<br>Next Breakpoint:"
                            f"<br>Level {next_level} ({percent:.0%}): {next_bonus}"
                        )
                        break
            else:
                progress = "Linear"
                goal = EmojiType.INFINITY.value
                label += f"<br>+{self._coefficient} per level"
        else:
            label += bonus
            progress = self.level
            goal = EmojiType.INFINITY.value
        return Advice(
            label=label,
            picture_class=_get_crop_image(self._crop_index),
            progression=progress,
            goal=goal,
        )

    def _get_percent_info(self, percent: float) -> tuple[int, str] | None:
        if percent >= 1.0 or percent < 0 or self._max_value is None:
            return None
        is_multi = "}" in self._template
        next_value = f"{_display_value(is_multi, self._max_value * percent)}"
        next_bonus = self._template.replace("{", next_value).replace("}", next_value)
        match self._scaling_type:
            case 1:
                next_level = int(1000 * percent / (1 - percent))
                return next_level, next_bonus
            case _:
                return None


class LandRankUpgrade:
    def __init__(self, index: int, level: int, info: dict, total_level: int):
        self.name = info["Name"]
        self.level = level
        self._base_value = info["Base Value"]
        self.value = 0
        self._index = index
        self._template = info["Description"]
        self._unlock_level = info["UnlockLevel"]
        self._unlocked = info["UnlockLevel"] <= total_level
        if index % 5 != 4:
            self.max_level = None
        else:
            self.max_level = max_land_rank_level

    def calculate_bonus(self, multi: float):
        self.value = self.get_value(multi)
        self.max_value = (
            None if self.max_level is None
            else multi * self._base_value * self.max_level
        )

    def get_value(self, multi: float) -> float:
        if self.max_level is None:
            return multi * 1.7 * self._base_value * self.level / (self.level + 80)
        return multi * self._base_value * self.level

    def get_bonus_advice(
        self, link_to_section: bool = True, level_goal: int = None
    ) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Land Ranks|#farming }} - "
        label += f"{self.name}:<br>"
        progress = f"{round_and_trim(self.value):,}"
        if self.max_level is not None and self.level < self.max_level:
            progress += f"/{round_and_trim(self.max_value)}"
        label += self._template.replace("{", progress)
        if not link_to_section and not self._unlocked:
            label += f"<br>Unlocked at {self._unlock_level} total land ranks"
        if level_goal is not None:
            goal = level_goal
        elif self.max_level is None:
            goal = ""
        else:
            goal = self.max_level
        return Advice(
            label=label, picture_class=self.name, progression=self.level, goal=goal
        )


class LandRank(dict[str, LandRankUpgrade]):
    def __init__(self, land_rank_levels: list[int], land_rank_upgrade: list[int]):
        try:
            self.levels = land_rank_levels
            self.total_level = sum(land_rank_levels)
            self.min_level = min([v for v in land_rank_levels if v > 0], default=0)
            self.max_level = max(land_rank_levels, default=0)
        except:
            self.levels = land_rank_levels
            self.total_level = 0
            self.min_level = 0
            self.max_level = 0
        for index, info in enumerate(landrank_list):
            level = safer_index(land_rank_upgrade, index, 0)
            bonus = LandRankUpgrade(index, level, info, self.total_level)
            self[bonus.name] = bonus

    def get_bonus_with_land_rank_advice(self, name: str) -> list[Advice]:
        min_lr = max(self.min_level, floor(0.8 * self.max_level))
        if self.min_level < floor(0.8 * self.min_level):
            llr_note = "80% of Max"
        else:
            llr_note = "Lowest"
        low_advice = Advice(
            label=f"{llr_note} Land Rank: {min_lr}",
            picture_class=self._land_rank_image(min_lr),
        )
        high_advice = Advice(
            label=f"Highest Land Rank: {self.max_level}",
            picture_class=self._land_rank_image(self.max_level),
        )
        upgrade = self[name]
        upgrade_advice = upgrade.get_bonus_advice(False)
        upgrade_advice.label += (
            f"<br>Total on Lowest: +{round_and_trim(upgrade.value * self.min_level):,}%"
            "<br>Total on Highest: "
            f"+{round_and_trim(upgrade.value * self.max_level):,}%"
        )
        return [low_advice, high_advice, upgrade_advice]

    def _land_rank_image(self, level: int) -> str:
        if level >= 100:
            return "landrank-7"
        elif level >= 75:
            return "landrank-6"
        elif level >= 50:
            return "landrank-5"
        elif level >= 25:
            return "landrank-4"
        elif level >= 10:
            return "landrank-3"
        elif level >= 5:
            return "landrank-2"
        else:
            return "landrank-1"


class CropDepotMulti:
    def __init__(self, lab: float, grimoire: float):
        self.lab: float = lab
        self.grimoire: float = grimoire
        self.total: float = lab * grimoire


class CropValueMulti:
    def __init__(
        self,
        doubler: int,
        mboost_sboost: float,
        pboost_value: float,
        min_plot_rank: int,
        max_plot_rank: int,
        ballot_value: float,
        value_gmo: float,
    ):
        self.doubler: int = doubler
        self.mboost_sboost: float = mboost_sboost
        self.pboost_ballot_min: float = ValueToMulti(
            pboost_value * min_plot_rank + ballot_value
        )
        self.pboost_ballot_max: float = ValueToMulti(
            pboost_value * max_plot_rank + ballot_value
        )
        self.value_gmo: float = value_gmo
        self.before_cap_min: int = round(
            max(1, doubler) * mboost_sboost * self.pboost_ballot_min * value_gmo
        )
        self.before_cap_max: int = round(
            max(1, doubler) * mboost_sboost * self.pboost_ballot_max * value_gmo
        )
        self.final_min: int = min(max_farming_value, self.before_cap_min)


class CropEvoMulti:
    def __init__(
        self,
        maps_opened: int,
        cropius_mapper_value: float,
        crop_chapter_value: float,
        tome_score: int,
        vial_value: float,
        stamp_value: float,
        meals: Meals,
        markets: float,
        land_rank: float,
        star_signs: StarSigns,
        farming_levels: list[int],
        skill_mastery_unlocked: bool,
        ballot: float,
        lil_overgrowth: bool,
        skull_shop: float,
        wish_value: float,
        summoning: float,
    ):
        self.maps_opened: int = maps_opened
        self.cropius_value: float = maps_opened * cropius_mapper_value
        self.vial_value: float = vial_value
        self.tome_score = tome_score
        self.crop_chapter_stacks = max(0, (tome_score - 5000) // 2000)
        self.alchemy: float = (
            ValueToMulti(self.cropius_value)
            * ValueToMulti(
                crop_chapter_value * max(0, floor((tome_score - 5000) / 2000))
            )
            * ValueToMulti(vial_value)
        )
        self.stamp: float = ValueToMulti(stamp_value)
        self.nyan_stacks: int = meals.nyan_stacks
        self.meals: float = ValueToMulti(meals['Bill Jack Pep'].value) * ValueToMulti(
            meals.nyanborgir_value
        )
        self.markets: float = markets
        self.land_rank: float = land_rank
        self.starsign_value: float = (
            3
            * star_signs["Cropiovo Minor"].unlocked
            * max(farming_levels, default=0)
            * star_signs.silkrode_multi
            * star_signs.seraph_multi
        )
        self.starsign: float = ValueToMulti(self.starsign_value)
        self.total_farming_levels: int = sum(farming_levels)
        self.skill_mastery_active: bool = (
            skill_mastery_unlocked and self.total_farming_levels >= 300
        )
        self.misc: float = (
            ValueToMulti(5 * lil_overgrowth)
            * skull_shop
            * ValueToMulti(15 * self.skill_mastery_active * skill_mastery_unlocked)
            * ballot
        )
        self.wish: float = ValueToMulti(wish_value)
        # Excludes Crop Chapter
        self.total: float = (
            self.alchemy
            * self.stamp
            * self.meals
            * self.markets
            * self.land_rank
            * summoning
            * self.starsign
            * self.misc
            * self.wish
        )


class CropSpeedMulti:
    def __init__(
        self,
        vial_value: float,
        nutritious_soil_value: float,
        night_market: float,
        summoning: float,
    ):
        self.vial_value: float = vial_value
        self.vial_market: float = ValueToMulti(vial_value + nutritious_soil_value)
        self.night_market: float = night_market
        self.total: float = summoning * self.vial_market * night_market


class MagicBeanMulti:
    def __init__(self, day_market: float, emporium_achievement: float):
        self.day_market: float = day_market
        self.emporium_achievement: float = emporium_achievement
        self.total: float = day_market * emporium_achievement


class OvergrowthMulti:
    def __init__(
        self,
        achievement: float,
        starsign_value: float,
        night_market: float,
        merit: float,
        land_rank: float,
        pristine: float,
    ):
        self.achievement: float = achievement
        self.starsign_value: float = starsign_value
        self.starsign: float = ValueToMulti(starsign_value)
        self.night_market: float = night_market
        self.merit: float = merit
        self.land_rank: float = land_rank
        self.pristine: float = pristine
        self.total: float = (
            achievement * self.starsign * night_market * merit * land_rank * pristine
        )


class Farming:
    def __init__(self, raw_data: dict):
        self.crops: Crops = Crops()
        self.depot: dict[str, Depot] = {}
        raw_crops = safe_loads(raw_data.get("FarmCrop", {}))
        if not raw_crops:
            logger.warning("Farming Crop data not present.")
        for key, value in raw_crops.items():
            if value is None:
                raw_crops[key] = 0
        self._parse_crops(raw_crops)
        self._parse_crop_depot()
        self.market: dict[str, MarketUpgrade] = {}
        raw_market = safe_loads(raw_data.get("FarmUpg", []))
        if not raw_market:
            logger.warning("Farming Markets data not present.")
        self._parse_markets(raw_market)
        self.exotic_market: dict[str, ExoticMarketUpgrade] = {}
        self._parse_exotic_markets(raw_market)
        self.magic_beans = parse_number(raw_market[1])
        self.magic_bean_unlocked = False
        raw_landrank_info = safe_loads(raw_data.get("FarmRank", []))
        if raw_landrank_info is None:
            logger.warning("Farming Land Rank Database data not present.")
            raw_landrank_info = [[], 0, []]
        land_rank_levels: list[int] = safer_index(raw_landrank_info, 0, [])
        land_rank_upgrade: list[int] = safer_index(raw_landrank_info, 2, [])
        self.land_rank = LandRank(land_rank_levels, land_rank_upgrade)
        self.total_plots = 1
        self.depot_multi: CropDepotMulti | None = None
        self.value_multi: CropValueMulti | None = None
        self.evo_multi: CropEvoMulti | None = None
        self.speed_multi: CropSpeedMulti | None = None
        self.bean_multi: MagicBeanMulti | None = None
        self.og_multi: OvergrowthMulti | None = None

    def _parse_crops(self, raw_crops: dict):
        for index, amount in raw_crops.items():
            index = parse_number(index)
            # Once discovered, crops will always appear in raw_crops dict.
            self.crops.unlocked += 1
            self.crops.add_crop(index, float(amount))

    def _parse_crop_depot(self):
        for info in crop_depot_list:
            depot = Depot(info)
            self.depot[depot.name] = depot

    def _parse_markets(self, raw_market: list):
        for index, upgrade_info in enumerate(market_info):
            level = raw_market[index + 2]
            upgrade = MarketUpgrade(level, upgrade_info, index < 8)
            self.market[upgrade.name] = upgrade

    def _parse_exotic_markets(self, raw_market: list):
        for index, upgrade_info in enumerate(exotic_market_info):
            level = raw_market[index + 20]
            upgrade = ExoticMarketUpgrade(level, upgrade_info)
            self.exotic_market[upgrade.name] = upgrade

    def get_land_rank_multi(self, dank_rank_level: int) -> float:
        dank_rank = all_talentsDict[dank_rank_talent_index]
        dank_rank_multi = lava_func(
            dank_rank['funcX'], dank_rank_level, dank_rank['x1'], dank_rank['x2']
        )
        # "ExoticBonusQTY" 14 in source. Last updated in v2.531.0
        plump_multi = ValueToMulti(self.exotic_market['PLUMP DATABASE'].value)
        return max(1, dank_rank_multi) * plump_multi

    def calculate_land_rank_bonus(self, dank_rank_level: int):
        multi = self.get_land_rank_multi(dank_rank_level)
        for upgrade in self.land_rank.values():
            upgrade.calculate_bonus(multi)

    def calculate_crop_depot_bonus(
        self,
        depot_studies: LabBonus,
        pure_opal_rhombol: LabJewel,
        grimoire: Grimoire,
        vault: Vault,
        emporium: dict[str, Emporium],
        *,
        pure_opal_navette: LabJewel,
        spelunker_obol: LabBonus,
    ):
        self._depot_studies = depot_studies
        self._pure_opal_rhombol = pure_opal_rhombol
        self._pure_opal_navette = pure_opal_navette
        self._spelunker_obol = spelunker_obol
        lab_multi = ValueToMulti(
            (depot_studies.value + pure_opal_rhombol.value) * depot_studies.enabled
        )
        # "CropSCbonMulti" in source: Grimoire 22 + Exotic 40 + Vault 79 share one
        # multi. Last updated in v2.531.0
        grimoire_multi = ValueToMulti(
            MultiToValue(grimoire.upgrades['Superior Crop Research'].total_value)
            + self.exotic_market['SCIENTERRIFIC'].value
            + vault.upgrades['Properly Funded Research'].total_value
        )
        self.depot_multi = CropDepotMulti(lab_multi, grimoire_multi)
        for bonus in self.depot.values():
            bonus.calculate_bonus(self.depot_multi.total, self.crops.unlocked, emporium)

    def calculate_market_bonus(self, plot_of_land_owned: int, plot_merit_level: int):
        super_gmo = self.market["Super Gmo"]
        super_gmo.calculate_bonus(self.crops.stack, 1.0)
        for bonus in self.market.values():
            if bonus == super_gmo:
                continue
            bonus.calculate_bonus(self.crops.stack, super_gmo.as_multi)
        bought_plot = plot_of_land_owned + min(3, plot_merit_level)
        self.total_plots = 1 + self.market["Land Plots"].level + bought_plot

    def calculate_exotic_market_bonus(self):
        for bonus in self.exotic_market.values():
            bonus.calculate_bonus()

    def calculate_crop_value_multi(self, ballot: Ballot):
        self._value_ballot = ballot[29]
        # if ("CropsBonusValue" == e)
        # return Math.min(100, Math.round(Math.max(1, Math.floor(1 + (c.randomFloat() + q._customBlock_FarmingStuffs("BasketUpgQTY", 0, 5) / 100))) * (1 + q._customBlock_FarmingStuffs("LandRankUpgBonusTOTAL", 1, 0) / 100) * (1 + (q._customBlock_FarmingStuffs("LankRankUpgBonus", 1, 0) * c.asNumber(a.engine.getGameAttribute("FarmRank")[0][0 | t]) + q._customBlock_Summoning("VotingBonusz", 29, 0)) / 100)));
        self.value_multi = CropValueMulti(
            floor(self.market["Product Doubler"].as_multi),
            ValueToMulti(
                self.land_rank["Production Megaboost"].value
                + self.land_rank["Production Superboost"].value
            ),
            self.land_rank["Production Boost"].value,
            self.land_rank.min_level,
            self.land_rank.max_level,
            # Ballot Buff * Active status
            ballot[29].value * int(ballot[29].active),
            self.market["Value Gmo"].as_multi,
        )

    def calculate_crop_evo_multi(
        self,
        characters: list,
        alchemy_bubbles: dict,
        alchemy_vials: dict,
        tome_score: int,
        crop_evo_stamp_value: float,
        meals: Meals,
        star_signs: StarSigns,
        farming_levels: list[int],
        skill_mastery: RiftBonus,
        ballot_buff: BallotBuff,
        achievements: Achievements,
        skull_shop: SkullShop,
        lamp_wish: LampWish,
        summoning_bonuses: dict,
        *,
        max_summoning_level: int,
    ):
        self._max_summoning_level = max_summoning_level
        self._highest_farming_level = max(farming_levels)
        self._cropiovo_unlocked = star_signs["Cropiovo Minor"].unlocked
        self._lil_overgrowth = achievements["Lil' Overgrowth"].complete
        self._skull_shop = skull_shop
        self._skill_mastery_unlocked = skill_mastery.unlocked
        self._evo_ballot = ballot_buff
        maps_opened = 0
        mama_trolls_map_open = False
        for char in characters:
            # Clearing the fake portal at Samurai Guardians doesn't count
            for map_index in range(251, 264):
                if int(safer_index(char.kill_dict.get(map_index, [1]), 0, 1)) <= 0:
                    maps_opened += 1
                    mama_trolls_map_open = mama_trolls_map_open or map_index == 257
        self.magic_bean_unlocked = mama_trolls_map_open
        self.evo_multi = CropEvoMulti(
            maps_opened,
            alchemy_bubbles["Cropius Mapper"].base_value,
            alchemy_bubbles["Crop Chapter"].base_value,
            tome_score,
            alchemy_vials["Flavorgil (Caulifish)"].value,
            crop_evo_stamp_value,
            meals,
            self.market["Biology Boost"].as_multi
            * self.market["Evolution Gmo"].as_multi,
            ValueToMulti(
                self.land_rank["Evolution Boost"].value * self.land_rank.min_level
            )
            * ValueToMulti(self.land_rank["Evolution Megaboost"].value)
            * ValueToMulti(self.land_rank["Evolution Superboost"].value)
            * ValueToMulti(self.land_rank["Evolution Ultraboost"].value),
            star_signs,
            farming_levels,
            skill_mastery.unlocked,
            ballot_buff.active_multi,
            achievements["Lil' Overgrowth"].complete,
            skull_shop.crop_multi,
            lamp_wish.value_list[0],
            summoning_bonuses["Crop EVO"].as_multi,
        )

    def calculate_crop_speed(self, alchemy_vials: dict, summoning_bonuses: dict):
        self.speed_multi = CropSpeedMulti(
            alchemy_vials["Ricecakorade (Rice Cake)"].value,
            self.market["Nutritious Soil"].value,
            self.market["Speed Gmo"].as_multi,
            summoning_bonuses["Farming SPD"].as_multi,
        )

    def calculate_bean_bonus(self, deal_sweetening_value: float, achievements: Achievements):
        self._crop_flooding = achievements["Crop Flooding"].complete
        self.bean_multi = MagicBeanMulti(
            self.market["More Beenz"].as_multi,
            ValueToMulti(
                deal_sweetening_value
                + (5 * achievements["Crop Flooding"].complete)
            ),
        )

    def calculate_og(
        self,
        achievements: Achievements,
        star_signs: StarSigns,
        og_merit_level: int,
        taffy_disc_value: float,
    ):
        self._big_time_land_owner = achievements["Big Time Land Owner"].complete
        self._og_signalais_unlocked = star_signs["O.G. Signalais"].unlocked
        self._og_merit_level = og_merit_level
        self.og_multi = OvergrowthMulti(
            ValueToMulti(15 * achievements["Big Time Land Owner"].complete),
            15
            * star_signs["O.G. Signalais"].unlocked
            * star_signs.silkrode_multi
            * star_signs.seraph_multi,
            self.market["Og Fertilizer"].as_multi,
            ValueToMulti(2 * og_merit_level),
            ValueToMulti(
                self.land_rank["Overgrowth Boost"].value
                + self.land_rank["Overgrowth Megaboost"].value
                + self.land_rank["Overgrowth Superboost"].value
            ),
            ValueToMulti(taffy_disc_value),
        )

    def get_depot_lab_advices(self) -> list[Advice]:
        navette = self._pure_opal_navette
        spelunker = self._spelunker_obol
        rhombol = self._pure_opal_rhombol
        studies = self._depot_studies
        navette_value = navette.active_value
        navette_max = navette.base_value
        spelunker_multi = max(1, spelunker.value)
        spelunker_max = spelunker.base_value
        rhombol_value = rhombol.active_value
        rhombol_max = rhombol.base_value
        rhombol_enhanced_max = rhombol_max * (spelunker_max + (navette_max / 100))
        studies_value = max(1, ValueToMulti(studies.value + rhombol_value))
        studies_max = ValueToMulti(studies.base_value)
        lab_multi = round_and_trim(self.depot_multi.lab)
        lab_max = round_and_trim(
            ValueToMulti(studies.base_value + rhombol_enhanced_max)
        )
        return [
            Advice(
                label=f"Lab Jewel: Pure Opal Navette: Increases the value of "
                f"Spelunker Obol by +{navette_value / 100:.1f}/{navette_max / 100:.1f}"
                f"<br>(Yes, this jewel is bugged)",
                picture_class="pure-opal-navette",
                progression=int(navette.enabled),
                goal=1,
            ),
            Advice(
                label=f"Lab Bonus: Spelunker Obol: Multiplies the value of Pure Opal "
                f"Rhombol by {spelunker_multi:.1f}/{spelunker_max:.1f}x",
                picture_class="spelunker-obol",
                progression=int(spelunker.enabled),
                goal=1,
            ),
            Advice(
                label=f"Lab Jewel: Pure Opal Rhombol: Increases Depot Studies by "
                f"+.{rhombol_value:.0f}/.{rhombol_max:.0f}",
                picture_class="pure-opal-rhombol",
                progression=int(rhombol.enabled),
                goal=1,
            ),
            Advice(
                label=f"Lab Bonus: Depot Studies PhD: "
                f"{studies_value:.2f}/{studies_max:.2f}x",
                picture_class="depot-studies-phd",
                progression=int(studies.enabled),
                goal=1,
            ),
            Advice(
                label=f"Final Lab multi: {lab_multi}/{lab_max}x"
                f"<br>Note: Defaulted ON. Sorry {EmojiType.FROWN.value}",
                picture_class="laboratory",
                progression=f"{lab_multi}",
                goal=f"{lab_max}",
            ),
        ]

    def get_product_doubler_advice(self) -> Advice:
        doubler = self.market["Product Doubler"]
        return Advice(
            label=f"Highest full 100 Product Doubler reached for guarantee: "
            f"{(doubler.value // 100) * 100:.0f}%",
            picture_class="day-market",
            progression=f"{doubler.value:.0f}",
            goal=400,
            unit="%",
        )

    def get_value_ballot_advice(self) -> Advice:
        buff = self._value_ballot
        return Advice(
            label=f"Plus Weekly {{{{ Ballot|#bonus-ballot }}}}: "
            f"{buff.active_multi:.3f}/{buff.multi:.3f}x"
            f"<br>(Buff {buff.status})",
            picture_class="ballot-29",
            progression=int(buff.active),
            goal=1,
        )

    def get_value_lowest_plot_advice(self) -> Advice:
        return Advice(
            label="Total on Lowest ranked plot<br>Note: 10,000x is a HARD cap.",
            picture_class="crop-scientist",
            progression=f"{self.value_multi.before_cap_min:,.0f}",
            goal=f"{max_farming_value:,}",
        )

    def get_value_highest_plot_advice(self) -> Advice:
        return Advice(
            label="Total on Highest ranked plot",
            picture_class="crop-scientist",
            progression=f"{self.value_multi.before_cap_max:,.0f}",
            goal=f"{max_farming_value:,}",
        )

    def get_nyanborgir_level_advice(self) -> Advice:
        return Advice(
            label=f"Highest Summoning level: {self._max_summoning_level}"
            f"<br>Provides a {self.evo_multi.nyan_stacks}x multi to Nyanborgir",
            picture_class="summoning",
        )

    def get_highest_farming_level_advice(self) -> Advice:
        return Advice(
            label=f"Highest Farming level: {self._highest_farming_level}",
            picture_class="farming",
        )

    def get_cropiovo_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Starsign|#star-signs }}}}: Cropiovo Minor: "
            f"{3 * self._cropiovo_unlocked:.0f}/3% per farming level."
            f"<br>Total Value if doubled: {self.evo_multi.starsign_value:,.3f}%",
            picture_class="cropiovo-minor",
            progression=int(self._cropiovo_unlocked),
            goal=1,
        )

    def get_lil_overgrowth_advice(self) -> Advice:
        return Advice(
            label=f"W6 Achievement: Lil' Overgrowth: "
            f"{1.05 * self._lil_overgrowth:.2f}/1.05x",
            picture_class="lil-overgrowth",
            progression=int(self._lil_overgrowth),
            goal=1,
        )

    def get_skull_shop_advice(self) -> Advice:
        shop = self._skull_shop
        return Advice(
            label=f"Killroy Skull Shop: {shop.crop_multi:.3f}x"
            f"<br>1 purchase: +{shop.next_crop_multi - shop.crop_multi:.3f}x",
            picture_class="killroy-crop-evolution",
            progression=shop.crop_purchases,
        )

    def get_skill_mastery_advice(self) -> Advice:
        evo = self.evo_multi
        return Advice(
            label=f"Skill Mastery at 200 Farming: "
            f"+{1.15 * evo.skill_mastery_active * self._skill_mastery_unlocked}/1.15x",
            picture_class="farming",
            progression=evo.total_farming_levels,
            goal=200,
        )

    def get_evo_ballot_advice(self) -> Advice:
        buff = self._evo_ballot
        return Advice(
            label=f"Weekly Ballot: {buff.active_multi:.3f}/{buff.multi:.3f}x"
            f"<br>(Buff {buff.status})",
            picture_class="ballot-29",
            progression=int(buff.active),
            goal=1,
        )

    def get_target_evo_crop_advice(self) -> Advice:
        first_crop_index = crop_evo_breakpoint_list[0]
        target_evo_crop = (
            first_crop_index,
            ceil(1 / self.crops.evo_chance(first_crop_index)),
        )
        for crop_index in crop_evo_breakpoint_list[1:]:
            crop_evo_chance = ceil(1 / self.crops.evo_chance(crop_index))
            if self.evo_multi.total > crop_evo_chance:
                # Enough evo chance for this crop, so target the previous one
                break
            target_evo_crop = crop_index, crop_evo_chance
        crop_index, crop_evo_chance = target_evo_crop
        percent = self.evo_multi.total / crop_evo_chance
        return self.crops.get_crop_evo_advice(crop_index, crop_evo_chance, percent)

    def get_speed_total_advice(self) -> Advice:
        return Advice(
            label=f"Farming Speed Multi: {self.speed_multi.total:,.3f}x",
            picture_class="crop-scientist",
        )

    def get_bean_total_advice(self) -> Advice:
        return Advice(
            label=f"Magic Beans Bonus: {self.bean_multi.total:,.3f}x",
            picture_class="crop-scientist",
        )

    def get_crop_flooding_advice(self) -> Advice:
        return Advice(
            label=f"W6 Achievement: Crop Flooding: +{5 * self._crop_flooding}/5%",
            picture_class="crop-flooding",
            progression=int(self._crop_flooding),
            goal=1,
        )

    def get_og_total_advice(self) -> Advice:
        return Advice(
            label=f"Overgrowth Chance: {self.og_multi.total:,.3f}x",
            picture_class="crop-scientist",
        )

    def get_big_time_land_owner_advice(self) -> Advice:
        return Advice(
            label=f"W6 Achievement: Big Time Land Owner: "
            f"{self.og_multi.achievement:.2f}/1.15x",
            picture_class="big-time-land-owner",
            progression=int(self._big_time_land_owner),
            goal=1,
        )

    def get_og_signalais_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Starsign|#star-signs }}}}: O.G. Signalais: "
            f"{15 * self._og_signalais_unlocked:.0f}/15%."
            f"<br>Total Value if doubled: {self.og_multi.starsign_value:.3f}%",
            picture_class="og-signalais",
            progression=int(self._og_signalais_unlocked),
            goal=1,
        )

    def get_og_merit_advice(self) -> Advice:
        return Advice(
            label=f"W6 Taskboard Merit: +{2 * self._og_merit_level}/30%",
            picture_class="merit-5-2",
            progression=self._og_merit_level,
            goal=15,
        )
