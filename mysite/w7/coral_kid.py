from models.advice.advice import Advice
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_bonuses_info_group() -> AdviceGroup:
    advices: list[Advice] = [
        bonus.get_advice() for bonus in session_data.account.coral_kid.values()
    ]

    for advice in advices:
        advice.mark_advice_completed()

    return AdviceGroup(
        pre_string='Bonuses',
        advices=advices,
        tier='',
        informational=True
    )


def get_coral_kid_section():
    if session_data.account.highest_world_reached < 7:
        coral_kid_AdviceSection = AdviceSection(
            name='Coral Kid',
            tier='Not Yet Evaluated',
            header='Come back after finding the Coral Kid in Balloon Bay!',
            picture='extracted_sprites/CoralKid0.png',
            unreached=True,
        )
        return coral_kid_AdviceSection

    groups = [get_bonuses_info_group()]
    return AdviceSection(
        name='Coral Kid',
        tier='',
        header='Coral Kid',
        picture='extracted_sprites/CoralKid0.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
