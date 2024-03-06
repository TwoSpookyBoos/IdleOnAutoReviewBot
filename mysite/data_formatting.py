import datetime
import json
import re

import requests

from idleon_SkillLevels import getAllSkillLevelsDict, getHumanReadableClasses

from utils import get_logger


logger = get_logger(__name__)


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
        characterDict[list_index] = dict(
            character_index=list_index,
            character_name=playerNames[list_index],
            class_name=playerClasses[list_index],
            base_class=getBaseClass(playerClasses[list_index]),
            sub_class=getSubclass(playerClasses[list_index]),
            elite_class=getEliteClass(playerClasses[list_index]),
            all_skill_levels=characterSkillsDict[list_index]
        )

    return [playerCount, playerNames, playerClasses, characterDict]


class HeaderData:
    def __init__(self):
        self.direct_json = ""
        self.ie_link = ""
        self.link_text = ""
        self.first_name = ""
        self.json_error = ""
        self.last_update = ""
