import json

from flask import g as session_data

import consts
from consts import equinox_progressionTiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.text_formatting import pl


logger = get_logger(__name__)
optionalUpgradeList = ['Shades of K', 'Laboratory Fuse']


def getRawEquinoxValues():
    rawEquinoxBonusLevelsList = session_data.account.raw_data.get("Dream", [0]*30)
    if isinstance(rawEquinoxBonusLevelsList, str):
        rawEquinoxBonusLevelsList = json.loads(rawEquinoxBonusLevelsList)
    equinoxBonusLevelsDict = {
        'Equinox Dreams': [rawEquinoxBonusLevelsList[2], 5],
        'Equinox Resources': [rawEquinoxBonusLevelsList[3], 4],
        'Shades of K': [rawEquinoxBonusLevelsList[4], 3],
        'Liquidvestment': [rawEquinoxBonusLevelsList[5], 11],
        'Matching Scims': [rawEquinoxBonusLevelsList[6], 23],
        'Slow Roast Wiz': [rawEquinoxBonusLevelsList[7], 5],
        'Laboratory Fuse': [rawEquinoxBonusLevelsList[8], 10],
        'Metal Detector': [rawEquinoxBonusLevelsList[9], 6],
        'Faux Jewels': [rawEquinoxBonusLevelsList[10], 21],
        'Food Lust': [rawEquinoxBonusLevelsList[11], 14],
        'Equinox Symbols': [rawEquinoxBonusLevelsList[12], 9],
    }
    totalRecommendedUpgrades = 0
    totalOptionalUpgrades = 0
    totalMaxUpgrades = 0
    for upgradeName, valueList in equinoxBonusLevelsDict.items():
        if upgradeName in optionalUpgradeList:
            totalOptionalUpgrades += valueList[0]
        else:
            totalRecommendedUpgrades += valueList[0]
        totalMaxUpgrades += valueList[1]
    equinoxBonusLevelsDict["TotalUpgrades"] = [totalRecommendedUpgrades, totalOptionalUpgrades, totalMaxUpgrades]

    rawEquinoxDreamsDict = json.loads(session_data.account.raw_data.get("WeeklyBoss", "{}"))

    dreams_statuses = [True]
    dreams_statuses += [
        float(rawEquinoxDreamsDict.get(f'd_{i}', 0)) == -1
        for i in range(consts.maxDreams)
    ]
    return [equinoxBonusLevelsDict, dreams_statuses]


def setEquinoxUpgradeMaxLevels(equinoxDreamsDict, recommendedBonusOrderDict):
    if equinoxDreamsDict[7]:
        recommendedBonusOrderDict["Liquidvestment"] += 3
    if equinoxDreamsDict[13]:
        recommendedBonusOrderDict["Matching Scims"] += 5
    if equinoxDreamsDict[16]:
        recommendedBonusOrderDict["Liquidvestment"] += 4
    if equinoxDreamsDict[19]:
        recommendedBonusOrderDict["Matching Scims"] += 10
    if equinoxDreamsDict[22]:
        recommendedBonusOrderDict["Faux Jewels"] += 5
    if equinoxDreamsDict[26]:
        recommendedBonusOrderDict["Food Lust"] += 4
    if equinoxDreamsDict[27]:
        recommendedBonusOrderDict["Faux Jewels"] += 10
    if equinoxDreamsDict[31]:
        recommendedBonusOrderDict["Equinox Symbols"] += 4


