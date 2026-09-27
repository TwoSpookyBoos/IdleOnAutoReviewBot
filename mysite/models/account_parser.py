from collections import defaultdict
from math import floor
from flask import g

from consts.consts_autoreview import items_codes_and_names
from consts.idleon.consts_idleon import max_characters
from consts.consts_general import (
    key_cards, cardset_names, card_raw_data
)
from consts.consts_monster_data import decode_monster_name
from models.w1.statues import Statues
from models.general.assets import Assets
from models.general.character import Character
from models.general.quests import Quests
from models.general.cards import Card
from utils.data_formatting import getCharacterDetails
from utils.safer_data_handling import safe_loads, safer_get, safer_convert
from utils.logging import get_logger
from utils.number_formatting import parse_number

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
    _parse_w1(account)
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
    account.quests = Quests(account.raw_data, account.character_count)
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

    account.family_bonuses.calculate_levels(account.safe_characters)
    _parse_general_item_filter(account)
    _parse_general_inventory_slots_account_wide(account)

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

def _parse_w1(account):
    account.statues = Statues(account.raw_data, account.safe_characters)

def _parse_w3(account):
    _parse_w3_deathnote(account)
    _parse_w3_equinox(account)

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
    account.rift.calculate_unlocked(account.quests.by_character)

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
