import json
from consts import progressionTiers
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl

def parseConsSaltLick():
    saltLickList = json.loads(session_data.account.raw_data["SaltLick"])
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
    return saltLickDict

def setConsSaltLickProgressionTier() -> AdviceSection:
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
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        saltlick_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return saltlick_AdviceSection
    elif json.loads(session_data.account.raw_data["Tower"])[3] < 1:
        saltlick_AdviceSection.header = "Come back after unlocking the Salt Lick within the Construction skill in World 3!"
        return saltlick_AdviceSection

    max_tier = progressionTiers["Construction Salt Lick"][-1][0]
    tier_RequiredSaltLickUpgrades = 0
    sum_TotalMaxedSaltLickUpgrades = 0
    overall_ConsSaltLickTier = 0
    saltLickDict = parseConsSaltLick()

    #Assess tiers
    for tier in progressionTiers["Construction Salt Lick"]:
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

    tier_RequiredSaltLickUpgrades = sum_TotalMaxedSaltLickUpgrades

    # Generate AdviceGroups
    saltlick_AdviceGroupDict["UnmaxedUpgrades"] = AdviceGroup(
        tier=str(tier_RequiredSaltLickUpgrades),
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
