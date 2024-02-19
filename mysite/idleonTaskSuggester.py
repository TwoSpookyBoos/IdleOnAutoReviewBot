#idleonTaskSuggester.py
import re
import requests
import json
import datetime

#general stuff that makes this file too big if I include directly
from models import AdviceWorld, WorldName
from models import Character
from idleon_SkillLevels import getHumanReadableClasses
from idleon_SkillLevels import getAllSkillLevelsDict
import idleon_ProgressionTiers


#general autoreview
import idleon_Pinchy
import idleon_CombatLevels
import idleon_Consumables
import idleon_GemShop
import idleon_Greenstacks
import idleon_MaestroHands
import idleon_Cards

from idleon_Pinchy import Placements

#w1
import idleon_Stamps
import idleon_Bribes
import idleon_Smithing

#w2
import idleon_Alchemy
#import idleon_Obols

#w3
#import idleon_Sampling
import idleon_ConsRefinery
import idleon_ConsSaltLick
import idleon_ConsDeathNote
import idleon_ConsBuildings
import idleon_Worship
import idleon_Trapping

#w4
import idleon_Breeding
from utils import get_logger

#Global variables
logger = get_logger(__name__)


#Step 1: Retrieve data from public IdleonEfficiency website or from file
def getJSONfromAPI(runType, url="https://scoli.idleonefficiency.com/raw-data"):
    result = re.search('https://(.*?).idleonefficiency.com', url)
    username = result.group(1)
    username = username.lower()
    #print("Searching for character data from: " + str(url[:-9]))
    if len(username) > 0:
        headers = {
            "Content-Type": "text/json",
            "method": "GET"
        }
        response = requests.get(f"https://cdn2.idleonefficiency.com/profiles/{username.lower()}.json", headers=headers)
    try:
        jsonvalue = response.json()
        parsed = jsonvalue
        return parsed
    except Exception as reason:
        if runType == "web":
            print("idleonTaskSuggester.getJSONfromAPI~ Error retrieving data from IE!", response, reason)
            parsed = []
            return parsed
        elif runType == "consoleTest":
            return "PublicIEProfileNotFound"

def getJSONfromText(runType, rawJSON):
    parsed = []
    #print("idleonTaskSuggester.getJSONfromText~ Input type and Length:", type(rawJSON), len(rawJSON))
    if isinstance(rawJSON, dict):  # Console testing
        if "data" in rawJSON:  # Check to see if this is Toolbox JSON
            parsed = rawJSON["data"]
            if "charNames" in rawJSON:
                parsed["charNames"] = rawJSON["charNames"]
            if "companion" in rawJSON:
                parsed["companion"] = rawJSON["companion"]
                #print("idleonTaskSuggester.getJSONfromText~ Return Point 1: DICT Toolbox JSON found.")
            return parsed
        else:  # Non-Toolbox JSON
            try:
                jsonString = json.dumps(rawJSON)
                #print("idleonTaskSuggester.getJSONfromText~ Type after json.dumps (expecting str):", type(jsonString))
                parsed = json.loads(jsonString)
                #print("idleonTaskSuggester.getJSONfromText~ Type after json.loads (excepting dict):", type(parsed))
                #print("idleonTaskSuggester.getJSONfromText~ Return Point 2: Non-Toolbox JSON found.")
                return parsed
            except Exception as reason:
                if runType == "web":
                    print("idleonTaskSuggester.getJSONfromText~ EXCEPTION Parsing JSON data from console input!", reason)
                    print("idleonTaskSuggester.getJSONfromText~ EXCEPTION Return Point 3: Non-Toolbox JSON found, failed to parse. Returning empty list:", reason)
                    return []
                elif runType == "consoleTest":
                    #print("idleonTaskSuggester.getJSONfromText~ Return Point 4: Non-Toolbox JSON found, failed to parse. Returning 'JSONParseFail-DictException'")
                    print("idleonTaskSuggester.getJSONfromText~ EXCEPTION Parsing JSON data from console input!", reason)
                    return "JSONParseFail-DictException"
    elif isinstance(rawJSON, str):  # Input from the actual website
        #Check to see if this is Toolbox JSON
        if rawJSON.find("lastUpdated") != -1:
            toolboxParsed = json.loads(rawJSON)
            parsed = toolboxParsed["data"]
            if "charNames" in rawJSON:
                parsed["charNames"] = toolboxParsed["charNames"]
            if "companion" in rawJSON:
                parsed["companion"] = toolboxParsed["companion"]
            #print("idleonTaskSuggester.getJSONfromText~ Return Point 5: STRING Toolbox JSON found.")
            return parsed
        else:
            try:
                parsed = json.loads(rawJSON)
                #print("idleonTaskSuggester.getJSONfromText~ Type after json.loads (excepting dict):", type(parsed))
                #print("idleonTaskSuggester.getJSONfromText~ Return Point 6: STRING Non-Toolbox JSON found.")
                return parsed
            except Exception as reason:
                if runType == "web":
                    print("idleonTaskSuggester.getJSONfromText~ Error parsing JSON data from website input!")
                    print("idleonTaskSuggester.getJSONfromText~ Exception reason: ", reason)
                    #print("idleonTaskSuggester.getJSONfromText~ Return Point 7: STRING Non-Toolbox JSON found, failed to parse. Returning empty list.")
                    return []
                elif runType == "consoleTest":
                    #print("idleonTaskSuggester.getJSONfromText~ Return Point 8: STRING Non-Toolbox JSON found, failed to parse. Returning 'JSONParseFail-StringException'")
                    return "JSONParseFail-StringException"
    #print("parsed is a ", type(parsed))
    #print("idleonTaskSuggester.getJSONfromText~ Return Point 9: End of getJSONfromText reached. Returning results.")
    return parsed

