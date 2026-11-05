from typing import TypedDict, Callable
from consts.idleon.w7.spelunk import Spelunky

coral_kid_description_templates = [desc.replace("_", " ").replace(" @ ", " ") for desc in Spelunky[25]]

# "this._GenINFO[118] =" in source, first 12 values (6 per page). Last updated in v2.550
coral_kid_upgrades_divinity_requirements = [
    0, 600, 900, 1200, 1500, 1750,
    500, 3000, 5000, 8000, 10000, 12000,
]


# derived from `"CoralKidUpgBonus" == "` in source. Last updated in v2.550
class CoralKidUpgradeBonusFormulaInput(TypedDict):
    level: int
    god_rank: int
    total_divinity_level: int
    coral_reef_upgrade_count: int


coral_kid_upgrades_bonus_base_formulas: list[Callable[[CoralKidUpgradeBonusFormulaInput], int | float]] = [
    lambda data: 10 * data["level"],
    lambda data: 2 * data["level"],
    lambda data: (data["level"] / (25 + data["level"])) * 20,
    lambda data: data["level"],  # "CoralKidUpgBonus" 3 in source. v2.531.0
    lambda data: 2 * data["level"],
    lambda data: (data["level"] / (40 + data["level"])) * 100,
    lambda data: 100 * data["level"],
    lambda data: 10 * data["level"],
    lambda data: 50 * data["level"],
    lambda data: 125 * data["level"] / (data["level"] + 100),
    lambda data: 5 * data["level"],
    lambda data: data["level"],
]

coral_kid_upgrades_bonus_final_formulas: list[Callable[[CoralKidUpgradeBonusFormulaInput], int | float]] = [
    coral_kid_upgrades_bonus_base_formulas[0],
    coral_kid_upgrades_bonus_base_formulas[1],
    lambda data: coral_kid_upgrades_bonus_base_formulas[2](data) * data["god_rank"],
    coral_kid_upgrades_bonus_base_formulas[3],
    lambda data: coral_kid_upgrades_bonus_base_formulas[4](data) * data["coral_reef_upgrade_count"],
    coral_kid_upgrades_bonus_base_formulas[5],
    coral_kid_upgrades_bonus_base_formulas[6],
    coral_kid_upgrades_bonus_base_formulas[7],
    coral_kid_upgrades_bonus_base_formulas[8],
    # "CK_NonDivHourTime" in source: share of AFK hours, capped at 100%
    lambda data: min(100, coral_kid_upgrades_bonus_base_formulas[9](data)),
    coral_kid_upgrades_bonus_base_formulas[10],
    # "Total Bonus" in the Coral Kid UI: compounds per Divinity[25] above 35,
    # i.e. per god_rank above 25
    lambda data: 100 * (
        (1 + coral_kid_upgrades_bonus_base_formulas[11](data) / 100)
        ** max(0, data["god_rank"] - 25)
        - 1
    ),
]
