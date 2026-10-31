import math

from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.dancing_coral import dancing_coral_bonus_data
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_convert, safer_index

logger = get_logger(__name__)

class DancingCoralBonus:
    def __init__(
        self, info: dict, index: int, unlocked_bonuses: int, cost_reduction_level: int
    ):
        self.index = index
        self.unlocked = index < unlocked_bonuses
        # Bonuses are bought one at a time, in order
        self.next_to_buy = index == unlocked_bonuses
        self.base_cost = info["Base Cost"]
        # "DancingCoralCOST" in source
        cost_reduction = (10 * cost_reduction_level + 1.05**cost_reduction_level) / 100
        self.cost = math.ceil(self.base_cost / (1 + cost_reduction))
        self.cost_name = info["Cost Name"]
        self.cost_source = info["Cost Source"]
        self.description_template = info["Description Template"]
        self.base_value = info["Base Value"]
        self.target_shrine_name = info["Target Shrine Name"]
        self.value = 0
        self.target_shrine_level = 0
        self.image = f"dancing-coral-bonus-{self.index}"

    def calculate_bonus(self, construction_buildings):
        self.target_shrine_level = construction_buildings[self.target_shrine_name].level
        levels_above_threshold = max(self.target_shrine_level - 200, 0)
        self.value = levels_above_threshold * self.base_value
        if "}" in self.description_template:
            self.value = ValueToMulti(self.value)


    def get_advice(self):
        if self.next_to_buy:
            return self.get_unlock_advice()

        description = self._description()
        if not self.unlocked:
            description += "<br>Unlock the previous bonus first"

        return Advice(
            label=f"{description}",
            picture_class=self.image,
            progression=0 if not self.unlocked else self.target_shrine_level,
            goal=1 if not self.unlocked else ""
        )

    def get_unlock_advice(self) -> Advice:
        advice = Advice(
            label=(
                f"{self._description()}<br>Unlock for {self.cost:,} {self.cost_name}"
                f" {self.cost_source}"
            ),
            picture_class=self.image,
            progression=f"{self.owned_cost_items:,}",
            goal=f"{self.cost:,}",
            resource=self.cost_name,
        )
        # Having enough coral doesn't unlock the bonus by itself
        advice.completed = False
        return advice

    def _description(self) -> str:
        description = self.description_template
        total_bonus = ""
        if "{" in description:
            description = description.replace("{", str(self.base_value))
            total_bonus = self.description_template.replace("{", str(self.value))
        elif "}" in description:
            description = description.replace("}", str(ValueToMulti(self.base_value)))
            total_bonus = self.description_template.replace("}", str(self.value))

        description += f" per {self.target_shrine_name} level above 200"
        if self.unlocked:
            description += f"<br>Total Bonus: {total_bonus}"
        return description

    @property
    def owned_cost_items(self) -> int:
        from models.general.session_data import session_data

        match self.index:
            case 0:
                return session_data.account.coral_reef.town_corals
            case _:
                stored_assets = session_data.account.stored_assets
                return stored_assets.get(f"Coral{self.index}").amount


class DancingCoral(dict[int, DancingCoralBonus]):
    def __init__(self, raw_data: dict):
        raw_spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        if not raw_spelunk_info:
            logger.warning("Dancing Coral data not present.")
        raw_dancing_coral = safer_index(raw_spelunk_info, 4, [])
        unlocked_bonuses = safer_convert(safer_index(raw_dancing_coral, 6, 0), 0)
        cost_reduction_level = safer_convert(safer_index(raw_dancing_coral, 7, 0), 0)
        for index, info in enumerate(dancing_coral_bonus_data):
            self[index] = DancingCoralBonus(
                info, index, unlocked_bonuses, cost_reduction_level
            )

    def calculate_bonuses(self, construction_buildings):
        for bonus in self.values():
            bonus.calculate_bonus(construction_buildings)