def setEquinoxProgressionTier():
    equinox_AdviceDict = {
        "DreamsCompleted": [],
        "TotalUpgrades": {},
    }
    equinox_AdviceGroupDict = {}
    equinox_AdviceSection = AdviceSection(
        name="Equinox",
        tier="Not Yet Evaluated",
        header="Best Equinox tier met: Not Yet Evaluated",
        picture="Equinox_Valley_Mirror.gif"
    )
    # highestEquinoxSkillLevel = max(session_data.account.all_skills["EquinoxSkill"])
    # if highestEquinoxSkillLevel < 1:
    #     equinox_AdviceSection.header = "Come back after unlocking Equinox!"
    #     return equinox_AdviceSection

    playerEquinoxBonusLevelsDict, playerEquinoxDreams = getRawEquinoxValues()
    totalDreamsCompleted = sum(playerEquinoxDreams)
    tier_TotalDreamsCompleted = 0
    tier_TotalEquinoxUpgrades = 0
    max_tier = max(equinox_progressionTiers.keys())
    maxRecommendedUpgradeLevelDict = {
        'Equinox Dreams': 5,
        'Equinox Resources': 4,
        'Liquidvestment': 11,
        'Matching Scims': 23,
        'Slow Roast Wiz': 5,
        'Metal Detector': 6,
        'Faux Jewels': 21,
        'Food Lust': 14,
        'Equinox Symbols': 9,
    }
    maxIgnorableUpgradeLevelDict = {
        'Shades of K': 3,
        'Laboratory Fuse': 10,
    }
    recommendedBonusOrderDict = {
        'Equinox Symbols': 5,
        'Equinox Resources': 4,
        'Metal Detector': 6,
        'Slow Roast Wiz': 5,
        'Liquidvestment': 4,
        'Faux Jewels': 6,
        'Matching Scims': 8,
        'Food Lust': 10,
        'Equinox Dreams': 5,
    }
    optionalBonusOrderDict = {
        'Shades of K': 3,
        'Laboratory Fuse': 10,
    }
    setEquinoxUpgradeMaxLevels(playerEquinoxDreams, recommendedBonusOrderDict)
    recommendedBonusUnlockedDict = {
        'Equinox Dreams': playerEquinoxDreams[0],
        'Equinox Resources': playerEquinoxDreams[1],
        'Shades of K': playerEquinoxDreams[3],
        'Liquidvestment': playerEquinoxDreams[6],
        'Matching Scims': playerEquinoxDreams[8],
        'Slow Roast Wiz': playerEquinoxDreams[11],
        'Laboratory Fuse': playerEquinoxDreams[14],
        'Metal Detector': playerEquinoxDreams[18],
        'Faux Jewels': playerEquinoxDreams[21],
        'Food Lust': playerEquinoxDreams[24],
        'Equinox Symbols': playerEquinoxDreams[29],
    }
    recommendedBonusTotal = sum(list(maxRecommendedUpgradeLevelDict.values()))
    optionalBonusTotal = sum(list(maxIgnorableUpgradeLevelDict.values()))
    currentMaxBonusTotal = recommendedBonusTotal + optionalBonusTotal
    playerBonusTotal = playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0,0])[0] + playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0,0])[1]

    for tier, (dream_number, label) in equinox_progressionTiers.items():
        #Total Dreams Completed
        if playerEquinoxDreams[dream_number] == True:  #If the player has this dream completed
            tier_TotalDreamsCompleted = tier
        else:
            equinox_AdviceDict["DreamsCompleted"].append(Advice(
                label=label,
                picture_class=label[7:],
                goal=f"Dream {dream_number}"
            ))

    # Upgrades Purchased
    if playerBonusTotal < recommendedBonusTotal:
        
        # equinox_AdviceDict["TotalUpgrades"][f"{playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0])[0]}/{recommendedBonusTotal}"].append(Advice(
        #     label="Total Recommended Upgrades Purchased",
        #     picture_class="equinox",
        #     progression=playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0])[0],
        #     goal=recommendedBonusTotal
        # ))
        subgroupName = f"Recommended {playerEquinoxBonusLevelsDict.get('TotalUpgrades', [0, 0, 0])[0]}/{recommendedBonusTotal}"
        if subgroupName not in equinox_AdviceDict["TotalUpgrades"]:
            equinox_AdviceDict["TotalUpgrades"][subgroupName] = []
        for bonusName, bonusMaxLevel in recommendedBonusOrderDict.items():
            if playerEquinoxBonusLevelsDict.get(bonusName, [0,0])[0] < bonusMaxLevel\
            and recommendedBonusUnlockedDict.get(bonusName, False) == True:
                equinox_AdviceDict["TotalUpgrades"][subgroupName].append(Advice(
                    label=bonusName,
                    picture_class=bonusName,
                    progression=playerEquinoxBonusLevelsDict.get(bonusName, [0,0])[0],
                    goal=recommendedBonusOrderDict.get(bonusName, 0)
                ))
        if len(equinox_AdviceDict["TotalUpgrades"][subgroupName]) == 0:
            equinox_AdviceDict["TotalUpgrades"][subgroupName].append(Advice(
                label="Nothing good available :( Maybe wait for future unlocks!",
                picture_class="",
            ))
        for bonusName, bonusMaxLevel in optionalBonusOrderDict.items():
            if playerEquinoxBonusLevelsDict.get(bonusName, [0,0])[0] < bonusMaxLevel\
            and recommendedBonusUnlockedDict.get(bonusName, False) == True:
                subgroupName = f"Optional {playerEquinoxBonusLevelsDict.get('TotalUpgrades', [0, 0,0])[1]}/{optionalBonusTotal}"
                if subgroupName not in equinox_AdviceDict["TotalUpgrades"]:
                    equinox_AdviceDict["TotalUpgrades"][subgroupName] = []
                equinox_AdviceDict["TotalUpgrades"][subgroupName].append(Advice(
                    label=bonusName,
                    picture_class=bonusName,
                    progression=playerEquinoxBonusLevelsDict.get(bonusName, [0,0])[0],
                    goal=optionalBonusOrderDict.get(bonusName, 0)
                ))

    #Generate AdviceGroups
    equinox_AdviceGroupDict["DreamsCompleted"] = AdviceGroup(
        tier=str(tier_TotalDreamsCompleted),
        pre_string=f"Complete {pl(max_tier-tier_TotalDreamsCompleted, 'the final Equinox goal', 'more Equinox goals')}",
        advices=equinox_AdviceDict.get("DreamsCompleted", []),
        post_string=""
    )

    equinox_AdviceGroupDict["BonusUpgrades"] = AdviceGroup(
        tier="",
        pre_string="Upgrade more Equinox Bonuses",
        advices=equinox_AdviceDict.get("TotalUpgrades", []),
        post_string=""
    )

    #Generate AdviceSection

    overall_EquinoxTier = min(max_tier, tier_TotalDreamsCompleted)
    tier_section = f"{overall_EquinoxTier}/{max_tier}"
    equinox_AdviceSection.tier = tier_section
    equinox_AdviceSection.pinchy_rating = overall_EquinoxTier
    equinox_AdviceSection.groups = equinox_AdviceGroupDict.values()
    if overall_EquinoxTier == max_tier:
        equinox_AdviceSection.header = f"Best Equinox tier met: {tier_section}<br>You best ❤️"
    else:
        equinox_AdviceSection.header = f"Best Equinox tier met: {tier_section}"

    return equinox_AdviceSection
