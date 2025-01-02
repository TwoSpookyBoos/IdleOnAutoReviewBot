from models.models import Advice, AdviceGroup, AdviceSection
from consts import starsigns_progressionTiers, break_you_best
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup():
    starsigns_AdviceDict = {
        "Signs": {},
    }
    infoTiers = 0
    max_tier = max(starsigns_progressionTiers.keys()) - infoTiers
    tier_Signs = 0
    ss = session_data.account.star_signs
    sse = session_data.account.star_sign_extras

    #Assess Tiers
    for tierNumber, tierRequirements in starsigns_progressionTiers.items():
        subgroupName = f"To Reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        # Total Unlocked Starsigns
        if sse.get('UnlockedSigns', 0) < tierRequirements['UnlockedSigns']:
            # logger.debug(f"Requirement failure at Tier {tierNumber} - Unlocked Signs: {sse['UnlockedSigns']} < {tierRequirements['UnlockedSigns']}")
            if subgroupName not in starsigns_AdviceDict['Signs'] and len(starsigns_AdviceDict['Signs']) < session_data.account.maxSubgroupsPerGroup:
                starsigns_AdviceDict['Signs'][subgroupName] = []
            if subgroupName in starsigns_AdviceDict['Signs']:
                starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                    label=f"Unlock {tierRequirements['UnlockedSigns'] - sse.get('UnlockedSigns', 0)} more Star Signs (Min to unlock {tierRequirements['Goal']})",
                    picture_class=f"telescope",
                    progression=sse.get('UnlockedSigns', 0),
                    goal=tierRequirements['UnlockedSigns']
                ))

        # Specific Starsigns unlocked
        if tierRequirements['SpecificSigns']:
            for ssName in tierRequirements['SpecificSigns']:
                if not ss.get(ssName, {}).get('Unlocked', False):
                    # logger.debug(f"Requirement failure at Tier {tierNumber} - Specific Sign: {ssName}")
                    if subgroupName not in starsigns_AdviceDict['Signs'] and len(starsigns_AdviceDict['Signs']) < session_data.account.maxSubgroupsPerGroup:
                        starsigns_AdviceDict['Signs'][subgroupName] = []
                    if subgroupName in starsigns_AdviceDict['Signs']:
                        starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                            label=f"Unlock {ssName}",
                            picture_class=ssName.strip("."),
                            progression=0,
                            goal=1
                        ))

        if subgroupName not in starsigns_AdviceDict['Signs'] and tier_Signs == tierNumber - 1:
            tier_Signs = tierNumber

    # Generate AdviceGroups
    tiers_ag = AdviceGroup(
        tier=tier_Signs,
        pre_string="Unlock additional Star Signs",
        advices=starsigns_AdviceDict['Signs'],
        post_string='Custom Star Sign artwork created by Listix'
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_Signs)
    return tiers_ag, overall_SectionTier, max_tier

def getStarsignsAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    starsigns_AdviceGroupDict = {}
    starsigns_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    starsigns_AdviceSection = AdviceSection(
        name="Star Signs",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Star Signs tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Telescope.gif',
        groups=starsigns_AdviceGroupDict.values()
    )

    return starsigns_AdviceSection
