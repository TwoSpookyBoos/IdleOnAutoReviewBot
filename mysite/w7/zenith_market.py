from models.advice.advice import Advice
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_upgrades_info_group() -> AdviceGroup:
    upgrade_advice: list[Advice] = [
        upgrade.get_advice() for upgrade in session_data.account.zenith_market.values()
    ]
    return AdviceGroup(
        pre_string='Upgrades',
        advices=upgrade_advice,
        tier='',
        informational=True
    )


def get_zenith_market_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        zenith_AdviceSection = AdviceSection(
            name='Zenith Market',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Zenith Market in Doodle Reef!',
            picture='data/Quest110.png',
            unreached=True,
        )
        return zenith_AdviceSection

    groups = [get_upgrades_info_group()]
    return AdviceSection(
        name='Zenith Market',
        tier='',
        header='Zenith Market',
        picture='data/Quest110.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
