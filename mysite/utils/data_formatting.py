import datetime
import json
import re
import traceback
from pathlib import Path

import requests
import yaml
from babel.dates import format_datetime
from flask import request, g as session_data

from consts import humanReadableClasses, skillIndexList, emptySkillList
from models.custom_exceptions import ProfileNotFound, EmptyResponse, IEConnectionFailed

from .logging import get_logger
from config import app


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
            self.link_text = app.config["IE_PROFILE_TEMPLATE"].format(username=username)
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
            timeAwayDict = safe_loads(session_data.account.raw_data["TimeAway"])
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
        url = app.config["IE_JSON_TEMPLATE"].format(username=username)
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
    parsed = rawJSON.get("data", {})
    parsed["charNames"] = rawJSON.get("charNames", [])
    parsed["companion"] = rawJSON.get("companion", {})
    parsed["guildData"] = rawJSON.get("guildData", {})
    parsed["AutoLoot"] = rawJSON.get("serverVars", {}).get("AutoLoot", 0)
    if not isinstance(parsed.get("AutoLoot"), int):
        try:
            parsed["AutoLoot"] = int(parsed["AutoLoot"])
        except:
            logger.exception(f"Unexpected datatype found for AutoLoot: {type(parsed.get('AutoLoot'))}: {parsed.get('AutoLoot')}. Setting to 0")
            parsed["AutoLoot"] = 0

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
            if isinstance(cogDataForNames, str):
                cogDataForNames = safe_loads(cogDataForNames)
            for item in cogDataForNames:
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
    equipped_prayers = {}
    postOfficeList = []
    for list_index in range(0, playerCount):
        try:
            playerClasses.append(getHumanReadableClasses(inputJSON[f"CharacterClass_{list_index}"]))
        except:
            playerClasses.append(f"UnknownClass{list_index}")
        try:
            postOfficeList.append(safe_loads(inputJSON[f"POu_{list_index}"]))
        except:
            postOfficeList.append([0]*36)
        try:
            equipped_prayers[list_index] = safe_loads(inputJSON[f"Prayers_{list_index}"])
        except:
            equipped_prayers[list_index] = []
        characterDict[list_index] = dict(
            character_index=list_index,
            character_name=playerNames[list_index],
            class_name=playerClasses[list_index],
            base_class=getBaseClass(playerClasses[list_index]),
            sub_class=getSubclass(playerClasses[list_index]),
            elite_class=getEliteClass(playerClasses[list_index]),
            equipped_prayers=equipped_prayers[list_index],
            all_skill_levels=characterSkillsDict[list_index],
            po_boxes=postOfficeList[list_index]
        )

    return [playerCount, playerNames, playerClasses, characterDict, perSkillDict]


def getAllSkillLevelsDict(inputJSON, playerCount):
    allSkillsDict = {'Skills': {}}
    for characterIndex in range(0, playerCount):
        if characterIndex not in allSkillsDict:
            allSkillsDict[characterIndex] = {}
        try:
            characterSkillList = inputJSON[f'Lv0_{characterIndex}']
        except:
            characterSkillList = emptySkillList
            logger.exception(f"Could not retrieve LV0_{characterIndex} from JSON. Setting character to all -1s for levels")
        for skillCounter in range(0, len(skillIndexList)):
            if skillIndexList[skillCounter] not in allSkillsDict['Skills']:
                allSkillsDict['Skills'][skillIndexList[skillCounter]] = []
            try:
                allSkillsDict[characterIndex][skillIndexList[skillCounter]] = characterSkillList[skillCounter]
                allSkillsDict['Skills'][skillIndexList[skillCounter]].append(characterSkillList[skillCounter])
            except:
                allSkillsDict[characterIndex][skillIndexList[skillCounter]] = 0
                allSkillsDict['Skills'][skillIndexList[skillCounter]].append(0)
                logger.exception(f"Unable to retrieve Lv0_{characterIndex}'s Skill level for {skillIndexList[skillCounter]}")
    return allSkillsDict


def getHumanReadableClasses(classNumber):
    return humanReadableClasses.get(classNumber, f"Unknown class: {classNumber}")


def getSpecificSkillLevelsList(desiredSkill: str|int) -> list[int]:
    if isinstance(desiredSkill, str):
        try:
            return session_data.account.all_skills[desiredSkill]
        except:
            logger.exception(f"Could not retrieve skill data for {desiredSkill}")
            return emptySkillList
    elif isinstance(desiredSkill, int):
        try:
            return session_data.account.all_skills[skillIndexList[desiredSkill]]
        except:
            logger.exception(f"Could not find Index for desiredSkill of {desiredSkill}")
            return emptySkillList


def setCustomTiers(filename="input.csv"):
    return


def safe_loads(data):
    return json.loads(data) if isinstance(data, str) else data

def mark_advice_completed(advice):
    try:
        prog = str(advice.progression).strip("%")
        goal = str(advice.goal).strip("%")
        if advice.goal and advice.progression and float(prog) >= float(goal):
            advice.progression = ""
            advice.goal = "✔"
            setattr(advice, "status", "complete")
    except:
        pass


def scrape_slab():
    url_wiki_slab_raw = "https://raw.githubusercontent.com/BigCoight/IdleonWikiBot3.0/master/exported/ts/data/SpecificItemRepo.ts"
    response = requests.get(url_wiki_slab_raw)
    slab_file = response.text

    regex = (r'''
        "internalName":   # find the key and skip it
        \s*               # skip any whitespace between the key and value
        "([^"]+)"         # capture everything between, but not also, quotes
        ,\s*              # skip the trailing comma and whitespace (newline, leading whitespace) to next line
        "displayName":    # find the key and skip it
        \s*               # skip any whitespace between the key and value
        "([^"]+)"         # capture everything between, but not also, quotes
    ''')
    pattern = re.compile(regex, re.VERBOSE | re.DOTALL)
    matches = pattern.findall(slab_file)

    # Prepare the dictionary for YAML conversion
    item_dict = {internal: display for internal, display in matches}
    # This stuff isn't exactly an item but it does show up
    item_dict.update(dict(
        Blank="Blank",
        LockedInvSpace="Locked Inventory Space",
        # oah is the proper spelling for the dungeon bow, but aoh is the spelling of the normal Bow
        DungWeaponBowD1="Pharaoh Bow I",
        DungWeaponBowD2="Pharaoh Bow II",
        DungWeaponBowD3="Pharaoh Bow III",
        DungWeaponBowD4="Pharaoh Bow IV",
        DungWeaponBowD5="Pharaoh Bow V",
        #Similar to the bow, force consistency between 'Hotdog' and 'Hot Dog'
        FoodHealth3="Hot Dog",
        FoodHealth2d="Hot Dog",
        Critter6A="Eternal Lord of The Undying Ember",  #Wiki has 2x spaces in the name "of  The"
        Quest2="Mining Certificate"
    ))

    # Convert the dictionary to YAML format
    with open(Path(app.static_folder)/"items.yaml", "w+") as items_file:
        items_file.truncate()
        yaml.dump(item_dict, items_file, sort_keys=False)
        items_file.seek(0)
        yaml_content = items_file.read()

        # Output the YAML content
        print(yaml_content)
