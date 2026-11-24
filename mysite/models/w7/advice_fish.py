from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.advice_fish import advice_fish_upgrade_data
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.misc.next_break_point_tooltip import next_break_point_tooltip
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class AdviceFishUpgrade:
    # "BigFishBonuses" in source: max * L / (L + 100),
    # so it's the level giving half of the max
    _HALF_LEVEL = 100

    def __init__(self, info: dict, level: int, index: int):
        self.level = level
        self.name = info["Name"]
        self._template = info["Bonus"]
        self.max_value = info["MaxValue"]
        self.value = 0
        self._image = f"advice-fish-{index}"
        self._unit = "%" if "{" in self._template else "x"

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Advice Fish|#advice-fish}} - "
        bonus = f"{self._format_value(self.value)}/{self._format_value(self.max_value)}"
        bonus_description = self._template.replace("{", bonus).replace("}", bonus)
        label += f"{self.name}:<br>Level {self.level}: {bonus_description}"
        current_percent = self.value / self.max_value
        tooltip = ""
        if not link_to_section:
            tooltip = next_break_point_tooltip(
                self.value,
                self.max_value,
                self._HALF_LEVEL,
                self._format_bonus,
            )
        return Advice(
            label=label,
            picture_class=self._image,
            resource="coins",
            goal="100%",
            progression=f"{current_percent:.2%}",
            progression_tooltip=tooltip,
        )

    def _format_value(self, value: float) -> str:
        if self._unit == "%":
            return f"{round_and_trim(value)}"
        return f"{round_and_trim(ValueToMulti(value))}"

    def _format_bonus(self, value: float) -> str:
        return f"{self._format_value(value)}{self._unit}"

    def calculate_bonus(self):
        # "BigFishBonuses" in source. Last update 2.48 Giftmas Event
        self.value = self.max_value * self.level / (self.level + self._HALF_LEVEL)
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
