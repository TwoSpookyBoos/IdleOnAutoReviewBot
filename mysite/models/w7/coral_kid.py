from consts.consts_autoreview import ValueToMulti, EmojiType
from consts.idleon.w7.coral_kid import coral_kid_description_templates, coral_kid_upgrades_divinity_requirements, \
    coral_kid_upgrades_bonus_base_formulas, coral_kid_upgrades_bonus_final_formulas
from models.advice.advice import Advice
from utils.number_formatting import round_and_trim
from utils.safer_data_handling import safe_loads, logger, safer_index


class CoralKidUpgrade:
    def __init__(self, index: int, level: int, description_template: str):
        self.index = index
        self.level = level
        self.description_template = description_template
        self.divinity_required = coral_kid_upgrades_divinity_requirements[index]
        self.image = f"coral-kid-upgrade-{index}"
        self.base_value = 0
        self.value = 0
        self.unlocked = False

    def calculate_bonus(self):
        from models.general.session_data import session_data
        self.base_value = round_and_trim(coral_kid_upgrades_bonus_base_formulas[self.index]({
            "level": self.level,
            "total_divinity_level": sum(session_data.account.all_skills["Divinity"]),
            "coral_reef_upgrade_count": sum(
                [coral["Level"] for coral in list(session_data.account.coral_reef["Reef Corals"].values())]
            ),
            "god_rank": session_data.account.divinity["GodRank"],
        }), 0)

        self.value = round_and_trim(coral_kid_upgrades_bonus_final_formulas[self.index]({
            "level": self.level,
            "total_divinity_level": sum(session_data.account.all_skills["Divinity"]),
            "coral_reef_upgrade_count": sum(
                [coral["Level"] for coral in list(session_data.account.coral_reef["Reef Corals"].values())]
            ),
            "god_rank": session_data.account.divinity["GodRank"],
        }), 0)

    def get_advice(self):
        from models.general.session_data import session_data
        total_div_level: int = sum(session_data.account.all_skills["Divinity"])
        self.unlocked = self.divinity_required <= total_div_level
        description = self.description_template
        if "{" in description:
            description = description.replace("{", str(self.base_value))
        elif "}" in description:
            description = description.replace("}", str(ValueToMulti(self.base_value)))

        if "$x" in description:
            description = description.replace("$x", f" {ValueToMulti(self.value)}x")
        elif "+$%" in description:
            description = description.replace("+$%", f" +{self.value}%")

        if self.index == 3:
            description = "Character's Divinity Skill Lv boosts Minor Link Bonuses."
        return Advice(
            label=description,
            picture_class=self.image,
            progression=self.level if self.unlocked else 0,
            goal=EmojiType.INFINITY.value if self.unlocked else 1,
        )


class CoralKid(dict[int, CoralKidUpgrade]):
    def __init__(self, raw_data: dict):
        raw_optlacc = safe_loads(raw_data.get("OptLacc", []))
        if not raw_optlacc:
            logger.warning("Coral Kid data not present.")
        for index, description_template in enumerate(coral_kid_description_templates):
            level = safer_index(raw_optlacc, 427 + index, 0)
            upgrade = CoralKidUpgrade(index, level, description_template)
            self[index] = upgrade

    def calculate_bonuses(self):
        for bonus in self.values():
            bonus.calculate_bonus()
