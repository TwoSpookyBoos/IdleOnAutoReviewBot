import datetime
import json
import re
import traceback
from pathlib import Path

import requests
import yaml
from babel.dates import format_datetime
from flask import request, g as session_data

from consts.consts_general import cardset_identifiers, cardset_names, getBaseClass, getSubclass, getEliteClass, \
    getMasterClass
from consts.consts_idleon import getAllSkillLevelsDict, getHumanReadableClasses, max_characters
from models.custom_exceptions import ProfileNotFound, APIConnectionFailed, WtfDataException

from utils.logging import get_logger
from config import app
from .safer_data_handling import safe_loads
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
            time_away_dict = safe_loads(session_data.account.raw_data['TimeAway'])
            last_updated_time_epoch = time_away_dict['GlobalTime']
            last_updated_time_utc = datetime.datetime.fromtimestamp(last_updated_time_epoch, datetime.timezone.utc)
            current_time_utc = datetime.datetime.now(datetime.timezone.utc)
            deltaTime = current_time_utc - last_updated_time_utc
            days, rest = divmod(deltaTime.total_seconds(), 24 * 60 * 60)
            hours, rest = divmod(rest, 60 * 60)
            minutes, seconds = divmod(rest, 60)

            locale = request.accept_languages.best.replace("-", "_")
            self.elapsed = f"{days:02g}:{hours:02g}:{minutes:02g}:{int(seconds):02g}"
            self.last_update = format_datetime(last_updated_time_utc, locale=locale) + " UTC"
            self.is_stale = deltaTime.total_seconds() >= 24 * 60 * 60

        except:
            logger.exception('Unable to parse last updated time.')
            self.elapsed = '00:00:00:00'
            self.last_update = 'Unable to parse last updated time, sorry :('


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
    parsed['parsedData'] = rawJSON.get(
        'parsedData',  #Available on Public Toolbox profiles
        rawJSON.get(
            'extraData',  #Available on signed-in Toolbox
            {}  #Otherwise default to empty dict
        )
    )
    if not isinstance(parsed.get("AutoLoot"), int):
        try:
            parsed["AutoLoot"] = int(parsed["AutoLoot"])
        except:
            logger.exception(f"Unexpected datatype found for AutoLoot: {type(parsed.get('AutoLoot'))}: {parsed.get('AutoLoot')}. Setting to 0")
            parsed["AutoLoot"] = 0

    return parsed

