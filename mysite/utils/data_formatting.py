import datetime
import json
import math
import re
import traceback
from pathlib import Path

import requests
import yaml
from babel.dates import format_datetime
from flask import request, g as session_data

from consts import humanReadableClasses, skillIndexList, emptySkillList, maxCharacters, obols_dict
from models.custom_exceptions import ProfileNotFound, EmptyResponse, APIConnectionFailed, WtfDataException

from .logging import get_logger
from config import app
from .text_formatting import InputType

logger = get_logger(__name__)


class HeaderData:
    JSON = "JSON"
    PUBLIC = "Public Profile"
    is_stale: bool = False

    def __init__(self, input_data, source_string):
        self.ie_link = ""
        self.link_text = ""
        self.first_name = ""
        self.json_error = ""

        if isinstance(input_data, str) and len(input_data) < 16:
            username = input_data

            self.data_source = self.PUBLIC
            self.link_text = app.config[f"{source_string}_PROFILE_TEMPLATE"].format(username=username)
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
            self.is_stale = deltaTime.total_seconds() >= 24 * 60 * 60

        except Exception as e:
            logger.warning("Unable to parse last updated time.")
            self.elapsed = "00:00:00:00"
            self.last_update = "Unable to parse last updated time, sorry :("


def getJSONfromAPI(runType, username="scoli", source_string=InputType.ALL):
    # logger.debug(f"{username = }")
    accepted_apis = [
        InputType.IE,
        #InputType.LB,
        InputType.IT  #Last to be evaluated intentionally as it currently provides the fullest data
    ] if source_string == InputType.ALL else [source_string]
    api_data = {
        entry.value: {'Data': {}, 'LastUpdated': 0, 'Summary': '', 'Exception': '', 'Traceback': ''} for entry in accepted_apis
    }

    for api_name in api_data.keys():
        try:
            url = app.config[f'{api_name}_JSON_TEMPLATE'].format(username=username if api_name == 'IT' else username.lower())
            if runType == "web":
                logger.info(f"~~~ Getting JSON from {api_name} API: {url} ~~~")
            headers = {"Content-Type": "text/json", "method": "GET"}
            response = requests.get(url, headers=headers)

            if response.status_code in [204, 403, 404]:
                api_data[api_name]['Summary'] = 'ProfileNotFound'
                logger.debug(f"{api_name} responded with {response.status_code}. Skipping.")
                continue
                #raise ProfileNotFound(username)

            account_data = response.json()
            if not account_data:
                api_data[api_name]['Summary'] = 'EmptyResponse'
                continue
                #raise EmptyResponse(username)

            api_data[api_name]['Data'] = (
                load_toolbox_data(account_data) if api_name == 'IT'
                else account_data
            )
            api_data[api_name]['LastUpdated'] = safe_loads(safe_loads(safe_loads(api_data[api_name]['Data']).get('TimeAway', {})).get('GlobalTime', 0))
            # logger.debug(f"Last updated time epoch = {api_data[api_name]['LastUpdated']}")
        except requests.exceptions.RequestException as e:
            logger.warning(f"Error retrieving data from {api_name}: {e}")
            api_data[api_name]['Exception'] = e
            api_data[api_name]['Traceback'] = traceback.format_exc()

    freshest = ('', 0)
    for api_name, api_dict in api_data.items():
        #If IE and IT are tied (the equals scenario), take Toolbox as it contains more information
        if api_dict['LastUpdated'] >= freshest[1]:
            freshest = (api_name, api_dict['LastUpdated'])
    if freshest[1] == 0:
        raise ProfileNotFound(username)
    if freshest[0] == '':
        # TODO: Figure out combining this information into a single exception, if somehow all sources errored
        raise APIConnectionFailed(api_data["IE"]["Exception"], api_data["IE"]["Traceback"])
    else:
        # logger.debug(f'Freshest data source: {freshest[0]}')
        return api_data[freshest[0]]['Data'], freshest[0]

