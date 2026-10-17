from functools import cached_property

from consts.consts_w1 import (
    get_seraph_cosmos_max_summ_level_goal,
    get_seraph_cosmos_multi,
    get_seraph_cosmos_summ_level_goal,
    get_seraph_stacks,
    seraph_max,
    starsigns_dict,
)
from models.advice.advice import Advice
from models.w4.lab_chips import LabChip
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safe_loads, safer_get

logger = get_logger(__name__)


def get_infinite_star_sign_levels(infinite_shiny_levels: int) -> int:
    # Passives don't use up infinite levels
    infinite_levels = infinite_shiny_levels * 2 + 5
    i = 1
    while i < min(len(starsigns_dict), infinite_levels):
        infinite_levels += int(starsigns_dict[i]["Passive"])
        i += 1
    return infinite_levels


class StarSign:
    def __init__(self, index: int, info: dict, unlocked: bool):
        self.name: str = info["Name"]
        self.index: int = index
        self.passive: bool = info["Passive"]
        self.unlocked: bool = unlocked

    def is_infinite(self, infinite_levels: int) -> bool:
        return self.unlocked and self.index <= infinite_levels

    def is_equipped(self, character) -> bool:
        return (self.index - 1) in character.equipped_star_signs

    def value_for(
        self, character, base: float, infinite_levels: int, seraph_multi: float
    ) -> float:
        # "StarSigns" in source. Last updated in v2.531.0
        infinite = self.is_infinite(infinite_levels)
        if not (infinite or self.is_equipped(character)):
            return 0
        value = base * seraph_multi
        if infinite and "Silkrode Nanochip" in character.equipped_lab_chips:
            value *= 2
        return value

    def get_unlock_advice(self) -> Advice:
        return Advice(
            label=f"Unlock {self.name}",
            picture_class=self.name.strip("."),
            progression=int(self.unlocked),
            goal=1,
        )


class StarSigns(dict[str, StarSign]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_star_signs = safe_loads(raw_data.get("StarSg", {}))
        for index, info in starsigns_dict.items():
            try:
                # Saved as either "1" or 1
                unlocked = (
                    parse_number(
                        safer_get(raw_star_signs, info["Name"].replace(" ", "_"), 0)
                    )
                    > 0
                )
            except Exception as e:
                logger.warning(
                    f"Star Sign Parse error at signIndex {index}: {e}. "
                    f"Defaulting to Locked"
                )
                unlocked = False
            self[info["Name"]] = StarSign(index, info, unlocked)

        self.seraph_multi: float = 1
        self.seraph_goal: int = 0
        self.seraph_eval: str = ""
        self._max_summoning_level: int = 0
        self.silkrode_owned: bool = False
        self.silkrode_multi: int = 1
        self._silkrode_chip: LabChip | None = None
        self._silkrode_eval: str = ""

    @cached_property
    def unlocked_count(self) -> int:
        return sum(sign.unlocked for sign in self.values())

    def calculate_seraph(
        self, astrology_cultism_level: int, summoning_levels: list[int]
    ):
        max_summoning_goal = get_seraph_cosmos_max_summ_level_goal(
            astrology_cultism_level
        )
        self.seraph_multi = get_seraph_cosmos_multi(
            astrology_cultism_level=astrology_cultism_level,
            all_summoning_levels=summoning_levels,
        )
        self.seraph_goal = get_seraph_cosmos_summ_level_goal(
            astrology_cultism_level=astrology_cultism_level,
            all_summoning_levels=summoning_levels,
        )
        self._max_summoning_level = max(summoning_levels, default=0)
        min_stacks = get_seraph_stacks(min(summoning_levels, default=0))
        max_stacks = get_seraph_stacks(self._max_summoning_level)
        inequality_notice = (
            " (Note: Some lower leveled characters have less)"
            if min_stacks != max_stacks
            else ""
        )
        if self["Seraph Cosmos"].unlocked:
            multi = round(self.seraph_multi, 3)
            self.seraph_eval = f"Multis Passive signs by {multi:g}/{seraph_max}x."
        else:
            self.seraph_eval = (
                f"Locked. Would increase other Passive signs by "
                f"{self.seraph_multi:.2f}/{seraph_max}x if unlocked.{inequality_notice}"
            )
            self.seraph_multi = 1
        if self.seraph_goal < max_summoning_goal:
            self.seraph_eval += (
                f" Increases every 20 Summoning levels.{inequality_notice}"
            )

    def calculate_silkrode(self, silkrode_chip: LabChip):
        self._silkrode_chip = silkrode_chip
        self.silkrode_owned = silkrode_chip.owned
        if self.silkrode_owned:
            self._silkrode_eval = (
                f"{silkrode_chip.count} owned. Doubles star signs when equipped."
            )
            self.silkrode_multi = 2
        else:
            self._silkrode_eval = "None Owned. Would double other signs if equipped."
            self.silkrode_multi = 1

    def get_seraph_advice(self) -> Advice:
        return Advice(
            label=f"{{{{ Star Sign|#star-signs }}}} - Seraph Cosmos: "
            f"{self.seraph_eval}",
            picture_class="seraph-cosmos",
            progression=self._max_summoning_level,
            goal=self.seraph_goal,
            completed=True if self.seraph_multi == seraph_max else None,
        )

    def get_silkrode_advice(self) -> Advice:
        return self._silkrode_chip.get_advice(f": {self._silkrode_eval}")
