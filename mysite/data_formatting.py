import datetime
import json
import re

import requests
from babel.dates import format_datetime
from flask import request, g as session_data

from consts import getHumanReadableClasses, getAllSkillLevelsDict

from utils import get_logger


logger = get_logger(__name__)


class HeaderData:
    JSON = "JSON"
    PUBLIC = "Public Profile"

    def __init__(self):
        self.data_source = ""
        self.direct_json = ""
        self.ie_link = ""
        self.link_text = ""
        self.first_name = ""
        self.json_error = ""
        self.last_update = ""
        self.elapsed = ""


def getJSONfromAPI(runType, url="https://scoli.idleonefficiency.com/raw-data"):
    result = re.search('https://(.*?).idleonefficiency.com', url)
    username = result.group(1)
    username = username.lower()
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
    except:
        if runType == "web":
            logger.exception(f"Error retrieving data from IE! Response: {response}")
            parsed = []
            return parsed
        elif runType == "consoleTest":
            return "PublicIEProfileNotFound"


def getJSONfromText(runType, rawJSON):
    parsed = []
    if isinstance(rawJSON, dict):  # Console testing
        if "data" in rawJSON:  # Check to see if this is Toolbox JSON
            parsed = rawJSON["data"]
            if "charNames" in rawJSON:
                parsed["charNames"] = rawJSON["charNames"]
            if "companion" in rawJSON:
                parsed["companion"] = rawJSON["companion"]
            if "serverVars" in rawJSON:
                if "AutoLoot" in rawJSON["serverVars"]:
                    parsed["AutoLoot"] = rawJSON["serverVars"]["AutoLoot"]
            return parsed
        else:  # Non-Toolbox JSON
            try:
                jsonString = json.dumps(rawJSON)
                parsed = json.loads(jsonString)
                return parsed
            except:
                if runType == "web":
                    logger.exception("Non-Toolbox JSON found during 'web' run failed to parse. Returning empty list :(")
                    return []
                elif runType == "consoleTest":
                    logger.debug("Non-Toolbox JSON found during 'consoleTest' run failed to parse. Returning 'JSONParseFail-DictException'")
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
            return parsed
        else:
            try:
                parsed = json.loads(rawJSON)
                return parsed
            except:
                if runType == "web":
                    logger.exception("Failure during json.loads during 'web' run. Returning empty list :(")
                    return []
                elif runType == "consoleTest":
                    logger.debug("Non-Toolbox JSON found during 'consoleTest' run failed to parse. Returning 'JSONParseFail-StringException'")
                    return "JSONParseFail-StringException"
    return parsed


def getLastUpdatedTime(headerData: HeaderData):
    try:
        timeAwayDict = json.loads(session_data.account.raw_data["TimeAway"])
        lastUpdatedTimeEpoch = timeAwayDict["GlobalTime"]
        lastUpdatedTimeUTC = datetime.datetime.utcfromtimestamp(lastUpdatedTimeEpoch)
        currentTimeUTC = datetime.datetime.utcnow()
        deltaTime = currentTimeUTC - lastUpdatedTimeUTC
        days, rest = divmod(deltaTime.total_seconds(), 24 * 60 * 60)
        hours, rest = divmod(rest, 60 * 60)
        minutes, seconds = divmod(rest, 60)

        locale = request.accept_languages.best.replace('-', '_')
        headerData.elapsed = f"{days:02g}:{hours:02g}:{minutes:02g}:{int(seconds):02g}"
        headerData.last_update = format_datetime(lastUpdatedTimeUTC, locale=locale) + " UTC"

    except Exception as e:
        logger.warning("Unable to parse last updated time.")
        headerData.elapsed = "00:00:00:00"
        headerData.last_update = "Unable to parse last updated time, sorry :("


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
            return "Beginner"
        case _:
            return f"UnknownBaseClass-{inputClass}"


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
            return f"UnknownSubclass-{inputClass}"


def getEliteClass(inputClass):
    match inputClass:
        case "Blood Berserker" | "Divine Knight" | "Bubonic Conjuror" | "Elemental Sorcerer" | "Siege Breaker" | "Beast Master" | "Voidwalker":
            return inputClass
        case "Beginner" | "Warrior" | "Barbarian" | "Squire" | "Mage" | "Shaman" | "Wizard" | "Archer" | "Bowman" | "Hunter" | "Journeyman" | "Maestro":
            return "None"
        case _:
            return f"UnknownEliteClass-{inputClass}"


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
            logger.info(f"From Toolbox JSON, found %s characters: %s", playerCount, ', '.join(playerNames))
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
                logger.info(f"From IE JSON or Toolbox Raw Game JSON, found {playerCount} unsorted characters: %s", ', '.join(playerNames))
        except:
            if runType == "web":
                logger.warning("Failed to load Cog data to get the unsorted list of names. Replacing with generic list.")

        # Produce a "sorted" list of generic Character names
        playerNames = []
        for counter in range(0, playerCount):
            playerNames.append(f"Character{counter+1}")

    characterSkillsDict = getAllSkillLevelsDict(inputJSON, playerCount)
    perSkillDict = characterSkillsDict['Skills']

    for list_index in range(0, playerCount):
        playerClasses.append(getHumanReadableClasses(inputJSON[f'CharacterClass_{list_index}']))
        characterDict[list_index] = dict(
            character_index=list_index,
            character_name=playerNames[list_index],
            class_name=playerClasses[list_index],
            base_class=getBaseClass(playerClasses[list_index]),
            sub_class=getSubclass(playerClasses[list_index]),
            elite_class=getEliteClass(playerClasses[list_index]),
            all_skill_levels=characterSkillsDict[list_index]
        )

    return [playerCount, playerNames, playerClasses, characterDict, perSkillDict]
