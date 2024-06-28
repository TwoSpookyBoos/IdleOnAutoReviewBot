import json
import os
from math import floor
from math import ceil

from config import app
from consts import deathNote_progressionTiers
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import safe_loads
from utils.logging import get_logger


logger = get_logger(__name__)
dnSkullRequirementList = [0, 25000, 100000, 250000, 500000, 1000000, 5000000, 100000000, 1000000000]
dnSkullValueList = [0, 1, 2, 3, 4, 5, 7, 10, 20]
reversed_dnSkullRequirementList = dnSkullRequirementList[::-1]
reversed_dnSkullValueList = dnSkullValueList[::-1]

class EnemyWorld:
    def __init__(self, worldnumber: int, mapsdict: dict):
        self.world_number: int = worldnumber
        self.maps_dict: dict = mapsdict
        self.lowest_skulls_dict: dict = {}
        self.lowest_skull_value: int = -1
        self.current_lowest_skull_name: str = "None"
        self.next_lowest_skull_name: str = "Normal Skull"
        for skullValue in dnSkullValueList:
            self.lowest_skulls_dict[skullValue] = []
        if len(mapsdict) > 0:
            for enemy_map_index in self.maps_dict:
                self.lowest_skulls_dict[self.maps_dict[enemy_map_index].skull_mk_value].append(
                    [self.maps_dict[enemy_map_index].map_name,
                     self.maps_dict[enemy_map_index].kills_to_next_skull,
                     self.maps_dict[enemy_map_index].percent_toward_next_skull,
                     self.maps_dict[enemy_map_index].monster_image])
            for skullDict in self.lowest_skulls_dict:
                self.lowest_skulls_dict[skullDict] = sorted(self.lowest_skulls_dict[skullDict], key=lambda item: item[2], reverse=True)
            for skullDict in self.lowest_skulls_dict:
                if len(self.lowest_skulls_dict[skullDict]) > 0:
                    if self.lowest_skull_value == -1:
                        self.lowest_skull_value = skullDict
            self.current_lowest_skull_name = getSkullNames(self.lowest_skull_value)
            self.next_lowest_skull_name = getNextSkullNames(self.lowest_skull_value)

    def __str__(self):
        if self.world_number == 0:
            return "Barbarian Only Extras"
        else:
            return f"World {self.world_number}"


class EnemyMap:
    def __init__(self, mapname: str, monstername: str, mapindex: int, portalrequirement: int, zowrating: str, chowrating: str, meowrating: str, monsterimage: str = ""):
        self.map_name: str = mapname
        self.map_index: int = mapindex
        self.monster_name: str = monstername
        self.portal_requirement: int = portalrequirement
        self.zow_rating: str = zowrating
        self.chow_rating: str = chowrating
        self.meow_rating: str = meowrating
        self.kill_count: float = 0
        self.skull_mk_value: int = 0
        self.skull_name: str = "None"
        self.kills_to_next_skull: int = 0
        self.percent_toward_next_skull: int = 0
        self.zow_dict = {}
        if monsterimage:
            self.monster_image = monsterimage.lower()
        else:
            self.monster_image = monstername

    def __str__(self):
        return self.map_name

    def getRating(self, ratingType: str):
        if ratingType == 'ZOW':
            return self.zow_rating
        elif ratingType == 'CHOW':
            return self.chow_rating
        elif ratingType == 'MEOW':
            return self.meow_rating

    def updateZOWDict(self, characterIndex: int, KLAValue: float):
        if characterIndex not in self.zow_dict:
            self.zow_dict[characterIndex] = {}
        self.zow_dict[characterIndex] = int(abs(float(KLAValue) - self.portal_requirement))

    def addRawKLA(self, additionalKills: float):
        try:
            self.kill_count += abs(float(additionalKills) - self.portal_requirement)
        except Exception as reason:
            logger.warning(f"Unable to add additionalKills value of {type(additionalKills)} {additionalKills} to {self.map_name} because: {reason}")

    def generateDNSkull(self):
        self.kill_count = int(self.kill_count)
        for counter in range(0, len(dnSkullRequirementList)):
            if self.kill_count >= dnSkullRequirementList[counter]:
                self.skull_mk_value = dnSkullValueList[counter]
        self.skull_name = getSkullNames(self.skull_mk_value)
        if self.skull_mk_value == reversed_dnSkullValueList[0]:
            #If map's skull is highest, currently Eclipse Skull, set in defaults
            self.kills_to_next_skull = 0
            self.percent_toward_next_skull = 100
        else:
            for skullValueIndex in range(1, len(reversed_dnSkullValueList)):
                if self.skull_mk_value == reversed_dnSkullValueList[skullValueIndex]:
                    self.kills_to_next_skull = ceil(reversed_dnSkullRequirementList[skullValueIndex-1] - self.kill_count)
                    self.percent_toward_next_skull = floor((self.kill_count / reversed_dnSkullRequirementList[skullValueIndex-1]) * 100)

