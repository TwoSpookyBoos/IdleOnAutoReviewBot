import math
from abc import ABC, abstractmethod
from dataclasses import dataclass

from consts.caverns.cavern import cavern_names
from models.advice.advice import Advice
from utils.safer_data_handling import safer_math_pow


@dataclass
class Villager(ABC):
    index: int
    level: int
    exp: float
    opals: int
    name: str
    unlock_at: int
    role: str

    def __post_init__(self):
        self.title = f"{self.name}, {self.role}"

    @abstractmethod
    def parse_feature(self, raw_caverns_list: list):
        pass

    @abstractmethod
    def stat_advices(self) -> list[Advice]:
        pass

    @abstractmethod
    def feature_advice(self) -> dict[str, list[Advice]] | None:
        pass

    def calculate_exp_percent(self, game_version: float):
        self._level_percent = self.exp / self._next_level_exp(game_version)

    def _next_level_exp(self, game_version):
        # "VillagerExpREQ" in source. Last update 2.495
        match self.index:
            case 0:
                if self.level == 1:
                    result = 5
                else:
                    result = (
                        10
                        * (
                            (10 + 7 * safer_math_pow(self.level, 2.1))
                            * safer_math_pow(2.1, self.level)
                            * (1 + 0.75 * max(0, self.level - 4))
                            * safer_math_pow(
                                3.4,
                                min(
                                    1,
                                    max(0, math.floor((1e5 + game_version) / 100247.3)),
                                )
                                * max(0, self.level - 12),
                            )
                        )
                        - 1.5
                    )
            case 1:
                result = 30 * (
                    (10 + 6 * safer_math_pow(self.level, 1.8))
                    * safer_math_pow(1.57, self.level)
                )
            case 2:
                result = 50 * (
                    (10 + 5 * safer_math_pow(self.level, 1.7))
                    * safer_math_pow(1.4, self.level)
                )
            case 3:
                result = 120 * (
                    (30 + 10 * safer_math_pow(self.level, 2))
                    * safer_math_pow(2, self.level)
                )
            case 4:
                result = (
                    500
                    * (10 + 5 * safer_math_pow(self.level, 1.3))
                    * safer_math_pow(1.13, self.level)
                )
            case _:
                result = 10 * safer_math_pow(10, 20)
        return result

    def base_stat_advice(self, max_level: int | None) -> list[Advice]:
        return [
            # Practical Max Level
            Advice(
                label=f"{self.title} level for all implemented unlocks",
                picture_class=self.name,
                progression=self.level,
                goal=max_level if max_level is not None else "",
            ),
            Advice(
                label="Next level progress",
                picture_class=self.name,
                progression=f"{self._level_percent * 100:.1f}",
                goal=100,
                unit="%",
            ),
            # Invested Opals
            Advice(
                label="Opals Invested",
                picture_class="opal",
                progression=self.opals,
            ),
        ]

    def level_ready_alert(self) -> Advice | None:
        if self._level_percent < 1:
            return None
        return Advice(
            label=f"{{{{ {self.name}|#villagers }}}} ready to level!",
            picture_class=self.name,
        )

    def get_unlock_advice(self, explorer_level: int) -> Advice:
        cavern_name = cavern_names[self.unlock_at]
        return Advice(
            label=f"Discover Villager {self.title} at Cavern {cavern_name}",
            picture_class=f"{self.name}-undiscovered",
            progression=explorer_level,
            goal=self.unlock_at,
        )
