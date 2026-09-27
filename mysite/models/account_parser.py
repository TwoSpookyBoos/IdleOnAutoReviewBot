import copy
from collections import defaultdict
from math import floor
from flask import g

from consts.consts_autoreview import items_codes_and_names
from consts.idleon.consts_idleon import max_characters
from consts.idleon.lava_func import lava_func
from consts.consts_general import (
    key_cards, cardset_names, card_raw_data, gem_shop_dict, gem_shop_optlacc_dict,
    gem_shop_bundles_dict, achievements_list, allMeritsDict
)
from consts.consts_item_data import ITEM_DATA
from consts.consts_monster_data import decode_monster_name
from consts.consts_w1 import starsigns_dict, event_points_shop_dict
from consts.w1.stamps import stamp_types
from consts.consts_w2 import ballot_dict, killroy_dict
from consts.consts_w3 import refinery_dict, buildings_dict
from consts.consts_w4 import (
    max_cooking_tables, max_meal_count, max_meal_plate_level, cooking_meal_dict, lab_bonuses_dict, lab_jewels_dict,
)
from consts.consts_w5 import (
    sailing_list, captain_buffs,
    sailing_artifacts_dict, artifact_tier_names, sailing_artifacts_description_overrides
)
from models.w1.statues import Statues
from models.general.assets import Assets
from models.general.character import Character
from models.general.cards import Card
from models.w1.stamps import Stamp
from utils.data_formatting import getCharacterDetails
from utils.safer_data_handling import safe_loads, safer_get, safer_convert, safer_index
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.text_formatting import numberToLetter, kebab, letterToNumber

logger = get_logger(__name__)


def _make_cards(account):
    card_counts = safe_loads(account.raw_data.get(key_cards, {}))

    #Parse card data from source code
    parsed_card_data = {}
    unknown_cards = []
    for cardset_index, cardset_details in enumerate(card_raw_data):
        try:
            cardset_name = cardset_names[cardset_index]
        except:
            logger.warning(f"No name found for Card Set Index {cardset_index}!")
            cardset_name = f"UnknownSet-{cardset_index}"
        for card_info in cardset_details:
            if card_info[0] == 'Blank':
                continue  #Skip the blank placeholders
            # ["mushG", "A0", "5", "+{_Base_HP", "12"],
            enemy_decoded_name = decode_monster_name(card_info[0], card=True)
            if enemy_decoded_name.startswith('Unknown'):
                unknown_cards.append(card_info)
            parsed_card_data[enemy_decoded_name] = {
                'Card Name': card_info[0],
                'Enemy Name': enemy_decoded_name,
                'Cards For 1star': parse_number(card_info[2], 1.0),
                'Description': card_info[3].replace('_', ' '),
                'Value per Level': parse_number(card_info[4], 0.0),
                'Set Name': cardset_name
            }

    if unknown_cards:
        logger.error(f"Unknown Card name(s) found: {unknown_cards}")

    # "OptionsListAccount"[603]/[155] in source: card level floors.
    # Last updated in v2.531.0
    min_7_cards = set(f"{safer_get(account.raw_optlacc_dict, 603, '')}".split(','))
    min_6_cards = set(f"{safer_get(account.raw_optlacc_dict, 155, '')}".split(','))
    cards = [
        Card(
            codename=card_values['Card Name'],
            name=decoded_enemy_name,
            cardset=card_values['Set Name'],
            count=safer_get(card_counts, card_values['Card Name'], 0),
            coefficient=card_values['Cards For 1star'],
            value_per_level=card_values['Value per Level'],
            description=card_values['Description'],
            min_level=(
                7 if card_values['Card Name'] in min_7_cards
                else 6 if card_values['Card Name'] in min_6_cards
                else 0
            ),
        ) for decoded_enemy_name, card_values in parsed_card_data.items()
    ]

    for character in g.account.all_characters:
        for equipped_card_codename in character.equipped_cards_codenames:
            try:
                equipped_card = next(card for card in cards if card.codename == equipped_card_codename)
                character.equipped_cards.append(equipped_card)
            except:
                logger.warning(f"Unknown equipped_card_codename: {equipped_card_codename}. Skipping")
    # cards = [
    #     Card(codename, name, cardset, safer_get(card_counts, codename, 0), coefficient)
    #     for cardset, cards in card_data.items()
    #     for codename, (name, coefficient) in cards.items()
    # ]

    # unknown_cards = [
    #     codename for codename in card_counts if not any(codename in items for items in card_data.values())
    # ]

    return cards


