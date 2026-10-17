from consts.consts_autoreview import EmojiType, ValueToMulti
from consts.idleon.w1.darts import darts_upgrade_descriptions
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_index

logger = get_logger(__name__)


class DartsUpgrade:
    def __init__(self, index: int, level: int, description_template: str):
        self.index = index
        self.level = level
        self.description = description_template
        self.image = f"darts-upgrade-{index + 1}"
        self.value = 0

    def calculate(self):
        if "{" in self.description:
            self.value = self.level
            self.description = self.description.replace("{", str(self.value))
        elif "}" in self.description:
            self.value = ValueToMulti(self.level)
            self.description = self.description.replace("}", str(self.value))

    def get_advice(self, link_to_section: bool = True) -> Advice:
        link_to_section_text = "{{ Darts|#darts }} - " if link_to_section else ""
        return Advice(
            label=f"{link_to_section_text}Upgrade {self.index + 1}: {self.description}",
            picture_class=self.image,
            progression=self.level,
            goal=EmojiType.INFINITY.value,
            resource="darts-shop-currency",
        )


class Darts:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[int, DartsUpgrade] = {}
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        if not raw_optlacc:
            logger.warning("Darts data not present.")
        # skip the first item in the array because that's just the default shop text, not an upgrade description
        for index, description_template in enumerate(darts_upgrade_descriptions[1:]):
            level = safer_index(raw_optlacc, 435 + index, 0)
            upgrade = DartsUpgrade(index, level, description_template)
            self.upgrades[index] = upgrade

    def calculate(self):
        for upgrade in self.upgrades.values():
            upgrade.calculate()
