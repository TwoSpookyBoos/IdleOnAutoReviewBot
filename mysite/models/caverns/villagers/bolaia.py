from dataclasses import dataclass
from math import ceil

from consts.caverns.cavern import cavern_names
from consts.caverns.villager.bolaia import studies_data
from consts.consts_autoreview import EmojiType, ValueToMulti
from models.advice.advice import Advice
from models.caverns.villagers.villager import Villager
from utils.logging import get_logger

logger = get_logger(__name__)


class StudyBonus:
    def __init__(self, index: int, data: dict, level: int):
        self.level = level
        template = data["Template"]
        self._value_per_level = data["PerLevel"]
        self.value = 0
        self._is_multi = "}" in template
        self._caver_number = index + 1
        self._caver_name = cavern_names[self._caver_number]
        # "StudyBolaiaBonuses" in source. Last update v2.497
        match index:
            case 3:
                base = 12
                value_cap = 32
                self.value = min(value_cap, base + self.level * self._value_per_level)
                self._max_level = ceil((value_cap - base) / self._value_per_level)
                value_per_level = self._value_per_level
                cap = f", capped at {value_cap}%"
            case 9:
                base = 50
                self.value = base + self.level * self._value_per_level
                self._max_level = EmojiType.INFINITY.value
                value_per_level = self._value_per_level
                cap = ""
            case _:
                base = "No"
                self.value = self.level * self._value_per_level
                self._max_level = EmojiType.INFINITY.value
                if self._is_multi:
                    value_per_level = f"{ValueToMulti(self._value_per_level) - 1:.2f}"
                else:
                    value_per_level = self._value_per_level
                cap = ""
        if self.level == 0:
            self.value = 0
        self._base_note = f"<br>{base} base, +{value_per_level} per level{cap}"
        if self._is_multi:
            self._description = template.replace("}", f"{ValueToMulti(self.value)}")
        else:
            self._description = template.replace("{", f"{self.value}")

    def get_bonus_advice(self):
        return Advice(
            label=f"{self._caver_name}: {self._description}{self._base_note}",
            picture_class=f"cavern-{self._caver_number}",
            progression=self.level,
            goal=self._max_level,
        )


@dataclass
class Studies(list[StudyBonus]):
    total: int = 0


class Bolaia(Villager):
    def __init__(self, **kwargs):
        super().__init__(name="Bolaia", unlock_at=12, role="The Librarian", **kwargs)
        self.studies = Studies()

    def parse_feature(self, raw_caverns_list: list):
        studies_level_list = raw_caverns_list[26]
        total = 0
        for index, data in enumerate(studies_data):
            level = studies_level_list[index]
            bonus = StudyBonus(index, data, level)
            self.studies.append(bonus)
            total += bonus.level
        self.studies.total = total

    def stat_advices(self) -> list[Advice]:
        return self.base_stat_advice(max_level=None)

    def feature_advice(self) -> dict[str, list[Advice]] | None:
        return {
            "Study Bonuses": [
                Advice(
                    label=f"Total Studies: {self.studies.total}",
                    picture_class=self.name,
                ),
                *(study.get_bonus_advice() for study in self.studies),
            ]
        }
