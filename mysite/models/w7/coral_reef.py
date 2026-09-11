from consts.w7.coral_reef import coral_reef_bonus_data
from models.advice.advice import Advice
from utils.safer_data_handling import (
    safe_loads,
    safer_convert,
    safer_index,
    safer_math_pow,
)


class CoralReefBonus:
    def __init__(self, index: int, info: dict, unlocked: bool, level: int):
        self.name = info["Name"]
        self.description = info["Description"]
        self.max_level = info["Max Level"]
        self.image = f"coral-{index}"
        self.unlocked = unlocked
        self.level = level
        self.next_cost = int(
            info["Coefficient"] * safer_math_pow(info["Exponent Base"], self.level, 0)
        )

    def get_advice(self) -> Advice:
        unlock_or_upgrade_text = "Level up" if self.unlocked else "Unlock"
        next_level_cost_text = (
            f"<br>Next level costs {self.next_cost} corals"
            if self.unlocked and self.level < self.max_level
            else ""
        )
        return Advice(
            label=(
                f"{unlock_or_upgrade_text} {self.name}: {self.description}"
                f"{next_level_cost_text}"
            ),
            picture_class=self.image,
            progression=self.level,
            goal=self.max_level,
            resource="coral",
        )


class CoralReef(dict[str, CoralReefBonus]):
    def __init__(self, raw_data: dict):
        raw_spelunk = safe_loads(raw_data.get("Spelunk", []))
        self.town_corals = safer_convert(
            safer_index(safer_index(raw_spelunk, 4, []), 5, 0), 0
        )

        unlocked_reef_corals = safer_index(raw_spelunk, 12, [])
        coral_levels = safer_index(raw_spelunk, 13, [])

        for index, info in enumerate(coral_reef_bonus_data):
            unlocked = bool(safer_index(unlocked_reef_corals, index, False))
            level = safer_index(coral_levels, index, 0)
            bonus = CoralReefBonus(index, info, unlocked, level)
            self[bonus.name] = bonus

        self.total_level = sum(bonus.level for bonus in self.values())
