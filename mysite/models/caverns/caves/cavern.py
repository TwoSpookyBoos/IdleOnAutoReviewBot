from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

from models.advice.advice import Advice


class Cavern(ABC):
    def __init__(self, name: str, cavern_number: int):
        self.name = name
        self.cavern_number = cavern_number
        self._image = f"cavern-{cavern_number}"
        self.opals_found: int = 0

    @cached_property
    def unlocked(self) -> bool:
        from models.general.session_data import session_data
        polonai_level = session_data.account.caverns_.villagers["Polonai"].level
        return polonai_level >= self.cavern_number

    def parse_opals_found(self, raw_caverns_list: list):
        try:
            self.opals_found = raw_caverns_list[7][self.cavern_number - 1] or 0
        except Exception:
            self.opals_found = 0

    @abstractmethod
    def parse(self, raw_caverns_list: list):
        pass

    def pre_string(self) -> str:
        return f"Cavern {self.cavern_number}- {self.name}"

    def objective_advice(self, objective: str, **kwargs: Any) -> Advice:
        return Advice(
            label=f"Objective- {objective}",
            picture_class=self._image,
            **kwargs,
        )

    def opals_found_advice(self) -> Advice:
        return Advice(
            label=f"Total Opals Found: {self.opals_found}",
            picture_class='opal',
        )
