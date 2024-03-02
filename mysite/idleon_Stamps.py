import progressionResults
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger

logger = get_logger(__name__)

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
    priorityStampsDict = {}
    maxExpectedStampLengths = {
        "Combat": 42,  #42 total, ranging from 0 to 41
        "Skill": 54,  #54 total, ranging from 0 to 53
        "Misc": 23,  #23 total, ranging from 0 to 22
    }
    stampTypes = ["Combat", "Skill", "Misc"]
    for stampType in stampTypes:
        for stampIndex in range(0, maxExpectedStampLengths[stampType]):
            try:
                priorityStampsDict[getReadableStampName(stampIndex, stampType)] = inputJSON["StampLv"][stampTypes.index(stampType)][str(stampIndex)]
            except:
                logger.debug(f"Level for {stampType} {stampIndex} ({getReadableStampName(stampIndex, stampType)}) not found in Save Data. Setting to 0.")
                priorityStampsDict[getReadableStampName(stampIndex, stampType)] = 0

    return priorityStampsDict

def getCapacityExclusions(priorityStampsDict: dict):
    exclusionsDict = {
        'Matty Bag Stamp': False,  # Materials
        'Foods': False,  # Doesn't exist currently, placeholder
        "Lil' Mining Baggy Stamp": False,  # Mining Ores
        "Choppin' Bag Stamp": False,  # Choppin Logs
        'Bag o Heads Stamp': False,  # Fish
        'Bugsack Stamp': False,  # Catching Bugs
        'Critters': False,  # Doesn't exist currently, placeholder
        'Souls': False  # Doesn't exist currently, placeholder
    }
    if priorityStampsDict['Crystallin'] >= 260:  # Max as of v2.01
        exclusionsDict['Matty Bag Stamp'] = True
    if priorityStampsDict['Multitool Stamp'] >= 220:  # Max as of v2.01
        exclusionsDict['Bugsack Stamp'] = True
        exclusionsDict['Bag o Heads Stamp'] = True
    return exclusionsDict

# Stamp p4
def getReadableStampName(stampNumber, stampType):
    #logger.debug(f"Fetching name for {stampType} + {stampNumber}")
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
                case 39:
                    return "Void Sword Stamp"
                case 40:
                    return "Void Axe Stamp"
                case 41:
                    return "Captalist Stats Stamp"
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
                case 47:
                    return "Crop Evo Stamp"
                case 48:
                    return "Sneaky Peeky Stamp"
                case 49:
                    return "Jade Mint Stamp"
                case 50:
                    return "Summoner Stone Stamp"
                case 51:
                    return "White Essence Stamp"
                case 52:
                    return "Triad Essence Stamp"
                case 53:
                    return "Dark Triad Essence Stamp"
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
                case 9:
                    return "Forge Stamp"
                case 10:
                    return "Vendor Stamp"
                case 11:
                    return "Sigil Stamp"
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
                case 22:
                    return "Atomic Stamp"
                case _:
                    return "Unknown Misc stamp: " + str(stampNumber)

# Stamp meta
def setStampProgressionTier(inputJSON, progressionTiers) -> AdviceSection:
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
                #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingCombatStamps}")
                if rStamp in missingCombatStamps:
                    allCombatStamps = False
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
                #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingSkillStamps}")
                if rStamp in missingSkillStamps:
                    allSkillStamps = False
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
                #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingMiscStamps}")
                if rStamp in missingMiscStamps:
                    allMiscStamps = False
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
                #logger.debug(f"{tier[0]}, {playerPriorityStamps[key]}, {requiredSpecificStamps[key]}, {playerPriorityStamps[key] >= requiredSpecificStamps[key]}")
                if playerPriorityStamps[key] < requiredSpecificStamps[key]:
                    if key in capacityExclusionsDict:
                        if capacityExclusionsDict[key] is False:
                            allSpecificStamps = False
                            stamp_AdviceDict["SpecificStamps"].append(
                                Advice(
                                    label=str(key),
                                    item_name=str(key),
                                    progression=playerPriorityStamps[key],
                                    goal=requiredSpecificStamps[key],
                                    unit=""
                                )
                            )
                    else:
                        allSpecificStamps = False
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

    # Generate AdviceGroups
    # Overall Stamp Levels
    stamp_AdviceGroupDict["StampLevels"] = AdviceGroup(
        tier=tier_StampLevels,
        pre_string="Improve your total stamp levels",
        advices=stamp_AdviceDict["StampLevels"]
    )

    # Combat Stamps
    stamp_AdviceGroupDict["CombatStamps"] = AdviceGroup(
        tier=str(tier_RequiredCombatStamps),
        pre_string=f"Collect the following Combat stamp{pl(stamp_AdviceDict['CombatStamps'])}",
        advices=stamp_AdviceDict['CombatStamps'])

    # Skill Stamps
    stamp_AdviceGroupDict["SkillStamps"] = AdviceGroup(
        tier=str(tier_RequiredSkillStamps),
        pre_string=f"Collect the following Skill stamp{pl(stamp_AdviceDict['SkillStamps'])}",
        advices=stamp_AdviceDict["SkillStamps"])

    # Misc Stamps
    stamp_AdviceGroupDict["MiscStamps"] = AdviceGroup(
        tier=str(tier_RequiredMiscStamps),
        pre_string=f"Collect the following Misc stamp{pl(stamp_AdviceDict['MiscStamps'])}",
        advices=stamp_AdviceDict["MiscStamps"])

    # Specific High-Priority Stamps
    stamp_AdviceGroupDict["SpecificStamps"] = AdviceGroup(
        tier=str(tier_RequiredSpecificStamps),
        pre_string=f"Improve the following high-priority stamp{pl(stamp_AdviceDict['MiscStamps'])}",
        advices=stamp_AdviceDict["SpecificStamps"])

    #Generate AdviceSection
    tier_section = f"{overall_StampTier}/{max_tier}"
    stamp_AdviceSection.pinchy_rating = overall_StampTier
    stamp_AdviceSection.tier = tier_section
    stamp_AdviceSection.groups = stamp_AdviceGroupDict.values()
    if overall_StampTier == max_tier:
        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}. You've reached the end of the recommendations. Let me know what important stamps you're aiming for next!"
    else:
        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}. Recommended stamp actions:"

    return stamp_AdviceSection
