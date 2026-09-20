from functools import cached_property

from consts.general.dungeons import (
    dungeon_credit_shop_names,
    dungeon_flurbo_shop_names,
    dungeon_rank_credit_requirements,
    max_credit_shop_level,
    max_flurbo_shop_level,
)
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


class DungeonShop(dict[str, int]):
    """Purchased levels of one Dungeon shop's upgrades, keyed by upgrade name."""

    def __init__(self, names: list[str], raw_levels: list, max_level: int):
        super().__init__()
        self.max_level: int = max_level
        for index, name in enumerate(names):
            self[name] = safer_convert(safer_index(raw_levels, index, 0), 0)

    @cached_property
    def maxed(self) -> bool:
        return bool(self) and all(level >= self.max_level for level in self.values())


class Dungeons:
    def __init__(self, raw_data: dict):
        raw_dungeon_upgrades = safe_loads(raw_data.get('DungUpg', []))
        raw_optlacc = safe_loads(raw_data.get('OptLacc', []))
        raw_max_purchases = safer_index(raw_dungeon_upgrades, 3, [])

        self.max_weapon: int = safer_convert(safer_index(raw_max_purchases, 0, 0), 0)
        self.max_armor: list[int] = [safer_convert(safer_index(raw_max_purchases, index, 0), 0) for index in range(4, 8)]
        self.max_jewelry: list[int] = [safer_convert(safer_index(raw_max_purchases, index, 0), 0) for index in range(8, 10)]
        self.credit_shop: DungeonShop = DungeonShop(
            dungeon_credit_shop_names, safer_index(raw_dungeon_upgrades, 1, []), max_credit_shop_level
        )
        self.flurbo_shop: DungeonShop = DungeonShop(
            dungeon_flurbo_shop_names, safer_index(raw_dungeon_upgrades, 5, []), max_flurbo_shop_level
        )
        self.lifetime_credits: int = safer_convert(safer_index(raw_optlacc, 71, 0), 0)

    @cached_property
    def rank(self) -> int:
        return sum(1 for requirement in dungeon_rank_credit_requirements if self.lifetime_credits >= requirement)
