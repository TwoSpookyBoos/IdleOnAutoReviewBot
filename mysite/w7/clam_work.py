from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.general.session_data import session_data
from models.w7.clam_work import ClamWork

from utils.logging import get_logger

logger = get_logger(__name__)


def get_clam_work_bonuses_advicegroup(clam_work: ClamWork) -> AdviceGroup:
    return AdviceGroup(
        tier="",
        pre_string="Clam Work Compensations",
        advices=[bonus.get_bonus_advice(False) for bonus in clam_work.bonuses],
        informational=True,
    )


def get_section() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Clam Work",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Clam Work in W7!",
            picture="",
            unreached=True,
        )
    # Generate AdviceGroups
    advice_group_list = [
        get_clam_work_bonuses_advicegroup(session_data.account.clam_work),
    ]
    for advice_group in advice_group_list:
        advice_group.mark_advice_completed()
    return AdviceSection(
        name="Clam Work",
        tier="",
        header="Clam Work WIP",
        picture="data/Clam.png",
        groups=advice_group_list,
        unrated=True,
    )
