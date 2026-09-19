from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_cells_group() -> AdviceGroup:
    advices = [
        cell.get_advice()
        for cell in session_data.account.jelly_operator.cells.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Cells",
        advices=advices,
        tier="",
        informational=True,
    )


def get_upgrades_group() -> AdviceGroup:
    advices = [
        upgrade.get_bonus_advice(False)
        for upgrade in session_data.account.jelly_operator.upgrades.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Jelly Operator Upgrades",
        advices=advices,
        tier="",
        informational=True,
    )


def get_obstructions_group() -> AdviceGroup:
    advices = [
        obstruction.get_advice()
        for obstruction in session_data.account.jelly_operator.obstructions.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Obstruction Bonuses",
        advices=advices,
        tier="",
        informational=True,
    )


def get_section():
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Jelly Operator",
            tier="Not Yet Evaluated",
            header=(
                "Come back after buying Jelly Operator Linguistics (H3)"
                " on the Research Grid in W7!"
            ),
            picture="data/JellyUpg23.png",
            unreached=True,
        )

    groups = [get_cells_group(), get_upgrades_group(), get_obstructions_group()]
    return AdviceSection(
        name="Jelly Operator",
        tier="",
        header="Jelly Operator",
        picture="data/JellyUpg23.png",
        groups=groups,
        informational=True,
        unrated=True,
    )
