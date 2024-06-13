from models.models import Advice, AdviceGroup, AdviceSection
from utils.text_formatting import pl
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

    max_tier = max(owl_progressionTiers.keys())
    tier_MegaFeathers = 0
    featherResetsDict = {
        0: 6, 1: 6, 2: 7, 3: 8, 4: 9,
        5: 11, 6: 12, 7: 11, 8: 12, 9: 14,
        10: 16, 11: 17, 12: 18, 13: 19, 14: 21,
        15: 22, 16: 23, 17: 23
    }

    # Generate Advice
    lastMFShown = -1
    for tierNumber, tierRequirementsDict in owl_progressionTiers.items():
        subgroupName = f"To Reach Tier {tierNumber}"
        if 'FeatherGeneration' in tierRequirementsDict:
            if session_data.account.owl['FeatherGeneration'] < tierRequirementsDict['FeatherGeneration']:
                if subgroupName not in owl_AdviceDict['MegaFeathers'] and len(owl_AdviceDict['MegaFeathers']) < maxTiersPerGroup:
                    owl_AdviceDict['MegaFeathers'][subgroupName] = []
                if subgroupName in owl_AdviceDict['MegaFeathers']:
                    if session_data.account.owl['MegaFeathersOwned'] == 0:
                        preString = f"Find the Owl in W1 and start generating Feathers!"
                    else:
                        preString = f"Start generating Feathers!"
                    owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                        label=preString,
                        picture_class=f"feather-generation"
                    ))
        if 'MegaFeathersOwned' in tierRequirementsDict:
            if session_data.account.owl['MegaFeathersOwned'] < tierRequirementsDict['MegaFeathersOwned']:
                for mf, resets in featherResetsDict.items():
                    if mf > lastMFShown and mf <= tierRequirementsDict['MegaFeathersOwned']:
                        if session_data.account.owl['MegaFeathersOwned'] <= mf:
                            if subgroupName not in owl_AdviceDict['MegaFeathers'] and len(owl_AdviceDict['MegaFeathers']) < maxTiersPerGroup:
                                owl_AdviceDict['MegaFeathers'][subgroupName] = []
                            if subgroupName in owl_AdviceDict['MegaFeathers']:
                                owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                                    label=f"Mega Feather {mf+1}: Complete {resets} Feather Restarts first",
                                    picture_class=f"megafeather-{mf}" if mf < 10 else "the-great-mega-reset",
                                    progression=session_data.account.owl['FeatherRestarts'] if len(owl_AdviceDict['MegaFeathers']) == 0 else 0,
                                    goal=resets
                                ))
                                lastMFShown = mf
        if 'BonusesOfOrion' in tierRequirementsDict:
            if session_data.account.owl['BonusesOfOrion'] < tierRequirementsDict['BonusesOfOrion']:
                if subgroupName not in owl_AdviceDict['MegaFeathers'] and len(owl_AdviceDict['MegaFeathers']) < maxTiersPerGroup:
                    owl_AdviceDict['MegaFeathers'][subgroupName] = []
                if subgroupName in owl_AdviceDict['MegaFeathers']:
                    owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                    label=f"After reaching Mega Feather 18, purchase level 23 of Bonuses of Orion",
                    picture_class="bonuses-of-orion",
                    progression=session_data.account.owl['BonusesOfOrion'],
                    goal=23
                ))
                owl_AdviceDict['MegaFeathers'][subgroupName].append(Advice(
                    label=f"40% Drop Rate will then be yours 🎉",
                    picture_class="drop-rate"
                ))

        if subgroupName not in owl_AdviceDict["MegaFeathers"] and tier_MegaFeathers == tierNumber - 1:
            tier_MegaFeathers = tierNumber

    # Generate AdviceGroups
    owl_AdviceGroupDict['MegaFeathers'] = AdviceGroup(
        tier=tier_MegaFeathers,
        pre_string="Collect Mega Feathers and Bonuses of Orion",
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
    else:
        owl_AdviceSection.header = f"Best Owl tier met: {tier_section}"

    return owl_AdviceSection
