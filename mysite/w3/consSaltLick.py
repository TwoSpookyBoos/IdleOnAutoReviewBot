from consts import saltLick_progressionTiers, break_you_best
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    saltlick_AdviceDict = {
        "UnmaxedUpgrades": []
    }
    info_tiers = 0
    max_tier = saltLick_progressionTiers[-1][0] - info_tiers
    sum_TotalMaxedSaltLickUpgrades = 0
    saltLickDict = session_data.account.saltlick

    # Assess tiers
    for tier in saltLick_progressionTiers:
        # tier[0] = int tier,
        # tier[1] = dict RequiredSaltLickUpgrades,
        # tier[2] = str Notes
        for key in tier[1].keys():
            if saltLickDict[key] < tier[1][key]:
                saltlick_AdviceDict["UnmaxedUpgrades"].append(
                    Advice(label=key, picture_class=tier[2], progression=saltLickDict[key], goal=tier[1][key])
                )
            else:
                sum_TotalMaxedSaltLickUpgrades += 1

    tier_RequiredSaltLickUpgrades = sum_TotalMaxedSaltLickUpgrades

    # Generate AdviceGroups
    tiers_ag = AdviceGroup(
        tier=str(tier_RequiredSaltLickUpgrades),
        pre_string=f"{pl(saltlick_AdviceDict['UnmaxedUpgrades'], 'Final Upgrade', 'Remaining Upgrades')} to max",
        advices=saltlick_AdviceDict['UnmaxedUpgrades'],
        post_string=f"{pl(saltlick_AdviceDict['UnmaxedUpgrades'], '', 'Shown upgrades are in Tier order.')}"
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_RequiredSaltLickUpgrades)
    return tiers_ag, overall_SectionTier, max_tier

def getSaltLickAdviceSection() -> AdviceSection:
    #highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if session_data.account.construction_buildings['Salt Lick']['Level'] < 1:
        saltlick_AdviceSection = AdviceSection(
            name="Salt Lick",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Salt Lick within the Construction skill in World 3!",
            picture="Construction_Salt_Lick.gif",
            unreached=True
        )
        return saltlick_AdviceSection

    #Generate AdviceGroup
    saltlick_AdviceGroupDict = {}
    saltlick_AdviceGroupDict["UnmaxedUpgrades"], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    saltlick_AdviceSection = AdviceSection(
        name="Salt Lick",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Salt Lick tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Construction_Salt_Lick.gif",
        groups=saltlick_AdviceGroupDict.values()
    )
    return saltlick_AdviceSection
