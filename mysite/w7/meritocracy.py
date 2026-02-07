from models.general.session_data import session_data
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.logging import get_logger

logger = get_logger(__name__)


def get_vote_info_group():
    advices = {
        "Current Bonus": (
            [
                session_data.account.meritocracy.get_active_bonus_advice(),
            ]
        ),
        "On Vote": [
            bonus.get_vote_advice()
            for bonus in session_data.account.meritocracy.on_vote
        ],
        "All Bonuses": [
            upgrade.get_bonus_advice(False)
            for upgrade in session_data.account.meritocracy[1:]
        ],
    }
    advice_group = AdviceGroup(
        pre_string="All Meritocracy Bonuses",
        advices=advices,
        tier="",
        informational=True,
    )
    advice_group.remove_empty_subgroups()
    return advice_group


def get_section() -> AdviceSection:
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        return AdviceSection(
            name="Meritocracy",
            tier="",
            header="Come back after reach W7!",
            picture="extracted_sprites/Meritocracy.gif",
            unreached=True,
        )
    groups = [get_vote_info_group()]
    return AdviceSection(
        name="Meritocracy",
        tier="",
        header="Meritocracy WIP",
        picture="extracted_sprites/Meritocracy.gif",
        groups=groups,
        informational=True,
        unrated=True,
    )
