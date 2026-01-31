from math import floor, ceil
from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.idleon.lava_func import lava_func
from consts.idleon.w6.farming import (
    market_info,
    crop_depot_list,
    landrank_list,
    seed_dict,
)
from consts.w6.farming import (
    max_land_rank_level,
    max_farming_crops,
    crop_dict,
    max_farming_value,
)

from models.advice.advice import Advice
from models.w6.sneaking import Emporium

from utils.number_formatting import parse_number, round_and_trim
from utils.safer_data_handling import safe_loads, safer_index, safer_math_pow
from utils.text_formatting import pl
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

    def _get_seed_index(self, crop_index: int) -> (str, int):
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
        self, crop_index: int, needed_evo: float, complete_precent: float
    ) -> Advice:
        crop_info = crop_dict[crop_index]
        crop_name = crop_info["Name"]
        return Advice(
            label=f"{crop_name} chance<br>{needed_evo:.3g} for 100% chance",
            picture_class=crop_info.get("Image", crop_name),
            progression=f"{min(complete_precent, 1):.2%}",
            goal="100%" if complete_precent < 1 else "",
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
            progress = f"/{_display_value(is_multi, self.max_value)}"
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


class Market:
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
                    crop_info = crop_dict[self._get_upgrade_crop_index()]
                    resource = crop_info.get("Image", crop_info["Name"])
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

    def _get_cost(self, cost_multi: float, to_level: int = None) -> float:
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
    ) -> tuple[float | None, Advice]:
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
            crop_info = crop_dict[self._get_upgrade_crop_index()]
            resource = crop_info.get("Image", crop_info["Name"])
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
        if self.max_level is None:
            self.value = multi * 1.7 * self._base_value * self.level / (self.level + 80)
            self.max_value = None
        else:
            self.value = multi * self._base_value * self.level
            self.max_value = multi * self._base_value * self.max_level

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


