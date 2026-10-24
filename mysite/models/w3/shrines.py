from consts.consts_autoreview import ValueToMulti
from consts.consts_w3 import (
    arbitrary_shrine_goal,
    arbitrary_shrine_note,
    buildings_dict,
    buildings_shrines,
)
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads


class Shrine:
    def __init__(self, name: str, info: dict, raw_shrine: list):
        self.name: str = name
        self.image: str = info["Image"]
        try:
            self.map_index: int = int(raw_shrine[0])
            self.level: int = int(raw_shrine[3])
            self.hours: float = float(raw_shrine[4])
        except (IndexError, TypeError, ValueError):
            self.map_index = 0
            self.level = 0
            self.hours = 0.0
        self.base_value: float = (
            info["ValueBase"] + (info["ValueIncrement"] * (self.level - 1))
            if self.level > 0
            else 0
        )
        self.value: float = self.base_value

    def get_advice(self) -> Advice:
        return Advice(
            label=f"Level {self.level} {self.name}: +{self.value:.0f}%"
            f"<br>{arbitrary_shrine_note}",
            picture_class=self.image,
            progression=self.level,
            goal=arbitrary_shrine_goal,
        )


class Shrines(dict[str, Shrine]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_shrines = safe_loads(raw_data.get("Shrine", []))
        for index, name in enumerate(buildings_shrines):
            raw_shrine = raw_shrines[index] if index < len(raw_shrines) else []
            self[name] = Shrine(name, buildings_dict[18 + index], raw_shrine)
        self._chizoar_stars: int = 0

    def calculate_values(self, chizoar_stars: int):
        self._chizoar_stars = chizoar_stars
        chizoar_multi = ValueToMulti(5 * (1 + chizoar_stars))
        for shrine in self.values():
            shrine.value *= chizoar_multi

    def get_chizoar_card_advice(self) -> Advice:
        chizoar_multi = 1 + (5 * (1 + self._chizoar_stars) / 100)
        return Advice(
            label=f"Chaotic Chizoar card to increase Shrine "
            f"({chizoar_multi}x multi already included)",
            picture_class="chaotic-chizoar-card",
            progression=1 + self._chizoar_stars,
            goal=6,
        )
