from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from models.advice.advice import Advice
from models.caverns.caves import Caves
from models.caverns.villagers import Villagers
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get

logger = get_logger(__name__)


class Caverns:
    def __init__(self, raw_data: dict):
        raw_caverns_list: list[list] = safe_loads(raw_data.get("Holes", []))
        if not raw_caverns_list:
            logger.warning("Caverns data not present.")
        while len(raw_caverns_list) < 30:
            raw_caverns_list.append([0] * 100)
        game_version = safer_get(raw_data, "DoOnceREAL", 0.00)
        self.villagers: Villagers = Villagers(raw_caverns_list, game_version)
        self.caves: Caves = Caves(raw_caverns_list)

    @cached_property
    def skilling_resource_discount(self) -> float:
        # Depends on: Bolaia's studies, each SkillingCavern's layers_destroyed,
        # and The Jar's Amethyst Heartstone collectible.
        collectible_bonus = (
            self.caves["The Jar"].collectibles["Amethyst Heartstone"].value
        )
        return ValueToMulti(
            collectible_bonus
            + (
                self.villagers["Bolaia"].studies[1].value
                * self.caves["Motherlode"].layers_destroyed
            )
            + (
                self.villagers["Bolaia"].studies[7].value
                * self.caves["The Hive"].layers_destroyed
            )
            + (
                self.villagers["Bolaia"].studies[11].value
                * self.caves["Evertree"].layers_destroyed
            )
            # Trench not implemented as of v2.31
        )

    @cached_property
    def skilling_resource_discount_advice(self) -> Advice:
        return Advice(
            label=(
                f"Resource Divisor from Amethyst Heartstone Collectible + Bolaia "
                f"Studies: {self.skilling_resource_discount:.3f}"
            ),
            picture_class="bolaia",
        )
