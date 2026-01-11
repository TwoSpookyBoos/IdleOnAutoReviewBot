from math import floor

from consts.consts_autoreview import ValueToMulti, MultiToValue, EmojiType
from consts.idleon.w6.emperor import (
    emperor_bonus_description,
    emperor_bonus_values,
    emperor_fight_bonus_index,
)
from consts.w6.emperor import emperor_bonus_info

from models.advice.advice import Advice
from models.w6.sneaking import Emporium

from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safer_convert, safer_index, safer_math_pow
from utils.text_formatting import notateNumber

from utils.logging import get_logger

logger = get_logger(__name__)


class EmperorBonus:
    def __init__(self, index: int, wins: int):
        self.wins = wins
        self._value_per_win = emperor_bonus_values[index]
        self._template, (self._bonus_type, display_name) = emperor_bonus_description[
            index
        ]
        bonus_info = emperor_bonus_info[index]
        self.name = bonus_info.get("rename", display_name)
        self._image = bonus_info["image"]

    def calculate_bonus(self, emperor_bonus_multi):
        self.value = floor(self.wins * self._value_per_win * emperor_bonus_multi)
        match self._bonus_type:
            case "$%":
                self._reward_per_win = ""
                self.value = 1 - (self.value / (self.value + 100))
                self._description = self._template.replace(
                    "$", f"{round_and_trim((1 - self.value) * 100)}"
                )
            case "+{" | "+{%":
                self._reward_per_win = self._bonus_type.replace(
                    "{", f"{self._value_per_win}"
                )
                self._description = self._template.replace(
                    "{", f"{round_and_trim(self.value, 0)}"
                )
            case "}x":
                self._reward_per_win = self._bonus_type.replace(
                    "}", f"+{round_and_trim(ValueToMulti(self._value_per_win) - 1)}"
                )
                self._description = self._template.replace(
                    "}", f"{round_and_trim(ValueToMulti(self.value))}"
                )

    def get_bonus_advice(self, link_to_section: bool = True):
        label = ""
        if link_to_section:
            label += "{{Emperor Showdown|#emperor}}:<br>"
        label += self._description
        if not link_to_section and self._reward_per_win:
            label += f"<br>{self._reward_per_win} per level"
        return Advice(
            label=label,
            picture_class="the-emperor" if link_to_section else self._image,
            progression=self.wins,
            goal=EmojiType.INFINITY.value,
        )


class Emperor(dict[str, EmperorBonus]):
    """
    Class for Emperor fight stat and bonus
    Use Emperor[bonus_name] to get emperor bonus.
    """

    def __init__(self, raw_data):
        raw_optlacc = raw_data.get("OptLacc", [])
        self._last_showdown = safer_convert(safer_index(raw_optlacc, 369, 0), 0)
        self.daily_attempts = 1 + safer_convert(safer_index(raw_optlacc, 382, 0), 0)
        self.attempts = 1 - safer_convert(safer_index(raw_optlacc, 370, 0), 0)
        wins = [0] * len(emperor_bonus_description)
        for running_total in range(0, self._last_showdown):
            fight_index = running_total % 48
            bonus_index = emperor_fight_bonus_index[fight_index]
            wins[bonus_index] += 1
        for bonus_index, bonus in enumerate(emperor_bonus_description):
            bonus = EmperorBonus(bonus_index, wins[bonus_index])
            self[bonus.name] = bonus

    def calculate_max_attempt(self, gemshop, emporium: Emporium):
        # "MaxEmperorAttemptStack" in source. Last updated in v2.48
        self.max_attempts = (
            5  # Base
            + emporium["Emperor Season Pass"].value
            + (6 * gemshop["Purchases"]["Lifetime Tickets"]["Owned"])
        )

    def calculate_bonus_multi(self, arcade, tesseract):
        # "EmperorBon" in source multi in return. Last updated in v2.48
        self.bonus_multi = ValueToMulti(
            arcade[51]["Value"]
            + MultiToValue(tesseract["Upgrades"]["Vicar of the Emperor"]["Total Value"])
        )

    def calculate_bonuses(self):
        for bonus in self.values():
            bonus.calculate_bonus(self.bonus_multi)

    def get_upcoming_figths_advice(self) -> list[Advice]:
        advice_list = []
        for next_showdown in range(self._last_showdown, self._last_showdown + 20):
            fight_index = next_showdown % 48
            bonus_index = emperor_fight_bonus_index[fight_index]
            template, (bonus_type, _) = emperor_bonus_description[bonus_index]
            value = emperor_bonus_values[bonus_index]
            match bonus_type:
                case "}x":
                    reward = template.replace(
                        "}", f"+{round_and_trim(ValueToMulti(value) - 1)}"
                    )
                case "+{" | "+{%":
                    reward = template.replace("{", f"{round_and_trim(value)}")
                case "$%":
                    reward = template.replace("$", f"{round_and_trim(value)}")
            bonus_info = emperor_bonus_info[bonus_index]
            showdown_number = next_showdown + 1
            advice_list.append(
                Advice(
                    label=f"Showdown {showdown_number}"
                    f"<br>HP: {self._calculate_emperor_health(next_showdown)}"
                    f"<br>Reward: {reward}",
                    picture_class=bonus_info["image"],
                    progression=self._last_showdown,
                    goal=showdown_number,
                )
            )
        return advice_list

    def _calculate_emperor_health(self, showdown_index: int) -> str:
        # _customBlock_Thingies -> if ("Boss6HP" == d)
        # Last updated in v2.48 Giftmas Event (December 8, 2025).
        hp = 135e12 * safer_math_pow(1.54, showdown_index)
        hp_string = notateNumber("Basic", hp, 2)
        return hp_string

    def get_currency_advice(self) -> Advice:
        return Advice(
            label=f"Daily Attempts: {self.daily_attempts}"
            f"<br>Current Attempts: {self.attempts}/{self.max_attempts}",
            picture_class="lifetime-tickets",
            completed=True,
        )
