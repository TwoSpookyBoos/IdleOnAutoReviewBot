from models.models import AdviceSection, AdviceGroup
from flask import g as session_data

from models.models_util import get_darts_minigame_advice


def get_upgrade_info_group():
    advices = [get_darts_minigame_advice(index, link_to_section=False)[1] for index in session_data.account.darts_minigame['Upgrades'].keys()]
    return AdviceGroup(
        pre_string='Upgrades',
        advices=advices,
        tier='',
        informational=True
    )

def get_darts_minigame_section():
    groups = [get_upgrade_info_group()]
    return AdviceSection(
        name='Darts Minigame',
        tier='',
        header='Darts Minigame',
        picture='data/DartArm.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