def getJSONfromText(runType, rawJSON):
    if runType == "web":
        logger.info("~~~~~~~~~~~~~~~ Parsing submitted JSON ~~~~~~~~~~~~~~~")

    parsed = rawJSON

    if from_toolbox(parsed):  # Check to see if this is Toolbox JSON
        parsed = load_toolbox_data(parsed)
        source_string = 'Toolbox JSON'
    else:
        source_string = 'Other JSON'

    if "OptLacc" not in parsed:
        raise WtfDataException(rawJSON)

    return parsed, source_string


def load_toolbox_data(rawJSON):
    parsed = rawJSON.get("data", {})
    parsed["charNames"] = rawJSON.get("charNames", [])
    parsed["companion"] = rawJSON.get("companion", {})
    parsed["guildData"] = rawJSON.get("guildData", {})
    parsed["serverVars"] = rawJSON.get("serverVars", {})
    parsed["AutoLoot"] = rawJSON.get("serverVars", {}).get("AutoLoot", 0)
    parsed['parsedData'] = rawJSON.get('parsedData', {})  #Only available on Public Toolbox profiles
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
        case "Warrior" | "Barbarian" | "Blood Berserker" | "Death Bringer" | "Squire" | "Divine Knight":
            return "Warrior"
        case "Mage" | "Shaman" | "Bubonic Conjuror" | "Wizard" | "Elemental Sorcerer":
            return "Mage"
        case "Archer" | "Bowman" | "Siege Breaker" | "Hunter" | "Beast Master" | 'Wind Walker':
            return "Archer"
        case "Journeyman" | "Maestro" | "Voidwalker":
            return "Journeyman"
        case "Beginner":
            return "Beginner"
        case _:
            return f"UnknownBaseClass-{inputClass}"


def getSubclass(inputClass):
    match inputClass:
        case "Barbarian" | "Blood Berserker" | "Death Bringer":
            return "Barbarian"
        case "Squire" | "Divine Knight":
            return "Squire"
        case "Shaman" | "Bubonic Conjuror":
            return "Shaman"
        case "Wizard" | "Elemental Sorcerer":
            return "Wizard"
        case "Bowman" | "Siege Breaker":
            return "Bowman"
        case "Hunter" | "Beast Master" | 'Wind Walker':
            return "Hunter"
        case "Maestro" | "Voidwalker":
            return "Maestro"
        case "Beginner" | "Warrior" | "Mage" | "Archer" | "Journeyman":
            return "None"
        case _:
            return f"UnknownSubclass-{inputClass}"


def getEliteClass(inputClass):
    match inputClass:
        case "Blood Berserker" | "Death Bringer":
            return "Blood Berserker"
        case 'Beast Master' | 'Wind Walker':
            return 'Beast Master'
        case "Divine Knight" | "Bubonic Conjuror" | "Elemental Sorcerer" | "Siege Breaker" | "Beast Master" | "Voidwalker":
            return inputClass
        case (
            "Beginner" | "Warrior" | "Barbarian" | "Squire" | "Mage" | "Shaman" | "Wizard" | "Archer" | "Bowman" | "Hunter" | "Journeyman" | "Maestro"
        ):
            return "None"
        case _:
            return f"UnknownEliteClass-{inputClass}"

def getMasterClass(inputClass):
    match inputClass:
        case 'Death Bringer' | 'Wind Walker':
            return inputClass
        case (
            "Blood Berserker" | "Divine Knight" | "Bubonic Conjuror" | "Elemental Sorcerer" | "Siege Breaker" | "Beast Master" | "Voidwalker" | "Beginner" | "Warrior" | "Barbarian" | "Squire" | "Mage" | "Shaman" | "Wizard" | "Archer" | "Bowman" | "Hunter" | "Journeyman" | "Maestro"
        ):
            return "None"
        case _:
            return f"UnknownMasterClass-{inputClass}"


