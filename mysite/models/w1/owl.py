from math import floor

from consts.consts_autoreview import ValueToMulti
from consts.progression_tiers import owl_bonuses_of_orion
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_index, safer_convert, logger


class OwlBonus:
    def __init__(self, name: str, base_value: float):
        self.name = name
        self.base_value = base_value
        self.num_unlocked = 0
        self.value = 0

    def calculate(self, num_unlocked: int, megafeather_mod: float, legend_talent_multi: float):
        self.num_unlocked = num_unlocked
        self.value = safer_convert(self.base_value * num_unlocked * megafeather_mod * legend_talent_multi, 0)

    def get_bonus_advice(self, link_to_section: bool = True, progression: int = 0, resource: str = "", goal=None) -> Advice:
        link_to_section_text = f"{{{{ Owl|#owl }}}}- " if link_to_section else ""
        return Advice(
            label=f"{link_to_section_text}{self.name}:<br>+{self.value}% {self.name}",
            picture_class='the-great-horned-owl',
            progression=progression,
            resource=resource,
            goal=goal,
        )


class Owl:
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        if len(raw_optlacc) <= 265:
            logger.warning("Owl data not present.")
        self.discovered: bool = safer_index(raw_optlacc, 265, False)
        self.feather_generation: int = safer_index(raw_optlacc, 254, 0)
        self.bonuses_of_orion_owned: int = safer_index(raw_optlacc, 255, 0)
        self.feather_restarts: int = safer_index(raw_optlacc, 258, 0)
        self.mega_feathers_owned: int = safer_index(raw_optlacc, 262, 0)
        self.bonuses: dict[str, OwlBonus] = {
            bonus_name: OwlBonus(bonus_name, bonus['BaseValue'])
            for bonus_name, bonus in owl_bonuses_of_orion.items()
        }

    def calculate(self, legend_talent_value: float):
        # Dependency: _calculate_w7_legend_talents must run first to populate legend_talent_value's source
        legend_talent_multi = ValueToMulti(legend_talent_value)
        bonuses_of_orion_num = len(self.bonuses)
        megafeather_mod = 0
        if self.mega_feathers_owned >= 10:
            megafeather_mod = 6 + ((self.mega_feathers_owned - 10) * 0.5)
        elif self.mega_feathers_owned > 7:
            megafeather_mod = 5
        elif self.mega_feathers_owned > 5:
            megafeather_mod = 4
        elif self.mega_feathers_owned > 3:
            megafeather_mod = 3
        elif self.mega_feathers_owned > 1:
            megafeather_mod = 2

        for bonus_index, bonus in enumerate(self.bonuses.values()):
            if self.discovered:
                num_unlocked = (
                    floor(self.bonuses_of_orion_owned / bonuses_of_orion_num)
                    + (1 if (self.bonuses_of_orion_owned % bonuses_of_orion_num) > bonus_index else 0)
                )
            else:
                num_unlocked = 0
            bonus.calculate(num_unlocked, megafeather_mod, legend_talent_multi)
