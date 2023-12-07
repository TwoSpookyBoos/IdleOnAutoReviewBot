import json
from idleon_CombatLevels import getHumanReadableClasses
from math import floor
from math import ceil
import progressionResults

def getSkullNames(mkValue):
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
            return ("Unknown"+str(mkValue)+" Skull")

def getEnemyNameFromMap(inputMap):
    match inputMap:
        #W1 Maps
        case "Spore Meadows":
            return "Green Mushrooms"
        case "Froggy Fields":
            return "Frogs"
        case "Valley of the Beans":
            return "Bored Beans"
        case "Birch Enclave":
            return "Red Mushrooms"
        case "Jungle Perimeter":
            return "Slimes"
        case "The Base of the Bark":
            return "Sticks"
        case "Hollowed Trunk":
            return "Nuttos"
        case "Where the Branches End":
            return "Wood Mushrooms"
        case "Winding Willows":
            return "Baby Boas"
        case "Vegetable Patch":
            return "Carrotmen"
        case "Forest Outskirts":
            return "Glublins"
        case "Encroaching Forest Villa":
            return "Wode Boards"
        case "Tucked Away":
            return "Gigafrogs"
        case "Poopy Sewers":
            return "Poops"
        case "Rats Nest":
            return "Rats"
        case "The Roots":
            return "Special- Single Nutto at WorshipTD map"
        case "The Office":
            return "Special- Poops surrounding Dr. Def"
        case "Meel's Crypt":
            return "Special- Boops"
        #W2 Maps
        case "Jar Bridge":
            return "Sandy Pots"
        case "The Mimic Hole":
            return "Mimics"
        case "Dessert Dunes":
            return "Crabcakes"
        case "The Grandioso Canyon":
            return "Mafiosos"
        case "Shifty Sandbox":
            return "Sand Castles"
        case "Pincer Plateau":
            return "Pincermin"
        case "Slamabam Straightaway":
            return "Mashed Potato"
        case "The Ring":
            return "Tysons"
        case "Up Up Down Down":
            return "Moonmoons"
        case "Sands of Time":
            return "Sand Giants"
        case "Djonnuttown":
            return "Snelbies"
        case "Mummy Memorial":
            return "Special- Invisible Green Mushroom inside King Doot's map"
        #W3 Maps
        case "Steep Sheep Ledge":
            return "Sheepies"
        case "Snowfield Outskirts":
            return "Frost Flakes"
        case "The Stache Split":
            return "Sir Staches"
        case "Refrigeration Station":
            return "Bloques"
        case "Mamooooth Mountain":
            return "Mamooths"
        case "Rollin' Tundra":
            return "Snowmen"
        case "Signature Slopes":
            return "Penguins"
        case "Thermonuclear Climb":
            return "Thermisters"
        case "Waterlogged Entrance":
            return "Quenchies"
        case "Cryo Catacombs":
            return "Cryosnake"
        case "Overpass of Sound":
            return "Bop Boxes"
        case "Crystal Basecamp":
            return "Neyeptunes"
        case "Wam Wonderland":
            return "Dedotated Rams"
        case "Hell Hath Frozen Over":
            return "Bloodbones"
        case "Equinox Valley":
            return "Special- AFK only Dedotated Rams"
        #W4 Maps
        case "Spaceway Raceway":
            return "Purp Mushrooms"
        case "TV Outpost":
            return "TVs"
        case "Donut Drive-In":
            return "Donuts"
        case "Outskirts of Fallstar Isle":
            return "Demon Genies"
        case "Mountainous Deugh":
            return "Soda Cans"
        case "Wurm Highway":
            return "Flying Worms"
        case "Jelly Cube Bridge":
            return "Gelatinous Cuboids"
        case "Cocoa Tunnel":
            return "Choccies"
        case "Standstill Plains":
            return "Biggole Wurms"
        case "Shelled Shores":
            return "Clammies"
        case "The Untraveled Octopath":
            return "Octodars"
        case "Flamboyant Bayou":
            return "Flombs"
        case "Enclave of Eyes":
            return "Stilted Seekers"
        case "The Rift":
            return "Rift Monsters"
        #W5 Maps
        case "Naut Sake Perimeter":
            return "Suggmas"
        case "Niagrilled Falls":
            return "Maccies"
        case "The Killer Roundabout":
            return "Mister Brightsides"
        case "Cracker Jack Lake":
            return "Cheese Nubs"
        case "The Great Molehill":
            return "Stiltmoles"
        case "Erruption River":
            return "Moltis"
        case "Mount Doomish":
            return "Purgatory Stalkers"
        case "OJ Bay":
            return "Citringes"
        case "Lampar Lake":
            return "Lampars"
        case "Spitfire River":
            return "Fire Spirits"
        case "Miner Mole Outskirts":
            return "Biggole Moles"
        case "Crawly Catacombs":
            return "Crawlers"
        case "The Worm Nest":
            return "Tremor Wurms"
        #Default
        case _:
            return ("UnknownEnemy"+inputMap)

def getApocalypseCharactersDict(inputJSON, playerCount, playerNames, fromPublicIEBool):
    #get classes, find Barbarian and BB
    playerClassesList = ["placeholder"]
    apocCharactersDict = {}
    classCounter = 0
    if fromPublicIEBool:
        while classCounter < playerCount:
            characterClass = getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)])
            characterNameAndClass = playerNames[classCounter] + " the " + characterClass
            if characterClass == "Barbarian" or characterClass == "Blood Berserker":
                apocCharactersDict[classCounter] = [[characterNameAndClass,0,0,0],[]]
            playerClassesList.append(characterNameAndClass)
            classCounter += 1
    else:
        while classCounter < playerCount:
            characterClass = getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)])
            characterNameAndClass = "Character" + str(classCounter+1) + " the " + getHumanReadableClasses(inputJSON['CharacterClass_'+str(classCounter)])
            if characterClass == "Barbarian" or characterClass == "Blood Berserker":
                apocCharactersDict[classCounter] = [[characterNameAndClass,0,0,0],[]]
            playerClassesList.append(characterNameAndClass)
            classCounter += 1

    #print("ConsDeathNote~ playerClassesList: ",playerClassesList[1:])
    #print("ConsDeathNote~ apocCharactersDict: ",apocCharactersDict)
    return apocCharactersDict


