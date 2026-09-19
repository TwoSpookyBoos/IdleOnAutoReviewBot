from models.general.session_data import session_data
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import bribes_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup():
    bribe_AdviceDict = {}

    optional_tiers = 0
    true_max = true_max_tiers['Bribes']
    max_tier = true_max - optional_tiers
    tier_BribesPurchased = 0

    player_bribes = session_data.account.bribes

    #Assess Tiers
    for tier, requirements in bribes_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier, max_tier)
        for set_name, specific_bribes in requirements.items():
            if len(specific_bribes) > player_bribes.purchased_count(set_name):
                add_subgroup_if_available_slot(bribe_AdviceDict, subgroup_label)
                if subgroup_label in bribe_AdviceDict:
                    for bribe_name in specific_bribes:
                        bribe = player_bribes[bribe_name]
                        if not bribe.purchased:
                            bribe_AdviceDict[subgroup_label].append(bribe.get_advice())
        if subgroup_label not in bribe_AdviceDict and tier_BribesPurchased >= tier - 1:
            tier_BribesPurchased = tier

    overall_SectionTier = min(true_max, tier_BribesPurchased)

    # Generate AdviceGroups
    bribes_ag = AdviceGroup(
        tier=overall_SectionTier,
        pre_string=f"Purchase remaining Bribes",
        advices=bribe_AdviceDict
    )
    bribes_ag.remove_empty_subgroups()

    return bribes_ag, overall_SectionTier, max_tier, true_max

def getBribesAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    bribe_AdviceGroupDict = {}
    bribe_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    bribe_AdviceSection = AdviceSection(
        name="Bribes",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Bribe tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Bribes.png',
        groups=bribe_AdviceGroupDict.values()
    )

    return bribe_AdviceSection
