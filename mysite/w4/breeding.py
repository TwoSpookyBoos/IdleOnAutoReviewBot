import copy
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import safe_loads
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfArtifacts, numberOfArtifactTiers, breeding_progressionTiers, getReadableVialNames

logger = get_logger(__name__)
shinyDaysList = [0, 3, 11, 33, 85, 200, 448, 964, 2013, 4107, 8227, 16234, 31633, 60989, 116522, 999999999]

def getShinyLevelFromDays(days: float) -> int:
    shinyLevel = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            shinyLevel += 1
        else:
            break
    return shinyLevel

def getDaysToNextShinyLevel(days: float) -> float:
    shinyLevel = 0
    for requirement in shinyDaysList:
        if float(days) > requirement:
            shinyLevel += 1
    #logger.debug(f"Input days of {days} found to be less than {shinyDaysList[highestExceeded]} by {shinyDaysList[highestExceeded] - float(days)} days")
    daysRemaining = shinyDaysList[shinyLevel] - float(days)
    return daysRemaining

def getShinyExclusions():
    shinyExclusionsDict = {
        "Exclude-InfiniteStarSigns": True,
        "Exclude-Sailing": False,
        "Exclude-Critters": False,
        "Exclude-ShinySpeed": False
        }

    # if Infinite Star Signs are unlocked, set False (as in False, the recommendation should NOT be excluded), otherwise default True
    if session_data.account.infinite_stars_unlocked:
        shinyExclusionsDict["Exclude-InfiniteStarSigns"] = False

    # if all artifacts are Eldritch tier, append True (as in True, the recommendation SHOULD be excluded), otherwise False
    try:
        sum_sailingArtifacts = sum(safe_loads(session_data.account.raw_data["Sailing"])[3])
        if sum_sailingArtifacts >= (numberOfArtifacts * numberOfArtifactTiers):
            shinyExclusionsDict["Exclude-Sailing"] = True
    except Exception as reason:
        logger.exception(f"Unable to get Sailing Artifacts: {reason}")

    try:
        critterVialsList = [
            getReadableVialNames(23),  #Crabbo
            getReadableVialNames(31),  #Mousey
            getReadableVialNames(37),  #Bunny
            getReadableVialNames(40),  #Honker
            getReadableVialNames(47),  #Blobfish
            getReadableVialNames(74),  #Tuttle
        ]
        alchemyVialsDict = session_data.account.alchemy_vials
        for vialName in critterVialsList:
            if alchemyVialsDict.get(vialName, 0) < 13:
                break
            elif vialName == critterVialsList[-1]:
                shinyExclusionsDict["Exclude-Critters"] = True
    except:
        logger.exception(f"Unable to get Critter Vials. Defaulting to INCLUDE Base Critter shiny pets.")

    shinyExclusionsDict["Exclude-ShinySpeed"] = "Science Crayon" in session_data.account.jade_emporium_purchases

    return shinyExclusionsDict

def getTerritoryName(territoryIndex: int) -> str:
    territoryNames = ["", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers",
                      "Desert Oasis", "Beach Docks", "Coarse Mountains", "Twilight Desert", "The Crypt",
                      "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake",
                      "Nebulon Mantle", "Starfield Skies", "Shores of Eternity",
                      "Molten Bay", "Smokey Lake", "Wurm Catacombs",
                      "Spirit Fields", "Bamboo Forest", "Lullaby Airways", "Dharma Mesa"]
    try:
        return territoryNames[int(territoryIndex)]
    except:
        return "Unknown Territory" + str(territoryIndex)

def getSpiceImage(territoryIndex: int) -> str:
    spiceImageNames = ["", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers",
                      "Desert Oasis", "Beach Docks", "Coarse Mountains", "Twilight Desert", "The Crypt",
                      "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake",
                      "Nebulon Mantle", "Starfield Skies", "Shores of Eternity",
                      "Molten Bay", "Smokey Lake", "Wurm Catacombs",
                      "Spirit Fields", "Bamboo Forest", "Lullaby Airways", "Dharma Mesa"]
    try:
        return f"{spiceImageNames[int(territoryIndex)]}-spice"
    except:
        return "UnknownSpice" + str(territoryIndex)

