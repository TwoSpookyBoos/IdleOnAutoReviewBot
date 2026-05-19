from models.general.session_data import session_data
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup


def get_upgrade_info_group():
    advices = [
        upgrade.get_bonus_advice(False)
        for upgrade in session_data.account.research.grid.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Research Grid",
        advices=advices,
        tier="",
        informational=True
    )

def get_observations_info_group():
    advices = [
        observation.get_advice()
        for observation in session_data.account.research.observations.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Observations",
        advices=advices,
        tier="",
        informational=True
    )

def get_section():
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Research",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Research in W7!",
            picture="research",
            unreached=True,
        )

    groups = [get_upgrade_info_group(), get_observations_info_group()]
    return AdviceSection(
        name="Research",
        tier="",
        header="Research",
        picture="data/ClassIcons61.png",
        groups=groups,
        informational=True,
        unrated=True,
    )