def getCharacterDetails(inputJSON, runType):
    character_count = 0
    character_names = []
    character_classes = []

    if "playerNames" in inputJSON.keys():
        # Present in Public IE and JSON copied from IE
        character_names = inputJSON["playerNames"]
        character_count = len(character_names)
        if runType == "web":
            logger.info(
                "From Public IE or IE JSON, found %s characters: %s",
                character_count,
                ", ".join(character_names),
            )
    elif "charNames" in inputJSON.keys():
        # Present in Toolbox JSON copies
        character_names = inputJSON["charNames"]
        character_count = len(character_names)
        if runType == "web":
            logger.info(
                f"From Toolbox JSON, found %s characters: %s",
                character_count,
                ", ".join(character_names),
            )
    elif "PlayerNames" in inputJSON.keys():
        #IdleonSaver tool, wow
        character_names = inputJSON['PlayerNames']
        character_count = len(character_names)
        if runType == "web":
            logger.info(
                "From IdleonSaver or other 3rd party tool, found %s characters: %s",
                character_count,
                ", ".join(character_names),
            )
    else:
        try:
            # this produces an unsorted list of names
            cogDataForNames = inputJSON["CogO"]
            if isinstance(cogDataForNames, str):
                cogDataForNames = safe_loads(cogDataForNames)
            for item in cogDataForNames:
                if item.startswith("Player_"):
                    character_count += 1
                    character_names.append(item[7:])
            if runType == "web":
                logger.info(
                    f"From IE JSON or Toolbox Raw Game JSON, found {character_count} unsorted characters: %s",
                    ", ".join(character_names),
                )
        except:
            if runType == "web":
                logger.warning("Failed to load Cog data to get the unsorted list of names. Replacing with generic list.")

        # Produce a "sorted" list of generic Character names
        character_names = []
        for counter in range(0, character_count):
            character_names.append(f"Character{counter+1}")

    if character_count == 0:
        logger.exception(f"This data has a character_count of 0, wtf? Aborting.")
        raise WtfDataException(json.dumps(inputJSON))
    characterSkillsDict = getAllSkillLevelsDict(inputJSON, character_count)
    perSkillDict = characterSkillsDict["Skills"]
    characterMaxTalents = {}
    characterCurrentPresetTalents = {}

    characterSecondaryPresetTalents = {}
    current_preset_talent_bar = {}
    secondary_preset_talent_bar = {}
    characterDict = {}
    equipped_prayers = {}
    postOfficeList = []
    equipped_lab_chips = {}
    inventory_bags = {}
    kill_lists = {}
    obols_list = {}
    obol_upgrades_list = {}
    big_alch_bubbles_dict = safe_loads(inputJSON.get('CauldronBubbles', [0,0,0] * maxCharacters))
    alchemy_jobs_list = safe_loads(inputJSON.get('CauldronJobs1', [-1] * maxCharacters))

    for character_index in range(0, character_count):
        character_classes.append(getHumanReadableClasses(inputJSON.get(f'CharacterClass_{character_index}', 0)))
        postOfficeList.append(safe_loads(inputJSON.get(f'POu_{character_index}', [0]*36)))
        equipped_prayers[character_index] = safe_loads(inputJSON.get(f'Prayers_{character_index}', []))
        characterMaxTalents[character_index] = safe_loads(inputJSON.get(f'SM_{character_index}', {}))
        characterCurrentPresetTalents[character_index] = safe_loads(inputJSON.get(f'SL_{character_index}', {}))
        characterSecondaryPresetTalents[character_index] = safe_loads(inputJSON.get(f'SLpre_{character_index}', {}))
        inventory_bags[character_index] = safe_loads(inputJSON.get(f'InvBagsUsed_{character_index}', {}))
        kill_lists[character_index] = safe_loads(inputJSON.get(f'KLA_{character_index}', []))
        obols_list[character_index] = safe_loads(inputJSON.get(f'ObolEqO0_{character_index}', []))
        obol_upgrades_list[character_index] = safe_loads(inputJSON.get(f'ObolEqMAP_{character_index}', {}))
        try:
            equipped_lab_chips[character_index] = safe_loads(inputJSON['Lab'])[character_index+1]
        except:
            equipped_lab_chips[character_index] = []
        current_preset_talent_bar[character_index] = safe_loads(inputJSON.get(f'AttackLoadout_{character_index}', []))
        secondary_preset_talent_bar[character_index] = safe_loads(inputJSON.get(f'AttackLoadoutpre_{character_index}', []))

        characterDict[character_index] = dict(
            character_index=character_index,
            character_name=character_names[character_index],
            class_name=character_classes[character_index],
            base_class=getBaseClass(character_classes[character_index]),
            sub_class=getSubclass(character_classes[character_index]),
            elite_class=getEliteClass(character_classes[character_index]),
            master_class=getMasterClass(character_classes[character_index]),
            equipped_prayers=equipped_prayers[character_index],
            all_skill_levels=characterSkillsDict[character_index],
            max_talents=characterMaxTalents[character_index],
            current_preset_talents=characterCurrentPresetTalents[character_index],
            secondary_preset_talents=characterSecondaryPresetTalents[character_index],
            current_preset_talent_bar=current_preset_talent_bar[character_index],
            secondary_preset_talent_bar=secondary_preset_talent_bar[character_index],
            po_boxes=postOfficeList[character_index],
            equipped_lab_chips=equipped_lab_chips[character_index],
            inventory_bags=inventory_bags[character_index],
            kill_dict={k:v for k, v in enumerate(kill_lists[character_index])},
            obols=obols_list[character_index],
            obol_upgrades=obol_upgrades_list[character_index],
            big_alch_bubbles=big_alch_bubbles_dict[character_index],
            alchemy_job=alchemy_jobs_list[character_index]
        )

    return [character_count, character_names, character_classes, characterDict, perSkillDict]