def getDeathNoteKills(inputJSON, playerCount, playerNames, fromPublicIEBool):
    apocCharactersDict = getApocalypseCharactersDict(inputJSON, playerCount, playerNames, fromPublicIEBool)
    apocableMapIndexList = [1, 2, 14, 17, 16, 13, 18, 31, 19, 24, 26, 27, 28, 8, 15, 30, 9, 38, 51, 52, 53, 57, 58, 59, 60, 62, 63, 64, 65, 69, 101, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117, 120, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 166, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213]
    apocableMapPortalRequirementList = [11, 15, 40, 0, 60, 2500, 5000, 0, 125, 100, 150, 30, 0, 20000, 35000, 0, 0, 0, 250, 600, 1000, 1200, 1600, 2000, 2500, 3000, 4000, 5000, 1, 0, 1000, 2000, 3000, 4000, 6000, 8000, 11000, 15000, 18000, 22000, 35000, 120000, 250000, 0, 0, 5000, 12000, 18000, 25000, 40000, 60000, 90000, 120000, 150000, 190000, 250000, 300000, 350000, 100, 25000, 30000, 50000, 75000, 125000, 300000, 500000, 1000000, 2000000, 3000000, 6000000, 10000000, 60000]
    #set maps with portal requirements, 0 kills default
    #"MapName":[
    #[0] = int Portal Requirement
    #[1] = int Kills
    #[2] = str ZOW difficulty
    #[3] = str CHOW difficulty
    #[4] = str Meow difficulty
    #[5] = int Skull rating (mk value)
    #[6] = int Count to next skull
    #[7] = float Percent to next skull
    apocDeathNoteDict = {
        'The Roots':[0,0,'Easy cleanup', 'Easy Cleanup', 'Medium Cleanup',0,0,0.00],
        'The Office':[0,0,'Easy cleanup', 'Easy Cleanup', 'Easy Cleanup',0,0,0.00],
        "Meel's Crypt":[0,0,'Easy cleanup', 'Difficult Cleanup', 'Difficult Cleanup',0,0,0.00],
        'Mummy Memorial':[0,0,'Difficult Cleanup', 'Difficult Cleanup', 'Difficult Cleanup',0,0,0.00],
        'Equinox Valley':[0,0,'Easy cleanup', 'Medium Cleanup', 'Difficult Cleanup',0,0,0.00],
        'The Rift':[100,0,'Easy cleanup', 'Medium Cleanup', 'Medium Cleanup',0,0,0.00],
        }
    w1DeathNoteDict = {
        'Spore Meadows':[11,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Froggy Fields':[15,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Valley of the Beans':[40,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Birch Enclave':[0,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Jungle Perimeter':[60,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'The Base of the Bark':[2500,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Hollowed Trunk':[5000,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Where the Branches End':[0,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Winding Willows':[125,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Vegetable Patch':[100,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Forest Outskirts':[150,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Encroaching Forest Villa':[30,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Tucked Away':[0,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Poopy Sewers':[20000,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        'Rats Nest':[35000,0,'Basic W1 Enemies', 'Basic W1 Enemies', 'Basic W1 Enemies',0,0,0.00],
        }
    w2DeathNoteDict = {
        'Jar Bridge':[250,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'The Mimic Hole':[600,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Dessert Dunes':[1000,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'The Grandioso Canyon':[1200,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Shifty Sandbox':[1600,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Pincer Plateau':[2000,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Slamabam Straightaway':[2500,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'The Ring':[3000,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Up Up Down Down':[4000,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Sands of Time':[5000,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        'Djonnuttown':[1,0,'Basic W2 Enemies', 'Basic W2 Enemies', 'Basic W2 Enemies',0,0,0.00],
        }
    w3DeathNoteDict = {
        'Steep Sheep Ledge':[1000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Snowfield Outskirts':[2000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'The Stache Split':[3000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Refrigeration Station':[4000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Mamooooth Mountain':[6000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        "Rollin' Tundra":[8000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Signature Slopes':[11000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Thermonuclear Climb':[15000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Waterlogged Entrance':[18000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Cryo Catacombs':[22000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Overpass of Sound':[35000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Crystal Basecamp':[120000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Wam Wonderland':[250000,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        'Hell Hath Frozen Over':[0,0,'Basic W3 Enemies', 'Basic W3 Enemies', 'Basic W3 Enemies',0,0,0.00],
        }
    w4DeathNoteDict = {
        'Spaceway Raceway':[5000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'TV Outpost':[12000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Donut Drive-In':[18000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Outskirts of Fallstar Isle':[25000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Mountainous Deugh':[40000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Wurm Highway':[60000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Jelly Cube Bridge':[90000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Cocoa Tunnel':[120000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Standstill Plains':[150000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Shelled Shores':[190000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'The Untraveled Octopath':[250000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Flamboyant Bayou':[300000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        'Enclave of Eyes':[350000,0,'Basic W4 Enemies', 'Basic W4 Enemies', 'Basic W4 Enemies',0,0,0.00],
        }
    w5DeathNoteDict = {
        'Naut Sake Perimeter':[25000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Niagrilled Falls':[30000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'The Killer Roundabout':[50000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Cracker Jack Lake':[75000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'The Great Molehill':[125000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Erruption River':[300000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Mount Doomish':[500000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'OJ Bay':[1000000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Lampar Lake':[2000000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Spitfire River':[3000000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Miner Mole Outskirts':[6000000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'Crawly Catacombs':[10000000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        'The Worm Nest':[60000,0,'Basic W5 Enemies', 'Basic W5 Enemies', 'Basic W5 Enemies',0,0,0.00],
        }

    #total up all kills across characters
    playerCounter = 0
    while playerCounter < playerCount:
        playerKillsList = json.loads(inputJSON['KLA_'+str(playerCounter)]) #String pretending to be a list of lists yet again
        killCounter = 0
        #try to adjust when kill count is stored as a String in scientific notation
        while killCounter < len(playerKillsList):
            if isinstance(playerKillsList[killCounter][0], str):
                try:
                    #print("ConsDeathNote~ Trying to Convert string to Float: ", type(playerKillsList[killCounter][0]), playerKillsList[killCounter][0])
                    playerKillsList[killCounter][0] = float(playerKillsList[killCounter][0])
                    #print("ConsDeathNote~ HURRAY Converted string to Float: ", type(playerKillsList[killCounter][0]), playerKillsList[killCounter][0])
                except Exception as reason:
                    print("ConsDeathNote~ EXCEPTION Unable to convert String to Float",playerKillsList[killCounter][0], reason)
            killCounter += 1
        #just for the sake of minimizing DeathNote counts
        if True == True:
            #apoc only, not in the real deathnote
            #try:
                #apocDeathNoteDict['The Roots'][1] += abs(playerKillsList[30][0]-apocDeathNoteDict['The Roots'][0])
                #apocDeathNoteDict['The Office'][1] += abs(playerKillsList[9][0]-apocDeathNoteDict['The Office'][0])
                #apocDeathNoteDict["Meel's Crypt"][1] += abs(playerKillsList[38][0]-apocDeathNoteDict["Meel's Crypt"][0])
                #apocDeathNoteDict['Mummy Memorial'][1] += abs(playerKillsList[69][0]-apocDeathNoteDict['Mummy Memorial'][0])
                #apocDeathNoteDict['Equinox Valley'][1] += abs(playerKillsList[120][0]-apocDeathNoteDict['Equinox Valley'][0])
                #apocDeathNoteDict['The Rift'][1] += abs(playerKillsList[166][0]-apocDeathNoteDict['The Rift'][0])
            #except Exception as reason:
                #print("ConsDeathNote~ EXCEPTION Unable to increase kill count in apocDeathNoteDict",playerCounter, playerCount, reason)
            #w1 dn
            try:
                w1DeathNoteDict['Spore Meadows'][1] += abs(playerKillsList[1][0]-w1DeathNoteDict['Spore Meadows'][0])
                w1DeathNoteDict['Froggy Fields'][1] += abs(playerKillsList[2][0]-w1DeathNoteDict['Froggy Fields'][0])
                w1DeathNoteDict['Valley of the Beans'][1] += abs(playerKillsList[14][0]-w1DeathNoteDict['Valley of the Beans'][0])
                w1DeathNoteDict['Birch Enclave'][1] += abs(playerKillsList[17][0]-w1DeathNoteDict['Birch Enclave'][0])
                w1DeathNoteDict['Jungle Perimeter'][1] += abs(playerKillsList[16][0]-w1DeathNoteDict['Jungle Perimeter'][0])
                w1DeathNoteDict['The Base of the Bark'][1] += abs(playerKillsList[13][0]-w1DeathNoteDict['The Base of the Bark'][0])
                w1DeathNoteDict['Hollowed Trunk'][1] += abs(playerKillsList[18][0]-w1DeathNoteDict['Hollowed Trunk'][0])
                w1DeathNoteDict['Where the Branches End'][1] += abs(playerKillsList[31][0]-w1DeathNoteDict['Where the Branches End'][0])
                w1DeathNoteDict['Winding Willows'][1] += abs(playerKillsList[19][0]-w1DeathNoteDict['Winding Willows'][0])
                w1DeathNoteDict['Vegetable Patch'][1] += abs(playerKillsList[24][0]-w1DeathNoteDict['Vegetable Patch'][0])
                w1DeathNoteDict['Forest Outskirts'][1] += abs(playerKillsList[26][0]-w1DeathNoteDict['Forest Outskirts'][0])
                w1DeathNoteDict['Encroaching Forest Villa'][1] += abs(playerKillsList[27][0]-w1DeathNoteDict['Encroaching Forest Villa'][0])
                w1DeathNoteDict['Tucked Away'][1] += abs(playerKillsList[28][0]-w1DeathNoteDict['Tucked Away'][0])
                w1DeathNoteDict['Poopy Sewers'][1] += abs(playerKillsList[8][0]-w1DeathNoteDict['Poopy Sewers'][0])
                w1DeathNoteDict['Rats Nest'][1] += abs(playerKillsList[15][0]-w1DeathNoteDict['Rats Nest'][0])
            except Exception as reason:
                print("ConsDeathNote~ EXCEPTION Unable to increase kill count in w1DeathNoteDict",playerCounter, playerCount, reason)
            #w2 dn
            try:
                w2DeathNoteDict['Jar Bridge'][1] += abs(playerKillsList[51][0]-w2DeathNoteDict['Jar Bridge'][0])
                w2DeathNoteDict['The Mimic Hole'][1] += abs(playerKillsList[52][0]-w2DeathNoteDict['The Mimic Hole'][0])
                w2DeathNoteDict['Dessert Dunes'][1] += abs(playerKillsList[53][0]-w2DeathNoteDict['Dessert Dunes'][0])
                w2DeathNoteDict['The Grandioso Canyon'][1] += abs(playerKillsList[57][0]-w2DeathNoteDict['The Grandioso Canyon'][0])
                w2DeathNoteDict['Shifty Sandbox'][1] += abs(playerKillsList[58][0]-w2DeathNoteDict['Shifty Sandbox'][0])
                w2DeathNoteDict['Pincer Plateau'][1] += abs(playerKillsList[59][0]-w2DeathNoteDict['Pincer Plateau'][0])
                w2DeathNoteDict['Slamabam Straightaway'][1] += abs(playerKillsList[60][0]-w2DeathNoteDict['Slamabam Straightaway'][0])
                w2DeathNoteDict['The Ring'][1] += abs(playerKillsList[62][0]-w2DeathNoteDict['The Ring'][0])
                w2DeathNoteDict['Up Up Down Down'][1] += abs(playerKillsList[63][0]-w2DeathNoteDict['Up Up Down Down'][0])
                w2DeathNoteDict['Sands of Time'][1] += abs(playerKillsList[64][0]-w2DeathNoteDict['Sands of Time'][0])
                w2DeathNoteDict['Djonnuttown'][1] += abs(playerKillsList[65][0]-w2DeathNoteDict['Djonnuttown'][0])
            except Exception as reason:
                print("ConsDeathNote~ EXCEPTION Unable to increase kill count in w2DeathNoteDict",playerCounter, playerCount, reason)
            #w3 dn
            try:
                w3DeathNoteDict['Steep Sheep Ledge'][1] += abs(playerKillsList[101][0]-w3DeathNoteDict['Steep Sheep Ledge'][0])
                w3DeathNoteDict['Snowfield Outskirts'][1] += abs(playerKillsList[103][0]-w3DeathNoteDict['Snowfield Outskirts'][0])
                w3DeathNoteDict['The Stache Split'][1] += abs(playerKillsList[104][0]-w3DeathNoteDict['The Stache Split'][0])
                w3DeathNoteDict['Refrigeration Station'][1] += abs(playerKillsList[105][0]-w3DeathNoteDict['Refrigeration Station'][0])
                w3DeathNoteDict['Mamooooth Mountain'][1] += abs(playerKillsList[106][0]-w3DeathNoteDict['Mamooooth Mountain'][0])
                w3DeathNoteDict["Rollin' Tundra"][1] += abs(playerKillsList[107][0]-w3DeathNoteDict["Rollin' Tundra"][0])
                w3DeathNoteDict['Signature Slopes'][1] += abs(playerKillsList[108][0]-w3DeathNoteDict['Signature Slopes'][0])
                w3DeathNoteDict['Thermonuclear Climb'][1] += abs(playerKillsList[109][0]-w3DeathNoteDict['Thermonuclear Climb'][0])
                w3DeathNoteDict['Waterlogged Entrance'][1] += abs(playerKillsList[110][0]-w3DeathNoteDict['Waterlogged Entrance'][0])
                w3DeathNoteDict['Cryo Catacombs'][1] += abs(playerKillsList[111][0]-w3DeathNoteDict['Cryo Catacombs'][0])
                w3DeathNoteDict['Overpass of Sound'][1] += abs(playerKillsList[112][0]-w3DeathNoteDict['Overpass of Sound'][0])
                w3DeathNoteDict['Crystal Basecamp'][1] += abs(playerKillsList[113][0]-w3DeathNoteDict['Crystal Basecamp'][0])
                w3DeathNoteDict['Wam Wonderland'][1] += abs(playerKillsList[116][0]-w3DeathNoteDict['Wam Wonderland'][0])
                w3DeathNoteDict['Hell Hath Frozen Over'][1] += abs(playerKillsList[117][0]-w3DeathNoteDict['Hell Hath Frozen Over'][0])
            except Exception as reason:
                print("ConsDeathNote~ EXCEPTION Unable to increase kill count in w3DeathNoteDict",playerCounter, playerCount, reason)
            #w4 dn
            try:
                w4DeathNoteDict['Spaceway Raceway'][1] += abs(playerKillsList[151][0]-w4DeathNoteDict['Spaceway Raceway'][0])
                w4DeathNoteDict['TV Outpost'][1] += abs(playerKillsList[152][0]-w4DeathNoteDict['TV Outpost'][0])
                w4DeathNoteDict['Donut Drive-In'][1] += abs(playerKillsList[153][0]-w4DeathNoteDict['Donut Drive-In'][0])
                w4DeathNoteDict['Outskirts of Fallstar Isle'][1] += abs(playerKillsList[154][0]-w4DeathNoteDict['Outskirts of Fallstar Isle'][0])
                w4DeathNoteDict['Mountainous Deugh'][1] += abs(playerKillsList[155][0]-w4DeathNoteDict['Mountainous Deugh'][0])
                w4DeathNoteDict['Wurm Highway'][1] += abs(playerKillsList[156][0]-w4DeathNoteDict['Wurm Highway'][0])
                w4DeathNoteDict['Jelly Cube Bridge'][1] += abs(playerKillsList[157][0]-w4DeathNoteDict['Jelly Cube Bridge'][0])
                w4DeathNoteDict['Cocoa Tunnel'][1] += abs(playerKillsList[158][0]-w4DeathNoteDict['Cocoa Tunnel'][0])
                w4DeathNoteDict['Standstill Plains'][1] += abs(playerKillsList[159][0]-w4DeathNoteDict['Standstill Plains'][0])
                w4DeathNoteDict['Shelled Shores'][1] += abs(playerKillsList[160][0]-w4DeathNoteDict['Shelled Shores'][0])
                w4DeathNoteDict['The Untraveled Octopath'][1] += abs(playerKillsList[161][0]-w4DeathNoteDict['The Untraveled Octopath'][0])
                w4DeathNoteDict['Flamboyant Bayou'][1] += abs(playerKillsList[162][0]-w4DeathNoteDict['Flamboyant Bayou'][0])
                w4DeathNoteDict['Enclave of Eyes'][1] += abs(playerKillsList[163][0]-w4DeathNoteDict['Enclave of Eyes'][0])
            except Exception as reason:
                print("ConsDeathNote~ EXCEPTION Unable to increase kill count in w4DeathNoteDict",playerCounter, playerCount, reason)
            #w5 dn
            try:
                w5DeathNoteDict['Naut Sake Perimeter'][1] += abs(playerKillsList[201][0]-w5DeathNoteDict['Naut Sake Perimeter'][0])
                w5DeathNoteDict['Niagrilled Falls'][1] += abs(playerKillsList[202][0]-w5DeathNoteDict['Niagrilled Falls'][0])
                w5DeathNoteDict['The Killer Roundabout'][1] += abs(playerKillsList[203][0]-w5DeathNoteDict['The Killer Roundabout'][0])
                w5DeathNoteDict['Cracker Jack Lake'][1] += abs(playerKillsList[204][0]-w5DeathNoteDict['Cracker Jack Lake'][0])
                w5DeathNoteDict['The Great Molehill'][1] += abs(playerKillsList[205][0]-w5DeathNoteDict['The Great Molehill'][0])
                w5DeathNoteDict['Erruption River'][1] += abs(playerKillsList[206][0]-w5DeathNoteDict['Erruption River'][0])
                w5DeathNoteDict['Mount Doomish'][1] += abs(playerKillsList[207][0]-w5DeathNoteDict['Mount Doomish'][0])
                w5DeathNoteDict['OJ Bay'][1] += abs(playerKillsList[208][0]-w5DeathNoteDict['OJ Bay'][0])
                w5DeathNoteDict['Lampar Lake'][1] += abs(playerKillsList[209][0]-w5DeathNoteDict['Lampar Lake'][0])
                w5DeathNoteDict['Spitfire River'][1] += abs(playerKillsList[210][0]-w5DeathNoteDict['Spitfire River'][0])
                w5DeathNoteDict['Miner Mole Outskirts'][1] += abs(playerKillsList[211][0]-w5DeathNoteDict['Miner Mole Outskirts'][0])
                w5DeathNoteDict['Crawly Catacombs'][1] += abs(playerKillsList[212][0]-w5DeathNoteDict['Crawly Catacombs'][0])
                w5DeathNoteDict['The Worm Nest'][1] += abs(playerKillsList[213][0]-w5DeathNoteDict['The Worm Nest'][0])
            except Exception as reason:
                print("ConsDeathNote~ EXCEPTION Unable to increase kill count in w5DeathNoteDict",playerCounter, playerCount, reason)
        #apoc counts for Barbarians and Blood Berserkers only
        if playerCounter in apocCharactersDict.keys():
            mapIndexCounter = 0
            while mapIndexCounter < len(apocableMapIndexList):
                try:
                    apocCharactersDict[playerCounter][1].append(abs(playerKillsList[apocableMapIndexList[mapIndexCounter]][0]-apocableMapPortalRequirementList[mapIndexCounter]))
                except Exception as reason:
                    print("ConsDeathNote~ EXCEPTION Unable to append kill count to apocDeathNoteDict for Character",playerCounter, "and MapIndexCouter",mapIndexCounter, reason)
                mapIndexCounter += 1
            for killCount in apocCharactersDict[playerCounter][1]:
                if killCount >= 100000000:
                    apocCharactersDict[playerCounter][0][1] += 1
                    apocCharactersDict[playerCounter][0][2] += 1
                    apocCharactersDict[playerCounter][0][3] += 1
                elif killCount >= 1000000:
                    apocCharactersDict[playerCounter][0][1] += 1
                    apocCharactersDict[playerCounter][0][2] += 1
                elif killCount >= 100000:
                    apocCharactersDict[playerCounter][0][1] += 1

        #all enemies finished, increase counter to access next character's kills
        playerCounter += 1

    #calculate skull type per enemy and count toward next
    dnSkullRequirementList = [0,25000,100000,250000,500000,1000000,5000000,100000000,1000000000]
    dnSkullValueList = [0,1,2,3,4,5,7,10,20]
    #"MapName":[
    #[0] = int Portal Requirement
    #[1] = int Kills
    #[2] = str ZOW difficulty
    #[3] = str CHOW difficulty
    #[4] = str Meow difficulty
    #[5] = int Skull rating (mk value)
    #[6] = int Count to next skull
    #[7] = float Percent to next skull
    for key in w1DeathNoteDict:
        if (w1DeathNoteDict[key][1] >= dnSkullRequirementList[8]) and (w1DeathNoteDict[key][5] < dnSkullValueList[8]):
            w1DeathNoteDict[key][5] = dnSkullValueList[8]
            w1DeathNoteDict[key][6] = 0
            w1DeathNoteDict[key][7] = 100
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[7]) and (w1DeathNoteDict[key][5] < dnSkullValueList[7]):
            w1DeathNoteDict[key][5] = dnSkullValueList[7]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[8]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[8])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[6]) and (w1DeathNoteDict[key][5] < dnSkullValueList[6]):
            w1DeathNoteDict[key][5] = dnSkullValueList[6]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[7]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[7])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[5]) and (w1DeathNoteDict[key][5] < dnSkullValueList[5]):
            w1DeathNoteDict[key][5] = dnSkullValueList[5]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[6]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[6])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[4]) and (w1DeathNoteDict[key][5] < dnSkullValueList[4]):
            w1DeathNoteDict[key][5] = dnSkullValueList[4]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[5]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[5])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[3]) and (w1DeathNoteDict[key][5] < dnSkullValueList[3]):
            w1DeathNoteDict[key][5] = dnSkullValueList[3]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[4]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[4])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[2]) and (w1DeathNoteDict[key][5] < dnSkullValueList[2]):
            w1DeathNoteDict[key][5] = dnSkullValueList[2]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[3]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[3])*100)
        elif (w1DeathNoteDict[key][1] >= dnSkullRequirementList[1]) and (w1DeathNoteDict[key][5] < dnSkullValueList[1]):
            w1DeathNoteDict[key][5] = dnSkullValueList[1]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[2]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[2])*100)
        else:
            w1DeathNoteDict[key][5] = dnSkullRequirementList[0]
            w1DeathNoteDict[key][6] = ceil(dnSkullRequirementList[1]-w1DeathNoteDict[key][1])
            w1DeathNoteDict[key][7] = floor((w1DeathNoteDict[key][1]/dnSkullRequirementList[1])*100)
    for key in w2DeathNoteDict:
        if (w2DeathNoteDict[key][1] >= dnSkullRequirementList[8]) and (w2DeathNoteDict[key][5] < dnSkullValueList[8]):
            w2DeathNoteDict[key][5] = dnSkullValueList[8]
            w2DeathNoteDict[key][6] = 0
            w2DeathNoteDict[key][7] = 100
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[7]) and (w2DeathNoteDict[key][5] < dnSkullValueList[7]):
            w2DeathNoteDict[key][5] = dnSkullValueList[7]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[8]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[8])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[6]) and (w2DeathNoteDict[key][5] < dnSkullValueList[6]):
            w2DeathNoteDict[key][5] = dnSkullValueList[6]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[7]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[7])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[5]) and (w2DeathNoteDict[key][5] < dnSkullValueList[5]):
            w2DeathNoteDict[key][5] = dnSkullValueList[5]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[6]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[6])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[4]) and (w2DeathNoteDict[key][5] < dnSkullValueList[4]):
            w2DeathNoteDict[key][5] = dnSkullValueList[4]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[5]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[5])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[3]) and (w2DeathNoteDict[key][5] < dnSkullValueList[3]):
            w2DeathNoteDict[key][5] = dnSkullValueList[3]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[4]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[4])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[2]) and (w2DeathNoteDict[key][5] < dnSkullValueList[2]):
            w2DeathNoteDict[key][5] = dnSkullValueList[2]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[3]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[3])*100)
        elif (w2DeathNoteDict[key][1] >= dnSkullRequirementList[1]) and (w2DeathNoteDict[key][5] < dnSkullValueList[1]):
            w2DeathNoteDict[key][5] = dnSkullValueList[1]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[2]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[2])*100)
        else:
            w2DeathNoteDict[key][5] = dnSkullRequirementList[0]
            w2DeathNoteDict[key][6] = ceil(dnSkullRequirementList[1]-w2DeathNoteDict[key][1])
            w2DeathNoteDict[key][7] = floor((w2DeathNoteDict[key][1]/dnSkullRequirementList[1])*100)
    for key in w3DeathNoteDict:
        if (w3DeathNoteDict[key][1] >= dnSkullRequirementList[8]) and (w3DeathNoteDict[key][5] < dnSkullValueList[8]):
            w3DeathNoteDict[key][5] = dnSkullValueList[8]
            w3DeathNoteDict[key][6] = 0
            w3DeathNoteDict[key][7] = 100
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[7]) and (w3DeathNoteDict[key][5] < dnSkullValueList[7]):
            w3DeathNoteDict[key][5] = dnSkullValueList[7]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[8]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[8])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[6]) and (w3DeathNoteDict[key][5] < dnSkullValueList[6]):
            w3DeathNoteDict[key][5] = dnSkullValueList[6]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[7]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[7])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[5]) and (w3DeathNoteDict[key][5] < dnSkullValueList[5]):
            w3DeathNoteDict[key][5] = dnSkullValueList[5]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[6]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[6])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[4]) and (w3DeathNoteDict[key][5] < dnSkullValueList[4]):
            w3DeathNoteDict[key][5] = dnSkullValueList[4]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[5]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[5])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[3]) and (w3DeathNoteDict[key][5] < dnSkullValueList[3]):
            w3DeathNoteDict[key][5] = dnSkullValueList[3]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[4]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[4])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[2]) and (w3DeathNoteDict[key][5] < dnSkullValueList[2]):
            w3DeathNoteDict[key][5] = dnSkullValueList[2]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[3]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[3])*100)
        elif (w3DeathNoteDict[key][1] >= dnSkullRequirementList[1]) and (w3DeathNoteDict[key][5] < dnSkullValueList[1]):
            w3DeathNoteDict[key][5] = dnSkullValueList[1]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[2]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[2])*100)
        else:
            w3DeathNoteDict[key][5] = dnSkullRequirementList[0]
            w3DeathNoteDict[key][6] = ceil(dnSkullRequirementList[1]-w3DeathNoteDict[key][1])
            w3DeathNoteDict[key][7] = floor((w3DeathNoteDict[key][1]/dnSkullRequirementList[1])*100)
    for key in w4DeathNoteDict:
        if (w4DeathNoteDict[key][1] >= dnSkullRequirementList[8]) and (w4DeathNoteDict[key][5] < dnSkullValueList[8]):
            w4DeathNoteDict[key][5] = dnSkullValueList[8]
            w4DeathNoteDict[key][6] = 0
            w4DeathNoteDict[key][7] = 100
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[7]) and (w4DeathNoteDict[key][5] < dnSkullValueList[7]):
            w4DeathNoteDict[key][5] = dnSkullValueList[7]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[8]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[8])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[6]) and (w4DeathNoteDict[key][5] < dnSkullValueList[6]):
            w4DeathNoteDict[key][5] = dnSkullValueList[6]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[7]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[7])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[5]) and (w4DeathNoteDict[key][5] < dnSkullValueList[5]):
            w4DeathNoteDict[key][5] = dnSkullValueList[5]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[6]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[6])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[4]) and (w4DeathNoteDict[key][5] < dnSkullValueList[4]):
            w4DeathNoteDict[key][5] = dnSkullValueList[4]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[5]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[5])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[3]) and (w4DeathNoteDict[key][5] < dnSkullValueList[3]):
            w4DeathNoteDict[key][5] = dnSkullValueList[3]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[4]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[4])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[2]) and (w4DeathNoteDict[key][5] < dnSkullValueList[2]):
            w4DeathNoteDict[key][5] = dnSkullValueList[2]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[3]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[3])*100)
        elif (w4DeathNoteDict[key][1] >= dnSkullRequirementList[1]) and (w4DeathNoteDict[key][5] < dnSkullValueList[1]):
            w4DeathNoteDict[key][5] = dnSkullValueList[1]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[2]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[2])*100)
        else:
            w4DeathNoteDict[key][5] = dnSkullRequirementList[0]
            w4DeathNoteDict[key][6] = ceil(dnSkullRequirementList[1]-w4DeathNoteDict[key][1])
            w4DeathNoteDict[key][7] = floor((w4DeathNoteDict[key][1]/dnSkullRequirementList[1])*100)
    for key in w5DeathNoteDict:
        if (w5DeathNoteDict[key][1] >= dnSkullRequirementList[8]) and (w5DeathNoteDict[key][5] < dnSkullValueList[8]):
            w5DeathNoteDict[key][5] = dnSkullValueList[8]
            w5DeathNoteDict[key][6] = 0
            w5DeathNoteDict[key][7] = 100
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[7]) and (w5DeathNoteDict[key][5] < dnSkullValueList[7]):
            w5DeathNoteDict[key][5] = dnSkullValueList[7]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[8]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[8])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[6]) and (w5DeathNoteDict[key][5] < dnSkullValueList[6]):
            w5DeathNoteDict[key][5] = dnSkullValueList[6]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[7]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[7])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[5]) and (w5DeathNoteDict[key][5] < dnSkullValueList[5]):
            w5DeathNoteDict[key][5] = dnSkullValueList[5]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[6]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[6])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[4]) and (w5DeathNoteDict[key][5] < dnSkullValueList[4]):
            w5DeathNoteDict[key][5] = dnSkullValueList[4]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[5]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[5])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[3]) and (w5DeathNoteDict[key][5] < dnSkullValueList[3]):
            w5DeathNoteDict[key][5] = dnSkullValueList[3]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[4]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[4])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[2]) and (w5DeathNoteDict[key][5] < dnSkullValueList[2]):
            w5DeathNoteDict[key][5] = dnSkullValueList[2]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[3]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[3])*100)
        elif (w5DeathNoteDict[key][1] >= dnSkullRequirementList[1]) and (w5DeathNoteDict[key][5] < dnSkullValueList[1]):
            w5DeathNoteDict[key][5] = dnSkullValueList[1]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[2]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[2])*100)
        else:
            w5DeathNoteDict[key][5] = dnSkullRequirementList[0]
            w5DeathNoteDict[key][6] = ceil(dnSkullRequirementList[1]-w5DeathNoteDict[key][1])
            w5DeathNoteDict[key][7] = floor((w5DeathNoteDict[key][1]/dnSkullRequirementList[1])*100)
    #print("ConsDeathNote~ w1DeathNoteDict:",w1DeathNoteDict)
    #print("ConsDeathNote~ w2DeathNoteDict:",w2DeathNoteDict)
    #print("ConsDeathNote~ w3DeathNoteDict:",w3DeathNoteDict)
    #print("ConsDeathNote~ w4DeathNoteDict:",w4DeathNoteDict)
    #print("ConsDeathNote~ w5DeathNoteDict:",w5DeathNoteDict)

    #calculate lowest skull per world
    w1LowestSkull = dnSkullValueList[-1]
    w2LowestSkull = dnSkullValueList[-1]
    w3LowestSkull = dnSkullValueList[-1]
    w4LowestSkull = dnSkullValueList[-1]
    w5LowestSkull = dnSkullValueList[-1]
    #w6LowestSkull = dnSkullValueList[-1]
    #w7LowestSkull = dnSkullValueList[-1]
    #w8LowestSkull = dnSkullValueList[-1]
    for key in w1DeathNoteDict:
        if (w1DeathNoteDict[key][5] < w1LowestSkull):
            #print("ConsDeathNote~ Updating W1 Lowest Skull from " + str(w1LowestSkull) + " to " + str(w1DeathNoteDict[key][5]),key)
            w1LowestSkull = w1DeathNoteDict[key][5]
    for key in w2DeathNoteDict:
        if (w2DeathNoteDict[key][5] < w2LowestSkull):
            #print("ConsDeathNote~ Updating W2 Lowest Skull from " + str(w2LowestSkull) + " to " + str(w2DeathNoteDict[key][5]),key)
            w2LowestSkull = w2DeathNoteDict[key][5]
    for key in w3DeathNoteDict:
        if (w3DeathNoteDict[key][5] < w3LowestSkull):
            #print("ConsDeathNote~ Updating W3 Lowest Skull from " + str(w3LowestSkull) + " to " + str(w3DeathNoteDict[key][5]),key)
            w3LowestSkull = w3DeathNoteDict[key][5]
    for key in w4DeathNoteDict:
        if (w4DeathNoteDict[key][5] < w4LowestSkull):
            #print("ConsDeathNote~ Updating W4 Lowest Skull from " + str(w4LowestSkull) + " to " + str(w4DeathNoteDict[key][5]),key)
            w4LowestSkull = w4DeathNoteDict[key][5]
    for key in w5DeathNoteDict:
        if (w5DeathNoteDict[key][5] < w5LowestSkull):
            #print("ConsDeathNote~ Updating W5 Lowest Skull from " + str(w5LowestSkull) + " to " + str(w5DeathNoteDict[key][5]),key)
            w5LowestSkull = w5DeathNoteDict[key][5]

    #Calculate closest enemy to next skull
    w1ClosestSkull = ["",dnSkullRequirementList[-1],0]
    w2ClosestSkull = ["",dnSkullRequirementList[-1],0]
    w3ClosestSkull = ["",dnSkullRequirementList[-1],0]
    w4ClosestSkull = ["",dnSkullRequirementList[-1],0]
    w5ClosestSkull = ["",dnSkullRequirementList[-1],0]
    #w6ClosestSkull = ["",0,0]

    if w1LowestSkull < 20:
        for key in w1DeathNoteDict:
            if w1DeathNoteDict[key][6] < w1ClosestSkull[1] and w1DeathNoteDict[key][6] != 0:
                w1ClosestSkull[0] = key
                w1ClosestSkull[1] = w1DeathNoteDict[key][6]
                w1ClosestSkull[2] = w1DeathNoteDict[key][7]
    if w2LowestSkull < 20:
        for key in w2DeathNoteDict:
            if w2DeathNoteDict[key][6] < w2ClosestSkull[1] and w2DeathNoteDict[key][6] != 0:
                w2ClosestSkull[0] = key
                w2ClosestSkull[1] = w2DeathNoteDict[key][6]
                w2ClosestSkull[2] = w2DeathNoteDict[key][7]
    if w3LowestSkull < 20:
        for key in w3DeathNoteDict:
            if w3DeathNoteDict[key][6] < w3ClosestSkull[1] and w3DeathNoteDict[key][6] != 0:
                w3ClosestSkull[0] = key
                w3ClosestSkull[1] = w3DeathNoteDict[key][6]
                w3ClosestSkull[2] = w3DeathNoteDict[key][7]
    if w4LowestSkull < 20:
        for key in w4DeathNoteDict:
            if w4DeathNoteDict[key][6] < w4ClosestSkull[1] and w4DeathNoteDict[key][6] != 0:
                w4ClosestSkull[0] = key
                w4ClosestSkull[1] = w4DeathNoteDict[key][6]
                w4ClosestSkull[2] = w4DeathNoteDict[key][7]
    if w5LowestSkull < 20:
        for key in w5DeathNoteDict:
            if w5DeathNoteDict[key][6] < w5ClosestSkull[1] and w5DeathNoteDict[key][6] != 0:
                w5ClosestSkull[0] = key
                w5ClosestSkull[1] = w5DeathNoteDict[key][6]
                w5ClosestSkull[2] = w5DeathNoteDict[key][7]

    #lowestSkullList = ["placeholder",w1LowestSkull,w2LowestSkull,w3LowestSkull,w4LowestSkull,w5LowestSkull]
    #print("ConsDeathNote~ Lowest Skulls per world:",lowestSkullList[1:])
    #closestSkullList = [["placeholder",0,0]]
    #closestSkullList = ["placeholder",w1ClosestSkull,w2ClosestSkull,w3ClosestSkull,w4ClosestSkull,w5ClosestSkull]
    #print("ConsDeathNote~ Closest Skulls per world:",closestSkullList[1:])

    fullDeathNoteDict = {
        "w1":[w1LowestSkull,w1ClosestSkull],
        "w2":[w2LowestSkull,w2ClosestSkull],
        "w3":[w3LowestSkull,w3ClosestSkull],
        "w4":[w4LowestSkull,w4ClosestSkull],
        "w5":[w5LowestSkull,w5ClosestSkull],
        "apoc":apocCharactersDict
        }
    #print("ConsDeathNote~ fullDeathNoteDict: ",fullDeathNoteDict)
    #print("ConsDeathNote~ apocCharactersDict: ",apocCharactersDict)
    return fullDeathNoteDict

