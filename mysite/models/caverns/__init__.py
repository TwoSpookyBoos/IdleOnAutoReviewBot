from models.caverns.caves import Caves
from models.caverns.villagers import Villagers
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get

logger = get_logger(__name__)


class Caverns:
    def __init__(self, raw_data: dict):
        raw_caverns_list: list[list] = safe_loads(raw_data.get("Holes", []))
        if not raw_caverns_list:
            logger.warning("Caverns data not present.")
        while len(raw_caverns_list) < 30:
            raw_caverns_list.append([0] * 100)
        game_version = safer_get(raw_data, 'DoOnceREAL', 0.00)
        self.villagers: Villagers = Villagers(raw_caverns_list, game_version)
        self.caves: Caves = Caves(raw_caverns_list)
