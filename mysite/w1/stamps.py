from models.models import AdviceSection, AdviceGroup, Advice, Character
from utils.text_formatting import pl
from utils.data_formatting import safe_loads
from utils.logging import get_logger
from consts import maxTiersPerGroup, stamps_progressionTiers, stamp_maxes, lavaFunc
from math import ceil, pow
from flask import g as session_data


logger = get_logger(__name__)

def ceilUpToBase(inputValue: int, base: int) -> int:
    toReturn = base
    while toReturn <= inputValue:
        toReturn += base
    return toReturn

# Stamp p1
def setStampLevels(inputIndex):
    totalStampLevels = 0
    totalStampLevels -= safe_loads(session_data.account.raw_data["StampLv"])[inputIndex]['length']
    for stamp in session_data.account.raw_data["StampLv"][inputIndex].values():
        totalStampLevels += int(stamp)
    return totalStampLevels

# Stamp p2
def setMissingStamps(playerStampsDict):
    unavailableStampsList = [
            'Shiny Crab Stamp', 'Gear Stamp', 'SpoOoky Stamp', 'Prayday Stamp',  #Skill
            'Talent I Stamp', 'Talent V Stamp',  #Misc
    ]
    missingStampsList = []
    for stampTypeIndex in range(0, 2):
        for stamp, value in playerStampsDict.items():
            if value == 0 and stamp not in unavailableStampsList:
                missingStampsList.append(stamp)
    return missingStampsList

# Stamp p3
def setPriorityStamps():
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
                priorityStampsDict[getReadableStampName(stampIndex, stampType)] = session_data.account.raw_data["StampLv"][stampTypes.index(stampType)][str(stampIndex)]
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
        'Souls': False,  # Doesn't exist currently, placeholder
        'Mason Jar Stamp': False,  #All types, but less per level
    }
    if priorityStampsDict['Crystallin'] >= 250:  #Old Max Pre-W6
        exclusionsDict['Matty Bag Stamp'] = True
    if priorityStampsDict['Multitool Stamp'] >= 210:  #Old Max Pre-W6
        exclusionsDict['Bugsack Stamp'] = True
        exclusionsDict['Bag o Heads Stamp'] = True
    if priorityStampsDict['Crystallin'] >= 250 and priorityStampsDict['Multitool Stamp'] >= 210:
        exclusionsDict['Mason Jar Stamp'] = True
    return exclusionsDict

