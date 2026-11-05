from models.advice.advice_group import AdviceGroup
from models.advice.advice_group_tabbed import TabbedAdviceGroup, TabbedAdviceGroupTab
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import (
    add_tabbed_advice_group_or_spread_advice_group_list,
)

section_name = "Luminous Menagerie"
section_picture = "w7/menagerie/MenaJelly0.png"


def get_jellyfish_tabbed() -> TabbedAdviceGroup:
    return TabbedAdviceGroup(
        {
            jellyfish.name: (
                TabbedAdviceGroupTab(jellyfish.image),
                AdviceGroup(
                    tier="",
                    pre_string=jellyfish.name,
                    advices=jellyfish.get_advices(),
                    informational=True,
                    # Jellyfish upgrades are endless, never hide a tab as completed
                    completed=False,
                ),
            )
            for jellyfish in session_data.account.menagerie.jellyfish.values()
        }
    )


def get_missions_group() -> AdviceGroup:
    missions = session_data.account.menagerie.missions
    advices = [mission.get_advice() for mission in missions if mission.visible]
    return AdviceGroup(
        pre_string="Missions",
        advices=advices,
        tier="",
        informational=True,
    )


def get_unlocks_group() -> AdviceGroup:
    advices = [unlock.get_advice() for unlock in session_data.account.menagerie.unlocks]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Unlocks",
        advices=advices,
        tier="",
        informational=True,
    )


def get_boosts_group() -> AdviceGroup:
    advices = [
        boost.get_bonus_advice(link_to_section=False)
        for boost in session_data.account.menagerie.boosts
        if boost.visible
    ]
    return AdviceGroup(
        pre_string="Boosts",
        advices=advices,
        tier="",
        informational=True,
    )


def get_section() -> AdviceSection:
    menagerie = session_data.account.menagerie
    if session_data.account.world_progress.highest_reached < 7 or menagerie.rank < 1:
        return AdviceSection(
            name=section_name,
            tier="Not Yet Evaluated",
            header=(
                "Come back after visiting the Luminous Menagerie"
                " in the Molten Edge, 15 maps away from W7 town!"
            ),
            picture=section_picture,
            unreached=True,
        )

    session_data.account.add_alert_list(
        "World 7", [mission.get_claim_alert() for mission in menagerie.missions]
    )
    groups = {
        "Missions": get_missions_group(),
        "Unlocks": get_unlocks_group(),
        "Boosts": get_boosts_group(),
    }
    add_tabbed_advice_group_or_spread_advice_group_list(
        groups, get_jellyfish_tabbed(), "Jellyfish"
    )
    return AdviceSection(
        name=section_name,
        tier="",
        header=section_name,
        picture=section_picture,
        groups=groups.values(),
        informational=True,
        unrated=True,
    )
