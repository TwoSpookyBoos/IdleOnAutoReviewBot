from models.models import Advice, AdviceGroup, AdviceSection
from consts import owl_progressionTiers, maxTiersPerGroup
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def setOwlProgressionTier() -> AdviceSection:
    owl_AdviceDict = {
        "MegaFeathers": {}
    }
    owl_AdviceGroupDict = {}
    owl_AdviceSection = AdviceSection(
        name="Owl",
        tier="Not Yet Evaluated",
        header="Best Owl tier met: Not Yet Evaluated. Recommended Owl actions",
        picture='Owl.gif'
    )

    max_tier = max(owl_progressionTiers.keys())-1  #One informational tier
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

    # Generate Alert Advice
    session_data.account.owl['FeatherGeneration'] = 0
    if session_data.account.owl['FeatherGeneration'] < 1:
        alert_advice = Advice(
            label=("Find the Owl in W1 and start generating Feathers!"
                   if session_data.account.owl['MegaFeathersOwned'] == 0
                   else "You aren't generating any {{ Owl|#owl }} Feathers!"),
            picture_class=f"feather-generation"
        )
        session_data.account.alerts_AdviceDict['World 1'].append(alert_advice)

    # Generate Advice
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

    # Generate AdviceGroups
    owl_AdviceGroupDict['MegaFeathers'] = AdviceGroup(
        tier=tier_MegaFeathers if tier_MegaFeathers <= max_tier else "",
        pre_string="Collect Mega Feathers and Bonuses of Orion" if tier_MegaFeathers <= max_tier else "Info- Goals at this point will take months",
        advices=owl_AdviceDict['MegaFeathers']
    )

    # Generate AdviceSection
    overall_OwlTier = min(max_tier, tier_MegaFeathers)
    tier_section = f"{overall_OwlTier}/{max_tier}"
    owl_AdviceSection.pinchy_rating = overall_OwlTier
    owl_AdviceSection.tier = tier_section
    owl_AdviceSection.groups = owl_AdviceGroupDict.values()
    if overall_OwlTier == max_tier:
        owl_AdviceSection.header = f"Best Owl tier met: {tier_section}<br>You best ❤️"
        owl_AdviceSection.complete = True
    else:
        owl_AdviceSection.header = f"Best Owl tier met: {tier_section}"

    return owl_AdviceSection
