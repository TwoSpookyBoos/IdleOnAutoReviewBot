from models.general.cards import Card
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
    coral_reef = session_data.account.coral_reef
    shellslug = session_data.account.companions['Shellslug']
    more_coral = session_data.account.gemshop.purchases['More Coral']
    more_coral_advice = more_coral.get_advice(additional_text=f": x{coral_reef.more_coral_multi}/x3.0 Daily Corals")
    demonblub_card: Card = next(card for card in session_data.account.cards if card.name == 'Demonblub')

    multi_group_d_advice: list[Advice] = [
        session_data.account.coral_kid[5].get_advice(),
        session_data.account.dancing_coral[0].get_advice(),
        coral_reef.get_clam_work_advice(),
        coral_reef.get_killroy_advice(),
        session_data.account.stamps['Corale Stamp'].get_advice(),
        session_data.account.alchemy_vials['Scale On Ice (Scaled Fragment)'].get_advice(
            additional_text=' Daily Corals', full_name=False, resource='scaled-fragment'
        ),
        session_data.account.legend_talents['Coral Restoration'].get_advice(),
        session_data.account.arcade[57].get_advice(),
        session_data.account.sneaking.emporium['Coral Conservationism'].get_obtained_advice(),
        demonblub_card.getAdvice(),
        coral_reef.get_coral_statue_advice(),
    ]

    coral_sources: dict[str, list[Advice]] = {
        f'Total daily corals: {round(coral_reef.total_daily_corals, 2):g}': [],
        f'Base: {coral_reef.base_daily_corals}': [coral_reef.get_base_daily_corals_advice()],
        f'Multi Group A: x{round(coral_reef.shellslug_multi, 2):g}': [shellslug.get_advice()],
        f'Multi Group B: x{round(coral_reef.coolral_multi, 2):g}': [coral_reef.get_coolral_advice()],
        f'Multi Group C: x{round(coral_reef.more_coral_multi, 2):g}': [more_coral_advice],
        f'Multi Group D: x{round(coral_reef.multi_group_d_mult, 2):g}': multi_group_d_advice,
    }

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
