from models.models import AdviceSection, AdviceGroup, Advice
from consts import maxTiersPerGroup, prayers_progressionTiers
from flask import g as session_data
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def setWorshipPrayersProgressionTier() -> AdviceSection:
    worshipPrayersDict = session_data.account.prayers
    max_tier = prayers_progressionTiers[-3][0]  # Final tier is ignorable, second to final is optional
    tier_WorshipPrayers = 0
    overall_WorshipPrayersTier = 0

    prayers_AdviceDict = {
        "Recommended": {},
        "Optional": [],
        "Ignorable": []
    }
    prayers_AdviceGroupDict = {}
    prayers_AdviceSection = AdviceSection(
        name="Prayers",
        tier="Not Yet Evaluated",
        header="Best Prayers tier met: Not Yet Evaluated. Recommended prayer actions:",
        picture="Prayer_Stone.gif"
    )
    highestWorshipLevel = max(session_data.account.all_skills["Worship"])
    if highestWorshipLevel < 1:
        prayers_AdviceSection.header = "Come back after unlocking the Worship skill in World 3!"
        return prayers_AdviceSection

    adviceCountsDict = {"Recommended": 0, "Optional": 0, "Ignorable": 0}

    #Check Recommended Prayers
    for tier in prayers_progressionTiers[:-2]:
        #tier[0] = int Tier
        #tier[1] = dict requiredPrayersDict
        #tier[2] = str Notes
        allPrayersLeveled = True
        for requiredPrayer in tier[1]:
            if worshipPrayersDict[requiredPrayer]['Level'] < tier[1][requiredPrayer]:
                allPrayersLeveled = False
                subgroupName = f"To reach Tier {tier[0]}"
                if subgroupName not in prayers_AdviceDict["Recommended"] and len(prayers_AdviceDict["Recommended"]) < maxTiersPerGroup:
                    prayers_AdviceDict["Recommended"][subgroupName] = []
                if subgroupName in prayers_AdviceDict["Recommended"]:
                    adviceCountsDict["Recommended"] += 1
                    prayers_AdviceDict["Recommended"][subgroupName].append(
                        Advice(
                            label=worshipPrayersDict[requiredPrayer]['DisplayName'],
                            picture_class=requiredPrayer,
                            progression=str(worshipPrayersDict[requiredPrayer]['Level']),
                            goal=str(tier[1][requiredPrayer]))
                    )
        if tier_WorshipPrayers == (tier[0] - 1) and allPrayersLeveled == True:  # Only update if they already met the previous tier
            tier_WorshipPrayers = tier[0]

    #Check Optional Prayers
    optionalTierPrayers = prayers_progressionTiers[-2][1]
    for optionalPrayer in optionalTierPrayers:
        if worshipPrayersDict[optionalPrayer]['Level'] < optionalTierPrayers[optionalPrayer]:
            prayers_AdviceDict["Optional"].append(
                Advice(
                    label=optionalPrayer,
                    picture_class=optionalPrayer,
                    progression=str(worshipPrayersDict[optionalPrayer]['Level']),
                    goal=str(optionalTierPrayers[optionalPrayer]))
                )

    #Check Ignorable Prayers
    ignorableTierPrayers = prayers_progressionTiers[-1][1]
    for ignorablePrayer in ignorableTierPrayers:
        if worshipPrayersDict[ignorablePrayer]['Level'] < ignorableTierPrayers[ignorablePrayer]:
            prayers_AdviceDict["Ignorable"].append(
                Advice(
                    label=ignorablePrayer,
                    picture_class=ignorablePrayer,
                    progression=str(worshipPrayersDict[ignorablePrayer]['Level']),
                    goal=str(ignorableTierPrayers[ignorablePrayer]))
                )

#Generate Advice Groups
    prayers_AdviceGroupDict['Recommended'] = AdviceGroup(
        tier=tier_WorshipPrayers,
        pre_string=f"Recommended Prayer{pl([''] * adviceCountsDict['Recommended'])}",
        advices=prayers_AdviceDict['Recommended'],
        post_string="",
    )
    prayers_AdviceGroupDict['Optional'] = AdviceGroup(
        tier="",
        pre_string=f"Situational Prayer{pl(prayers_AdviceDict['Optional'])} you may consider levelling",
        advices=prayers_AdviceDict['Optional'],
        post_string="These are niche use prayers. They have different benefits/purposes at low level and high levels",
    )
    prayers_AdviceGroupDict['Ignorable'] = AdviceGroup(
        tier="",
        pre_string=f"Ignorable Prayer{pl(prayers_AdviceDict['Ignorable'])}",
        advices=prayers_AdviceDict['Ignorable'],
        post_string="Prayers in this group should still be unlocked, but can stay at level 1 after that as of v2.10.",
    )

    #Generate Advice Section
    overall_WorshipPrayersTier = min(max_tier, tier_WorshipPrayers)
    tier_section = f"{overall_WorshipPrayersTier}/{max_tier}"
    prayers_AdviceSection.pinchy_rating = overall_WorshipPrayersTier
    prayers_AdviceSection.tier = tier_section
    prayers_AdviceSection.groups = prayers_AdviceGroupDict.values()
    if overall_WorshipPrayersTier == max_tier:
        prayers_AdviceSection.header = f"Best Prayer tier met: {tier_section}<br>You best ❤️"
    else:
        prayers_AdviceSection.header = f"Best Prayer tier met: {tier_section}"
    return prayers_AdviceSection
