from models.models import Advice, AdviceGroup, AdviceSection
from consts import starsigns_progressionTiers, maxTiersPerGroup
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def setStarsignsProgressionTier() -> AdviceSection:
    starsigns_AdviceDict = {
        "Signs": {},
    }
    starsigns_AdviceGroupDict = {}
    starsigns_AdviceSection = AdviceSection(
        name="Star Signs",
        tier="Not Yet Evaluated",
        header="Best Star Signs tier met: Not Yet Evaluated. Recommended Star Sign actions",
        picture='Telescope.gif'
    )

    infoTiers = 0
    max_tier = max(starsigns_progressionTiers.keys()) - infoTiers
    tier_TotalSigns = 0
    tier_SpecificSigns = 0

    ss = session_data.account.star_signs
    sse = session_data.account.star_sign_extras

    # Generate Alert Advice

    # Generate Advice
    for tierNumber, tierRequirements in starsigns_progressionTiers.items():
        subgroupName = f"To Reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        #Total Unlocked Starsigns
        if sse.get('UnlockedSigns', 0) < tierRequirements['UnlockedSigns']:
            #logger.debug(f"Requirement failure at Tier {tierNumber} - Unlocked Signs: {sse['UnlockedSigns']} < {tierRequirements['UnlockedSigns']}")
            if subgroupName not in starsigns_AdviceDict['Signs'] and len(starsigns_AdviceDict['Signs']) < maxTiersPerGroup:
                starsigns_AdviceDict['Signs'][subgroupName] = []
            if subgroupName in starsigns_AdviceDict['Signs']:
                starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                    label=f"Unlock {tierRequirements['UnlockedSigns'] - sse.get('UnlockedSigns', 0)} more Star Signs (Min to unlock {tierRequirements['Goal']})",
                    picture_class=f"telescope",
                    progression=sse.get('UnlockedSigns', 0),
                    goal=tierRequirements['UnlockedSigns']
                ))
        if subgroupName not in starsigns_AdviceDict['Signs'] and tier_TotalSigns == tierNumber - 1:
            tier_TotalSigns = tierNumber

        #Specific Starsigns unlocked
        if tierRequirements['SpecificSigns']:
            for ssName in tierRequirements['SpecificSigns']:
                if not ss.get(ssName, {}).get('Unlocked', False):
                    #logger.debug(f"Requirement failure at Tier {tierNumber} - Specific Sign: {ssName}")
                    if subgroupName not in starsigns_AdviceDict['Signs'] and len(starsigns_AdviceDict['Signs']) < maxTiersPerGroup:
                        starsigns_AdviceDict['Signs'][subgroupName] = []
                    if subgroupName in starsigns_AdviceDict['Signs']:
                        starsigns_AdviceDict['Signs'][subgroupName].append(Advice(
                            label=ssName,
                            picture_class=ssName.strip("."),
                        ))

        if subgroupName not in starsigns_AdviceDict['Signs'] and tier_SpecificSigns == tierNumber - 1:
            tier_SpecificSigns = tierNumber

    # Generate AdviceGroups
    starsigns_AdviceGroupDict['Signs'] = AdviceGroup(
        tier=tier_TotalSigns,
        pre_string="Unlock additional Star Signs",
        advices=starsigns_AdviceDict['Signs']
    )

    # Generate AdviceSection
    overall_StarsignsTier = min(max_tier + infoTiers, tier_TotalSigns, tier_SpecificSigns)
    tier_section = f"{overall_StarsignsTier}/{max_tier}"
    starsigns_AdviceSection.pinchy_rating = overall_StarsignsTier
    starsigns_AdviceSection.tier = tier_section
    starsigns_AdviceSection.groups = starsigns_AdviceGroupDict.values()
    if overall_StarsignsTier >= max_tier:
        starsigns_AdviceSection.header = f"Best Star Signs tier met: {tier_section}<br>You best ❤️"
        starsigns_AdviceSection.complete = True
    else:
        starsigns_AdviceSection.header = f"Best Star Signs tier met: {tier_section}"

    return starsigns_AdviceSection
