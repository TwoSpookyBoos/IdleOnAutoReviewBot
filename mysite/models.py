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
    def __init__(self, formatting: str, default_collapsed: bool, tier: str, pre_string: str, advice_list: list[Advice], post_string: str):
        self.formatting: str = formatting  # example usage: strong, em
        self.default_collapsed: bool = default_collapsed  # true, false
        self.tier: str = tier  # "17", "S"
        self.pre_string: str = pre_string  # "Tier 17- Do these things
        self.advice_list: list[Advice] = advice_list  # Each Advice on its own row within the same Group
        self.post_string: str = post_string  # Trailing advice
