from models.w2.alchemy_bubbles import parse_raw_cauldrons
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index


logger = get_logger(__name__)

# CauldUpgLVs indexes, 4 boost levels per cauldron then 2 decant levels per liquid
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

        self.bubbles_per_world: list[int] = []
        self.next_world_missing_bubbles: int = 0

    @property
    def water_droplets(self) -> list[int]:
        return self.decants['WaterDroplets']

    def calculate_bubble_unlocks(self):
        per_world = [20, 0, 0, 0, 0, 0, 0, 0, 0]
        for unlocked in self.bubbles_unlocked:
            world = 1
            while unlocked >= 5 and world <= len(per_world) - 1:
                per_world[world] += 5
                unlocked -= 5
                world += 1
            if unlocked > 0 and world <= len(per_world) - 1:
                per_world[world] += unlocked
        self.bubbles_per_world = per_world
        self.next_world_missing_bubbles = min(
            [unlocked // 5 for unlocked in self.bubbles_unlocked], default=0
        ) + 1
