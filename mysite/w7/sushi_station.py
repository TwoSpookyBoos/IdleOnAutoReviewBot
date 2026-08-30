from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data


def get_upgrades_group() -> AdviceGroup:
    advices = [
        upgrade.get_bonus_advice(False)
        for upgrade in session_data.account.sushi_station.upgrades.values()
    ]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Sushi Station Upgrades",
        advices=advices,
        tier="",
        informational=True,
    )


def get_milestones_group() -> AdviceGroup:
    sushi_station = session_data.account.sushi_station
    advices = [sushi_station.get_unique_sushi_advice()]
    advices += [milestone.get_advice() for milestone in sushi_station.milestones.values()]
    for advice in advices:
        advice.mark_advice_completed()
    return AdviceGroup(
        pre_string="Unique Sushi Bonuses",
        advices=advices,
        tier="",
        informational=True,
    )


def get_section():
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Sushi Station",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Sushi Station in W7!",
            picture="data/Sushi62.png",
            unreached=True,
        )

    groups = [get_upgrades_group(), get_milestones_group()]
    return AdviceSection(
        name="Sushi Station",
        tier="",
        header="Sushi Station",
        picture="data/Sushi62.png",
        groups=groups,
        informational=True,
        unrated=True,
    )
