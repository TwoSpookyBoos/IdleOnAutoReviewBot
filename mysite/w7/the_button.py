from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_bonuses_group() -> AdviceGroup:
    bonus_sources = session_data.account.the_button.get_upcoming_bonuses()
    for subgroup in bonus_sources.values():
        for advice in subgroup:
            advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Upcoming Button Bonuses",
        advices=bonus_sources,
        tier="",
        informational=True,
    )


def get_totals_group() -> AdviceGroup:
    advices = [bonus.get_advice() for bonus in session_data.account.the_button.bonuses]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Total Bonuses Earned",
        advices=advices,
        tier="",
        informational=True,
    )


def get_section():
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="The Button",
            tier="Not Yet Evaluated",
            header="Come back after unlocking The Button on the Mantaray map in W7!",
            picture="data/ButtonG.gif",
            unreached=True,
        )

    groups = [get_bonuses_group(), get_totals_group()]
    return AdviceSection(
        name="The Button",
        tier="",
        header="The Button",
        picture="data/ButtonG.gif",
        groups=groups,
        informational=True,
        unrated=True,
    )
