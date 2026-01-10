from consts.consts_autoreview import EmojiType
from consts.consts_item_data import ITEM_DATA

from models.advice.advice import Advice

from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safer_math_log
from utils.text_formatting import getItemCodeName

from utils.logging import get_logger

logger = get_logger(__name__)


class GoldenFood:
    """
    Class for track of golden item, calculate it's bonus and generate advice
    for it
    """

    def __init__(self, name: str, amount: int = 0):
        self.name = name
        self.amount = amount
        item_data = ITEM_DATA[getItemCodeName(name)]
        self.bonus_coefficient = item_data.amount
        self._description = item_data.description
        self.bonus_value = 0
        self.max_bonus = None

    def calculate_bonus(self, golden_food_multi, max_amount: int | None = None):
        self.bonus_value = self._calculate_bonus(golden_food_multi, self.amount)
        if max_amount is not None:
            self.max_bonus = self._calculate_bonus(golden_food_multi, max_amount)

    def _calculate_bonus(self, golden_food_multi, amount):
        # _customBlock_GoldFoodBonuses in source. Last update v2.48 Jan 01 2026
        log_value = safer_math_log(1 + amount, "lava")
        return (
            self.bonus_coefficient
            * 0.05
            * golden_food_multi
            * log_value
            * (1 + log_value / 2.14)
        )

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        """Advice for golden food bonus"""
        label = ""
        if link_to_section:
            label += "{{Beanstalk|#beanstalk}} - "
        if self.max_bonus is not None:
            goal = self.max_bonus
            bonus = f"{round_and_trim(self.bonus_value)}/{round_and_trim(goal)}"
        else:
            bonus = f"{round_and_trim(self.bonus_value)}"
            goal = EmojiType.INFINITY.value
        description = (
            self._description.replace(". Golden foods are never consumed", "")
            .replace("[", bonus)
            .strip()
        )
        label += f"{self.name}: {description}"
        return Advice(
            label=label, picture_class=self.name, progression=self.amount, goal=goal
        )
