from typing import Optional
from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.idleon.w6.sneaking import (
    pristine_charms_info,
    gemstones_info,
    jade_emporium,
    jade_emporium_order,
)
from consts.w6.sneaking import pristine_charm_images_override
from models.advice.advice import Advice

from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index

from utils.logging import get_logger

logger = get_logger(__name__)


class PristineCharm:
    def __init__(self, name: str, is_obtained: bool):
        self.name = name
        self.obtained = is_obtained
        info = pristine_charms_info[name]
        description_template = info["Description"]
        bonus_value = info["Value"]
        self.value = bonus_value if is_obtained else 0
        if "}" in description_template:
            self._description = description_template.replace(
                "}", f"{ValueToMulti(bonus_value)}"
            )
        else:
            self._description = description_template.replace("{", f"{bonus_value}")
        self._image = pristine_charm_images_override.get(name, name)

    def get_obtained_advice(self, link_to_section: bool = True):
        label = ""
        if link_to_section:
            label += "{{Pristine Charms|#sneaking}} - "
        label += f"{self.name}:<br>{self._description}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=int(self.obtained),
            goal=1,
        )


class Gemstone:
    def __init__(self, name: str, info: dict, level: int):
        self._name = name
        self._level = level
        self._base_value = info["Base Value"]
        self._scaling_value = info["Scaling Value"]
        self._max_value = self._base_value + self._scaling_value
        self._net_value = 0.0
        self.value = 0.0
        self._percent = 0
        self._description = info["Description"]

    @cached_property
    def as_multi(self):
        return ValueToMulti(self.value)

    def calculate_value(self, moissanite: Optional["Gemstone"], talent_multi: float):
        if self._level == 0:
            return
        self._net_value = self._base_value + self._scaling_value * (
            self._level / (self._level + 1000)
        )
        if self._name == "Moissanite":
            self.value = self._net_value
        else:
            self.value = self._net_value * moissanite.as_multi * talent_multi
        self._percent = 100 * self._net_value / self._max_value

    def get_bonus_advice(self) -> Advice:
        label = (
            f"{self._name}: {self._description}"
            f"<br>Level {self._level}: "
            f"+{round_and_trim(self._net_value)}/{self._max_value}"
            f"{'%' if self._name != 'Firefrost' else ''} "
        )
        if self._net_value != self.value and self._name != "Moissanite":
            label += (
                f"<br>Total: +{round_and_trim(self.value)}"
                f"{'%' if self._name != 'Firefrost' else ''}"
            )
        if self._name == "Emerald":
            label += f" = {round_and_trim(1 / self.as_multi, 4)}x cost multiplier"
        return Advice(
            label=label,
            picture_class=self._name,
            progression=round_and_trim(self._percent),
            goal=100,
            unit="%",
        )


class Emporium:
    def __init__(self, index: int, bought: str):
        info = jade_emporium[index]
        self.obtained = info["CodeString"] in bought
        self.name = info["Name"]
        self._bonus = info["Bonus"]
        self._image = info["Name"]
        self.value = self._get_bouns_value()

    def _get_bouns_value(self) -> int:

        if not self.obtained:
            return 0
        match self.name:
            case "Deal Sweetening":
                # (25 * m._customBlock_Ninja("EmporiumBonus", 15, 0) in source
                return 25
            case "Coral Conservationism":
                # (20 * m._customBlock_Ninja("EmporiumBonus", 43, 0) in source
                return 20
            case "Emperor Season Pass":
                # (5 * m._customBlock_Ninja("EmporiumBonus", 39, 0) in source
                return 5
            case _:
                return 0

    def get_obtained_advice(self, link_to_section: bool = True):
        label = ""
        if link_to_section:
            label += "{{Jade Emporium|#sneaking}} - "
        label += f"{self.name}:<br>{self._bonus}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=int(self.obtained),
            goal=1,
        )


class Sneaking:
    def __init__(self, raw_data):
        raw_optlacc = raw_data.get("OptLacc", [])
        self.current_mastery = safer_index(raw_optlacc, 231, 0)
        self.unlocked_mastery = safer_index(raw_optlacc, 232, 0)
        self.pristine_charms: dict[str, PristineCharm] = {}
        self.gemstones: dict[str, Gemstone] = {}
        self.emporium: dict[str, Emporium] = {}
        raw_ninja_list = safe_loads(raw_data.get("Ninja", []))
        if not raw_ninja_list:
            logger.warning("Sneaking data not present.")
        self._parse_pristine(raw_ninja_list)
        self._parse_gemstones(raw_optlacc)
        self._parse_emporium(raw_ninja_list)

    def _parse_pristine(self, raw_ninja_list):
        if raw_ninja_list:
            raw_pristine_charms_list = raw_ninja_list[107]
        else:
            raw_pristine_charms_list = [0] * len(pristine_charms_info)
        for index, name in enumerate(pristine_charms_info.keys()):
            is_obtained = bool(raw_pristine_charms_list[index])
            self.pristine_charms[name] = PristineCharm(name, is_obtained)

    def _parse_emporium(self, raw_ninja_list):
        max_exist_bonus = len(jade_emporium)
        raw_emporium_purchases = safer_index(
            safer_index(raw_ninja_list, 102, []), 9, ""
        )
        for index in jade_emporium_order:
            if index >= max_exist_bonus:
                continue
            bonus = Emporium(index, raw_emporium_purchases)
            self.emporium[bonus.name] = bonus

    def _parse_gemstones(self, raw_optlacc):
        for name, info in gemstones_info.items():
            level = safer_index(raw_optlacc, info["OptlAcc Index"], 0)
            self.gemstones[name] = Gemstone(name, info, level)

    def calculate_gemstones_values(self, talent_level, gemstone_multi):
        moissanite = self.gemstones["Moissanite"]
        moissanite.calculate_value(None, 1.0)
        self.gemstone_multi_source = (talent_level, gemstone_multi)
        for gemstone in self.gemstones.values():
            gemstone.calculate_value(moissanite, gemstone_multi)
