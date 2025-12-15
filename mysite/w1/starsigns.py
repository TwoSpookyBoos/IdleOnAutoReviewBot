
from models.models import Advice, AdviceGroup, AdviceSection, session_data
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import starsigns_progressionTiers, true_max_tiers
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger


logger = get_logger(__name__)

def getProgressionTiersAdviceGroup():
    starsigns_AdviceDict = {
        'Signs': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Star Signs']
    max_tier = true_max - optional_tiers
    tier_Signs = 0
    ss = session_data.account.star_signs
    sse = session_data.account.star_sign_extras

    #Assess Tiers
    for tier_number, requirements in starsigns_progressionTiers.items():
        subgroupName = build_subgroup_label(tier_number, max_tier)

        # Total Unlocked Starsigns
        if sse.get('UnlockedSigns', 0) < requirements['UnlockedSigns']:
            # logger.debug(f"Requirement failure at Tier {tier_number} - Unlocked Signs: {sse['UnlockedSigns']} < {requirements['UnlockedSigns']}")
            add_subgroup_if_available_slot(starsigns_AdviceDict['Signs'], subgroupName)
            if subgroupName in starsigns_AdviceDict['Signs']:
                starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                    label=f"Unlock {requirements['UnlockedSigns'] - sse.get('UnlockedSigns', 0)} more Star Signs (Min to unlock {requirements['Goal']})",
                    picture_class=f"telescope",
                    progression=sse.get('UnlockedSigns', 0),
                    goal=requirements['UnlockedSigns']
                ))

        # Specific Starsigns unlocked
        if requirements['SpecificSigns']:
            for ssName in requirements['SpecificSigns']:
                if not ss.get(ssName, {}).get('Unlocked', False):
                    add_subgroup_if_available_slot(starsigns_AdviceDict['Signs'], subgroupName)
                    if subgroupName in starsigns_AdviceDict['Signs']:
                        starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                            label=f"Unlock {ssName}",
                            picture_class=ssName.strip("."),
                            progression=0,
                            goal=1
                        ))
        if subgroupName not in starsigns_AdviceDict['Signs'] and tier_Signs == tier_number - 1:
            tier_Signs = tier_number

    # Generate AdviceGroups
    tiers_ag = AdviceGroup(
        tier=tier_Signs,
        pre_string='Unlock additional Star Signs',
        advices=starsigns_AdviceDict['Signs'],
        post_string='Custom Star Sign artwork created by Listix'
    )
    overall_SectionTier = min(true_max, tier_Signs)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getStarsignsAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    starsigns_AdviceGroupDict = {}
    starsigns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    starsigns_AdviceSection = AdviceSection(
        name='Star Signs',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Star Signs tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Telescope.gif',
        groups=starsigns_AdviceGroupDict.values()
    )

    return starsigns_AdviceSection
