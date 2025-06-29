from consts.progression_tiers_updater import true_max_tiers
from models.models import Advice, AdviceGroup, AdviceSection
from utils.logging import get_logger
from consts.consts import break_you_best, build_subgroup_label
from consts.progression_tiers import bribes_progressionTiers
from flask import g as session_data

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup():
    bribe_AdviceDict = {}

    optional_tiers = 0
    true_max = true_max_tiers['Bribes']
    max_tier = true_max - optional_tiers
    tier_BribesPurchased = 0

    player_bribes = session_data.account.bribes
    sum_bribes_list = {}
    for set_name, bribe_set in player_bribes.items():
        set_sum = 0
        for bribe in bribe_set.values():
            set_sum += max(0, bribe)  # Int representing purchase status. -1 = unavailable, 0 = available but unpurchased, 1 = purchased
        sum_bribes_list[set_name] = set_sum

    #Assess Tiers
    for tier, requirements in bribes_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier, max_tier)
        for set_name, specific_bribes in requirements.items():
            if len(specific_bribes) > sum_bribes_list[set_name]:
                if (
                    subgroup_label not in bribe_AdviceDict
                    and len(bribe_AdviceDict) < session_data.account.max_subgroups
                ):
                    bribe_AdviceDict[subgroup_label] = []
                if subgroup_label in bribe_AdviceDict:
                    for bribe in specific_bribes:
                        if player_bribes[set_name][bribe] <= 0:
                            bribe_AdviceDict[subgroup_label].append(Advice(
                                label=f"{set_name}: {bribe}"
                                      f"{'<br>Unavailable for Purchase!' if player_bribes[set_name][bribe] == -1 else ''}",
                                picture_class=bribe,
                                progression=0,
                                goal=1
                            ))
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
