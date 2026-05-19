from consts.consts_autoreview import ValueToMulti
from consts.idleon.w7.research import research_grid_upgrade_data, research_grid_row_size
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)

class ResearchGridUpgrade:
    def __init__(self, info: dict, level: int):
        self.grid_index = info["Grid Index"]
        self.level = level
        self.name = info["Name"]
        self.description_template = info["Description Template"]
        self.max_level = info["Max Level"]
        self.base_value_per_level = info["Base Value Per Level"]
        self.value = 0
        self.max_value = self.base_value_per_level * self.max_level
        self._image = f"research-grid-{self.grid_index}"

    def calculate_bonus(self):
        # TODO: any mults that increase research bonuses
        self.value = self.level * self.base_value_per_level

    def get_bonus_advice(self, link_to_section: bool = True) -> Advice:
        label = ""
        if link_to_section:
            label += "{{Research|#research}} - "
        if "{" in self.description_template:
            value = self.value
            max_value = self.max_value
        else:
            value = ValueToMulti(self.value)
            max_value = ValueToMulti(self.max_value)

        # TODO: handle "^x" in description. The values are mostly based on other mechanics
        # TODO: handle "$" in description. The values are mostly based on other mechanics

        bonus = f"{round_and_trim(value)}/{round_and_trim(max_value)}"
        bonus_description = self.description_template.replace("{", bonus).replace("}", bonus).replace("|",  str(self.level))
        if self.name == "Divine Design":
            from utils.misc.has_companion import has_companion
            divine_design_description = "You_are_now_permanently_linked_to_Arctis_on_all_characters".replace("_", " ")
            if has_companion("King Doot"):
                divine_design_description = "Arctis_nods_in_approval..._all_Research_Grid_bonuses_are_1.05x_higher".replace("_", " ")
            bonus_description = bonus_description.replace("<", divine_design_description)

        label += f"{self.name} ({self.grid_index}):<br>{bonus_description}"
        return Advice(
            label=label,
            picture_class=self._image,
            progression=self.level,
            goal=self.max_level,
        )


class ResearchGrid(dict[str, ResearchGridUpgrade]):
    def __init__(self, raw_research_info: list):

        research_levels: list[int] = safer_index(raw_research_info, 0, [])
        research_levels: list[list[int]] = [research_levels[i:i + research_grid_row_size] for i in range(0, len(research_levels), research_grid_row_size)]
        research_levels.reverse()
        research_levels: list[int] = [level for row in research_levels for level in row]

        for index, info in enumerate(research_grid_upgrade_data):
            if info["Name"] == "Name":
                continue
            level = safer_index(research_levels, index, 0)
            upgrade = ResearchGridUpgrade(info, level)
            self[upgrade.name] = upgrade

    def calculate_bonuses(self):
        for upgrade in self.values():
            upgrade.calculate_bonus()
class Research:
    def __init__(self, raw_data: dict):
        raw_research_info = safe_loads(raw_data.get("Research", []))
        if not raw_research_info:
            logger.warning("Research data not present.")
        self.grid = ResearchGrid(raw_research_info)

    def calculate_bonuses(self):
        self.grid.calculate_bonuses()