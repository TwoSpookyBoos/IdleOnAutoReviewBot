from typing import Literal, overload

from models.caverns.caves.bravery_monument import BraveryMonument
from models.caverns.caves.cavern import Cavern
from models.caverns.caves.grotto import Grotto
from models.caverns.caves.justice_monument import JusticeMonument
from models.caverns.caves.skilling_cavern import SkillingCavern
from models.caverns.caves.the_bell import TheBell
from models.caverns.caves.the_den import TheDen
from models.caverns.caves.the_harp import TheHarp
from models.caverns.caves.the_lamp import TheLamp
from models.caverns.caves.the_well import TheWell
from models.caverns.caves.wisdom_monument import WisdomMonument


class Caves(dict[str, Cavern]):
    _CAVE_TYPES = {
        "the_well": TheWell,
        "the_den": TheDen,
        "the_bell": TheBell,
        "the_harp": TheHarp,
        "the_lamp": TheLamp,
        "grotto": Grotto,
        "motherlode": lambda: SkillingCavern(
            name="Motherlode",
            cavern_number=2,
            offset=0,
            resource_type="Ore",
            resource_skill="Mining",
        ),
        "the_hive": lambda: SkillingCavern(
            name="The Hive",
            cavern_number=8,
            offset=2,
            resource_type="Bugs",
            resource_skill="Catching",
        ),
        "evertree": lambda: SkillingCavern(
            name="Evertree",
            cavern_number=12,
            offset=4,
            resource_type="Logs",
            resource_skill="Chopping",
        ),
        "bravery_monument": BraveryMonument,
        "justice_monument": JusticeMonument,
        "wisdom_monument": WisdomMonument,
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
    def __getitem__(self, key: Literal["The Den"]) -> TheDen: ...
    @overload
    def __getitem__(self, key: Literal["The Bell"]) -> TheBell: ...
    @overload
    def __getitem__(self, key: Literal["The Harp"]) -> TheHarp: ...
    @overload
    def __getitem__(self, key: Literal["The Lamp"]) -> TheLamp: ...
    @overload
    def __getitem__(self, key: Literal["Grotto"]) -> Grotto: ...
    @overload
    def __getitem__(
        self, key: Literal["Motherlode", "The Hive", "Evertree"]
    ) -> SkillingCavern: ...
    @overload
    def __getitem__(self, key: Literal["Bravery Monument"]) -> BraveryMonument: ...
    @overload
    def __getitem__(self, key: Literal["Justice Monument"]) -> JusticeMonument: ...
    @overload
    def __getitem__(self, key: Literal["Wisdom Monument"]) -> WisdomMonument: ...
    @overload
    def __getitem__(self, key: str) -> Cavern: ...
    def __getitem__(self, key: str) -> Cavern:
        return super().__getitem__(key)
