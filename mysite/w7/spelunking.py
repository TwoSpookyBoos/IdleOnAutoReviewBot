from consts.progression_tiers import true_max_tiers

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.general.session_data import session_data
from utils.logging import get_logger

logger = get_logger(__name__)


def get_cave_bonuses_advicegroup() -> AdviceGroup:
    cb_Advices = [
        cave.get_bonus_advice(False)
        for cave in session_data.account.spelunk.cave.values()
    ]

    for advice in cb_Advices:
        advice.mark_advice_completed()

    cb_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Cave Bonuses',
        advices=cb_Advices,
        informational=True
    )
    cb_AdviceGroup.remove_empty_subgroups()
    return cb_AdviceGroup

def get_progression_tiers_advicegroup() -> tuple[AdviceGroup, int, int, int]:
    spelunking_Advices = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers.get('Spelunking', 0)
    max_tier = true_max - optional_tiers
    tier_Spelunking = 0

    #Assess Tiers
    # for tier_number, requirements in spelunking_progressionTiers.items():
    #     subgroup_label = build_subgroup_label(tier_number, max_tier)
    #
    #     if subgroup_label not in spelunking_Advices['Tiers'] and tier_Spelunking == tier_number - 1:
    #         tier_Spelunking = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_Spelunking,
        pre_string='Progression Tiers',
        advices=spelunking_Advices['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Spelunking)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def get_spelunking_advicesection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        spelunking_AdviceSection = AdviceSection(
            name='Spelunking',
            tier='Not Yet Evaluated',
            header='Come back after unlocking Spelunking in W7!',
            picture='',
            unreached=True,
        )
        return spelunking_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    spelunking_AdviceGroupDict = {}
    spelunking_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = get_progression_tiers_advicegroup()
    spelunking_AdviceGroupDict['CaveBonuses'] = get_cave_bonuses_advicegroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    spelunking_AdviceSection = AdviceSection(
        name="Spelunking",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Spelunking Information WIP',
        #header=f"Best Spelunking tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="data/UIquickref13.png",
        groups=spelunking_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return spelunking_AdviceSection
