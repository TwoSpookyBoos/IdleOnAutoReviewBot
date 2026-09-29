from collections import defaultdict

from consts.consts_item_data import ITEM_DATA
from consts.idleon.w7.research import minehead_hatrack_bonus_index
from models.advice.advice import Advice
from models.general.item_definitions import ItemDefinition
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index


class HatRack:
    def __init__(self, raw_data: dict):
        spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        raw_hatrack: list[str] = safer_index(spelunk_info, 46, []) or []
        self.count = len(raw_hatrack)
        self.codes: set[str] = set(raw_hatrack)
        self.hats: list[ItemDefinition] = [
            ITEM_DATA[hat] for hat in raw_hatrack if hat in ITEM_DATA
        ]
        self.multi = 1.0
        self.bonuses: dict[str, tuple[str, float]] = {}

    def calculate_bonuses(self, companions, event_shop, minehead, sushi_station):
        # "HatrackBonusMulti" in source. Last updated in v2.531.0
        self.multi = 1 + (
            self.count
            + companions["Wild Boar"].bonus
            + 10 * event_shop["King of the Rack"].owned
            + minehead[minehead_hatrack_bonus_index].value
            + sushi_station.get_milestone_bonus_value("Hat Rack Multi")
        ) / 100
        # "InitializePremHatBonuses" in source. Last updated in v2.531.0
        total = defaultdict(float)
        for hat in self.hats:
            hat.bonus.add_to(total, self.multi)
        for key, value in total.items():
            if key == "0" or not key.startswith("%"):
                continue
            self.bonuses[key.split(" ", 1)[1]] = (key, value)

    def get_bonus_value(self, name: str) -> float:
        return self.bonuses.get(name, ("", 0))[1]

    def get_bonus_advice(self, name: str) -> Advice:
        value = self.get_bonus_value(name)
        return Advice(
            label=f"Hat Rack - {name}: +{round_and_trim(value)}%"
            f"<br>{self.count} hats, "
            f"{round_and_trim(self.multi)}x multi",
            picture_class=self.hats[-1].name if self.hats else "hatrack-stand",
        )
