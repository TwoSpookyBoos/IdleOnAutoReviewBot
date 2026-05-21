from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.dancing_coral import dancing_coral_bonus_data
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)

class DancingCoralBonus:
    def __init__(self, info: dict, unlocked: bool, index: int):
        self.index = index
        self.unlocked = unlocked
        self.base_cost = info["Base Cost"]
        self.description_template = info["Description Template"]
        self.base_value = info["Base Value"]
        self.target_shrine_name = info["Target Shrine Name"]
        self.value = 0
        self.image = f"dancing-coral-bonus-{self.index}"

    def calculate_bonus(self):
        from models.general.session_data import session_data
        target_shrine_level = session_data.account.construction_buildings[self.target_shrine_name]["Level"]
        levels_above_threshold = max(target_shrine_level - 200, 0)
        self.value = levels_above_threshold * self.base_value
        if "}" in self.description_template:
            self.value = ValueToMulti(self.value)


    def get_advice(self):
        from models.general.session_data import session_data
        target_shrine_level = session_data.account.construction_buildings[self.target_shrine_name]["Level"]
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

        return Advice(
            label=f"{description}",
            picture_class=self.image,
            progression=0 if not self.unlocked else target_shrine_level,
            goal=1 if not self.unlocked else ""
        )
    

class DancingCoral(dict[int, DancingCoralBonus]):
    def __init__(self, raw_data: dict):
        raw_spelunk_info = safe_loads(raw_data.get("Spelunk", []))
        if not raw_spelunk_info:
            logger.warning("Dancing Coral data not present.")
        unlocked_bonuses = safer_index(safer_index(raw_spelunk_info, 4, []), 6, 0)
        for index, info in enumerate(dancing_coral_bonus_data):
            upgrade = DancingCoralBonus(info, (index + 1) <= unlocked_bonuses, index)
            self[index] = upgrade

    def calculate_bonuses(self):
        for bonus in self.values():
            bonus.calculate_bonus()