from models.general.session_data import session_data
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup


def get_upgrade_info_group():
    advices = [
        upgrade.get_bonus_advice(False)
        for upgrade in session_data.account.advice_fish.values()
    ]
    return AdviceGroup(
        pre_string="Upgrades", advices=advices, tier="", informational=True
    )


def get_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Advice Fish",
            tier="Not Yet Evaluated",
            header="Come back after finding the Big Fish on Doodle Reef in W7!",
            picture="",
            unreached=True,
        )

    groups = [get_upgrade_info_group()]
    return AdviceSection(
        name="Advice Fish",
        tier="",
        header="Advice Fish",
        picture="data/W7_fish.png",
        groups=groups,
        informational=True,
        unrated=True,
    )
