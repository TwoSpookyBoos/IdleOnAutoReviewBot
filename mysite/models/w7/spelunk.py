from consts.idleon.w7.spelunk import spelunking_cave_list

from models.advice.advice import Advice

from utils.safer_data_handling import safe_loads, safer_index
from utils.logging import get_logger

logger = get_logger(__name__)


class SpelunkCave:
    def __init__(self, index: int, info: dict, state: int):
        self.name = info["Name"]
        self._description = info["Description"]
        self.bonus_obtained = bool(state)
        self._image = f"spelunking-boss-{index}"
        self._resource = f"spelunking-cavern-{index}"

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{ Spelunking|#spelunking }} - "
        label += f"{self.name}:<br>{self._description}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=int(self.bonus_obtained),
            goal=1,
            resource=self._resource,
        )

    def get_unlock_advice(self) -> Advice:
        return Advice(
            label="{{Spelunking|#spelunking}}:<br>"
            f"Defeat the Boss of the {self.name} Cave",
            picture_class=self._image,
            progression=int(self.bonus_obtained),
            goal=1,
        )


class Spelunk:
    def __init__(self, raw_data: dict):
        spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        raw_cave_state: list[int] = safer_index(spelunk_info, 0, [])
        if not raw_cave_state:
            logger.warning("Spelunk Cave data not present.")
        self.cave: dict[str, SpelunkCave] = {}
        for index, cave_info in enumerate(spelunking_cave_list):
            cave_state = safer_index(raw_cave_state, index, 0)
            cave = SpelunkCave(index, cave_info, cave_state)
            self.cave[cave.name] = cave
