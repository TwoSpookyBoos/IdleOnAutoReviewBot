from consts.consts_w2 import (
    islands_dict,
    islands_fractal_rewards_dict,
    islands_trash_shop,
)
from models.advice.advice import Advice
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class Island:
    def __init__(self, name: str, code: str, unlocked_codes: str):
        self.name: str = name
        self.unlocked: bool = code in unlocked_codes

    def get_unlock_advice(self) -> Advice:
        return Advice(
            label=f"Unlock {self.name}",
            picture_class=self.name,
            progression=int(self.unlocked),
            goal=1,
        )


class TrashShopItem:
    def __init__(self, name: str, info: dict, trash: int):
        self.name: str = name
        self.cost: int = info["Cost"]
        self.stamp_code: str | None = info.get("Stamp Code")
        self.unlocked: bool = False
        self._label: str = info.get("Label", name)
        self._image: str = info.get("Image", name)
        self._trash: int = trash

    def get_advice(self, step: int) -> Advice:
        return Advice(
            label=f"Step {step}: {self._label}",
            picture_class=self._image,
            progression=self._trash,
            goal=self.cost,
        )


class Islands(dict[str, Island]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        self.trash: int = safer_convert(safer_index(raw_optlacc, 161, 0), 0)
        self.bottles: int = safer_convert(safer_index(raw_optlacc, 162, 0), 0)
        self.garbage_purchases: int = safer_convert(safer_index(raw_optlacc, 163, 0), 0)
        self.bottle_purchases: int = safer_convert(safer_index(raw_optlacc, 164, 0), 0)
        self.nothing_hours: int = safer_convert(safer_index(raw_optlacc, 184, 0), 0)

        # e.g. "_dcabe", or int 0
        unlocked_codes = safer_convert(safer_index(raw_optlacc, 169, ""), "")
        for name, info in islands_dict.items():
            self[name] = Island(name, info["Code"], unlocked_codes)

        self.trash_shop: dict[str, TrashShopItem] = {
            name: TrashShopItem(name, info, self.trash)
            for name, info in islands_trash_shop.items()
        }

    def calculate_trash_shop(self, stamps, stored_assets, bribes):
        for item in self.trash_shop.values():
            if item.stamp_code:
                item.unlocked = (
                    stamps[item.name].delivered
                    or stored_assets.get(item.stamp_code).amount > 0
                )
        self.trash_shop["Unlock New Bribe Set"].unlocked = bribes[
            "Random Garbage"
        ].unlocked

    def get_garbage_generation_advice(self, step: int, goal: int) -> Advice:
        return Advice(
            label=f"Step {step}: Purchase {goal} total levels into Garbage Generation",
            picture_class="garbage",
            progression=self.garbage_purchases,
            goal=goal,
        )

    def get_fractal_rewards_advice(self) -> list[Advice]:
        return [
            Advice(
                label=details["Reward"],
                picture_class=details["Image"],
                progression=self.nothing_hours,
                goal=int(hours),
            )
            for hours, details in islands_fractal_rewards_dict.items()
        ]
