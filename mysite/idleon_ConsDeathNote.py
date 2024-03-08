import json
from math import floor
from math import ceil
from idleon_SkillLevels import getSpecificSkillLevelsList
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger

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
    rawMaps = getJSONDataFromFile('static/enemy-maps.json')
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
    match mkValue:
        case 0:
            return "None"
        case 1:
            return "Normal Skull"
        case 2:
            return "Copper Skull"
        case 3:
            return "Iron Skull"
        case 4:
            return "Gold Skull"
        case 5:
            return "Platinum Skull"
        case 7:
            return "Dementia Skull"
        case 10:
            return "Lava Skull"
        case 20:
            return "Eclipse Skull"
        case _:
            return "Unknown"+str(mkValue)+" Skull"

def getNextSkullNames(mkValue: int) -> str:
    match mkValue:
        case 0:
            return "Normal Skull"
        case 1:
            return "Copper Skull"
        case 2:
            return "Iron Skull"
        case 3:
            return "Gold Skull"
        case 4:
            return "Platinum Skull"
        case 5:
            return "Dementia Skull"
        case 7:
            return "Lava Skull"
        case 10:
            return "Eclipse Skull"
        case 20:
            return "Finished!"
        case _:
            return "Unknown"+str(mkValue)+" Skull"

