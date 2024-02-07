import progressionResults
from models import AdviceSection, AdviceGroup, Advice
from utils import pl

# Stamp p1
def setStampLevels(inputJSON, inputIndex):
    totalStampLevels = 0
    totalStampLevels -= inputJSON["StampLv"][inputIndex]['length']
    for stamp in inputJSON["StampLv"][inputIndex].values():
        totalStampLevels += int(stamp)
    return totalStampLevels


# Stamp p2
def setMissingStamps(inputJSON, inputIndex):
    missingStamps = []
    for stamp, value in inputJSON["StampLvM"][inputIndex].items():
        if value == 0:
            missingStamps.append(stamp)
    return missingStamps


# Stamp p3
def setPriorityStamps(inputJSON):
    priorityStampsDict = {
        'Maxo Slappo Stamp': inputJSON["StampLv"][0]['32'],
        'Sashe Sidestamp': inputJSON["StampLv"][0]['33'],
        'Intellectostampo': inputJSON["StampLv"][0]['34'],
        'Golden Sixes Stamp': 0,
        'Stat Wallstreet Stamp': 0,
        'Pickaxe Stamp': inputJSON["StampLv"][1]['0'],
        'Hatchet Stamp': inputJSON["StampLv"][1]['1'],
        'Matty Bag Stamp': inputJSON["StampLv"][1]['7'],
        'Drippy Drop Stamp': inputJSON["StampLv"][1]['14'],
        'Bag o Heads Stamp': inputJSON["StampLv"][1]['20'],
        'Bugsack Stamp': inputJSON["StampLv"][1]['22'],
        'Skelefish Stamp': 0,
        'Ladle Stamp': inputJSON["StampLv"][1]['38'],
        'Multitool Stamp': inputJSON["StampLv"][1]['45'],
        'Mason Jar Stamp': inputJSON["StampLv"][2]['1'],
        'Crystallin': inputJSON["StampLv"][2]['2'],
        'Golden Apple Stamp': inputJSON["StampLv"][2]['6'],
        'Card Stamp': inputJSON["StampLv"][2]['8']
    }
    # These are newer stamps from the Island Expedition update.
    if '37' in inputJSON["StampLv"][0]:
        priorityStampsDict['Golden Sixes Stamp'] = inputJSON["StampLv"][0]['37']
    if '38' in inputJSON["StampLv"][0]:
        priorityStampsDict['Stat Wallstreet'] = inputJSON["StampLv"][0]['38']
    if '37' in inputJSON["StampLv"][1]:
        priorityStampsDict['Skelefish'] = inputJSON["StampLv"][1]['37']

    return priorityStampsDict

def getCapacityExclusions(priorityStampsDict: dict):
    exclusionsDict = {
        'Materials': False,
        'Foods': False,
        'Ores': False,
        'Logs': False,
        'Fish': False,
        'Bugs': False,
        'Critters': False,
        'Souls': False
    }
    if priorityStampsDict['Crystallin'] >= 250:
        exclusionsDict['Materials'] = True
    if priorityStampsDict['Multitool Stamp'] >= 210:
        exclusionsDict['Bugs'] = True
    return exclusionsDict