def setConsDeathNoteProgressionTier(inputJSON, progressionTiers, playerCount, playerNames, fromPublicIEBool):
    fullDeathNoteDict = getDeathNoteKills(inputJSON, playerCount, playerNames, fromPublicIEBool)
    tier_w1DeathNoteSkulls = 0
    tier_w2DeathNoteSkulls = 0
    tier_w3DeathNoteSkulls = 0
    tier_w4DeathNoteSkulls = 0
    tier_w5DeathNoteSkulls = 0
    tier_w6DeathNoteSkulls = 0
    tier_w7DeathNoteSkulls = 0
    tier_w8DeathNoteSkulls = 0
    tier_zows = 0
    tier_chows = 0
    tier_meows = 0
    overall_DeathNoteTier = 0
    advice_w1DeathNoteSkulls = ""
    advice_w2DeathNoteSkulls = ""
    advice_w3DeathNoteSkulls = ""
    advice_w4DeathNoteSkulls = ""
    advice_w5DeathNoteSkulls = ""
    advice_w6DeathNoteSkulls = ""
    advice_w7DeathNoteSkulls = ""
    advice_w8DeathNoteSkulls = ""
    advice_zows = ""
    advice_chows = ""
    advice_meows = ""

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
        #World1
        if tier_w1DeathNoteSkulls >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            if fullDeathNoteDict["w1"][0] >= tier[1]:
                tier_w1DeathNoteSkulls = tier[0]
            else:
                advice_w1DeathNoteSkulls = "Kill more W1 enemies until the minimum skull is the " + getSkullNames(tier[1])
                if fullDeathNoteDict["w1"][1][0] != "":
                    advice_w1DeathNoteSkulls += ". The enemy closest to the next skull is " + getEnemyNameFromMap(fullDeathNoteDict["w1"][1][0]) + ", requires " + '{:,}'.format(fullDeathNoteDict["w1"][1][1]) + " more kills, and is " + str(fullDeathNoteDict["w1"][1][2]) +"% completed."
        #World2
        if tier_w2DeathNoteSkulls >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            if fullDeathNoteDict["w2"][0] >= tier[2]:
                tier_w2DeathNoteSkulls = tier[0]
            else:
                advice_w2DeathNoteSkulls = "Kill more W2 enemies until the minimum skull is the " + getSkullNames(tier[2])
                if fullDeathNoteDict["w2"][1][0] != "":
                    advice_w2DeathNoteSkulls += ". The enemy closest to the next skull is " + getEnemyNameFromMap(fullDeathNoteDict["w2"][1][0]) + ", requires " + '{:,}'.format(fullDeathNoteDict["w2"][1][1]) + " more kills, and is " + str(fullDeathNoteDict["w2"][1][2]) +"% completed."
        #World3
        if tier_w3DeathNoteSkulls >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            if fullDeathNoteDict["w3"][0] >= tier[3]:
                tier_w3DeathNoteSkulls = tier[0]
            else:
                advice_w3DeathNoteSkulls = "Kill more W3 enemies until the minimum skull is the " + getSkullNames(tier[3])
                if fullDeathNoteDict["w3"][1][0] != "":
                    advice_w3DeathNoteSkulls += ". The enemy closest to the next skull is " + getEnemyNameFromMap(fullDeathNoteDict["w3"][1][0]) + ", requires " + '{:,}'.format(fullDeathNoteDict["w3"][1][1]) + " more kills, and is " + str(fullDeathNoteDict["w3"][1][2]) +"% completed."
        #World4
        if tier_w4DeathNoteSkulls >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            if fullDeathNoteDict["w4"][0] >= tier[4]:
                tier_w4DeathNoteSkulls = tier[0]
            else:
                advice_w4DeathNoteSkulls = "Kill more W4 enemies until the minimum skull is the " + getSkullNames(tier[4])
                if fullDeathNoteDict["w4"][1][0] != "":
                    advice_w4DeathNoteSkulls += ". The enemy closest to the next skull is " + getEnemyNameFromMap(fullDeathNoteDict["w4"][1][0]) + ", requires " + '{:,}'.format(fullDeathNoteDict["w4"][1][1]) + " more kills, and is " + str(fullDeathNoteDict["w4"][1][2]) +"% completed."
        #World5
        if tier_w5DeathNoteSkulls >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            if fullDeathNoteDict["w5"][0] >= tier[5]:
                tier_w5DeathNoteSkulls = tier[0]
            else:
                advice_w5DeathNoteSkulls = "Kill more W5 enemies until the minimum skull is the " + getSkullNames(tier[5])
                if fullDeathNoteDict["w5"][1][0] != "":
                    advice_w5DeathNoteSkulls += ". The enemy closest to the next skull is " + getEnemyNameFromMap(fullDeathNoteDict["w5"][1][0]) + ", requires " + '{:,}'.format(fullDeathNoteDict["w5"][1][1]) + " more kills, and is " + str(fullDeathNoteDict["w5"][1][2]) +"% completed."
        #World6
        #World7
        #World8
        #ZOW
        zowRequirementMet = False
        if tier_zows >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            for bb in fullDeathNoteDict["apoc"]:
                if fullDeathNoteDict["apoc"][bb][0][1] >= tier[9]:
                    zowRequirementMet = True
            if zowRequirementMet == True:
                tier_zows = tier[0]
            else:
                if len(fullDeathNoteDict["apoc"]) == 0:
                    advice_zows = "Normally I'd say complete more ZOW stacks here, but first: You gotta have a Barbarian! Come back later :)"
                elif len(fullDeathNoteDict["apoc"]) == 1:
                    advice_zows = "Complete more ZOW stacks: "
                else:
                    advice_zows = "Complete more ZOW stacks on at least 1 Barb/BB: "
                for bb in fullDeathNoteDict["apoc"]:
                    advice_zows += fullDeathNoteDict["apoc"][bb][0][0] + " (" + str(fullDeathNoteDict["apoc"][bb][0][1]) + "/" + str(tier[9]) + "), "
                advice_zows = advice_zows[:-2] #trim off trailing comma and space
        #CHOW
        chowRequirementMet = False
        if tier_chows >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            for bb in fullDeathNoteDict["apoc"]:
                if fullDeathNoteDict["apoc"][bb][0][2] >= tier[10]:
                    chowRequirementMet = True
            if chowRequirementMet == True:
                tier_chows = tier[0]
            else:
                if len(fullDeathNoteDict["apoc"]) == 0:
                    advice_chows = "Normally I'd say complete more CHOW stacks here, but first: You gotta have a Barbarian! (Technically a Blood Barbarian) Come back later :)"
                elif len(fullDeathNoteDict["apoc"]) == 1:
                    advice_chows = "Complete more CHOW stacks: "
                else:
                    advice_chows = "Complete more CHOW stacks on at least 1 BB: "
                for bb in fullDeathNoteDict["apoc"]:
                    advice_chows += fullDeathNoteDict["apoc"][bb][0][0] + " (" + str(fullDeathNoteDict["apoc"][bb][0][2]) + "/" + str(tier[10]) + "), "
                advice_chows = advice_chows[:-2] #trim off trailing comma and space
        #MEOW
        meowRequirementMet = False
        if tier_meows >= (tier[0]-1): #Only evaluate if they already met the previous tier's requirement
            for bb in fullDeathNoteDict["apoc"]:
                if fullDeathNoteDict["apoc"][bb][0][3] >= tier[11]:
                    meowRequirementMet = True
            if meowRequirementMet == True:
                tier_meows = tier[0]
            else:
                if len(fullDeathNoteDict["apoc"]) == 0:
                    advice_meows = "Normally I'd say complete more CHOW stacks here, but first: You gotta have a Barbarian! (Technically a Blood Barbarian) Come back later :)"
                elif len(fullDeathNoteDict["apoc"]) == 1:
                    advice_meows = "Complete more Super CHOW stacks: "
                else:
                    advice_meows = "Complete more Super CHOW stacks on at least 1 BB: "
                for bb in fullDeathNoteDict["apoc"]:
                    advice_meows += fullDeathNoteDict["apoc"][bb][0][0] + " (" + str(fullDeathNoteDict["apoc"][bb][0][3]) + "/" + str(tier[11]) + "), "
                advice_meows = advice_meows[:-2] #trim off trailing comma and space
    #overall_DeathNoteTier = min(progressionTiers[-1][0], tier_w1DeathNoteSkulls)
    overall_DeathNoteTier = min(progressionTiers[-1][0], tier_w1DeathNoteSkulls, tier_w2DeathNoteSkulls, tier_w3DeathNoteSkulls, tier_w4DeathNoteSkulls, tier_w5DeathNoteSkulls)

    #Generate advice statements
    if advice_w1DeathNoteSkulls != "":
        advice_w1DeathNoteSkulls = " * Tier " + str(tier_w1DeathNoteSkulls) + "- " + advice_w1DeathNoteSkulls
    if advice_w2DeathNoteSkulls != "":
        advice_w2DeathNoteSkulls = " * Tier " + str(tier_w2DeathNoteSkulls) + "- " + advice_w2DeathNoteSkulls
    if advice_w3DeathNoteSkulls != "":
        advice_w3DeathNoteSkulls = " * Tier " + str(tier_w3DeathNoteSkulls) + "- " + advice_w3DeathNoteSkulls
    if advice_w4DeathNoteSkulls != "":
        advice_w4DeathNoteSkulls = " * Tier " + str(tier_w4DeathNoteSkulls) + "- " + advice_w4DeathNoteSkulls
    if advice_w5DeathNoteSkulls != "":
        advice_w5DeathNoteSkulls = " * Tier " + str(tier_w5DeathNoteSkulls) + "- " + advice_w5DeathNoteSkulls
    if advice_w6DeathNoteSkulls != "":
        advice_w6DeathNoteSkulls = " * Tier " + str(tier_w6DeathNoteSkulls) + "- " + advice_w6DeathNoteSkulls
    if advice_w7DeathNoteSkulls != "":
        advice_w7DeathNoteSkulls = " * Tier " + str(tier_w7DeathNoteSkulls) + "- " + advice_w7DeathNoteSkulls
    if advice_w8DeathNoteSkulls != "":
        advice_w8DeathNoteSkulls = " * Tier " + str(tier_w8DeathNoteSkulls) + "- " + advice_w8DeathNoteSkulls
    if advice_zows != "":
        advice_zows = " * Informational Tier " + str(tier_zows) + "- " + advice_zows
    if advice_chows != "":
        advice_chows = " * Informational Tier " + str(tier_chows) + "- " + advice_chows
    if advice_meows != "":
        advice_meows = " * Informational Tier " + str(tier_meows) + "- " + advice_meows
    if overall_DeathNoteTier == progressionTiers[-1][0]:
        advice_w1DeathNoteSkulls = " * Nada. You best <3"


    advice_DeathNoteCombined = ["### Best DeathNote tier met: " + str(overall_DeathNoteTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended DeathNote actions:",
        advice_w1DeathNoteSkulls, advice_w2DeathNoteSkulls, advice_w3DeathNoteSkulls, advice_w4DeathNoteSkulls,
        advice_w5DeathNoteSkulls, advice_w6DeathNoteSkulls, advice_w7DeathNoteSkulls, advice_w8DeathNoteSkulls,
        advice_zows, advice_chows, advice_meows]
    consDeathNotePR = progressionResults.progressionResults(overall_DeathNoteTier,advice_DeathNoteCombined,"")
    return consDeathNotePR