def getAllSkillLevelsDict(inputJSON, playerCount):
    allSkillsDict = {
        'Skills': {skill: [] for skill in skillIndexList}
    }
    for characterIndex in range(0, playerCount):
        if characterIndex not in allSkillsDict:
            allSkillsDict[characterIndex] = {}
        try:
            characterSkillList = inputJSON[f'Lv0_{characterIndex}']
        except:
            characterSkillList = emptySkillList
            logger.exception(f"Could not retrieve LV0_{characterIndex} from JSON. Setting character to all 0s for levels")
        for skillCounter in range(0, len(skillIndexList)):
            try:
                allSkillsDict[characterIndex][skillIndexList[skillCounter]] = characterSkillList[skillCounter]
                allSkillsDict['Skills'][skillIndexList[skillCounter]].append(characterSkillList[skillCounter])
            except:
                allSkillsDict[characterIndex][skillIndexList[skillCounter]] = 0
                allSkillsDict['Skills'][skillIndexList[skillCounter]].append(0)
                logger.exception(f"Unable to retrieve Lv0_{characterIndex}'s Skill level for {skillIndexList[skillCounter]}")
    return allSkillsDict

# This returns incomplete data, since the obols_dict currently only contains DR obols
# Dispite this, the function is written to work with whatever data is added to the obols_dict
def get_obol_totals(obol_list, obol_upgrade_dict):
    obols_totals = {}
    for obol_index, obol_name in enumerate(obol_list):
        obol_index = str(obol_index)
        # Adds the base values for each equipped obol
        for obol_base_name, obol_base_value in obols_dict.get(obol_name, {}).get('Base', {}).items():
            obols_totals[f"Total{obol_base_name}"] = obols_totals.get(f"Total{obol_base_name}", 0) + obol_base_value
        # Adds any upgrade value for each equipped obol
        if obol_index in obol_upgrade_dict.keys():
            if 'UQ1txt' in obol_upgrade_dict[obol_index] and obol_upgrade_dict[obol_index]['UQ1txt'] != 0:
                try:
                    obols_totals[f"Total{obol_upgrade_dict[obol_index]['UQ1txt']}"] = (
                        obols_totals.get(f"Total{obol_upgrade_dict[obol_index]['UQ1txt']}", 0)
                        + safer_convert(obol_upgrade_dict[obol_index]['UQ1val'], 0)
                    )
                except:
                    logger.exception(f"Could not parse Obol UQ1txt at {obol_index}: {obol_upgrade_dict[obol_index]}")
            if 'UQ2txt' in obol_upgrade_dict[obol_index] and obol_upgrade_dict[obol_index]['UQ2txt'] != 0:
                try:
                    obols_totals[f"Total{obol_upgrade_dict[obol_index]['UQ2txt']}"] = (
                        obols_totals.get(f"Total{obol_upgrade_dict[obol_index]['UQ2txt']}", 0)
                        + safer_convert(obol_upgrade_dict[obol_index]['UQ2val'], 0)
                    )
                except:
                    logger.exception(f"Could not parse Obol UQ2txt at {obol_index}: {obol_upgrade_dict[obol_index]}")
            for upgrade_val in ['STR', 'AGI', 'WIS', 'LUK', 'Defence', 'Weapon_Power', 'Reach', 'Speed']:
                obols_totals[f"Total{upgrade_val}"] = obols_totals.get(f"Total{upgrade_val}", 0) + obol_upgrade_dict.get(upgrade_val, 0)
    return obols_totals

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

