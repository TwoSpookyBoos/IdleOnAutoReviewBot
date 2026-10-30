from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from models.advice.advice import Advice
from utils.safer_data_handling import safer_convert, safer_index

if TYPE_CHECKING:
    from models.w7.menagerie import Menagerie


class Jellyfish(ABC):
    def __init__(self, index: int, info: dict, menagerie: Menagerie):
        self.index = index
        self.name = info["Name"]
        self.unlock_index: int | None = info["Unlock Index"]
        self.menagerie = menagerie
        self.image = f"menagerie-jelly-{index}"

    @staticmethod
    def _misc(raw_menagerie: list, index: int) -> float:
        # "Menagerie"[0] in source: Lumi, Shells, Rank and the jellyfish counters
        misc = safer_index(raw_menagerie, 0, [])
        return safer_convert(safer_index(misc, index, 0), 0)

    @abstractmethod
    def parse_feature(self, raw_menagerie: list):
        pass

    @abstractmethod
    def _feature_advices(self) -> list[Advice]:
        pass

    @property
    def unlocked(self) -> bool:
        # "SideJellyUnlocked" in source
        if self.unlock_index is None:
            return True
        return self.menagerie.unlocks[self.unlock_index].owned

    def get_advices(self) -> list[Advice]:
        if self.unlocked:
            return self._feature_advices()
        unlock = self.menagerie.unlocks[self.unlock_index]
        return [
            Advice(
                label=(
                    f"Needs Menagerie Unlock {unlock.index + 1}: {unlock.description}"
                ),
                picture_class=f"menagerie-unlock-{unlock.index}",
                progression=0,
                goal=1,
            )
        ]
