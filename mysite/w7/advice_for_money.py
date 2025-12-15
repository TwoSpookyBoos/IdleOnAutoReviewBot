
from models.models import AdviceSection, AdviceGroup, session_data

from models.models_util import get_advice_for_money_advice


def get_upgrade_info_group():
    advices = [get_advice_for_money_advice(upgrade_name, link_to_section=False)[1] for upgrade_name in session_data.account.advice_for_money['Upgrades'].keys()]
    return AdviceGroup(
        pre_string='Upgrades',
        advices=advices,
        tier='',
        informational=True
    )

def get_advice_for_money_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        afm_AdviceSection = AdviceSection(
            name='Advice For Money',
            tier='Not Yet Evaluated',
            header='Come back after finding the Big Fish on Doodle Reef in W7!',
            picture='',
            unreached=True,
        )
        return afm_AdviceSection

    groups = [get_upgrade_info_group()]
    return AdviceSection(
        name='Advice For Money',
        tier='',
        header='Advice For Money',
        picture='data/W7_fish.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
