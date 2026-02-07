from consts.consts_autoreview import ValueToMulti
from consts.general.common import percent_break_point
from consts.idleon.w7.advice_fish import advice_fish_upgrade_data

from models.advice.advice import Advice

from utils.safer_data_handling import safe_loads, safer_index
from utils.number_formatting import round_and_trim
from utils.logging import get_logger

logger = get_logger(__name__)


class AdviceFishUpgrade:
    def __init__(self, info: dict, level: int, index: int):
        self.level = level
        self.name = info["Name"]
        self._template = info["Bonus"]
        self.max_value = info["MaxValue"]
        self.value = 0
        self._image = f"advice-fish-{index}"

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Advice Fish|#advice-fish}} - "
        if "{" in self._template:
            value = self.value
            max_value = self.max_value
        else:
            value = ValueToMulti(self.value)
            max_value = ValueToMulti(self.max_value)
        bonus = f"{round_and_trim(value)}/{round_and_trim(max_value)}"
        bonus_description = self._template.replace("{", bonus).replace("}", bonus)
        label += f"{self.name}:<br>Level {self.level}: {bonus_description}"
        current_percent = self.value / self.max_value
        for percent in percent_break_point:
            if current_percent < percent:
                next_level, next_bonus = self._get_percent_info(percent)
                label += (
                    "<br>Next Breakpoint:"
                    f"<br> Level {next_level} ({percent:.0%}): {next_bonus}"
                )
                break
        return Advice(
            label=label,
            picture_class=self._image,
            resource="coins",
            goal="100%",
            progression=f"{self.value / self.max_value:.2%}",
        )

    def _get_percent_info(self, percent: float) -> tuple[int, str] | None:
        if percent >= 1.0 or percent < 0:
            return None
        next_value = self.max_value * percent
        if "{" in self._template:
            next_value = f"{round_and_trim(next_value)}"
        else:
            next_value = f"{round_and_trim(ValueToMulti(next_value))}"
        next_bonus = self._template.replace("{", next_value).replace("}", next_value)
        next_level = int(100 * percent / (1 - percent))
        return next_level, next_bonus

    def calculate_bonus(self):
        # "BigFishBonuses" in source. Last update 2.48 Giftmas Event
        self.value = self.max_value * self.level / (self.level + 100)
        # TODO: "isBigFishUpgUnlocked" in source
        # TODO: "BigFishUpgLVREQ" in source


class AdviceFish(dict[str, AdviceFishUpgrade]):
    def __init__(self, raw_data: dict):
        raw_spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        if not raw_spelunk_info:
            logger.warning("Advice Fish data not present.")
        advice_fish_levels: list[int] = safer_index(raw_spelunk_info, 11, [])
        for index, info in enumerate(advice_fish_upgrade_data):
            level = safer_index(advice_fish_levels, index, 0)
            upgrade = AdviceFishUpgrade(info, level, index)
            self[upgrade.name] = upgrade

    def calculate_bonuses(self):
        for upgrade in self.values():
            upgrade.calculate_bonus()