def getCapacityAdviceGroup(priorityStampsDict: dict) -> AdviceGroup:
    capacity_Advices = {"Stamps": [], "Account Wide": [], "Character Specific": []}

    if session_data.account.labChips.get('Silkrode Nanochip', 0) > 0:
        nanoEval = f"{session_data.account.labChips.get('Silkrode Nanochip',0)} owned. Doubles starsigns when equipped."
        silkrodeMulti = 2
    else:
        nanoEval = "None Owned. Would double other signs if equipped."
        silkrodeMulti = 1

    seraphMulti = min(3, 1.1 ** ceil((max(session_data.account.all_skills.get('Summoning', [0])) + 1) / 20))
    seraphGoal = min(240, ceilUpToBase(max(session_data.account.all_skills.get('Summoning', [0])), 20))
    if bool(session_data.account.star_signs.get("Seraph_Cosmos", False)):
        seraphEval = f"Multis signs by {seraphMulti:.2f}x."
    else:
        seraphEval = f"Locked. Would increase below signs by {seraphMulti:.2f}x if unlocked."
        seraphMulti = 1
    if seraphGoal < 240:
        seraphEval += " Next increase at Summoning level"
    starsignBase = 0
    starsignBase += 30 * bool(session_data.account.star_signs.get("Mr_No_Sleep", False))
    starsignBase += 10 * bool(session_data.account.star_signs.get("Pack_Mule", False))
    starsignBase += 5 * bool(session_data.account.star_signs.get("The_OG_Skiller", False))
    totalStarsignValue = starsignBase * silkrodeMulti * seraphMulti

    #Stamps
    capacity_Advices["Stamps"].append(Advice(
        label="Jade Emporium: Level Exemption",
        picture_class="level-exemption",
        progression=1 if "Level Exemption" in session_data.account.jade_emporium_purchases else 0,
        goal=1
    ))
    capacity_Advices["Stamps"].append(Advice(
        label="Lab Bonus: Certified Stamp Book",
        picture_class="certified-stamp-book",
        progression=f"{1 if session_data.account.labBonuses.get('Certified Stamp Book', {}).get('Enabled', False) else 0}",
        goal=1
    ))
    capacity_Advices["Stamps"].append(Advice(
        label="Lab Jewel: Pure Opal Navette (lol jk, this is bugged)",
        picture_class="pure-opal-navette",
    ))
    capacity_Advices["Stamps"].append(Advice(
        label="Pristine Charm: Liqorice Rolle",
        picture_class="liqorice-rolle",
        progression=int(session_data.account.pristine_charms.get("Liqorice Rolle", 0)),
        goal=1
    ))
    for capStamp in ["Mason Jar Stamp", "Lil' Mining Baggy Stamp", "Choppin' Bag Stamp", "Matty Bag Stamp", "Bag o Heads Stamp", "Bugsack Stamp"]:
        capacity_Advices["Stamps"].append(Advice(
            label=capStamp,
            picture_class=capStamp,
            progression=priorityStampsDict.get(capStamp, 0),
            goal=stamp_maxes.get(capStamp, 999)
        ))

    #Account-Wide
    capacity_Advices["Account Wide"].append(Advice(
        label="Bribe: Bottomless Bags",
        picture_class="bottomless-bags",
        progression=1 if session_data.account.bribes.get("Bottomless Bags") >= 1 else 0,
        goal=1
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label="Guild Bonus: Rucksack",
        picture_class="rucksack",
        progression=f"{session_data.account.guildBonuses.get('Rucksack', 0) if session_data.account.guildBonuses.get('Rucksack', 0) > 0 else 'IDK'}",
        goal=50
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label="Pantheon Shrine",
        picture_class="pantheon-shrine",
        progression=session_data.account.shrines.get("Pantheon Shrine", {}).get("Level", 0),
        goal="∞"
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label="Chaotic Chizoar card increases the capacity from Pantheon Shrine",
        picture_class="chaotic-chizoar-card",
        progression=next(c.getStars() for c in session_data.account.cards if c.name == "Chaotic Chizoar"),
        goal=5
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label="Gem Shop: Carry Capacity",
        picture_class="carry-capacity",
        progression=session_data.account.gemshop.get("Carry Capacity", 0),
        goal=10
    ))
    capacity_Advices["Account Wide"].append(Advice(
        label=f"Starsign: Seraph Cosmos: {seraphEval}",
        picture_class="seraph-cosmos",
        progression=max(session_data.account.all_skills.get('Summoning', [0])),
        goal=seraphGoal
    ))

    #Character Specific
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Lab Chip: Silkrode Nanochip: {nanoEval}",
        picture_class="silkrode-nanochip",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: Mr No Sleep: {30 * bool(session_data.account.star_signs.get('Mr_No_Sleep', False))}% base",
        picture_class="mr-no-sleep",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: Pack Mule: {10 * bool(session_data.account.star_signs.get('Pack_Mule', False))}% base",
        picture_class="pack-mule",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Starsign: The OG Skiller: {5 * bool(session_data.account.star_signs.get('The_OG_Skiller', False))}% base",
        picture_class="the-og-skiller",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label=f"Total Starsign Value: {totalStarsignValue:.2f}%",
        picture_class="",
    ))

    capacity_Advices["Character Specific"].append(Advice(
        label="Jman's Extra Bags talent (Materials only)",
        picture_class="extra-bags",
        goal=270
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="80 available Inventory Slots",
        picture_class="storage",
        as_link=True
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="Highest Type-Specific Capacity Bag crafted",
        picture_class="herculean-matty-pouch",
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="Prayer: Ruck Sack",
        picture_class="ruck-sack",
        progression=session_data.account.prayers.get("Ruck Sack (Rooted Soul)", 0),
        goal=50
    ))
    capacity_Advices["Character Specific"].append(Advice(
        label="PRAYER: REMOVE ZERG RUSHOGEN",
        picture_class="zerg-rushogen",
        goal="❌"
    ))
    w3meritList = safe_loads(session_data.account.raw_data.get("TaskZZ2", []))
    tkMaxLevel = w3meritList[2][3] * 5 if w3meritList else 0
    capacity_Advices["Character Specific"].append(Advice(
        label="Star Talent: Telekinetic Storage",
        picture_class="telekinetic-storage",
        progression=tkMaxLevel,
        goal=50
    ))

    for group_name in capacity_Advices:  #["Stamps", "Account Wide", "Character Specific"]:
        for advice in capacity_Advices[group_name]:
            mark_completed(advice)

    #Build the AdviceGroup
    capacity_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Carry Capacity",
        advices=capacity_Advices,
        post_string="",
    )
    return capacity_AdviceGroup


