from models.models import AdviceSection, AdviceGroup, Advice
from flask import g as session_data

from models.models_util import get_darts_advice


def get_upgrade_info_group():
    advices = [
        Advice(
            label="The shop is located in Winding Willows (Baby Boa)",
            picture_class="baby-boa",
        ),
        *[get_darts_advice(index, link_to_section=False)[1] for index in session_data.account.darts['Upgrades'].keys()]
    ]
    return AdviceGroup(
        pre_string='Upgrades',
        advices=advices,
        tier='',
        informational=True
    )

def get_darts_section():
    groups = [get_upgrade_info_group()]
    return AdviceSection(
        name='Darts',
        tier='',
        header='Darts',
        picture='data/DartArm.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
