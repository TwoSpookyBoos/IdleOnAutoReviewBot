from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from models.advice.generators.w1 import get_basketball_advice


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