def mark_completed(advice):
    try:
        if advice.goal and advice.progression and int(advice.goal) == int(advice.progression):
            advice.progression = ""
            advice.goal = "✔"
            setattr(advice, "status", "complete")
    except:
        pass


def getCostReductionAdviceGroup() -> AdviceGroup:
    costReduction_Advices = {"Vials": [], "Uncapped": []}

    costReduction_Advices["Vials"].append(Advice(
        label="Vial: Blue Flav (Platinum Ore)",
        picture_class="platinum-ore",
        progression=session_data.account.alchemy_vials.get("Blue Flav (Platinum Ore)", {}).get("Level", 0),
        goal=13
    ))
    costReduction_Advices["Vials"].append(Advice(
        label="Vial: Venison Malt (Mongo Worm Slices)",
        picture_class="mongo-worm-slices",
        progression=session_data.account.alchemy_vials.get("Venison Malt (Mongo Worm Slices)", {}).get("Level", 0),
        goal=13
    ))
    costReduction_Advices["Vials"].append(Advice(
        label="Lab Bonus: My 1st Chemistry Set",
        picture_class="my-1st-chemistry-set",
        progression=f"{1 if session_data.account.labBonuses.get('My 1st Chemistry Set', {}).get('Enabled', False) else 0}",
        goal=1
    ))

    blueFavReduction = session_data.account.alchemy_vials.get("Blue Flav (Platinum Ore)", {}).get("Value", 0)
    venisonMaltReduction = session_data.account.alchemy_vials.get("Venison Malt (Mongo Worm Slices)", {}).get("Value", 0)
    totalVialReduction = blueFavReduction + venisonMaltReduction
    vialMasteryMulti = 1 + (session_data.account.maxed_vials * .02) if session_data.account.vial_mastery_unlocked else 1
    totalVialReduction *= vialMasteryMulti
    if session_data.account.labBonuses.get("My 1st Chemistry Set", {}).get("Enabled", False):
        totalVialReduction *= 2
    costReduction_Advices["Vials"].append(Advice(
        label=f"Rift Bonus: Vial Mastery: {vialMasteryMulti:.2f}x",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.vial_mastery_unlocked else 0}",
        goal=1
    ))
    costReduction_Advices["Vials"].append(Advice(
        label="Total Vial reduction is hardcapped at 95%",
        picture_class="",
        progression=f"{totalVialReduction:.2f}",
        goal=95,
        unit="%"
    ))

    costReduction_Advices["Uncapped"].append(Advice(
        label="Jade Emporium: Ionized Sigils",
        picture_class="ionized-sigils",
        progression=f"{1 if 'Ionized Sigils' in session_data.account.jade_emporium_purchases else 0}",
        goal=1
    ))
    if (session_data.account.alchemy_p2w.get('Sigils', {}).get('Envelope Pile', {}).get('PrechargeLevel', 0)
        > session_data.account.alchemy_p2w.get('Sigils', {}).get('Envelope Pile', {}).get('Level', 0)):
        envelope_pile_precharged = '(Precharged)'
    else:
        envelope_pile_precharged = ''
    costReduction_Advices["Uncapped"].append(Advice(
        label=f"Sigil: Envelope Pile {envelope_pile_precharged}",
        picture_class="envelope-pile",
        progression=session_data.account.alchemy_p2w.get("Sigils", {}).get("Envelope Pile", {}).get("PrechargeLevel", 0),
        goal=3
    ))
    costReduction_Advices["Uncapped"].append(Advice(
        label=f"Artifact: Chilled Yarn increases sigil by {1 + session_data.account.artifacts.get('Chilled Yarn', 0)}x",
        picture_class="chilled-yarn",
        progression=session_data.account.artifacts.get("Chilled Yarn", 0),
        goal=4
    ))

    for group_name in costReduction_Advices:
        for advice in costReduction_Advices[group_name]:
            mark_completed(advice)

    # Build the AdviceGroup
    costReduction_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Stamp Cost Reduction",
        advices=costReduction_Advices,
        post_string="",
    )
    return costReduction_AdviceGroup

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
def setStampProgressionTier() -> AdviceSection:
    stamp_AdviceDict = {
        "StampLevels": [],
        "FindStamps": {
            "CombatStamps": {},
            "SkillStamps": {},
            "MiscStamps": {},
        },
        "SpecificStamps": {},
    }
    stamp_AdviceGroupDict = {}
    stamp_AdviceSection = AdviceSection(
        name="Stamps",
        tier="Not Yet Evaluated",
        header="Best Stamp tier met: Not Yet Evaluated. Recommended stamp actions:",
        picture="Stamps_Header.png"
    )

    totalCombatStampLevels = setStampLevels(0)
    totalSkillStampLevels = setStampLevels(1)
    totalMiscStampLevels = setStampLevels(2)
    totalAllStampLevels = totalCombatStampLevels + totalSkillStampLevels + totalMiscStampLevels
    playerPriorityStamps = setPriorityStamps()
    missingStampsDict = setMissingStamps(playerPriorityStamps)
    capacityExclusionsDict = getCapacityExclusions(playerPriorityStamps)
    tier_StampLevels = 0
    tier_RequiredCombatStamps = 0
    tier_RequiredSkillStamps = 0
    tier_RequiredMiscStamps = 0
    tier_RequiredSpecificStamps = 0
    max_tier = stamps_progressionTiers[-1][0]
    adviceCountsDict = {"CombatStamps": 0, "SkillStamps": 0, "MiscStamps": 0, "SpecificStamps": 0}

    for tier in stamps_progressionTiers:
        # TotalLevelStamps
        if tier_StampLevels == (tier[0] - 1):
            if totalAllStampLevels >= tier[1]:  # int
                tier_StampLevels = tier[0]
            else:
                advice_StampLevels = tier[1]
                stamp_AdviceDict["StampLevels"].append(
                    Advice(
                        label="Total Stamp Levels",
                        picture_class="stat-graph-stamp",
                        progression=totalAllStampLevels,
                        goal=advice_StampLevels)
                )

        # CombatStamps
        allCombatStamps = True
        for rStamp in tier[2]:
            #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingCombatStamps}")
            if getReadableStampName(rStamp, "Combat") in missingStampsDict:
                allCombatStamps = False
                subgroupName = f"To reach Old Tier {tier[0]}"
                if subgroupName not in stamp_AdviceDict["FindStamps"]["CombatStamps"] and len(stamp_AdviceDict["FindStamps"]["CombatStamps"]) < maxTiersPerGroup:
                    stamp_AdviceDict["FindStamps"]["CombatStamps"][subgroupName] = []
                if subgroupName in stamp_AdviceDict["FindStamps"]["CombatStamps"]:
                    adviceCountsDict["CombatStamps"] += 1
                    stamp_AdviceDict["FindStamps"]["CombatStamps"][subgroupName].append(
                        Advice(
                            label=getReadableStampName(int(rStamp), "Combat"),
                            picture_class=getReadableStampName(int(rStamp), "Combat"))
                    )
        if tier_RequiredCombatStamps == (tier[0] - 1) and allCombatStamps == True:  # Only update if they already met previous tier
            tier_RequiredCombatStamps = tier[0]

        # SkillStamps
        allSkillStamps = True
        for rStamp in tier[3]:
            #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingSkillStamps}")
            if getReadableStampName(rStamp, "Skill") in missingStampsDict:
                allSkillStamps = False
                subgroupName = f"To reach Old Tier {tier[0]}"
                if subgroupName not in stamp_AdviceDict["FindStamps"]["SkillStamps"] and len(stamp_AdviceDict["FindStamps"]["SkillStamps"]) < maxTiersPerGroup:
                    stamp_AdviceDict["FindStamps"]["SkillStamps"][subgroupName] = []
                if subgroupName in stamp_AdviceDict["FindStamps"]["SkillStamps"]:
                    adviceCountsDict["SkillStamps"] += 1
                    stamp_AdviceDict["FindStamps"]["SkillStamps"][subgroupName].append(
                        Advice(
                            label=getReadableStampName(int(rStamp), "Skill"),
                            picture_class=getReadableStampName(int(rStamp), "Skill"))
                    )
        if tier_RequiredSkillStamps == (tier[0] - 1) and allSkillStamps == True:  # Only update if they already met previous tier
            tier_RequiredSkillStamps = tier[0]

        # MiscStamps
        allMiscStamps = True
        for rStamp in tier[4]:
            #logger.debug(f"{rStamp} {missingCombatStamps} {rStamp in missingMiscStamps}")
            if getReadableStampName(rStamp, "Misc") in missingStampsDict:
                allMiscStamps = False
                subgroupName = f"To reach Old Tier {tier[0]}"
                if subgroupName not in stamp_AdviceDict["FindStamps"]["MiscStamps"] and len(stamp_AdviceDict["FindStamps"]["MiscStamps"]) < maxTiersPerGroup:
                    stamp_AdviceDict["FindStamps"]["MiscStamps"][subgroupName] = []
                if subgroupName in stamp_AdviceDict["FindStamps"]["MiscStamps"]:
                    adviceCountsDict["MiscStamps"] += 1
                    stamp_AdviceDict["FindStamps"]["MiscStamps"][subgroupName].append(
                        Advice(
                            label=getReadableStampName(int(rStamp), "Misc"),
                            picture_class=getReadableStampName(int(rStamp), "Misc"),
                            )
                    )
        if tier_RequiredMiscStamps == (tier[0] - 1) and allMiscStamps == True:  # Only update if they already met previous tier
            tier_RequiredMiscStamps = tier[0]

        # SpecificStampLevels
        requiredSpecificStamps = tier[5]  # dictionary
        allSpecificStamps = True
        for key, value in requiredSpecificStamps.items():
            #logger.debug(f"{tier[0]}, {playerPriorityStamps[key]}, {requiredSpecificStamps[key]}, {playerPriorityStamps[key] >= requiredSpecificStamps[key]}")
            if playerPriorityStamps[key] < requiredSpecificStamps[key]:
                if capacityExclusionsDict.get(key, 0) == 0:  #Check to see if this is a capacity-increasing stamp, and if it skipping it is set to False
                    allSpecificStamps = False
                    subgroupName = f"To reach Tier {tier[0]}"
                    if subgroupName not in stamp_AdviceDict["SpecificStamps"] and len(stamp_AdviceDict["SpecificStamps"]) < maxTiersPerGroup:
                        stamp_AdviceDict["SpecificStamps"][subgroupName] = []
                    if subgroupName in stamp_AdviceDict["SpecificStamps"]:
                        adviceCountsDict["SpecificStamps"] += 1
                        stamp_AdviceDict["SpecificStamps"][subgroupName].append(
                            Advice(
                                label=str(key),
                                picture_class=str(key),
                                progression=playerPriorityStamps[key],
                                goal=requiredSpecificStamps[key])
                        )

        if tier_RequiredSpecificStamps == (tier[0] - 1) and allSpecificStamps == True:
            tier_RequiredSpecificStamps = tier[0]

    # overall_StampTier = min(max_tier, tier_StampLevels, tier_RequiredCombatStamps, tier_RequiredSkillStamps,
    #                         tier_RequiredMiscStamps, tier_RequiredSpecificStamps)
    overall_StampTier = min(max_tier, tier_StampLevels, tier_RequiredSpecificStamps)

    # Generate AdviceGroups
    # Overall Stamp Levels
    stamp_AdviceGroupDict["StampLevels"] = AdviceGroup(
        tier=tier_StampLevels,
        pre_string="Improve your total stamp levels",
        advices=stamp_AdviceDict["StampLevels"]
    )
    # Specific High-Priority Stamps
    stamp_AdviceGroupDict["SpecificStamps"] = AdviceGroup(
        tier=str(tier_RequiredSpecificStamps),
        pre_string=f"Improve high-priority stamp{pl([''] * adviceCountsDict['SpecificStamps'])}",
        advices=stamp_AdviceDict["SpecificStamps"])

    # Collect stamps are now info-only as of 2.07
    # Combat Stamps
    # stamp_AdviceGroupDict["FindStamps"] = AdviceGroup(
    #     tier='',
    #     pre_string=f"Info only- Find all stamps",
    #     advices=stamp_AdviceDict["FindStamps"],
    #     post_string="As of 2.07's Sacred Methods Bundle, turning in ALL stamps can be detrimental. I no longer recommend nor require you do so.")
    stamp_AdviceGroupDict["CombatStamps"] = AdviceGroup(
        tier='',  #str(tier_RequiredCombatStamps),
        pre_string=f"Collect the following Combat stamp{pl([''] * adviceCountsDict['CombatStamps'])}",
        advices=stamp_AdviceDict["FindStamps"]['CombatStamps'],
        post_string="As of 2.07's Sacred Methods Bundle, turning in ALL stamps can be detrimental. I no longer recommend nor require you do so.")
    # Skill Stamps
    stamp_AdviceGroupDict["SkillStamps"] = AdviceGroup(
        tier='',  #str(tier_RequiredSkillStamps),
        pre_string=f"Collect the following Skill stamp{pl([''] * adviceCountsDict['SkillStamps'])}",
        advices=stamp_AdviceDict["FindStamps"]["SkillStamps"],
        post_string="As of 2.07's Sacred Methods Bundle, turning in ALL stamps can be detrimental. I no longer recommend nor require you do so.")
    # Misc Stamps
    stamp_AdviceGroupDict["MiscStamps"] = AdviceGroup(
        tier='',  #str(tier_RequiredMiscStamps),
        pre_string=f"Collect the following Misc stamp{pl([''] * adviceCountsDict['MiscStamps'])}",
        advices=stamp_AdviceDict["FindStamps"]["MiscStamps"],
        post_string="As of 2.07's Sacred Methods Bundle, turning in ALL stamps can be detrimental. I no longer recommend nor require you do so."
    )

    # Capacity
    stamp_AdviceGroupDict["Capacity"] = getCapacityAdviceGroup(playerPriorityStamps)
    stamp_AdviceGroupDict["CostReduction"] = getCostReductionAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_StampTier}/{max_tier}"
    stamp_AdviceSection.pinchy_rating = overall_StampTier
    stamp_AdviceSection.tier = tier_section
    stamp_AdviceSection.groups = stamp_AdviceGroupDict.values()
    if overall_StampTier == max_tier:
        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}. You've reached the end of the recommendations. Let me know what important stamps you're aiming for next!"
    else:
        stamp_AdviceSection.header = f"Best Stamp tier met: {tier_section}"

    return stamp_AdviceSection
