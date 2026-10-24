from consts.consts_general import achievements_list
from consts.general.achievements import achievement_tier_info
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class Achievement:
    def __init__(self, index: int, name: str, raw: int):
        self.index: int = index
        self.name: str = name
        self.raw: int = raw
        self.complete: bool = raw == -1
        tier_info = achievement_tier_info.get(name, {})
        self.world: int | None = tier_info.get("World")
        self.reward: str = tier_info.get("Reward", "")

    def get_tier_advice(
        self, progression: int | str, goal: int | str, resource: str = ""
    ) -> Advice:
        return Advice(
            label=f"W{self.world} {self.name}: {self.reward}",
            picture_class=self.name,
            progression=progression,
            goal=goal,
            resource=resource,
            completed=False,
        )


class Achievements(dict[str, Achievement]):
    def __init__(self, raw_data: dict):
        super().__init__()
        raw_achievements = safe_loads(raw_data.get("AchieveReg", []))
        if len(raw_achievements) < len(achievements_list):
            logger.warning(
                f"Achievements list shorter than expected by "
                f"{len(achievements_list) - len(raw_achievements)}. "
                f"Likely old data. Defaulting them all to Incomplete."
            )
        for index, info in enumerate(achievements_list):
            name = info[0].replace("_", " ")
            if name != "FILLERZZZ ACH":
                self[name] = Achievement(
                    index, name, safer_index(raw_achievements, index, 0)
                )