def getLastUpdatedTime(inputJSON):
    try:
        timeAwayDict = json.loads(inputJSON['TimeAway'])
        lastUpdatedTimeEpoch = timeAwayDict["GlobalTime"]
        lastUpdatedTimeUTC = datetime.datetime.utcfromtimestamp(lastUpdatedTimeEpoch)
        currentTimeUTC = datetime.datetime.utcnow()
        deltaTime = currentTimeUTC - lastUpdatedTimeUTC
        if deltaTime.days > 0:
            lastUpdatedString = "Save data last updated: " + lastUpdatedTimeUTC.strftime('%Y-%m-%d %H:%M:%S') + " UTC (" + str(deltaTime.days) + " days and " + "{:.1f}".format(deltaTime.seconds/3600) + " hours ago)"
        else:
            lastUpdatedString = "Save data last updated: " + lastUpdatedTimeUTC.strftime('%Y-%m-%d %H:%M:%S') + " UTC (" + "{:.1f}".format(deltaTime.seconds/3600) + " hours ago)"
        #print(lastUpdatedString)
        return lastUpdatedString
    except Exception as reason:
        print("idleonTaskSuggester.getLastUpdatedTime~ EXCEPTION Unable to parse last updated time:", reason)
        return "Unable to parse last updated time, sorry :("


def getBaseClass(inputClass):
    match inputClass:
        case "Warrior" | "Barbarian" | "Blood Berserker" | "Squire" | "Divine Knight":
            return "Warrior"
        case "Mage" | "Shaman" | "Bubonic Conjuror" | "Wizard" | "Elemental Sorcerer":
            return "Mage"
        case "Archer" | "Bowman" | "Siege Breaker" | "Hunter" | "Beast Master":
            return "Archer"
        case "Journeyman" | "Maestro" | "Voidwalker":
            return "Journeyman"
        case "Beginner":
            return "None"
        case _:
            return "UnknownBaseClass" + str(inputClass)

