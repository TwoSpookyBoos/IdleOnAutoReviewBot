from typing import Literal, overload

from models.caverns.villagers.bolaia import Bolaia
from models.caverns.villagers.cosmos import Cosmos
from models.caverns.villagers.kaipu import Kaipu
from models.caverns.villagers.minau import Minau
from models.caverns.villagers.polonai import Polonai
from models.caverns.villagers.villager import Villager


class Villagers(dict[str, Villager]):
    _VILLAGER_TYPES = {
        "polonai": Polonai,
        "kaipu": Kaipu,
        "cosmos": Cosmos,
        "minau": Minau,
        "bolaia": Bolaia,
    }

    def __init__(self, raw_caverns_list: list, game_version: float):
        super().__init__()
        levels = raw_caverns_list[1]
        exps = raw_caverns_list[2]
        opals = raw_caverns_list[3]
        self.total_opal = 0
        for i, cls in enumerate(self._VILLAGER_TYPES.values()):
            villager = cls(index=i, level=levels[i], exp=exps[i], opals=opals[i])
            villager.parse_feature(raw_caverns_list)
            villager.calculate_exp_percent(game_version)
            self[villager.name] = villager
            self.total_opal += villager.opals

    @overload
    def __getitem__(self, key: Literal["Polonai"]) -> Polonai: ...
    @overload
    def __getitem__(self, key: Literal["Kaipu"]) -> Kaipu: ...
    @overload
    def __getitem__(self, key: Literal["Cosmos"]) -> Cosmos: ...
    @overload
    def __getitem__(self, key: Literal["Minau"]) -> Minau: ...
    @overload
    def __getitem__(self, key: Literal["Bolaia"]) -> Bolaia: ...
    @overload
    def __getitem__(self, key: str) -> Villager: ...
    def __getitem__(self, key: str) -> Villager:
        return super().__getitem__(key)
