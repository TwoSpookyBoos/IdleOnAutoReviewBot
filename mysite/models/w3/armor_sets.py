from functools import cached_property

from consts.consts_autoreview import ValueToMulti
from consts.consts_w3 import equipment_sets_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_get
from utils.text_formatting import getItemDisplayName


class ArmorSet:
    def __init__(self, set_name: str, requirements: list, owned: bool):
        self.name: str = set_name.replace("_", " ")
        self.title: str = self.name.title()
        self.owned: bool = owned
        self.image: str = getItemDisplayName(requirements[0][0])
        self.armor: list[str] = requirements[0]
        self.tools: list[str] = requirements[1]
        self.required_tools: int = safer_convert(requirements[3][0], 0)
        self.weapons: list[str] = requirements[2]
        self.required_weapons: int = safer_convert(requirements[3][1], 0)
        self.base_value: float = safer_convert(requirements[3][2], 0)
        self._bonus_template: str = (
            requirements[3][3].replace("|", " ").replace("_", " ")
        )

    @cached_property
    def total_value(self) -> float:
        # `}` is a multi, `{` a flat value
        if "}" in self._bonus_template:
            return ValueToMulti(self.owned * self.base_value)
        return float(self.owned * self.base_value)

    @cached_property
    def description(self) -> str:
        if "}" in self._bonus_template:
            return self._bonus_template.replace("}", f"{self.total_value:.2f}")
        return self._bonus_template.replace("{", f"{self.total_value}")

    def get_bonus_advice(
        self, link_to_section: bool = True, additional_text: str = ""
    ) -> Advice:
        link_text = "{{ Armor Set|#armor-sets }} - " if link_to_section else ""
        return Advice(
            label=f"{link_text}{self.title}: {self.description}{additional_text}",
            picture_class=self.image,
            progression=int(self.owned),
            goal=1,
        )

    def get_tier_advice(self) -> Advice:
        return Advice(
            label=f"Complete the {self.title}: {self.description}",
            picture_class=self.image,
            progression=int(self.owned),
            goal=1,
        )


class ArmorSets(dict[str, ArmorSet]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        self.smithy_unlocked: bool = safer_convert(
            safer_get(raw_optlacc, 380, False), False
        )
        self.smithy_days_remaining: int = 30 - max(
            0, safer_convert(safer_get(raw_optlacc, 381, 0), 0)
        )
        raw_owned = safer_get(raw_optlacc, 379, "")
        owned_sets = raw_owned.split(",") if isinstance(raw_owned, str) else []
        for set_name, requirements in equipment_sets_dict.items():
            armor_set = ArmorSet(set_name, requirements, set_name in owned_sets)
            self[armor_set.name] = armor_set