def parseJSONtoBreedingDict() -> dict:
    maxNumberOfTerritories = 24  # as of w6 launch
    indexFirstTerritoryAssignedPet = 28
    try:
        rawBreedingList = safe_loads(session_data.account.raw_data["Breeding"])
    except Exception as reason:
        logger.exception(f"Could not load \"Breeding\" from JSON: {reason}")
        return {}

    try:
        rawTerritoriesList = safe_loads(session_data.account.raw_data["Territory"])
    except Exception as reason:
        logger.exception(f"Could not load \"Territory\" from JSON: {reason}")
        return {}

    rawPets: list = []
    anyPetsAssignedPerTerritory: list[bool] = []
    try:
        rawPets = safe_loads(session_data.account.raw_data["Pets"])
    except Exception as reason:
        logger.exception(f"Could not load \"Pets\" from JSON: {reason}")
        # Can use the spice progress instead later on. Not absolutely required.

    if rawPets != []:
        for territoryIndex in range(0, maxNumberOfTerritories):
            try:
                if rawPets[indexFirstTerritoryAssignedPet + 0 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 1 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 2 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                elif rawPets[indexFirstTerritoryAssignedPet + 3 + (territoryIndex * 4)][0] != "none":
                    anyPetsAssignedPerTerritory.append(True)
                else:
                    anyPetsAssignedPerTerritory.append(False)
            except:
                logger.debug(f"Unable to retrieve assigned pet name. Setting territoryIndex {territoryIndex} aka {getTerritoryName(territoryIndex+1)} to locked.")
                anyPetsAssignedPerTerritory.append(False)
            #logger.debug(f"Result of territoryIndex {territoryIndex} aka {getTerritoryName(territoryIndex+1)}: {anyPetsAssignedPerTerritory[-1]}")

    arenaMaxWave = 0
    petSlotsUnlocked = 2
    try:
        arenaMaxWave = session_data.account.raw_data["OptLacc"][89]
        slotUnlockWavesList = [2, 15, 50, 125]
        for requirement in slotUnlockWavesList:
            if arenaMaxWave > requirement:
                petSlotsUnlocked += 1
    except Exception as reason:
        logger.exception(f"Unable to retrieve \"OptLacc\" from JSON to get Arena Max Wave: {reason}")

    parsedBreedingDict = {}
    if rawBreedingList != []:
        # Straight data grabs
        parsedBreedingDict = {
            "W1 Unlocked Count": rawBreedingList[1][0],
            "W2 Unlocked Count": rawBreedingList[1][1],
            "W3 Unlocked Count": rawBreedingList[1][2],
            "W4 Unlocked Count": rawBreedingList[1][3],
            "W5 Unlocked Count": rawBreedingList[1][4],
            "W6 Unlocked Count": rawBreedingList[1][5],
            "W7 Unlocked Count": rawBreedingList[1][6],
            "W8 Unlocked Count": rawBreedingList[1][7],
            "Abilities": {},
            "Species": {},
            "W1 Shiny Days": rawBreedingList[22],
            "W2 Shiny Days": rawBreedingList[23],
            "W3 Shiny Days": rawBreedingList[24],
            "W4 Shiny Days": rawBreedingList[25],
            "W5 Shiny Days": rawBreedingList[26],
            "W6 Shiny Days": rawBreedingList[27],
            "W7 Shiny Days": rawBreedingList[28],
            "W8 Shiny Days": rawBreedingList[29],
            "Total Shiny Levels": {},
            "Grouped Bonus": {},

            "Highest Arena Wave": arenaMaxWave,
            "Pet Slots Unlocked": petSlotsUnlocked
            }

        # Data needing some logic behind it
        parsedBreedingDict["Total Unlocked Count"] = (parsedBreedingDict["W1 Unlocked Count"]
                                                      + parsedBreedingDict["W2 Unlocked Count"]
                                                      + parsedBreedingDict["W3 Unlocked Count"]
                                                      + parsedBreedingDict["W4 Unlocked Count"])
                                                      #+ parsedBreedingDict["W5 Unlocked Count"]
                                                      #+ parsedBreedingDict["W6 Unlocked Count"]
                                                      # + parsedBreedingDict["W7 Unlocked Count"]
                                                      # + parsedBreedingDict["W8 Unlocked Count"]

        abilitiesList: list[str] = ["Fighter", "Defender", "Forager", "Fleeter", "Breeder", "Special", "Mercenary", "Boomer",
                                    "Sniper", "Amplifier", "Tsar", "Rattler", "Cursory", "Fastidious", "Flashy", "Opticular",
                                    "Monolithic", "Alchemic", "Badumdum", "Defstone", "Targeter", "Looter", "Refiller", "Eggshell",
                                    "Lazarus", "Trasher", "Miasma", "Converter", "Heavyweight", "Fastihoop", "Ninja",
                                    "Superboomer", "Peapeapod", "Borger"]
        for ability in abilitiesList:
            parsedBreedingDict["Abilities"][ability] = False

        shinyBonusList: list[str] = [
            "Faster Shiny Pet Lv Up Rate", "Infinite Star Signs", "Total Damage", "Drop Rate", "Base Efficiency for All Skills",
            "Base WIS", "Base STR", "Base AGI", "Base LUK", "Class EXP", "Skill EXP",
            "Tab 1 Talent Pts", "Tab 2 Talent Pts", "Tab 3 Talent Pts", "Tab 4 Talent Pts", "Star Talent Pts",
            "Faster Refinery Speed", "Base Critter Per Trap", "Multikill Per Tier",
            "Bonuses from All Meals", "Line Width in Lab",
            "Higher Artifact Find Chance", "Sail Captain EXP Gain", "Lower Minimum Travel Time for Sailing",
            "Farming EXP", "Summoning EXP"]
        for bonus in shinyBonusList:
            parsedBreedingDict["Total Shiny Levels"][bonus] = 0

        speciesDict = {
            "W1 Unlocked Species": {
                "Green Mushroom": [
                    "Fighter",  # [0] = Genetic
                    parsedBreedingDict["W1 Unlocked Count"] >= 1,  # [1] = Pet unlock status
                    "Faster Shiny Pet Lv Up Rate",  # [2] = Pet shiny bonus name
                    getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][0]),  # [3] = Pet shiny bonus level
                    parsedBreedingDict["W1 Shiny Days"][0],  # [4] = Pet shiny bonus days
                    getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][0])  # [5] = Pet days to next shiny bonus level
                ],
                "Squirrel": ["Forager", parsedBreedingDict["W1 Unlocked Count"] >= 2, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][1]), parsedBreedingDict["W1 Shiny Days"][1], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][1])],
                "Frog": ["Boomer", parsedBreedingDict["W1 Unlocked Count"] >= 3, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][2]), parsedBreedingDict["W1 Shiny Days"][2], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][2])],
                "Bored Bean": ["Fleeter", parsedBreedingDict["W1 Unlocked Count"] >= 4, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][3]), parsedBreedingDict["W1 Shiny Days"][3], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][3])],
                "Red Mushroom": ["Fighter", parsedBreedingDict["W1 Unlocked Count"] >= 5, "Bonuses from All Meals", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][4]), parsedBreedingDict["W1 Shiny Days"][4], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][4])],
                "Slime": ["Cursory", parsedBreedingDict["W1 Unlocked Count"] >= 6, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][5]), parsedBreedingDict["W1 Shiny Days"][5], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][5])],
                "Piggo": ["Amplifier", parsedBreedingDict["W1 Unlocked Count"] >= 7, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][6]), parsedBreedingDict["W1 Shiny Days"][6], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][6])],
                "Baby Boa": ["Targeter", parsedBreedingDict["W1 Unlocked Count"] >= 8, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][7]), parsedBreedingDict["W1 Shiny Days"][7], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][7])],
                "Carrotman": ["Mercenary", parsedBreedingDict["W1 Unlocked Count"] >= 9, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][8]), parsedBreedingDict["W1 Shiny Days"][8], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][8])],
                "Glublin": ["Refiller", parsedBreedingDict["W1 Unlocked Count"] >= 10, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][9]), parsedBreedingDict["W1 Shiny Days"][9], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][9])],
                "Wode Board": ["Miasma", parsedBreedingDict["W1 Unlocked Count"] >= 11, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][10]), parsedBreedingDict["W1 Shiny Days"][10], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][10])],
                "Gigafrog": ["Amplifier", parsedBreedingDict["W1 Unlocked Count"] >= 12, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][11]), parsedBreedingDict["W1 Shiny Days"][11], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][11])],
                "Wild Boar": ["Heavyweight", parsedBreedingDict["W1 Unlocked Count"] >= 13, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][12]), parsedBreedingDict["W1 Shiny Days"][12], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][12])],
                "Walking Stick": ["Refiller", parsedBreedingDict["W1 Unlocked Count"] >= 14, "Base Critter Per Trap", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][13]), parsedBreedingDict["W1 Shiny Days"][13], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][13])],
                "Nutto": ["Borger", parsedBreedingDict["W1 Unlocked Count"] >= 15, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][14]), parsedBreedingDict["W1 Shiny Days"][14], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][14])],
                "Poop": ["Tsar", parsedBreedingDict["W1 Unlocked Count"] >= 16, "Farming EXP", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][15]), parsedBreedingDict["W1 Shiny Days"][15], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][15])],
                "Rat": ["Monolithic", parsedBreedingDict["W1 Unlocked Count"] >= 17, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["W1 Shiny Days"][16]), parsedBreedingDict["W1 Shiny Days"][16], getDaysToNextShinyLevel(parsedBreedingDict["W1 Shiny Days"][16])]
                },
            "W2 Unlocked Species": {
                "Sandy Pot": ["Looter", parsedBreedingDict["W2 Unlocked Count"] >= 1, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][0]), parsedBreedingDict["W2 Shiny Days"][0], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][0])],
                "Mimic": ["Defender", parsedBreedingDict["W2 Unlocked Count"] >= 2, "Tab 1 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][1]), parsedBreedingDict["W2 Shiny Days"][1], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][1])],
                "Crabcake": ["Fleeter", parsedBreedingDict["W2 Unlocked Count"] >= 3, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][2]), parsedBreedingDict["W2 Shiny Days"][2], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][2])],
                "Mafioso": ["Forager", parsedBreedingDict["W2 Unlocked Count"] >= 4, "Tab 2 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][3]), parsedBreedingDict["W2 Shiny Days"][3], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][3])],
                "Mallay": ["Opticular", parsedBreedingDict["W2 Unlocked Count"] >= 5, "Line Width in Lab", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][4]), parsedBreedingDict["W2 Shiny Days"][4], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][4])],
                "Sand Castle": ["Defstone", parsedBreedingDict["W2 Unlocked Count"] >= 6, "Base STR", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][5]), parsedBreedingDict["W2 Shiny Days"][5], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][5])],
                "Pincermin": ["Fighter", parsedBreedingDict["W2 Unlocked Count"] >= 7, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][6]), parsedBreedingDict["W2 Shiny Days"][6], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][6])],
                "Mashed Potato": ["Amplifier", parsedBreedingDict["W2 Unlocked Count"] >= 8, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][7]), parsedBreedingDict["W2 Shiny Days"][7], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][7])],
                "Tyson": ["Fastidious", parsedBreedingDict["W2 Unlocked Count"] >= 9, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][8]), parsedBreedingDict["W2 Shiny Days"][8], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][8])],
                "Whale": ["Badumdum", parsedBreedingDict["W2 Unlocked Count"] >= 10, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][9]), parsedBreedingDict["W2 Shiny Days"][9], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][9])],
                "Moonmoon": ["Mercenary", parsedBreedingDict["W2 Unlocked Count"] >= 11, "Base WIS", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][10]), parsedBreedingDict["W2 Shiny Days"][10], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][10])],
                "Sand Giant": ["Rattler", parsedBreedingDict["W2 Unlocked Count"] >= 12, "Base Efficiency for All Skills", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][11]), parsedBreedingDict["W2 Shiny Days"][11], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][11])],
                "Snelbie": ["Monolithic", parsedBreedingDict["W2 Unlocked Count"] >= 13, "Tab 4 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][12]), parsedBreedingDict["W2 Shiny Days"][12], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][12])],
                "Dig Doug": ["Lazarus", parsedBreedingDict["W2 Unlocked Count"] >= 14, "Farming EXP", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][13]), parsedBreedingDict["W2 Shiny Days"][13], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][13])],
                "Beefie": ["Trasher", parsedBreedingDict["W2 Unlocked Count"] >= 15, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][14]), parsedBreedingDict["W2 Shiny Days"][14], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][14])],
                "Crescent Spud": ["Monolithic", parsedBreedingDict["W2 Unlocked Count"] >= 16, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][15]), parsedBreedingDict["W2 Shiny Days"][15], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][15])],
                "Chippy": ["Eggshell", parsedBreedingDict["W2 Unlocked Count"] >= 17, "Summoning EXP", getShinyLevelFromDays(parsedBreedingDict["W2 Shiny Days"][16]), parsedBreedingDict["W2 Shiny Days"][16], getDaysToNextShinyLevel(parsedBreedingDict["W2 Shiny Days"][16])]
                },
            "W3 Unlocked Species": {
                "Sheepie": ["Sniper", parsedBreedingDict["W3 Unlocked Count"] >= 1, "Bonuses from All Meals", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][0]), parsedBreedingDict["W3 Shiny Days"][0], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][0])],
                "Frost Flake": ["Ninja", parsedBreedingDict["W3 Unlocked Count"] >= 2, "Tab 3 Talent Pts", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][1]), parsedBreedingDict["W3 Shiny Days"][1], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][1])],
                "Sir Stache": ["Eggshell", parsedBreedingDict["W3 Unlocked Count"] >= 3, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][2]), parsedBreedingDict["W3 Shiny Days"][2], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][2])],
                "Xylobone": ["Opticular", parsedBreedingDict["W3 Unlocked Count"] >= 4, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][3]), parsedBreedingDict["W3 Shiny Days"][3], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][3])],
                "Bunny": ["Flashy", parsedBreedingDict["W3 Unlocked Count"] >= 5, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][4]), parsedBreedingDict["W3 Shiny Days"][4], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][4])],
                "Bloque": ["Alchemic", parsedBreedingDict["W3 Unlocked Count"] >= 6, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][5]), parsedBreedingDict["W3 Shiny Days"][5], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][5])],
                "Mamooth": ["Looter", parsedBreedingDict["W3 Unlocked Count"] >= 7, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][6]), parsedBreedingDict["W3 Shiny Days"][6], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][6])],
                "Snowman": ["Defstone", parsedBreedingDict["W3 Unlocked Count"] >= 8, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][7]), parsedBreedingDict["W3 Shiny Days"][7], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][7])],
                "Penguin": ["Fastidious", parsedBreedingDict["W3 Unlocked Count"] >= 9, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][8]), parsedBreedingDict["W3 Shiny Days"][8], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][8])],
                "Thermister": ["Sniper", parsedBreedingDict["W3 Unlocked Count"] >= 10, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][9]), parsedBreedingDict["W3 Shiny Days"][9], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][9])],
                "Quenchie": ["Boomer", parsedBreedingDict["W3 Unlocked Count"] >= 11, "Faster Shiny Pet Lv Up Rate", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][10]), parsedBreedingDict["W3 Shiny Days"][10], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][10])],
                "Cryosnake": ["Eggshell", parsedBreedingDict["W3 Unlocked Count"] >= 12, "Star Talent Pts", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][11]), parsedBreedingDict["W3 Shiny Days"][11], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][11])],
                "Mecho Mouse": ["Trasher", parsedBreedingDict["W3 Unlocked Count"] >= 13, "Base STR", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][12]), parsedBreedingDict["W3 Shiny Days"][12], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][12])],
                "Bop Box": ["Converter", parsedBreedingDict["W3 Unlocked Count"] >= 14, "Infinite Star Signs", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][13]), parsedBreedingDict["W3 Shiny Days"][13], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][13])],
                "Neyeptune": ["Lazarus", parsedBreedingDict["W3 Unlocked Count"] >= 15, "Farming EXP", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][14]), parsedBreedingDict["W3 Shiny Days"][14], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][14])],
                "Dedotated Ram": ["Amplifier", parsedBreedingDict["W3 Unlocked Count"] >= 16, "Multikill Per Tier", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][15]), parsedBreedingDict["W3 Shiny Days"][15], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][15])],
                "Bloodbone": ["Targeter", parsedBreedingDict["W3 Unlocked Count"] >= 17, "Farming EXP", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][16]), parsedBreedingDict["W3 Shiny Days"][16], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][16])],
                "Panda": ["Converter", parsedBreedingDict["W3 Unlocked Count"] >= 18, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["W3 Shiny Days"][17]), parsedBreedingDict["W3 Shiny Days"][17], getDaysToNextShinyLevel(parsedBreedingDict["W3 Shiny Days"][17])]
                },
            "W4 Unlocked Species": {
                "Purp Mushroom": ["Tsar", parsedBreedingDict["W4 Unlocked Count"] >= 1, "Farming EXP", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][0]), parsedBreedingDict["W4 Shiny Days"][0], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][0])],
                "TV": ["Rattler", parsedBreedingDict["W4 Unlocked Count"] >= 2, "Sail Captain EXP Gain", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][1]), parsedBreedingDict["W4 Shiny Days"][1], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][1])],
                "Donut": ["Flashy", parsedBreedingDict["W4 Unlocked Count"] >= 3, "Summoning EXP", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][2]), parsedBreedingDict["W4 Shiny Days"][2], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][2])],
                "Demon Genie": ["Superboomer", parsedBreedingDict["W4 Unlocked Count"] >= 4, "Faster Refinery Speed", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][3]), parsedBreedingDict["W4 Shiny Days"][3], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][3])],
                "Flying Worm": ["Borger", parsedBreedingDict["W4 Unlocked Count"] >= 5, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][4]), parsedBreedingDict["W4 Shiny Days"][4], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][4])],
                "Dog": ["Peapeapod", parsedBreedingDict["W4 Unlocked Count"] >= 6, "Lower Minimum Travel Time for Sailing", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][5]), parsedBreedingDict["W4 Shiny Days"][5], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][5])],
                "Soda Can": ["Fastihoop", parsedBreedingDict["W4 Unlocked Count"] >= 7, "Higher Artifact Find Chance", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][6]), parsedBreedingDict["W4 Shiny Days"][6], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][6])],
                "Gelatinous Cuboid": ["Flashy", parsedBreedingDict["W4 Unlocked Count"] >= 8, "Total Damage", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][7]), parsedBreedingDict["W4 Shiny Days"][7], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][7])],
                "Choccie": ["Superboomer", parsedBreedingDict["W4 Unlocked Count"] >= 9, "Drop Rate", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][8]), parsedBreedingDict["W4 Shiny Days"][8], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][8])],
                "Biggole Wurm": ["Tsar", parsedBreedingDict["W4 Unlocked Count"] >= 10, "Class EXP", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][9]), parsedBreedingDict["W4 Shiny Days"][9], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][9])],
                "Cool Bird": ["Borger", parsedBreedingDict["W4 Unlocked Count"] >= 11, "Base STR", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][10]), parsedBreedingDict["W4 Shiny Days"][10], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][10])],
                "Clammie": ["Mercenary", parsedBreedingDict["W4 Unlocked Count"] >= 12, "Skill EXP", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][11]), parsedBreedingDict["W4 Shiny Days"][11], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][11])],
                "Octodar": ["Cursory", parsedBreedingDict["W4 Unlocked Count"] >= 13, "Base Critter Per Trap", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][12]), parsedBreedingDict["W4 Shiny Days"][12], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][12])],
                "Flombeige": ["Trasher", parsedBreedingDict["W4 Unlocked Count"] >= 14, "Base AGI", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][13]), parsedBreedingDict["W4 Shiny Days"][13], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][13])],
                "Stilted Seeker": ["Borger", parsedBreedingDict["W4 Unlocked Count"] >= 15, "Base WIS", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][14]), parsedBreedingDict["W4 Shiny Days"][14], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][14])],
                "Hedgehog": ["Peapeapod", parsedBreedingDict["W4 Unlocked Count"] >= 16, "Base LUK", getShinyLevelFromDays(parsedBreedingDict["W4 Shiny Days"][15]), parsedBreedingDict["W4 Shiny Days"][15], getDaysToNextShinyLevel(parsedBreedingDict["W4 Shiny Days"][15])]
                }
            }

        parsedBreedingDict["Species"] = speciesDict
        for world in speciesDict:
            for species in speciesDict[world]:
                if speciesDict[world][species][1] == True and parsedBreedingDict["Abilities"][speciesDict[world][species][0]] == False:
                    parsedBreedingDict["Abilities"][speciesDict[world][species][0]] = True
                if speciesDict[world][species][3] > 0:
                    parsedBreedingDict["Total Shiny Levels"][speciesDict[world][species][2]] += speciesDict[world][species][3]
                if speciesDict[world][species][2] in parsedBreedingDict["Grouped Bonus"].keys():
                    parsedBreedingDict["Grouped Bonus"][speciesDict[world][species][2]].append((species, speciesDict[world][species][3], speciesDict[world][species][5]))
                else:
                    parsedBreedingDict["Grouped Bonus"][speciesDict[world][species][2]] = [(species, speciesDict[world][species][3], speciesDict[world][species][5])]
        for groupedBonus in parsedBreedingDict["Grouped Bonus"]:
            parsedBreedingDict["Grouped Bonus"][groupedBonus].sort(key=lambda x: float(x[2]))

        parsedBreedingDict["Highest Unlocked Territory"] = 0
        for index in range(0, maxNumberOfTerritories):
            # Spice Progress above 0 or any pet assigned to territory
            if rawTerritoriesList[index][0] > 0 or anyPetsAssignedPerTerritory[index] == True:
                parsedBreedingDict["Highest Unlocked Territory"] = index+1
                #logger.debug(f"Increasing Territories Unlocked Count for {getTerritoryName(index+1)}")
    else:
        return {}

    #for element in parsedBreedingDict:
        #print("Breeding.parseJSON~ OUTPUT parsedBreedingDict[\"", element, "\"]:", parsedBreedingDict[element])
    return parsedBreedingDict

