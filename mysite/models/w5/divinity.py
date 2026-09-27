from math import ceil

from consts.consts_autoreview import default_huge_number_replacement
from consts.consts_w5 import (
    divinity_divinities_dict,
    divinity_offerings_dict,
    getDivinityNameFromIndex,
    getStyleNameFromIndex,
)
from models.advice.advice import Advice
from models.general.character import Character
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_math_pow

logger = get_logger(__name__)


class God:
    def __init__(self, index: int, info: dict, unlocked: bool, blessing_level: int):
        self.index: int = index
        self.name: str = info["Name"]
        self.unlocked: bool = unlocked
        self.blessing_level: int = blessing_level
        self.blessing_material: str = info["BlessingMaterial"]

    def get_blessing_advice(self, additional_text: str = "") -> Advice:
        return Advice(
            label=f"{self.name} Blessing{additional_text}",
            picture_class=self.name,
            progression=self.blessing_level,
            goal=100,
            resource=self.blessing_material,
        )


class Divinity(dict[int, God]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_divinity = safe_loads(raw_data.get("Divinity", []))
        if not raw_divinity:
            logger.warning("Divinity data not present")
        while len(raw_divinity) < 40:
            raw_divinity.append(0)
        self._raw_divinity: list = raw_divinity

        self.points = raw_divinity[24]
        if isinstance(self.points, str):
            try:
                self.points = int(float(self.points))
            except ValueError:
                logger.exception(
                    f"Could not convert {self.points} to int. Defaulting to 0"
                )
                self.points = 0
        self.gods_unlocked: int = min(10, raw_divinity[25])
        self.god_rank: int = max(0, raw_divinity[25] - 10)
        self.low_offering: int = raw_divinity[26]
        self.high_offering: int = raw_divinity[27]
        self.low_offering_goal = ""
        self.high_offering_goal = ""
        self.account_wide_arctis: bool = False

        for index, info in divinity_divinities_dict.items():
            # Snake is index 1, its Blessing level is stored in 28
            self[index] = God(
                index, info, self.gods_unlocked >= index, raw_divinity[index + 27]
            )

    def named(self, name: str) -> God:
        return next(god for god in self.values() if god.name == name)

    def link_characters(self, characters: list[Character]):
        for character in characters:
            try:
                character.setDivinityStyle(
                    getStyleNameFromIndex(self._raw_divinity[character.character_index])
                )
                character.setDivinityLink(
                    getDivinityNameFromIndex(
                        self._raw_divinity[character.character_index + 12] + 1
                    )
                )
            except (IndexError, TypeError):
                continue

    def calculate(self, account_wide_arctis: bool, div_cost_after_3: float):
        self.account_wide_arctis = account_wide_arctis
        unlocked = self.gods_unlocked + self.god_rank
        self.low_offering_goal = offering_cost(
            div_cost_after_3, self.low_offering, unlocked
        )
        self.high_offering_goal = offering_cost(
            div_cost_after_3, self.high_offering, unlocked
        )


def offering_cost(div_cost_after_3: float, offering_index: int, unlocked: int) -> int:
    try:
        cost = (
            (
                20 * safer_math_pow(unlocked + 1.3, 2.3) * safer_math_pow(2.2, unlocked)
                + 60
            )
            * divinity_offerings_dict.get(offering_index, {}).get("Chance", 1)
            / 100
        )
        if unlocked >= 3:
            cost = cost * safer_math_pow(
                min(1.8, max(1, 1 + div_cost_after_3 / 100)), unlocked - 2
            )
        return ceil(cost)
    except OverflowError:
        logger.exception(
            f"Could not calc Divinity Offering cost with {unlocked} unlocked. "
            f"Returning {default_huge_number_replacement}"
        )
        return default_huge_number_replacement