# Stamp p4
def getReadableStampName(stampNumber, stampType):
    # print("Fetching name for " + stampType + " stamp: " + stampNumber)
    match stampType:
        case "Combat":
            match stampNumber:
                case 0:
                    return "Sword Stamp"
                case 1:
                    return "Heart Stamp"
                case 2:
                    return "Mana Stamp"
                case 3:
                    return "Tomahawk Stamp"
                case 4:
                    return "Target Stamp"
                case 5:
                    return "Shield Stamp"
                case 6:
                    return "Longsword Stamp"
                case 7:
                    return "Kapow Stamp"
                case 8:
                    return "Fist Stamp"
                case 9:
                    return "Battleaxe Stamp"
                case 10:
                    return "Agile Stamp"
                case 11:
                    return "Vitality Stamp"
                case 12:
                    return "Book Stamp"
                case 13:
                    return "Manamoar Stamp"
                case 14:
                    return "Clover Stamp"
                case 15:
                    return "Scimitar Stamp"
                case 16:
                    return "Bullseye Stamp"
                case 17:
                    return "Feather Stamp"
                case 18:
                    return "Polearm Stamp"
                case 19:
                    return "Violence Stamp"
                case 20:
                    return "Buckler Stamp"
                case 21:
                    return "Hermes Stamp"
                case 22:
                    return "Sukka Foo"
                case 23:
                    return "Arcane Stamp"
                case 24:
                    return "Avast Yar Stamp"
                case 25:
                    return "Steve Sword"
                case 26:
                    return "Blover Stamp"
                case 27:
                    return "Stat Graph Stamp"
                case 28:
                    return "Gilded Axe Stamp"
                case 29:
                    return "Diamond Axe Stamp"
                case 30:
                    return "Tripleshot Stamp"
                case 31:
                    return "Blackheart Stamp"
                case 32:
                    return "Maxo Slappo Stamp"
                case 33:
                    return "Sashe Sidestamp"
                case 34:
                    return "Intellectostampo"
                case 35:
                    return "Conjocharmo Stamp"
                case 36:
                    return "Dementia Sword Stamp"
                case 37:
                    return "Golden Sixes Stamp"
                case 38:
                    return "Stat Wallstreet Stamp"
                case _:
                    return "Unknown Combat stamp: " + str(stampNumber)
        case "Skill":
            match stampNumber:
                case 0:
                    return "Pickaxe Stamp"
                case 1:
                    return "Hatchet Stamp"
                case 2:
                    return "Anvil Zoomer Stamp"
                case 3:
                    return "Lil' Mining Baggy Stamp"
                case 4:
                    return "Twin Ores Stamp"
                case 5:
                    return "Choppin' Bag Stamp"
                case 6:
                    return "Duplogs Stamp"
                case 7:
                    return "Matty Bag Stamp"
                case 8:
                    return "Smart Dirt Stamp"
                case 9:
                    return "Cool Diggy Tool Stamp"
                case 10:
                    return "High IQ Lumber Stamp"
                case 11:
                    return "Swag Swingy Tool Stamp"
                case 12:
                    return "Alch Go Brrr Stamp"
                case 13:
                    return "Brainstew Stamp"
                case 14:
                    return "Drippy Drop Stamp"
                case 15:
                    return "Droplots Stamp"
                case 16:
                    return "Fishing Rod Stamp"
                case 17:
                    return "Fishhead Stamp"
                case 18:
                    return "Catch Net Stamp"
                case 19:
                    return "Fly Intel Stamp"
                case 20:
                    return "Bag o Heads Stamp"
                case 21:
                    return "Holy Mackerel Stamp"
                case 22:
                    return "Bugsack Stamp"
                case 23:
                    return "Buzz Buzz Stamp"
                case 24:
                    return "Hidey Box Stamp"
                case 25:
                    return "Purp Froge Stamp"
                case 26:
                    return "Spikemouth Stamp"
                case 27:
                    return "Shiny Crab Stamp"
                case 28:
                    return "Gear Stamp"
                case 29:
                    return "Stample Stamp"
                case 30:
                    return "Saw Stamp"
                case 31:
                    return "Amplestample Stamp"
                case 32:
                    return "SpoOoky Stamp"
                case 33:
                    return "Flowin Stamp"
                case 34:
                    return "Prayday Stamp"
                case 35:
                    return "Banked Pts Stamp"
                case 36:
                    return "Cooked Meal Stamp"
                case 37:
                    return "Spice Stamp"
                case 38:
                    return "Ladle Stamp"
                case 39:
                    return "Nest Eggs Stamp"
                case 40:
                    return "Egg Stamp"
                case 41:
                    return "Lab Tube Stamp"
                case 42:
                    return "Sailboat Stamp"
                case 43:
                    return "Gamejoy Stamp"
                case 44:
                    return "Divine Stamp"
                case 45:
                    return "Multitool Stamp"
                case 46:
                    return "Skelefish Stamp"
                case _:
                    return "Unknown Skill stamp: " + str(stampNumber)
        case "Misc":
            match stampNumber:
                case 0:
                    return "Questin Stamp"
                case 1:
                    return "Mason Jar Stamp"
                case 2:
                    return "Crystallin"
                case 3:
                    return "Arcade Ball Stamp"
                case 4:
                    return "Gold Ball Stamp"
                case 5:
                    return "Potion Stamp"
                case 6:
                    return "Golden Apple Stamp"
                case 7:
                    return "Ball Timer Stamp"
                case 8:
                    return "Card Stamp"
                # case 9:
                #    return "Blue Hatchet Stamp"
                # case 10:
                #    return "Red Sword Stamp"
                # case 11:
                #    return "Blue Sword Stamp"
                case 12:
                    return "Talent I Stamp"
                case 13:
                    return "Talent II Stamp"
                case 14:
                    return "Talent III Stamp"
                case 15:
                    return "Talent IV Stamp"
                case 16:
                    return "Talent V Stamp"
                case 17:
                    return "Talent S Stamp"
                case 18:
                    return "Multikill Stamp"
                case 19:
                    return "Biblio Stamp"
                case 20:
                    return "DNA Stamp"
                case 21:
                    return "Refinery Stamp"
                case _:
                    return "Unknown Misc stamp: " + str(stampNumber)


