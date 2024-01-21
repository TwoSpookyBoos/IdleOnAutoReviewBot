from typing import Any


class Advice:
    def __init__(self, label: str, item_name: str, progression: Any, goal: Any = "", unit: str = ""):
        self.label: str = label
        self.item_name: str = item_name
        self.progression: str = str(progression)
        self.goal: str = str(goal)
        self.unit: str = unit

    @property
    def css_class(self) -> str:
        return self.item_name.replace(' ', '-').lower()
