from typing import Literal, overload

from models.caverns.caves.cavern import Cavern
from models.caverns.caves.skilling_cavern import SkillingCavern
from models.caverns.caves.the_well import TheWell


class Caves(dict[str, Cavern]):
    _CAVE_TYPES = {
        "the_well": TheWell,
        "motherlode": lambda: SkillingCavern(
            name="Motherlode", cavern_number=2, offset=0,
            resource_type="Ore", resource_skill="Mining",
        ),
        "the_hive": lambda: SkillingCavern(
            name="The Hive", cavern_number=8, offset=2,
            resource_type="Bugs", resource_skill="Catching",
        ),
        "evertree": lambda: SkillingCavern(
            name="Evertree", cavern_number=12, offset=4,
            resource_type="Logs", resource_skill="Chopping",
        ),
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
    def __getitem__(
        self, key: Literal["Motherlode", "The Hive", "Evertree"]
    ) -> SkillingCavern: ...
    @overload
    def __getitem__(self, key: str) -> Cavern: ...
    def __getitem__(self, key: str) -> Cavern:
        return super().__getitem__(key)
