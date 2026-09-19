from functools import cached_property

from models.w2.alchemy_bubbles import parse_raw_cauldrons
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


logger = get_logger(__name__)

# `CauldUpgLVs`: 32 levels, 8 groups of 4 - whole group per cauldron, last 2 per liquid.
_BOOST_INDEXES = {'Orange': (0, 1, 2, 3), 'Green': (4, 5, 6, 7), 'Purple': (8, 9, 10, 11), 'Yellow': (12, 13, 14, 15)}
_DECANT_INDEXES = {'WaterDroplets': (18, 19), 'LiquidNitrogen': (22, 23), 'TrenchSeawater': (26, 27), 'ToxicMercury': (30, 31)}


class AlchemyCauldrons:
    def __init__(self, raw_data: dict):
        cauldrons = parse_raw_cauldrons(raw_data)
        self.bubbles_unlocked: list[int] = [
            sum(1 for level in cauldron.values() if level > 0) for cauldron in cauldrons
        ]
        self.total_unlocked: int = sum(self.bubbles_unlocked)

        raw_upgrades = safe_loads(raw_data.get('CauldUpgLVs', []))
        self.boosts: dict[str, list[int]] = {
            colour: [safer_convert(safer_index(raw_upgrades, i, 0), 0) for i in indexes]
            for colour, indexes in _BOOST_INDEXES.items()
        }
        self.decants: dict[str, list[int]] = {
            liquid: [safer_convert(safer_index(raw_upgrades, i, 0), 0) for i in indexes]
            for liquid, indexes in _DECANT_INDEXES.items()
        }

    @property
    def water_droplets(self) -> list[int]:
        return self.decants['WaterDroplets']

    @cached_property
    def bubbles_per_world(self) -> list[int]:
        per_world = [20, 0, 0, 0, 0, 0, 0, 0, 0]
        for unlocked in self.bubbles_unlocked:
            world = 1
            while unlocked >= 5 and world <= len(per_world) - 1:
                per_world[world] += 5
                unlocked -= 5
                world += 1
            if unlocked > 0 and world <= len(per_world) - 1:
                per_world[world] += unlocked
        return per_world

    @cached_property
    def next_world_missing_bubbles(self) -> int:
        return min([unlocked // 5 for unlocked in self.bubbles_unlocked], default=0) + 1
