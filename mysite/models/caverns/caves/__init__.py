from typing import Literal, overload

from models.caverns.caves.cavern import Cavern
from models.caverns.caves.the_well import TheWell


class Caves(dict[str, Cavern]):
    _CAVE_TYPES = {
        "the_well": TheWell,
    }

    def __init__(self, raw_caverns_list: list):
        super().__init__()
        for cls in self._CAVE_TYPES.values():
            cave = cls()
            cave.parse_opals_found(raw_caverns_list)
            cave.parse(raw_caverns_list)
            self[cave.name] = cave

    @overload
    def __getitem__(self, key: Literal["The Well"]) -> TheWell: ...
    @overload
    def __getitem__(self, key: str) -> Cavern: ...
    def __getitem__(self, key: str) -> Cavern:
        return super().__getitem__(key)