def getSubclass(inputClass):
    match inputClass:
        case "Barbarian" | "Blood Berserker":
            return "Barbarian"
        case "Squire" | "Divine Knight":
            return "Squire"
        case "Shaman" | "Bubonic Conjuror":
            return "Shaman"
        case "Wizard" | "Elemental Sorcerer":
            return "Wizard"
        case "Bowman" | "Siege Breaker":
            return "Bowman"
        case "Hunter" | "Beast Master":
            return "Hunter"
        case "Maestro" | "Voidwalker":
            return "Maestro"
        case "Beginner" | "Warrior" | "Mage" | "Archer" | "Journeyman":
            return "None"
        case _:
            return "UnknownSubclass" + str(inputClass)

def getEliteClass(inputClass):
    match inputClass:
        case "Blood Berserker" | "Divine Knight" | "Bubonic Conjuror" | "Elemental Sorcerer" | "Siege Breaker" | "Beast Master" | "Voidwalker":
            return inputClass
        case "Beginner" | "Warrior" | "Barbarian" | "Squire" | "Mage" | "Shaman" | "Wizard" | "Archer" | "Bowman" | "Hunter" | "Journeyman" | "Maestro":
            return "None"
        case _:
            return "UnknownSubclass" + str(inputClass)

def getCharacterDetails(inputJSON, runType):
    playerCount = 0
    playerNames = []
    playerClasses = []
    characterDict: dict = {}

    if "playerNames" in inputJSON.keys():
        # Present in Public IE and JSON copied from IE
        playerNames = inputJSON['playerNames']
        playerCount = len(playerNames)
        if runType == "web":
            logger.info("From Public IE, found %s characters: %s", playerCount, ', '.join(playerNames))
    elif "charNames" in inputJSON.keys():
        # Present in Toolbox JSON copies
        playerNames = inputJSON['charNames']
        playerCount = len(playerNames)
        if runType == "web":
            print("idleonTaskSuggester.getPlayerCountAndNames~ INFO From Toolbox JSON, found " + str(
                playerCount) + " characters: ", playerNames)
    else:
        try:
            # this produces an unsorted list of names
            cogDataForNames = inputJSON['CogO']
            cogDataList = json.loads(cogDataForNames)
            for item in cogDataList:
                if item.startswith("Player_"):
                    playerCount += 1
                    playerNames.append(item[7:])
            if runType == "web":
                print(
                    "idleonTaskSuggester.getPlayerCountAndNames~ INFO From IE JSON or Toolbox Raw Game JSON, found " + str(
                        playerCount) + " characters: ", playerNames)
        except Exception as reason:
            if runType == "web":
                print(
                    "idleonTaskSuggester.getPlayerCountAndNames~ EXCEPTION Couldn't load Cog data for this account to get the unsorted list of names. Oh well:",
                    reason)

        # Produce a "sorted" list of generic Character names
        counter = 0
        playerNames = []
        while counter < playerCount:
            playerNames.append("Character" + str(counter + 1))
            counter += 1
        # print("idleonTaskSuggester.getPlayerCountAndNames~ INFO Because that playerNames list was unsorted, replacing with generic list for deeper functions to use:", playerNames)

    characterSkillsDict = getAllSkillLevelsDict(inputJSON, playerCount)
    for list_index in range(0, playerCount):
        playerClasses.append(getHumanReadableClasses(inputJSON['CharacterClass_'+str(list_index)]))
        characterDict[list_index] = Character(
            character_index=list_index,
            character_name=playerNames[list_index],
            class_name=playerClasses[list_index],
            base_class=getBaseClass(playerClasses[list_index]),
            sub_class=getSubclass(playerClasses[list_index]),
            elite_class=getEliteClass(playerClasses[list_index]),
            all_skill_levels=characterSkillsDict[list_index]
        )

    return [playerCount, playerNames, playerClasses, characterDict]

def getRoastableStatus(playerNames):
    roastworthyBool = False
    roastworthyList = ["scoli", "weebgasm", "herusx", "rashaken", "trickzbunny", "redpaaaaanda"]
    for name in playerNames:
        if name.lower() in roastworthyList:
            roastworthyBool = True
    return roastworthyBool

