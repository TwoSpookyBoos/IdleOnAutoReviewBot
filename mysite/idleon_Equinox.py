import json
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, equinox_progressionTiers

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
    equinoxDreamsDict = {
        0: True,
        1: rawEquinoxDreamsDict.get('d_0', 0) == -1,
        2: rawEquinoxDreamsDict.get('d_1', 0) == -1,
        3: rawEquinoxDreamsDict.get('d_2', 0) == -1,
        4: rawEquinoxDreamsDict.get('d_3', 0) == -1,
        5: rawEquinoxDreamsDict.get('d_4', 0) == -1,
        6: rawEquinoxDreamsDict.get('d_5', 0) == -1,
        7: rawEquinoxDreamsDict.get('d_6', 0) == -1,
        8: rawEquinoxDreamsDict.get('d_7', 0) == -1,
        9: rawEquinoxDreamsDict.get('d_8', 0) == -1,
        10: rawEquinoxDreamsDict.get('d_9', 0) == -1,
        11: rawEquinoxDreamsDict.get('d_10', 0) == -1,
        12: rawEquinoxDreamsDict.get('d_11', 0) == -1,
        13: rawEquinoxDreamsDict.get('d_12', 0) == -1,
        14: rawEquinoxDreamsDict.get('d_13', 0) == -1,
        15: rawEquinoxDreamsDict.get('d_14', 0) == -1,
        16: rawEquinoxDreamsDict.get('d_15', 0) == -1,
        17: rawEquinoxDreamsDict.get('d_16', 0) == -1,
        18: rawEquinoxDreamsDict.get('d_17', 0) == -1,
        19: rawEquinoxDreamsDict.get('d_18', 0) == -1,
        20: rawEquinoxDreamsDict.get('d_19', 0) == -1,
        21: rawEquinoxDreamsDict.get('d_20', 0) == -1,
        22: rawEquinoxDreamsDict.get('d_21', 0) == -1,
        23: rawEquinoxDreamsDict.get('d_22', 0) == -1,
        24: rawEquinoxDreamsDict.get('d_23', 0) == -1,
        25: rawEquinoxDreamsDict.get('d_24', 0) == -1,
        26: rawEquinoxDreamsDict.get('d_25', 0) == -1,
        27: rawEquinoxDreamsDict.get('d_26', 0) == -1,
        28: rawEquinoxDreamsDict.get('d_27', 0) == -1,
        29: rawEquinoxDreamsDict.get('d_28', 0) == -1,
        30: rawEquinoxDreamsDict.get('d_29', 0) == -1,
        31: rawEquinoxDreamsDict.get('d_30', 0) == -1,
    }
    equinoxDreamsDict["TotalCompleted"] = list(equinoxDreamsDict.values()).count(True)
    return [equinoxBonusLevelsDict, equinoxDreamsDict]

def setEquinoxUpgradeMaxLevels(equinoxDreamsDict, recommendedBonusOrderDict):
    if equinoxDreamsDict.get(7, False):
        recommendedBonusOrderDict["Liquidvestment"] += 3
    if equinoxDreamsDict.get(13, False):
        recommendedBonusOrderDict["Matching Scims"] += 5
    if equinoxDreamsDict.get(16, False):
        recommendedBonusOrderDict["Liquidvestment"] += 4
    if equinoxDreamsDict.get(19, False):
        recommendedBonusOrderDict["Matching Scims"] += 10
    if equinoxDreamsDict.get(22, False):
        recommendedBonusOrderDict["Faux Jewels"] += 5
    if equinoxDreamsDict.get(26, False):
        recommendedBonusOrderDict["Food Lust"] += 4
    if equinoxDreamsDict.get(27, False):
        recommendedBonusOrderDict["Faux Jewels"] += 10
    if equinoxDreamsDict.get(31, False):
        recommendedBonusOrderDict["Equinox Symbols"] += 4
    return

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

    playerEquinoxBonusLevelsDict, playerEquinoxDreamsDict = getRawEquinoxValues()
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
    setEquinoxUpgradeMaxLevels(playerEquinoxDreamsDict, recommendedBonusOrderDict)
    recommendedBonusUnlockedDict = {
        'Equinox Dreams': True,
        'Equinox Resources': playerEquinoxDreamsDict.get(1, False),
        'Shades of K': playerEquinoxDreamsDict.get(3, False),
        'Liquidvestment': playerEquinoxDreamsDict.get(6, False),
        'Matching Scims': playerEquinoxDreamsDict.get(8, False),
        'Slow Roast Wiz': playerEquinoxDreamsDict.get(11, False),
        'Laboratory Fuse': playerEquinoxDreamsDict.get(14, False),
        'Metal Detector': playerEquinoxDreamsDict.get(18, False),
        'Faux Jewels': playerEquinoxDreamsDict.get(21, False),
        'Food Lust': playerEquinoxDreamsDict.get(24, False),
        'Equinox Symbols': playerEquinoxDreamsDict.get(29, False),
    }
    recommendedBonusTotal = sum(list(maxRecommendedUpgradeLevelDict.values()))
    optionalBonusTotal = sum(list(maxIgnorableUpgradeLevelDict.values()))
    currentMaxBonusTotal = recommendedBonusTotal + optionalBonusTotal
    playerBonusTotal = playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0,0])[0] + playerEquinoxBonusLevelsDict.get("TotalUpgrades", [0,0,0])[1]

    for tier, requiredDreamCompleted in equinox_progressionTiers.items():
        #Total Dreams Completed
        if playerEquinoxDreamsDict.get(requiredDreamCompleted[0], 0) == True:  #If the player has this dream completed
            tier_TotalDreamsCompleted = tier
        else:
            equinox_AdviceDict["DreamsCompleted"].append(Advice(
                label=requiredDreamCompleted[1],
                picture_class=requiredDreamCompleted[1][7:],
                goal=f"Dream {requiredDreamCompleted[0]}"
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
