from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger

from consts.consts_w5 import snail_max_possible_rank, snail_first_consecration_rank

logger = get_logger(__name__)

def getSnailInformationGroup() -> AdviceGroup:
    snail = session_data.account.gaming.snail
    snail_AdviceDict = {
        'General': [snail.get_rank_advice()],
    }

    if snail.rank > 0:
        snail_AdviceDict['General'].append(snail.get_envelopes_advice())
        current_rank_group_label = f"Current Rank {snail.rank} Info"

        if snail.maxed:
            snail_AdviceDict[current_rank_group_label] = [snail.get_maxed_advice()]
        elif snail.sodium_too_low:
            snail_AdviceDict[current_rank_group_label] = [snail.get_sodium_too_low_advice()]
        else:
            snail_AdviceDict['General'].append(snail.get_final_ballad_advice())

            # Current Rank Info
            snail_AdviceDict[current_rank_group_label] = [snail.get_encouragement_advice(snail.rank, "Step 1")]
            num_encourage = snail.encouragement_info[snail.rank][0]
            if snail.rank > snail_first_consecration_rank and num_encourage > 0:
                snail_AdviceDict[current_rank_group_label].append(snail.get_consecrated_advice())
            else:
                snail_AdviceDict[current_rank_group_label].extend(snail.get_safety_advices())

            # All relevant encouragement info
            subgroup_label = 'Relevant Encouragement Info (for resets or advancement)'
            snail_AdviceDict[subgroup_label] = []

            for level in range(snail.min_rank, snail.target_rank):
                rank_type = (
                    'Previous' if level < snail.rank
                    else 'Future' if level > snail.rank
                    else 'Current'
                )

                snail_AdviceDict[subgroup_label].append(snail.get_encouragement_advice(level, f"{rank_type} Rank {level}"))

    for subgroup in snail_AdviceDict:
        for advice in snail_AdviceDict[subgroup]:
            advice.mark_advice_completed()

    snail_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Snail Ranks',
        post_string='Safety means your chance of not ending up worse than you started due to potential Resets',
        advices=snail_AdviceDict,
        informational=True,
        completed=snail.rank >= snail_max_possible_rank
    )
    snail_AdviceGroup.remove_empty_subgroups()
    return snail_AdviceGroup

def getGamingProgressionTierAdviceGroups():
    gaming_AdviceGroups = {}
    optional_tiers = 0
    true_max = true_max_tiers['Gaming']
    max_tier = true_max - optional_tiers

    # Generate AdviceGroups (none right now!)

    overall_SectionTier = min(true_max, 0)
    return gaming_AdviceGroups, overall_SectionTier, max_tier, true_max

def getGamingAdviceSection() -> AdviceSection:
    highestGamingSkillLevel = max(session_data.account.characters.all_skills.get('Gaming', [0]))
    if highestGamingSkillLevel < 1:
        gaming_AdviceSection = AdviceSection(
            name='Gaming',
            tier='0',
            pinchy_rating=0,
            header='Come back after unlocking the Gaming skill in W5!',
            picture='data/ClassIcons56.png',
            unreached=True
        )
        return gaming_AdviceSection

    # Generate AdviceGroup
    gaming_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getGamingProgressionTierAdviceGroups()
    if session_data.account.gaming.snail.rank < snail_max_possible_rank:
        gaming_AdviceGroupDict['Snail'] = getSnailInformationGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    gaming_AdviceSection = AdviceSection(
        name='Gaming',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header='Gaming Information',  #f"Best Gaming tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/ClassIcons56.png',
        groups=gaming_AdviceGroupDict.values(),
        unrated=True
    )

    return gaming_AdviceSection
