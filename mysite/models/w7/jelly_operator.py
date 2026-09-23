from math import floor, log2

from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.jelly_operator import (
    jelly_cell_count,
    jelly_obstruction_data,
    jelly_upgrade_shop_order,
    jelly_upgrades,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import (
    safe_loads,
    safer_convert,
    safer_get,
    safer_index,
    safer_math_log,
    safer_math_pow,
)
from utils.text_formatting import notateNumber

logger = get_logger(__name__)


class JellyCell:
    def __init__(self, index: int, info: dict, unlock_level: int, level: int):
        self.index = index
        self.name = info["Name"].replace(" Cell Cultivation", "")
        self.description = info["Description"]
        self.unlocked = unlock_level >= 1
        self.level = level
        # "CellExpREQ" in source
        self.exp_required = 20 * safer_math_pow(1.3, self.level)

    def get_advice(self) -> Advice:
        label = self.name
        if self.unlocked:
            exp = round_and_trim(self.exp_required, 0)
            label += f" (LV {self.level}, {exp} EXP to next)"
        label += f":<br>{self.description}"
        return Advice(
            label=label,
            picture_class=f"jelly-cell-{self.index}",
            progression=int(self.unlocked),
            goal=1,
        )


class JellyUpgrade:
    def __init__(self, index: int, info: dict, level: int):
        self.index = index
        self.name = info["Name"]
        self.description = info["Description"]
        self.max_level = info["Max Level"]
        self.value_per_level = info["Value Per Level"]
        self.level = level
        self.value = 0
        self.total_display: str = ""

    def calculate_bonus(self):
        # "UpgradeQTY" in source
        self.value = self.level * self.value_per_level

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Jelly Operator|#jelly-operator}} - "
        max_value = self.max_level * self.value_per_level
        if "{" in self.description:
            value, displayed_max = self.value, max_value
        else:
            value, displayed_max = ValueToMulti(self.value), ValueToMulti(max_value)
        bonus = f"{round_and_trim(value)}/{round_and_trim(displayed_max)}"
        description = self.description.replace("{", bonus).replace("}", bonus)
        if self.total_display:
            description = description.replace("$", self.total_display)
        label += f"{self.name}:<br>{description}"
        return Advice(
            label=label,
            picture_class=f"jelly-upgrade-{self.index}",
            progression=self.level,
            goal=self.max_level,
        )


class JellyObstruction:
    def __init__(self, index: int, info: dict, obstructions_defeated: int):
        self.index = index
        self.name = info["Name"]
        self.description = info["Description"]
        self.value = info["Value"]
        self.unlocked = obstructions_defeated > index

    def get_advice(self) -> Advice:
        rendered = (
            self.description
            .replace("{", f"{round_and_trim(self.value)}")
            .replace("}", f"{round_and_trim(ValueToMulti(self.value))}")
        )
        return Advice(
            label=f"Obstruction {self.index + 1} - {self.name}:<br>{rendered}",
            picture_class=f"jelly-obstruction-{self.index}",
            progression=int(self.unlocked),
            goal=1,
        )


class JellyOperator:
    def __init__(self, raw_data: dict):
        raw_research = safe_loads(raw_data.get("Research", []))
        if not raw_research:
            logger.warning("Jelly Operator data not present.")

        # Research[7] in source
        misc = safer_index(raw_research, 7, [])
        # capped at len(obstructions) - 1, so the last bonus never unlocks
        self.obstructions_defeated = safer_convert(safer_index(misc, 9, 0), 0)
        self.best_dps = safer_convert(safer_index(misc, 12, 0.0), 0.0)
        self.selected_fever = safer_convert(safer_index(misc, 13, -1), -1)
        self.best_operation_bloodcells = safer_convert(safer_index(misc, 14, 0.0), 0.0)
        # Research[18] in source
        self.slot_unlocks_spent = len(safer_index(raw_research, 18, []))
        # "Have_ban_j" in source
        raw_bundles = safe_loads(raw_data.get("BundlesReceived", {}))
        self.has_bundle_j = int(safer_get(raw_bundles, "ban_j", 0) == 1)

        upgrade_levels = safer_index(raw_research, 17, [])
        cell_levels = safer_index(raw_research, 16, [])
        # "CellLV_tot" in source: 9 slots, not 8
        self.cell_level_total = sum(
            safer_convert(safer_index(cell_levels, index, 0), 0) for index in range(9)
        )

        self.cells: dict[str, JellyCell] = {}
        for index in range(jelly_cell_count):
            cell = JellyCell(
                index,
                jelly_upgrades[index],
                safer_convert(safer_index(upgrade_levels, index, 0), 0),
                safer_convert(safer_index(cell_levels, index, 0), 0),
            )
            self.cells[cell.name] = cell

        # cells are listed separately
        self.upgrades: dict[str, JellyUpgrade] = {}
        for index in jelly_upgrade_shop_order:
            if index < jelly_cell_count:
                continue
            level = safer_convert(safer_index(upgrade_levels, index, 0), 0)
            upgrade = JellyUpgrade(index, jelly_upgrades[index], level)
            self.upgrades[upgrade.name] = upgrade
        self._by_index = {upgrade.index: upgrade for upgrade in self.upgrades.values()}

        self.obstructions: dict[str, JellyObstruction] = {}
        for index, info in enumerate(jelly_obstruction_data):
            obstruction = JellyObstruction(index, info, self.obstructions_defeated)
            self.obstructions[obstruction.name] = obstruction
        self._obstructions_by_index = {o.index: o for o in self.obstructions.values()}

    def _qty(self, index: int) -> float:
        # "UpgradeQTY" in source
        upgrade = self._by_index.get(index)
        return upgrade.value if upgrade else 0

    def _fever_bonus(self, effect: int) -> float:
        # "FeverBonus" in source. Effects 4 and 5 (50/25 and 40) are unmodelled;
        # only 2 and 3 are read here
        if self.selected_fever != effect or self._qty(16) < 1:
            return 0
        return 100 if effect in (1, 2, 3) else 0

    def _dps_multi(self) -> float:
        # "DPSmulti" in source
        best = self.best_dps
        return 1 + (
            min(2, log2(max(best / 100, 1)) / 20)
            + safer_math_log(best, "Lava") / 50
            * 15 / (safer_math_log(best / 50, "Lava") + 20)
        )

    def _currency_multi(self, account) -> float:
        # "CurrencyMulti" in source
        grid_bonus = account.research.grid["Jelly Operator Linguistics"].value
        atoms = account.atom_collider["Atoms"]
        atom_bonus = atoms["Sulfur - Jelly Bloodcell Juicer"]["Value"]
        return (
            (1 + (self._qty(23) + self._qty(24) + self._qty(25)
                  + self._qty(33) * self.cell_level_total) / 100)
            * (1 + account.arcade[72].value / 100)
            * (1 + grid_bonus / 100)
            * (1 + self._fever_bonus(2) / 100)
            * (1 + self.has_bundle_j)
            * (1 + self._obstruction_value(24) / 100)
            * self._dps_multi()
            * (1 + self._qty(26) / 100)
            * (1 + self._qty(27) / 100)
            * (1 + atom_bonus / 100)
        )

    def _obstruction_value(self, index: int) -> float:
        # "RoG_BonusQTY" in source
        obstruction = self._obstructions_by_index.get(index)
        return obstruction.value if obstruction and obstruction.unlocked else 0

    def calculate_bonuses(self, account):
        for upgrade in self.upgrades.values():
            upgrade.calculate_bonus()

        exp_multi = (
            (1 + self._fever_bonus(3) / 100)
            * (1 + (self._qty(30) + self._qty(31) + self._qty(10)) / 100)
            * (1 + self._qty(11) / 100)
        )
        slots_left = round(
            self._qty(9) + self._qty(8) + self._obstruction_value(44)
            + self.has_bundle_j - self.slot_unlocks_spent
        )
        totals = {
            9: f"{slots_left}",
            10: f"{floor(100 * exp_multi) / 100}",
            15: f"{round(1 + self._qty(15))}",  # "VirusesAllowed"
            17: f"{round(1 + self._qty(17))}",
            23: f"{round(100 * self._currency_multi(account)) / 100}",
            29: f"{round_and_trim(1 + (50 + self._qty(29)) / 100)}",  # "RoidMulti"
            32: f"{round_and_trim(self._qty(32) * floor(self.cell_level_total / 10))}",
            33: f"{round_and_trim(self._qty(33) * self.cell_level_total)}",
            34: f"{round(10000 * (1 - 1 / (1 + self._qty(34) / 100))) / 100}",
            # "BloodcellDaily" in source
            38: notateNumber(
                "Basic", self.best_operation_bloodcells * self._qty(38) / 100, 2
            ),
        }
        for index, display in totals.items():
            upgrade = self._by_index.get(index)
            if upgrade:
                upgrade.total_display = display

        # the flat "1.01x" grows with Cell Mutilation
        cell_biology = self._by_index.get(10)
        if cell_biology and self._qty(17) >= 1:
            multiplier = ValueToMulti(1 + self._qty(17))
            cell_biology.description = cell_biology.description.replace(
              "1.01x", f"{multiplier:.2f}x"
            )
