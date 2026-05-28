from typing import TypedDict, Callable
from consts.idleon.w7.spelunk import Spelunky

coral_kid_description_templates = [desc.replace("_", " ").replace(" @ ", " ") for desc in Spelunky[25]]

# "this._GenINFO[118] =" in source. Last updates in v2.505 May 25
coral_kid_upgrades_divinity_requirements = [0, 600, 900, 1250, 1700, 2200]


# derived from `"CoralKidUpgBonus" == "` in source. Last updated in v2.505 May 25
class CoralKidUpgradeBonusFormulaInput(TypedDict):
    level: int
    god_rank: int
    total_divinity_level: int
    coral_reef_upgrade_count: int


coral_kid_upgrades_bonus_base_formulas: list[Callable[[CoralKidUpgradeBonusFormulaInput], int | float]] = [
    lambda data: 10 * data["level"],
    lambda data: 2 * data["level"],
    lambda data: 20 * data["level"] / (25 + data["level"]),
    lambda data: -1,
    lambda data: 2 * data["level"],
    lambda data: 100 * data["level"] / (40 + data["level"])
]

coral_kid_upgrades_bonus_final_formulas: list[Callable[[CoralKidUpgradeBonusFormulaInput], int | float]] = [
    coral_kid_upgrades_bonus_base_formulas[0],
    coral_kid_upgrades_bonus_base_formulas[1],
    lambda data: coral_kid_upgrades_bonus_base_formulas[2](data) * data["god_rank"],
    lambda data: -1,
    lambda data: coral_kid_upgrades_bonus_base_formulas[4](data) * data["coral_reef_upgrade_count"],
    coral_kid_upgrades_bonus_base_formulas[5],
]