def safer_get(data, query, default):
    """
    Replace Nonetype result with default param if encountered.
    Also attempts to typecast the result to the same type as Default param.
    """
    try:
        result = data.get(query, default)
        if isinstance(result, type(default)):
            return result
        else:
            return safer_convert(result, default)
    except AttributeError:
        logger.exception(f"Could not .get() from provided {type(data)} data. Returning default.")
        return default
    except Exception as e:
        logger.exception(f"Something else went wrong lol: {e}")
        return default


def safer_convert(data, default):
    try:
        if data is None:
            return default
        elif isinstance(default, int):
            return int(float(data)) if data else default
        else:
            return type(default)(data)
    except (TypeError, ValueError):
        logger.exception(f"Could not convert [{type(data)}: {data}] to [{type(default)}: {default}]. Returning default.")
        return default
    except Exception as e:
        logger.exception(f"Something else went wrong lol: {e}")
        return default

def safer_math_pow(base, exponent, default=1e100):
    try:
        return math.pow(base, exponent)
    except:
        logger.exception(f"An error occurred during math.pow() call. Replacing with default: {default}")
        return 1e100

def safer_math_log(input_value, base):
    """
    :param input_value:
    :param base: Lava, lava, or 10 will all use Lava's pow10 estimate
    """
    if base == 'Lava' or base == 'lava' or base == 10:
        # When you see _customBlock_getLOG called in source code, use base='Lava' here
        return math.log(max(input_value, 1)) / 2.30259
    elif input_value <= 0:
        return 0
    else:
        return math.log(input_value, base)

def mark_advice_completed(advice, force=False):
    def complete():
        advice.progression = ""
        advice.goal = "✔"
        advice.completed = True
        advice.status = "gilded"

    if force:
        complete()

    elif not advice.goal and str(advice.progression).endswith("+"):
        advice.completed = True

    elif not advice.goal and str(advice.progression).endswith("%"):
        try:
            if float(str(advice.progression).strip("%")) > 100:
                complete()
        except:
            pass

    elif advice.percent == '100%':
        #If the progress bar is set to 100%
        complete()

    else:
        try:
            prog = str(advice.progression).strip('x%')
            goal = str(advice.goal).strip('x%')
            if advice.goal and advice.progression and float(prog) >= float(goal):
                complete()
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
