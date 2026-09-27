from collections import defaultdict
from math import floor
from flask import g

from consts.consts_autoreview import items_codes_and_names
from consts.idleon.consts_idleon import max_characters
from consts.idleon.lava_func import lava_func
from consts.consts_general import (
    key_cards, cardset_names, card_raw_data, achievements_list
)
from consts.consts_item_data import ITEM_DATA
from consts.consts_monster_data import decode_monster_name
from consts.w1.stamps import stamp_types
from consts.consts_w3 import buildings_dict
from models.w1.statues import Statues
from models.general.assets import Assets
from models.general.character import Character
from models.general.cards import Card
from models.w1.stamps import Stamp
from utils.data_formatting import getCharacterDetails
from utils.safer_data_handling import safe_loads, safer_get, safer_convert
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.text_formatting import numberToLetter, letterToNumber

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

    account.family_bonuses.calculate_levels(account.safe_characters)
    _parse_general_achievements(account)
    _parse_general_item_filter(account)
    _parse_general_quests(account)
    _parse_general_inventory_slots_account_wide(account)

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

def _parse_general_item_filter(account):
    account.item_filter = []
    raw_printer_xtra = safe_loads(account.raw_data.get('PrinterXtra', []))
    if len(raw_printer_xtra) >= 121:
        for codeName in raw_printer_xtra[120:]:
            if codeName != 'Blank':
                account.item_filter.append(codeName)

def _parse_general_inventory_slots_account_wide(account):
    account.inventory.calculate_owned(
        account.all_characters,
        account.autoloot,
        account.event_points_shop['Secret Pouch'].owned,
        account.gemshop.bundles['bon_f'].owned,
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
    _parse_w1_stamps(account)
    account.statues = Statues(account.raw_data, account.safe_characters)

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
    _parse_w2_weekly_boss(account)


def _parse_w2_weekly_boss(account):
    account.weekly_boss_kills = safer_get(account.raw_optlacc_dict, 189, 0)


def _parse_w3(account):
    _parse_w3_buildings(account)
    _parse_w3_deathnote(account)
    _parse_w3_equinox(account)

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
    _parse_w4_rift(account)
    _parse_w4_breeding(account)

def _parse_w4_rift(account):
    # Seam: hands the model the already-parsed quest data it needs
    account.rift.calculate_unlocked(account.all_quests)

def _parse_w4_breeding(account):
    # Seam: egg slots need gem shop and merits
    account.breeding.calculate_egg_slots(
        account.gemshop.purchases['Royal Egg Cap'].owned,
        account.merits[3][2].level,
    )

def _parse_w5(account):
    _parse_w5_slab(account)
    _parse_w5_divinity(account)

def _parse_w5_slab(account):
    account.registered_slab = set(safe_loads(account.raw_data.get("Cards1", [])))

def _parse_w5_divinity(account):
    account.divinity.link_characters(account.safe_characters)