def getJSONDataFromFile(filePath):
    with open(filePath, 'r') as inputFile:
        jsonData = json.load(inputFile)
    inputFile.close()
    return jsonData

def buildMaps() -> dict[int, dict]:
    mapDict = {
        0: {},
        1: {},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        #7: {},
        #8: {}
    }
    rawMaps = getJSONDataFromFile(os.path.join(app.static_folder, 'enemy-maps.json'))
    for mapData in rawMaps["mapData"]:
        #["Spore Meadows", 1, "Green Mushroom", 11, "Basic W1 Enemies", "Basic W1 Enemies", "Basic W1 Enemies"],
        #mapData[0]: str = map name
        #mapData[1]: int = map index
        #mapData[2]: str = enemy name
        #mapData[3]: int = portal requirement
        #mapData[4]: str = zow rating
        #mapData[5]: str = chow rating
        #mapData[6]: str = meow rating
        if mapData[1] in [30, 9, 38, 69, 120, 166]:
            world = 0
        else:
            world = floor(mapData[1]/50)+1
        mapDict[world][mapData[1]] = EnemyMap(
            mapname=mapData[0],
            mapindex=mapData[1],
            monstername=mapData[2],
            portalrequirement=mapData[3],
            zowrating=mapData[4],
            chowrating=mapData[5],
            meowrating=mapData[6],
            monsterimage=mapData[7])
    return mapDict

