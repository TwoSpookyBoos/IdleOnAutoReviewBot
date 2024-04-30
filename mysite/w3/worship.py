import json
from models.models import AdviceSection, AdviceGroup, Advice
from consts import maxTiersPerGroup, prayers_progressionTiers, prayersList
from flask import g as session_data
from utils.text_formatting import pl
from utils.data_formatting import safe_loads
from utils.logging import get_logger


logger = get_logger(__name__)

def getPrayerImage(inputValue: str | int) -> str:
    match inputValue:
        case 0 | "Big Brain Time (Forest Soul)":
            return "big-brain-time"
        case 1 | "Skilled Dimwit (Forest Soul)":
            return "skilled-dimwit"
        case 2 | "Unending Energy (Forest Soul)":
            return "unending-energy"
        case 3 | "Shiny Snitch (Forest Soul)":
            return "shiny-snitch"
        case 4 | "Zerg Rushogen (Forest Soul)":
            return "zerg-rushogen"
        case 5 | "Tachion of the Titans (Dune Soul)":
            return "tachion-of-the-titans"
        case 6 | "Balance of Precision (Dune Soul)":
            return "balance-of-precision"
        case 7 | "Midas Minded (Dune Soul)":
            return "midas-minded"
        case 8 | "Jawbreaker (Dune Soul)":
            return "jawbreaker"
        case 9 | "The Royal Sampler (Rooted Soul)":
            return "the-royal-sampler"
        case 10 | "Antifun Spirit (Rooted Soul)":
            return "antifun-spirit"
        case 11 | "Circular Criticals (Rooted Soul)":
            return "circular-criticals"
        case 12 | "Ruck Sack (Rooted Soul)":
            return "ruck-sack"
        case 13 | "Fibers of Absence (Frigid Soul)":
            return "fibers-of-absence"
        case 14 | "Vacuous Tissue (Frigid Soul)":
            return "vacuous-tissue"
        case 15 | "Beefy For Real (Frigid Soul)":
            return "beefy-for-real"
        case 16 | "Balance of Pain (Squishy Soul)":
            return "balance-of-pain"
        case 17 | "Balance of Proficiency (Squishy Soul)":
            return "balance-of-proficiency"
        case 18 | "Glitterbug (Squishy Soul)":
            return "glitterbug"
        case _:
            return "Unknown-Prayer"

def getPrayerMaterialImage(inputValue: str | int) -> str:
    match inputValue:
        case 0 | "Big Brain Time (Forest Soul)" | 1 | "Skilled Dimwit (Forest Soul)" | 2 | "Unending Energy (Forest Soul)" | 3 | "Shiny Snitch (Forest Soul)" | 4 | "Zerg Rushogen (Forest Soul)":
            return "forest-soul"
        case 5 | "Tachion of the Titans (Dune Soul)" | 6 | "Balance of Precision (Dune Soul)" | 7 | "Midas Minded (Dune Soul)" | 8 | "Jawbreaker (Dune Soul)":
            return "dune-soul"
        case 9 | "The Royal Sampler (Rooted Soul)" | 10 | "Antifun Spirit (Rooted Soul)" | 11 | "Circular Criticals (Rooted Soul)" | 12 | "Ruck Sack (Rooted Soul)":
            return "rooted-soul"
        case 13 | "Fibers of Absence (Frigid Soul)" | 14 | "Vacuous Tissue (Frigid Soul)" | 15 | "Beefy For Real (Frigid Soul)":
            return "frigid-soul"
        case 16 | "Balance of Pain (Squishy Soul)" | 17 | "Balance of Proficiency (Squishy Soul)" | 18 | "Glitterbug (Squishy Soul)":
            return "squishy-soul"
        case _:
            return "Unknown-Material"

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
            if worshipPrayersDict[requiredPrayer] < tier[1][requiredPrayer]:
                allPrayersLeveled = False
                subgroupName = f"To reach Tier {tier[0]}"
                if subgroupName not in prayers_AdviceDict["Recommended"] and len(prayers_AdviceDict["Recommended"]) < maxTiersPerGroup:
                    prayers_AdviceDict["Recommended"][subgroupName] = []
                if subgroupName in prayers_AdviceDict["Recommended"]:
                    adviceCountsDict["Recommended"] += 1
                    prayers_AdviceDict["Recommended"][subgroupName].append(
                        Advice(
                            label=requiredPrayer,
                            picture_class=getPrayerImage(requiredPrayer),
                            progression=str(worshipPrayersDict[requiredPrayer]),
                            goal=str(tier[1][requiredPrayer]))
                    )
        if tier_WorshipPrayers == (tier[0] - 1) and allPrayersLeveled == True:  # Only update if they already met the previous tier
            tier_WorshipPrayers = tier[0]

    #Check Optional Prayers
    optionalTierPrayers = prayers_progressionTiers[-2][1]
    for optionalPrayer in optionalTierPrayers:
        if worshipPrayersDict[optionalPrayer] < optionalTierPrayers[optionalPrayer]:
            prayers_AdviceDict["Optional"].append(
                Advice(
                    label=optionalPrayer,
                    picture_class=getPrayerImage(optionalPrayer),
                    progression=str(worshipPrayersDict[optionalPrayer]),
                    goal=str(optionalTierPrayers[optionalPrayer]))
                )

    #Check Ignorable Prayers
    ignorableTierPrayers = prayers_progressionTiers[-1][1]
    for ignorablePrayer in ignorableTierPrayers:
        if worshipPrayersDict[ignorablePrayer] < ignorableTierPrayers[ignorablePrayer]:
            prayers_AdviceDict["Ignorable"].append(
                Advice(
                    label=ignorablePrayer,
                    picture_class=getPrayerImage(ignorablePrayer),
                    progression=str(worshipPrayersDict[ignorablePrayer]),
                    goal=str(ignorableTierPrayers[ignorablePrayer]))
                )

#Generate Advice Groups
    recommended_post_string_list = [
        "Royal Sampler is an oddity. The Printer Sample Rate bonus it gives is fantastic, but a few levels (5-10) is usually enough to help you reach the 90% maximum.",
        "Level 20 is half the maximum value for Skilled Dimwit.Rush this ASAP after all characters have Ceramic Skulls or better equipped.",
        "Level 11 is half the maximum value for Balance of Pain. This prayer is crucial for farming Death Note and improving your 3D Printer samples of Monster materials.",
        "This tier is roughly 75% of max prayer value for Skilled Dimwit and Balance of Pain.",
        "This tier is roughly 50% max value for Midas. This prayer is great to use when you start farming older content, like Crystal Mobs for statues.",
        "These are the best Prayer from each Totem/Soul type and are worth maxing first.",
        "These are the last group of important prayers to max.",
        ""
    ]
    prayers_AdviceGroupDict['Recommended'] = AdviceGroup(
        tier=tier_WorshipPrayers,
        pre_string=f"Recommended Prayer{pl([''] * adviceCountsDict['Recommended'])}",
        advices=prayers_AdviceDict['Recommended'],
        post_string="",  #recommended_post_string_list[tier_WorshipPrayers],
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
        post_string="Prayers in this group should still be unlocked, but can stay at level 1 after that as of v2.03.",
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
