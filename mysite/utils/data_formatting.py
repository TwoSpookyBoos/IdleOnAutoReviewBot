import datetime
import json
import traceback

import requests
from babel.dates import format_datetime
from flask import request, g as session_data

from consts import getHumanReadableClasses, getAllSkillLevelsDict
from models.custom_exceptions import ProfileNotFound, EmptyResponse, IEConnectionFailed

from .logging import get_logger


logger = get_logger(__name__)


class HeaderData:
    JSON = "JSON"
    PUBLIC = "Public Profile"

    def __init__(self, input_data):
        self.ie_link = ""
        self.link_text = ""
        self.first_name = ""
        self.json_error = ""

        if isinstance(input_data, str) and len(input_data) < 16:
            username = input_data

            self.data_source = self.PUBLIC
            self.link_text = f"{username}.idleonefficiency.com"
            self.ie_link = f"https://{self.link_text}"
            self.first_name = session_data.account.names[0]
        else:
            self.data_source = self.JSON
            if session_data.account.names[0] == "Character1":
                self.json_error = "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
            else:
                self.first_name = session_data.account.names[0]

        self.__getLastUpdatedTime()

    def __getLastUpdatedTime(self):
        try:
            timeAwayDict = json.loads(session_data.account.raw_data["TimeAway"])
            lastUpdatedTimeEpoch = timeAwayDict["GlobalTime"]
            lastUpdatedTimeUTC = datetime.datetime.utcfromtimestamp(lastUpdatedTimeEpoch)
            currentTimeUTC = datetime.datetime.utcnow()
            deltaTime = currentTimeUTC - lastUpdatedTimeUTC
            days, rest = divmod(deltaTime.total_seconds(), 24 * 60 * 60)
            hours, rest = divmod(rest, 60 * 60)
            minutes, seconds = divmod(rest, 60)

            locale = request.accept_languages.best.replace("-", "_")
            self.elapsed = f"{days:02g}:{hours:02g}:{minutes:02g}:{int(seconds):02g}"
            self.last_update = format_datetime(lastUpdatedTimeUTC, locale=locale) + " UTC"

        except Exception as e:
            logger.warning("Unable to parse last updated time.")
            self.elapsed = "00:00:00:00"
            self.last_update = "Unable to parse last updated time, sorry :("


def getJSONfromAPI(runType, username="scoli"):
    if runType == "web":
        logger.info("~~~~~~~~~~~~~~~ Getting JSON from API ~~~~~~~~~~~~~~~")

    try:
        url = f"https://cdn2.idleonefficiency.com/profiles/{username}.json"
        headers = {"Content-Type": "text/json", "method": "GET"}
        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            raise ProfileNotFound(username)

        account_data = response.json()

        if not account_data:
            raise EmptyResponse(username)

        return account_data

    except requests.exceptions.RequestException as e:
        logger.exception(f"Error retrieving data from IE for %s", e.request.url, exc_info=e)
        raise IEConnectionFailed(e, traceback.format_exc())


def getJSONfromText(runType, rawJSON):
    if runType == "web":
        logger.info("~~~~~~~~~~~~~~~ Parsing submitted JSON ~~~~~~~~~~~~~~~")

    parsed = rawJSON

    if from_toolbox(parsed):  # Check to see if this is Toolbox JSON
        parsed = load_toolbox_data(parsed)

    return parsed


def load_toolbox_data(rawJSON):
    parsed = rawJSON["data"]
    if "charNames" in rawJSON:
        parsed["charNames"] = rawJSON["charNames"]
    if "companion" in rawJSON:
        parsed["companion"] = rawJSON["companion"]
    if "serverVars" in rawJSON:
        if "AutoLoot" in rawJSON["serverVars"]:
            parsed["AutoLoot"] = rawJSON["serverVars"]["AutoLoot"]
    return parsed


def from_toolbox(rawJSON):
    return "data" in rawJSON


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
        case (
            "Beginner" | "Warrior" | "Barbarian" | "Squire" | "Mage" | "Shaman" | "Wizard" | "Archer" | "Bowman" | "Hunter" | "Journeyman" | "Maestro"
        ):
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
        playerNames = inputJSON["playerNames"]
        playerCount = len(playerNames)
        if runType == "web":
            logger.info(
                "From Public IE, found %s characters: %s",
                playerCount,
                ", ".join(playerNames),
            )
    elif "charNames" in inputJSON.keys():
        # Present in Toolbox JSON copies
        playerNames = inputJSON["charNames"]
        playerCount = len(playerNames)
        if runType == "web":
            logger.info(
                f"From Toolbox JSON, found %s characters: %s",
                playerCount,
                ", ".join(playerNames),
            )
    else:
        try:
            # this produces an unsorted list of names
            cogDataForNames = inputJSON["CogO"]
            cogDataList = json.loads(cogDataForNames)
            for item in cogDataList:
                if item.startswith("Player_"):
                    playerCount += 1
                    playerNames.append(item[7:])
            if runType == "web":
                logger.info(
                    f"From IE JSON or Toolbox Raw Game JSON, found {playerCount} unsorted characters: %s",
                    ", ".join(playerNames),
                )
        except:
            if runType == "web":
                logger.warning("Failed to load Cog data to get the unsorted list of names. Replacing with generic list.")

        # Produce a "sorted" list of generic Character names
        playerNames = []
        for counter in range(0, playerCount):
            playerNames.append(f"Character{counter+1}")

    characterSkillsDict = getAllSkillLevelsDict(inputJSON, playerCount)
    perSkillDict = characterSkillsDict["Skills"]

    for list_index in range(0, playerCount):
        try:
            playerClasses.append(getHumanReadableClasses(inputJSON[f"CharacterClass_{list_index}"]))
        except:
            playerClasses.append("Unknown")
        characterDict[list_index] = dict(
            character_index=list_index,
            character_name=playerNames[list_index],
            class_name=playerClasses[list_index],
            base_class=getBaseClass(playerClasses[list_index]),
            sub_class=getSubclass(playerClasses[list_index]),
            elite_class=getEliteClass(playerClasses[list_index]),
            all_skill_levels=characterSkillsDict[list_index],
        )

    return [playerCount, playerNames, playerClasses, characterDict, perSkillDict]