def getEnemyNameFromMap(inputMap: str) -> str:
    match inputMap:
        #W1 Maps
        case "Spore Meadows":
            return "Green Mushroom"
        case "Froggy Fields":
            return "Frog"
        case "Valley of the Beans":
            return "Bored Bean"
        case "Birch Enclave":
            return "Red Mushroom"
        case "Jungle Perimeter":
            return "Slime"
        case "The Base of the Bark":
            return "Stick"
        case "Hollowed Trunk":
            return "Nutto"
        case "Where the Branches End":
            return "Wood Mushroom"
        case "Winding Willows":
            return "Baby Boa"
        case "Vegetable Patch":
            return "Carrotman"
        case "Forest Outskirts":
            return "Glublin"
        case "Encroaching Forest Villa":
            return "Wode Board"
        case "Tucked Away":
            return "Gigafrog"
        case "Poopy Sewers":
            return "Poop"
        case "Rats Nest":
            return "Rat"
        case "The Roots":
            return "Special- Single Nutto at WorshipTD map"
        case "The Office":
            return "Special- Poops surrounding Dr. Def"
        case "Meel's Crypt":
            return "Special- Boop"
        #W2 Maps
        case "Jar Bridge":
            return "Sandy Pot"
        case "The Mimic Hole":
            return "Mimic"
        case "Dessert Dunes":
            return "Crabcake"
        case "The Grandioso Canyon":
            return "Mafioso"
        case "Shifty Sandbox":
            return "Sand Castle"
        case "Pincer Plateau":
            return "Pincermin"
        case "Slamabam Straightaway":
            return "Mashed Potato"
        case "The Ring":
            return "Tyson"
        case "Up Up Down Down":
            return "Moonmoon"
        case "Sands of Time":
            return "Sand Giant"
        case "Djonnuttown":
            return "Snelbie"
        case "Mummy Memorial":
            return "Special- Invisible Green Mushroom inside King Doot's map"
        #W3 Maps
        case "Steep Sheep Ledge":
            return "Sheepie"
        case "Snowfield Outskirts":
            return "Frost Flake"
        case "The Stache Split":
            return "Sir Stache"
        case "Refrigeration Station":
            return "Bloque"
        case "Mamooooth Mountain":
            return "Mamooth"
        case "Rollin' Tundra":
            return "Snowmen"
        case "Signature Slopes":
            return "Penguin"
        case "Thermonuclear Climb":
            return "Thermister"
        case "Waterlogged Entrance":
            return "Quenchie"
        case "Cryo Catacombs":
            return "Cryosnake"
        case "Overpass of Sound":
            return "Bop Box"
        case "Crystal Basecamp":
            return "Neyeptune"
        case "Wam Wonderland":
            return "Dedotated Ram"
        case "Hell Hath Frozen Over":
            return "Bloodbone"
        case "Equinox Valley":
            return "Special- AFK only Dedotated Ram"
        #W4 Maps
        case "Spaceway Raceway":
            return "Purp Mushroom"
        case "TV Outpost":
            return "TV"
        case "Donut Drive-In":
            return "Donut"
        case "Outskirts of Fallstar Isle":
            return "Demon Genie"
        case "Mountainous Deugh":
            return "Soda Can"
        case "Wurm Highway":
            return "Flying Worm"
        case "Jelly Cube Bridge":
            return "Gelatinous Cuboid"
        case "Cocoa Tunnel":
            return "Choccie"
        case "Standstill Plains":
            return "Biggole Wurm"
        case "Shelled Shores":
            return "Clammie"
        case "The Untraveled Octopath":
            return "Octodar"
        case "Flamboyant Bayou":
            return "Flombeige"
        case "Enclave of Eyes":
            return "Stilted Seeker"
        case "The Rift":
            return "Rift Monsters"
        #W5 Maps
        case "Naut Sake Perimeter":
            return "Suggma"
        case "Niagrilled Falls":
            return "Maccie"
        case "The Killer Roundabout":
            return "Mister Brightside"
        case "Cracker Jack Lake":
            return "Cheese Nub"
        case "The Great Molehill":
            return "Stiltmole"
        case "Erruption River":
            return "Molti"
        case "Mount Doomish":
            return "Purgatory Stalker"
        case "OJ Bay":
            return "Citringe"
        case "Lampar Lake":
            return "Lampar"
        case "Spitfire River":
            return "Fire Spirit"
        case "Miner Mole Outskirts":
            return "Biggole Mole"
        case "Crawly Catacombs":
            return "Crawler"
        case "The Worm Nest":
            return "Tremor Wurm"
        case "Gooble Goop Creek":
            return "Sprout Spirit"
        case "Picnic Bridgeways":
            return "Ricecake"
        case "Irrigation Station":
            return "River Spirit"
        case "Troll Playground":
            return "Baby Troll"
        case "Edge of the Valley":
            return "Woodlin Spirit"
        case "Bamboo Laboredge":
            return "Bamboo Spirit"
        case "Lightway Path":
            return "Lantern Spirit"
        case "Troll Broodnest":
            return "Mama Troll"
        case "Above the Clouds":
            return "Leek Spirit"
        case "Sleepy Skyline":
            return "Ceramic Spirit"
        case "Dozey Dogpark":
            return "Skydoggie Spirit"
        case "Yolkrock Basin":
            return "Royal Egg"
        case "Chieftain Stairway":
            return "Minichief Spirit"
        case "Emperor's Castle Doorstep":
            return "Samurai Guardian"

        #Default
        case _:
            return "UnknownEnemy"+str(inputMap)

def getapocCharactersIndexList(characterDict: dict) -> list:
    #get classes, find Barbarian and BB
    apocCharactersIndexList = []
    for characterIndex in characterDict:
        if characterDict[characterIndex].sub_class == "Barbarian":
            apocCharactersIndexList.append(characterDict[characterIndex].character_index)
    return apocCharactersIndexList

def getChowMeowCharactersIndexList(characterDict: dict) -> list:
    # get classes, find BB ONLY for Chow and Meow
    bbCharactersIndexList = []
    for characterIndex in characterDict:
        if characterDict[characterIndex].elite_class == "Blood Berserker":
            bbCharactersIndexList.append(characterDict[characterIndex].character_index)
    return bbCharactersIndexList

