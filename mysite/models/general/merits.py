from consts.consts_general import allMeritsDict
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Merit:
    def __init__(self, info: dict, level: int):
        self.name: str = info["Name"]
        self.level: int = level
        self.max_level: int = info["MaxLevel"]


class Merits(dict[int, dict[int, Merit]]):
    def __init__(self, raw_data: dict):
        super().__init__()
        # Taskboard merit shop levels, per world
        raw_merits = safe_loads(raw_data.get("TaskZZ2", []))
        for world, merits in allMeritsDict.items():
            raw_world = safer_index(raw_merits, world, [])
            self[world] = {
                index: Merit(info, safer_convert(safer_index(raw_world, index, 0), 0))
                for index, info in merits.items()
            }
