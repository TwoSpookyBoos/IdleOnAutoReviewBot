from consts.idleon.w1.basketball import basketball_upgrade_descriptions
from utils.safer_data_handling import safe_loads, safer_index, logger


class BasketballUpgrade:
    def __init__(self, index: int, level: int, description_template: str):
        self.index = index
        self.level = level
        self.description = description_template
        self.image = f"basketball-upgrade-{index + 1}"
        self.value = 0

    def calculate(self):
        if "{" in self.description:
            self.value = self.level
            self.description = self.description.replace("{", str(self.value))


class Basketball:
    def __init__(self, raw_data: dict):
        self.upgrades: dict[int, BasketballUpgrade] = {}
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        if not raw_optlacc:
            logger.warning("Basketball data not present.")
        # skip the first item in the array because that's just the default shop text, not an upgrade description
        for index, description_template in enumerate(basketball_upgrade_descriptions[1:]):
            level = safer_index(raw_optlacc, 419 + index, 0)
            upgrade = BasketballUpgrade(index, level, description_template)
            self.upgrades[index] = upgrade

    def calculate(self):
        for upgrade in self.upgrades.values():
            upgrade.calculate()
