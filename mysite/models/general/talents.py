from consts.idleon.lava_func import lava_func
from models.advice.advice import Advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.number_formatting import round_and_trim

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

    def get_bonus_advice(
        self,
        label_prefix: str,
        max_level: float,
        bonus_text: str,
        level: float | None = None,
        note: str = "",
    ) -> Advice:
        """Without `level`, shows only the value at `max_level`, with no progress."""
        max_value = self.value_at_level(max_level)
        value = None if level is None else self.value_at_level(level)
        if value is None:
            value_text = f"{round_and_trim(max_value)}{bonus_text} if maxed"
        else:
            value_text = (
                f"{round_and_trim(value)}/{round_and_trim(max_value)}{bonus_text}"
            )
        note_text = f"<br>{note}" if note else ""
        return Advice(
            label=f"{label_prefix} - {self.name}: +{value_text}{note_text}",
            picture_class=self.name,
            progression="" if level is None else level,
            goal="" if level is None else max_level,
            completed=None if value is None else value >= max_value,
        )


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