def _all_stored_items(account) -> Assets:
    chest_keys = (("ChestOrder", "ChestQuantity"),)
    name_quantity_key_pairs = chest_keys + tuple(
        (f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in account.safe_character_indexes
    )
    all_stuff_stored_or_in_inv = dict.fromkeys(items_codes_and_names.keys(), 0)

    for name_key, quantity_key in name_quantity_key_pairs:
        pair_item_name_to_quantity = zip(account.raw_data.get(name_key, list()), account.raw_data.get(quantity_key, list()))
        for name, count in pair_item_name_to_quantity:
            if name not in all_stuff_stored_or_in_inv:
                all_stuff_stored_or_in_inv[name] = safer_convert(count, 0)
            else:
                all_stuff_stored_or_in_inv[name] += safer_convert(count, 0)

    return Assets(all_stuff_stored_or_in_inv)


def _all_worn_items(account) -> Assets:
    stuff_worn = defaultdict(int)
    for toon in account.safe_characters:
        for item in [*toon.equipment.foods, *toon.equipment.equips, *toon.equipment.tools]:
            if item.codename == 'Blank':
                continue
            stuff_worn[item.codename] += item.amount

    return Assets(stuff_worn)

def parse_account(account, run_type):
    _parse_wave_1(account, run_type)

def _parse_wave_1(account, run_type):
    _parse_switches(account)
    _parse_characters(account, run_type)
    _parse_general(account)
    _parse_master_classes(account)
    _parse_w1(account)
    _parse_w2(account)
    _parse_w3(account)
    _parse_w4(account)
    _parse_w5(account)

def _parse_switches(account):
    # AutoLoot
    if g.autoloot:
        account.autoloot = True
    elif account.raw_data.get("AutoLoot", 0) == 1 or safe_loads(account.raw_data.get('BundlesReceived', {})).get('bun_i', 0) == 1:
        account.autoloot = True
        g.autoloot = True
    else:
        account.autoloot = False

    # Shows the switch on when the save has it, like Autoloot
    if account.vault.potluck_pack_owned:
        g.potluck_pack = True

    account.max_subgroups = 3
    account.library_group_characters = g.library_group_characters
    account.tabbed_advice_groups = g.tabbed_advice_groups
    account.manual_tome_score = g.get("tome_score") if g.manual_tome else None

def _parse_characters(account, run_type):
    character_count, character_names, character_classes, characterDict, perSkillDict = getCharacterDetails(
        account.raw_data, run_type
    )
    account.names = character_names
    account.character_count = character_count
    account.all_characters = [Character(account.raw_data, **char) for char in characterDict.values()]
    account.classes = set()
    for char in account.all_characters:
        for className in char.all_classes:
            if className != 'None':
                account.classes.add(className)
    account.safe_characters = [char for char in account.all_characters if char]  # Use this if touching raw_data instead of all_characters
    account.safe_character_indexes = [char.character_index for char in account.all_characters if char]
    account.all_skills = perSkillDict
    account.all_quests = [safe_loads(account.raw_data.get(f"QuestComplete_{i}", {})) for i in range(account.character_count)]
    account.max_toon_count = max(max_characters, character_count)  # OPTIMIZE: find a way to read this from somewhere

    _parse_character_class_lists(account)

def _parse_character_class_lists(account):
    account.beginners = [toon for toon in account.all_characters if 'Beginner' in toon.all_classes or 'Journeyman' in toon.all_classes]
    account.jmans = [toon for toon in account.all_characters if 'Journeyman' in toon.all_classes]
    account.maestros = [toon for toon in account.all_characters if 'Maestro' in toon.all_classes]
    account.vmans = [toon for toon in account.all_characters if 'Voidwalker' in toon.all_classes]
    account.no_beginners = len(account.beginners) == 0 and account.character_count >= account.max_toon_count

    account.barbs = [toon for toon in account.all_characters if 'Barbarian' in toon.all_classes]
    account.bbs = [toon for toon in account.all_characters if 'Blood Berserker' in toon.all_classes]
    account.dbs = [toon for toon in account.all_characters if 'Death Bringer' in toon.all_classes]
    account.dks = [toon for toon in account.all_characters if 'Divine Knight' in toon.all_classes]

    account.mages = [toon for toon in account.all_characters if 'Mage' in toon.all_classes]
    account.bubos = [toon for toon in account.all_characters if 'Bubonic Conjuror' in toon.all_classes]
    account.sorcs = [toon for toon in account.all_characters if 'Elemental Sorcerer' in toon.all_classes]
    account.acs = [toon for toon in account.all_characters if 'Arcane Cultist' in toon.all_classes]

    account.wws = [toon for toon in account.all_characters if 'Wind Walker' in toon.all_classes]
    account.sbs = [toon for toon in account.all_characters if 'Siege Breaker' in toon.all_classes]

def _parse_general(account):
    # General / Multiple uses
    account.raw_optlacc_dict = {k: v for k, v in enumerate(safe_loads(account.raw_data.get("OptLacc", [])))}
    # Toolbox provides serverVars,Efficiency provides servervars, otherwise return an empty dict if neither present
    account.raw_serverVars_dict = safe_loads(account.raw_data.get("serverVars", account.raw_data.get("servervars", {})))

    account.stored_assets = _all_stored_items(account)
    account.worn_assets = _all_worn_items(account)
    account.all_assets = account.stored_assets + account.worn_assets

    account.cards = _make_cards(account)

    account.minigame_plays_remaining = safer_get(account.raw_optlacc_dict, 33, 0)
    account.daily_world_boss_kills = safer_get(account.raw_optlacc_dict, 195, 0)
    account.daily_particle_clicks_remaining = safer_get(account.raw_optlacc_dict, 135, 0)

    _parse_general_gem_shop(account)
    _parse_general_gem_shop_optlacc(account)
    _parse_general_gem_shop_bundles(account)
    account.family_bonuses.calculate_levels(account.safe_characters)
    _parse_general_achievements(account)
    _parse_general_merits(account)
    _parse_general_item_filter(account)
    _parse_general_event_points_shop(account)
    _parse_general_quests(account)
    _parse_general_inventory_slots_account_wide(account)

def _parse_general_gem_shop(account):
    raw_gem_items_purchased = safe_loads(account.raw_data.get('GemItemsPurchased', []))
    for purchase_name, details in gem_shop_dict.items():
        try:
            purchased_amount = safer_convert(raw_gem_items_purchased[details['Index']], 0)
        except Exception as e:
            logger.warning(f"Gemshop Parse error with details {details}: {e}. Defaulting to 0")
            purchased_amount = 0
        account.gemshop['Purchases'][purchase_name] = {
            'Owned': purchased_amount,
            'ItemCodename': details['ItemCodename'],
            'Description': details['Description'],
            'Index': details['Index'],
            'MaxLevel': details['MaxLevel'],
            'BaseGemCost': details['BaseGemCost'],
            'IncrementGemCost': details['IncrementGemCost'],
            'Section': details['Section'],
            'Subsection': details['Subsection'],
        }
    raw_caverns_list: list[int] = safe_loads(account.raw_data.get('Holes', []))
    parallel_villagers = safer_index(raw_caverns_list, 23, [0] * 10)
    for villager in account.caverns.villagers.values():
        account.gemshop["Purchases"][f"Parallel Villagers {villager.role}"] = {
            'Owned': parallel_villagers[villager.index],
            'MaxLevel': 1,
            'ItemCodename': 'GemP40',
            'Section': 'Oddities',
            'Subsection': 'Caverns'
        }
    account.minigame_plays_daily = 5 + (4 * account.gemshop['Purchases']['Daily Minigame Plays']['Owned'])

def _parse_general_gem_shop_optlacc(account):
    for purchase_name, details in gem_shop_optlacc_dict.items():
        try:
            purchased_amount = safer_convert(safer_get(account.raw_optlacc_dict, details['Index'], 0), 0)
        except:
            purchased_amount = 0
            if max(account.raw_optlacc_dict.keys()) < details['Index']:
                logger.info(f"Error parsing {purchase_name} because optlacc_index {details['Index']} not present in JSON. Defaulting to 0")
            else:
                logger.exception(f"Error parsing {purchase_name} at optlacc_index {details['Index']}: Could not convert {account.raw_optlacc_dict.get(details['Index'])} to int")
        account.gemshop['Purchases'][purchase_name] = {
            'Owned': purchased_amount,
            'ItemCodename': '',
            'Description': details['Description'],
            'Index': details['Index'],
            'MaxLevel': details['MaxLevel'],
            'BaseGemCost': details['BaseGemCost'],
            'IncrementGemCost': details['IncrementGemCost'],
            'Section': details['Section'],
            'Subsection': details['Subsection'],
        }

def _parse_general_gem_shop_bundles(account):
    raw_gem_shop_bundles = safe_loads(account.raw_data.get('BundlesReceived', []))
    account.gemshop['Bundle Data Present'] = 'BundlesReceived' in account.raw_data
    for code_name, display_name in gem_shop_bundles_dict.items():
        account.gemshop['Bundles'][code_name] = {
            'Display': display_name,
            'Owned': code_name in raw_gem_shop_bundles
        }
    #logger.debug(f"{account.gemshop['Bundles'] = }")
    unknown_bundles = [v for v in account.gemshop['Bundles'] if v not in gem_shop_bundles_dict]
    if unknown_bundles:
        logger.warning(f"Unknown Gem Shop Bundles found: {unknown_bundles}")

def _parse_general_quests(account):
    account.compiled_quests = {}
    for charIndex, questsDict in enumerate(account.all_quests):
        for questName, questStatus in questsDict.items():
            if questName not in account.compiled_quests:
                account.compiled_quests[questName] = {
                    'CompletedCount': 0,
                    'CompletedChars': [],
                    'AcceptedCount': 0,
                    'AcceptedChars': [],
                    'UnacceptedCount': 0,
                    'UnacceptedChars': []
                }
            if questStatus == 1:
                status = 'Completed'
            elif questStatus == 0:
                status = 'Accepted'
            else:  # Won't be reliable. If they haven't interacted with the NPC, their quest may not appear here at all.
                status = 'Unaccepted'
            account.compiled_quests[questName][f'{status}Count'] += 1
            account.compiled_quests[questName][f'{status}Chars'].append(charIndex)

def _parse_general_achievements(account):
    account.achievements = {}
    raw_reg_achieves = safe_loads(account.raw_data.get('AchieveReg', []))
    if len(raw_reg_achieves) < len(achievements_list):
        logger.warning(f"Achievements list shorter than expected by {len(achievements_list) - len(raw_reg_achieves)}. "
                       f"Likely old data. Defaulting them all to Incomplete.")
        while len(raw_reg_achieves) < len(achievements_list):
            raw_reg_achieves.append(0)

    for achieveIndex, achieveData in enumerate(achievements_list):
        ach_name = achieveData[0].replace('_', ' ')
        try:
            if ach_name != "FILLERZZZ ACH":
                account.achievements[ach_name] = {
                    'Complete': raw_reg_achieves[achieveIndex] == -1,
                    'Raw': raw_reg_achieves[achieveIndex]
                }
        except Exception as e:
            logger.warning(f"Achievements Parse error for {ach_name} at Index {achieveIndex}: {e}. Defaulting to Incomplete")
            account.achievements[ach_name] = {
                'Complete': False,
                'Raw': 0
            }

def _parse_general_merits(account):
    account.merits = copy.deepcopy(allMeritsDict)
    raw_merits_list = safe_loads(account.raw_data.get("TaskZZ2", []))
    for worldIndex in account.merits:
        for meritIndex in account.merits[worldIndex]:
            try:
                account.merits[worldIndex][meritIndex]["Level"] = safer_convert(raw_merits_list[worldIndex][meritIndex], 0)
            except Exception as e:
                logger.warning(f"Merit Parse error: {e}. Defaulting to 0")
                continue  # Already defaulted to 0 in Consts

def _parse_general_item_filter(account):
    account.item_filter = []
    raw_printer_xtra = safe_loads(account.raw_data.get('PrinterXtra', []))
    if len(raw_printer_xtra) >= 121:
        for codeName in raw_printer_xtra[120:]:
            if codeName != 'Blank':
                account.item_filter.append(codeName)

def _parse_general_event_points_shop(account):
    account.event_points_shop = {
        'Points Owned': safer_get(account.raw_optlacc_dict, 310, 0),
        'Raw Purchases': safer_get(account.raw_optlacc_dict, 311, ''),
        'Bonuses': {}
    }
    if isinstance(account.event_points_shop['Raw Purchases'], str):
        account.event_points_shop['Raw Purchases'] = list(account.event_points_shop['Raw Purchases'])
    else:
        logger.warning(f"Event Shop Purchases not String type: {type(account.event_points_shop['Raw Purchases'])} with value of: {account.event_points_shop['Raw Purchases']}")
        account.event_points_shop['Raw Purchases'] = []
    for bonusName, bonusDetails in event_points_shop_dict.items():
        try:
            account.event_points_shop['Bonuses'][bonusName] = {
                'Owned': bonusDetails['Code'] in account.event_points_shop['Raw Purchases'],
                'Cost': bonusDetails['Cost'],
                'Description': bonusDetails['Description'],
                'Image': bonusDetails['Image']
            }
        except Exception as e:
            logger.warning(f"Event Shop Parse error: {e}. Defaulting to Unowned")
            account.event_points_shop['Bonuses'][bonusName] = {
                'Owned': False,
                'Cost': bonusDetails['Cost'],
                'Description': bonusDetails['Description'],
                'Image': bonusDetails['Image']
            }

def _parse_general_inventory_slots_account_wide(account):
    account.inventory.calculate_owned(
        account.all_characters,
        account.autoloot,
        account.event_points_shop['Bonuses']['Secret Pouch']['Owned'],
        account.gemshop['Bundles']['bon_f']['Owned'],
    )

def _parse_master_classes(account):
    # Grimoire, Compass, and Tesseract/Arcane Cultist are now self-parsing; see Grimoire(account.raw_data),
    # Compass(account.raw_data), and Tesseract(account.raw_data) in Account.__init__
    pass

def _parse_master_classes_exalted_stamps(account):
    raw_compass = safe_loads(account.raw_data.get('Compass', []))
    if not raw_compass:
        logger.warning(f"Exalted Stamp data not present{', as expected' if account.version < 264 else ''}.")
    while len(raw_compass) < 5:
        raw_compass.append([])
    raw_stamps_exalted = raw_compass[4]

    for stamp in ITEM_DATA.get_all_stamps():
        stamp_codename = stamp.code_name.split('Stamp')[1]
        stamp_type_code = numberToLetter(letterToNumber(stamp_codename[0].lower()) - 1)
        stamp_code = int(''.join(stamp_codename[1:])) - 1
        try:
            exalted_stamp_key = f"{stamp_type_code}{stamp_code}"
            # if exalted_stamp_key in raw_stamps_exalted:
            #     logger.debug(f"{stampType}{stampIndex} ({exalted_stamp_key}): {stampValuesDict['Name']} is Exalted")
            account.stamps[stamp.name].exalted = exalted_stamp_key in raw_stamps_exalted
        except:
            if raw_compass:
                logger.exception(f"Error parsing Exalted status for stamp {stamp_type_code}{stamp_code}: {stamp.name}")
            account.stamps[stamp.name].exalted = False


def _parse_w1(account):
    _parse_w1_starsigns(account)
    _parse_w1_stamps(account)
    account.statues = Statues(account.raw_data, account.safe_characters)

def _parse_w1_starsigns(account):
    account.star_signs = {}
    account.star_sign_extras = {}
    raw_star_signs = safe_loads(account.raw_data.get('StarSg', {}))
    for signIndex, signValuesDict in starsigns_dict.items():
        try:
            account.star_signs[signValuesDict['Name']] = {
                'Index': signIndex,
                'Passive': signValuesDict['Passive'],
                'Unlocked': parse_number(safer_get(raw_star_signs, signValuesDict['Name'].replace(' ', '_'), 0)) > 0
                # Some StarSigns are saved as strings "1", some are int 1 to mean unlocked.
                # 'Bonus1': signValuesDict.get('Bonus1', 0),
                # 'Bonus2': signValuesDict.get('Bonus2', 0),
                # 'Bonus3': signValuesDict.get('Bonus3', 0),
            }
        except Exception as e:
            logger.warning(f"Star Sign Parse error at signIndex {signIndex}: {e}. Defaulting to Locked")
            account.star_signs[signValuesDict['Name']] = {
                'Index': signIndex,
                'Passive': signValuesDict['Passive'],
                'Unlocked': False,
                # 'Bonus1': signValuesDict.get('Bonus1', 0),
                # 'Bonus2': signValuesDict.get('Bonus2', 0),
                # 'Bonus3': signValuesDict.get('Bonus3', 0),
            }

    account.star_sign_extras['UnlockedSigns'] = sum(account.star_signs[name]['Unlocked'] for name in account.star_signs)

def _parse_w1_stamps(account):
    raw_stamps_list = safe_loads(account.raw_data.get("StampLv", [{}, {}, {}]))
    raw_stamps_dict = {}
    for stamp_type_index, stamp_type_stamps in enumerate(raw_stamps_list):
        for stamp_key, stamp_level in stamp_type_stamps.items():
            if stamp_key != "length":
                stamp_code = f"Stamp{numberToLetter(stamp_type_index + 1).upper()}{int(stamp_key) + 1}"
                raw_stamps_dict[stamp_code] = int(stamp_level)
    raw_stamp_max_list = safe_loads(account.raw_data.get("StampLvM", {0: {}, 1: {}, 2: {}}))
    raw_stamp_max_dict = {}
    for stamp_type_index, stamp_type_stamps in enumerate(raw_stamp_max_list):
        for stamp_key, stamp_level in stamp_type_stamps.items():
            if stamp_key != "length":
                stamp_code = f"Stamp{numberToLetter(stamp_type_index + 1).upper()}{int(stamp_key) + 1}"
                try:
                    raw_stamp_max_dict[stamp_code] = int(stamp_level)
                except:
                    logger.exception(f"Unexpected stamp_type_index {stamp_type_index} or stamp_key {stamp_key} or stamp_level: {stamp_level}")
                    try:
                        raw_stamp_max_dict[stamp_code] = 0
                        logger.debug(f"Able to set the value of stamp {stamp_type_index}-{stamp_key} to 0. Hopefully no accuracy was lost.")
                    except:
                        logger.exception(f"Couldn't set the value to 0, meaning it was the Index or Key that was bad. You done messed up, cowboy.")
    all_stamps = ITEM_DATA.get_all_stamps()
    for stamp_definition in all_stamps:
        stamp_type = stamp_types[letterToNumber(stamp_definition.code_name.split('Stamp')[1][0].lower()) - 1]
        try:
            stamp_level = safer_convert(raw_stamps_dict.get(stamp_definition.code_name, 0), 0)
            account.stamps[stamp_definition.name] = Stamp(
                name=stamp_definition.name,
                code_name=stamp_definition.code_name,
                material=ITEM_DATA.get_item_from_codename(stamp_definition.stamp_bonus.code_material),
                effect=stamp_definition.stamp_bonus.effect,
                level=stamp_level,
                max_level=safer_convert(raw_stamp_max_dict.get(stamp_definition.code_name, 0), 0),
                delivered=safer_convert(raw_stamp_max_dict.get(stamp_definition.code_name, 0), 0) > 0,
                stamp_type=stamp_type,
                value=lava_func(
                    stamp_definition.stamp_bonus.scaling_type,
                    stamp_level,
                    stamp_definition.stamp_bonus.x1,
                    stamp_definition.stamp_bonus.x2,
                ),
                exalted=False
            )
            account.stamp_totals['Total'] += account.stamps[stamp_definition.name].level
            account.stamp_totals[stamp_type] += account.stamps[stamp_definition.name].level
        except Exception as e:
            logger.warning(f"Stamp Parse error at {stamp_type}: {e}. Defaulting to Undelivered")
            account.stamps[stamp_definition.name] = Stamp(
                name=stamp_definition.name,
                code_name=stamp_definition.code_name,
                level=0,
                max_level=0,
                delivered=False,
                stamp_type=stamp_type,
                value=0,
                exalted=False,
                material=None,
                effect=""
            )
    _parse_master_classes_exalted_stamps(account)

def _parse_w2(account):
    _parse_w2_ballot(account)
    _parse_w2_killroy(account)
    _parse_w2_weekly_boss(account)


def _parse_w2_ballot(account):
    raw_vote_categories = safer_get(account.raw_serverVars_dict, 'voteCategories', [0,0,0,0])
    raw_vote_categories = [safer_convert(v, 0) for v in raw_vote_categories]  #Convert any None to 0 as a default
    account.ballot = {
        "CurrentBuff": raw_vote_categories[0],
        "OnTheBallot": raw_vote_categories[1:],
        "Week": safer_get(account.raw_optlacc_dict, 309, 0),
        "Buffs": {}
    }
    for buffIndex, buffValuesDict in ballot_dict.items():
        account.ballot['Buffs'][buffIndex] = {
            'Description': buffValuesDict['Description'],
            'BaseValue': buffValuesDict['BaseValue'],
            'Value': buffValuesDict['BaseValue'],
            'Image': buffValuesDict['Image'],
        }

def _parse_w2_killroy(account):
    _parse_w2_killroy_skull_shop(account)
    account.killroy = {}
    account.killroy_total_fights = safer_get(account.raw_optlacc_dict, 112, 0)
    for upgradeName, upgradeDict in killroy_dict.items():
        account.killroy[upgradeName] = {
            'Available': False,
            'Remaining': max(0, upgradeDict['Required Fights'] - account.killroy_total_fights),
            'Upgrades': safer_get(account.raw_optlacc_dict, upgradeDict['UpgradesIndex'], 0),
            'Image': upgradeDict['Image']
        }

def _parse_w2_killroy_skull_shop(account):
    account.killroy_skullshop = {
        'Third Battle Unlocked': safer_get(account.raw_optlacc_dict, 227, 0) == 1,
        'Artifact Purchases': safer_get(account.raw_optlacc_dict, 228, 0),
        'Artifact Multi': 1 + (safer_get(account.raw_optlacc_dict, 228, 0) / (300 + safer_get(account.raw_optlacc_dict, 228, 0))),
        'Crop Purchases': safer_get(account.raw_optlacc_dict, 229, 0),
        'Crop Multi': 1 + ((safer_get(account.raw_optlacc_dict, 229, 0) / (300 + safer_get(account.raw_optlacc_dict, 229, 0))) * 9),
        'Crop Multi Plus 1': 1 + (((1 + safer_get(account.raw_optlacc_dict, 229, 0)) / (1 + 300 + safer_get(account.raw_optlacc_dict, 229, 0))) * 9),
        'Jade Purchases': safer_get(account.raw_optlacc_dict, 230, 0),
        'Jade Multi': 1 + ((safer_get(account.raw_optlacc_dict, 230, 0) / (300 + safer_get(account.raw_optlacc_dict, 230, 0))) * 2),
    }

def _parse_w2_weekly_boss(account):
    account.weekly_boss_kills = safer_get(account.raw_optlacc_dict, 189, 0)


def _parse_w3(account):
    _parse_w3_refinery(account)
    _parse_w3_buildings(account)
    _parse_w3_deathnote(account)
    _parse_w3_equinox(account)

def _parse_w3_refinery(account):
    account.refinery = {}
    raw_refinery_list = safe_loads(account.raw_data.get("Refinery", []))
    for saltColor, saltDetails in refinery_dict.items():
        try:
            account.refinery[saltColor] = {
                'Rank': parse_number(raw_refinery_list[saltDetails[0]][1]),
                'Running': parse_number(raw_refinery_list[saltDetails[0]][3]),
                'AutoRefine': parse_number(raw_refinery_list[saltDetails[0]][4]),
                'Image': saltDetails[1],
                'CyclesPerSynthCycle': saltDetails[2],
                'PreviousSaltConsumption': saltDetails[3],
                'NextSaltConsumption': saltDetails[4],
                'NextSaltCyclesPerSynthCycle': saltDetails[5]
            }
        except:
            account.refinery[saltColor] = {
                'Rank': 0,
                'Running': False,
                'AutoRefine': 0,
                'Image': saltDetails[1],
                'CyclesPerSynthCycle': saltDetails[2],
                'PreviousSaltConsumption': saltDetails[3],
                'NextSaltConsumption': saltDetails[4],
                'NextSaltCyclesPerSynthCycle': saltDetails[5]
            }

def _parse_w3_buildings(account):
    account.construction_buildings = {}
    raw_buildings_list = safe_loads(account.raw_data.get("Tower", []))
    for buildingIndex, buildingValuesDict in buildings_dict.items():
        try:
            account.construction_buildings[buildingValuesDict['Name']] = {
                'Level': int(raw_buildings_list[buildingIndex]),
                'MaxLevel': buildingValuesDict['BaseMaxLevel'],
                'Image': buildingValuesDict['Image'],
                'Type': buildingValuesDict['Type'],
            }
        except:
            account.construction_buildings[buildingValuesDict['Name']] = {
                'Level': 0,
                'MaxLevel': buildingValuesDict['BaseMaxLevel'],
                'Image': buildingValuesDict['Image'],
                'Type': buildingValuesDict['Type'],
            }

def _parse_w3_deathnote(account):
    # Dependency: _parse_character_class_lists
    account.death_note.calculate_apocalypse_characters(account.barbs, account.bbs)
    account.death_note.calculate_kills(account.all_characters)
    account.death_note.calculate_rift_meowed(account.all_characters)

def _parse_w3_equinox(account):
    account.equinox.calculate_unlocked(account.achievements, account.research.grid['Equinox Nightmares'].level)

def _parse_w4(account):
    _parse_w4_cooking(account)
    _parse_w4_lab(account)
    _parse_w4_rift(account)
    _parse_w4_breeding(account)

def _parse_w4_cooking(account):
    _parse_w4_cooking_tables(account)
    _parse_w4_cooking_meals(account)
    _parse_w4_cooking_ribbons(account)

def _parse_w4_cooking_tables(account):
    emptyTable = [0] * 11  # Some tables only have 10 fields, others have 11. Scary.
    emptyCooking = [emptyTable for table in range(max_cooking_tables)]
    raw_cooking_list = safe_loads(account.raw_data.get("Cooking", emptyCooking))
    for sublistIndex, value in enumerate(raw_cooking_list):
        if isinstance(raw_cooking_list[sublistIndex], list):
            # Pads out the length of all tables to 11 entries, to be safe.
            while len(raw_cooking_list[sublistIndex]) < 11:
                raw_cooking_list[sublistIndex].append(0)
    account.cooking['Tables'] = raw_cooking_list
    account.cooking['Tables Owned'] = sum(1 for table in account.cooking['Tables'] if table[0] == 2)

def _parse_w4_cooking_meals(account):
    emptyMeal = [0] * max_meal_count
    # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
    emptyMeals = [emptyMeal for meal in range(4)]
    raw_meals_list = safe_loads(account.raw_data.get('Meals', emptyMeals))
    if len(raw_meals_list[0]) < max_meal_count:
        logger.warning(f"Data's meal levels list shorter than expected: {len(raw_meals_list[0])} < {max_meal_count}")
        while len(raw_meals_list[0]) < max_meal_count:
            raw_meals_list[0].append(0)

    # CookMaster[0] in source: meal mastery. Last updated in v2.531.0
    raw_cook_master = safe_loads(account.raw_data.get('CookMaster', []))
    raw_mastery_list = safer_index(raw_cook_master, 0, [])

    # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
    for index, details in cooking_meal_dict.items():
        account.meals[details['Name']] = {
            'Level': parse_number(raw_meals_list[0][index], 0),
            'Mastery': parse_number(safer_index(raw_mastery_list, index, 0), 0),
            'Value': parse_number(raw_meals_list[0][index], 0) * details['BaseValue'],  # Mealmulti applied in calculate section
            'BaseValue': details['BaseValue'],
            'Effect': details['Effect'],
            'Index': index,
            'Image': details['Image'],
            'World': details['World']
        }

    account.cooking['PlayerTotalMealLevels'] = sum([details['Level'] for details in account.meals.values()])
    account.cooking['MealsUnlocked'] = sum([details['Level'] > 0 for details in account.meals.values()])
    for meal in account.meals.values():
        account.cooking['MealsUnlockedByWorld'][meal['World']] += meal['Level'] > 0
    account.cooking['UnlockedMealsUnder11'] = sum([0 < details['Level'] < 11 for details in account.meals.values()])
    account.cooking['UnlockedMealsUnder30'] = sum([0 < details['Level'] < 30 for details in account.meals.values()])
    account.cooking['MealsUnder11'] = sum([details['Level'] < 11 for details in account.meals.values()])
    account.cooking['MealsUnder30'] = sum([details['Level'] < 30 for details in account.meals.values()])


def _parse_w4_cooking_ribbons(account):
    raw_ribbons = safe_loads(account.raw_data.get('Ribbon', []))
    if not raw_ribbons:
        logger.warning(f"Meal Ribbons data not present{', as expected' if account.version < 236 else ''}")
    for meal_name, meal_values in account.meals.items():
        try:
            account.meals[meal_name]['RibbonTier'] = safer_convert(raw_ribbons[meal_values['Index']+28], 0)  #Ribbon shelf occupies first 28 indexes
        except:
            account.meals[meal_name]['RibbonTier'] = 0
            if raw_ribbons:
                logger.exception(f"Could not retrieve Ribbon for {meal_name}")

def _parse_w4_lab(account):
    raw_lab = safe_loads(account.raw_data.get("Lab", []))
    _parse_w4_lab_bonuses(account, raw_lab)
    _parse_w4_jewels(account, raw_lab)

def _parse_w4_lab_bonuses(account, raw_lab):
    # TODO: Actually figure out lab :(
    account.labBonuses = {}
    for index, node in lab_bonuses_dict.items():
        account.labBonuses[node["Name"]] = {
            "Enabled": True,
            "Owned": True,  # For W6 nodes
            "Value": node["BaseValue"],  # Currently no modifiers available, might change if the pure opal navette changes
            "BaseValue": node["BaseValue"]
        }

def _parse_w4_jewels(account, raw_lab):
    # TODO: Account for if the jewel is actually connected.

    account.labJewels = {}
    for jewelIndex, jewelInfo in lab_jewels_dict.items():
        try:
            account.labJewels[jewelInfo["Name"]] = {
                "Owned": bool(raw_lab[14][jewelIndex]),
                "Enabled": bool(raw_lab[14][jewelIndex]),  # Same as owned until connection range is implemented
                "Value": jewelInfo["BaseValue"],  # Jewelmulti added in calculate section
                "BaseValue": jewelInfo["BaseValue"]
            }
        except:
            account.labJewels[jewelInfo["Name"]] = {
                "Owned": False,
                "Enabled": False,  # Same as owned until connection range is implemented
                "Value": jewelInfo["BaseValue"],  # Jewelmulti added in calculate section
                "BaseValue": jewelInfo["BaseValue"]
            }

def _parse_w4_rift(account):
    # Seam: hands the model the already-parsed quest data it needs
    account.rift.calculate_unlocked(account.all_quests)

def _parse_w4_breeding(account):
    # Seam: egg slots need gem shop and merits
    account.breeding.calculate_egg_slots(
        account.gemshop['Purchases']['Royal Egg Cap']['Owned'],
        account.merits[3][2]['Level'],
    )

def _parse_w5(account):
    _parse_w5_slab(account)
    _parse_w5_sailing(account)
    _parse_w5_divinity(account)

def _parse_w5_slab(account):
    account.registered_slab = set(safe_loads(account.raw_data.get("Cards1", [])))

def _parse_w5_sailing(account):
    account.sailing = {"Artifacts": {}, "Boats": {}, "Captains": {}, "Islands": {}, 'Islands Discovered': 1, 'CaptainsOwned': 1, 'BoatsOwned': 1}
    raw_sailing_list = safe_loads(safe_loads(account.raw_data.get("Sailing", [])))  # Some users have needed to have data converted twice
    if not raw_sailing_list:
        logger.warning(f"Sailing data not present")
    try:
        account.sailing['CaptainsOwned'] += raw_sailing_list[2][0]
        account.sailing['BoatsOwned'] += raw_sailing_list[2][1]
        account.sum_artifact_tiers = sum(raw_sailing_list[3])
    except:
        account.sum_artifact_tiers = 0
    #Islands
    for island_index, island_values_dict in enumerate(sailing_list):
        try:
            account.sailing['Islands'][island_values_dict['Name']] = {
                'Unlocked': raw_sailing_list[0][island_index] == -1,
                'Distance': island_values_dict['Distance'],
                'NormalTreasure': island_values_dict['NormalTreasure'],
                'RareTreasure': island_values_dict['RareTreasure']
            }
        except:
            account.sailing['Islands'][island_values_dict['Name']] = {
                'Unlocked': False,
                'Distance': island_values_dict['Distance'],
                'NormalTreasure': island_values_dict['NormalTreasure'],
                'RareTreasure': island_values_dict['RareTreasure']
            }
    account.sailing['Islands Discovered'] = sum([details['Unlocked'] for details in account.sailing['Islands'].values()])
    #Artifacts
    for artifact_index, artifact_values_dict in sailing_artifacts_dict.items():
        try:
            artifact_level = parse_number(raw_sailing_list[3][artifact_index], 0)
        except:
            artifact_level = 0
        description = sailing_artifacts_description_overrides.get(artifact_values_dict['Name'], {}).get(artifact_level, artifact_values_dict['Description'])
        account.sailing['Artifacts'][artifact_values_dict['Name']] = {
            'Level': artifact_level,
            'Description': description,
            'FormBonuses': {index: description for index, description in enumerate(artifact_values_dict['FormBonuses'])},
            'FormBonus': artifact_values_dict['FormBonuses'].get(artifact_level, 'Unknown Bonus'),
            'Form': artifact_tier_names.get(artifact_level),
            'Values': {index: value for index, value in enumerate(artifact_values_dict['Values'])},
            'Island': artifact_values_dict['Island'],
            'Image': kebab(artifact_values_dict['Name'])
        }

    _parse_w5_sailing_boats(account)
    _parse_w5_sailing_captains(account)

def _parse_w5_sailing_boats(account):
    raw_sailing_boats = safe_loads(safe_loads(account.raw_data.get("Boats", [])))  # Some users have needed to have data converted twice
    for boatIndex, boatDetails in enumerate(raw_sailing_boats):
        try:
            account.sailing['Boats'][boatIndex] = {
                'Captain': boatDetails[0],
                'Destination': boatDetails[1],
                'LootUpgrades': boatDetails[3],
                'SpeedUpgrades': boatDetails[5],
                'TotalUpgrades': boatDetails[3] + boatDetails[5]
            }
        except:
            account.sailing['Boats'][boatIndex] = {
                'Captain': -1,
                'Destination': -1,
                'LootUpgrades': 0,
                'SpeedUpgrades': 0,
                'TotalUpgrades': 0
            }

def _parse_w5_sailing_captains(account):
    raw_sailing_captains = safe_loads(safe_loads(account.raw_data.get("Captains", [])))  # Some users have needed to have data converted twice
    for captainIndex, captainDetails in enumerate(raw_sailing_captains):
        try:
            account.sailing['Captains'][captainIndex] = {
                'Tier': captainDetails[0],
                'TopBuff': captain_buffs[captainDetails[1]],
                'BottomBuff': captain_buffs[captainDetails[2]],
                'Level': captainDetails[3],
                # 'EXP': captainDetails[4],
                'TopBuffBaseValue': captainDetails[5],
                'BottomBuffBaseValue': captainDetails[6],
            }
        except:
            account.sailing['Captains'][captainIndex] = {
                'Tier': 0,
                'TopBuff': 'None',
                'BottomBuff': 'None',
                'Level': 0,
                # 'EXP': 0,
                'TopBuffBaseValue': 0,
                'BottomBuffBaseValue': 0,
            }

def _parse_w5_divinity(account):
    account.divinity.link_characters(account.safe_characters)