# Stamp meta
def setStampProgressionTier(inputJSON, progressionTiers):
    totalCombatStampLevels = setStampLevels(inputJSON, 0)
    totalSkillStampLevels = setStampLevels(inputJSON, 1)
    totalMiscStampLevels = setStampLevels(inputJSON, 2)
    totalAllStampLevels = totalCombatStampLevels + totalSkillStampLevels + totalMiscStampLevels
    missingCombatStamps = setMissingStamps(inputJSON, 0)
    missingSkillStamps = setMissingStamps(inputJSON, 1)
    missingMiscStamps = setMissingStamps(inputJSON, 2)
    playerPriorityStamps = setPriorityStamps(inputJSON)
    capacityExclusionsDict = getCapacityExclusions(playerPriorityStamps)
    tier_StampLevels = 0
    tier_RequiredCombatStamps = 0
    tier_RequiredSkillStamps = 0
    tier_RequiredMiscStamps = 0
    tier_RequiredSpecificStamps = 0
    max_tier = progressionTiers[-1][0]
    advice_StampLevels = ""
    advice_CollectCombatStamps = ""
    advice_CollectSkillStamps = ""
    advice_CollectMiscStamps = ""
    advice_CollectStamps = ""
    advice_SpecificStamps = ""
    stamp_AdviceDict = {
        "StampLevels": [],
        "CombatStamps": [],
        "SkillStamps": [],
        "MiscStamps": [],
        "SpecificStamps": [],
    }
    stamp_AdviceGroupDict = {}
    stamp_AdviceSection = AdviceSection(
        name="Stamps",
        tier="Not Yet Evaluated",
        header="Best Stamp tier met: Not Yet Evaluated. Recommended stamp actions:",
        picture="Stamps_Mr_Pigibank.gif"
    )

    for tier in progressionTiers:
        # TotalLevelStamps
        if tier_StampLevels == (tier[0] - 1):
            if totalAllStampLevels >= tier[1]:  # int
                tier_StampLevels = tier[0]
            else:
                advice_StampLevels = tier[1]
                stamp_AdviceDict["StampLevels"].append(
                    Advice(
                        label="Total Stamp Levels",
                        item_name="stat-graph-stamp",
                        progression=totalAllStampLevels,
                        goal=advice_StampLevels,
                    )
                )

        # CombatStamps
        if tier_RequiredCombatStamps == (tier[0] - 1):  # Only check if they already met previous tier
            allCombatStamps = True
            splitRequiredCombatStamps = tier[2].split(",")  # string of numbers, no spaces
            for rStamp in splitRequiredCombatStamps:
                # print(rStamp, missingCombatStamps, (rStamp in missingCombatStamps))
                if rStamp in missingCombatStamps:
                    allCombatStamps = False
                    advice_CollectStamps += (getReadableStampName(int(rStamp), "Combat") + ", ")
                    advice_CollectCombatStamps += (getReadableStampName(int(rStamp), "Combat") + ", ")
                    stamp_AdviceDict["CombatStamps"].append(
                        Advice(
                            label=getReadableStampName(int(rStamp), "Combat"),
                            item_name=getReadableStampName(int(rStamp), "Combat"),
                        )
                    )
            if allCombatStamps == True:
                tier_RequiredCombatStamps = tier[0]

        # SkillStamps
        if tier_RequiredSkillStamps == (tier[0] - 1):  # Only check if they already met previous tier
            allSkillStamps = True
            splitRequiredSkillStamps = tier[3].split(",")  # string of numbers, no spaces
            for rStamp in splitRequiredSkillStamps:
                # print(rStamp, missingSkillStamps, (rStamp in missingSkillStamps))
                if rStamp in capacityExclusionsDict:
                    if capacityExclusionsDict[rStamp] is False:
                        if rStamp in missingSkillStamps:
                            allSkillStamps = False
                            advice_CollectStamps += (getReadableStampName(int(rStamp), "Skill") + ", ")
                            advice_CollectSkillStamps += (getReadableStampName(int(rStamp), "Skill") + ", ")
                            stamp_AdviceDict["SkillStamps"].append(
                                Advice(
                                    label=getReadableStampName(int(rStamp), "Skill"),
                                    item_name=getReadableStampName(int(rStamp), "Skill"),
                                    progression="",
                                    goal="",
                                    unit=""
                                )
                            )
            if allSkillStamps == True:
                tier_RequiredSkillStamps = tier[0]

        # MiscStamps
        if tier_RequiredMiscStamps == (tier[0] - 1):  # Only check if they already met previous tier
            allMiscStamps = True
            splitRequiredMiscStamps = tier[4].split(",")  # string of numbers, no spaces
            for rStamp in splitRequiredMiscStamps:
                if rStamp in missingMiscStamps:
                    allMiscStamps = False
                    advice_CollectStamps += (getReadableStampName(int(rStamp), "Misc") + ", ")
                    advice_CollectMiscStamps += (getReadableStampName(int(rStamp), "Misc") + ", ")
                    stamp_AdviceDict["MiscStamps"].append(
                        Advice(
                            label=getReadableStampName(int(rStamp), "Misc"),
                            item_name=getReadableStampName(int(rStamp), "Misc"),
                            progression="",
                            goal="",
                            unit=""
                        )
                    )
            if allMiscStamps == True:
                tier_RequiredMiscStamps = tier[0]

        # SpecificStampLevels
        if tier_RequiredSpecificStamps == (tier[0] - 1):  # Only check if they already met previous tier
            requiredSpecificStamps = tier[5]  # dictionary
            allSpecificStamps = True
            for key, value in requiredSpecificStamps.items():
                # print(tier[0], playerPriorityStamps[key], requiredSpecificStamps[key], playerPriorityStamps[key] >= requiredSpecificStamps[key])
                if playerPriorityStamps[key] < requiredSpecificStamps[key]:
                    allSpecificStamps = False
                    advice_SpecificStamps += (str(key) + " to " + str(value) + "+, ")
                    stamp_AdviceDict["SpecificStamps"].append(
                        Advice(
                            label=str(key),
                            item_name=str(key),
                            progression=playerPriorityStamps[key],
                            goal=requiredSpecificStamps[key],
                            unit=""
                        )
                    )
            if allSpecificStamps == True:
                tier_RequiredSpecificStamps = tier[0]

    overall_StampTier = min(max_tier, tier_StampLevels, tier_RequiredCombatStamps, tier_RequiredSkillStamps,
                            tier_RequiredMiscStamps, tier_RequiredSpecificStamps)

    # Generate advice statements
    # Overall Stamp Levels
    if advice_StampLevels != "":
        advice_StampLevels = (f"Tier {tier_StampLevels}- Improve your total stamp levels "
                              f"to {advice_StampLevels}+")
        stamp_AdviceGroupDict["StampLevels"] = AdviceGroup(
            tier=tier_StampLevels,
            pre_string="Improve your total stamp levels",
            advices=stamp_AdviceDict["StampLevels"]
        )

    # Combat Stamps
    if advice_CollectCombatStamps != "":
        advice_CollectCombatStamps = (f"Tier {tier_RequiredCombatStamps}- Collect the "
                                      f"following Combat stamp(s): {advice_CollectCombatStamps[:-2]}")
        stamp_AdviceGroupDict["CombatStamps"] = AdviceGroup(
            tier=str(tier_RequiredCombatStamps),
            pre_string=f"Collect the following Combat stamp{pl(stamp_AdviceDict['CombatStamps'])}",
            advices=stamp_AdviceDict['CombatStamps']
        )

    # Skill Stamps
    if advice_CollectSkillStamps != "":
        advice_CollectSkillStamps = (f"Tier {tier_RequiredSkillStamps}- Collect the "
                                     f"following Skill stamp(s): {advice_CollectSkillStamps[:-2]}")
        stamp_AdviceGroupDict["SkillStamps"] = AdviceGroup(
            tier=str(tier_RequiredSkillStamps),
            pre_string=f"Collect the following Skill stamp{pl(stamp_AdviceDict['SkillStamps'])}",
            advices=stamp_AdviceDict["SkillStamps"])

    # Misc Stamps
    if advice_CollectMiscStamps != "":
        advice_CollectMiscStamps = (f"Tier {tier_RequiredMiscStamps}- Collect the "
                                    f"following Misc stamp(s): {advice_CollectMiscStamps[:-2]}")
        stamp_AdviceGroupDict["MiscStamps"] = AdviceGroup(
            tier=str(tier_RequiredMiscStamps),
            pre_string=f"Collect the following Misc stamp{pl(stamp_AdviceDict['MiscStamps'])}",
            advices=stamp_AdviceDict["MiscStamps"]
        )

    # Specific High-Priority Stamps
    if advice_SpecificStamps != "":
        advice_SpecificStamps = (f"Tier {tier_RequiredSpecificStamps}- Improve these "
                                 f"high-priority stamp(s): {advice_SpecificStamps[:-2]}")
        stamp_AdviceGroupDict["SpecificStamps"] = AdviceGroup(
            tier=str(tier_RequiredSpecificStamps),
            pre_string=f"Improve the following high-priority stamp{pl(stamp_AdviceDict['MiscStamps'])}",
            advices=stamp_AdviceDict["SpecificStamps"]
        )

    tier_section = f"{overall_StampTier}/{max_tier}"
    stamp_AdviceSection.tier = tier_section
    if overall_StampTier == max_tier:
        advice_CombinedStamps = [
            f"Best Stamp tier met: {tier_section}. Recommended stamp actions:", "", "",
            "You've reached the end of the recommendations. Let me know what important stamps you're aiming for next!"]

        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}. You've reached the end of the recommendations. Let me know what important stamps you're aiming for next!"
    else:
        advice_CombinedStamps = [
            f"Best Stamp tier met: {tier_section}. Recommended stamp actions:",
            advice_StampLevels,
            advice_CollectCombatStamps,
            advice_CollectSkillStamps,
            advice_CollectMiscStamps,
            advice_SpecificStamps]
        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}. Recommended stamp actions:"
        stamp_AdviceSection.groups = [
            stamp_AdviceGroupDict.get("StampLevels"),
            stamp_AdviceGroupDict.get("CombatStamps"),
            stamp_AdviceGroupDict.get("SkillStamps"),
            stamp_AdviceGroupDict.get("MiscStamps"),
            stamp_AdviceGroupDict.get("SpecificStamps")
        ]

    stampPR = progressionResults.progressionResults(overall_StampTier, advice_CombinedStamps, "")
    return {"PR": stampPR, "AdviceSection": stamp_AdviceSection}