def getDeathNoteKills(inputJSON, characterDict):
    apocAmountsList = [100000, 1000000, 100000000]
    apocNamesList = ["ZOW", "CHOW", "MEOW"]
    enemyMaps = buildMaps()
    apocCharactersIndexList = getapocCharactersIndexList(characterDict)
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
    for characterIndex in range(0, len(characterDict)):
        try:
            characterKillsList = json.loads(inputJSON['KLA_'+str(characterIndex)])  #String pretending to be a list of lists yet again
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
                    enemyMaps[worldIndex][mapIndex].addRawKLA(characterKillsList[mapIndex][0])
                #else:
                    #print("ConsDeathNote.getDeathNoteKills~ INFO characterIndex", characterIndex, "kill list has no data for mapIndex", mapIndex, ", len(characterKillsList)=", len(characterKillsList))

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
                            characterDict[barbCharacterIndex].addUnmetApoc(
                                apocNamesList[apocIndex], enemyMaps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                                [
                                    enemyMaps[worldIndex][enemy_map].map_name,  #map name
                                    apocAmountsList[apocIndex] - kill_count,  #kills short of zow/chow/meow
                                    floor((kill_count / apocAmountsList[apocIndex]) * 100),  #percent toward zow/chow/meow
                                    enemyMaps[worldIndex][enemy_map].monster_image  #monster image
                                ]
                            )
                        else:
                            characterDict[barbCharacterIndex].increaseApocTotal(apocNamesList[apocIndex])
                else:
                    #This condition can be hit when reviewing data from before a World release
                    #For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                    for apocIndex in range(0, len(apocAmountsList)):
                        characterDict[barbCharacterIndex].addUnmetApoc(
                            apocNamesList[apocIndex], enemyMaps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                            [
                                enemyMaps[worldIndex][enemy_map].map_name,  # map name
                                apocAmountsList[apocIndex],  # kills short of zow/chow/meow
                                0,  # percent toward zow/chow/meow
                                enemyMaps[worldIndex][enemy_map].monster_image  # monster image
                            ]
                        )
        #Sort them
        characterDict[barbCharacterIndex].sortApocByProgression()
                #else:
                    #print("DN~ INFO barbCharacterIndex", barbCharacterIndex, "NOT found in worldIndex", worldIndex, "enemy_map", enemy_map)

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

