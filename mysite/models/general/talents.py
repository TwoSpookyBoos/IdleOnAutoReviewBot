from consts.idleon.lava_func import lava_func
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger

logger = get_logger(__name__)


class Talent:
    def __init__(self, index: int, info: dict):
        self.index: int = index
        self.name: str = info["name"]
        self._func_type: str = info["funcX"]
        self._x1: float = info["x1"]
        self._x2: float = info["x2"]

    def value_at_level(self, level: float) -> float:
        return lava_func(self._func_type, level, self._x1, self._x2)


class Talents(dict[str, Talent]):
    def __init__(self):
        super().__init__()
        for index, info in all_talentsDict.items():
            name = info["name"]
            if name in self:
                logger.error(
                    f"Duplicate talent name '{name}': {self[name].index} and {index}. "
                    f"Keeping {self[name].index}"
                )
                continue
            self[name] = Talent(index, info)


# Static game data, the same for every account
talents = Talents()
