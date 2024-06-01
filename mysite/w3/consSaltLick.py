from consts import saltLick_progressionTiers
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl

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
    elif session_data.account.construction_buildings.get("Salt Lick", 0) < 1:
        saltlick_AdviceSection.header = "Come back after unlocking the Salt Lick within the Construction skill in World 3!"
        return saltlick_AdviceSection

    max_tier = saltLick_progressionTiers[-1][0]
    tier_RequiredSaltLickUpgrades = 0
    sum_TotalMaxedSaltLickUpgrades = 0
    overall_ConsSaltLickTier = 0
    saltLickDict = session_data.account.saltlick

    #Assess tiers
    for tier in saltLick_progressionTiers:
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
