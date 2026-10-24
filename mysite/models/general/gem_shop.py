from consts.caverns.villager.roles import villager_roles
from consts.consts_general import (
    gem_shop_bundles_dict,
    gem_shop_dict,
    gem_shop_optlacc_dict,
)
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_get, safer_index

logger = get_logger(__name__)


class GemShopPurchase:
    def __init__(self, name: str, info: dict, owned: int):
        self.name: str = name
        self.owned: int = owned
        self.max_level: int | str = info["MaxLevel"]
        self.item_codename: str = info.get("ItemCodename", "")
        self.description: str = info.get("Description", "")
        self.section: str = info["Section"]
        self.subsection: str = info["Subsection"]

    def get_advice(
        self,
        link_to_section: bool = True,
        override_goal: int | None = None,
        additional_text: str = "",
    ) -> Advice:
        link_text = "{{ Gem Shop|#gem-shop }} - " if link_to_section else ""
        goal = (
            override_goal
            if override_goal is not None
            else int(self.max_level)
            if isinstance(self.max_level, float)
            else self.max_level
        )
        advice = Advice(
            label=f"{link_text}{self.name} ({self.subsection}){additional_text}",
            picture_class=self.name,
            progression=self.owned,
            goal=goal,
        )
        advice.resource = "gem" if advice.percent < 100 else ""
        return advice


class GemShopBundle:
    def __init__(self, code_name: str, display: str, owned: bool):
        self.code_name: str = code_name
        self.display: str = display
        self.owned: bool = owned


class GemShop:
    def __init__(self, raw_data: dict):
        raw_purchased = safe_loads(raw_data.get("GemItemsPurchased", []))
        self.purchases: dict[str, GemShopPurchase] = {
            name: GemShopPurchase(
                name,
                info,
                safer_convert(safer_index(raw_purchased, info["Index"], 0), 0),
            )
            for name, info in gem_shop_dict.items()
        }

        raw_holes = safe_loads(raw_data.get("Holes", []))
        raw_parallel = safer_index(raw_holes, 23, [])
        for index, role in enumerate(villager_roles.values()):
            name = f"Parallel Villagers {role}"
            self.purchases[name] = GemShopPurchase(
                name,
                {
                    "MaxLevel": 1,
                    "ItemCodename": "GemP40",
                    "Section": "Oddities",
                    "Subsection": "Caverns",
                },
                safer_index(raw_parallel, index, 0),
            )

        # FOMO purchases are tracked in OptLacc instead
        raw_optlacc = dict(enumerate(safe_loads(raw_data.get("OptLacc", []))))
        for name, info in gem_shop_optlacc_dict.items():
            owned = safer_get(raw_optlacc, info["Index"], 0)
            self.purchases[name] = GemShopPurchase(name, info, owned)

        raw_bundles = safe_loads(raw_data.get("BundlesReceived", []))
        self.bundle_data_present: bool = "BundlesReceived" in raw_data
        self.bundles: dict[str, GemShopBundle] = {
            code_name: GemShopBundle(code_name, display, code_name in raw_bundles)
            for code_name, display in gem_shop_bundles_dict.items()
        }
        unknown_bundles = [
            code_name for code_name in raw_bundles if code_name not in self.bundles
        ]
        if unknown_bundles:
            logger.warning(f"Unknown Gem Shop Bundles found: {unknown_bundles}")

    @property
    def minigame_plays_daily(self) -> int:
        return 5 + 4 * self.purchases["Daily Minigame Plays"].owned
