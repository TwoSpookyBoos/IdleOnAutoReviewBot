from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.research import (
    minehead_bonus_data,
    minehead_opponents_defeated_index,
)
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class MineheadBonus:
    def __init__(self, index: int, info: dict, opponents_defeated: int):
        self.index = index
        self._template = info["Description"]
        self._base_value = info["Value"]
        self.unlocked = opponents_defeated > index
        # "BonusQTY" in source. Last updated in v2.531.0
        self.value = self._base_value if self.unlocked else 0

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Research|#research }} - "
        rendered = self._template.replace(
            "}", f"{round_and_trim(ValueToMulti(self._base_value))}"
        ).replace("{", f"{round_and_trim(self._base_value)}")
        label += f"Minehead Opponent {self.index + 1}:<br>{rendered}"
        return Advice(
            label=label,
            picture_class="mine-tile",
            progression=int(self.unlocked),
            goal=1,
        )


class Minehead(list[MineheadBonus]):
    def __init__(self, raw_data: dict):
        raw_research_info = safe_loads(raw_data.get("Research", []))
        # "Research"[7][4] in source. Last updated in v2.531.0
        self.opponents_defeated: int = safer_convert(
            safer_index(
                safer_index(raw_research_info, 7, []),
                minehead_opponents_defeated_index,
                0,
            ),
            0,
        )
        super().__init__(
            MineheadBonus(index, info, self.opponents_defeated)
            for index, info in enumerate(minehead_bonus_data)
        )
