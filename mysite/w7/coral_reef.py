from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data


def get_corals_info_group() -> AdviceGroup:
    coral_advice: list[Advice] = [
        Advice(
            label=f"Town Corals: {session_data.account.coral_reef.town_corals}",
            picture_class="coral"
        ), *[bonus.get_advice() for bonus in session_data.account.coral_reef.values()]
    ]
    return AdviceGroup(
        pre_string='Corals',
        advices=coral_advice,
        tier='',
        informational=True
    )

def get_sources_of_coral_info_group() -> AdviceGroup:
    coral_sources = session_data.account.coral_reef.get_daily_corals_advices()

    for subgroup in coral_sources.values():
        for advice in subgroup:
            advice.mark_advice_completed()

    return AdviceGroup(
        pre_string='Sources of daily Corals',
        advices=coral_sources,
        tier='',
        informational=True
    )

def get_coral_reef_section():
    # Check if player has reached this section
    if session_data.account.world_progress.highest_reached < 7:
        reef_AdviceSection = AdviceSection(
            name='Coral Reef',
            tier='Not Yet Evaluated',
            header='Come back after unlocking W7!',
            picture='',
            unreached=True,
        )
        return reef_AdviceSection

    groups = [get_corals_info_group(), get_sources_of_coral_info_group()]
    return AdviceSection(
        name='Coral Reef',
        tier='',
        header='Coral Reef',
        picture='extracted_sprites/HumbleHugh.gif',
        groups=groups,
        informational=True,
        unrated=True,
    )