def from_toolbox(rawJSON):
    return "data" in rawJSON

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

    current_map_index = {}
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
    big_alch_bubbles = safe_loads(inputJSON.get('CauldronBubbles', [0, 0, 0] * max_characters))
    while len(big_alch_bubbles) < character_count:
        if isinstance(big_alch_bubbles, list):
            big_alch_bubbles.append([0,0,0])
        elif isinstance(big_alch_bubbles, dict):
            big_alch_bubbles[len(big_alch_bubbles)] = [0, 0, 0]
    alchemy_jobs_list = safe_loads(inputJSON.get('CauldronJobs1', [-1] * max_characters))
    equipped_cards_codenames = {}
    equipped_cardset = {}
    equipped_star_signs = {}
    main_stats = {}

    for character_index in range(0, character_count):
        character_classes.append(getHumanReadableClasses(inputJSON.get(f'CharacterClass_{character_index}', 0)))
        current_map_index[character_index] = safe_loads(inputJSON.get(f'CurrentMap_{character_index}', 0))
        postOfficeList.append(safe_loads(inputJSON.get(f'POu_{character_index}', [0] * 36)))
        equipped_prayers[character_index] = safe_loads(inputJSON.get(f'Prayers_{character_index}', []))
        characterMaxTalents[character_index] = safe_loads(inputJSON.get(f'SM_{character_index}', {}))
        characterCurrentPresetTalents[character_index] = safe_loads(inputJSON.get(f'SL_{character_index}', {}))
        characterSecondaryPresetTalents[character_index] = safe_loads(inputJSON.get(f'SLpre_{character_index}', {}))
        inventory_bags[character_index] = safe_loads(inputJSON.get(f'InvBagsUsed_{character_index}', {}))
        kill_lists[character_index] = safe_loads(inputJSON.get(f'KLA_{character_index}', []))
        obols_list[character_index] = safe_loads(inputJSON.get(f'ObolEqO0_{character_index}', []))
        obol_upgrades_list[character_index] = safe_loads(inputJSON.get(f'ObolEqMAP_{character_index}', {}))
        try:
            equipped_lab_chips[character_index] = safe_loads(inputJSON['Lab'])[character_index + 1]
        except:
            equipped_lab_chips[character_index] = []
        current_preset_talent_bar[character_index] = safe_loads(inputJSON.get(f'AttackLoadout_{character_index}', []))
        secondary_preset_talent_bar[character_index] = safe_loads(inputJSON.get(f'AttackLoadoutpre_{character_index}', []))
        equipped_cards_codenames[character_index] = [codename for codename in safe_loads(inputJSON.get(f'CardEquip_{character_index}', [])) if codename != 'B']
        try:
            equipped_cardset_identifier = list(safe_loads(inputJSON.get(f'CSetEq_{character_index}', {})).keys())[0]
            if equipped_cardset_identifier in cardset_identifiers:
                equipped_cardset[character_index] = cardset_names[cardset_identifiers.index(equipped_cardset_identifier)]
            else:
                logger.warning(f'Found unknown cardset "{equipped_cardset_identifier}"')
                equipped_cardset[character_index] = ""
        except IndexError:
            equipped_cardset[character_index] = ""
        equipped_star_signs[character_index] = [int(star_sign_id) for star_sign_id in inputJSON.get(f'PVtStarSign_{character_index}','_,')[:-1].split(',') if star_sign_id not in ['_', '']]
        main_stats_array = safe_loads(inputJSON.get(f'PVStatList_{character_index}', [0, 0, 0, 0]))
        main_stats[character_index] = {'STR': main_stats_array[0], 'AGI': main_stats_array[1], 'WIS': main_stats_array[2], 'LUK': main_stats_array[3]}

        characterDict[character_index] = dict(
            alchemy_job=alchemy_jobs_list[character_index],
            all_skill_levels=characterSkillsDict[character_index],
            base_class=getBaseClass(character_classes[character_index]),
            big_alch_bubbles=big_alch_bubbles[character_index],
            character_index=character_index,
            character_name=character_names[character_index],
            class_name=character_classes[character_index],
            current_map_index=current_map_index[character_index],
            current_preset_talent_bar=current_preset_talent_bar[character_index],
            current_preset_talents=characterCurrentPresetTalents[character_index],
            elite_class=getEliteClass(character_classes[character_index]),
            equipped_lab_chips=equipped_lab_chips[character_index],
            equipped_prayers=equipped_prayers[character_index],
            inventory_bags=inventory_bags[character_index],
            kill_dict={k:v for k, v in enumerate(kill_lists[character_index])},
            master_class=getMasterClass(character_classes[character_index]),
            max_talents=characterMaxTalents[character_index],
            obol_upgrades=obol_upgrades_list[character_index],
            obols=obols_list[character_index],
            po_boxes=postOfficeList[character_index],
            secondary_preset_talent_bar=secondary_preset_talent_bar[character_index],
            secondary_preset_talents=characterSecondaryPresetTalents[character_index],
            sub_class=getSubclass(character_classes[character_index]),
            equipped_cards_codenames=equipped_cards_codenames[character_index],
            equipped_cardset=equipped_cardset[character_index],
            equipped_star_signs=equipped_star_signs[character_index],
            main_stats=main_stats[character_index]
        )

    return [character_count, character_names, character_classes, characterDict, perSkillDict]

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
    # This stuff isn't exactly an item, but it does show up
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
