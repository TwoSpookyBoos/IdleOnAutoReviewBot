from collections import Counter

from consts.consts_w2 import get_obol_totals, ignorable_obols_list, obols_dict
from utils.safer_data_handling import safe_loads

# Family slots, then each character's personal slots
equipped_obol_keys = [
    "ObolEqO1",
    "ObolEqO2",
    *[f"ObolEqO0_{index}" for index in range(10)],
]


class Obols:
    def __init__(self, raw_data: dict):
        raw_owned = []
        for key in equipped_obol_keys:
            raw_owned += safe_loads(raw_data.get(key, []))
        for inventory_page in safe_loads(raw_data.get("ObolInvOr", [])):
            raw_owned += inventory_page.values()
        # Owned count per obol codename
        self.owned: Counter[str] = Counter(
            obol for obol in raw_owned if obol not in ignorable_obols_list
        )
        self.family_bonus_totals: dict = get_obol_totals(
            safe_loads(raw_data.get("ObolEqO1", [])),
            safe_loads(raw_data.get("ObolEqMAPz1", {})),
        )

    def count(self, bonus: str, shape: str) -> int:
        return sum(
            amount
            for obol, amount in self.owned.items()
            if obols_dict.get(obol, {}).get("Bonus") == bonus
            and obols_dict.get(obol, {}).get("Shape") == shape
        )