def getSkullNames(mkValue: int) -> str:
    skullDict = {
        0: "None",
        1: "Normal Skull",
        2: "Copper Skull",
        3: "Iron Skull",
        4: "Gold Skull",
        5: "Platinum Skull",
        7: "Dementia Skull",
        10: "Lava Skull",
        20: "Eclipse Skull"
    }
    try:
        return skullDict.get(mkValue, f"UnknownSkull{mkValue}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"

def getNextSkullNames(mkValue: int) -> str:
    nextSkullDict = {
        0: "Normal Skull",
        1: "Copper Skull",
        2: "Iron Skull",
        3: "Gold Skull",
        4: "Platinum Skull",
        5: "Dementia Skull",
        7: "Lava Skull",
        10: "Eclipse Skull",
        20: "Finished!"
    }
    try:
        return nextSkullDict.get(mkValue, f"UnknownSkull{mkValue}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"

def getEnemyNameFromMap(inputMap: str) -> str:
    mapNametoEnemyNameDict = {
        # W1 Maps
        "Spore Meadows": "Green Mushroom",
        "Froggy Fields": "Frog",
        "Valley of the Beans": "Bored Bean",
        "Birch Enclave": "Red Mushroom",
        "Jungle Perimeter": "Slime",
        "The Base of the Bark": "Stick",
        "Hollowed Trunk": "Nutto",
        "Where the Branches End": "Wood Mushroom",
        "Winding Willows": "Baby Boa",
        "Vegetable Patch": "Carrotman",
        "Forest Outskirts": "Glublin",
        "Encroaching Forest Villa": "Wode Board",
        "Tucked Away": "Gigafrog",
        "Poopy Sewers": "Poop",
        "Rats Nest": "Rat",
        "The Roots": "Special - Single Nutto at WorshipTD map",
        "The Office": "Special - Poops surrounding Dr.Def",
        "Meel's Crypt": "Special- Boop",

        # W2 Maps
        "Jar Bridge": "Sandy Pot",
        "The Mimic Hole": "Mimic",
        "Dessert Dunes": "Crabcake",
        "The Grandioso Canyon": "Mafioso",
        "Shifty Sandbox": "Sand Castle",
        "Pincer Plateau": "Pincermin",
        "Slamabam Straightaway": "Mashed Potato",
        "The Ring": "Tyson",
        "Up Up Down Down": "Moonmoon",
        "Sands of Time": "Sand Giant",
        "Djonnuttown": "Snelbie",
        "Mummy Memorial": "Special- Invisible Green Mushroom inside King Doot's map",

        # W3 Maps
        "Steep Sheep Ledge": "Sheepie",
        "Snowfield Outskirts": "Frost Flake",
        "The Stache Split": "Sir Stache",
        "Refrigeration Station": "Bloque",
        "Mamooooth Mountain": "Mamooth",
        "Rollin' Tundra": "Snowmen",
        "Signature Slopes": "Penguin",
        "Thermonuclear Climb": "Thermister",
        "Waterlogged Entrance": "Quenchie",
        "Cryo Catacombs": "Cryosnake",
        "Overpass of Sound": "Bop Box",
        "Crystal Basecamp": "Neyeptune",
        "Wam Wonderland": "Dedotated Ram",
        "Hell Hath Frozen Over": "Bloodbone",
        "Equinox Valley": "Special- AFK only Dedotated Ram",

        # W4 Maps
        "Spaceway Raceway": "Purp Mushroom",
        "TV Outpost": "TV",
        "Donut Drive-In": "Donut",
        "Outskirts of Fallstar Isle": "Demon Genie",
        "Mountainous Deugh": "Soda Can",
        "Wurm Highway": "Flying Worm",
        "Jelly Cube Bridge": "Gelatinous Cuboid",
        "Cocoa Tunnel": "Choccie",
        "Standstill Plains": "Biggole Wurm",
        "Shelled Shores": "Clammie",
        "The Untraveled Octopath": "Octodar",
        "Flamboyant Bayou": "Flombeige",
        "Enclave of Eyes": "Stilted Seeker",
        "The Rift": "Rift Monsters",

        # W5 Maps
        "Naut Sake Perimeter": "Suggma",
        "Niagrilled Falls": "Maccie",
        "The Killer Roundabout": "Mister Brightside",
        "Cracker Jack Lake": "Cheese Nub",
        "The Great Molehill": "Stiltmole",
        "Erruption River": "Molti",
        "Mount Doomish": "Purgatory Stalker",
        "OJ Bay": "Citringe",
        "Lampar Lake": "Lampar",
        "Spitfire River": "Fire Spirit",
        "Miner Mole Outskirts": "Biggole Mole",
        "Crawly Catacombs": "Crawler",
        "The Worm Nest": "Tremor Wurm",

        # W6 Maps
        "Gooble Goop Creek": "Sprout Spirit",
        "Picnic Bridgeways": "Ricecake",
        "Irrigation Station": "River Spirit",
        "Troll Playground": "Baby Troll",
        "Edge of the Valley": "Woodlin Spirit",
        "Bamboo Laboredge": "Bamboo Spirit",
        "Lightway Path": "Lantern Spirit",
        "Troll Broodnest": "Mama Troll",
        "Above the Clouds": "Leek Spirit",
        "Sleepy Skyline": "Ceramic Spirit",
        "Dozey Dogpark": "Skydoggie Spirit",
        "Yolkrock Basin": "Royal Egg",
        "Chieftain Stairway": "Minichief Spirit",
        "Emperor's Castle Doorstep": "Samurai Guardian",
    }
    try:
        return mapNametoEnemyNameDict.get(inputMap, f"UnknownMap:{inputMap}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"

def getapocCharactersIndexList() -> list:
    #get classes, find Barbarian and BB
    apocCharactersIndexList = [c.character_index for c in session_data.account.safe_characters if c.sub_class == "Barbarian"]
    return apocCharactersIndexList

def getChowMeowCharactersIndexList() -> list:
    # get classes, find BB ONLY for Chow and Meow
    bbCharactersIndexList = [c.character_index for c in session_data.account.safe_characters if c.elite_class == "Blood Berserker"]
    return bbCharactersIndexList

def getDeathNoteKills():
    apocAmountsList = [100000, 1000000, 100000000]
    apocNamesList = ["ZOW", "CHOW", "MEOW"]
    enemyMaps = buildMaps()
    apocCharactersIndexList = getapocCharactersIndexList()
    apocableMapIndexDict = {
        0: [30, 9, 38, 69, 120, 166],  #Barbarian only, not in regular DeathNote
        1: [1, 2, 14, 17, 16, 13, 18, 31, 19, 24, 26, 27, 28, 8, 15],
        2: [51, 52, 53, 57, 58, 59, 60, 62, 63, 64, 65],
        3: [101, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117],
        4: [151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163],
        5: [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213],
        6: [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264]
    }

    #total up all kills across characters
    for characterIndex in range(0, len(session_data.account.safe_characters)):
        try:
            characterKillsList = safe_loads(session_data.account.raw_data['KLA_' + str(characterIndex)])  #String pretending to be a list of lists yet again
        except Exception as reason:
            logger.warning(f"Unable to retrieve kill list for Character{characterIndex} because:{reason}")
            #print("ConsDeathNote.getDeathNoteKills~ EXCEPTION Unable to retrieve kill list for Character", characterIndex, "because:", reason)
            continue

        #If the character's subclass is Barbarian, add their special Apoc-Only kills to EnemyMap's zow_dict
        if characterIndex in apocCharactersIndexList:
            for worldIndex in range(0, len(apocableMapIndexDict)):
                for mapIndex in apocableMapIndexDict[worldIndex]:
                    if len(characterKillsList) > mapIndex:
                        enemyMaps[worldIndex][mapIndex].updateZOWDict(characterIndex, characterKillsList[mapIndex][0])
                    #else:
                        #print("ConsDeathNote.getDeathNoteKills~ INFO Barbarian with characterIndex", characterIndex, "kill list has no data for mapIndex", mapIndex, ", len(characterKillsList)=", len(characterKillsList))

        #Regardless of class, for each map within each world, add this player's kills to EnemyMap's kill_count
        for worldIndex in range(1, len(apocableMapIndexDict)):
            for mapIndex in apocableMapIndexDict[worldIndex]:
                if len(characterKillsList) > mapIndex:
                    if isinstance(characterKillsList[mapIndex], list):
                        try:
                            enemyMaps[worldIndex][mapIndex].addRawKLA(characterKillsList[mapIndex][0])
                        except:
                            enemyMaps[worldIndex][mapIndex].addRawKLA(0)
                            logger.exception(f"Kill list for characterIndex: {characterIndex}, worldIndex: {worldIndex}, mapIndex: {mapIndex} failed: Expecting a list, found {type(characterKillsList[mapIndex])}: {characterKillsList[mapIndex]}")
                    else:
                        try:
                            enemyMaps[worldIndex][mapIndex].addRawKLA(characterKillsList[mapIndex])
                        except:
                            enemyMaps[worldIndex][mapIndex].addRawKLA(0)
                            logger.exception(
                                f"Kill list for characterIndex: {characterIndex}, worldIndex: {worldIndex}, mapIndex: {mapIndex} failed: Knew it wasn't a list, could add {type(characterKillsList[mapIndex])}: {characterKillsList[mapIndex]}")

    deathnote_EnemyWorlds = {}

    #Have each EnemyMap calculate its Skull Value, Name, Count to Next, and Percent to Next now that all kills are totaled
    # Barbarian Only in worldIndex 0
    for worldIndex in range(1, len(enemyMaps)):
        for enemy_map in enemyMaps[worldIndex]:
            enemyMaps[worldIndex][enemy_map].generateDNSkull()
        #After each Map in that World has its Skull Info, create the corresponding EnemyWorld
        deathnote_EnemyWorlds[worldIndex] = EnemyWorld(worldIndex, enemyMaps[worldIndex])

    # Barbarian Only in 0
    for barbCharacterIndex in apocCharactersIndexList:
        for worldIndex in range(0, len(enemyMaps)):
            for enemy_map in enemyMaps[worldIndex]:
                if barbCharacterIndex in enemyMaps[worldIndex][enemy_map].zow_dict:
                    #print("DN~ INFO barbCharacterIndex", barbCharacterIndex, "found in worldIndex", worldIndex, "enemy_map", enemy_map)
                    kill_count = enemyMaps[worldIndex][enemy_map].zow_dict[barbCharacterIndex]
                    for apocIndex in range(0, len(apocAmountsList)):
                        if kill_count < apocAmountsList[apocIndex]:
                            #characterDict[barbCharacterIndex].apoc_dict[apocNamesList[apocIndex]][enemyMaps[worldIndex][enemy_map].zow_rating].append([
                            session_data.account.all_characters[barbCharacterIndex].addUnmetApoc(
                                apocNamesList[apocIndex], enemyMaps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                                [
                                    enemyMaps[worldIndex][enemy_map].map_name,  #map name
                                    apocAmountsList[apocIndex] - kill_count,  #kills short of zow/chow/meow
                                    floor((kill_count / apocAmountsList[apocIndex]) * 100),  #percent toward zow/chow/meow
                                    enemyMaps[worldIndex][enemy_map].monster_image  #monster image
                                ]
                            )
                        else:
                            session_data.account.all_characters[barbCharacterIndex].increaseApocTotal(apocNamesList[apocIndex])
                else:
                    #This condition can be hit when reviewing data from before a World release
                    #For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                    for apocIndex in range(0, len(apocAmountsList)):
                        session_data.account.all_characters[barbCharacterIndex].addUnmetApoc(
                            apocNamesList[apocIndex], enemyMaps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                            [
                                enemyMaps[worldIndex][enemy_map].map_name,  # map name
                                apocAmountsList[apocIndex],  # kills short of zow/chow/meow
                                0,  # percent toward zow/chow/meow
                                enemyMaps[worldIndex][enemy_map].monster_image  # monster image
                            ]
                        )
        #Sort them
        session_data.account.all_characters[barbCharacterIndex].sortApocByProgression()
    return deathnote_EnemyWorlds

def getMEOWBBIndex(apocCharactersIndexList):
    if len(apocCharactersIndexList) == 1:
        return apocCharactersIndexList[0]
    elif len(apocCharactersIndexList) >= 2:
        return apocCharactersIndexList[1]
    else:
        if len(apocCharactersIndexList) > 0:
            logger.warning(f"Could not retrieve which BB should complete MEOWs from this list: {apocCharactersIndexList}")
        return None

def setConsDeathNoteProgressionTier():
    deathnote_AdviceDict = {
        "W1": [],
        "W2": [],
        "W3": [],
        "W4": [],
        "W5": [],
        "W6": [],
        "ZOW": {},
        "CHOW": {},
        "MEOW": {}
    }
    zow_TotalAdvices = 0
    chow_TotalAdvices = 0
    meow_TotalAdvices = 0
    deathnote_AdviceGroupDict = {}
    deathnote_AdviceSection = AdviceSection(
        name="Death Note",
        tier="",
        header="Recommended Death Note actions",
        picture="Construction_Death_Note.png"
    )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return deathnote_AdviceSection
    elif session_data.account.construction_buildings['Death Note']['Level'] < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Death Note within the Construction skill in World 3!"
        return deathnote_AdviceSection

    currentMaxWorld = 6
    apocCharactersIndexList = getapocCharactersIndexList()
    bbCharactersIndexList = getChowMeowCharactersIndexList()
    meowBBIndex = getMEOWBBIndex(bbCharactersIndexList)
    session_data.account.meowBBIndex = meowBBIndex
    fullDeathNoteDict = getDeathNoteKills()

    max_tier = deathNote_progressionTiers[-2][0]
    overall_DeathNoteTier = 0
    worldIndexes = []
    tier_combo = {}
    for number in range(1, currentMaxWorld + 1):
        worldIndexes.append(number)
        tier_combo[number] = 0
    tier_combo['ZOW'] = 0
    tier_combo['CHOW'] = 0
    tier_combo['MEOW'] = 0
    apocToNextTier = {
        'ZOW': 0,
        'CHOW': 0,
        'MEOW': 0
    }
    zowsForNextTier = 0
    chowsForNextTier = 0
    meowsForNextTier = 0
    apocDifficultyNameList = ['Basic W1 Enemies', 'Basic W2 Enemies', 'Basic W3 Enemies', 'Basic W4 Enemies', 'Basic W5 Enemies', 'Basic W6 Enemies',
                              'Easy Extras', 'Medium Extras', 'Difficult Extras', 'Insane', 'Impossible']
    apocDifficultyCountDict = {
        'ZOW': {
            'Basic W1 Enemies': 15,
            'Basic W2 Enemies': 11,
            'Basic W3 Enemies': 14,
            'Basic W4 Enemies': 13,
            'Basic W5 Enemies': 13,
            'Basic W6 Enemies': 14,
            'Easy Extras': 4,
            'Medium Extras': 0,
            'Difficult Extras': 1,
            'Insane': 1,
            'Impossible': 0
        },
        'CHOW': {
            'Basic W1 Enemies': 15,
            'Basic W2 Enemies': 11,
            'Basic W3 Enemies': 14,
            'Basic W4 Enemies': 13,
            'Basic W5 Enemies': 13,
            'Basic W6 Enemies': 14,
            'Easy Extras': 2,
            'Medium Extras': 1,
            'Difficult Extras': 2,
            'Insane': 1,
            'Impossible': 0
        },
        'MEOW': {
            'Basic W1 Enemies': 15,
            'Basic W2 Enemies': 11,
            'Basic W3 Enemies': 14,
            'Basic W4 Enemies': 13,
            'Basic W5 Enemies': 13,
            'Basic W6 Enemies': 14,
            'Easy Extras': 1,
            'Medium Extras': 2,
            'Difficult Extras': 1,
            'Insane': 1,
            'Impossible': 1
        }
    }
    highestZOWCount = 0
    highestZOWCountIndex = None
    highestCHOWCount = 0
    highestCHOWCountIndex = None
    for barbIndex in apocCharactersIndexList:
        if highestZOWCountIndex is None:
            highestZOWCountIndex = barbIndex
        if highestCHOWCountIndex is None:
            highestCHOWCountIndex = barbIndex
        if session_data.account.all_characters[barbIndex].apoc_dict['ZOW']['Total'] > highestZOWCount:
            highestZOWCount = session_data.account.all_characters[barbIndex].apoc_dict['ZOW']['Total']
            highestZOWCountIndex = barbIndex
        if session_data.account.all_characters[barbIndex].apoc_dict['CHOW']['Total'] > highestCHOWCount:
            highestCHOWCount = session_data.account.all_characters[barbIndex].apoc_dict['CHOW']['Total']
            highestCHOWCountIndex = barbIndex

    #assess tiers
    for tier in deathNote_progressionTiers:
        #tier[0] = int tier
        #tier[1] = int w1LowestSkull
        #tier[2] = int w2LowestSkull
        #tier[3] = int w3LowestSkull
        #tier[4] = int w4LowestSkull
        #tier[5] = int w5LowestSkull
        #tier[6] = int w6LowestSkull
        #tier[7] = int w7LowestSkull
        #tier[8] = int w8LowestSkull
        #tier[9] = int zowCount
        #tier[10] = int chowCount
        #tier[11] = int meowCount
        #tier[12] = str Notes

        # Basic Worlds
        for worldIndex in worldIndexes:
            if tier_combo[worldIndex] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
                if fullDeathNoteDict[worldIndex].lowest_skull_value >= tier[worldIndex]:
                    tier_combo[worldIndex] = tier[0]
                else:
                    for enemy in fullDeathNoteDict[worldIndex].lowest_skulls_dict[fullDeathNoteDict[worldIndex].lowest_skull_value]:
                        deathnote_AdviceDict[f"W{worldIndex}"].append(
                            Advice(
                                label=enemy[0],
                                picture_class=enemy[3],
                                progression=f"{enemy[2]}%")
                        )

        # ZOW
        if tier_combo['ZOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestZOWCount >= tier[9]:
                tier_combo['ZOW'] = tier[0]
            else:
                zowsForNextTier = f"({highestZOWCount}/{tier[9]})"
                if highestZOWCountIndex is not None:
                    apocToNextTier['ZOW'] = tier[9] - highestZOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(session_data.account.all_characters[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['ZOW']:
                                deathnote_AdviceDict['ZOW'][difficultyName] = []
                            for enemy in session_data.account.all_characters[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]:
                                deathnote_AdviceDict["ZOW"][difficultyName].append(
                                    Advice(
                                        label=enemy[0],
                                        picture_class=enemy[3],
                                        progression=f"{enemy[2]}%"),
                                )
                else:
                    deathnote_AdviceDict["ZOW"] = [
                        Advice(
                            label="Create a Barbarian",
                            picture_class="barbarian-icon",
                            progression=0,
                            goal=1)
                    ]
        # CHOW
        if tier_combo['CHOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestCHOWCount >= tier[10]:
                tier_combo['CHOW'] = tier[0]
            else:
                chowsForNextTier = f"({highestCHOWCount}/{tier[10]})"
                if highestCHOWCountIndex is not None:
                    apocToNextTier['CHOW'] = tier[10] - highestCHOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(session_data.account.all_characters[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['CHOW']:
                                deathnote_AdviceDict['CHOW'][difficultyName] = []
                            for enemy in session_data.account.all_characters[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]:
                                deathnote_AdviceDict["CHOW"][difficultyName].append(
                                    Advice(
                                        label=enemy[0],
                                        picture_class=enemy[3],
                                        progression=f"{enemy[2]}%"),
                                    )
                else:
                    deathnote_AdviceDict["CHOW"] = [
                        Advice(
                            label="Create a Blood Berserker",
                            picture_class="blood-berserker-icon",
                            progression=0,
                            goal=1)
                    ]
        # MEOW
        if tier_combo['MEOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if tier[11] == 0:
                tier_combo['MEOW'] = tier[0]
            else:
                if meowBBIndex is not None:
                    if session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total'] >= tier[11]:
                        tier_combo['MEOW'] = tier[0]
                    else:
                        meowsForNextTier = f"({session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total']}/{tier[11]})"
                        apocToNextTier['MEOW'] = tier[11] - session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Total']
                        for difficultyName in apocDifficultyNameList:
                            if len(session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW'][difficultyName]) > 0:
                                if difficultyName not in deathnote_AdviceDict['MEOW']:
                                    deathnote_AdviceDict['MEOW'][difficultyName] = []
                                for enemy in session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW'][difficultyName]:
                                    deathnote_AdviceDict["MEOW"][difficultyName].append(
                                        Advice(
                                            label=enemy[0],
                                            picture_class=enemy[3],
                                            progression=f"{enemy[2]}%"),
                                        )
                else:
                    deathnote_AdviceDict["MEOW"] = [
                        Advice(
                            label="Create a Blood Berserker",
                            picture_class="blood-berserker-icon",
                            progression=0,
                            goal=1)
                    ]

        #Check for Rift Meow Specifically
        #TODO: Move to Account
        if meowBBIndex is not None:
            riftPresent = False
            for remainingMap in session_data.account.all_characters[meowBBIndex].apoc_dict['MEOW']['Medium Extras']:
                if remainingMap[0] == 'The Rift':
                    riftPresent = True
                    break
            if not riftPresent:
                session_data.account.rift_meowed = True

    #Generate Advice Groups
    #Basic Worlds
    for worldIndex in worldIndexes:
        deathnote_AdviceGroupDict[f"W{worldIndex}"] = AdviceGroup(
            tier=str(tier_combo[worldIndex]),
            pre_string=f"Kill more W{worldIndex} enemies to reach a minimum skull of {fullDeathNoteDict[worldIndex].next_lowest_skull_name}",
            advices=deathnote_AdviceDict[f"W{worldIndex}"],
            post_string=""
        )
        if fullDeathNoteDict[worldIndex].next_lowest_skull_name == "Eclipse Skull":
            deathnote_AdviceGroupDict[f"W{worldIndex}"].post_string = "Complete Super CHOWs with your Blood Berserker before finishing Eclipse Skulls"

    # ZOW
    if highestZOWCountIndex is not None:
        deathnote_AdviceGroupDict['ZOW'] = AdviceGroup(
            tier=str(tier_combo['ZOW'] if tier_combo['ZOW'] < 27 else ""),
            pre_string=f"{'Informational- ' if tier_combo['ZOW'] >= 27 else ''}Complete {apocToNextTier['ZOW']} more ZOW{pl(['dummy'] * apocToNextTier['ZOW'])} with {session_data.account.all_characters[highestZOWCountIndex].character_name} {zowsForNextTier}",
            advices=deathnote_AdviceDict['ZOW'],
            post_string="Aim for 12hrs or less (8k+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['ZOW'] = AdviceGroup(
            tier=str(tier_combo['ZOW'] if tier_combo['ZOW'] < 27 else ""),
            pre_string=f"ZOW Progress unavailable until a Barbarian is found in your account",
            advices=deathnote_AdviceDict['ZOW'],
        )

    # CHOW
    if highestCHOWCountIndex is not None:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW'] if tier_combo['CHOW'] < 27 else ""),
            pre_string=f"{'Informational- ' if tier_combo['CHOW'] >= 27 else ''}Complete {apocToNextTier['CHOW']} more CHOW{pl(['dummy'] * apocToNextTier['CHOW'])} with {session_data.account.all_characters[highestCHOWCountIndex].character_name} {chowsForNextTier}",
            advices=deathnote_AdviceDict['CHOW'],
            post_string="Aim for 12hrs or less (83k+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW'] if tier_combo['CHOW'] < 27 else ""),
            pre_string=f"CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['CHOW'],
        )

    # MEOW
    if meowBBIndex is not None:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < 27 else ""),
            pre_string=f"{'Informational- ' if tier_combo['MEOW'] >= 27 else ''}Complete {apocToNextTier['MEOW']} more Super CHOW{pl(['dummy']*apocToNextTier['MEOW'])} with {session_data.account.all_characters[meowBBIndex].character_name} {meowsForNextTier}",
            advices=deathnote_AdviceDict['MEOW'],
            post_string="Aim for 24hrs or less (4m+ KPH) per enemy"
        )
    else:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW'] if tier_combo['MEOW'] < 27 else ""),
            pre_string=f"Super CHOW Progress unavailable until a Blood Berserker is found in your account",
            advices=deathnote_AdviceDict['MEOW'],
        )

    #Generate Advice Section
    overall_DeathNoteTier = min(max_tier+1, tier_combo[1], tier_combo[2], tier_combo[3],
                                tier_combo[4], tier_combo[5], tier_combo[6],
                                tier_combo['ZOW'], tier_combo['CHOW'], tier_combo['MEOW'])  #tier_zows, tier_chows, tier_meows

    tier_section = f"{overall_DeathNoteTier}/{max_tier}"
    deathnote_AdviceSection.tier = tier_section
    deathnote_AdviceSection.pinchy_rating = overall_DeathNoteTier
    deathnote_AdviceSection.groups = deathnote_AdviceGroupDict.values()
    if overall_DeathNoteTier == max_tier:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}<br>You best ❤️"
    else:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}"

    return deathnote_AdviceSection
