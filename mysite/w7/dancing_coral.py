from models.advice.advice import Advice
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_bonuses_info_group() -> AdviceGroup:
    advices: list[Advice] = [
        bonus.get_advice() for bonus in session_data.account.dancing_coral.values()
    ]

    for advice in advices:
        advice.mark_advice_completed()

    return AdviceGroup(
        pre_string='Bonuses',
        advices=advices,
        tier='',
        informational=True
    )


def get_dancing_coral_section():
    if session_data.account.highest_world_reached < 7:
        dancing_coral_AdviceSection = AdviceSection(
            name='Dancing Coral',
            tier='Not Yet Evaluated',
            header='Come back after finding the Dancing Coral in Barnacle Curb!',
            picture='extracted_sprites/DancingCoral0.png',
            unreached=True,
        )
        return dancing_coral_AdviceSection

    groups = [get_bonuses_info_group()]
    return AdviceSection(
        name='Dancing Coral',
        tier='',
        header='Dancing Coral',
        picture='extracted_sprites/DancingCoral0.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
