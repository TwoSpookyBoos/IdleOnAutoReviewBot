from typing import Any


class Advice:
    def __init__(self, label: str, item_name: str, progression: Any, goal: Any = "", unit: str = "", extra: dict = {}):
        self.label: str = label
        self.item_name: str = item_name
        self.progression: str = str(progression)
        self.goal: str = str(goal)
        self.unit: str = unit
        self.extra: dict = extra

    @property
    def css_class(self) -> str:
        return self.item_name.replace(' ', '-').lower()

class AdviceGroup:
    def __init__(self, formatting: str, default_collapsed: bool, tier: str, pre_string: str, advice_list: list[Advice], post_string: str, group_extra: dict = {}):
        self.formatting: str = formatting  # example usage: strong, em
        self.default_collapsed: bool = default_collapsed  # true, false
        self.tier: str = tier  # "17", "S"
        self.pre_string: str = pre_string  # "Tier 17- Do these things
        self.advice_list: list[Advice] = advice_list  # Each Advice on its own row within the same Group
        self.post_string: str = post_string  # Trailing advice
        self.group_extra: dict = group_extra

class AdviceSection:
    def __init__(self, default_collapsed: bool, section_name: str, section_tier: str, section_header: str, advicegroup_list: list[AdviceGroup], section_pinchy_rating: str = "", section_extra: dict = {}):
        self.default_collapsed: bool = default_collapsed  # true, false
        self.section_name: str = section_name  # "Stamps", "Bribes"
        self.section_tier: str = section_tier  # Not always present. X/Y style, such as "17/36"
        self.section_header: str = section_header  # "Best Stamp tier met: 17/36. Recommended stamp actions", "Maestro Right Hands"
        self.advicegroup_list: list = advicegroup_list  # Each AdviceGroup separated into its own box + background color
        self.section_pinchy_rating: str = section_pinchy_rating
        self.section_extra: dict = section_extra

class AdviceWorld:
    def __init__(self, default_collapsed: bool, advicesections_list: list[AdviceSection], world_extra:dict = {}):
        self.default_collapsed: bool = default_collapsed  # true, false
        self.advicesections_list: list = advicesections_list
        self.world_extra: dict = world_extra
