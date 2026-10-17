from consts.consts_w3 import prayers_dict
from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads


class Prayer:
    def __init__(self, info: dict, raw_level):
        self.name: str = info["Name"]
        self.material: str = info["Material"]
        self.level: int = 0
        self.bonus_value: float = 0
        self.bonus_string: str = "Level at least once to receive the bonus!"
        self.curse_value: float = 0
        self.curse_string: str = "Level at least once to receive the curse!"
        try:
            self.level = int(raw_level)
        except (TypeError, ValueError):
            return
        if self.level > 0:
            self.bonus_value = lava_func(
                info["bonus_funcType"], self.level, info["bonus_x1"], info["bonus_x2"]
            )
            self.curse_value = lava_func(
                info["curse_funcType"], self.level, info["curse_x1"], info["curse_x2"]
            )
        self.bonus_string = (
            f"{info['bonus_pre']}{self.bonus_value}{info['bonus_post']}"
            f" {info['bonus_stat']}"
        )
        self.curse_string = (
            f"{info['curse_pre']}{self.curse_value}{info['curse_post']}"
            f" {info['curse_stat']}"
        )

    def get_advice(self, goal: int) -> Advice:
        return Advice(
            label=self.name,
            picture_class=self.name,
            progression=self.level,
            goal=goal,
            resource=self.material,
        )


class Prayers(dict[str, Prayer]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_levels = safe_loads(raw_data.get("PrayOwned", []))
        for index, info in prayers_dict.items():
            raw_level = raw_levels[index] if index < len(raw_levels) else None
            self[info["Name"]] = Prayer(info, raw_level)
