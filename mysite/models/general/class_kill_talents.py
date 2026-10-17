from collections.abc import Callable
from functools import cached_property

from consts.consts_general import class_kill_talents_dict
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from models.general.character import Character
from utils.all_talentsDict import all_talentsDict
from utils.safer_data_handling import safe_loads, safer_get, safer_math_log
from utils.text_formatting import kebab, notateNumber


class ClassKillTalent:
    def __init__(self, name: str, info: dict, kills: int):
        self.name: str = name
        self.talent_number: int = info["Talent Number"]
        self.bonus_type: str = info["Bonus"]
        self.kills: int = kills
        self.highest_preset_level: int = 0
        self.total_value: float = 0
        self._farm_label: str = info["Farm Label"]
        self._resource: str = info["Resource"]
        talent = all_talentsDict[self.talent_number]
        self._func_type: str = talent["funcX"]
        self._x1: float = talent["x1"]
        self._x2: float = talent["x2"]

    @cached_property
    def kill_stacks(self) -> float:
        return safer_math_log(self.kills, "Lava")

    def talent_value(self, level: int) -> float:
        return lava_func(self._func_type, level, self._x1, self._x2)

    def value_at_level(self, level: int) -> float:
        return self.talent_value(level) * self.kill_stacks

    def calculate_value(self, highest_preset_level: int):
        self.highest_preset_level = highest_preset_level
        self.total_value = self.value_at_level(highest_preset_level)

    def get_kills_advice(self, kill_target: float) -> Advice:
        goal = notateNumber("Basic", kill_target, 1)
        return Advice(
            label=self._farm_label,
            picture_class=kebab(self.name),
            progression=notateNumber("Match", self.kills, 2, "", goal),
            goal=goal,
            resource=self._resource,
        )


class ClassKillTalents(dict[str, ClassKillTalent]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        for name, info in class_kill_talents_dict.items():
            kills = safer_get(raw_optlacc, info["Kills OptLacc"], 0)
            self[name] = ClassKillTalent(name, info, kills)

    def calculate_values(
        self,
        characters: list[Character],
        best_talent_level: Callable[[int, Character], int],
    ):
        # Per current char; account-wide shows the best char
        for talent in self.values():
            talent.calculate_value(
                max(
                    [
                        best_talent_level(talent.talent_number, char)
                        for char in characters
                    ],
                    default=0,
                )
            )
