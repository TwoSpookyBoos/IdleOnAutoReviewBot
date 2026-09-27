from consts.consts_w3 import buildings_dict
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Building:
    def __init__(self, index: int, info: dict, level: int):
        self.index: int = index
        self.name: str = info["Name"]
        self.level: int = level
        self.max_level: int = info["BaseMaxLevel"]
        self.image: str = info["Image"]
        self.type: str = info["Type"]

    def get_tier_advice(self, goal: int, unlock_only: bool = False) -> Advice:
        return Advice(
            label=self.name,
            picture_class=self.image,
            progression=0 if unlock_only else self.level,
            goal=1 if unlock_only else goal,
        )


class Buildings(dict[str, Building]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_buildings = safe_loads(raw_data.get("Tower", []))
        for index, info in buildings_dict.items():
            level = safer_convert(safer_index(raw_buildings, index, 0), 0)
            self[info["Name"]] = Building(index, info, level)

    def increase_max_level(self, building_type: str, levels: int):
        for building in self.values():
            if building.type == building_type:
                building.max_level += levels

    def calculate_max_levels(
        self,
        skill_mastery_unlocked: bool,
        total_construction_level: int,
        wizard_maximizer_level: int,
    ):
        # Rift Skill Mastery milestones
        if skill_mastery_unlocked:
            if total_construction_level >= 500:
                self["Trapper Drone"].max_level += 35
            if total_construction_level >= 1000:
                self["Talent Book Library"].max_level += 35
            if total_construction_level >= 1500:
                self.increase_max_level("Shrine", 30)
            if total_construction_level >= 2500:
                self.increase_max_level("Tower", 30)
        # Atom Collider Carbon
        self.increase_max_level("Tower", 2 * wizard_maximizer_level)

    def calculate_gambit_levels(self, tower_bonus_unlocked: bool):
        # Gambit bonus 9: +100 Tower levels
        if tower_bonus_unlocked:
            self.increase_max_level("Tower", 100)
