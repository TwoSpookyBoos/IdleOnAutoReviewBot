from models.models import Advice, AdviceGroup, AdviceSection
from consts import owl_progressionTiers, maxTiersPerGroup, break_you_best
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getNoFeathersGeneratingAlert():
    if session_data.account.owl['FeatherGeneration'] < 1:
        alert_advice = Advice(
            label=f"Find the Owl in W1 and start generating Feathers!"
            if not session_data.account.owl['Discovered']
            else f"You aren't generating any {{{{ Owl|#owl }}}} Feathers!",
            picture_class=f"feather-generation"
        )
        session_data.account.alerts_AdviceDict['World 1'].append(alert_advice)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    owl_AdviceDict = {
        "MegaFeathers": {}
    }
    infoTiers = 1
    max_tier = max(owl_progressionTiers.keys()) - infoTiers
    tier_MegaFeathers = 0

    featherResetsDict = {
        0: 6, 1: 6, 2: 7, 3: 8, 4: 9,
        5: 11, 6: 12, 7: 11, 8: 12, 9: 14,
        10: 16, 11: 17, 12: 18, 13: 19, 14: 21,
        15: 22, 16: 23, 17: 24, 18: 25, 19: 27,
        20: 28, 21: 29, 22: 30, 23: 31, 24: 32
    }
    orionDRValues = {
        23: 40, 29: 67.5
    }

    #Assess Tiers
    lastMFShown = -1
    for tierNumber, tierRequirementsDict in owl_progressionTiers.items():
        subgroupName = f"To Reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        if 'MegaFeathersOwned' in tierRequirementsDict:
            if session_data.account.owl['MegaFeathersOwned'] < tierRequirementsDict['MegaFeathersOwned']+1:
                for mf, resets in featherResetsDict.items():
                    if lastMFShown < mf <= tierRequirementsDict['MegaFeathersOwned']:
                        if session_data.account.owl['MegaFeathersOwned'] <= mf:
                            if subgroupName not in owl_AdviceDict['MegaFeathers'] and len(owl_AdviceDict['MegaFeathers']) < maxTiersPerGroup:
                                owl_AdviceDict['MegaFeathers'][subgroupName] = []
                            if subgroupName in owl_AdviceDict['MegaFeathers']:
                                lastMFShown = mf
                                owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                                    label=f"MF{mf+1}: Restart {resets} times first",
                                    picture_class=f"megafeather-{mf}" if mf < 10 else "the-great-mega-reset",
                                    progression=session_data.account.owl['FeatherRestarts'] if session_data.account.owl['MegaFeathersOwned'] == mf else 0,
                                    goal=resets
                                ))
        if 'BonusesOfOrion' in tierRequirementsDict:
            if session_data.account.owl['BonusesOfOrion'] < tierRequirementsDict['BonusesOfOrion']:
                if subgroupName not in owl_AdviceDict['MegaFeathers'] and len(owl_AdviceDict['MegaFeathers']) < maxTiersPerGroup:
                    owl_AdviceDict['MegaFeathers'][subgroupName] = []
                if subgroupName in owl_AdviceDict['MegaFeathers']:
                    orion_advice = Advice(
                            label=f"Before MF{tierRequirementsDict['MegaFeathersOwned']+1}, purchase Bonuses of Orion {tierRequirementsDict['BonusesOfOrion']}",
                            picture_class="bonuses-of-orion",
                            progression=session_data.account.owl['BonusesOfOrion'],
                            goal=tierRequirementsDict['BonusesOfOrion']
                        )
                    if len(owl_AdviceDict['MegaFeathers']) > 0:
                        owl_AdviceDict['MegaFeathers'][subgroupName].insert(-1, orion_advice)
                    else:
                        owl_AdviceDict['MegaFeathers'][subgroupName].append(orion_advice)
                    owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                        label=f"{orionDRValues.get(tierRequirementsDict['BonusesOfOrion'], 'IDK')}% Drop Rate will then be yours 🎉",
                        picture_class="drop-rate"
                    ))

        if subgroupName not in owl_AdviceDict["MegaFeathers"] and tier_MegaFeathers == tierNumber - 1:
            tier_MegaFeathers = tierNumber

    tiers_ag = AdviceGroup(
        tier=tier_MegaFeathers if tier_MegaFeathers <= max_tier else "",
        pre_string="Collect Mega Feathers and Bonuses of Orion" if tier_MegaFeathers <= max_tier else "Info- Goals at this point will take months",
        advices=owl_AdviceDict['MegaFeathers'],
        informational=tier_MegaFeathers >= max_tier
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_MegaFeathers)
    return tiers_ag, overall_SectionTier, max_tier

def getOwlAdviceSection() -> AdviceSection:
    # Generate Alert Advice
    getNoFeathersGeneratingAlert()

    # Generate AdviceGroups
    owl_AdviceGroupDict = {}
    owl_AdviceGroupDict['MegaFeathers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    owl_AdviceSection = AdviceSection(
        name="Owl",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Owl tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Owl.gif',
        groups=owl_AdviceGroupDict.values()
    )
    return owl_AdviceSection
