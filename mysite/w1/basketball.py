from models.models import AdviceSection, AdviceGroup, Advice
from flask import g as session_data

from models.models_util import get_basketball_advice


def get_upgrade_info_group():
    advices = [
        Advice(
            label="The shop is located in the Valley of the Beans (Bored Beans)",
            picture_class="bored-bean",
        ),
        *[get_basketball_advice(index, link_to_section=False)[1] for index in session_data.account.basketball['Upgrades'].keys()]
    ]
    return AdviceGroup(
        pre_string='Upgrades',
        advices=advices,
        tier='',
        informational=True
    )

def get_basketball_section():
    groups = [get_upgrade_info_group()]
    return AdviceSection(
        name='Basketball',
        tier='',
        header='Basketball',
        picture='customized/hoops_blob.gif',
        groups=groups,
        informational=True,
        unrated=True,
    )
