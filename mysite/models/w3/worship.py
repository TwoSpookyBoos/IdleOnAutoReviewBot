from functools import cached_property

from consts.consts_w3 import totems_list, totems_max_wave
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Totem:
    def __init__(self, index: int, name: str, waves: int):
        self.index: int = index
        self.name: str = name
        self.waves: int = waves


class Worship(dict[int, Totem]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_totem_data = safe_loads(raw_data.get('TotemInfo', []))
        if not raw_totem_data:
            return  # Worship not yet unlocked
        raw_waves = raw_totem_data[0]
        for totem_index, totem_name in enumerate(totems_list):
            self[totem_index] = Totem(
                totem_index, totem_name, safer_convert(safer_index(raw_waves, totem_index, 0), 0)
            )

    @cached_property
    def total_waves(self) -> int:
        return sum(totem.waves for totem in self.values())

    @cached_property
    def max_total_waves(self) -> int:
        return len(self) * totems_max_wave
