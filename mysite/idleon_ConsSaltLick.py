import json
from consts import getSpecificSkillLevelsList
from models import AdviceSection, AdviceGroup, Advice
from utils import pl

def parseConsSaltLick(inputJSON):
    saltLickList = json.loads(inputJSON["SaltLick"])
    saltLickDict = {
        'Printer Sample Size':saltLickList[0],
        'Obol Storage':saltLickList[1],
        'Refinery Speed':saltLickList[2],
        'EXP':saltLickList[3],
        'Max Book':saltLickList[4],
        'Alchemy Liquids':saltLickList[5],
        'TD Points':saltLickList[6],
        'Movespeed':saltLickList[7],
        'Multikill':saltLickList[8],
        'Damage':saltLickList[9]
        #'Tab3-1':saltLickList[10] #Not Yet Implemented
        #'Tab3-2':saltLickList[11] #Not Yet Implemented
        #'Tab3-3':saltLickList[12] #Not Yet Implemented
        #'Tab3-4':saltLickList[13] #Not Yet Implemented
        #'Tab3-5':saltLickList[14] #Not Yet Implemented
        #'Tab4-1':saltLickList[15] #Not Yet Implemented
        #'Tab4-2':saltLickList[16] #Not Yet Implemented
        #'Tab4-3':saltLickList[17] #Not Yet Implemented
        #'Tab4-4':saltLickList[18] #Not Yet Implemented
        #'Tab4-5':saltLickList[19] #Not Yet Implemented
        }
    #print(saltLickDict)
    return saltLickDict

def setConsSaltLickProgressionTier(inputJSON, progressionTiers, characterDict) -> AdviceSection:
    saltlick_AdviceDict = {
        "UnmaxedUpgrades": []
    }
    saltlick_AdviceGroupDict = {}
    saltlick_AdviceSection = AdviceSection(
        name="Salt Lick",
        tier="Not Yet Evaluated",
        header="Best Salt Lick tier met: Not Yet Evaluated. Recommended salt lick actions:",
        picture="Construction_Salt_Lick.png",
    )
    constructionLevelsList = getSpecificSkillLevelsList(inputJSON, len(characterDict), "Construction")
    if max(constructionLevelsList) < 1:
        saltlick_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return saltlick_AdviceSection
    elif json.loads(inputJSON["Tower"])[3] < 1:
        saltlick_AdviceSection.header = "Come back after unlocking the Salt Lick within the Construction skill in World 3!"
        return saltlick_AdviceSection

    max_tier = progressionTiers[-1][0]
    tier_RequiredSaltLickUpgrades = 0
    sum_TotalMaxedSaltLickUpgrades = 0
    overall_ConsSaltLickTier = 0
    saltLickDict = parseConsSaltLick(inputJSON)

    #Assess tiers
    for tier in progressionTiers:
        #tier[0] = int tier,
        #tier[1] = dict RequiredSaltLickUpgrades,
        #tier[2] = str Notes
        for key in tier[1].keys():
            if saltLickDict[key] < tier[1][key]:
                saltlick_AdviceDict["UnmaxedUpgrades"].append(
                    Advice(label=key, picture_class=tier[2], progression=saltLickDict[key], goal=tier[1][key])
                    )
            else:
                sum_TotalMaxedSaltLickUpgrades += 1
                if len(saltlick_AdviceDict["UnmaxedUpgrades"]) == 0:
                    tier_RequiredSaltLickUpgrades = tier[0]

    # Generate AdviceGroups
    saltlick_AdviceGroupDict["UnmaxedUpgrades"] = AdviceGroup(
        tier=tier_RequiredSaltLickUpgrades,
        pre_string=f"{pl(saltlick_AdviceDict['UnmaxedUpgrades'], 'Final Upgrade', 'Remaining Upgrades')} to max",
        advices=saltlick_AdviceDict['UnmaxedUpgrades'],
        post_string=f"{pl(saltlick_AdviceDict['UnmaxedUpgrades'], '', 'Shown upgrades are in Tier order.')}"
    )

    # Generate AdviceSection
    overall_ConsSaltLickTier = min(max_tier, tier_RequiredSaltLickUpgrades)  #Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_ConsSaltLickTier}/{max_tier}"
    saltlick_AdviceSection.tier = tier_section
    saltlick_AdviceSection.pinchy_rating = overall_ConsSaltLickTier
    saltlick_AdviceSection.groups = saltlick_AdviceGroupDict.values()
    if overall_ConsSaltLickTier == max_tier:
        saltlick_AdviceSection.header = f"Best Salt Lick tier met: {tier_section}<br>You best ❤️"
    else:
        saltlick_AdviceSection.header = f"Best Salt Lick tier met: {tier_section}"
    return saltlick_AdviceSection
