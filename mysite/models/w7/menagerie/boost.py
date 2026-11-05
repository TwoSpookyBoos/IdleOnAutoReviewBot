from __future__ import annotations

from typing import TYPE_CHECKING

from consts.consts_autoreview import ValueToMulti
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.text_formatting import notateNumber

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie


class MenagerieBoost:
    def __init__(self, index: int, info: dict, level: int, menagerie: Menagerie):
        self.index = index
        self.description = info["Description"]
        self.value_per_level = info["Value Per Level"]
        self.level = level
        self.menagerie = menagerie
        # "BoostQTY" in source
        self.value = self.value_per_level * self.level
        # "Cost" 2 in source, in Lumi
        self.cost = (
            3 * level
            + level**1.5
            + (5 + index**1.5)
            * max(1.45, 2.25 + (index / 4) * -0.15) ** index
            * self._cost_exponent() ** level
        )

    def _cost_exponent(self) -> float:
        # "CostExponent" in source. Last updated in v2.550.0
        match self.index:
            case 8 | 10 | 12:
                return 35
            case 2 | 5 | 17:
                return 22.8
            case 6:
                return 3.5
            case 0 | 1 | 7:
                return 2.1
            case _:
                return 1.3

    @property
    def visible(self) -> bool:
        # "UpgUnlocked" 2 in source
        return self.index < self.menagerie.visible_boosts

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = "{{Menagerie|#luminous-menagerie}} - " if link_to_section else ""
        if "}" in self.description:
            value = round_and_trim(ValueToMulti(self.value))
        else:
            value = round_and_trim(self.value)
        description = self.description.replace("{", f"{value}").replace("}", f"{value}")
        label += f"Boost {self.index + 1}: {description}"
        if self.visible:
            label += f"<br>Next LV costs {notateNumber('Basic', self.cost, 2)} Lumi"
        else:
            label += "<br>Needs a higher Menagerie Rank"
        return Advice(
            label=label,
            picture_class=f"menagerie-boost-{self.index}",
            progression=self.level,
        )
