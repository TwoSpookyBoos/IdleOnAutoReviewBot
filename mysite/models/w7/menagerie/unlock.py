from __future__ import annotations

from typing import TYPE_CHECKING

from models.advice.advice import Advice
from utils.text_formatting import notateNumber

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie


class MenagerieUnlock:
    def __init__(self, index: int, info: dict, owned: bool, menagerie: Menagerie):
        self.index = index
        self.description = info["Description"]
        self.tooltip = info["Tooltip"]
        self.owned = owned
        self.menagerie = menagerie
        # "Cost" 1 in source, in Lumi
        self.cost = (10 + index**2) * max(1.6, 2.5 + (index / 4) * -0.15) ** index

    @property
    def visible(self) -> bool:
        # "UpgUnlocked" 1 in source
        return self.index < self.menagerie.visible_unlocks

    def get_advice(self) -> Advice:
        label = f"Unlock {self.index + 1}: {self.description}"
        if self.tooltip:
            label += f"<br>{self.tooltip}"
        if not self.owned:
            label += f"<br>Costs {notateNumber('Basic', self.cost, 2)} Lumi"
            if not self.visible:
                label += ", needs a higher Menagerie Rank"
        return Advice(
            label=label,
            picture_class=f"menagerie-unlock-{self.index}",
            progression=int(self.owned),
            goal=1,
        )
