import copy
from collections import defaultdict
from math import floor
from flask import g

from consts.consts_autoreview import ValueToMulti, items_codes_and_names
from consts.idleon.consts_idleon import companions_data, max_characters
from consts.idleon.lava_func import lava_func
from consts.consts_general import (
    key_cards, cardset_names, card_raw_data, gem_shop_dict, gem_shop_optlacc_dict,
    gem_shop_bundles_dict,
    guild_bonuses_dict, family_bonuses_dict, achievements_list, allMeritsDict, vault_stack_types,
    vault_section_indexes, UpgradeVault, vault_dont_scale, inventory_bags_dict, inventory_other_sources_dict, storage_chests_dict
)
from consts.consts_item_data import ITEM_DATA
from consts.consts_master_classes import (
    grimoire_upgrades_list, grimoire_dont_scale, grimoire_bones_list, compass_upgrades_list, compass_dusts_list,
    compass_titans, compass_path_ordering, compass_medallions, tesseract_upgrades_list, tesseract_tachyon_list
)
from consts.consts_monster_data import decode_monster_name
from consts.consts_w1 import (
    starsigns_dict, forge_upgrades_dict, statues_dict, statue_type_dict,
    statue_count, event_points_shop_dict,
    statue_type_count, get_statue_type_index_from_name, basketball_upgrade_descriptions, darts_upgrade_descriptions
)
from consts.w1.stamps import stamp_types
from consts.w1.bribes import bribes_dict
from consts.consts_w2 import (
    max_index_of_vials, max_vial_level, max_implemented_bubble_index, vials_dict, sigils_dict, bubbles_dict, arcade_bonuses,
    arcade_max_level, ballot_dict, obols_dict, ignorable_obols_list, islands_dict, killroy_dict, getReadableVialNames, get_obol_totals
)
from consts.consts_w3 import (
    max_implemented_dreams, dreams_that_unlock_new_bonuses, equinox_bonuses_dict, refinery_dict, buildings_dict, buildings_shrines, atoms_list,
    collider_storage_limit_list, prayers_dict, salt_lick_list, dn_miniboss_skull_requirement_list, dn_miniboss_names, dn_skull_value_list,
    apocable_map_index_dict,
    apoc_amounts_list, apoc_names_list, getSkullNames, printer_all_indexes_being_printed, equipment_sets_dict, totems_list
)
from consts.consts_w4 import (
    max_cooking_tables, max_meal_count, max_meal_level, cooking_meal_dict, rift_rewards_dict, lab_chips_dict, lab_bonuses_dict, lab_jewels_dict,
    max_breeding_territories, slot_unlock_waves_list, territory_names, breeding_upgrades_dict, breeding_genetics_list, breeding_shiny_bonus_list, breeding_species_dict,
    getShinyLevelFromDays, getDaysToNextShinyLevel, getBreedabilityMultiFromDays, getBreedabilityHeartFromMulti
)
from consts.consts_w5 import (
    sailing_dict, captain_buffs, divinity_divinities_dict, gaming_superbits_dict, getDivinityNameFromIndex, getStyleNameFromIndex, npc_tokens,
    sailing_artifacts_dict, artifact_tier_names, sailing_artifacts_description_overrides
)
from consts.consts_caverns import (
    getCavernResourceImage, caverns_cavern_names, caverns_villagers, caverns_engineer_schematics,
    caverns_engineer_schematics_unlock_order, schematics_unlocking_harp_chords, max_buckets, sediment_bars, max_sediments, caverns_conjuror_majiks,
    caverns_measurer_measurements, caverns_measurer_HI55, caverns_librarian_studies, monument_bonuses, bell_ring_bonuses, bell_clean_improvements,
    harp_chord_effects, max_harp_notes, lamp_world_wish_values, lamp_wishes, caverns_jar_collectibles_count, caverns_jar_max_rupies, caverns_jar_jar_types,
    caverns_jar_max_jar_types, caverns_gambit_pts_bonuses, caverns_gambit_challenge_names, schematics_unlocking_gambit_challenges,
    caverns_gambit_total_challenges, getVillagerEXPRequired, getBellExpRequired, getGrottoKills, getWishCost, caverns_jar_collectibles
)
from consts.consts_w6 import (
    max_farming_crops, landrank_dict,
    market_upgrade_details,
    crop_depot_dict, summoning_sanctuary_counts, summoning_upgrades,
    max_summoning_upgrades, summoning_regular_match_colors,
    summoning_dict, summoning_endlessDict, summoning_stone_locations,
    summoning_stone_boss_images, summoning_stone_stone_images, summoning_stone_boss_base_hp,
    summoning_stone_boss_base_damage,
    summoning_regular_battles
)
from models.general.models_consumables import Bag, StorageChest
from consts.consts_w7 import Spelunky
from models.general.assets import Assets
from models.general.enemies import EnemyWorld, buildMaps
from models.general.character import Character
from models.general.cards import Card
from models.w1.stamps import Stamp
from utils.data_formatting import getCharacterDetails
from utils.safer_data_handling import safe_loads, safer_get, safer_convert, safer_math_pow, safer_index
from utils.logging import get_logger
from utils.number_formatting import parse_number
from utils.text_formatting import getItemDisplayName, numberToLetter, kebab, vault_string_cleaner, letterToNumber

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

    cards = [
        Card(
            codename=card_values['Card Name'],
            name=decoded_enemy_name,
            cardset=card_values['Set Name'],
            count=safer_get(card_counts, card_values['Card Name'], 0),
            coefficient=card_values['Cards For 1star'],
            value_per_level=card_values['Value per Level'],
            description=card_values['Description']
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
    _parse_companions(account)
    _parse_master_classes(account)
    _parse_w1(account)
    _parse_w2(account)
    _parse_w3(account)
    _parse_w4(account)
    _parse_w5(account)
    _parse_caverns(account)
    _parse_w6(account)
    _parse_w7(account)

def _parse_switches(account):
    # AutoLoot
    if g.autoloot:
        account.autoloot = True
    elif account.raw_data.get("AutoLoot", 0) == 1 or safe_loads(account.raw_data.get('BundlesReceived', {})).get('bun_i', 0) == 1:
        account.autoloot = True
        g.autoloot = True
    else:
        account.autoloot = False

    account.max_subgroups = 3
    account.library_group_characters = g.library_group_characters
    account.tabbed_advice_groups = g.tabbed_advice_groups

def _parse_companions(account):
    # Companions v2
    account.companions = {}

    # Read the player's data to capture all unique Companion IDs
    acquired_companion_ids = set()
    # If the data comes from Toolbox, it'll be a dictionary called companion singular
    raw_companion = account.raw_data.get('companion', None)
    # If the data comes from Efficiency, it'll be a flat list of just companion ID: "companions": [7, 10, 4, 5, 9, 2, 3, 6]
    raw_companions = account.raw_data.get('companions', None)
    if raw_companion is not None:
        account.companions['Companion Data Present'] = True
        for companionInfo in raw_companion.get('l', []):
            try:
                companionID = int(companionInfo.split(',')[0])
                acquired_companion_ids.add(companionID)
            except:
                continue
    elif raw_companions is not None:
        account.companions['Companion Data Present'] = True
        for companionID in raw_companions:
            acquired_companion_ids.add(companionID)
    else:
        account.companions['Companion Data Present'] = False
        logger.debug(f"No companion data present in JSON. Relying only on Switches")

    # Match the Companion IDs to their names
    for companion_name, companion_data in companions_data.items():
        if companion_data['Id'] in acquired_companion_ids:
            account.companions[companion_name] = copy.deepcopy(companion_data)
            if companion_name == 'Biggole Mole':
                biggole_mole_max_days = 100
                biggole_mole_days = min(biggole_mole_max_days, safer_get(account.raw_optlacc_dict, 354, 0))
                account.companions[companion_name]['Description'] += f" ({biggole_mole_days}/{biggole_mole_max_days} days)"

    # Account for the manual entries in the Switches
    try:
        if g.doot:
            account.companions['King Doot'] = companions_data['King Doot']
        if g.riftslug:
            account.companions['Rift Slug'] = companions_data['Rift Slug']
        if g.sheepie:
            account.companions['Sheepie'] = companions_data['Sheepie']
    except:
        pass

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

    _parse_class_unique_kill_stacks(account)
    _parse_general_gem_shop(account)
    _parse_general_gem_shop_optlacc(account)
    _parse_general_gem_shop_bundles(account)
    _parse_family_bonuses(account)
    _parse_dungeon_upgrades(account)
    _parse_general_achievements(account)
    _parse_general_merits(account)
    _parse_general_guild_bonuses(account)
    _parse_general_printer(account)
    _parse_general_maps(account)
    _parse_general_colo_scores(account)
    _parse_general_event_points_shop(account)
    _parse_general_quests(account)
    _parse_general_npc_tokens(account)
    _parse_general_inventory_slots_account_wide(account)
    _parse_general_inventory_characters(account)
    _parse_general_storage_slots(account)

def _parse_class_unique_kill_stacks(account):
    account.class_kill_talents = {
        'Archlord of the Pirates': {
            'Kills': safer_get(account.raw_optlacc_dict, 139, 0),
        },
        'King of the Remembered': {
            'Kills': safer_get(account.raw_optlacc_dict, 138, 0),
        },
        'Wormhole Emperor': {
            'Kills': safer_get(account.raw_optlacc_dict, 152, 0),
        }
    }

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

def _parse_general_npc_tokens(account):
    account.npc_tokens = {}
    raw_npc_tokens = account.raw_data.get('CYNPC', [])
    for tokenIndex, tokenName in enumerate(npc_tokens):
        try:
            account.npc_tokens[tokenName] = safer_convert(raw_npc_tokens[tokenIndex], 0)
        except Exception as e:
            logger.warning(f"NPC Token Parse error at tokenIndex {tokenIndex}: {e}. Defaulting to 0")
            account.npc_tokens[tokenName] = 0
    # for tokenName, tokenCount in account.npc_tokens.items():
    #     account.all_assets.get(tokenName).add(tokenCount)

def _parse_family_bonuses(account):
    account.family_bonuses = {}
    for className in family_bonuses_dict.keys():
        # Create the skeleton for all current classes, with level and value of 0
        account.family_bonuses[className] = {'Level': 0, 'Value': 0}
    for char in account.safe_characters:
        for className in [char.base_class, char.sub_class, char.elite_class]:
            if className in family_bonuses_dict:
                if char.combat_level > account.family_bonuses[className]['Level']:
                    account.family_bonuses[className]['Level'] = char.combat_level
    for className in account.family_bonuses.keys():
        try:
            account.family_bonuses[className]['Value'] = lava_func(
                family_bonuses_dict[className]['funcType'],
                account.family_bonuses[className]['Level'] - min(family_bonuses_dict[className]['levelDiscount'], account.family_bonuses[className]['Level']),
                family_bonuses_dict[className]['x1'],
                family_bonuses_dict[className]['x2'])
        except:
            logger.exception(f"Error parsing Family Bonus for {className}. Defaulting to 0 value")
            account.family_bonuses[className]['Value'] = 0
        account.family_bonuses[className]['DisplayValue'] = (
            f"{'+' if family_bonuses_dict[className]['PrePlus'] else ''}"
            f"{account.family_bonuses[className]['Value']:.2f}"
            f"{family_bonuses_dict[className]['PostDisplay']}"
            f" {family_bonuses_dict[className]['Stat']}"
        )

def _parse_dungeon_upgrades(account):
    account.dungeon_upgrades = {}
    raw_dungeon_upgrades = safe_loads(account.raw_data.get('DungUpg', []))
    try:
        account.dungeon_upgrades["MaxWeapon"] = raw_dungeon_upgrades[3][0]
    except Exception as e:
        logger.warning(f"Dungeon Upgrade Max Weapon Parse error: {e}. Defaulting to 0")
        account.dungeon_upgrades["MaxWeapon"] = 0

    try:
        account.dungeon_upgrades["MaxArmor"] = [
            raw_dungeon_upgrades[3][4], raw_dungeon_upgrades[3][5], raw_dungeon_upgrades[3][6], raw_dungeon_upgrades[3][7]
        ]
    except Exception as e:
        logger.warning(f"Dungeon Upgrade Max Armor Parse error: {e}. Defaulting to 0")
        account.dungeon_upgrades["MaxArmor"] = [0, 0, 0, 0]

    try:
        account.dungeon_upgrades["MaxJewelry"] = [raw_dungeon_upgrades[3][8], raw_dungeon_upgrades[3][9]]
    except Exception as e:
        logger.warning(f"Dungeon Upgrade Max Jewelry Parse error: {e}. Defaulting to 0")
        account.dungeon_upgrades["MaxJewelry"] = [0, 0]

    try:
        account.dungeon_upgrades["FlurboShop"] = raw_dungeon_upgrades[5]
        account.dungeon_upgrades["CreditShop"] = raw_dungeon_upgrades[1]
    except Exception as e:
        logger.warning(f"Dungeon UFlurbo+Credit Shops Parse error: {e}. Defaulting to 0")
        account.dungeon_upgrades["FlurboShop"] = [0, 0, 0, 0, 0, 0, 0, 0]
        account.dungeon_upgrades["CreditShop"] = [0, 0, 0, 0, 0, 0, 0, 0]

    ##Blatantly stolen list from IE lol
    # https://github.com/Sludging/idleon-efficiency/blob/74f83dd4c0b15f399ffb1f87bc2bc8c9bc9b924c/data/domain/dungeons.tsx#L16
    dungeonLevelsList = [0, 4, 10, 18, 28, 40, 70, 110, 160, 230, 320, 470, 670, 940, 1310, 1760, 2400, 3250, 4000, 5000, 6160, 8000, 10000, 12500,
                         15000, 18400, 21000, 25500, 30500, 36500, 45400, 52000, 61000, 72500, 85000, 110000, 125000, 145000, 170000, 200000, 250000,
                         275000, 325000, 400000, 490000, 600000, 725000, 875000, 1000000, 1200000, 1500000, 3000000, 5000000, 10000000, 20000000,
                         30000000, 40000000, 50000000, 60000000, 80000000, 100000000, 999999999, 999999999, 999999999, 999999999, 999999999, 1999999999,
                         1999999999, 1999999999, 1999999999, 1999999999]
    playerDungeonXP = safer_get(account.raw_optlacc_dict, 71, 0)
    account.playerDungeonRank = 0
    for xpRequirement in dungeonLevelsList:
        if playerDungeonXP >= xpRequirement:
            account.playerDungeonRank += 1

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

def _parse_general_guild_bonuses(account):
    account.guild_bonuses = {}
    raw_guild = safe_loads(account.raw_data.get('Guild', [[]]))
    for bonus_index, (bonus_name, bonus) in enumerate(guild_bonuses_dict.items()):
        try:
            guild_bonus_level = safer_convert(raw_guild[0][bonus_index], 0)
        except Exception as e:
            logger.warning(f"Guild Bonus Parse error: {e}. Defaulting to 0")
            guild_bonus_level = 0
        account.guild_bonuses[bonus_name] = {
            'Level': guild_bonus_level,
            'Value': lava_func(bonus['funcType'], guild_bonus_level, bonus['x1'], bonus['x2']),
            'Max Level': bonus['Max Level'],
            'Max Value': bonus['Max Value'],
            'Image': bonus['Image'],
            'Description': bonus['Description']
        }

def _parse_general_printer(account):
    account.printer = {
        'HighestValue': 0,
        'AllSamplesSorted': {},
        'CurrentPrintsByCharacter': {},
        'AllCurrentPrints': {},
    }

    raw_print = safe_loads(account.raw_data.get('Print', [0, 0, 0, 0, 0, 'Blank']))[5:]
    raw_printer_xtra = safe_loads(account.raw_data.get('PrinterXtra', []))
    _parse_general_item_filter(account, raw_printer_xtra)
    account.printer['HighestValue'] = max([p for p in raw_print if isinstance(p, int)] + [p for p in raw_printer_xtra if isinstance(p, int)], default=0)

    try:
        sample_names = raw_print[0::2] + raw_printer_xtra[0:119:2]
        sample_values = raw_print[1::2] + raw_printer_xtra[1:119:2]
    except Exception as e:
        logger.warning(f"3d Printer Parse error: {e}. Defaulting to []")
        sample_names = []
        sample_values = []
    for sampleIndex, sampleItem in enumerate(sample_names):
        if sampleItem:
            if sampleIndex in printer_all_indexes_being_printed:
                if sampleIndex // 7 not in account.printer['CurrentPrintsByCharacter']:
                    account.printer['CurrentPrintsByCharacter'][sampleIndex // 7] = {}
                if getItemDisplayName(sampleItem) not in account.printer['CurrentPrintsByCharacter'][sampleIndex // 7]:
                    account.printer['CurrentPrintsByCharacter'][sampleIndex // 7][getItemDisplayName(sampleItem)] = []
                try:
                    account.printer['CurrentPrintsByCharacter'][sampleIndex // 7][getItemDisplayName(sampleItem)].append(sample_values[sampleIndex])
                except:
                    logger.exception(f"Failed on characterIndex '{sampleIndex // 7}', sampleIndex '{sampleIndex}', sampleItem '{sampleItem}'")
            else:
                if sampleItem != 'Blank':  # Don't want blanks in the AllSorted list, but they're desired in the Character-Specific group
                    if getItemDisplayName(sampleItem) not in account.printer['AllSamplesSorted']:
                        account.printer['AllSamplesSorted'][getItemDisplayName(sampleItem)] = []
                    try:
                        account.printer['AllSamplesSorted'][getItemDisplayName(sampleItem)].append(float(sample_values[sampleIndex]))
                    except:
                        logger.exception(f"Failed on sampleIndex '{sampleIndex}', sampleItem '{sampleItem}'")
    for sampleItem in account.printer['AllSamplesSorted']:
        account.printer['AllSamplesSorted'][sampleItem].sort(reverse=True)
    for characterIndex, printDict in account.printer['CurrentPrintsByCharacter'].items():
        if characterIndex < account.character_count:
            account.all_characters[characterIndex].setPrintedMaterials(printDict)
        for printName, printValues in printDict.items():
            if printName not in account.printer['AllCurrentPrints']:
                account.printer['AllCurrentPrints'][printName] = []
            account.printer['AllCurrentPrints'][printName] += printValues

def _parse_general_item_filter(account, raw_printer_xtra):
    account.item_filter = []
    if len(raw_printer_xtra) >= 121:
        for codeName in raw_printer_xtra[120:]:
            if codeName != 'Blank':
                account.item_filter.append(codeName)

def _parse_general_maps(account):
    account.enemy_maps = buildMaps()
    account.enemy_worlds = {}

def _parse_general_colo_scores(account):
    account.colo_scores = {}
    raw_colo_scores = safe_loads(account.raw_data.get('FamValColosseumHighscores', []))
    for coloIndex, coloScore in enumerate(raw_colo_scores):
        try:
            account.colo_scores[coloIndex] = safer_convert(coloScore, 0)
        except Exception as e:
            logger.warning(f"Colo Score Parse error at coloIndex {coloIndex}: {e}. Defaulting to 0")
            account.colo_scores[coloIndex] = 0

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
    #Dependencies: _parse_switches, _parse_characters, _parse_general_gem_shop_bundles, _parse_general_event_points_shop
    #Create dictionary for Account Wide Inventory sources
    fourth_anni_bag_owned = any([char.character_name for char in account.all_characters if '112' in char.inventory_bags])
    account.inventory['Account Wide Inventory'] = {
        'Default': {
            'Description': inventory_other_sources_dict['Default']['Description'],
            'Max Slots': inventory_other_sources_dict['Default']['Max Slots'],
            'Owned': True,
            'Owned Slots': inventory_other_sources_dict['Default']['Max Slots'],
            'Image': inventory_other_sources_dict['Default']['Image']
        },
        'Autoloot': {
            'Description': inventory_other_sources_dict['Autoloot']['Description'],
            'Max Slots': inventory_other_sources_dict['Autoloot']['Max Slots'],
            'Owned': account.autoloot,
            'Owned Slots': inventory_other_sources_dict['Autoloot']['Max Slots'] * account.autoloot,
            'Image': inventory_other_sources_dict['Autoloot']['Image'],
            'Resource': inventory_other_sources_dict['Autoloot']['Resource']
        },
        'Secret Pouch': {
            'Description': inventory_other_sources_dict['Secret Pouch']['Description'],
            'Max Slots': inventory_other_sources_dict['Secret Pouch']['Max Slots'],
            'Owned': account.event_points_shop['Bonuses']['Secret Pouch']['Owned'],
            'Owned Slots': inventory_other_sources_dict['Secret Pouch']['Max Slots'] * account.event_points_shop['Bonuses']['Secret Pouch']['Owned'],
            'Image': inventory_other_sources_dict['Secret Pouch']['Image'],
            'Resource': inventory_other_sources_dict['Secret Pouch']['Resource']
        },
        'Fourth Anni': {
            'Description': inventory_other_sources_dict['Fourth Anni']['Description'],
            'Max Slots': inventory_other_sources_dict['Fourth Anni']['Max Slots'],
            'Owned': fourth_anni_bag_owned,
            'Owned Slots': inventory_other_sources_dict['Fourth Anni']['Max Slots'] * fourth_anni_bag_owned,
            'Image': inventory_other_sources_dict['Fourth Anni']['Image']
        },
        'bon_f': {
            'Description': inventory_other_sources_dict['bon_f']['Description'],
            'Max Slots': inventory_other_sources_dict['bon_f']['Max Slots'],
            'Owned': account.gemshop['Bundles']['bon_f']['Owned'],
            'Owned Slots': inventory_other_sources_dict['bon_f']['Max Slots'] * account.gemshop['Bundles']['bon_f']['Owned'],
            'Image': inventory_other_sources_dict['bon_f']['Image'],
            'Resource': inventory_other_sources_dict['bon_f']['Resource']
        },
    }
    account.inventory['Account Wide Inventory Slots Owned'] = sum([source['Owned Slots'] for source in account.inventory['Account Wide Inventory'].values()])
    account.inventory['Account Wide Inventory Slots Max'] = sum([source['Max Slots'] for source in account.inventory['Account Wide Inventory'].values()])

def _parse_general_inventory_characters(account):
    #Dependencies: _parse_general_inventory_slots_account_wide
    # Sanity check for any unknown bags present in the JSON
    unknown_bags_in_json = set()
    for character in account.all_characters:
        for bag in character.inventory_bags:
            if int(bag) not in inventory_bags_dict:
                unknown_bags_in_json.add(f"{bag}: {character.inventory_bags[bag]}")
    if len(unknown_bags_in_json) > 0:
        logger.warning(f"Unknown Inventory Bags found in JSON: {unknown_bags_in_json}. Get these added to consts_general.inventory_bags_dict")

    for character in account.all_characters:
        account.inventory['Characters Missing Bags'][character.character_index] = [bag for bag in Bag if str(bag.value) not in character.inventory_bags]
        character.inventory_slots = account.inventory['Account Wide Inventory Slots Owned']
        for bag in character.inventory_bags:
            if int(bag) == 112:
                continue  #4th anniversary bag accounted for in account wide inventory
            if isinstance(character.inventory_bags[bag], int | float | str):
                try:
                    character.inventory_slots += parse_number(character.inventory_bags[bag])
                except:
                    logger.exception(f"Could not increase character {character.character_index}'s bagslots by {type(character.inventory_bags[bag])} {character.inventory_bags[bag]}")
            else:
                logger.warning(f"Funky bag value found in {character.character_index}'s bagsDict for bag {bag}: {type(character.inventory_bags[bag])} {character.inventory_bags[bag]}. Searching for expected value.")
                if int(bag) in inventory_bags_dict:
                    logger.debug(f"Bag {bag} has a known value: {inventory_bags_dict.get(int(bag), 0)}. All is well :)")
                else:
                    logger.error(f"Bag {bag} has no known value. Defaulting to 0 :(")
                character.inventory_slots += inventory_bags_dict.get(int(bag), 0)

def _parse_general_storage_slots(account):
    #Dependencies: None
    raw_used_chests = safe_loads(account.raw_data.get('InvStorageUsed', []))
    # Sanity check for any unknown chests present in the JSON
    unknown_chests_in_json = [f"{key}:{value}" for key, value in raw_used_chests.items() if int(key) not in storage_chests_dict.keys()]
    if len(unknown_chests_in_json) > 0:
        logger.warning(f"Unknown Storage Chest found in JSON: {unknown_chests_in_json}. Get these added to consts_general.storage_chests_dict")

    account.storage['Used Chests'] = [chest for chest in StorageChest if str(chest.value) in raw_used_chests.keys()]
    account.storage['Used Chest Slots'] = sum([storage_chests_dict.get(chest.value) for chest in account.storage['Used Chests']])
    account.storage['Missing Chests'] = [chest for chest in StorageChest if str(chest.value) not in raw_used_chests.keys()]
    account.storage['Missing Chest Slots'] = sum([storage_chests_dict.get(chest.value) for chest in account.storage['Missing Chests']])


def _parse_master_classes(account):
    _parse_master_classes_grimoire(account)
    _parse_master_classes_compass(account)
    _parse_master_classes_tesseract(account)

def _parse_master_classes_grimoire(account):
    account.grimoire = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Total Bones Collected': safer_convert(safer_get(account.raw_optlacc_dict, 329, 0), 0.0),
        'Bone1': safer_convert(safer_get(account.raw_optlacc_dict, 330, 0), 0.0),
        'Bone2': safer_convert(safer_get(account.raw_optlacc_dict, 331, 0), 0.0),
        'Bone3': safer_convert(safer_get(account.raw_optlacc_dict, 332, 0), 0.0),
        'Bone4': safer_convert(safer_get(account.raw_optlacc_dict, 333, 0), 0.0),
        'Knockout Stacks': safer_convert(safer_get(account.raw_optlacc_dict, 334, 0), 0),
        'Elimination Stacks': safer_convert(safer_get(account.raw_optlacc_dict, 335, 0), 0),
        'Annihilation Stacks': safer_convert(safer_get(account.raw_optlacc_dict, 336, 0), 0),
        'Charred Bones Enabled': safer_convert(safer_get(account.raw_optlacc_dict, 367, False), False)
    }
    #Parse Grimoire Upgrades
    raw_grimoire = safe_loads(account.raw_data.get('Grimoire', []))
    if not raw_grimoire:
        logger.warning(f"Grimore data not present{', as expected' if account.version < 236 else ''}.")
    for upgrade_index, upgrade_values_list in enumerate(grimoire_upgrades_list):
        clean_name = upgrade_values_list[0].replace('(Tap_for_more_info)', '').replace('製', '').replace('_', ' ').rstrip()
        if '(#)' in clean_name:
            stack_type = clean_name.split('!')[0]
            clean_name = clean_name.replace('(#)', f"({account.grimoire.get(f'{stack_type} Stacks', '#')})")
        if clean_name != 'Ripped Page':
            try:
                account.grimoire['Upgrades'][clean_name] = {
                    'Level': min(int(upgrade_values_list[4]), int(raw_grimoire[upgrade_index])),
                    'Index': upgrade_index,
                    'Image': f"grimoire-upgrade-{upgrade_index}",
                    'Cost Base': int(upgrade_values_list[1]),
                    'Cost Increment': float(upgrade_values_list[2]),
                    'Bone Name': grimoire_bones_list[int(upgrade_values_list[3])],
                    'Bone Image': f"grimoire-bone-{upgrade_values_list[3]}",
                    'Max Level': int(upgrade_values_list[4]),
                    'Value Per Level': int(upgrade_values_list[5]),
                    'Unlock Requirement': int(upgrade_values_list[6]),
                    # 'Placeholder7': upgrade_values_list[7],
                    # 'Placeholder8': upgrade_values_list[8],
                    'Description': upgrade_values_list[9].replace('_', ' '),
                    'Scaling Value': upgrade_index not in grimoire_dont_scale
                }
            except:
                #logger.exception(f"Error parsing Grimoire Index {upgrade_index}")
                account.grimoire['Upgrades'][clean_name] = {
                    'Level': 0,
                    'Index': upgrade_index,
                    'Image': f"grimoire-upgrade-{upgrade_index}",
                    'Cost Base': int(upgrade_values_list[1]),
                    'Cost Increment': float(upgrade_values_list[2]),
                    'Bone Name': grimoire_bones_list[int(upgrade_values_list[3])],
                    'Bone Image': f"grimoire-bone-{upgrade_values_list[3]}",
                    'Max Level': int(upgrade_values_list[4]),
                    'Value Per Level': int(upgrade_values_list[5]),
                    'Unlock Requirement': int(upgrade_values_list[6]),
                    # 'Placeholder7': upgrade_values_list[7],
                    # 'Placeholder8': upgrade_values_list[8],
                    'Description': upgrade_values_list[9].replace('_', ' '),
                    'Scaling Value': upgrade_index not in grimoire_dont_scale
                }

    #Sum total upgrades
    account.grimoire['Total Upgrades'] = sum([v['Level'] for v in account.grimoire['Upgrades'].values()])
    for upgrade_name in account.grimoire['Upgrades']:
        account.grimoire['Upgrades'][upgrade_name]['Unlocked'] = account.grimoire['Total Upgrades'] >= account.grimoire['Upgrades'][upgrade_name]['Unlock Requirement']

def _parse_master_classes_compass(account):
    account.compass = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Total Dust Collected': safer_convert(safer_get(account.raw_optlacc_dict, 362, 0), 0.0),
        'Dust1': safer_convert(safer_get(account.raw_optlacc_dict, 357, 0), 0.0),
        'Dust2': safer_convert(safer_get(account.raw_optlacc_dict, 358, 0), 0.0),
        'Dust3': safer_convert(safer_get(account.raw_optlacc_dict, 359, 0), 0.0),
        'Dust4': safer_convert(safer_get(account.raw_optlacc_dict, 360, 0), 0.0),
        'Dust5': safer_convert(safer_get(account.raw_optlacc_dict, 361, 0), 0.0),
        "Top of the Mornin'": max(0, safer_convert(safer_get(account.raw_optlacc_dict, 365, 0),0)),
        'Abominations': {},
        'Elements': {0: 'Fire', 1: 'Wind', 2: 'Grass', 3: 'Ice'},
        'Medallions': {},
        'Total Medallions': 0,
        'Aethermoons Enabled': safer_convert(safer_get(account.raw_optlacc_dict, 401, False), False)
    }
    #Parse Compass Upgrades
    raw_compass = safe_loads(account.raw_data.get('Compass', []))
    if not raw_compass:
        logger.warning(f"Compass data not present{', as expected' if account.version < 264 else ''}.")
    while len(raw_compass) < 5:
        raw_compass.append([])

    raw_abom_status = [safer_convert(v, 0) for v in raw_compass[1]]
    account.compass['Total Abominations Slain'] = sum(raw_abom_status)
    _parse_master_classes_abominations(account, raw_abom_status)  #Need their status for Upgrades

    raw_compass_upgrades = [safer_convert(v, 0) for v in raw_compass[0]]
    account.compass['Total Upgrades'] = sum([safer_convert(v, 0) for v in raw_compass_upgrades])
    _parse_master_classes_compass_upgrades(account, raw_compass_upgrades)

    # raw_portals_opened = raw_compass[2]
    raw_medallions = raw_compass[3]
    account.compass['Total Medallions'] = len(raw_medallions)
    _parse_master_classes_medallions(account, raw_medallions)

    raw_stamps_exalted = raw_compass[4]
    account.compass['Total Exalted'] = len(raw_stamps_exalted)
    # see _parse_master_classes_exalted_stamps for more info. Has to come after w1 stamps are parsed

def _parse_master_classes_abominations(account, raw_abom_status):
    for abom_index, abom_data in enumerate(compass_titans):
        clean_name = abom_data[0].replace('_', ' ')
        if 50 > int(abom_data[2]):
            weakness = 0
        elif 100 > int(abom_data[2]):
            weakness = 3
        elif 150 > int(abom_data[2]):
            weakness = 2
        elif 200 > int(abom_data[2]):
            weakness = 1
        else:
            weakness = int(abom_data[11]) % 4
        try:
            account.compass['Abominations'][clean_name] = {
                'Defeated': raw_abom_status[abom_index] > 0,
                'Map Index': int(abom_data[2]),
                'World': 1 + (int(abom_data[2])//50),
                'Image': f'titan-{abom_index}',
                'Weakness': account.compass['Elements'].get(weakness, 'Unknown')
            }
        except:
            account.compass['Abominations'][clean_name] = {
                'Defeated': False,
                'Map Index': int(abom_data[2]),
                'World': 1 + (int(abom_data[2]) // 50),
                'Image': f'titan-{abom_index}',
                'Weakness': account.compass['Elements'].get(weakness, 'Unknown')
            }

def _parse_master_classes_compass_upgrades(account, raw_compass_upgrades):
    for path_name, upgrade_indexes_list in compass_path_ordering.items():
        for path_ordering, upgrade_index in enumerate(upgrade_indexes_list):
            upgrade_values_list = compass_upgrades_list[upgrade_index]
            clean_name = upgrade_values_list[0].replace('(Tap_for_more_info)', '').replace('製', '').replace('_', ' ').rstrip()
            clean_description = upgrade_values_list[11].replace('_', ' ')  #.replace('@', '<br>')
            # if 'Titan doesnt exist' not in clean_description:  #Placeholders as of v2.35 release patch
            try:
                account.compass['Upgrades'][clean_name] = {
                    'Level': min(int(upgrade_values_list[4]), int(raw_compass_upgrades[upgrade_index])),
                    'Index': upgrade_index,
                    'Image': f"compass-upgrade-{upgrade_index}",
                    'Cost Base': int(upgrade_values_list[1]),
                    'Cost Increment': float(upgrade_values_list[2]),
                    'Dust Name': compass_dusts_list[int(upgrade_values_list[3])],
                    'Dust Image': f"compass-dust-{upgrade_values_list[3]}",
                    'Max Level': int(upgrade_values_list[4]),
                    'Value Per Level': safer_convert(upgrade_values_list[5], 0.00 if '.' in upgrade_values_list[5] else 0),
                    # 'Unlock Requirement': int(upgrade_values_list[6]),
                    # 'Placeholder7': upgrade_values_list[7],
                    # 'Placeholder8': upgrade_values_list[8],
                    'Shape': 'Square' if int(upgrade_values_list[9]) == 0 else 'Circle' if int(upgrade_values_list[9]) == 1 else 'UnknownShape',
                    # 'Path Index': int(upgrade_values_list[10]),
                    'Path Name': path_name,
                    'Path Ordering': path_ordering if path_name != 'Abomination' else path_ordering + 1,
                    'Description': clean_description,
                }
            except:
                if raw_compass_upgrades:
                    # No need for 200 exceptions if they don't have any Compass data
                    logger.exception(f"Error parsing Compass Upgrade Index {upgrade_index} ({clean_name})")
                account.compass['Upgrades'][clean_name] = {
                    'Level': 0,
                    'Index': upgrade_index,
                    'Image': f"compass-upgrade-{upgrade_index}",
                    'Cost Base': int(upgrade_values_list[1]),
                    'Cost Increment': float(upgrade_values_list[2]),
                    'Dust Name': compass_dusts_list[int(upgrade_values_list[3])],
                    'Dust Image': f"compass-dust-{upgrade_values_list[3]}",
                    'Max Level': int(upgrade_values_list[4]),
                    'Value Per Level': safer_convert(upgrade_values_list[5], 0.00 if '.' in upgrade_values_list[5] else 0),
                    # 'Unlock Requirement': int(upgrade_values_list[6]),
                    # 'Placeholder7': upgrade_values_list[7],
                    # 'Placeholder8': upgrade_values_list[8],
                    'Shape': 'Square' if int(upgrade_values_list[9]) == 0 else 'Circle' if int(upgrade_values_list[9]) == 1 else 'UnknownShape',
                    # 'Path Index': int(upgrade_values_list[10]),
                    'Path Name': path_name,
                    'Path Ordering': path_ordering,
                    'Description': clean_description,
                }
            account.compass['Upgrades'][clean_name]['Base Value'] = (
                account.compass['Upgrades'][clean_name]['Level']
                * account.compass['Upgrades'][clean_name]['Value Per Level']
            )

    # Determine Unlock Status
    for upgrade_name, upgrade_details in account.compass['Upgrades'].items():
        path_name = f"{upgrade_details['Path Name']} Path"
        if path_name == 'Default Path':
            if upgrade_name == 'Pathfinder':
                account.compass['Upgrades'][upgrade_name]['Unlocked'] = True
            else:
                account.compass['Upgrades'][upgrade_name]['Unlocked'] = account.compass['Upgrades']['Pathfinder']['Level'] >= 1
        elif path_name == 'Abomination Path':
            if 'Titan doesnt exist' not in upgrade_details['Description']:
                try:
                    account.compass['Upgrades'][upgrade_name]['Abomination Name'] = compass_titans[upgrade_details['Path Ordering']-1][0].replace('_', ' ')
                    account.compass['Upgrades'][upgrade_name]['Unlocked'] = account.compass['Abominations'][account.compass['Upgrades'][upgrade_name]['Abomination Name']]['Defeated']
                except:
                    account.compass['Upgrades'][upgrade_name]['Abomination Name'] = '??????'
                    logger.exception(f"Could not look up Abomination defeated status for {upgrade_name}")
                    account.compass['Upgrades'][upgrade_name]['Unlocked'] = False
        else:
            account.compass['Upgrades'][upgrade_name]['Unlocked'] = account.compass['Upgrades'][path_name]['Level'] >= upgrade_details['Path Ordering']

def _parse_master_classes_medallions(account, raw_medallions):
    known_extras = {
        'reindeer': ['Spirit Reindeer', 'spirit-reindeer'],
        'Crystal0': ['Crystal Carrot (Glitterbug prayer)', 'crystal-carrot'],
        'Crystal1': ['Crystal Crabal (Glitterbug prayer)', 'crystal-crabal'],
        'Crystal2': ['Crystal Cattle (Glitterbug prayer)', 'crystal-cattle'],
        'Crystal3': ['Crystal Custard (Glitterbug prayer)', 'crystal-custard'],
        'Crystal4': ['Crystal Capybara (Glitterbug prayer)', 'crystal-capybara'],
        'Crystal5': ['Crystal Candalight (Glitterbug prayer)', 'crystal-candalight'],
        'caveA': ['Cavern 3: Dawg Den', 'dawg-den-dawgs'],
        'rockS': ['W3 Colo: Skull Rock', 'skull-rock'],
        'Meteor': ['Random Event Boss: Fallen Meteor', 'fallen-meteor'],
        'rocky': ['Random Event Boss: Mega Grumblo', 'mega-grumblo'],
        'iceknight': ['Random Event Boss: Glacial Guild', 'ice-guard'],
        'snakeZ': ['Random Event Boss: Snake Swarm', 'snake-swarm'],
        'frogGR': ['Random Event Boss: Angry Frogs', 'angry-frogs'],
        'ChestA1': ['W1 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB1': ['W1 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC1': ['W1 Colo: Gold Chest', 'colo-gold-chest'],
        'ChestA2': ['W2 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB2': ['W2 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC2': ['W2 Colo: Gold Chest', 'colo-gold-chest'],
        'ChestA3': ['W3 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB3': ['W3 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC3': ['W3 Colo: Gold Chest', 'colo-gold-chest'],
        'ChestA4': ['W4 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB4': ['W4 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC4': ['W4 Colo: Gold Chest', 'colo-gold-chest'],
        'ChestA5': ['W5 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB5': ['W5 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC5': ['W5 Colo: Gold Chest', 'colo-gold-chest'],
        'ChestA6': ['W6 Colo: Bronze Chest', 'colo-bronze-chest'],
        'ChestB6': ['W6 Colo: Silver Chest', 'colo-silver-chest'],
        'ChestC6': ['W6 Colo: Gold Chest', 'colo-gold-chest'],
    }

    for raw_enemy_name in compass_medallions:
        if raw_enemy_name in known_extras:  #Anything that isn't a standard Card
            account.compass['Medallions'][raw_enemy_name] = {
                'Obtained': raw_enemy_name in raw_medallions,
                'Enemy Name': known_extras[raw_enemy_name][0],
                'Image': known_extras[raw_enemy_name][1],
            }
        else:
            decoded_name = decode_monster_name(raw_enemy_name, card=True)
            account.compass['Medallions'][raw_enemy_name] = {
                'Obtained': raw_enemy_name in raw_medallions,
                'Enemy Name': decoded_name,
                'Image': f"{decoded_name}-card"
            }

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

def _parse_master_classes_tesseract(account):
    account.tesseract = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Total Tachyons Collected': safer_convert(safer_get(account.raw_optlacc_dict, 394, 0), 0.0),
        'Tachyon1': safer_convert(safer_get(account.raw_optlacc_dict, 388, 0), 0.0),
        'Tachyon2': safer_convert(safer_get(account.raw_optlacc_dict, 389, 0), 0.0),
        'Tachyon3': safer_convert(safer_get(account.raw_optlacc_dict, 390, 0), 0.0),
        'Tachyon4': safer_convert(safer_get(account.raw_optlacc_dict, 391, 0), 0.0),
        'Tachyon5': safer_convert(safer_get(account.raw_optlacc_dict, 392, 0), 0.0),
        'Tachyon6': safer_convert(safer_get(account.raw_optlacc_dict, 393, 0), 0.0),
        'Prisma Bubbles': safer_convert(safer_get(account.raw_optlacc_dict, 395, 0), 0.0),
        'Arcane Rocks Enabled': safer_convert(safer_get(account.raw_optlacc_dict, 452, False), False)
    }
    raw_tesseract = safe_loads(account.raw_data.get('Arcane', []))
    if not raw_tesseract:
        logger.warning(f"Tesseract data not present{', as expected' if account.version < 236 else ''}.")
    for upgrade_index, upgrade_values_list in enumerate(tesseract_upgrades_list):
        clean_name = upgrade_values_list[0].replace('(Tap_for_more_info)', '').replace('製', '').replace('_', ' ').rstrip()
        if clean_name != 'Boundless Energy':
            try:
                level = min(int(upgrade_values_list[4]), int(raw_tesseract[upgrade_index]))
            except IndexError:
                level = 0
            account.tesseract['Upgrades'][clean_name] = {
                'Level': level,
                'Index': upgrade_index,
                'Image': f"tesseract-upgrade-{upgrade_index}",
                'Cost Base': int(upgrade_values_list[1]),
                'Cost Increment': float(upgrade_values_list[2]),
                'Tachyon Name': tesseract_tachyon_list[int(upgrade_values_list[3])],
                'Tachyon Image': f"tesseract-tachyon-{upgrade_values_list[3]}",
                'Max Level': int(upgrade_values_list[4]),
                'Value Per Level': int(upgrade_values_list[5]),
                'Unlock Requirement': int(upgrade_values_list[6]),
                # 'Placeholder7': upgrade_values_list[7],
                # 'Placeholder8': upgrade_values_list[8],
                'Description': upgrade_values_list[9].replace('_', ' '),
            }

    # Sum total upgrades
    account.tesseract['Total Upgrades'] = sum([v['Level'] for v in account.tesseract['Upgrades'].values()])
    for upgrade_name in account.tesseract['Upgrades']:
        account.tesseract['Upgrades'][upgrade_name]['Unlocked'] = account.tesseract['Total Upgrades'] >= account.tesseract['Upgrades'][upgrade_name]['Unlock Requirement']


def _parse_w1(account):
    _parse_w1_upgrade_vault(account)
    _parse_w1_starsigns(account)
    _parse_w1_forge(account)
    _parse_w1_bribes(account)
    _parse_w1_stamps(account)
    _parse_w1_owl(account)
    _parse_w1_statues(account)
    _parse_w1_minigames(account)

def _parse_w1_upgrade_vault(account):
    account.vault = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Knockout Stacks': safer_get(account.raw_optlacc_dict, 338, 0),
    }
    #Parse Vault Upgrades
    raw_vault = safe_loads(account.raw_data.get('UpgVault', []))
    if not raw_vault:
        logger.warning(f"Upgrade Vault data not present{', as expected' if account.version < 237 else ''}.")
    for upgrade_index, upgrade_values_list in enumerate(UpgradeVault):
        clean_name = vault_string_cleaner(upgrade_values_list[0])
        if len(upgrade_values_list) >= 11:
            secondary_description = vault_string_cleaner(upgrade_values_list[10]) if upgrade_values_list != '_' else ''
        else:
            secondary_description = ''
        if clean_name.split('!')[0] in vault_stack_types:
            stack_type = clean_name.split('!')[0]
            clean_name += f" ({account.vault.get(f'{stack_type} Stacks', '#')} stacks)"
        vault_section = 0
        for list_index, vault_section_index in enumerate(vault_section_indexes):
            if upgrade_index <= vault_section_index:
                vault_section = list_index + 1
                break
        try:
            account.vault['Upgrades'][clean_name] = {
                'Level': min(int(upgrade_values_list[4]), int(raw_vault[upgrade_index])),
                'Index': upgrade_index,
                'Image': f"vault-upgrade-{upgrade_index}",
                'Cost Base': safer_convert(upgrade_values_list[1], 0),
                'Cost Increment': float(upgrade_values_list[2]),
                # 'Placeholder3': upgrade_values_list[3],
                'Max Level': int(upgrade_values_list[4]),
                'Value Per Level': int(upgrade_values_list[5]),
                'Unlock Requirement': int(upgrade_values_list[6]),
                # 'Placeholder7': upgrade_values_list[7],
                # 'Placeholder8': upgrade_values_list[8],
                'Description': f"{vault_string_cleaner(upgrade_values_list[9])} {secondary_description}",
                'Scaling Value': upgrade_index not in vault_dont_scale,
                'Vault Section': vault_section
            }
        except:
            # logger.exception(f"Vault parse error on index {upgrade_index}")
            account.vault['Upgrades'][clean_name] = {
                'Level': 0,
                'Index': upgrade_index,
                'Image': f"vault-upgrade-{upgrade_index}",
                'Cost Base': safer_convert(upgrade_values_list[1], 0),
                'Cost Increment': float(upgrade_values_list[2]),
                # 'Placeholder3': upgrade_values_list[3],
                'Max Level': int(upgrade_values_list[4]),
                'Value Per Level': int(upgrade_values_list[5]),
                'Unlock Requirement': int(upgrade_values_list[6]),
                # 'Placeholder7': upgrade_values_list[7],
                # 'Placeholder8': upgrade_values_list[8],
                'Description': f"{upgrade_values_list[9].replace('_', ' ')}{secondary_description}",
                'Scaling Value': upgrade_index not in vault_dont_scale,
                'Vault Section': vault_section
            }
    #logger.debug(account.vault)

    #Sum total upgrades
    account.vault['Total Upgrades'] = sum([v['Level'] for v in account.vault['Upgrades'].values()])
    for upgrade_name in account.vault['Upgrades']:
        account.vault['Upgrades'][upgrade_name]['Unlocked'] = account.vault['Total Upgrades'] >= account.vault['Upgrades'][upgrade_name]['Unlock Requirement']

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

def _parse_w1_forge(account):
    account.forge_upgrades = copy.deepcopy(forge_upgrades_dict)
    raw_forge_upgrades = account.raw_data.get("ForgeLV", [])
    for upgradeIndex, upgrade in enumerate(raw_forge_upgrades):
        try:
            account.forge_upgrades[upgradeIndex]["Purchased"] = upgrade
        except Exception as e:
            logger.warning(f"Forge Upgrade Parse error at upgradeIndex {upgradeIndex}: {e}. Defaulting to 0")
            continue  # Already defaulted to 0 in Consts

def _parse_w1_bribes(account):
    account.bribes = {}
    raw_bribes_list = safe_loads(account.raw_data.get("BribeStatus", []))
    overall_bribe_index = 0
    for bribeSet in bribes_dict:
        account.bribes[bribeSet] = {}
        for bribeIndex, bribeName in enumerate(bribes_dict[bribeSet]):
            try:
                account.bribes[bribeSet][bribeName] = safer_convert(raw_bribes_list[overall_bribe_index], -1)
            except Exception as e:
                logger.warning(f"Bribes Parse error at {bribeSet} {bribeName}: {e}. Defaulting to -1")
                account.bribes[bribeSet][bribeName] = -1  # -1 means unavailable for purchase, 0 means available, and 1 means purchased
            overall_bribe_index += 1

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

def _parse_w1_owl(account):
    if 265 not in account.raw_optlacc_dict:
        logger.warning(f"Owl data not present{', as expected' if account.version < 217 else ''}.")
    account.owl = {
        'Discovered': safer_get(account.raw_optlacc_dict, 265, False),
        'FeatherGeneration': safer_get(account.raw_optlacc_dict, 254, 0),
        'BonusesOfOrion': safer_get(account.raw_optlacc_dict, 255, 0),
        'FeatherRestarts': safer_get(account.raw_optlacc_dict, 258, 0),
        'MegaFeathersOwned': safer_get(account.raw_optlacc_dict, 262, 0)
    }

def _parse_w1_statues(account):
    account.statues = {}
    account.maxed_statues = 0
    # "StuG": "[2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0]",
    raw_statue_type_list = safe_loads(account.raw_data.get("StuG", []))
    if len(raw_statue_type_list) != statue_count:
        raw_statue_type_list += [0] * (statue_count - len(raw_statue_type_list))
    account.onyx_statues_unlocked = (
            max(raw_statue_type_list, default=0) >= get_statue_type_index_from_name('Onyx')
            or parse_number(safer_get(account.raw_optlacc_dict, 69, 0), 0) >= 2
    )
    account.zenith_statues_unlocked = (
            max(raw_statue_type_list, default=0) >= get_statue_type_index_from_name('Zenith')
            or parse_number(safer_get(account.raw_optlacc_dict, 69, 0), 0) >= 3
    )
    statue_levels = [0] * statue_count

    # Find the maximum value across all characters. Only matters while Normal, since Gold shares across all characters
    for char in account.safe_characters:
        try:
            char_statues = safe_loads(account.raw_data.get(f"StatueLevels_{char.character_index}"))
            for statueIndex, statueDetails in enumerate(char_statues):
                try:
                    if statueDetails[0] > statue_levels[statueIndex]:
                        statue_levels[statueIndex] = statueDetails[0]
                except IndexError:
                    logger.warning(f"statue_levels list does not contain index {statueIndex}, meaning consts_w1.statues_dict is missing a statue!")
        except Exception as e:
            logger.warning(f"Per-Character statue level Parse error for Character{char.character_index}: {e}. Skipping them.")
            continue

    for statueIndex, statueDetails in statues_dict.items():
        try:
            account.statues[statueDetails['Name']] = {
                'Level': statue_levels[statueIndex],
                'Type': statue_type_dict.get(raw_statue_type_list[statueIndex], 'UnknownType'),  # Description: Normal, Gold, Onyx, Zenith
                'TypeNumber': raw_statue_type_list[statueIndex],  # Integer: 0-3
                'ItemName': statueDetails['ItemName'],
                'Effect': statueDetails['Effect'],
                'BaseValue': statueDetails['BaseValue'],
                'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statue_multi()
                'Farmer': statueDetails['Farmer'],
                'Resource': statueDetails['Resource'],
            }
        except Exception as e:
            logger.warning(f"Statue Parse error: {e}. Defaulting to level 0")
            account.statues[statueDetails['Name']] = {
                'Level': 0,
                'Type': statue_type_dict.get(raw_statue_type_list[statueIndex], 'UnknownType'),  # Description: Normal, Gold, Onyx, Zenith
                'TypeNumber': 0,
                'ItemName': statueDetails['ItemName'],
                'Effect': statueDetails['Effect'],
                'BaseValue': statueDetails['BaseValue'],
                'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statues()
                'Farmer': statueDetails['Farmer'],
                'Resource': statueDetails['Resource'],
            }
        account.statues[statueDetails['Name']]['Image'] = f"{account.statues[statueDetails['Name']]['Type']}-{statueDetails['Name']}".lower().replace(' ', '-')
        if account.statues[statueDetails['Name']]['TypeNumber'] >= statue_type_count:
            account.maxed_statues += 1


def _parse_w1_minigames(account):
    _parse_w1_basketball(account)
    _parse_w1_darts(account)

def _parse_w1_basketball(account):
    # skip the first item in the array because that's just the default shop text, not an upgrade description
    for index, description in enumerate(basketball_upgrade_descriptions[1:]):
        account.basketball['Upgrades'][index] = {
            'Level': safer_get(account.raw_optlacc_dict, 419 + index, 0),
            'Description': description.replace('_', ' '),
            'Image': f'basketball-upgrade-{index + 1}'
        }

def _parse_w1_darts(account):
    # skip the first item in the array because that's just the default shop text, not an upgrade description
    for index, description in enumerate(darts_upgrade_descriptions[1:]):
        account.darts['Upgrades'][index] = {
            'Level': safer_get(account.raw_optlacc_dict, 435 + index, 0),
            'Description': description.replace('_', ' '),
            'Image': f'darts-upgrade-{index + 1}'
        }

def _parse_w2(account):
    _parse_w2_vials(account)
    _parse_w2_cauldrons(account)
    _parse_w2_bubbles(account)
    _parse_w2_p2w(account)
    _parse_w2_postOffice(account)
    _parse_w2_arcade(account)
    _parse_w2_ballot(account)
    _parse_w2_obols(account)
    _parse_w2_islands(account)
    _parse_w2_killroy(account)
    _parse_w2_weekly_boss(account)

def _parse_w2_vials(account):
    account.alchemy_vials = {}
    raw_alchemy_vials = safe_loads(account.raw_data.get('CauldronInfo', [0, 0, 0, 0, {}])[4])
    if 'length' in raw_alchemy_vials:
        del raw_alchemy_vials['length']
    if len(raw_alchemy_vials) < max_index_of_vials:
        logger.warning(f'Vials list shorter than expected by {max_index_of_vials - len(raw_alchemy_vials)}')

    #Normalize Vial data
    cleaner_alchemy_vials = {}
    for key, value in raw_alchemy_vials.items():
        try:
            # Attempts to normalize the data, which may otherwise have strings or floats as keys and values
            cleaner_alchemy_vials[int(key)] = int(value)
        except:
            logger.warning(f'Unable to normalize Vials level to int: {type(value)}: {value}. Replacing with 0.')
            cleaner_alchemy_vials[int(key)] = 0

    for vial_index, vial_values in vials_dict.items():
        try:
            account.alchemy_vials[getReadableVialNames(vial_index)] = {
                'Level': cleaner_alchemy_vials[vial_index],
                'BaseValue': lava_func(
                    vials_dict[vial_index]['funcType'],
                    cleaner_alchemy_vials[vial_index],
                    vials_dict[vial_index]['x1'],
                    vials_dict[vial_index]['x2'],
                ),
                'Material': vials_dict[vial_index]['Material'],
                'Image': getItemDisplayName(vials_dict[vial_index]['Material'])
            }
        except Exception as e:
            logger.warning(f"Alchemy Vial Parse error at vial_index {vial_index}: {e}. Defaulting to level 0")
            account.alchemy_vials[getReadableVialNames(vial_index)] = {
                'Level': 0,
                'BaseValue': 0,
                'Material': vials_dict[vial_index]['Material'],
                'Image': getItemDisplayName(vials_dict[vial_index]['Material'])
            }

    account.maxed_vials = sum([details['Level'] >= max_vial_level for name, details in account.alchemy_vials.items()])

def _parse_w2_cauldrons(account):
    raw_cauldron_upgrades = account.raw_data.get('CauldUpgLVs', [])
    account.alchemy_cauldrons = {
        'OrangeUnlocked': 0,
        'GreenUnlocked': 0,
        'PurpleUnlocked': 0,
        'YellowUnlocked': 0,
        'TotalUnlocked': 0,
    }
    try:
        account.alchemy_cauldrons["OrangeBoosts"] = [
            safer_convert(raw_cauldron_upgrades[0], 0),
            safer_convert(raw_cauldron_upgrades[1], 0),
            safer_convert(raw_cauldron_upgrades[2], 0),
            safer_convert(raw_cauldron_upgrades[3], 0),
        ]
        account.alchemy_cauldrons["GreenBoosts"] = [
            safer_convert(raw_cauldron_upgrades[4], 0),
            safer_convert(raw_cauldron_upgrades[5], 0),
            safer_convert(raw_cauldron_upgrades[6], 0),
            safer_convert(raw_cauldron_upgrades[7], 0),
        ]
        account.alchemy_cauldrons["PurpleBoosts"] = [
            safer_convert(raw_cauldron_upgrades[8], 0),
            safer_convert(raw_cauldron_upgrades[9], 0),
            safer_convert(raw_cauldron_upgrades[10], 0),
            safer_convert(raw_cauldron_upgrades[11], 0),
        ]
        account.alchemy_cauldrons["PurpleBoosts"] = [
            safer_convert(raw_cauldron_upgrades[12], 0),
            safer_convert(raw_cauldron_upgrades[13], 0),
            safer_convert(raw_cauldron_upgrades[14], 0),
            safer_convert(raw_cauldron_upgrades[15], 0),
        ]
    except Exception as e:
        logger.warning(f"Alchemy bubble cauldron Boosts Parse error: {e}. Defaulting to 0s")
        account.alchemy_cauldrons["OrangeBoosts"] = [0, 0, 0, 0]
        account.alchemy_cauldrons["GreenBoosts"] = [0, 0, 0, 0]
        account.alchemy_cauldrons["PurpleBoosts"] = [0, 0, 0, 0]
        account.alchemy_cauldrons["YellowBoosts"] = [0, 0, 0, 0]
    try:
        account.alchemy_cauldrons["WaterDroplets"] = [safer_convert(raw_cauldron_upgrades[18], 0), safer_convert(raw_cauldron_upgrades[19], 0)]
        account.alchemy_cauldrons["LiquidNitrogen"] = [safer_convert(raw_cauldron_upgrades[22], 0), safer_convert(raw_cauldron_upgrades[23], 0)]
        account.alchemy_cauldrons["TrenchSeawater"] = [safer_convert(raw_cauldron_upgrades[26], 0), safer_convert(raw_cauldron_upgrades[27], 0)]
        account.alchemy_cauldrons["ToxicMercury"] = [safer_convert(raw_cauldron_upgrades[30], 0), safer_convert(raw_cauldron_upgrades[31], 0)]
    except Exception as e:
        logger.warning(f"Alchemy Water Cauldron decants Parse error: {e}. Defaulting to 0s")
        account.alchemy_cauldrons["WaterDroplets"] = [0, 0]
        account.alchemy_cauldrons["LiquidNitrogen"] = [0, 0]
        account.alchemy_cauldrons["TrenchSeawater"] = [0, 0]
        account.alchemy_cauldrons["ToxicMercury"] = [0, 0]

def _parse_w2_bubbles(account):
    account.alchemy_bubbles = {}

    try:
        all_raw_bubbles = [
            {int(k):safer_convert(v, 0) for k,v in account.raw_data["CauldronInfo"][0].items() if k != 'length'},
            {int(k):safer_convert(v, 0) for k,v in account.raw_data["CauldronInfo"][1].items() if k != 'length'},
            {int(k):safer_convert(v, 0) for k,v in account.raw_data["CauldronInfo"][2].items() if k != 'length'},
            {int(k):safer_convert(v, 0) for k,v in account.raw_data["CauldronInfo"][3].items() if k != 'length'},
        ]
    except:
        all_raw_bubbles = [
            {k:0 for k in range(0, max_implemented_bubble_index + 1)},  #+1 to compensate for range() stopping before max
            {k:0 for k in range(0, max_implemented_bubble_index + 1)},
            {k:0 for k in range(0, max_implemented_bubble_index + 1)},
            {k:0 for k in range(0, max_implemented_bubble_index + 1)},
        ]

    account.alchemy_cauldrons['OrangeUnlocked'] = sum([1 for v in all_raw_bubbles[0].values() if v > 0])
    account.alchemy_cauldrons['GreenUnlocked'] = sum([1 for v in all_raw_bubbles[1].values() if v > 0])
    account.alchemy_cauldrons['PurpleUnlocked'] = sum([1 for v in all_raw_bubbles[2].values() if v > 0])
    account.alchemy_cauldrons['YellowUnlocked'] = sum([1 for v in all_raw_bubbles[3].values() if v > 0])
    account.alchemy_cauldrons['TotalUnlocked'] = (
        account.alchemy_cauldrons['OrangeUnlocked']
        + account.alchemy_cauldrons['GreenUnlocked']
        + account.alchemy_cauldrons['PurpleUnlocked']
        + account.alchemy_cauldrons['YellowUnlocked']
    )

    for cauldronIndex in bubbles_dict:
        for bubbleIndex in bubbles_dict[cauldronIndex]:
            if bubbleIndex <= max_implemented_bubble_index:  #Don't waste time calculating unimplemented bubbles
                try:
                    account.alchemy_bubbles[bubbles_dict[cauldronIndex][bubbleIndex]['Name']] = {
                        'CauldronIndex': cauldronIndex,
                        'BubbleIndex': bubbleIndex,
                        'Level': all_raw_bubbles[cauldronIndex][bubbleIndex],
                        'BaseValue': lava_func(
                            bubbles_dict[cauldronIndex][bubbleIndex]['funcType'],
                            all_raw_bubbles[cauldronIndex][bubbleIndex],
                            bubbles_dict[cauldronIndex][bubbleIndex]['x1'],
                            bubbles_dict[cauldronIndex][bubbleIndex]['x2']),
                        'Material': getItemDisplayName(bubbles_dict[cauldronIndex][bubbleIndex]['Material'])
                    }
                except:
                    account.alchemy_bubbles[bubbles_dict[cauldronIndex][bubbleIndex]['Name']] = {
                        'CauldronIndex': cauldronIndex,
                        'BubbleIndex': bubbleIndex,
                        'Level': 0,
                        'BaseValue': 0.0,
                        'Material': getItemDisplayName(bubbles_dict[cauldronIndex][bubbleIndex]['Material'])
                    }

def _parse_w2_p2w(account):
    account.alchemy_p2w = {
        'Sigils': copy.deepcopy(sigils_dict)
    }
    raw_p2w_list = safe_loads(account.raw_data.get('CauldronP2W', []))
    for subElementIndex, subElementValue in enumerate(raw_p2w_list):
        if not isinstance(subElementValue, list):
            raw_p2w_list[subElementIndex] = [subElementValue]
    try:
        account.alchemy_p2w['Cauldrons'] = raw_p2w_list[0]
    except:
        account.alchemy_p2w['Cauldrons'] = [0] * 12
    try:
        account.alchemy_p2w['Liquids'] = raw_p2w_list[1]
    except:
        account.alchemy_p2w['Liquids'] = [0] * 8
    try:
        account.alchemy_p2w['Vials'] = raw_p2w_list[2]
    except:
        account.alchemy_p2w['Vials'] = [0] * 2
    try:
        account.alchemy_p2w['Player'] = raw_p2w_list[3]
    except:
        account.alchemy_p2w['Player'] = [0] * 2

    for sigilName in account.alchemy_p2w['Sigils']:
        try:
            account.alchemy_p2w['Sigils'][sigilName]['PlayerHours'] = float(raw_p2w_list[4][account.alchemy_p2w["Sigils"][sigilName]["Index"]])
            account.alchemy_p2w['Sigils'][sigilName]['Level'] = raw_p2w_list[4][account.alchemy_p2w["Sigils"][sigilName]["Index"] + 1] + 1
        except:
            pass  # Already defaulted to 0s in consts.sigils_dict
        
def _parse_w2_postOffice(account):
    account.postOffice = {
        'Completing Orders': safer_convert(account.raw_data.get("CYDeliveryBoxComplete", 0), 0),
        'Streak Bonuses': safer_convert(account.raw_data.get("CYDeliveryBoxStreak", 0), 0),
        'Miscellaneous': safer_convert(account.raw_data.get("CYDeliveryBoxMisc", 0), 0),
        'Upgrade Vault': safer_convert(account.raw_optlacc_dict.get(347, 0), 0)
    }

def _parse_w2_arcade(account):
    account.arcade_currency = {
        'Balls': safer_get(account.raw_optlacc_dict, 74, 0),
        'Gold Balls': safer_get(account.raw_optlacc_dict, 75, 0),
        'Cosmic Balls': safer_get(account.raw_optlacc_dict, 324, 0),
    }

    account.arcade = {}
    raw_arcade_upgrades = safe_loads(account.raw_data.get('ArcadeUpg', []))
    for upgrade_index, upgrade_details in arcade_bonuses.items():
        try:
            account.arcade[upgrade_index] = {
                'Level': raw_arcade_upgrades[upgrade_index],
                'Value': lava_func(
                    upgrade_details['funcType'],
                    min(arcade_max_level, raw_arcade_upgrades[upgrade_index]),
                    upgrade_details['x1'],
                    upgrade_details['x2']
                ),
                'MaxValue':(
                    2  #Cosmic
                    * 2  #Reindeer Companion
                    * lava_func(
                        upgrade_details['funcType'],
                        arcade_max_level,
                        upgrade_details['x1'],
                        upgrade_details['x2']
                    )
                ),
                'Cosmic': raw_arcade_upgrades[upgrade_index] >= arcade_max_level,
                'Material': (
                    '' if raw_arcade_upgrades[upgrade_index] == 101
                    else 'arcade-cosmic-ball' if raw_arcade_upgrades[upgrade_index] == 100
                    else 'arcade-gold-ball'
                ),
                'Image': f'arcade-bonus-{upgrade_index}',
                'Display Type': upgrade_details['displayType'],
                'Stat': upgrade_details['Stat']
            }
        except Exception as e:
            logger.warning(f"Arcade Gold Ball Bonus Parse error at upgrade_index {upgrade_index}: {e}. Defaulting to 0")
            account.arcade[upgrade_index] = {
                'Level': 0,
                'Value': lava_func(
                    upgrade_details['funcType'],
                    0,
                    upgrade_details['x1'],
                    upgrade_details['x2']
                ),
                'MaxValue':(
                    2  #Cosmic
                    * 2  #Reindeer Companion
                    * lava_func(
                        upgrade_details['funcType'],
                        arcade_max_level,
                        upgrade_details['x1'],
                        upgrade_details['x2']
                    )
                ),
                'Cosmic': False,
                'Material': 'arcade-gold-ball',
                'Image': f'arcade-bonus-{upgrade_index}',
                'Display Type': upgrade_details['displayType'],
                'Stat': upgrade_details['Stat']
            }

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

def _parse_w2_obols(account):
    # Please send help, I hate Obols so much
    account.obols = {
        'Unknown': {
            'Unknown': {'Total': 0},
            'Circle': {'Total': 0},
            'Square': {'Total': 0},
            'Hexagon': {'Total': 0},
            'Sparkle': {'Total': 0},
        },
        'Drop Rate': {
            'Circle': {'Total': 0},
            'Square': {'Total': 0},
            'Hexagon': {'Total': 0},
            'Sparkle': {'Total': 0},
        },
        'Choppin': {
            'Circle': {'Total': 0},
            'Square': {'Total': 0},
            'Hexagon': {'Total': 0},
            'Sparkle': {'Total': 0},
        },
        'Card Drop Chance': {
            'Circle': {'Total': 0},
            'Square': {'Total': 0},
            'Hexagon': {'Total': 0},
            'Sparkle': {'Total': 0},
        },
    }
    raw_owned_obols = []
    for jsonkey in [
        'ObolEqO1', 'ObolEqO2', 'ObolEqO0_0', 'ObolEqO0_1', 'ObolEqO0_2', 'ObolEqO0_3', 'ObolEqO0_4',
        'ObolEqO0_5', 'ObolEqO0_6', 'ObolEqO0_7', 'ObolEqO0_8', 'ObolEqO0_9'
    ]:
        raw_owned_obols += safe_loads(account.raw_data.get(jsonkey, []))
    raw_obol_inventory_list = safe_loads(account.raw_data.get("ObolInvOr"))
    for subdict in raw_obol_inventory_list:
        raw_owned_obols += subdict.values()
    for obol in raw_owned_obols:
        if obol not in ignorable_obols_list:
            obolBonusType = obols_dict.get(obol, {}).get('Bonus', 'Unknown')
            obolShape = obols_dict.get(obol, {}).get('Shape', 'Unknown')
            account.obols[obolBonusType][obolShape]['Total'] += 1
            if obol not in account.obols[obolBonusType][obolShape]:
                account.obols[obolBonusType][obolShape][obol] = {'Count': 1}
            else:
                account.obols[obolBonusType][obolShape][obol]['Count'] += 1
    
    raw_family_obols_list = safe_loads(account.raw_data.get('ObolEqO1'))
    raw_family_obols_upgrades = safe_loads(account.raw_data.get('ObolEqMAPz1'))
    account.obols['BonusTotals'] = get_obol_totals(raw_family_obols_list, raw_family_obols_upgrades)

def _parse_w2_islands(account):
    account.islands = {
        'Trash': safer_get(account.raw_optlacc_dict, 161, 0),  # [161]: 362.202271805249
        'Bottles': safer_get(account.raw_optlacc_dict, 162, 0),  # [162]: 106.90044163281846
    }

    raw_islands_list = list(safer_get(account.raw_optlacc_dict, 169, ''))  # [169]: "_dcabe" or could be int 0 for whatever reason...
    for islandName, islandData in islands_dict.items():
        account.islands[islandName] = {
            'Unlocked': islandData['Code'] in raw_islands_list,
            'Description': islandData['Description']
        }

    account.nothing_hours = safer_get(account.raw_optlacc_dict, 184, 0)

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
    _parse_w3_library(account)
    _parse_w3_deathnote(account)
    _parse_w3_equinox_dreams(account)
    _parse_w3_equinox_bonuses(account)
    _parse_w3_shrines(account)
    _parse_w3_atom_collider(account)
    _parse_w3_prayers(account)
    _parse_w3_saltlick(account)
    _parse_w3_armor_sets(account)
    _parse_w3_worship(account)

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

def _parse_w3_library(account):
    account.library = {
        'BooksReady': safer_get(account.raw_optlacc_dict, 55, 0)
    }

def _parse_w3_deathnote(account):
    account.apocCharactersIndexList = [c.character_index for c in account.barbs]
    account.bbCharactersIndexList = [c.character_index for c in account.bbs]
    account.apocalypse_character_index = _parse_w3_apocalypse_BBIndex(account)
    account.rift_meowed = _parse_w3_deathnote_rift_meowed(account)
    _parse_w3_deathnote_kills(account)
    _parse_w3_deathnote_miniboss_kills(account)

def _parse_w3_apocalypse_BBIndex(account):
    if len(account.bbCharactersIndexList) == 1:
        return account.bbCharactersIndexList[0]
    elif len(account.bbCharactersIndexList) >= 2:
        return account.bbCharactersIndexList[1]
    else:
        return None

def _parse_w3_deathnote_rift_meowed(account):
    if account.apocalypse_character_index is not None:
        riftPresent = False
        for remainingMap in account.all_characters[account.apocalypse_character_index].apoc_dict['MEOW']['Medium Extras']:
            if remainingMap[0] == 'The Rift':
                riftPresent = True
                break
        if not riftPresent:
            account.rift_meowed = True
    else:
        riftPresent = True
    return not riftPresent

def _parse_w3_deathnote_kills(account):
    # total up all kills across characters
    for characterIndex, characterData in enumerate(account.all_characters):
        characterKillsDict = characterData.kill_dict

        # If the character's subclass is Barbarian, add their special Apoc-Only kills to EnemyMap's zow_dict
        if characterIndex in account.apocCharactersIndexList:
            for worldIndex in range(0, len(apocable_map_index_dict)):
                for mapIndex in apocable_map_index_dict[worldIndex]:
                    try:
                        account.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, characterKillsDict.get(mapIndex, [0])[0])
                    except:
                        account.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, 0)

        # Regardless of class, for each map within each world, add this player's kills to EnemyMap's kill_count
        for worldIndex in range(1, len(apocable_map_index_dict)):
            for mapIndex in apocable_map_index_dict[worldIndex]:
                try:
                    account.enemy_maps[worldIndex][mapIndex].addRawKLA(characterKillsDict.get(mapIndex, [0])[0])
                except:
                    account.enemy_maps[worldIndex][mapIndex].addRawKLA(0)

    # Have each EnemyMap calculate its Skull Value, Name, Count to Next, and Percent to Next now that all kills are totaled
    # Barbarian Only in worldIndex 0
    for worldIndex in range(1, len(account.enemy_maps)):
        for enemy_map in account.enemy_maps[worldIndex]:
            account.enemy_maps[worldIndex][enemy_map].generateDNSkull()
        # After each Map in that World has its Skull Info, create the corresponding EnemyWorld
        account.enemy_worlds[worldIndex] = EnemyWorld(worldIndex, account.enemy_maps[worldIndex])

    # Barbarian Only in 0
    for barbCharacterIndex in account.apocCharactersIndexList:
        for worldIndex in range(0, len(account.enemy_maps)):
            for enemy_map in account.enemy_maps[worldIndex]:
                if barbCharacterIndex in account.enemy_maps[worldIndex][enemy_map].zow_dict:
                    kill_count = account.enemy_maps[worldIndex][enemy_map].zow_dict[barbCharacterIndex]
                    for apoc_index, apoc_amount in enumerate(apoc_amounts_list):
                        if (
                            kill_count < apoc_amount  #normal trigger for not meeting the apocalypse amount
                            or apoc_index+1 == len(apoc_amounts_list)  #secondary trigger to make sure every map shows up in Unfiltered
                        ):
                            # characterDict[barbCharacterIndex].apoc_dict[apoc_names_list[apoc_index]][enemyMaps[worldIndex][enemy_map].zow_rating].append([
                            account.all_characters[barbCharacterIndex].addUnmetApoc(
                                apoc_names_list[apoc_index],
                                account.enemy_maps[worldIndex][enemy_map].getRating(apoc_names_list[apoc_index]),
                                [
                                    account.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                    apoc_amount - kill_count if apoc_index < len(apoc_amounts_list) - 1 else kill_count,  # kills short of Apoc stack
                                    # Note: The final entry in apoc_amounts_list is a placeholder used for the unfiltered display with no goal
                                    min(99, floor(round((kill_count / apoc_amount) * 100))),  # percent toward Apoc stack
                                    account.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                    worldIndex,
                                    account.enemy_maps[worldIndex][enemy_map].monster_name
                                ]
                            )
                        else:
                            account.all_characters[barbCharacterIndex].increaseApocTotal(apoc_names_list[apoc_index])
                else:
                    # This condition can be hit when reviewing data from before a World release
                    # For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                    # If you get this right after a new world, check that the new world and map indexes are added in consts_w3.apocable_map_index_dict
                    logger.debug(f"barbCharacterIndex {barbCharacterIndex} not in account.enemy_maps[{worldIndex}][{enemy_map}].zow_dict")
                    for apoc_index, apoc_amount in enumerate(apoc_amounts_list):
                        account.all_characters[barbCharacterIndex].addUnmetApoc(
                            apoc_names_list[apoc_index],
                            account.enemy_maps[worldIndex][enemy_map].getRating(apoc_names_list[apoc_index]),
                            [
                                account.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                apoc_amounts_list[apoc_index],  # kills short of zow/chow/meow
                                0,  # percent toward zow/chow/meow
                                account.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                worldIndex,
                                account.enemy_maps[worldIndex][enemy_map].monster_name
                            ]
                        )
        # Sort them
        account.all_characters[barbCharacterIndex].sortApocByProgression()

def _parse_w3_deathnote_miniboss_kills(account):
    account.miniboss_deathnote = {
        'Minis': {}
    }

    raw_ninja = safe_loads(account.raw_data.get('Ninja', []))
    raw_mb_kills = raw_ninja[105] if len(raw_ninja) >= 106 else [0] * len(dn_miniboss_names)
    for mb_index, mb_name in enumerate(dn_miniboss_names):
        try:
            kill_count = safer_convert(raw_mb_kills[mb_index] if len(raw_mb_kills) >= mb_index+1 else 0, 0)
        except:
            logger.warning(f"Unable to parse Miniboss Deathnote killcount for {mb_name} in index {mb_index}: {raw_mb_kills}. Setting to the default of 0.")
        skull_number = 0
        kills_to_next_skull = 0
        percent_to_next_skull = 0.0
        for requirement_index, skull_requirement in enumerate(dn_miniboss_skull_requirement_list):
            if kill_count >= skull_requirement:
                skull_number = requirement_index
            elif kill_count < skull_requirement and kills_to_next_skull == 0:
                kills_to_next_skull = skull_requirement - kill_count
                percent_to_next_skull = 100 * (kills_to_next_skull / skull_requirement)
        skull_mk_value = dn_skull_value_list[skull_number] if len(dn_skull_value_list) >= skull_number else 0
        skull_name = getSkullNames(skull_mk_value)
        account.miniboss_deathnote['Minis'][mb_name] = {
            'Kills': kill_count,
            'Skull Name': skull_name,
            'Skull MK': skull_mk_value,
            'Progress Percent': percent_to_next_skull
        }
    # Sum up all the MK value of the individual skulls
    account.miniboss_deathnote['TotalMK'] = sum(mb_values['Skull MK'] for mb_values in account.miniboss_deathnote['Minis'].values())

def _parse_w3_equinox_dreams(account):
    account.equinox_unlocked = account.achievements['Equinox Visitor']['Complete']
    account.equinox_dreams = [True]  # d_0 in the code is Dream 1. By padding the first slot, we can get Dream 1 by that same index: equinox_dreams[1]
    raw_equinox_dreams = safe_loads(account.raw_data.get("WeeklyBoss", {}))
    account.equinox_dreams += [
        float(raw_equinox_dreams.get(f'd_{i}', 0)) == -1
        for i in range(max_implemented_dreams)
    ]
    account.total_dreams_completed = sum(account.equinox_dreams) - 1  # Remove the placeholder in 0th index
    account.total_equinox_bonuses_unlocked = 0
    account.remaining_equinox_dreams_unlocking_new_bonuses = []
    for dreamNumber in dreams_that_unlock_new_bonuses:
        if account.equinox_dreams[dreamNumber] == True:
            account.total_equinox_bonuses_unlocked += 1
        else:
            account.remaining_equinox_dreams_unlocking_new_bonuses.append(dreamNumber)

def _parse_w3_equinox_bonuses(account):
    account.equinox_bonuses = {}
    raw_equinox_bonuses = safe_loads(account.raw_data.get("Dream", [0] * 30))
    for bonusIndex, bonusValueDict in equinox_bonuses_dict.items():
        upgradeName = bonusValueDict['Name']
        account.equinox_bonuses[upgradeName] = {
            'PlayerMaxLevel': 0,  # This will get updated in the next Try block. Do not fret, dear reader.
            'Category': bonusValueDict['Category'],
            'Unlocked': account.total_equinox_bonuses_unlocked >= bonusIndex - 2,
            'FinalMaxLevel': bonusValueDict['FinalMaxLevel'],
            'RemainingUpgrades': [],
            'SummoningExpands': bonusValueDict['SummoningExpands']
        }
        try:
            account.equinox_bonuses[upgradeName]['CurrentLevel'] = int(raw_equinox_bonuses[bonusIndex])
        except:
            account.equinox_bonuses[upgradeName]['CurrentLevel'] = 0
        if account.equinox_bonuses[upgradeName]['Unlocked']:
            account.equinox_bonuses[upgradeName]['PlayerMaxLevel'] = bonusValueDict['BaseLevel']
            for dreamIndex, bonusMaxLevelIncrease in bonusValueDict['MaxLevelIncreases'].items():
                if account.equinox_dreams[dreamIndex]:
                    account.equinox_bonuses[upgradeName]['PlayerMaxLevel'] += bonusMaxLevelIncrease
                else:
                    account.equinox_bonuses[upgradeName]['RemainingUpgrades'].append(dreamIndex)

def _parse_w3_shrines(account):
    account.shrines = {}
    raw_shrines_list = safe_loads(account.raw_data.get("Shrine", []))
    for shrineIndex, shrineName in enumerate(buildings_shrines):
        try:
            account.shrines[shrineName] = {
                "MapIndex": int(raw_shrines_list[shrineIndex][0]),
                1: int(raw_shrines_list[shrineIndex][1]),
                2: int(raw_shrines_list[shrineIndex][2]),
                "Level": int(raw_shrines_list[shrineIndex][3]),
                "Hours": float(raw_shrines_list[shrineIndex][4]),
                5: int(raw_shrines_list[shrineIndex][5]),
                "BaseValue": (
                    buildings_dict[18 + shrineIndex]['ValueBase']
                    + (buildings_dict[18 + shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                    if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                ),
                "Value": (
                    buildings_dict[18 + shrineIndex]['ValueBase']
                    + (buildings_dict[18 + shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                    if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                ),
                'Image': buildings_dict[18 + shrineIndex]['Image']
            }
        except:
            account.shrines[shrineName] = {
                "MapIndex": 0,
                1: 0,
                2: 0,
                "Level": 0,
                "Hours": 0.0,
                5: 0,
                "BaseValue": 0,
                "Value": 0,
                'Image': buildings_dict[18 + shrineIndex]['Image']
            }

def _parse_w3_atom_collider(account):
    account.atom_collider = {
        'OnOffStatus': safer_get(account.raw_optlacc_dict, 132, False),
        'Magnesium Days': safer_get(account.raw_optlacc_dict, 363, 0)
    }
    try:
        account.atom_collider['StorageLimit'] = collider_storage_limit_list[safer_get(account.raw_optlacc_dict, 133, -1)]
    except:
        account.atom_collider['StorageLimit'] = collider_storage_limit_list[-1]
    try:
        account.atom_collider['Particles'] = account.raw_data.get("Divinity", {})[39]
    except:
        account.atom_collider['Particles'] = "Unknown"  # 0.0

    _parse_w3_atoms(account)

def _parse_w3_atoms(account):
    account.atom_collider['Atoms'] = {}
    raw_atoms_list = safe_loads(account.raw_data.get("Atoms", []))
    for atomIndex, atomInfoList in enumerate(atoms_list):
        try:
            account.atom_collider['Atoms'][atomInfoList[0]] = {
                'Level': int(raw_atoms_list[atomIndex]),
                'MaxLevel': 20,
                'AtomInfo1': atomInfoList[1],
                'AtomInfo2': atomInfoList[2],
                'AtomInfo3': atomInfoList[3],
                'Value per Level': atomInfoList[4],
                'Description': atomInfoList[5],
                'BaseCostToUpgrade': 0,
                'DiscountedCostToUpgrade': 0,
                'BaseCostToMax': 0,
                'DiscountedCostToMax': 0
            }
        except:
            account.atom_collider['Atoms'][atomInfoList[0]] = {
                'Level': 0,
                'MaxLevel': 20,
                'AtomInfo1': atomInfoList[1],
                'AtomInfo2': atomInfoList[2],
                'AtomInfo3': atomInfoList[3],
                'Value per Level': atomInfoList[4],
                'Description': atomInfoList[5],
                'BaseCostToUpgrade': 0,
                'DiscountedCostToUpgrade': 0,
                'BaseCostToMax': 0,
                'DiscountedCostToMax': 0
            }

def _parse_w3_prayers(account):
    account.prayers = {}
    raw_prayers_list = safe_loads(account.raw_data.get("PrayOwned", []))
    for prayerIndex, prayerValuesDict in prayers_dict.items():
        account.prayers[prayerValuesDict['Name']] = {
            'DisplayName': prayerValuesDict['Display'],
            'Material': prayerValuesDict['Material'],
            'Level': 0,
            'BonusValue': 0,
            'BonusString': f"Level at least once to receive the bonus!",
            'CurseValue': 0,
            'CurseString': f"Level at least once to receive the curse!"
        }
        try:
            account.prayers[prayerValuesDict['Name']]['Level'] = int(raw_prayers_list[prayerIndex])
            account.prayers[prayerValuesDict['Name']]['BonusValue'] = lava_func(
                prayerValuesDict['bonus_funcType'],
                account.prayers[prayerValuesDict['Name']]['Level'],
                prayerValuesDict['bonus_x1'],
                prayerValuesDict['bonus_x2']) if account.prayers[prayerValuesDict['Name']]['Level'] > 0 else 0
            account.prayers[prayerValuesDict['Name']]['BonusString'] = (
                f"{prayerValuesDict['bonus_pre']}"
                f"{account.prayers[prayerValuesDict['Name']]['BonusValue']}"
                f"{prayerValuesDict['bonus_post']}"
                f" {prayerValuesDict['bonus_stat']}"
            )
            account.prayers[prayerValuesDict['Name']]['CurseValue'] = lava_func(
                prayerValuesDict['curse_funcType'],
                account.prayers[prayerValuesDict['Name']]['Level'],
                prayerValuesDict['curse_x1'],
                prayerValuesDict['curse_x2']) if account.prayers[prayerValuesDict['Name']]['Level'] > 0 else 0
            account.prayers[prayerValuesDict['Name']]['CurseString'] = (
                f"{prayerValuesDict['curse_pre']}"
                f"{account.prayers[prayerValuesDict['Name']]['CurseValue']}"
                f"{prayerValuesDict['curse_post']}"
                f" {prayerValuesDict['curse_stat']}"
            )
        except:
            pass

def _parse_w3_saltlick(account):
    account.saltlick = {}
    raw_saltlick_list = safe_loads(account.raw_data.get("SaltLick"))
    for saltlickIndex, saltlickName in enumerate(salt_lick_list):
        try:
            account.saltlick[saltlickName] = int(raw_saltlick_list[saltlickIndex])
        except:
            account.saltlick[saltlickName] = 0

def _parse_w3_armor_sets(account):
    account.armor_sets = {
        'Unlocked': safer_convert(safer_get(account.raw_optlacc_dict, 380, False), False),
        'Days Remaining': 30 - max(0, safer_convert(safer_get(account.raw_optlacc_dict, 381, 0), 0)),
        'Sets': {}
    }
    raw_armor_sets = safer_get(account.raw_optlacc_dict, 379, "")
    try:
        raw_armor_sets_list = raw_armor_sets.split(',')
    except:
        raw_armor_sets_list = []
    for set_name, requirements in equipment_sets_dict.items():
        clean_name = set_name.replace('_', ' ')
        account.armor_sets['Sets'][clean_name] = {
            'Owned': set_name in raw_armor_sets_list,
            'Image': getItemDisplayName(requirements[0][0]),
            'Armor': requirements[0],
            'Tools': requirements[1],
            'Required Tools': safer_convert(requirements[3][0], 0),
            'Weapons': requirements[2],
            'Required Weapons': safer_convert(requirements[3][1], 0),
            'Bonus Type': requirements[3][3].replace('|', ' ').replace('_', ' '),
            'Base Value': safer_convert(requirements[3][2], 0)
        }

def _parse_w3_worship(account):
    account.worship = {
        'Totems': {}
    }
    raw_totem_data = safe_loads(account.raw_data.get("TotemInfo", []))
    if len(raw_totem_data) > 0:
        waves = raw_totem_data[0]
        for totem_index, totem_name in enumerate(totems_list):
            try:
                account.worship['Totems'][totem_index] = {
                    'Name': totem_name,
                    'Waves': safer_convert(waves[totem_index], 0)
                }
            except:
                account.worship['Totems'][totem_index] = {
                    'Name': totem_name,
                    'Waves': 0
                }


def _parse_w4(account):
    _parse_w4_cooking(account)
    _parse_w4_lab(account)
    _parse_w4_rift(account)
    _parse_w4_breeding(account)
    _parse_w4_tome(account)

def _parse_w4_cooking(account):
    account.cooking = {
        'MealsUnlocked': 0,
        'MealsUnder11': 0,
        'MealsUnder30': 0,
        'PlayerMaxPlateLvl': 30,  # 30 is the default starting point
        'PlayerTotalMealLevels': 0,
        'MaxTotalMealLevels': max_meal_count * max_meal_level,
        'PlayerMissingPlateUpgrades': []
    }
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

    account.meals = {}
    # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
    for index, details in cooking_meal_dict.items():
        account.meals[details['Name']] = {
            'Level': parse_number(raw_meals_list[0][index], 0),
            'Value': parse_number(raw_meals_list[0][index], 0) * details['BaseValue'],  # Mealmulti applied in calculate section
            'BaseValue': details['BaseValue'],
            'Effect': details['Effect'],
            'Index': index,
            'Image': details['Image']
        }

    account.cooking['PlayerTotalMealLevels'] = sum([details['Level'] for details in account.meals.values()])
    account.cooking['MealsUnlocked'] = sum([details['Level'] > 0 for details in account.meals.values()])
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

def _parse_w4_tome(account):
    account.tome = {
        'Data Present': 'totalTomePoints' in account.raw_data.get('parsedData', {}),
        'Total Points': floor(account.raw_data.get('parsedData', {}).get('totalTomePoints', 0)),
        'Blue Pages Unlocked': safer_convert(safer_get(account.raw_optlacc_dict, 196, False), False),
        'Red Pages Unlocked': safer_convert(safer_get(account.raw_optlacc_dict, 197, False), False),
        'Bonuses': {
            'DMG': {},
            'Skill Efficiency': {},
            'Drop Rarity': {},
        },
        'Tome Percent': 100
    }

def _parse_w4_lab(account):
    raw_lab = safe_loads(account.raw_data.get("Lab", []))
    _parse_w4_lab_chips(account, raw_lab)
    _parse_w4_lab_bonuses(account, raw_lab)
    _parse_w4_jewels(account, raw_lab)

def _parse_w4_lab_chips(account, raw_lab):
    account.labChips = {}
    raw_labChips_list = raw_lab
    if len(raw_labChips_list) >= 15:
        raw_labChips_list = raw_labChips_list[15]
    for labChipIndex, labChip in lab_chips_dict.items():
        try:
            account.labChips[labChip["Name"]] = max(0, int(raw_labChips_list[labChipIndex]))
        except:
            account.labChips[labChip["Name"]] = 0

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
    account.rift = {
        'Unlocked': False,
        'Level': account.raw_data.get("Rift", [0])[0],
    }
    account.rift_level = account.raw_data.get("Rift", [0])[0]
    if account.rift['Level'] > 0:
        account.rift['Unlocked'] = True
    else:
        for characterIndex in range(0, len(account.all_quests)):
            if account.all_quests[characterIndex].get("Rift_Ripper1", 0) == 1:
                account.rift['Unlocked'] = True
                break
    for riftLevel, riftBonusDict in rift_rewards_dict.items():
        account.rift[riftBonusDict['Shorthand']] = account.rift['Level'] >= riftLevel

def _parse_w4_breeding(account):
    account.breeding = {
        'Egg Slots': 3,
        'Unlocked Counts': {
            "W1": 0,
            "W2": 0,
            "W3": 0,
            "W4": 0,
            "W5": 0,
            "W6": 0,
            "W7": 0,
            "W8": 0,
        },
        'Total Unlocked Count': 0,
        'Breedability Days': {
            "W1": [],
            "W2": [],
            "W3": [],
            "W4": [],
            "W5": [],
            "W6": [],
            "W7": [],
            "W8": [],
        },
        'Shiny Days': {
            "W1": [],
            "W2": [],
            "W3": [],
            "W4": [],
            "W5": [],
            "W6": [],
            "W7": [],
            "W8": [],
        },
        "Genetics": {},
        "Species": {},
        "Total Shiny Levels": {},
        "Grouped Bonus": {},
        'Territories': {},
        'Highest Unlocked Territory Number': 0,
        'Highest Unlocked Territory Name': '',
        'Upgrades': {},
        'ArenaMaxWave': 0,
        'PetSlotsUnlocked': 2,
    }
    raw_breeding_list = safe_loads(account.raw_data.get("Breeding", []))
    # raw_territory_list = safe_loads(account.raw_data.get("Territory", []))
    # raw_breeding_pets = safe_loads(account.raw_data.get("Pets", []))

    _parse_w4_breeding_defaults(account)
    _parse_w4_breeding_misc(account)
    _parse_w4_breeding_upgrades(account, raw_breeding_list)
    _parse_w4_breeding_territories(account)
    _parse_w4_breeding_pets(account, raw_breeding_list)
    account.breeding['Egg Slots'] += (
        account.gemshop['Purchases']['Royal Egg Cap']['Owned']
        + account.breeding['Upgrades']['Egg Capacity']['Level']
        + account.merits[3][2]['Level']
    )

def _parse_w4_breeding_defaults(account):
    # Abilities defaulted to False
    for genetic in breeding_genetics_list:
        account.breeding["Genetics"][genetic] = False

    # Total Shiny Bonus Levels defaulted to 0
    # Grouped Bonus per Shiny Bonus defaulted to empty list
    for bonus in breeding_shiny_bonus_list:
        account.breeding["Total Shiny Levels"][bonus] = 0
        account.breeding['Grouped Bonus'][bonus] = []

def _parse_w4_breeding_misc(account):
    # Highest Arena Wave
    try:
        account.breeding['ArenaMaxWave'] = int(account.raw_data["OptLacc"][89])
    except:
        pass

    # Number of Pet Slots Unlocked
    for requirement in slot_unlock_waves_list:
        if account.breeding['ArenaMaxWave'] > requirement:
            account.breeding['PetSlotsUnlocked'] += 1

def _parse_w4_breeding_upgrades(account, rawBreeding):
    for upgradeIndex, upgradeValuesDict in breeding_upgrades_dict.items():
        try:
            account.breeding['Upgrades'][upgradeValuesDict['Name']] = {
                'Level': rawBreeding[2][upgradeIndex],
                'MaxLevel': upgradeValuesDict['MaxLevel'],
                'Value': upgradeValuesDict['BonusValue'] * rawBreeding[2][upgradeIndex]
            }
        except:
            account.breeding['Upgrades'][upgradeValuesDict['Name']] = {
                'Level': 0,
                'MaxLevel': upgradeValuesDict['MaxLevel'],
                'Value': 0
            }

def _parse_w4_breeding_territories(account):
    account.breeding["Highest Unlocked Territory Number"] = safer_get(account.raw_optlacc_dict, 85, 0)
    account.breeding["Highest Unlocked Territory Name"] = territory_names[min(max_breeding_territories, account.breeding["Highest Unlocked Territory Number"])]

    for territoryIndex in range(0, max_breeding_territories):
        if territoryIndex < account.breeding["Highest Unlocked Territory Number"]:
            account.breeding['Territories'][territory_names[territoryIndex + 1]] = {'Unlocked': True}

        else:
            account.breeding['Territories'][territory_names[territoryIndex + 1]] = {'Unlocked': False}

def _parse_w4_breeding_pets(account, rawBreeding):
    # Unlocked Counts per World
    for index in range(0, 8):
        try:
            account.breeding['Unlocked Counts'][f"W{index + 1}"] = rawBreeding[1][index]
            account.breeding['Total Unlocked Count'] += rawBreeding[1][index]
        except:
            continue  # Already defaulted to 0 during initialization

    # Breedability Days
    for index in range(13, 21):
        account.breeding['Breedability Days'][f"W{index - 12}"] = []
        for entry in rawBreeding[index]:
            account.breeding['Breedability Days'][f"W{index - 12}"].append(safer_convert(entry, 0.0))

    # Shiny Days
    for index in range(22, 30):
        account.breeding['Shiny Days'][f"W{index - 21}"] = []
        for entry in rawBreeding[index]:
            account.breeding['Shiny Days'][f"W{index - 21}"].append(safer_convert(entry, 0.0))

    # Parse data for each individual pet, increase their shiny bonus level, and mark their Genetic as obtained
    for worldIndex, worldPetsDict in breeding_species_dict.items():
        account.breeding['Species'][worldIndex] = {}
        for petIndex, petValuesDict in worldPetsDict.items():
            try:
                account.breeding['Species'][worldIndex][petValuesDict['Name']] = {
                    'Unlocked': account.breeding['Unlocked Counts'][f"W{worldIndex}"] > petIndex,
                    'Genetic': petValuesDict['Genetic'],
                    'ShinyBonus': petValuesDict['ShinyBonus'],
                    'ShinyLevel': getShinyLevelFromDays(account.breeding['Shiny Days'][f"W{worldIndex}"][petIndex]),
                    'DaysToShinyLevel': getDaysToNextShinyLevel(account.breeding['Shiny Days'][f"W{worldIndex}"][petIndex]),
                    'BreedabilityDays': account.breeding['Breedability Days'][f"W{worldIndex}"][petIndex],
                    'BreedabilityMulti': getBreedabilityMultiFromDays(account.breeding['Breedability Days'][f"W{worldIndex}"][petIndex]),
                    'BreedabilityHeart': getBreedabilityHeartFromMulti(
                        getBreedabilityMultiFromDays(account.breeding['Breedability Days'][f"W{worldIndex}"][petIndex])),
                }
                # Increase the total shiny bonus level
                account.breeding["Total Shiny Levels"][petValuesDict['ShinyBonus']] += account.breeding['Species'][worldIndex][petValuesDict['Name']]['ShinyLevel']
                # If this pet is unlocked, but their Genetic isn't marked as unlocked, update the Abilities
                if account.breeding['Species'][worldIndex][petValuesDict['Name']]['Unlocked'] and not account.breeding["Genetics"][petValuesDict['Genetic']]:
                    account.breeding["Genetics"][petValuesDict['Genetic']] = True
            except:
                logger.exception(f"Failed to parse breeding pet {petValuesDict['Name']}")
                account.breeding['Species'][worldIndex][petValuesDict['Name']] = {
                    'Unlocked': False,
                    'Genetic': petValuesDict['Genetic'],
                    'ShinyBonus': petValuesDict['ShinyBonus'],
                    'ShinyLevel': 0,
                    'DaysToShinyLevel': 0,
                    'BreedabilityDays': 0.0,
                    'BreedabilityMulti': 1,
                    'BreedabilityHeart': 'breedability-heart-1',
                }
            # Add this pet to the shiny bonus grouped list
            account.breeding['Grouped Bonus'][petValuesDict['ShinyBonus']].append(
                (
                    petValuesDict['Name'],
                    account.breeding['Species'][worldIndex][petValuesDict['Name']]['ShinyLevel'],
                    account.breeding['Species'][worldIndex][petValuesDict['Name']]['DaysToShinyLevel'],
                )
            )

    # Sort the Grouped bonus by Days to next Shiny Level
    for groupedBonus in account.breeding["Grouped Bonus"]:
        account.breeding["Grouped Bonus"][groupedBonus].sort(key=lambda x: float(x[2]))

def _parse_w5(account):
    account.gaming = {
        'BitsOwned': 0,
        'FertilizerValue': 0,
        'FertilizerSpeed': 0,
        'FertilizerCapacity': 0,
        'MutationsUnlocked': 0,
        'EvolutionChance': 0,
        'DNAOwned': 0,
        'Nugget': 0,
        'Acorns': 0,
        'PoingHighscore': 0,
        'LogbookString': "",
        'Logbook': {},
        'SuperBitsString': "",
        'SuperBits': {},
        'Envelopes': 0,
        'Imports': {}
    }
    _parse_w5_gaming(account)
    _parse_w5_gaming_sprouts(account)
    _parse_w5_slab(account)
    _parse_w5_sailing(account)
    _parse_w5_divinity(account)

def _parse_w5_gaming(account):
    raw_gaming_list = safe_loads(account.raw_data.get('Gaming', []))
    if not raw_gaming_list:
        logger.warning('Gaming data not present')
    if raw_gaming_list:
        # Bits Owned sometimes Float, sometimes String
        try:
            account.gaming['BitsOwned'] = safer_convert(raw_gaming_list[0], 0.00)
        except:
            account.gaming['BitsOwned'] = 0.00

        try:
            account.gaming['FertilizerValue'] = raw_gaming_list[1]
            account.gaming['FertilizerSpeed'] = raw_gaming_list[2]
            account.gaming['FertilizerCapacity'] = raw_gaming_list[3]
            account.gaming['MutationsUnlocked'] = raw_gaming_list[4]
            account.gaming['DNAOwned'] = raw_gaming_list[5]
            account.gaming['EvolutionChance'] = raw_gaming_list[7]  #TODO: Look into this being duplicated
            account.gaming['Nugget'] = raw_gaming_list[8]
            account.gaming['Acorns'] = raw_gaming_list[9]
            account.gaming['EvolutionChance'] = raw_gaming_list[10]  #TODO: Look into this being duplicated
            account.gaming['LogbookString'] = raw_gaming_list[11]
            account.gaming['SuperBitsString'] = str(raw_gaming_list[12])
            account.gaming['Envelopes'] = raw_gaming_list[13]
        except:
            account.gaming['FertilizerValue'] = 0
            account.gaming['FertilizerSpeed'] = 0
            account.gaming['FertilizerCapacity'] = 0
            account.gaming['MutationsUnlocked'] = 0
            account.gaming['DNAOwned'] = 0
            account.gaming['EvolutionChance'] = 0
            account.gaming['Nugget'] = 0
            account.gaming['Acorns'] = 0
            account.gaming['LogbookString'] = 0
            account.gaming['SuperBitsString'] = ''
            account.gaming['Envelopes'] = 0

    for name, valuesDict in gaming_superbits_dict.items():
        try:
            account.gaming['SuperBits'][name] = {
                'Unlocked': valuesDict['CodeString'] in account.gaming['SuperBitsString'],
                'BonusText': valuesDict['BonusText']
            }
        except:
            account.gaming['SuperBits'][valuesDict['Name']] = {
                'Unlocked': False,
                'BonusText': valuesDict['BonusText']
            }

def _parse_w5_gaming_sprouts(account):
    # [0] through [24] = actual sprouts
    # [300, 25469746.803332243, 0, 0, 655, 70],  # [25] = Sprinkler Import
    # [315, 1335, 0, 0, 654, 383],  # [26] = Shovel Import
    # [300, 1335, 503, 711, 429.34312394215203, 237.05230565943967],  # [27] = Squirrel Import
    # [275, 287171, 26, 0, 82, 153],  # [28] = Seashell Import
    # [260, 1, 0, 0, 82, 225],  # [29] = Kitsune Roxie Import
    # [224, 1345, 0, 0, 98, 383],  # [30] = Log Import
    # [1, 842957708.5889401, 0, 0, 83, 70],  # [31] = Poing Import
    # [160, 23, 0, 0, 77, 295],  # [32] = Snail Import
    # [0, 21884575.351264, 0, 0, 309, 210],  # [33] = Box9 Import
    # [0, 842957708.5889401, 0, 0, 0, 0],  # [34] = Box10 Import
    raw_gaming_sprout_list = safe_loads(account.raw_data.get("GamingSprout", []))
    try:
        account.gaming['Imports'] = {
            'Snail': {
                'Level': raw_gaming_sprout_list[32][0],
                'SnailRank': raw_gaming_sprout_list[32][1],
                'Encouragements': raw_gaming_sprout_list[32][2]
            }
        }
    except:
        account.gaming['Imports'] = {
            'Snail': {
                'Level': 0,
                'SnailRank': 0,
                'Encouragements': 0
            }
        }

def _parse_w5_slab(account):
    account.registered_slab = safe_loads(account.raw_data.get("Cards1", []))

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
    for island_index, island_values_dict in sailing_dict.items():
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
    account.divinity = {
        'Divinities': copy.deepcopy(divinity_divinities_dict),
        'DivinityLinks': {}
    }
    raw_divinity_list = safe_loads(account.raw_data.get("Divinity", []))
    if not raw_divinity_list:
        logger.warning("Divinity data not present")
    while len(raw_divinity_list) < 40:
        raw_divinity_list.append(0)
    account.divinity['DivinityPoints'] = raw_divinity_list[24]
    if isinstance(account.divinity['DivinityPoints'], str):
        try:
            account.divinity['DivinityPoints'] = int(float(account.divinity['DivinityPoints']))
        except:
            logger.exception(f"Could not convert '{type(account.divinity['DivinityPoints'])}' {account.divinity['DivinityPoints']} to int. Defaulting to 0")
            account.divinity['DivinityPoints'] = 0
    account.divinity['GodsUnlocked'] = min(10, raw_divinity_list[25])
    account.divinity['GodRank'] = max(0, raw_divinity_list[25] - 10)
    account.divinity['LowOffering'] = raw_divinity_list[26]
    account.divinity['HighOffering'] = raw_divinity_list[27]
    account.divinity['LowOfferingGoal'] = ""
    account.divinity['HighOfferingGoal'] = ""
    for divinityIndex in account.divinity['Divinities']:
        if account.divinity['GodsUnlocked'] >= divinityIndex:
            account.divinity['Divinities'][divinityIndex]["Unlocked"] = True
        # Snake has a divinityIndex of 0, Blessing level stored in 28
        account.divinity['Divinities'][divinityIndex]["BlessingLevel"] = raw_divinity_list[divinityIndex + 27]
    for character in account.safe_characters:
        try:
            character.setDivinityStyle(getStyleNameFromIndex(raw_divinity_list[character.character_index]))
            character.setDivinityLink(getDivinityNameFromIndex(raw_divinity_list[character.character_index + 12] + 1))
        except:
            continue

def _parse_caverns(account):
    account.caverns = {
        'Villagers': {},
        'TotalOpalsInvested': 0,
        'Caverns': {},
        'CavernsUnlocked': 0,
        'Schematics': {},
        'TotalSchematics': 0,
        'Majiks': {},
        'TotalMajiks': 0,
        'Measurements': {},
        'Studies': {},
        'TotalStudies': 0,
        'Collectibles': {}
    }
    raw_caverns_list: list[list] = safe_loads(account.raw_data.get('Holes', []))
    if not raw_caverns_list:
        logger.warning(f"Caverns data not present{', as expected' if account.version < 230 else ''}.")
    while len(raw_caverns_list) < 30:
        raw_caverns_list.append([0]*100)
    _parse_caverns_villagers(account, raw_caverns_list[1], raw_caverns_list[2], raw_caverns_list[3], raw_caverns_list[23])
    _parse_caverns_actual_caverns(account, raw_caverns_list[7])
    _parse_caverns_majiks(account, raw_caverns_list[4], raw_caverns_list[5], raw_caverns_list[6], raw_caverns_list[11])
    _parse_caverns_schematics(account, raw_caverns_list[13])
    _parse_caverns_measurements(account, raw_caverns_list[22])
    _parse_caverns_studies(account, raw_caverns_list[26])
    _parse_caverns_biome1(account, raw_caverns_list)
    _parse_caverns_biome2(account, raw_caverns_list)
    _parse_caverns_biome3(account, raw_caverns_list)

    # for key in account.caverns:
    #     logger.debug(f"{key}: {account.caverns[key]}")

def _parse_caverns_villagers(account, villager_levels, villager_exp, opals_invested, parallel_villagers):
    for villager_index, villager_data in enumerate(caverns_villagers):
        try:
            account.caverns['Villagers'][villager_data['Name']] = {
                'Unlocked': villager_levels[villager_index] > 0,
                'UnlockedCavern': villager_data['UnlockedAtCavern'],
                'Level': villager_levels[villager_index],
                'Opals': opals_invested[villager_index],
                'Title': f"{villager_data['Name']}, {villager_data['Role']}",
                'VillagerNumber': villager_data['VillagerNumber'],
                'LevelPercent': 100 * (float(villager_exp[villager_index]) / getVillagerEXPRequired(villager_index, villager_levels[villager_index], account.version)),
            }
            account.gemshop['Purchases'][f"Parallel Villagers {villager_data['Role']}"] = {
                'Owned': parallel_villagers[villager_index],
                'MaxLevel': 1,
                'ItemCodename': 'GemP40',
                'Section': 'Oddities',
                'Subsection': 'Caverns'
            }
            account.caverns['TotalOpalsInvested'] += account.caverns['Villagers'][villager_data['Name']]['Opals']
        except:
            account.caverns['Villagers'][villager_data['Name']] = {
                'Unlocked': villager_data['Name'] == 'Polonai',
                'UnlockedCavern': villager_data['UnlockedAtCavern'],
                'Level': 0,
                'Opals': 0,
                'Title': f"{villager_data['Name']}, {villager_data['Role']}",
                'VillagerNumber': villager_data['VillagerNumber'],
                'LevelPercent': 0,
            }
            account.gemshop['Purchases'][f"Parallel Villagers {villager_data['Role']}"] = {
                'Owned': 0,
                'MaxLevel': 1,
                'ItemCodename': 'GemP40',
                'Section': 'Oddities',
                'Subsection': 'Caverns'
            }

def _parse_caverns_actual_caverns(account, opals_per_cavern):
    for cavern_index, cavern_name in caverns_cavern_names.items():
        try:
            account.caverns['Caverns'][cavern_name] = {
                'Unlocked': account.caverns['Villagers']['Polonai']['Level'] >= cavern_index,
                'OpalsFound': 0 if cavern_name == 'Camp' else opals_per_cavern[cavern_index - 1] or 0,
                'Image': f'cavern-{cavern_index}',
                'CavernNumber': cavern_index
            }
        except:
            account.caverns['Caverns'][cavern_name] = {
                'Unlocked': False,
                'OpalsFound': 0,
                'Image': f'cavern-{cavern_index}',
                'CavernNumber': cavern_index
            }

def _parse_caverns_majiks(account, hole_majiks, village_majiks, idleon_majiks, extras):
    account.caverns['TotalMajiks'] = sum([sum(hole_majiks), sum(village_majiks), sum(idleon_majiks)])
    raw_majiks: dict = {
        'Hole': hole_majiks,
        'Village': village_majiks,
        'IdleOn': idleon_majiks
    }
    for majik_type, majiks in caverns_conjuror_majiks.items():
        for majik_index, majik_data in enumerate(majiks):
            try:
                account.caverns['Majiks'][majik_data['Name']] = {
                    'MajikType': majik_type,
                    'MajikIndex': majik_index,
                    'Level': int(raw_majiks[majik_type][majik_index]),
                    'MaxLevel': majik_data['MaxLevel'],
                    'Description': majik_data['Description'],
                    # 'Value': 0  #Calculated later in _calculate_caverns_majiks
                }
            except:
                account.caverns['Majiks'][majik_data['Name']] = {
                    'MajikType': majik_type,
                    'MajikIndex': majik_index,
                    'Level': 0,
                    'MaxLevel': majik_data['MaxLevel'],
                    'Description': majik_data['Description'],
                    # 'Value': 0  # Calculated later in _calculate_caverns_majiks
                }
    #Pocket Divinity
    account.caverns['PocketDivinityLinks'] = []
    try:
        raw_pocket_div_links = [int(v) for v in extras[29:31] if v is not None]
    except:
        logger.exception(f"Could not cast Pocket Divinity link values to ints, or data isn't present. Defaulting to no links.")
        #logger.debug(f"extras = {extras}")
        raw_pocket_div_links = [-1, -1]
    for entry_index, entry_value in enumerate(raw_pocket_div_links):
        if int(entry_value) != -1 and entry_index < account.caverns['Majiks']['Pocket Divinity']['Level']:
            if int(entry_value)+1 in divinity_divinities_dict:
                account.caverns['PocketDivinityLinks'].append(divinity_divinities_dict[int(entry_value) + 1]['Name'])
            else:
                logger.exception(f"Pocket Divinity link value of {entry_value}+1 not found in consts.divinity_divinitiesDict")
                account.caverns['PocketDivinityLinks'].append('')
    #logger.debug(f"Pocket Divinity Links: {account.caverns['PocketDivinityLinks']}")

def _parse_caverns_schematics(account, raw_schematics_list):
    try:
        account.caverns['TotalSchematics'] = sum(raw_schematics_list)
    except:
        logger.warning(f"Error summing raw_schematics_list")
        account.caverns['TotalSchematics'] = 0
        pass
    for schematic_index, schematic_details in enumerate(caverns_engineer_schematics):
        clean_name = schematic_details[0].replace("_", " ")
        if clean_name == 'NameNameName':  #Placeholders added in v2.31 all share this name
            continue
        else:
            resource_type = getCavernResourceImage(schematic_details[2])
            try:
                account.caverns['Schematics'][clean_name] = {
                    'Purchased': raw_schematics_list[schematic_index] > 0,
                    'Image': f'engineer-schematic-{schematic_index}',
                    'Description': schematic_details[5].replace("_", " "),
                    'UnlockOrder': caverns_engineer_schematics_unlock_order.index(schematic_index) + 1,
                    'Resource': resource_type
                }
            except:
                try:
                    #logger.warning(f"Error processing schematic {clean_name} at index {schematic_index}")
                    account.caverns['Schematics'][clean_name] = {
                        'Purchased': False,
                        'Image': f'engineer-schematic-{schematic_index}',
                        'Description': schematic_details[5].replace("_", " "),
                        'UnlockOrder': caverns_engineer_schematics_unlock_order.index(schematic_index) + 1,
                        'Resource': resource_type
                    }
                except:
                    logger.exception(f"Error processing schematic {clean_name} at index {schematic_index}. Usually caused by HolesInfo[40] not being updated after new schematics were added!")
                    account.caverns['Schematics'][clean_name] = {
                        'Purchased': False,
                        'Image': f'engineer-schematic-{schematic_index}',
                        'Description': schematic_details[5].replace("_", " "),
                        'UnlockOrder': 999,
                        'Resource': resource_type
                    }

def _parse_caverns_measurements(account, raw_measurements_list):
    for measurement_index, measurement_details in enumerate(caverns_measurer_measurements):
        try:
            hi55 = caverns_measurer_HI55[measurement_index]
            tot = 'TOT' in hi55
            hi55_after_split = safer_convert(hi55.split('TOT')[0], 1)
        except:
            logger.exception(f"Unable to read and split HolesInfo[55] for index {measurement_index}")
            tot = False
            hi55_after_split = 1
        try:
            account.caverns['Measurements'][measurement_index] = {
                'Level': safer_convert(raw_measurements_list[measurement_index], 0),
                'Unit': measurement_details[0],
                'Description': measurement_details[1].strip(),
                'ScalesWith': measurement_details[2],
                'Image': f"measurement-{measurement_index}",
                'Resource': measurement_details[3],
                'MeasurementNumber': measurement_index + 1,
                'TOT': tot,
                'HI55': hi55_after_split
            }
        except:
            account.caverns['Measurements'][measurement_index] = {
                'Level': 0,
                'Unit': measurement_details[0],
                'Description': measurement_details[1].strip(),
                'ScalesWith': measurement_details[2],
                'Image': f"measurement-{measurement_index}",
                'Resource': measurement_details[3],
                'MeasurementNumber': measurement_index + 1,
                'TOT': tot,
                'HI55': hi55_after_split
            }

def _parse_caverns_studies(account, raw_studies_list):
    for study_index, study_details in caverns_librarian_studies.items():
        try:
            account.caverns['TotalStudies'] += raw_studies_list[study_index]
            account.caverns['Studies'][study_index] = {
                'Level': raw_studies_list[study_index],
                'MaxLevel': 999,  #Fixed in account_calcs._calculate_caverns_studies()
                'CavernNumber': study_index+1,
                'CavernName': caverns_cavern_names.get(study_index+1, f'UnknownCavern{study_index+1}'),
                'Description': study_details[0],
                'ScalingValue': study_details[1],
                'Value': 0  #Fixed in account_calcs._calculate_caverns_studies()
            }
        except:
            account.caverns['Studies'][study_index] = {
                'Level': 0,
                'MaxLevel': 999,  #Fixed in account_calcs._calculate_caverns_studies()
                'CavernNumber': study_index + 1,
                'CavernName': caverns_cavern_names.get(study_index + 1, f'UnknownCavern{study_index + 1}'),
                'Description': study_details[0],
                'ScalingValue': study_details[1],
                'Value': 0
            }

def _parse_caverns_biome1(account, raw_caverns_list):
    _parse_caverns_the_well(account, raw_caverns_list)
    _parse_caverns_motherlode(account, raw_caverns_list)
    _parse_caverns_the_den(account, raw_caverns_list)
    _parse_caverns_bravery_monument(account, raw_caverns_list)
    _parse_caverns_the_bell(account, raw_caverns_list)

def _parse_caverns_the_well(account, raw_caverns_list):
    account.caverns['Caverns']['The Well']['BucketTargets'] = []
    for i in range(0, max_buckets):
        try:
            account.caverns['Caverns']['The Well']['BucketTargets'].append(safer_convert(raw_caverns_list[10][i], 0))
        except IndexError:
            account.caverns['Caverns']['The Well']['BucketTargets'].append(0)

    account.caverns['Caverns']['The Well']['SedimentsOwned'] = []
    account.caverns['Caverns']['The Well']['SedimentLevels'] = []
    for i in range(0, max_sediments):
        try:
            account.caverns['Caverns']['The Well']['SedimentsOwned'].append(safer_convert(raw_caverns_list[9][i], sediment_bars[i] * -1))
        except IndexError:
            account.caverns['Caverns']['The Well']['SedimentsOwned'].append(sediment_bars[i] * -1)
        try:
            account.caverns['Caverns']['The Well']['SedimentLevels'].append(safer_convert(raw_caverns_list[8][i], 0))
        except IndexError:
            account.caverns['Caverns']['The Well']['SedimentLevels'].append(0)

    try:
        account.caverns['Caverns']['The Well']['BarExpansion'] = raw_caverns_list[11][10]
    except:
        account.caverns['Caverns']['The Well']['BarExpansion'] = False

    # From looking at data, holes_11_9 is just the number of previously completed trades. Maybe it changes higher up at some point /shrug
    account.caverns['Caverns']['The Well']['Holes-11-9'] = safer_convert(raw_caverns_list[11][9], 0)

def _parse_caverns_motherlode(account, raw_caverns_list):
    cavern_name = 'Motherlode'
    motherlode_offset = 0
    try:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = safer_convert(raw_caverns_list[11][0 + motherlode_offset], 0.0)
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = safer_convert(raw_caverns_list[11][1 + motherlode_offset], 0)
    except:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = 0

def _parse_caverns_the_den(account, raw_caverns_list):
    try:
        account.caverns['Caverns']['The Den']['HighScore'] = round(float(raw_caverns_list[11][8]))
    except:
        account.caverns['Caverns']['The Den']['HighScore'] = 0

def _parse_caverns_bravery_monument(account, raw_caverns_list):
    monument_name = 'Bravery Monument'
    monument_index = 0

    # Layer Data
    try:
        account.caverns['Caverns'][monument_name]['Hours'] = int(raw_caverns_list[14][0 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['Hours'] = 0
    try:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = int(raw_caverns_list[14][1 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = 0

    # Setup Bonuses
    account.caverns['Caverns'][monument_name]['Bonuses'] = {}
    for bonus_index, bonus_details in monument_bonuses[monument_name].items():
        try:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': raw_caverns_list[15][bonus_index],
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }
        except:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': 0,
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }

def _parse_caverns_the_bell(account, raw_caverns_list):
    cavern_name = 'The Bell'

    # Charge
    account.caverns['Caverns'][cavern_name]['Charges'] = {}
    try:
        account.caverns['Caverns'][cavern_name]['Charges']['Ring'] = [
            safer_convert(raw_caverns_list[18][0], 0),
            safer_convert(raw_caverns_list[18][1], 0),
            getBellExpRequired(0, raw_caverns_list[18][1])
        ]
    except:
        account.caverns['Caverns'][cavern_name]['Charges']['Ring'] = [0, 0, getBellExpRequired(0, 0)],
    try:
        account.caverns['Caverns'][cavern_name]['Charges']['Ping'] = [
            safer_convert(raw_caverns_list[18][2], 0),
            safer_convert(raw_caverns_list[18][3], 0),
            getBellExpRequired(1, raw_caverns_list[18][3])
        ]
    except:
        account.caverns['Caverns'][cavern_name]['Charges']['Ping'] = [0, 0, getBellExpRequired(1, 0)]
    try:
        account.caverns['Caverns'][cavern_name]['Charges']['Clean'] = [
            safer_convert(raw_caverns_list[18][4], 0),
            safer_convert(raw_caverns_list[18][5], 0),
            getBellExpRequired(2, raw_caverns_list[18][5])
        ]
    except:
        account.caverns['Caverns'][cavern_name]['Charges']['Clean'] = [0, 0, getBellExpRequired(2, 0)]
    try:
        account.caverns['Caverns'][cavern_name]['Charges']['Renew'] = [
            safer_convert(raw_caverns_list[18][6], 0),
            safer_convert(raw_caverns_list[18][7], 0),
            getBellExpRequired(3, raw_caverns_list[18][7])
        ]
    except:
        account.caverns['Caverns'][cavern_name]['Charges']['Renew'] = [0, 0, getBellExpRequired(3, 0)]

    # Ring Bonuses
    account.caverns['Caverns'][cavern_name]['Ring Bonuses'] = {}
    ring_levels = raw_caverns_list[17]
    for ring_index, ring_details in bell_ring_bonuses.items():
        try:
            account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index] = {
                'Level': int(ring_levels[ring_index]),
                'Description': ring_details['Description'],
                'ScalingValue': ring_details['ScalingValue'],
                'Image': ring_details['Image']
            }
        except:
            account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index] = {
                'Level': 0,
                'Description': ring_details['Description'].replace('{', '0.00'),
                'ScalingValue': ring_details['ScalingValue'],
                'Image': ring_details['Image']
            }
        account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Value'] = (
                account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Level']
                * account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['ScalingValue']
        )
        account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Description'] = (
            account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Description'].replace(
                '{', f"{account.caverns['Caverns'][cavern_name]['Ring Bonuses'][ring_index]['Value']:.2f}"
            )
        )

    # Improvements
    account.caverns['Caverns'][cavern_name]['Improvements'] = {}
    improvement_levels = raw_caverns_list[16]
    for improvement_index, improvement_details in bell_clean_improvements.items():
        try:
            account.caverns['Caverns'][cavern_name]['Improvements'][improvement_index] = {
                'Level': improvement_levels[improvement_index],
                'Description': improvement_details['Description'],
                'Image': improvement_details['Image'],
                'Resource': improvement_details['Resource']
            }
        except:
            account.caverns['Caverns'][cavern_name]['Improvements'][improvement_index] = {
                'Level': 0,
                'Description': improvement_details['Description'],
                'Image': improvement_details['Image'],
                'Resource': improvement_details['Resource']
            }

def _parse_caverns_biome2(account, raw_caverns_list):
    _parse_caverns_the_lamp(account, raw_caverns_list)
    _parse_caverns_the_hive(account, raw_caverns_list)
    _parse_caverns_grotto(account, raw_caverns_list)
    _parse_caverns_justice_monument(account, raw_caverns_list)
    _parse_caverns_the_harp(account, raw_caverns_list)

def _parse_caverns_the_harp(account, raw_caverns_list):
    cavern_name = 'The Harp'
    try:
        account.caverns['Caverns'][cavern_name]['HarpPower'] = raw_caverns_list[11][22]
    except:
        account.caverns['Caverns'][cavern_name]['HarpPower'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['NotesUnlocked'] = raw_caverns_list[11][20]
    except:
        account.caverns['Caverns'][cavern_name]['NotesUnlocked'] = 0

    account.caverns['Caverns'][cavern_name]['Chords'] = {}
    for chord_index, chord_name in enumerate(harp_chord_effects.keys()):
        try:
            account.caverns['Caverns'][cavern_name]['Chords'][chord_name] = {
                'Level': raw_caverns_list[19][0 + (2 * chord_index)],
                'Exp': raw_caverns_list[19][1 + (2 * chord_index)],
                'Strum': harp_chord_effects[chord_name][0],
                'LVBonus': harp_chord_effects[chord_name][1],
            }
        except:
            account.caverns['Caverns'][cavern_name]['Chords'][chord_name] = {
                'Level': 0,
                'Exp': 0,
                'Strum': harp_chord_effects[chord_name][0],
                'LVBonus': harp_chord_effects[chord_name][1],
            }
        if chord_index < 2:
            account.caverns['Caverns'][cavern_name]['Chords'][chord_name]['Unlocked'] = True
        else:
            account.caverns['Caverns'][cavern_name]['Chords'][chord_name]['UnlockedBy'] = schematics_unlocking_harp_chords[chord_index - 2]
            account.caverns['Caverns'][cavern_name]['Chords'][chord_name]['Unlocked'] = (
                account.caverns['Schematics'][schematics_unlocking_harp_chords[chord_index-2]]['Purchased']
            )

    try:
        account.caverns['Caverns'][cavern_name]['NotesOwned'] = [safer_convert(entry, 0) for entry in raw_caverns_list[9][max_sediments:max_sediments+max_harp_notes]]
    except:
        account.caverns['Caverns'][cavern_name]['NotesOwned'] = [0] * max_harp_notes
    while len(account.caverns['Caverns'][cavern_name]['NotesOwned']) < max_harp_notes:
        account.caverns['Caverns'][cavern_name]['NotesOwned'].append(0)

def _parse_caverns_the_lamp(account, raw_caverns_list):
    cavern_name = 'The Lamp'
    try:
        account.caverns['Caverns'][cavern_name]['WishesStored'] = raw_caverns_list[11][25]
    except:
        account.caverns['Caverns'][cavern_name]['WishesStored'] = 0
    account.caverns['Caverns'][cavern_name]['WishTypes'] = {}
    try:
        account.caverns['Caverns'][cavern_name]['WishTypesUnlocked'] = (
            raw_caverns_list[21][0] + (1 * account.caverns['Caverns'][cavern_name]['Unlocked'])
        )
    except:
        account.caverns['Caverns'][cavern_name]['WishTypesUnlocked'] = 1 * account.caverns['Caverns'][cavern_name]['Unlocked']
    for wish_index, wish_dict in enumerate(lamp_wishes):
        account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index] = {
            'Name': wish_dict['Name'],
            'BaseCost': wish_dict['BaseCost'],
            'CostIncreaser': wish_dict['CostIncreaser'],
            'Description': f"{wish_dict['Description']}{'. Cost does not increase.' if wish_dict['DoesCostIncrease'] is False else ''}",
            'Image': f'lamp-wish-{wish_index}',
            'BonusList': []
        }
        try:
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Unlocked'] = (
                    account.caverns['Villagers']['Polonai']['Level'] >= 7
                    and account.caverns['Caverns'][cavern_name]['WishTypesUnlocked'] > wish_index
                )
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level'] = parse_number(raw_caverns_list[21][wish_index])
        except:
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Unlocked'] = False
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level'] = 0
        account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['NextCost'] = getWishCost(
            wish_index, account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level']
        )

        #If this is a World X stuff wish, calculate each Value into BonusList then update the Description
        if wish_dict['Name'].startswith('World '):
            world_number = safer_convert(wish_dict['Name'].split('World ')[1][0], 0)
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'] = [
                v * account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level']
                for v in lamp_world_wish_values.get(world_number, [0]*3)
            ]
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '{', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][0]), 1))
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '}', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][1]), 1))
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '~', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][2]), 1))

