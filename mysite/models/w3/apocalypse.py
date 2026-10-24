from consts.consts_w3 import apoc_names_list
from consts.idleon.consts_idleon import current_world
from models.advice.advice import Advice
from utils.text_formatting import notateNumber


class UnmetApocMap:
    def __init__(
        self,
        map_name: str,
        kills_short: int,
        percent: int,
        monster_image: str,
        world: int,
        monster_name: str,
    ):
        self.map_name: str = map_name
        self.kills_short: int = kills_short
        self.percent: int = percent
        self.monster_image: str = monster_image
        self.world: int = world
        self.monster_name: str = monster_name

    def get_advice(self) -> Advice:
        return Advice(
            label=f"{self.monster_name} in {self.map_name} "
            f"({notateNumber('Basic', self.kills_short, 0)} remaining)",
            picture_class=self.monster_image,
            progression=self.percent,
            goal=100,
            unit="%",
        )


class ApocProgress:
    def __init__(self):
        self.total: int = 0
        self.unmet: dict[str, list[UnmetApocMap]] = {
            **{f"Basic W{i} Enemies": [] for i in range(1, current_world + 1)},
            "Easy Extras": [],
            "Medium Extras": [],
            "Difficult Extras": [],
            "Insane": [],
            "Impossible": [],
        }

    def sort_by_progression(self):
        # Most kills remaining first
        for difficulty, maps in self.unmet.items():
            self.unmet[difficulty] = sorted(
                maps, key=lambda unmet: unmet.kills_short, reverse=True
            )


def new_apocalypses() -> dict[str, ApocProgress]:
    return {name: ApocProgress() for name in apoc_names_list}