def main(inputData, runType="web"):
    bannedAccountsList = ["thedyl", "wooddyl", "3boyy", "4minez", "5arch5", "6knight6", "7maestro7", "bowboy8", "8barb8", "10es10", "favicon.ico", "robots.txt"]
    empty = ""
    emptyList = [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    banned = "This account has been banned from lookups."
    bannedList = [banned,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    bannedListofLists = [
        [bannedList,empty,empty,empty,empty,empty,empty,empty,empty,empty], #general placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w1 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w2 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w3 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w4 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w5 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w6 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w7 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty], #w8 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty] #pinchy placeholder
    ]

    if isinstance(inputData, str):
        inputData = inputData.strip()  # remove leading and trailing whitespaces

    ieLinkList = dict(
        direct_json="",
        ie_link="",
        link_text="",
        first_name="",
        json_error="",
        last_update=""
    )
    #Step 1: Retrieve data from public IdleonEfficiency website or from file
    if len(inputData) < 16 and isinstance(inputData, str):
        #print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for", inputData, "~~~~~~~~~~~~~~~")
        inputData = inputData.replace(" ", "_")  # IE expects underscores instead of spaces in names
        #print("inputData:'" + inputData + "' found in the banned list?", (inputData in bannedAccountsList))
        if inputData.lower() in bannedAccountsList:
            if runType == "web":
                print("idleonTaskSuggester~ PETTY BITCH MODE ACTIVATED. Banned name entered:", inputData)
                return bannedListofLists
            elif runType == "consoleTest":
                return "Banned"
        else:
            parsedJSON = getJSONfromAPI(runType, "https://" + inputData + ".idleonefficiency.com/raw-data")
            if parsedJSON == "PublicIEProfileNotFound" and runType == "consoleTest":
                return "PublicIEProfileNotFound"
            ieLinkString = "Searching for character data from: https://" + inputData.lower() + ".idleonefficiency.com"
            ieLinkList["ie_link"] = f"https://{inputData.lower()}.idleonefficiency.com"
            ieLinkList["link_text"] = f"{inputData.lower()}.idleonefficiency.com"
    else:
        if runType == "web":
            print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for direct web JSON input.~~~~~~~~~~~~~~~")
        parsedJSON = getJSONfromText(runType, inputData)
        ieLinkString = "Searching for character data from direct JSON paste. "
        ieLinkList["direct_json"] = " direct JSON paste"

    if isinstance(parsedJSON, str):
        if parsedJSON.startswith("JSONParseFail"):
            return parsedJSON
    elif parsedJSON is None:
        if runType == "web":
            raise ValueError(f"data for {inputData} not found")
        elif runType == "consoleTest":
            return "JSONParseFail-NoneType"
    elif parsedJSON == []:
        if runType == "web":
            raise ValueError(f"data for {inputData} not found")
            # return errorListofLists
        elif runType == "consoleTest":
            return "JSONParseFail-EmptyList"
        #raise ValueError(f"data for {inputData} not found")

    #Step 2: Get Default progression tiers
    progressionTiers = idleon_ProgressionTiers.setDefaultTiers()

    #Step 3: Send that data off to all the different analyzers
    characterDetailsList = getCharacterDetails(parsedJSON, runType)
    playerCount = characterDetailsList[0]
    playerNames = characterDetailsList[1]
    playerClasses = characterDetailsList[2]
    characterDict = characterDetailsList[3]
    for name in playerNames:
        #print("Checking for name in bannedAccountsList:", name.lower(),  (name.lower() in bannedAccountsList))
        if name.lower() in bannedAccountsList:
            if runType == "web":
                print("idleonTaskSuggester~ WARNING! PETTY BITCH MODE ACTIVATED. Banned name entered:", name)
                return bannedListofLists
            elif runType == "consoleTest":
                return "Banned"
    roastworthyBool = getRoastableStatus(playerNames)

    if ieLinkString.endswith("JSON paste. "):
        if playerNames[0] == "Character1":
            ieLinkString += "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
            ieLinkList["json_error"] = "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
        else:
            ieLinkString += "First character name found: " + playerNames[0]
            ieLinkList["first_name"] = playerNames[0]
            ieLinkList["link_text"] = f"{playerNames[0]}.idleonefficiency.com"
            ieLinkList["ie_link"] = f"https://{playerNames[0]}.idleonefficiency.com"

    #General
    lastUpdatedTimeString = getLastUpdatedTime(parsedJSON)
    ieLinkList["last_update"] = lastUpdatedTimeString
    if runType == "web":
        logger.info(f"{lastUpdatedTimeString = }")
    combatLevelsPR = idleon_CombatLevels.setCombatLevelsProgressionTier(parsedJSON, progressionTiers['Combat Levels'], playerCount, playerNames)
    consumablesList = idleon_Consumables.parseConsumables(parsedJSON, playerCount, playerNames)
    gemShopPR = idleon_GemShop.setGemShopProgressionTier(parsedJSON, progressionTiers['Gem Shop'], playerCount)
    allGStacksList = idleon_Greenstacks.setGStackProgressionTier(parsedJSON, playerCount, progressionTiers['Greenstacks'])
    maestroHandsListOfLists = idleon_MaestroHands.getHandsStatus(parsedJSON, playerCount, playerNames)
    try:
        cardsList = idleon_Cards.getCardSetReview(parsedJSON)
    except Exception as reason:
        cardsList = [["Unable to evaluate card sets :(", str(reason)]]

    #World 1
    stamps_AdviceSection = idleon_Stamps.setStampProgressionTier(parsedJSON, progressionTiers['Stamps'])
    bribes_ActiveSection = idleon_Bribes.setBribesProgressionTier(parsedJSON, progressionTiers['Bribes'])
    smithing_AdviceSection = idleon_Smithing.setSmithingProgressionTier(parsedJSON, progressionTiers['Smithing'], playerCount, characterDict)

    #World 2
    alchBubbles_AdviceSection = idleon_Alchemy.setAlchemyBubblesProgressionTier(parsedJSON, progressionTiers['Alchemy Bubbles'])
    alchVials_AdviceSection = idleon_Alchemy.setAlchemyVialsProgressionTier(parsedJSON, progressionTiers['Alchemy Vials'])
    alchP2W_AdviceSection = idleon_Alchemy.setAlchemyP2W(parsedJSON, playerCount)
    #obolsPR = idleon_Obols.setObolsProgressionTier(parsedJSON, playerCount, progressionTiers['Obols'], fromPublicIEBool)

    #World 3
    #consPrinterPR =
    consRefineryPR = idleon_ConsRefinery.setConsRefineryProgressionTier(parsedJSON, progressionTiers['Construction Refinery'])
    consSaltLickPR = idleon_ConsSaltLick.setConsSaltLickProgressionTier(parsedJSON, progressionTiers['Construction Salt Lick'])
    consDeathNotePR = idleon_ConsDeathNote.setConsDeathNoteProgressionTier(parsedJSON, progressionTiers['Construction Death Note'], playerCount, playerNames)
    consBuildingsPR = idleon_ConsBuildings.setConsBuildingsProgressionTier(parsedJSON, progressionTiers['Construction Buildings Pre-Buffs'], progressionTiers['Construction Buildings Post-Buffs'], playerCount)
    #consAtomColliderPR =
    #worshipTotemsPR =
    worshipPrayersPR = idleon_Worship.setWorshipPrayersProgressionTier(parsedJSON, progressionTiers['Worship Prayers'])
    trappingPR = idleon_Trapping.setTrappingProgressionTier(parsedJSON, playerCount, playerNames)

    #World 4
    #cookingPR =
    #labPR =
    breedingPR = idleon_Breeding.setBreedingProgressionTier(parsedJSON, progressionTiers['Breeding'])
    #print("## World 5 AutoReview")
    #sailingPR =
    #gamingPR =
    #divinityPR =

    generalList = [[ieLinkList, lastUpdatedTimeString], combatLevelsPR.nTR, consumablesList, gemShopPR.nTR, allGStacksList, maestroHandsListOfLists, cardsList]
    w1list = [stamps_AdviceSection["PR"].nTR, bribes_ActiveSection["PR"].nTR, smithing_AdviceSection["PR"].nTR]  # len(stampPR) = 4, len(bribesPR.nTR) = 2, len(smithingPR.nTR) = 4
    w2list = [alchBubbles_AdviceSection["PR"].nTR, alchVials_AdviceSection["PR"].nTR, [alchP2W_AdviceSection['Header'], alchP2W_AdviceSection['OldAdvice']], emptyList]  # len(alchBubblesPR.nTR) = 6, len(alchVialsPR.nTR) = 5
    #w2list = [alchBubblesPR.nTR,alchVialsPR.nTR,alchP2WList, obolsPR.nTR]  # len(alchBubblesPR.nTR) = 6, len(alchVialsPR.nTR) = 4, len(obolsPR.nTR) = 4
    w3list = [
        ["Construction 3D Printer coming soon!"], consRefineryPR.nTR, consSaltLickPR.nTR, consDeathNotePR.nTR,  # len(consRefineryPR.nTR) = 5, len(consSaltLickPR.nTR) = 2, len(consDeathNotePR.nTR) = 12)
        consBuildingsPR.nTR, ["Construction Atom Collider coming soon!"], ["Worship Totems coming soon!"], worshipPrayersPR.nTR, trappingPR.nTR]  # len(consBuildingsPR.nTR) = 8, len(trappingPR.nTR) = 9
    w4list = [breedingPR.nTR, [""], [""]]
    w5list = [[""], [""], [""]]
    #w4list = [["Cooking coming soon!"], ["Breeding coming soon!"], ["Lab coming soon!"]]
    #w5list = [["Sailing coming soon!"], ["Gaming coming soon!"], ["Divinity coming soon!"]]
    w6list = [["w6 mechanic 1 placeholder"], ["w6 mechanic 2 placeholder"], ["w6 mechanic 3 placeholder"]]
    w7list = [["w7 mechanic 1 placeholder"], ["w7 mechanic 2 placeholder"], ["w7 mechanic 3 placeholder"]]
    w8list = [["w8 mechanic 1 placeholder"], ["w8 mechanic 2 placeholder"], ["w8 mechanic 3 placeholder"]]
    biggoleProgressionTiersDict = {
        Placements.COMBAT_LEVELS: combatLevelsPR.cT,
        Placements.STAMPS: stamps_AdviceSection["PR"].cT,
        Placements.BRIBES: bribes_ActiveSection["PR"].cT,
        Placements.SMITHING: smithing_AdviceSection["PR"].cT,
        Placements.BUBBLES: alchBubbles_AdviceSection["PR"].cT,
        Placements.VIALS: alchVials_AdviceSection["PR"].cT,
        Placements.P2W: alchP2W_AdviceSection['AdviceSection'].pinchy_rating,
        Placements.REFINERY: consRefineryPR.cT,
        Placements.SALT_LICK: consSaltLickPR.cT,
        Placements.DEATH_NOTE: consDeathNotePR.cT,
        Placements.PRAYERS: worshipPrayersPR.cT
        }
    pinchy = idleon_Pinchy.generatePinchyWorld(parsedJSON, playerCount, biggoleProgressionTiersDict)

    w1Review = AdviceWorld(
        name=WorldName.WORLD1,
        sections=[stamps_AdviceSection["AdviceSection"], bribes_ActiveSection["AdviceSection"], smithing_AdviceSection["AdviceSection"]],
        banner="w1banner.png"
    )
    w2Review = AdviceWorld(
        name=WorldName.WORLD2,
        sections=[alchBubbles_AdviceSection["AdviceSection"], alchVials_AdviceSection["AdviceSection"], alchP2W_AdviceSection["AdviceSection"]],
        banner="w2banner.png"
    )
    w3Review = AdviceWorld(
        name=WorldName.WORLD3,
        sections=[],
        banner="w3banner.png"
    )

    biggoleAdviceList = [generalList, w1list, w2list, w3list, w4list, w5list, w6list, w7list, w8list, w3Review, w2Review, w1Review, pinchy]

    if runType == "consoleTest":
        return "Pass"
    else:
        return biggoleAdviceList
