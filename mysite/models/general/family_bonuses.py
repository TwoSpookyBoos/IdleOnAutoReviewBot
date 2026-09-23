from functools import cached_property

from consts.consts_general import family_bonuses_dict
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from models.general.character import Character
from utils.number_formatting import round_and_trim
from utils.text_formatting import kebab


class FamilyBonus:
    def __init__(self, class_name: str, info: dict):
        self.name: str = class_name
        self.level: int = 0
        self.image: str = f"{kebab(class_name)}-icon"
        self._func_type: str = info['funcType']
        self._x1: float = info['x1']
        self._x2: float = info['x2']
        self._level_discount: int = info['levelDiscount']
        self._post_display: str = info['PostDisplay']

    @cached_property
    def value(self) -> float:
        return self.value_at_level(self.level)

    def value_at_level(self, level: int) -> float:
        return lava_func(self._func_type, level - min(self._level_discount, level), self._x1, self._x2)

    def get_bonus_advice(self, goal_level: int) -> Advice:
        return Advice(
            label=f"{self.name} Family Bonus: {self.value:.2f}"
                  f"/{round_and_trim(self.value_at_level(goal_level))}{self._post_display}"
                  f" at Class Level {self.level}",
            picture_class=self.image,
            progression=self.level,
            goal=goal_level,
        )


class FamilyBonuses(dict[str, FamilyBonus]):
    def __init__(self):
        super().__init__()
        for class_name, info in family_bonuses_dict.items():
            self[class_name] = FamilyBonus(class_name, info)

    def calculate_levels(self, characters: list[Character]):
        for character in characters:
            for class_name in character.all_classes:
                if class_name in self:
                    bonus = self[class_name]
                    bonus.level = max(bonus.level, character.combat_level)