def setBreedingProgressionTier() -> AdviceSection:
    breeding_AdviceDict = {
        "UnlockedTerritories": {"Unlock more Spice Territories": [], "Recommended Territory Team (Left to Right)": []},
        "MaxArenaWave": {"Recommended Arena Team (Left to Right)": []},
        "ShinyLevels": {},
        "ShinyLevelsTierList": {}
    }
    breeding_AdviceGroupDict = {}
    breeding_AdviceSection = AdviceSection(
        name="Breeding",
        tier="Not Yet Evaluated",
        header="Best Breeding tier met: Not Yet Evaluated. Recommended breeding actions:",
        picture="Breeding.png",
        collapse=False
    )
    highestBreedingLevel = max(session_data.account.all_skills["Breeding"])
    if highestBreedingLevel < 1:
        breeding_AdviceSection.header = "Come back after unlocking the Breeding skill in World 4!"
        breeding_AdviceSection.collapse = True
        return breeding_AdviceSection

    progressionTiersBreeding = copy.deepcopy(breeding_progressionTiers)
    maxBreedingTier = max(progressionTiersBreeding.keys())
    tier_UnlockedTerritories = 0
    tier_MaxArenaWave = 0
    tier_ShinyLevels = 0
    overall_BreedingTier = 0
    nextArenaWaveUnlock = 0
    recommendedTerritoryCompsList: dict[int, list[list[str]]] = {
        0: [
            [],
            []],
        1: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        2: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        3: [
            ['Rattler or Mercenary', 'Cursory', 'Refiller', 'Defender'],
            ['rattler', 'cursory', 'refiller', 'defender']],
        4: [
            ['Rattler', 'Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['rattler', 'monolithic', 'refiller', 'defender', 'refiller']],
        5: [
            ['Rattler', 'Looter', 'Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['rattler', 'looter', 'monolithic', 'refiller', 'defender', 'refiller']],
        6: [
            ['Peapeapod or Rattler', 'Looter', 'Trasher', 'Refiller', 'Refiller', 'Lazarus or Filler'],
            ['peapeapod', 'looter', 'trasher', 'refiller', 'refiller', 'lazarus']]
    }
    recommendedArenaCompsDict: dict[int, list[list[str]]] = {
        # 2-pet comp used to beat Wave 3
        0: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        # 3-pet comp used to beat Wave 15
        1: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        # 4-pet comp used to beat Wave 50
        2: [
            ['Rattler', 'Monolithic', 'Refiller', 'Borger or Defender'],
            ['rattler', 'monolithic', 'refiller', 'borger']],
        # 5-pet comp used to beat Wave 125
        3: [
            ['Rattler', 'Monolithic', 'Looter', 'Refiller', 'Borger'],
            ['rattler', 'monolithic', 'looter', 'refiller', 'borger']],
        # 6-pet comp used to beat Wave 200
        4: [
            ['Rattler', 'Defender', 'Looter', 'Refiller', 'Badumdum', 'Borger'],
            ['rattler', 'defender', 'looter', 'refiller', 'badumdum', 'borger']]
    }
    shinyPetsTierList = {
        "S": ['Bonuses from All Meals', 'Base Efficiency for All Skills', 'Drop Rate'],
        "A": ['Multikill Per Tier', 'Infinite Star Signs', 'Faster Refinery Speed', 'Farming EXP', 'Base Critter Per Trap'],
        "B": ['Lower Minimum Travel Time for Sailing', 'Higher Artifact Find Chance', 'Tab 4 Talent Pts', 'Star Talent Pts', 'Faster Shiny Pet Lv Up Rate'],
        "C": ['Skill EXP', 'Base WIS', 'Base STR', 'Base AGI', 'Base LUK'],
        "D": ['Summoning EXP', 'Sail Captain EXP Gain', 'Total Damage', 'Tab 1-3 Talent Pts'],
        "F": ['Class EXP', 'Line Width in Lab']
    }

    failedShinyRequirements = []
    failedShinyBonus = {}
    #advice_ShinyPets = []
    breedingDict = parseJSONtoBreedingDict()
    shinyExclusionsDict = getShinyExclusions()
    if breedingDict == {}:
        breeding_AdviceSection.header = "Breeding info could not be read from your save data :( Please file a bug report if you have Breeding unlocked"
        return breeding_AdviceSection
    else:
        if shinyExclusionsDict["Exclude-Sailing"] == True:
            if "Lower Minimum Travel Time for Sailing" in shinyPetsTierList["B"]:
                shinyPetsTierList["B"].remove("Lower Minimum Travel Time for Sailing")
                shinyPetsTierList["F"].append("Lower Minimum Travel Time for Sailing")
            if "Higher Artifact Find Chance" in shinyPetsTierList["B"]:
                shinyPetsTierList["B"].remove("Higher Artifact Find Chance")
                shinyPetsTierList["F"].append("Higher Artifact Find Chance")
        if shinyExclusionsDict["Exclude-Critters"] == True:
            if "Base Critter Per Trap" in shinyPetsTierList["A"]:
                shinyPetsTierList["A"].remove('Base Critter Per Trap')
                shinyPetsTierList["D"].append('Base Critter Per Trap')
        if shinyExclusionsDict["Exclude-ShinySpeed"] == True:
            if "Faster Shiny Pet Lv Up Rate" in shinyPetsTierList["B"]:
                shinyPetsTierList["B"].remove('Faster Shiny Pet Lv Up Rate')
                shinyPetsTierList["D"].append('Faster Shiny Pet Lv Up Rate')

        for tier in progressionTiersBreeding:
            if "Infinite Star Signs" in progressionTiersBreeding[tier] and shinyExclusionsDict["Exclude-InfiniteStarSigns"] == True:
                progressionTiersBreeding[tier]["Infinite Star Signs"] = 0
                #logger.debug("Excluding Shiny- Infinite Star Signs because player does not have Rift bonus unlocked.")
            if 'Lower Minimum Travel Time for Sailing' in progressionTiersBreeding[tier] and shinyExclusionsDict["Exclude-Sailing"] == True:
                progressionTiersBreeding[tier]['Lower Minimum Travel Time for Sailing'] = 0
                #logger.debug("Excluding Shiny- Sailing Min Time because player has all Sailing Artifacts discovered.")
            if "Higher Artifact Find Chance" in progressionTiersBreeding[tier] and shinyExclusionsDict["Exclude-Sailing"] == True:
                progressionTiersBreeding[tier]["Higher Artifact Find Chance"] = 0
                #logger.debug("Excluding Shiny- Higher Artifact Find Chance because player has all Sailing Artifacts discovered.")
            if "Faster Shiny Pet Lv Up Rate" in progressionTiersBreeding[tier] and shinyExclusionsDict["Exclude-ShinySpeed"] == True:
                progressionTiersBreeding[tier]["Faster Shiny Pet Lv Up Rate"] = 0


            #Unlocked Territories
            if tier_UnlockedTerritories >= (tier-1):
                if breedingDict["Highest Unlocked Territory"] >= progressionTiersBreeding[tier]["TerritoriesUnlocked"]:
                    tier_UnlockedTerritories = tier
                else:
                    for territoryIndex in range(breedingDict["Highest Unlocked Territory"]+1, progressionTiersBreeding[tier]["TerritoriesUnlocked"]+1):
                        breeding_AdviceDict["UnlockedTerritories"]["Unlock more Spice Territories"].append(
                            Advice(label=getTerritoryName(territoryIndex), picture_class=getSpiceImage(territoryIndex)))
                    for petIndex in range(0, len(recommendedTerritoryCompsList[tier][0])):
                        breeding_AdviceDict["UnlockedTerritories"]["Recommended Territory Team (Left to Right)"].append(
                            Advice(label=recommendedTerritoryCompsList[tier][0][petIndex],
                                   picture_class=recommendedTerritoryCompsList[tier][1][petIndex]))

            #Arena Waves to unlock Pet Slots
            if tier_MaxArenaWave >= (tier-1):
                if breedingDict["Highest Arena Wave"] >= progressionTiersBreeding[tier]["ArenaWaves"]:
                    tier_MaxArenaWave = tier
                else:
                    for petIndex in range(0, len(recommendedArenaCompsDict[tier_MaxArenaWave][0])):
                        breeding_AdviceDict["MaxArenaWave"]["Recommended Arena Team (Left to Right)"].append(
                            Advice(label=recommendedArenaCompsDict[tier_MaxArenaWave][0][petIndex],
                                   picture_class=recommendedArenaCompsDict[tier_MaxArenaWave][1][petIndex]))

            #Shinies
            if tier_ShinyLevels >= (tier-1):
                if len(progressionTiersBreeding[tier]["Shinies"]) == 0:
                    # free pass
                    tier_ShinyLevels = tier
                else:
                    # if there are actual level requirements
                    allRequirementsMet = True
                    for requiredShinyBonusType in progressionTiersBreeding[tier]["Shinies"]:
                        if breedingDict["Total Shiny Levels"][requiredShinyBonusType] < progressionTiersBreeding[tier]["Shinies"][requiredShinyBonusType]:
                            allRequirementsMet = False
                            failedShinyRequirements.append([
                                requiredShinyBonusType,
                                breedingDict["Total Shiny Levels"][requiredShinyBonusType],
                                progressionTiersBreeding[tier]["Shinies"][requiredShinyBonusType]])
                            failedShinyBonus[requiredShinyBonusType] = breedingDict["Grouped Bonus"][requiredShinyBonusType]
                    if allRequirementsMet == True:
                        tier_ShinyLevels = tier
                    else:
                        for failedRequirement in failedShinyRequirements:
                            yuckyDictName = f"{failedRequirement[0]}: {failedRequirement[1]}/{failedRequirement[2]}"
                            if failedRequirement[0] not in breeding_AdviceDict["ShinyLevels"]:
                                breeding_AdviceDict["ShinyLevels"][yuckyDictName] = []
                            for possibleShinyPet in failedShinyBonus[failedRequirement[0]]:
                                breeding_AdviceDict["ShinyLevels"][yuckyDictName].append(
                                    Advice(label=f"{possibleShinyPet[0]}: Level {possibleShinyPet[1]}", picture_class=possibleShinyPet[0],
                                           progression=f"{possibleShinyPet[2]:.2f} days to level", goal=""))

                        # advice_perShinyBonus = ""
                        # for shinyBonus in failedShinyBonus:
                        #     advice_perShinyBonus = shinyBonus + " pets: "
                        #     for pet in failedShinyBonus[shinyBonus]:
                        #         advice_perShinyBonus += "Lv" + str(pet[1]) + " " + pet[0] + ", "
                        #     advice_perShinyBonus = advice_perShinyBonus[:-2]  # trim off final space and comma
                        #     advice_ShinyPets.append(advice_perShinyBonus)

    overall_BreedingTier = min(maxBreedingTier, tier_UnlockedTerritories, tier_ShinyLevels)

    #Generate Advice Groups
    if tier_UnlockedTerritories < maxBreedingTier:
        breeding_AdviceGroupDict["UnlockedTerritories"] = AdviceGroup(
            tier=str(tier_UnlockedTerritories),
            pre_string=f"Unlock {progressionTiersBreeding[tier_UnlockedTerritories+1]['TerritoriesUnlocked'] - breedingDict['Highest Unlocked Territory']} more Spice Territor{pl(breeding_AdviceDict['UnlockedTerritories'], 'y', 'ies')}",
            advices=breeding_AdviceDict["UnlockedTerritories"],
            post_string=""
        )
    if tier_MaxArenaWave != maxBreedingTier:
        nextArenaWaveUnlock = progressionTiersBreeding[tier_MaxArenaWave+1]["ArenaWaves"]
    breeding_AdviceGroupDict["MaxArenaWave"] = AdviceGroup(
        tier=str(tier_MaxArenaWave),
        pre_string=f"Complete Arena Wave {nextArenaWaveUnlock} {pl(5-tier_MaxArenaWave, 'to unlock the final Arena bonus', 'to unlock another pet slot')}",
        advices=breeding_AdviceDict["MaxArenaWave"],
        post_string=""
    )

    if highestBreedingLevel >= 40:
        if tier_ShinyLevels < maxBreedingTier:
            breeding_AdviceGroupDict["ShinyLevels"] = AdviceGroup(
                tier=str(tier_ShinyLevels),
                pre_string=f"Level the following Shiny {pl(breeding_AdviceDict['ShinyLevels'], 'Bonus', 'Bonuses')}",
                advices=breeding_AdviceDict["ShinyLevels"],
                post_string=""
            )
        else:
            for shinyTier in shinyPetsTierList:
                if shinyTier not in breeding_AdviceDict["ShinyLevelsTierList"]:
                    breeding_AdviceDict["ShinyLevelsTierList"][shinyTier] = []
                for shinyPet in shinyPetsTierList[shinyTier]:
                    breeding_AdviceDict["ShinyLevelsTierList"][shinyTier].append(Advice(label=shinyPet, picture_class="")
                                                                                 )
            breeding_AdviceGroupDict["ShinyLevelsTierList"] = AdviceGroup(
                tier="",
                pre_string="Advance Shiny levels per your desires",
                advices=breeding_AdviceDict["ShinyLevelsTierList"],
                post_string=""
            )

    #Generate Advice Section
    tier_section = f"{overall_BreedingTier}/{maxBreedingTier}"
    breeding_AdviceSection.tier = tier_section
    breeding_AdviceSection.pinchy_rating = overall_BreedingTier
    breeding_AdviceSection.groups = breeding_AdviceGroupDict.values()
    if overall_BreedingTier == maxBreedingTier:
        breeding_AdviceSection.header = f"Best Breeding tier met: {tier_section}<br>You best ❤️"
    else:
        breeding_AdviceSection.header = f"Best Breeding tier met: {tier_section}"

    return breeding_AdviceSection