class Farming:
    def __init__(self, raw_data: dict):
        self.crops: Crops = Crops()
        self.depot: dict[str, Depot] = {}
        raw_crops = safe_loads(raw_data.get("FarmCrop", {}))
        if not raw_crops:
            logger.warning("Farming Crop data not present.")
        self._parse_crops(raw_crops)
        self._parse_crop_depot()
        self.market: dict[str, Market] = {}
        raw_market = safe_loads(raw_data.get("FarmUpg", []))
        if not raw_market:
            logger.warning("Farming Markets data not present.")
        self._parse_markets(raw_market)
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
        self.multi = {}

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
            upgrade = Market(level, upgrade_info, index < 8)
            self.market[upgrade.name] = upgrade

    def calculate_land_rank_bonus(self, multi: float):
        for upgrade in self.land_rank.values():
            upgrade.calculate_bonus(multi)

    def calculate_crop_depot_bonus(
        self, lab_multi: float, grimoire_multi: float, emporium: dict[str, Emporium]
    ):
        total_multi = lab_multi * grimoire_multi
        for bonus in self.depot.values():
            bonus.calculate_bonus(total_multi, self.crops.unlocked, emporium)

    def calculate_market_bonus(self, bought_plot: int):
        super_gmo = self.market["Super Gmo"]
        super_gmo.calculate_bonus(self.crops.stack, 1.0)
        for bonus in self.market.values():
            if bonus == super_gmo:
                continue
            bonus.calculate_bonus(self.crops.stack, super_gmo.as_multi)
        self.total_plots = 1 + self.market["Land Plots"].level + bought_plot

    def calculate_crop_value_multi(self, ballot: dict):
        # if ("CropsBonusValue" == e)
        # return Math.min(100, Math.round(Math.max(1, Math.floor(1 + (c.randomFloat() + q._customBlock_FarmingStuffs("BasketUpgQTY", 0, 5) / 100))) * (1 + q._customBlock_FarmingStuffs("LandRankUpgBonusTOTAL", 1, 0) / 100) * (1 + (q._customBlock_FarmingStuffs("LankRankUpgBonus", 1, 0) * c.asNumber(a.engine.getGameAttribute("FarmRank")[0][0 | t]) + q._customBlock_Summoning("VotingBonusz", 29, 0)) / 100)));
        value_multi = {}
        value_multi["Doubler Multi"] = floor(self.market["Product Doubler"].as_multi)
        value_multi["Mboost Sboost Multi"] = ValueToMulti(
            self.land_rank["Production Megaboost"].value
            + self.land_rank["Production Superboost"].value
        )
        value_multi["Value GMO Current"] = self.market["Value Gmo"].as_multi

        # Ballot Buff * Active status
        ballot_value = ballot["Buffs"][29]["Value"] * int(ballot["CurrentBuff"] == 29)
        # Calculate with the Min Plot Rank
        value_multi["Pboost Ballot Multi Min"] = ValueToMulti(
            # Value of PBoost * Lowest Plot Rank
            self.land_rank["Production Boost"].value * self.land_rank.min_level
            + ballot_value
        )
        value_multi["BeforeCapMin"] = round(
            max(1, value_multi["Doubler Multi"])  # end of max
            * value_multi["Mboost Sboost Multi"]
            * value_multi["Pboost Ballot Multi Min"]
            * value_multi["Value GMO Current"]
        )  # end of round

        # Now calculate with the Max Plot Rank
        value_multi["Pboost Ballot Multi Max"] = ValueToMulti(
            # Value of PBoost * Highest Plot Rank
            self.land_rank["Production Boost"].value * self.land_rank.max_level
            + ballot_value
        )
        value_multi["BeforeCapMax"] = round(
            max(1, value_multi["Doubler Multi"])  # end of max
            * value_multi["Mboost Sboost Multi"]
            * value_multi["Pboost Ballot Multi Max"]
            * value_multi["Value GMO Current"]
        )  # end of round
        value_multi["FinalMin"] = min(max_farming_value, value_multi["BeforeCapMin"])
        value_multi["FinalMax"] = min(max_farming_value, value_multi["BeforeCapMax"])
        self.multi["Value"] = value_multi

    def calculate_crop_evo_multi(self, map_opened: int, account: "Account"):
        evo_multi = {}
        evo_multi["Maps Opened"] = map_opened
        evo_multi["Cropius Final Value"] = (
            # TODO: Move to alchemy bonus calculate
            evo_multi["Maps Opened"]
            * account.alchemy_bubbles["Cropius Mapper"]["BaseValue"]
        )
        evo_multi["Vial Value"] = account.alchemy_vials["Flavorgil (Caulifish)"][
            "Value"
        ]
        evo_multi["Alch Multi"] = (
            ValueToMulti(evo_multi["Cropius Final Value"])
            * ValueToMulti(
                # TODO: Move to alchemy bonus calculate
                account.alchemy_bubbles["Crop Chapter"]["BaseValue"]
                * max(0, floor((account.tome["Total Points"] - 5000) / 2000))
            )
            * ValueToMulti(evo_multi["Vial Value"])
        )
        # Stamp
        evo_multi["Stamp Multi"] = ValueToMulti(
            account.stamps["Crop Evo Stamp"].total_value
        )
        # Meals
        evo_multi["Nyan Stacks"] = ceil(
            (max(account.all_skills["Summoning"], default=0) + 1) / 50
        )
        evo_multi["Meals Multi"] = (
            ValueToMulti(account.meals["Bill Jack Pepper"]["Value"])
            # TODO: move to meal bonus calculate
            * ValueToMulti(
                account.meals["Nyanborgir"]["Value"] * evo_multi["Nyan Stacks"]
            )
        )
        # Markets
        evo_multi["Farm Multi"] = (
            self.market["Biology Boost"].as_multi
            * self.market["Evolution Gmo"].as_multi
        )
        # Land Ranks
        evo_multi["LR Multi"] = (
            ValueToMulti(
                self.land_rank["Evolution Boost"].value * self.land_rank.min_level
            )
            * ValueToMulti(self.land_rank["Evolution Megaboost"].value)
            * ValueToMulti(self.land_rank["Evolution Superboost"].value)
            * ValueToMulti(self.land_rank["Evolution Ultraboost"].value)
        )
        # Starsign
        evo_multi["Starsign Final Value"] = (
            3
            * account.star_signs["Cropiovo Minor"]["Unlocked"]
            * max(account.all_skills["Farming"], default=0)
            * account.star_sign_extras["SilkrodeNanoMulti"]
            * account.star_sign_extras["SeraphMulti"]
        )
        evo_multi["SS Multi"] = ValueToMulti(evo_multi["Starsign Final Value"])
        # Misc
        evo_multi["Total Farming Levels"] = sum(account.all_skills["Farming"])
        evo_multi["Skill Mastery Bonus Bool"] = (
            account.rift["SkillMastery"] and evo_multi["Total Farming Levels"] >= 300
        )
        evo_multi["Ballot Active"] = account.ballot["CurrentBuff"] == 29
        # TODO: move to Ballot class method that create advice for it
        if evo_multi["Ballot Active"]:
            evo_multi["Ballot Status"] = "is Active"
        elif not evo_multi["Ballot Active"] and account.ballot["CurrentBuff"] != 0:
            evo_multi["Ballot Status"] = "is Inactive"
        else:
            evo_multi["Ballot Status"] = "status is not available in provided data"
        evo_multi["Ballot Multi Max"] = ValueToMulti(
            account.ballot["Buffs"][29]["Value"]
        )
        evo_multi["Ballot Multi Current"] = max(
            1, evo_multi["Ballot Multi Max"] * evo_multi["Ballot Active"]
        )
        evo_multi["Misc Multi"] = (
            ValueToMulti(5 * account.achievements["Lil' Overgrowth"]["Complete"])
            * account.killroy_skullshop["Crop Multi"]
            * ValueToMulti(
                15
                * evo_multi["Skill Mastery Bonus Bool"]
                * account.rift["SkillMastery"]
            )
            * evo_multi["Ballot Multi Current"]
        )
        evo_multi["Wish Multi"] = ValueToMulti(
            account.caverns["Caverns"]["The Lamp"]["WishTypes"][8]["BonusList"][0]
        )
        # subtotal doesn't include Crop Chapter
        evo_multi["Subtotal Multi"] = (
            evo_multi["Alch Multi"]
            * evo_multi["Stamp Multi"]
            * evo_multi["Meals Multi"]
            * evo_multi["Farm Multi"]
            * evo_multi["LR Multi"]
            * account.summoning["Bonuses"]["<x Crop EVO"]["Value"]
            * evo_multi["SS Multi"]
            * evo_multi["Misc Multi"]
            * evo_multi["Wish Multi"]
        )
        self.multi["Evo"] = evo_multi

    def calculate_crop_speed(self, account: "Account"):
        speed_multi = {}
        # Vial and Day Market
        speed_multi["Vial Value"] = account.alchemy_vials["Ricecakorade (Rice Cake)"][
            "Value"
        ]
        speed_multi["VM Multi"] = ValueToMulti(
            speed_multi["Vial Value"] + self.market["Nutritious Soil"].value
        )
        # Night Market
        speed_multi["NM Multi"] = self.market["Speed Gmo"].as_multi
        # Total
        speed_multi["Total Multi"] = (
            account.summoning["Bonuses"]["<x Farming SPD"]["Value"]
            * speed_multi["VM Multi"]
            * speed_multi["NM Multi"]
        )
        self.multi["Speed"] = speed_multi

    def calculate_bean_bonus(self, account):
        bean_multi = {}
        bean_multi["mga"] = self.market["More Beenz"].as_multi
        bean_multi["mgb"] = ValueToMulti(
            account.sneaking.emporium["Deal Sweetening"].value
            + (5 * account.achievements["Crop Flooding"]["Complete"])
        )
        bean_multi["Total Multi"] = bean_multi["mga"] * bean_multi["mgb"]
        self.multi["Bean"] = bean_multi

    def calculate_og(self, account: "Account"):
        # Fun calculations
        og_multi = {}
        og_multi["Ach Multi"] = ValueToMulti(
            15 * account.achievements["Big Time Land Owner"]["Complete"]
        )
        og_multi["Starsign Final Value"] = (
            15
            * account.star_signs["O.G. Signalais"]["Unlocked"]
            * account.star_sign_extras["SilkrodeNanoMulti"]
            * account.star_sign_extras["SeraphMulti"]
        )
        og_multi["SS Multi"] = ValueToMulti(og_multi["Starsign Final Value"])
        og_multi["NM Multi"] = self.market["Og Fertilizer"].as_multi
        og_multi["Merit Multi"] = ValueToMulti(2 * account.merits[5][2]["Level"])
        og_multi["LR Multi"] = ValueToMulti(
            self.land_rank["Overgrowth Boost"].value
            + self.land_rank["Overgrowth Megaboost"].value
            + self.land_rank["Overgrowth Superboost"].value
        )
        og_multi["Pristine Multi"] = ValueToMulti(
            account.sneaking.pristine_charms["Taffy Disc"].value
        )
        og_multi["Total Multi"] = (
            og_multi["Ach Multi"]
            * og_multi["SS Multi"]
            * og_multi["NM Multi"]
            * og_multi["Merit Multi"]
            * og_multi["LR Multi"]
            * og_multi["Pristine Multi"]
        )
        self.multi["OG"] = og_multi