def setConsDeathNoteProgressionTier(inputJSON, progressionTiers, characterDict):
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
    constructionLevelsList = getSpecificSkillLevelsList(inputJSON, len(characterDict), "Construction")
    if max(constructionLevelsList) < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return deathnote_AdviceSection
    elif json.loads(inputJSON["Tower"])[3] < 1:
        deathnote_AdviceSection.header = "Come back after unlocking the Salt Lick within the Construction skill in World 3!"
        return deathnote_AdviceSection

    currentMaxWorld = 6
    maxEnemiesPerGroup = 10
    apocCharactersIndexList = getapocCharactersIndexList(characterDict)
    bbCharactersIndexList = getChowMeowCharactersIndexList(characterDict)
    meowBBIndex = getMEOWBBIndex(bbCharactersIndexList)
    fullDeathNoteDict = getDeathNoteKills(inputJSON, characterDict)

    max_tier = progressionTiers[-1][0]
    overall_DeathNoteTier = 0
    worldIndexes = []
    maxedGroupsList = []
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
    apocDifficultyNameList = ['Basic W1 Enemies', 'Basic W2 Enemies', 'Basic W3 Enemies', 'Basic W4 Enemies', 'Basic W5 Enemies', 'Basic W6 Enemies',
                              'Easy Extras', 'Medium Extras', 'Difficult Extras', 'Impossible']
    apocDifficultyCountDict = {
        'ZOW': {
            'Basic W1 Enemies': 15,
            'Basic W2 Enemies': 11,
            'Basic W3 Enemies': 14,
            'Basic W4 Enemies': 13,
            'Basic W5 Enemies': 13,
            'Basic W6 Enemies': 14,
            'Easy Extras': 4,
            'Medium Extras': 1,
            'Difficult Extras': 1,
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
            'Medium Extras': 2,
            'Difficult Extras': 2,
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
            'Difficult Extras': 2,
            'Impossible': 1
        }
    }
    highestZOWCount = 0
    highestZOWCountIndex = None
    highestCHOWCount = 0
    highestCHOWCountIndex = None
    for barbIndex in apocCharactersIndexList:
        if characterDict[barbIndex].apoc_dict['ZOW']['Total'] > highestZOWCount:
            highestZOWCount = characterDict[barbIndex].apoc_dict['ZOW']['Total']
            highestZOWCountIndex = barbIndex
        if characterDict[barbIndex].apoc_dict['CHOW']['Total'] > highestCHOWCount:
            highestCHOWCount = characterDict[barbIndex].apoc_dict['CHOW']['Total']
            highestCHOWCountIndex = barbIndex

    #assess tiers
    for tier in progressionTiers:
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
                        if len(deathnote_AdviceDict[f"W{worldIndex}"]) < maxEnemiesPerGroup:
                            deathnote_AdviceDict[f"W{worldIndex}"].append(Advice(label=enemy[0], picture_class=enemy[3], progression=f"{enemy[2]}%")
                                                                          )
                        else:
                            if worldIndex not in maxedGroupsList:
                                maxedGroupsList.append(worldIndex)

        # ZOW
        if tier_combo['ZOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestZOWCount >= tier[9]:
                tier_combo['ZOW'] = tier[0]
            else:
                if highestZOWCountIndex is not None:
                    apocToNextTier['ZOW'] = tier[9] - highestZOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(characterDict[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]) > 0:
                            if zow_TotalAdvices < maxEnemiesPerGroup - 1:
                                if difficultyName not in deathnote_AdviceDict['ZOW']:
                                    deathnote_AdviceDict['ZOW'][difficultyName] = []
                                for enemy in characterDict[highestZOWCountIndex].apoc_dict['ZOW'][difficultyName]:
                                    if zow_TotalAdvices < maxEnemiesPerGroup:
                                        deathnote_AdviceDict["ZOW"][difficultyName].append(
                                            Advice(label=enemy[0], picture_class=enemy[3], progression=f"{enemy[2]}%"),
                                            )
                                        zow_TotalAdvices += 1
                                    else:
                                        if 'ZOW' not in maxedGroupsList:
                                            maxedGroupsList.append('ZOW')
                            else:
                                if 'ZOW' not in maxedGroupsList:
                                    maxedGroupsList.append('ZOW')

        # CHOW
        if tier_combo['CHOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highestCHOWCount >= tier[10]:
                tier_combo['CHOW'] = tier[0]
            else:
                if highestCHOWCountIndex is not None:
                    apocToNextTier['CHOW'] = tier[10] - highestCHOWCount
                    for difficultyName in apocDifficultyNameList:
                        if len(characterDict[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]) > 0:
                            if chow_TotalAdvices < maxEnemiesPerGroup - 1:
                                if difficultyName not in deathnote_AdviceDict['CHOW']:
                                    deathnote_AdviceDict['CHOW'][difficultyName] = []
                                for enemy in characterDict[highestCHOWCountIndex].apoc_dict['CHOW'][difficultyName]:
                                    if chow_TotalAdvices < maxEnemiesPerGroup:
                                        deathnote_AdviceDict["CHOW"][difficultyName].append(
                                            Advice(label=enemy[0], picture_class=enemy[3], progression=f"{enemy[2]}%"),
                                            )
                                        chow_TotalAdvices += 1
                                    else:
                                        if 'CHOW' not in maxedGroupsList:
                                            maxedGroupsList.append('CHOW')
                            else:
                                if 'CHOW' not in maxedGroupsList:
                                    maxedGroupsList.append('CHOW')

        # MEOW
        if tier_combo['MEOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if meowBBIndex is not None:
                if characterDict[meowBBIndex].apoc_dict['MEOW']['Total'] >= tier[11]:
                    tier_combo['MEOW'] = tier[0]
                else:
                    apocToNextTier['MEOW'] = tier[11] - characterDict[meowBBIndex].apoc_dict['MEOW']['Total']
                    #for difficultyIndex in range(0, len(apocDifficultyNameList)):
                    for difficultyName in apocDifficultyNameList:
                        if len(characterDict[meowBBIndex].apoc_dict['MEOW'][difficultyName]) > 0:
                            if meow_TotalAdvices < maxEnemiesPerGroup - 1:
                                if difficultyName not in deathnote_AdviceDict['MEOW']:
                                    deathnote_AdviceDict['MEOW'][difficultyName] = []
                                for enemy in characterDict[meowBBIndex].apoc_dict['MEOW'][difficultyName]:
                                    if meow_TotalAdvices < maxEnemiesPerGroup:
                                        deathnote_AdviceDict["MEOW"][difficultyName].append(
                                            Advice(label=enemy[0], picture_class=enemy[3], progression=f"{enemy[2]}%"),
                                            )
                                        meow_TotalAdvices += 1
                                    else:
                                        if 'MEOW' not in maxedGroupsList:
                                            maxedGroupsList.append('MEOW')
                            else:
                                if 'MEOW' not in maxedGroupsList:
                                    maxedGroupsList.append('MEOW')

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
            deathnote_AdviceGroupDict[f"W{worldIndex}"].post_string = "Complete Super CHOWs on your Blood Berserker in this window"

    # ZOW
    if highestZOWCountIndex is not None:
        deathnote_AdviceGroupDict['ZOW'] = AdviceGroup(
            tier=str(tier_combo['ZOW']),
            pre_string=f"Complete {apocToNextTier['ZOW']} more ZOW{pl(['dummy'] * apocToNextTier['ZOW'])} with {characterDict[highestZOWCountIndex].character_name}",
            advices=deathnote_AdviceDict['ZOW'],
            post_string="Aim for 12hrs or less (8k+ KPH) per enemy"
        )

    # CHOW
    if highestCHOWCountIndex is not None:
        deathnote_AdviceGroupDict['CHOW'] = AdviceGroup(
            tier=str(tier_combo['CHOW']),
            pre_string=f"Complete {apocToNextTier['CHOW']} more CHOW{pl(['dummy'] * apocToNextTier['CHOW'])} with {characterDict[highestCHOWCountIndex].character_name}",
            advices=deathnote_AdviceDict['CHOW'],
            post_string="Aim for 12hrs or less (83k+ KPH) per enemy"
        )

    # MEOW
    if meowBBIndex is not None:
        deathnote_AdviceGroupDict['MEOW'] = AdviceGroup(
            tier=str(tier_combo['MEOW']),
            pre_string=f"Complete {apocToNextTier['MEOW']} more Super CHOW{pl(['dummy']*apocToNextTier['MEOW'])} with {characterDict[meowBBIndex].character_name}",
            advices=deathnote_AdviceDict['MEOW'],
            post_string="Aim for 24hrs or less (4m+ KPH) per enemy"
        )

    #Generate Advice Section
    overall_DeathNoteTier = min(max_tier, tier_combo[1], tier_combo[2], tier_combo[3],
                                tier_combo[4], tier_combo[5], tier_combo[6],
                                tier_combo['ZOW'], tier_combo['CHOW'], tier_combo['MEOW'])  #tier_zows, tier_chows, tier_meows

    tier_section = f"{overall_DeathNoteTier}/{max_tier}"
    deathnote_AdviceSection.tier = tier_section
    deathnote_AdviceSection.pinchy_rating = overall_DeathNoteTier
    if overall_DeathNoteTier == max_tier:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}. You best ❤️"
    else:
        deathnote_AdviceSection.header = f"Best Death Note tier met: {tier_section}. Recommended death note actions"
        deathnote_AdviceSection.groups = deathnote_AdviceGroupDict.values()
    return deathnote_AdviceSection
