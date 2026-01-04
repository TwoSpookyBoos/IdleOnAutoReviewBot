from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data

from models.advice.generators.w7 import get_legend_talent_advice


def get_legend_talents_info_group() -> AdviceGroup:
    sorted_talents = dict(sorted(session_data.account.legend_talents['Talents'].items(), key=lambda c: c[1]['Display Order']))
    advices = [get_legend_talent_advice(talent_name, False) for talent_name in sorted_talents.keys()]

    for advice in advices:
        advice.mark_advice_completed()

    return AdviceGroup(
        pre_string='Legend Talents',
        advices=advices,
        tier='',
        informational=True
    )

def get_legend_talents_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        lt_AdviceSection = AdviceSection(
            name='Legend Talents',
            tier='Not Yet Evaluated',
            header='Come back after unlocking Legend Talents in W7!',
            picture='',
            unreached=True,
        )
        return lt_AdviceSection

    groups = [get_legend_talents_info_group()]
    return AdviceSection(
        name='Legend Talents',
        tier='',
        header='Legend Talents',
        picture='extracted_sprites/Whallamus0.png',
        groups=groups,
        informational=True,
        unrated=True,
    )