def _parse_caverns_the_hive(account, raw_caverns_list):
    cavern_name = 'The Hive'
    motherlode_offset = 2
    try:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = safer_convert(raw_caverns_list[11][0 + motherlode_offset], 0)
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = safer_convert(raw_caverns_list[11][1 + motherlode_offset], 0)
    except:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = 0

def _parse_caverns_grotto(account, raw_caverns_list):
    cavern_name = 'Grotto'
    try:
        account.caverns['Caverns'][cavern_name]['PlayerKills'] = safer_convert(raw_caverns_list[11][27], 0)
    except:
        account.caverns['Caverns'][cavern_name]['PlayerKills'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['KillsRequired'] = getGrottoKills(account.caverns['Caverns'][cavern_name]['OpalsFound'])
    except:
        account.caverns['Caverns'][cavern_name]['KillsRequired'] = getGrottoKills(0)
    account.caverns['Caverns'][cavern_name]['KillsRemaining'] = max(
        0,
        account.caverns['Caverns'][cavern_name]['KillsRequired'] - account.caverns['Caverns'][cavern_name]['PlayerKills']
    )
    account.caverns['Caverns'][cavern_name]['PercentRemaining'] = max(
        0,
        100 * (1 - (account.caverns['Caverns'][cavern_name]['PlayerKills'] / account.caverns['Caverns'][cavern_name]['KillsRequired']))
    )

def _parse_caverns_justice_monument(account, raw_caverns_list):
    monument_name = 'Justice Monument'
    monument_index = 1

    # Layer Data
    try:
        account.caverns['Caverns'][monument_name]['Hours'] = int(raw_caverns_list[14][0 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['Hours'] = 0
    try:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = int(raw_caverns_list[14][1 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = 0

    # Setup Bonuses
    account.caverns['Caverns'][monument_name]['Bonuses'] = {}
    for bonus_index, bonus_details in monument_bonuses[monument_name].items():
        try:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': raw_caverns_list[15][bonus_index],
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }
        except:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': 0,
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }

def _parse_caverns_biome3(account, raw_caverns_list):
    _parse_caverns_the_jar(account, raw_caverns_list)
    _parse_caverns_evertree(account, raw_caverns_list)
    _parse_caverns_wisdom_monument(account, raw_caverns_list)
    _parse_caverns_gambit(account, raw_caverns_list)
    _parse_caverns_the_temple(account, raw_caverns_list)

def _parse_caverns_the_jar(account, raw_caverns_list):
    cavern_name = caverns_cavern_names[11]

    #Rupies
    try:
        account.caverns['Caverns'][cavern_name]['RupiesOwned'] = [
            safer_convert(entry, 0.00) for entry in raw_caverns_list[9][max_sediments + max_harp_notes:max_sediments + max_harp_notes + caverns_jar_max_rupies]]
    except:
        account.caverns['Caverns'][cavern_name]['RupiesOwned'] = [0] * caverns_jar_max_rupies
    while len(account.caverns['Caverns'][cavern_name]['RupiesOwned']) < caverns_jar_max_rupies:
        account.caverns['Caverns'][cavern_name]['RupiesOwned'].append(0)

    #Jars
    raw_jars_destroyed = [0] * caverns_jar_max_jar_types
    for i in range(0, caverns_jar_max_jar_types):
        try:
            raw_jars_destroyed[i] = raw_caverns_list[11][40+i]
        except:
            continue
    account.caverns['Caverns'][cavern_name]['Jars'] = {}
    for jar_index, jar_name in enumerate(caverns_jar_jar_types):
        try:
            account.caverns['Caverns'][cavern_name]['Jars'][jar_index] = {
                'Name': f'{jar_name} Jar',
                'Image': f'jar-type-{jar_index}',
                'Destroyed': raw_jars_destroyed[jar_index]
            }
        except:
            account.caverns['Caverns'][cavern_name]['Jars'][jar_index] = {
                'Name': f'{jar_name} Jar',
                'Image': f'jar-type-{jar_index}',
                'Destroyed': 0
            }

    #Collectible Levels
    account.caverns['Caverns'][cavern_name]['CollectiblesOwned'] = []
    for entry in raw_caverns_list[24]:
        try:
            account.caverns['Caverns'][cavern_name]['CollectiblesOwned'].append(safer_convert(entry, 0))
        except:
            account.caverns['Caverns'][cavern_name]['CollectiblesOwned'] = 0
    #Extend the levels to the expected length
    while len(account.caverns['Caverns'][cavern_name]['CollectiblesOwned']) < caverns_jar_collectibles_count:
        account.caverns['Caverns'][cavern_name]['CollectiblesOwned'].append(0)

    #Individual Collectibles
    for collectible_index, collectible_details in enumerate(caverns_jar_collectibles):
        clean_name = collectible_details[0].title().replace('_', ' ')
        scaling_value = safer_convert(collectible_details[1], 0)
        try:
            account.caverns['Collectibles'][clean_name] = {
                'Level': account.caverns['Caverns'][cavern_name]['CollectiblesOwned'][collectible_index],
                'ScalingValue': scaling_value,
                'Value': 0,
                'Description': collectible_details[3].replace('_', ' '),
                'Image': f"jar-collectible-{collectible_index}"
            }
        except:
            account.caverns['Collectibles'][clean_name] = {
                'Level': 0,
                'ScalingValue': scaling_value,
                'Value': 0,
                'Description': collectible_details[3].replace('_', ' '),
                'Image': f"jar-collectible-{collectible_index}"
            }

    # for collectible_name in account.caverns['Collectibles']:
    #     if account.caverns['Collectibles'][collectible_name]['Level'] > 0:
    #         logger.debug(f"{collectible_name}: {account.caverns['Collectibles'][collectible_name]}")

def _parse_caverns_evertree(account, raw_caverns_list):
    cavern_name = caverns_cavern_names[12]
    motherlode_offset = 4
    try:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = safer_convert(raw_caverns_list[11][0 + motherlode_offset], 0)
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = safer_convert(raw_caverns_list[11][1 + motherlode_offset], 0)
    except:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = 0

def _parse_caverns_wisdom_monument(account, raw_caverns_list):
    monument_name = caverns_cavern_names[13]
    monument_index = 2

    # Layer Data
    try:
        account.caverns['Caverns'][monument_name]['Hours'] = int(raw_caverns_list[14][0 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['Hours'] = 0
    try:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = int(raw_caverns_list[14][1 + 2 * monument_index])
    except:
        account.caverns['Caverns'][monument_name]['LayersCleared'] = 0

    # Setup Bonuses
    account.caverns['Caverns'][monument_name]['Bonuses'] = {}
    for bonus_index, bonus_details in monument_bonuses[monument_name].items():
        try:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': raw_caverns_list[15][bonus_index],
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }
        except:
            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index] = {
                'Level': 0,
                'Description': bonus_details['Description'],
                'ScalingValue': bonus_details['ScalingValue'],
                'ValueType': bonus_details['ValueType'],
                'Image': bonus_details['Image'],
                'Value': 0,  # Calculated later in _calculate_caverns_monuments()
            }

def _parse_caverns_gambit(account, raw_caverns_list):
    cavern_name = caverns_cavern_names[14]

    # Pts
    account.caverns['Caverns'][cavern_name]['BasePts'] = 0
    account.caverns['Caverns'][cavern_name]['PtsMulti'] = 1
    account.caverns['Caverns'][cavern_name]['TotalPts'] = 0

    # Challenges
    account.caverns['Caverns'][cavern_name]['Challenges'] = {}
    challenge_index_offset = 65  # Taken from  _customBlock_Holes2."GambitPts"
    raw_challenge_times = []
    for i in range(caverns_gambit_total_challenges):
        try:
            raw_challenge_times.append(raw_caverns_list[11][i + challenge_index_offset])
        except:
            logger.exception(f"Could not retrieve Caverns > Gambit > {caverns_gambit_challenge_names[i]} score")
            raw_challenge_times.append(0)

    for challenge_index, challenge_name in enumerate(caverns_gambit_challenge_names):
        base_value = 100 if challenge_index == 0 else 200
        base_pts = (
            base_value * (
                raw_challenge_times[challenge_index]  #1 point per second
                + (3 * floor(raw_challenge_times[challenge_index] / 10))  #3 points per 10 seconds
                + (10 * floor(raw_challenge_times[challenge_index] / 60))  #10 points per 60 seconds
            )
        )
        account.caverns['Caverns'][cavern_name]['BasePts'] += base_pts
        try:
            unlocked = (
                True if schematics_unlocking_gambit_challenges[challenge_index] is None else
                account.caverns['Schematics'][schematics_unlocking_gambit_challenges[challenge_index]]['Purchased']
            )
        except:
            unlocked = False
        account.caverns['Caverns'][cavern_name]['Challenges'][challenge_name] = {
            'Seconds': raw_challenge_times[challenge_index],
            'TimeDisplay': f"{raw_challenge_times[challenge_index] // 60:.0f}min {raw_challenge_times[challenge_index] % 60:.1f}sec",
            'BasePts': base_pts,
            'Unlocked': unlocked,
            'Image': 'engineer-schematic-78' if challenge_index == 0 else f'engineer-schematic-{88 + challenge_index}'
        }

    # Bonuses
    account.caverns['Caverns'][cavern_name]['Bonuses'] = {}
    for bonus_index, bonus_details in enumerate(caverns_gambit_pts_bonuses):
        details_list = bonus_details.split('|')
        clean_name = details_list[3].replace('_', ' ').replace('梦', '').replace('(TAP ME)', '').replace('而', 'x').strip().strip("'")
        clean_description = details_list[2].replace('_', ' ').strip().strip("'")
        if clean_description == 'no':
            clean_description = ''
        pts_required = 2e3 + 1e3 * (bonus_index + 1) * (1 + bonus_index / 5) * safer_math_pow(1.26, bonus_index)
        account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index] = {
            'ScalingValue': safer_convert(details_list[0], 0),
            'ScalesWithPts': safer_convert(details_list[1], False),
            'Description': clean_description,
            'Name': clean_name,
            'PtsRequired': pts_required,
            'Unlocked': False,  #Fixed later in account_calcs._calculate_caverns_gambit(),
            'Image': f'gambit-bonus-{bonus_index}'
        }

def _parse_caverns_the_temple(account, raw_caverns_list):
    cavern_name = caverns_cavern_names[15]
    try:
        account.caverns['Caverns'][cavern_name]['Torches Owned'] = safer_convert(raw_caverns_list[11][56], 0.0)
    except:
        account.caverns['Caverns'][cavern_name]['Torches Owned'] = 0.0
    try:
        account.caverns['Caverns'][cavern_name]['Illuminate'] = safer_convert(raw_caverns_list[11][57], 0)
    except:
        account.caverns['Caverns'][cavern_name]['Illuminate'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['Amplify'] = safer_convert(raw_caverns_list[11][59], 0)
    except:
        account.caverns['Caverns'][cavern_name]['Amplify'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['Golems Killed'] = safer_convert(raw_caverns_list[11][63], 0.0)
    except:
        account.caverns['Caverns'][cavern_name]['Golems Killed'] = 0.0

def _parse_w6(account):
    _parse_w6_farming(account)
    _parse_w6_summoning(account)


def _parse_w6_farming(account):
    account.farming = {
        'MagicBeans': 0,
        'Crops': {},
        'CropCountsPerSeed': {
            'Basic': 0,
            'Earthy': 0,
            'Bulbo': 0,
            'Sushi': 0,
            'Mushie': 0,
            'Glassy': 0,
        },
        "CropsUnlocked": 0,
        "MarketUpgrades": {},
        "CropStacks": {
            "Evolution Gmo": 0,  # 200
            "Speed Gmo": 0,  # 1,000
            "Exp Gmo": 0,  # 2,500
            "Value Gmo": 0,  # 10,000
            "Super Gmo": 0  # 100,000
        },
        'LandRankDatabase': {},
        'Depot': {},
    }

    raw_farmcrop_dict = safe_loads(account.raw_data.get("FarmCrop", {}))
    if not raw_farmcrop_dict:
        logger.warning(f"Farming Crop data not present{', as expected' if account.version < 200 else ''}.")
    _parse_w6_farming_crops(account, raw_farmcrop_dict)
    _parse_w6_farming_crop_depot(account)

    raw_farmupg_list = safe_loads(account.raw_data.get("FarmUpg", []))
    if not raw_farmupg_list:
        logger.warning(f"Farming Markets data not present{', as expected' if account.version < 200 else ''}.")
    _parse_w6_farming_markets(account, raw_farmupg_list)

    raw_farmrank_list = safe_loads(account.raw_data.get("FarmRank"))
    if raw_farmrank_list is None:
        logger.warning(f"Farming Land Rank Database data not present{', as expected' if account.version < 219 else ''}.")
        raw_farmrank_list = [0] * 36
    _parse_w6_farming_land_ranks(account, raw_farmrank_list)

    account.farming['Total Plots'] = (
        1
        + account.farming['MarketUpgrades']['Land Plots']['Level']
        + account.gemshop['Purchases']['Plot Of Land']['Owned']
        + min(3, account.merits[5][2]['Level'])
    )

def _parse_w6_farming_crops(account, rawCrops):
    for cropIndexStr, cropAmountOwned in rawCrops.items():
        try:
            account.farming["CropsUnlocked"] += 1  # Once discovered, crops will always appear in this dict.
            if int(cropIndexStr) < 21:
                account.farming['CropCountsPerSeed']['Basic'] += 1
            elif int(cropIndexStr) < 46:
                account.farming['CropCountsPerSeed']['Earthy'] += 1
            elif int(cropIndexStr) < 61:
                account.farming['CropCountsPerSeed']['Bulbo'] += 1
            elif int(cropIndexStr) < 84:
                account.farming['CropCountsPerSeed']['Sushi'] += 1
            elif int(cropIndexStr) < 107:
                account.farming['CropCountsPerSeed']['Mushie'] += 1
            else:
                account.farming['CropCountsPerSeed']['Glassy'] += 1
            account.farming['Crops'][int(cropIndexStr)] = float(cropAmountOwned)
            if float(cropAmountOwned) >= 200:
                account.farming["CropStacks"]["Evolution Gmo"] += 1
            if float(cropAmountOwned) >= 1000:
                account.farming["CropStacks"]["Speed Gmo"] += 1
            if float(cropAmountOwned) >= 2500:
                account.farming["CropStacks"]["Exp Gmo"] += 1
            if float(cropAmountOwned) >= 10000:
                account.farming["CropStacks"]["Value Gmo"] += 1
            if float(cropAmountOwned) >= 100000:
                account.farming["CropStacks"]["Super Gmo"] += 1
        except:
            continue

def _parse_w6_farming_crop_depot(account):
    for bonusIndex, bonusDetails in crop_depot_dict.items():
        account.farming['Depot'][bonusIndex] = {
            'BonusString': bonusDetails['BonusString'],
            'Image': bonusDetails['Image'],
            'ScalingType': bonusDetails['funcType'],
            'ScalingNumber': bonusDetails['x1'],
            'Unlocked': account.sneaking.emporium[bonusDetails['EmporiumUnlockName']].obtained,
            'BaseValue': lava_func(
                bonusDetails['funcType'],
                account.farming['CropsUnlocked'] if bonusIndex != 7 else max(0, account.farming['CropsUnlocked'] - 100),
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'BaseValuePlus1': lava_func(
                bonusDetails['funcType'],
                min(max_farming_crops, account.farming['CropsUnlocked'] + 1) if bonusIndex != 7 else min(max_farming_crops - 100, account.farming['CropsUnlocked'] + 1),
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'MaxValue': lava_func(
                bonusDetails['funcType'],
                max_farming_crops,
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'Value': 0,
            'ValuePlus1': 0,
        }

def _parse_w6_farming_markets(account, rawMarkets):
    try:
        account.farming['MagicBeans'] = int(float(rawMarkets[1]))
    except:
        pass
    for marketUpgradeIndex, marketUpgrade in enumerate(market_upgrade_details):
        try:
            account.farming["MarketUpgrades"][marketUpgrade[0].replace('_', ' ').title()] = {
                'Level': rawMarkets[marketUpgradeIndex + 2],
                'Description': marketUpgrade[1].replace('_', ' '),
                'Value': rawMarkets[marketUpgradeIndex + 2] * float(marketUpgrade[8]),
                'StackedValue': rawMarkets[marketUpgradeIndex + 2] * float(marketUpgrade[8]),  # Updated later in calculate function
                'UpgradesAtSameCrop': int(marketUpgrade[2]),
                'CropTypeValue': float(marketUpgrade[3]),
                'BaseCost': int(marketUpgrade[4]),
                'CostIncrement': float(marketUpgrade[5]),
                'UnlockRequirement': int(marketUpgrade[6]),
                'MaxLevel': int(marketUpgrade[7]),
                'BonusPerLevel': float(marketUpgrade[8]),
                'MarketType': 'Day' if marketUpgradeIndex < 8 else 'Night'
            }
        except:
            account.farming["MarketUpgrades"][marketUpgrade[0].replace('_', ' ').title()] = {
                'Level': 0,
                'Description': marketUpgrade[1].replace('_', ' '),
                'Value': 0,
                'StackedValue': 0,  # Updated later in calculate function
                'UpgradesAtSameCrop': marketUpgrade[2],
                'CropTypeValue': marketUpgrade[3],
                'BaseCost': marketUpgrade[4],
                'CostIncrement': marketUpgrade[5],
                'UnlockRequirement': marketUpgrade[6],
                'MaxLevel': marketUpgrade[7],
                'BonusPerLevel': marketUpgrade[8],
                'MarketType': 'Day' if marketUpgradeIndex < 8 else 'Night'
            }

def _parse_w6_farming_land_ranks(account, rawRanks):
    try:
        account.farming['LandRankPlotRanks'] = rawRanks[0]
        account.farming['LandRankTotalRanks'] = sum(rawRanks[0])
        account.farming['LandRankMinPlot'] = min([v for v in rawRanks[0] if v > 0], default=0)
        account.farming['LandRankMaxPlot'] = max(rawRanks[0], default=0)
    except:
        account.farming['LandRankPlotRanks'] = [0] * 36
        account.farming['LandRankTotalRanks'] = 0
        account.farming['LandRankMinPlot'] = 0
        account.farming['LandRankMaxPlot'] = 0
    for upgradeIndex, upgradeValuesDict in landrank_dict.items():
        try:
            account.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                'Level': rawRanks[2][upgradeIndex],
                'BaseValue': upgradeValuesDict['Value'],
                'Value': 0,  #Updated in account_calcs._calculate_w6_farming_land_ranks()
                'Index': upgradeIndex
            }
        except:
            account.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                'Level': 0,
                'BaseValue': upgradeValuesDict['Value'],
                'Value': 0,
                'Index': upgradeIndex
            }

def _parse_w6_summoning(account):
    account.summoning = {}
    raw_summoning_list = safe_loads(account.raw_data.get('Summon', []))
    if not raw_summoning_list:
        logger.warning(f"Summoning data not present{', as expected' if account.version < 200 else ''}.")
    while len(raw_summoning_list) < 5:
        raw_summoning_list.append([])

    # Summoning Upgrade doublers
    raw_caverns_list = safe_loads(account.raw_data.get('Holes', []))
    try:
        raw_doubled_upgrades = [int(entry) for entry in raw_caverns_list[28] if int(entry) >= 0]
    except:
        raw_doubled_upgrades = []
    account.summoning['Doubled Upgrades'] = len(raw_doubled_upgrades)

    # raw_summoning_list[0] = Upgrades
    account.summoning['Upgrades'] = {}
    if raw_summoning_list[0]:
        raw_upgrades = raw_summoning_list[0]
    else:
        raw_upgrades = [0] * max_summoning_upgrades
    while len(raw_upgrades) < max_summoning_upgrades:
        raw_upgrades.append(0)
    for upg_index, upg_details in enumerate(summoning_upgrades):
        upg_name = upg_details[3].replace('_', ' ')
        locked_behind_index = int(upg_details[9])
        try:
            account.summoning['Upgrades'][upg_name] = {
                'Image': f'summoning-upgrade-{upg_index}',
                'Level': raw_upgrades[upg_index],
                'MaxLevel': int(upg_details[8]),
                'UpgradeIndex': upg_index,
                'Doubled': upg_index in raw_doubled_upgrades,
                'Color': summoning_regular_match_colors[int(upg_details[2])],
                'LockedBehindIndex': locked_behind_index,
                'LockedBehindName': summoning_upgrades[locked_behind_index][3].replace('_', ' '),
                'Unlocked': locked_behind_index < 0
            }
        except:
            logger.exception(f"Summoning Upgrade problemo")
            account.summoning['Upgrades'][upg_name] = {
                'Image': f'summoning-upgrade-{upg_index}',
                'Level': 0,
                'MaxLevel': int(upg_details[8]),
                'UpgradeIndex': upg_index,
                'Doubled': upg_index in raw_doubled_upgrades,
                'Color': summoning_regular_match_colors[int(upg_details[2])],
                'LockedBehindIndex': locked_behind_index,
                'LockedBehindName': summoning_upgrades[int(upg_details[10])][3].replace('_', ' '),
                'Unlocked': locked_behind_index < 0
            }

    for upg_name, upg_details in account.summoning['Upgrades'].items():
        if not account.summoning['Upgrades'][upg_name]['Unlocked']:
            account.summoning['Upgrades'][upg_name]['Unlocked'] = (
                #Check if own level is greater than 0
                account.summoning['Upgrades'][upg_name]['Level'] > 0
                #or the level of the upgrade it was locked behind having at least 1 level into it
                or account.summoning['Upgrades'][summoning_upgrades[upg_details['LockedBehindIndex']][3].replace('_', ' ')]['Level'] >= 1
            )

    # raw_summoning_list[1] = List of codified names of enemies from battles won
    account.summoning["Battles"] = {}
    account.summoning["BattleDetails"] = {}
    for color in summoning_dict:
        account.summoning["BattleDetails"][color] = {}
    _parse_w6_summoning_battles(account, raw_summoning_list[1])

    # Endless Summoning
    account.summoning["BattleDetails"]['Endless'] = {}
    _parse_w6_summoning_battles_endless(account)

    # raw_summoning_list[2] looks to be essence owned
    # raw_summoning_list[3] I have no idea what this is

    # raw_summoning_list[4] = list[int] familiars in the Sanctuary, starting with Slime in [0], Vrumbi in [1], etc.
    account.summoning['SanctuaryTotal'] = 0
    _parse_w6_summoning_sanctuary(account, raw_summoning_list[4])

    # Used later to create a list of Advices for Winner Bonuses. Can be added directly into an AdviceGroup as the advices attribute
    account.summoning['WinnerBonusesAdvice'] = []

    account.summoning['Summoning Stones'] = {}
    raw_kr_best = safe_loads(account.raw_data.get('KRbest', {}))
    if raw_kr_best:
        for color_index in range(len(summoning_regular_match_colors)):
            color = summoning_regular_match_colors[color_index]
            # TODO: remove this if/continue once the Teal Summoning Stone exists
            if color == "Teal":
                continue
            wins = safer_get(raw_kr_best, f'SummzTrz{color_index}', 0)
            account.summoning['Summoning Stones'][color] = {
                'Wins': wins,
                'Location': summoning_stone_locations[color_index],
                'Base HP': int(summoning_stone_boss_base_hp[color_index]),
                'Base DMG': int(summoning_stone_boss_base_damage[color_index]),
                'StoneImage': summoning_stone_stone_images[color_index],
                'BossImage': summoning_stone_boss_images[color_index]
            }

def _parse_w6_summoning_battles(account, raw_battles):
    safe_battles = [safer_convert(battle, '') for battle in raw_battles]
    regular_battles = [battle for battle in safe_battles if battle in summoning_regular_battles]
    account.summoning['Battles']['RegularTotal'] = len(regular_battles)
    account.summoning['AllRegularBattlesWon'] = len(regular_battles) >= len(summoning_regular_battles)
    # Endless doesn't follow the same structure as the once-only battles
    account.summoning['Battles']['Endless'] = safer_get(account.raw_optlacc_dict, 319, 0)
    account.summoning['Bonuses'] = {}

    for color_name, color_dict in summoning_dict.items():
        if color_name in summoning_regular_match_colors:
            account.summoning['Battles'][color_name] = sum([battle_values_dict['EnemyID'] in raw_battles for battle_values_dict in color_dict.values()])
            for battle_index, battle_values_dict in color_dict.items():
                this_battle = {
                    'Defeated': battle_values_dict['EnemyID'] in raw_battles,
                    'Image': battle_values_dict['Image'],
                    'RewardType': battle_values_dict['RewardID'],
                    'RewardQTY': battle_values_dict['RewardQTY'],
                    'RewardBaseValue': battle_values_dict['RewardQTY'] * 3.5,
                    'OpponentName': battle_values_dict['OpponentName']
                }
                if this_battle['RewardType'].startswith('+{ '):
                    this_battle['Description'] = this_battle['RewardType'].replace('+{ ', f"+{this_battle['RewardBaseValue']} ")
                elif this_battle['RewardType'].startswith('+{%'):
                    this_battle['Description'] = this_battle['RewardType'].replace('{', f"{this_battle['RewardBaseValue']}")
                elif this_battle['RewardType'].startswith('<x'):
                    this_battle['Description'] = this_battle['RewardType'].replace('<', f"{round(ValueToMulti(this_battle['RewardBaseValue']), 4):g}")
                account.summoning['BattleDetails'][color_name][battle_index + 1] = this_battle
                if this_battle['RewardType'] not in account.summoning['Bonuses']:
                    account.summoning['Bonuses'][this_battle['RewardType']] = {'Value': 0, 'Max': 0}
                account.summoning['Bonuses'][this_battle['RewardType']]['Value'] += this_battle['RewardBaseValue'] * this_battle['Defeated']
                account.summoning['Bonuses'][this_battle['RewardType']]['Max'] += this_battle['RewardBaseValue']
    #logger.debug(f"Base Regular Bonuses: {account.summoning['Bonuses']}")

def _parse_w6_summoning_battles_endless(account):
    account.summoning['Endless Bonuses'] = {}
    true_battle_index = 0
    while true_battle_index < max(40, account.summoning['Battles']['Endless'] + 20):
        image_index = min(4, true_battle_index // 20)
        endless_enemy_index = true_battle_index % 40
        this_battle = {
            'Defeated': true_battle_index < account.summoning['Battles']['Endless'],
            'Image': summoning_dict['Endless'][image_index]['Image'],
            'RewardType': summoning_endlessDict.get(endless_enemy_index, {}).get('RewardID', 'Unknown'),
            'Challenge': summoning_endlessDict.get(endless_enemy_index, {}).get('Challenge', 'Unknown'),
            # 'RewardQTY': summoning_endlessDict.get(endless_enemy_index, {}).get('RewardQTY', 0),
            'RewardBaseValue': (
                summoning_endlessDict.get(endless_enemy_index, {}).get('RewardQTY', 0)
            )
        }
        if this_battle['RewardType'].startswith('+{ '):
            this_battle['Description'] = this_battle['RewardType'].replace('+{ ', f"+{this_battle['RewardBaseValue']} ")
        elif this_battle['RewardType'].startswith('+{%'):
            this_battle['Description'] = this_battle['RewardType'].replace('{', f"{this_battle['RewardBaseValue']}")
        elif this_battle['RewardType'].startswith('<x'):
            this_battle['Description'] = this_battle['RewardType'].replace('<', f"{round(ValueToMulti(this_battle['RewardBaseValue']), 4):g}")
        account.summoning['BattleDetails']['Endless'][true_battle_index + 1] = this_battle
        if this_battle['RewardType'] not in account.summoning['Endless Bonuses']:
            account.summoning['Endless Bonuses'][this_battle['RewardType']] = 0
        account.summoning['Endless Bonuses'][this_battle['RewardType']] += this_battle['RewardBaseValue'] * this_battle['Defeated']
        # logger.debug(f"Endless {true_battle_index + 1}: {account.summoning['BattleDetails']['Endless'][true_battle_index + 1]}")
        true_battle_index += 1
    # logger.debug(f"Base Endless Bonuses after {account.summoning['Battles']['Endless']} wins: {account.summoning['Endless Bonuses']}")

def _parse_w6_summoning_sanctuary(account, rawSanctuary):
    # [2,3,2,1,1,0,0,0,0,0,0,0,0,0]
    while len(rawSanctuary) < 14:
        rawSanctuary.append(0)
    for index, value in enumerate(summoning_sanctuary_counts):
        try:
            account.summoning['SanctuaryTotal'] += value * safer_convert(rawSanctuary[index], 0)
        except Exception as e:
            logger.warning(f"Summoning Sanctuary Parse error at index {index}: {e}. Not adding anything.")

def _parse_w7(account):
    _parse_advice_for_money(account)
    _parse_w7_coral_reef(account)
    _parse_w7_legend_talents(account)

def _parse_advice_for_money(account):
    # Dependencies: None
    advice_for_money_upgrade_data = Spelunky[18]
    try:
        advice_for_money_account_data = safe_loads(account.raw_data.get('Spelunk', []))[11]
    except:
        advice_for_money_account_data = []

    for index, (upgrade_data, upgrade_level) in enumerate(zip(advice_for_money_upgrade_data, advice_for_money_account_data)):
        name, description_and_effect, bonus, cost,  _ = upgrade_data.split(',')
        name = name.replace('_', ' ')
        description, effect = description_and_effect.split('@')
        description = description.replace('_', ' ').strip()
        effect = effect.replace('_', ' ').strip()
        account.advice_for_money['Upgrades'][name] = {
            'Description': description,
            'Effect': effect,
            'Level': int(upgrade_level),
            'Bonus': int(bonus),
            'Cost': int(cost),
            'Index': index,
        }


def _parse_w7_coral_reef(account):
    # Dependencies: None
    town_corals_count = safer_index(safer_index(safe_loads(account.raw_data.get('Spelunk', [])),4, []), 5, 0)
    account.coral_reef['Town Corals'] = town_corals_count

    unlocked_reef_corals = safer_index(safe_loads(account.raw_data.get('Spelunk', [])),12 , [])
    coral_levels = safer_index(safe_loads(account.raw_data.get('Spelunk', [])), 13, [])

    for index, coral_data in enumerate(account.coral_reef['Reef Corals'].values()):
        coral_data['Unlocked'] = bool(safer_index(unlocked_reef_corals, index, False))
        coral_data['Level'] = safer_index(coral_levels, index, 0)

def _parse_w7_legend_talents(account):
    # Dependencies: None
    legend_talents_levels = safer_index(safe_loads(account.raw_data.get('Spelunk', [])), 18, [])
    for index, talent_data in enumerate(account.legend_talents['Talents'].values()):
        talent_data['Level'] = safer_index(legend_talents_levels, index, 0)