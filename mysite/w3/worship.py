from models.models import AdviceSection, AdviceGroup, Advice
from consts import prayers_progressionTiers, break_you_best, optional_prayers, ignorable_prayers
from flask import g as session_data
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def get_antifun_spirit_next_level_cost(current_prayer_level: int) -> int:
    max_cost = round(9 + (optional_prayers['Antifun Spirit'] * .9))  #Max level
    if current_prayer_level >= optional_prayers['Antifun Spirit']:
        return max_cost
    else:
        result = round(9 + (current_prayer_level+1 * .9))
        return result

def setPrayersProgressionTierAdviceGroup():
    prayers_AdviceDict = {
        "Recommended": {},
        "Optional": [],
        "Ignorable": []
    }
    prayers_AdviceGroupDict = {}
    worshipPrayersDict = session_data.account.prayers
    info_tiers = 0
    max_tier = prayers_progressionTiers[-1][0] - info_tiers  # Final tier is ignorable, second to final is optional
    tier_WorshipPrayers = 0
    adviceCountsDict = {"Recommended": 0, "Optional": 0, "Ignorable": 0}

    # Check Recommended Prayers
    for tier in prayers_progressionTiers:
        # tier[0] = int Tier
        # tier[1] = dict requiredPrayersDict
        # tier[2] = str Notes
        allPrayersLeveled = True
        for requiredPrayer in tier[1]:
            if worshipPrayersDict[requiredPrayer]['Level'] < tier[1][requiredPrayer]:
                allPrayersLeveled = False
                subgroupName = f"To reach Tier {tier[0]}"
                if subgroupName not in prayers_AdviceDict["Recommended"] and len(prayers_AdviceDict["Recommended"]) < session_data.account.maxSubgroupsPerGroup:
                    prayers_AdviceDict["Recommended"][subgroupName] = []
                if subgroupName in prayers_AdviceDict["Recommended"]:
                    adviceCountsDict["Recommended"] += 1
                    prayers_AdviceDict["Recommended"][subgroupName].append(
                        Advice(
                            label=requiredPrayer,
                            picture_class=requiredPrayer,
                            progression=str(worshipPrayersDict[requiredPrayer]['Level']),
                            goal=str(tier[1][requiredPrayer]),
                            resource=worshipPrayersDict[requiredPrayer]['Material']
                        ))
        if tier_WorshipPrayers == (tier[0] - 1) and allPrayersLeveled == True:  # Only update if they already met the previous tier
            tier_WorshipPrayers = tier[0]

    # Check Optional Prayers
    next_antifun_cost = get_antifun_spirit_next_level_cost(worshipPrayersDict['Antifun Spirit']['Level'])
    for optionalPrayer in optional_prayers:
        if worshipPrayersDict[optionalPrayer]['Level'] < optional_prayers[optionalPrayer]:
            if (
                optionalPrayer == 'Antifun Spirit'
                and session_data.account.minigame_plays_daily < next_antifun_cost
            ):
                #logger.debug(f"Skipping Antifun Spirit because next level costs {next_antifun_cost} while player has {session_data.account.minigame_plays_daily} daily minigame plays")
                continue
            else:
                prayers_AdviceDict["Optional"].append(
                    Advice(
                        label=optionalPrayer,
                        picture_class=optionalPrayer,
                        progression=str(worshipPrayersDict[optionalPrayer]['Level']),
                        goal=str(optional_prayers[optionalPrayer]),
                        resource=worshipPrayersDict[optionalPrayer]['Material']
                    ))

    # Check Ignorable Prayers
    for ignorablePrayer in ignorable_prayers:
        if worshipPrayersDict[ignorablePrayer]['Level'] < ignorable_prayers[ignorablePrayer]:
            prayers_AdviceDict["Ignorable"].append(
                Advice(
                    label=ignorablePrayer,
                    picture_class=ignorablePrayer,
                    progression=str(worshipPrayersDict[ignorablePrayer]['Level']),
                    goal=str(ignorable_prayers[ignorablePrayer]),
                    resource=worshipPrayersDict[ignorablePrayer]['Material']
                ))

    # Generate Advice Groups
    prayers_AdviceGroupDict['Recommended'] = AdviceGroup(
        tier=tier_WorshipPrayers,
        pre_string=f"Recommended Prayer{pl(adviceCountsDict['Recommended'])}",
        advices=prayers_AdviceDict['Recommended'],
        post_string="",
    )
    prayers_AdviceGroupDict['Optional'] = AdviceGroup(
        tier="",
        pre_string=f"Situational Prayer{pl(prayers_AdviceDict['Optional'])} you may consider levelling",
        advices=prayers_AdviceDict['Optional'],
        post_string="These are niche use prayers. They have different benefits/purposes at low level and high levels",
        informational=True,
        completed=True
    )
    prayers_AdviceGroupDict['Ignorable'] = AdviceGroup(
        tier="",
        pre_string=f"Ignorable Prayer{pl(prayers_AdviceDict['Ignorable'])}",
        advices=prayers_AdviceDict['Ignorable'],
        post_string="Prayers in this group should still be unlocked, but can stay at level 1 after that as of v2.12",
        informational=True,
        completed=True
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_WorshipPrayers)
    return prayers_AdviceGroupDict, overall_SectionTier, max_tier, max_tier + info_tiers

def getPrayersAdviceSection() -> AdviceSection:
    highestWorshipLevel = max(session_data.account.all_skills["Worship"])
    if highestWorshipLevel < 1:
        prayers_AdviceSection = AdviceSection(
            name="Prayers",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Worship skill in World 3!",
            picture="Prayer_Stone.gif",
            unreached=True
        )
        return prayers_AdviceSection

    #Generate AdviceGroups
    prayers_AdviceGroupDict, overall_SectionTier, max_tier, true_max = setPrayersProgressionTierAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    prayers_AdviceSection = AdviceSection(
        name="Prayers",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Prayer tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Prayer_Stone.gif",
        groups = prayers_AdviceGroupDict.values()
    )
    return prayers_AdviceSection
