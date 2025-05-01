import copy
from collections import defaultdict
from math import floor
from flask import g
from consts import (
    # General
    lavaFunc, ValueToMulti, items_codes_and_names,
    maxCharacters,
    gfood_codes,
    card_data, card_raw_data, cardset_names, decode_enemy_name,
    gemShopDict, gem_shop_optlacc_dict, gem_shop_bundles_dict,
    guildBonusesList, familyBonusesDict, achievementsList, allMeritsDict, starsignsDict,
    event_points_shop_dict,
    npc_tokens,
    companions,
    # Master Classes
    grimoire_upgrades_list, grimoire_bones_list, grimoire_dont_scale,
    compass_upgrades_list, compass_dusts_list, compass_path_ordering, compass_titans, compass_medallions,
    # W1
    stampsDict, stampTypes, bribesDict,
    forgeUpgradesDict,
    statuesDict, statueTypeList, statueCount,
    vault_upgrades_list, vault_stack_types, vault_dont_scale, vault_section_indexes,
    # W2
    bubblesDict, max_IndexOfImplementedBubbles,
    vialsDict, max_IndexOfVials, getReadableVialNames, max_VialLevel,
    sigilsDict,
    arcadeBonuses, arcade_max_level,
    ballotDict,
    obolsDict, ignorable_obols_list,
    islands_dict, killroy_dict,
    # W3
    refineryDict, buildingsDict, saltLickList, atomsList, colliderStorageLimitList, buildings_shrines, prayersDict,
    equinoxBonusesDict, max_implemented_dreams, dreamsThatUnlockNewBonuses,
    printerAllIndexesBeingPrinted,
    apocableMapIndexDict, apocAmountsList, apocNamesList, dn_miniboss_names, dn_miniboss_skull_requirement_list, dnSkullValueList, getSkullNames,
    # W4
    riftRewardsDict,
    labJewelsDict, labBonusesDict, labChipsDict,
    maxMealCount, maxMealLevel, cookingMealDict, maxCookingTables,
    maxNumberOfTerritories, territoryNames, slotUnlockWavesList, breedingUpgradesDict, breedingGeneticsList,
    breedingShinyBonusList, breedingSpeciesDict, getShinyLevelFromDays, getDaysToNextShinyLevel, getBreedabilityMultiFromDays, getBreedabilityHeartFromMulti,
    # W5
    sailingDict, captainBuffs,
    getStyleNameFromIndex, divinity_divinitiesDict, getDivinityNameFromIndex, gamingSuperbitsDict,
    # W6
    jade_emporium, pristineCharmsList, sneaking_gemstones_all_values, getGemstoneBaseValue, getGemstonePercent,
    marketUpgradeDetails, landrankDict, cropDepotDict, maxFarmingCrops, summoningBattleCountsDict, summoningDict, summoning_endlessEnemies,
    summoning_endlessDict, max_summoning_upgrades, summoning_sanctuary_counts, summoning_upgrades, summoning_match_colors,
    # Caverns
    caverns_villagers, caverns_conjuror_majiks, caverns_engineer_schematics, caverns_engineer_schematics_unlock_order, caverns_cavern_names,
    caverns_measurer_measurements, caverns_measurer_HI55, getCavernResourceImage, max_buckets, max_sediments, sediment_bars, getVillagerEXPRequired,
    monument_bonuses, bell_clean_improvements, bell_ring_bonuses, getBellExpRequired, getGrottoKills, lamp_wishes, key_cards, getWishCost,
    schematics_unlocking_harp_chords, harp_chord_effects, max_harp_notes, lamp_world_wish_values, caverns_librarian_studies,
    caverns_jar_max_rupies, caverns_jar_collectibles_count, caverns_jar_collectibles, caverns_jar_jar_types, caverns_jar_max_jar_types,
    caverns_gambit_pts_bonuses, caverns_gambit_challenge_names, caverns_gambit_total_challenges, schematics_unlocking_gambit_challenges,
)
from models.models import Character, buildMaps, EnemyWorld, Card, Assets
from utils.data_formatting import getCharacterDetails, safe_loads, safer_get, safer_convert
from utils.logging import get_logger
from utils.text_formatting import getItemDisplayName, numberToLetter

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
            enemy_decoded_name = decode_enemy_name(card_info[0])
            if enemy_decoded_name.startswith('Unknown'):
                unknown_cards.append(card_info[0])
            parsed_card_data[enemy_decoded_name] = {
                'Card Name': card_info[0],
                'Enemy Name': enemy_decoded_name,
                'Cards For 1star': safer_convert(card_info[2], 1.0),
                'Description': card_info[3].replace('_', ' '),
                'Value per Level': safer_convert(card_info[4], 0.0),
                'Set Name': cardset_name
            }

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
    # cards = [
    #     Card(codename, name, cardset, safer_get(card_counts, codename, 0), coefficient)
    #     for cardset, cards in card_data.items()
    #     for codename, (name, coefficient) in cards.items()
    # ]

    # unknown_cards = [
    #     codename for codename in card_counts if not any(codename in items for items in card_data.values())
    # ]
    if unknown_cards:
        logger.warning(f"Unknown Card name(s) found: {unknown_cards}")

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
                all_stuff_stored_or_in_inv[name] = int(count)
            else:
                all_stuff_stored_or_in_inv[name] += int(count)

    return Assets(all_stuff_stored_or_in_inv)


def _all_worn_items(account) -> Assets:
    stuff_worn = defaultdict(int)
    for toon in account.safe_characters:
        for item in [*toon.equipment.foods, *toon.equipment.equips]:
            if item.codename == 'Blank':
                continue
            stuff_worn[item.codename] += item.amount

    return Assets(stuff_worn)

def parse_account(account, run_type):
    _parse_wave_1(account, run_type)

def _parse_wave_1(account, run_type):
    _parse_switches(account)
    _parse_companions(account)
    _parse_characters(account, run_type)
    _parse_general(account)
    _parse_master_classes(account)
    _parse_w1(account)
    _parse_w2(account)
    _parse_w3(account)
    _parse_w4(account)
    _parse_w5(account)
    _parse_caverns(account)
    _parse_w6(account)

def _parse_switches(account):
    # AutoLoot
    if g.autoloot:
        account.autoloot = True
    elif account.raw_data.get("AutoLoot", 0) == 1 or safe_loads(account.raw_data.get('BundlesReceived', {})).get('bun_i', 0) == 1:
        account.autoloot = True
        g.autoloot = True
    else:
        account.autoloot = False

    account.maxSubgroupsPerGroup = 1 if g.overwhelmed else 3
    account.library_group_characters = g.library_group_characters

def _parse_companions(account):
    # Companions v2
    account.companions = {}

    # Read the player's data to capture all unique Companion IDs
    simplified_companion_set = set()
    # If the data comes from Toolbox, it'll be a dictionary called companion singular
    raw_companion = account.raw_data.get('companion', None)
    # If the data comes from Efficiency, it'll be a flat list of just companion ID: "companions": [7, 10, 4, 5, 9, 2, 3, 6]
    raw_companions = account.raw_data.get('companions', None)
    if raw_companion is not None:
        account.companions['Companion Data Present'] = True
        for companionInfo in raw_companion.get('l', []):
            try:
                companionID = int(companionInfo.split(',')[0])
                simplified_companion_set.add(companionID)
            except:
                continue
    elif raw_companions is not None:
        account.companions['Companion Data Present'] = True
        for companionID in raw_companions:
            simplified_companion_set.add(companionID)
    else:
        account.companions['Companion Data Present'] = False
        logger.debug(f"No companion data present in JSON. Relying only on Switches")

    # Match the Companion IDs to their names
    for c_index, c_name in enumerate(companions):
        account.companions[c_name] = c_index in simplified_companion_set

    # Account for the manual entries in the Switches
    try:
        account.companions['King Doot'] = account.companions['King Doot'] or g.doot
        account.companions['Rift Slug'] = account.companions['Rift Slug'] or g.riftslug
        account.companions['Sheepie'] = account.companions['Sheepie'] or g.sheepie
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
    account.max_toon_count = max(maxCharacters, character_count)  # OPTIMIZE: find a way to read this from somewhere
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

    account.wws = [toon for toon in account.all_characters if 'Wind Walker' in toon.all_classes]

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
    _parse_general_upgrade_vault(account)

def _parse_general_gem_shop(account):
    account.gemshop = {}
    raw_gem_items_purchased = safe_loads(account.raw_data.get("GemItemsPurchased", []))
    for purchaseName, purchaseIndex in gemShopDict.items():
        try:
            account.gemshop[purchaseName] = safer_convert(raw_gem_items_purchased[purchaseIndex], 0)
        except Exception as e:
            logger.warning(f"Gemshop Parse error with purchaseIndex {purchaseIndex}: {e}. Defaulting to 0")
            account.gemshop[purchaseName] = 0

    account.minigame_plays_daily = 5 + (4 * account.gemshop['Daily Minigame Plays'])

def _parse_general_gem_shop_optlacc(account):
    for purchase_name, details in gem_shop_optlacc_dict.items():
        try:
            account.gemshop[purchase_name] = safer_convert(safer_get(account.raw_optlacc_dict, details[0], 0), 0)
        except Exception as e:
            if max(account.raw_optlacc_dict.keys()) < details[0]:
                logger.info(f"Error parsing {purchase_name} because optlacc_index {details[0]} not present in JSON. Defaulting to 0")
            else:
                logger.exception(f"Error parsing {purchase_name} at optlacc_index {details[0]}: Could not convert {account.raw_optlacc_dict.get(details[0])} to int")
                account.gemshop[purchase_name] = 0

def _parse_general_gem_shop_bundles(account):
    raw_gem_shop_bundles = safe_loads(account.raw_data.get('BundlesReceived', []))
    account.gemshop['Bundle Data Present'] = 'BundlesReceived' in account.raw_data
    account.gemshop['Bundles'] = {}
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

def _parse_class_unique_kill_stacks(account):
    account.dk_orb_kills = safer_get(account.raw_optlacc_dict, 138, 0)
    account.sb_plunder_kills = safer_get(account.raw_optlacc_dict, 139, 0)
    account.es_wormhole_kills = safer_get(account.raw_optlacc_dict, 152, 0)

def _parse_family_bonuses(account):
    account.family_bonuses = {}
    for className in familyBonusesDict.keys():
        # Create the skeleton for all current classes, with level and value of 0
        account.family_bonuses[className] = {'Level': 0, 'Value': 0}
    for char in account.safe_characters:
        for className in [char.base_class, char.sub_class, char.elite_class]:
            if className in familyBonusesDict:
                if char.combat_level > account.family_bonuses[className]['Level']:
                    account.family_bonuses[className]['Level'] = char.combat_level
    for className in account.family_bonuses.keys():
        try:
            account.family_bonuses[className]['Value'] = lavaFunc(
                familyBonusesDict[className]['funcType'],
                account.family_bonuses[className]['Level'] - min(familyBonusesDict[className]['levelDiscount'], account.family_bonuses[className]['Level']),
                familyBonusesDict[className]['x1'],
                familyBonusesDict[className]['x2'])
        except:
            logger.exception(f"Error parsing Family Bonus for {className}. Defaulting to 0 value")
            account.family_bonuses[className]['Value'] = 0
        account.family_bonuses[className]['DisplayValue'] = (
            f"{'+' if familyBonusesDict[className]['PrePlus'] else ''}"
            f"{account.family_bonuses[className]['Value']:.2f}"
            f"{familyBonusesDict[className]['PostDisplay']}"
            f" {familyBonusesDict[className]['Stat']}"
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
    if len(raw_reg_achieves) < len(achievementsList):
        logger.warning(f"Achievements list shorter than expected by {len(achievementsList) - len(raw_reg_achieves)}. "
                       f"Likely old data. Defaulting them all to Incomplete.")
        while len(raw_reg_achieves) < len(achievementsList):
            raw_reg_achieves.append(0)

    for achieveIndex, achieveData in enumerate(achievementsList):
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
    account.guildBonuses = {}
    raw_guild = safe_loads(account.raw_data.get('Guild', [[]]))
    for bonusIndex, bonusName in enumerate(guildBonusesList):
        try:
            account.guildBonuses[bonusName] = safer_convert(raw_guild[0][bonusIndex], 0)
        except Exception as e:
            logger.warning(f"Guild Bonus Parse error: {e}. Defaulting to 0")
            account.guildBonuses[bonusName] = 0

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
            if sampleIndex in printerAllIndexesBeingPrinted:
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

def _parse_general_upgrade_vault(account):
    account.vault = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Knockout Stacks': safer_get(account.raw_optlacc_dict, 338, 0),
    }
    #Parse Vault Upgrades
    raw_vault = safe_loads(account.raw_data.get('UpgVault', []))
    if not raw_vault:
        logger.warning(f"Upgrade Vault data not present{', as expected' if account.version < 237 else ''}.")
    for upgrade_index, upgrade_values_list in enumerate(vault_upgrades_list):
        clean_name = upgrade_values_list[0].replace('(Tap_for_more_info)', '').replace('(Tap_for_Info)', '').replace('製', '').replace('_', ' ').rstrip()
        if clean_name.split('!')[0] in vault_stack_types:
            stack_type = clean_name.split('!')[0]
            clean_name += f" ({account.vault.get(f'{stack_type} Stacks', '#')} stacks)"
        for list_index, vault_section_index in enumerate(vault_section_indexes):
            if upgrade_index <= vault_section_index:
                vault_section = list_index+1
                break
        try:
            account.vault['Upgrades'][clean_name] = {
                'Level': int(raw_vault[upgrade_index]),
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
                'Description': (
                    f"{upgrade_values_list[9].replace('_', ' ')}"
                    f"<br>{upgrade_values_list[10].replace('_', ' ') if len(upgrade_values_list) >= 10 else ''}"
                ),
                'Scaling Value': upgrade_index not in vault_dont_scale,
                'Vault Section': vault_section
            }
        except Exception as e:
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
                'Description': (
                    f"{upgrade_values_list[9].replace('_', ' ')}"
                    f"<br>{upgrade_values_list[10].replace('_', ' ') if len(upgrade_values_list) >= 10 else ''}"
                ),
                'Scaling Value': upgrade_index not in vault_dont_scale,
                'Vault Section': vault_section
            }
    #logger.debug(account.vault)

    #Sum total upgrades
    account.vault['Total Upgrades'] = sum([v['Level'] for v in account.vault['Upgrades'].values()])
    for upgrade_name in account.vault['Upgrades']:
        account.vault['Upgrades'][upgrade_name]['Unlocked'] = account.vault['Total Upgrades'] >= account.vault['Upgrades'][upgrade_name]['Unlock Requirement']


def _parse_master_classes(account):
    _parse_master_classes_grimoire(account)
    _parse_master_classes_compass(account)

def _parse_master_classes_grimoire(account):
    account.grimoire = {
        'Upgrades': {},
        'Total Upgrades': 0,
        'Total Bones Collected': safer_get(account.raw_optlacc_dict, 329, 0),
        'Bone1': safer_get(account.raw_optlacc_dict, 330, 0),
        'Bone2': safer_get(account.raw_optlacc_dict, 331, 0),
        'Bone3': safer_get(account.raw_optlacc_dict, 332, 0),
        'Bone4': safer_get(account.raw_optlacc_dict, 333, 0),
        'Knockout Stacks': safer_get(account.raw_optlacc_dict, 334, 0),
        'Elimination Stacks': safer_get(account.raw_optlacc_dict, 335, 0),
        'Annihilation Stacks': safer_get(account.raw_optlacc_dict, 336, 0),
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
                    'Level': int(raw_grimoire[upgrade_index]),
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
            except Exception as e:
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
        'Total Dust Collected': safer_get(account.raw_optlacc_dict, 362, 0),
        'Dust1': safer_get(account.raw_optlacc_dict, 357, 0),
        'Dust2': safer_get(account.raw_optlacc_dict, 358, 0),
        'Dust3': safer_get(account.raw_optlacc_dict, 359, 0),
        'Dust4': safer_get(account.raw_optlacc_dict, 360, 0),
        'Dust5': safer_get(account.raw_optlacc_dict, 361, 0),
        "Top of the Mornin'": max(0, safer_convert(safer_get(account.raw_optlacc_dict, 365, 0),0)),
        'Abominations': {},
        'Elements': {0: 'Fire', 1: 'Wind', 2: 'Grass', 3: 'Ice'},
        'Medallions': {},
        'Total Medallions': 0
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
                    'Level': int(raw_compass_upgrades[upgrade_index]),
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
            except Exception as e:
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
            decoded_name = decode_enemy_name(raw_enemy_name)
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

    for stampType in stampsDict:
        exalted_stamp_type = numberToLetter(stampTypes.index(stampType))
        for stampIndex, stampValuesDict in stampsDict[stampType].items():
            try:
                exalted_stamp_key = f"{exalted_stamp_type}{stampIndex}"
                # if exalted_stamp_key in raw_stamps_exalted:
                #     logger.debug(f"{stampType}{stampIndex} ({exalted_stamp_key}): {stampValuesDict['Name']} is Exalted")
                account.stamps[stampValuesDict['Name']]['Exalted'] = exalted_stamp_key in raw_stamps_exalted
            except:
                if raw_compass:
                    logger.exception(f"Error parsing Exalted status for stamp {stampType}{stampIndex}: {stampValuesDict['Name']}")
                account.stamps[stampValuesDict['Name']]['Exalted'] = False

def _parse_w1(account):
    _parse_w1_starsigns(account)
    _parse_w1_forge(account)
    _parse_w1_bribes(account)
    _parse_w1_stamps(account)
    _parse_w1_owl(account)
    _parse_w1_statues(account)

def _parse_w1_starsigns(account):
    account.star_signs = {}
    account.star_sign_extras = {"UnlockedSigns": 0}
    raw_star_signs = safe_loads(account.raw_data.get("StarSg", {}))
    for signIndex, signValuesDict in starsignsDict.items():
        account.star_signs[signValuesDict['Name']] = {
            'Index': signIndex,
            'Passive': signValuesDict['Passive'],
            '1_Value': signValuesDict.get('1_Value', 0),
            '1_Stat': signValuesDict.get('1_Stat', ''),
            '2_Value': signValuesDict.get('2_Value', 0),
            '2_Stat': signValuesDict.get('2_Stat', ''),
            '3_Value': signValuesDict.get('3_Value', 0),
            '3_Stat': signValuesDict.get('3_Stat', ''),
        }
        try:
            # Some StarSigns are saved as strings "1" to mean unlocked.
            # The names in the JSON also have underscores instead of spaces
            account.star_signs[signValuesDict['Name']]['Unlocked'] = safer_get(raw_star_signs, signValuesDict['Name'].replace(" ", "_"), 0) > 0
            if account.star_signs[signValuesDict['Name']]['Unlocked']:
                account.star_sign_extras['UnlockedSigns'] += 1
        except Exception as e:
            logger.warning(f"Star Sign Parse error at signIndex {signIndex}: {e}. Defaulting to Locked")
            account.star_signs[signValuesDict['Name']]['Unlocked'] = False

def _parse_w1_forge(account):
    account.forge_upgrades = copy.deepcopy(forgeUpgradesDict)
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
    for bribeSet in bribesDict:
        account.bribes[bribeSet] = {}
        for bribeIndex, bribeName in enumerate(bribesDict[bribeSet]):
            try:
                account.bribes[bribeSet][bribeName] = safer_convert(raw_bribes_list[overall_bribe_index], -1)
            except Exception as e:
                logger.warning(f"Bribes Parse error at {bribeSet} {bribeName}: {e}. Defaulting to -1")
                account.bribes[bribeSet][bribeName] = -1  # -1 means unavailable for purchase, 0 means available, and 1 means purchased
            overall_bribe_index += 1

def _parse_w1_stamps(account):
    account.stamps = {}
    account.stamp_totals = {"Total": 0}
    for stampType in stampTypes:
        account.stamp_totals[stampType] = 0
    raw_stamps_list = safe_loads(account.raw_data.get("StampLv", [{}, {}, {}]))
    raw_stamps_dict = {}
    for stampTypeIndex, stampTypeValues in enumerate(raw_stamps_list):
        raw_stamps_dict[int(stampTypeIndex)] = {}
        for stampKey, stampValue in stampTypeValues.items():
            if stampKey != "length":
                raw_stamps_dict[int(stampTypeIndex)][int(stampKey)] = int(stampValue)
    raw_stamp_max_list = safe_loads(account.raw_data.get("StampLvM", {0: {}, 1: {}, 2: {}}))
    raw_stamp_max_dict = {}
    for stampTypeIndex, stampTypeValues in enumerate(raw_stamp_max_list):
        raw_stamp_max_dict[int(stampTypeIndex)] = {}
        for stampKey, stampValue in stampTypeValues.items():
            if stampKey != "length":
                try:
                    raw_stamp_max_dict[int(stampTypeIndex)][int(stampKey)] = int(stampValue)
                except:
                    logger.exception(f"Unexpected stampTypeIndex {stampTypeIndex} or stampKey {stampKey} or stampValue: {stampValue}")
                    try:
                        raw_stamp_max_dict[int(stampTypeIndex)][int(stampKey)] = 0
                        logger.debug(f"Able to set the value of stamp {stampTypeIndex}-{stampKey} to 0. Hopefully no accuracy was lost.")
                    except:
                        logger.exception(f"Couldn't set the value to 0, meaning it was the Index or Key that was bad. You done messed up, cowboy.")
    for stampType in stampsDict:
        for stampIndex, stampValuesDict in stampsDict[stampType].items():
            try:
                account.stamps[stampValuesDict['Name']] = {
                    'Index': stampIndex,
                    'Material': stampValuesDict['Material'],
                    'Level': safer_convert(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0), 0),
                    'Max': safer_convert(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0), 0),
                    'Delivered': safer_convert(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0), 0) > 0,
                    'StampType': stampType,
                    'Value': lavaFunc(
                        stampValuesDict['funcType'],
                        safer_convert(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0), 0),
                        stampValuesDict['x1'],
                        stampValuesDict['x2'],
                    ),
                }
                account.stamp_totals['Total'] += account.stamps[stampValuesDict['Name']]['Level']
                account.stamp_totals[stampType] += account.stamps[stampValuesDict['Name']]['Level']
            except Exception as e:
                logger.warning(f"Stamp Parse error at {stampType} {stampIndex}: {e}. Defaulting to Undelivered")
                account.stamps[stampValuesDict['Name']] = {
                    "Index": stampIndex,
                    "Level": 0,
                    "Max": 0,
                    "Delivered": False,
                    "StampType": stampType,
                    "Value": 0,
                    'Exalted': False
                }
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
    if not raw_statue_type_list:
        raw_statue_type_list = [0] * statueCount
    account.onyx_statues_unlocked = max(raw_statue_type_list, default=0) >= statueTypeList.index("Onyx")
    statue_levels = [0] * statueCount

    # Find the maximum value across all characters. Only matters while Normal, since Gold shares across all characters
    for char in account.safe_characters:
        try:
            char_statues = safe_loads(account.raw_data.get(f"StatueLevels_{char.character_index}"))
            for statueIndex, statueDetails in enumerate(char_statues):
                if statueDetails[0] > statue_levels[statueIndex]:
                    statue_levels[statueIndex] = statueDetails[0]
        except Exception as e:
            logger.warning(f"Per-Character statue level Parse error for Character{char.character_index}: {e}. Skipping them.")
            continue

    for statueIndex, statueDetails in statuesDict.items():
        try:
            account.statues[statueDetails['Name']] = {
                'Level': statue_levels[statueIndex],
                'Type': statueTypeList[raw_statue_type_list[statueIndex]],  # Description: Normal, Gold, Onyx
                'TypeNumber': raw_statue_type_list[statueIndex],  # Integer: 0-2
                'ItemName': statueDetails['ItemName'],
                'Effect': statueDetails['Effect'],
                'BaseValue': statueDetails['BaseValue'],
                'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statue_multi()
                'Farmer': statueDetails['Farmer'],
                'Target': statueDetails['Target'],
            }
        except Exception as e:
            logger.warning(f"Statue Parse error: {e}. Defaulting to level 0")
            account.statues[statueDetails['Name']] = {
                'Level': 0,
                'Type': statueTypeList[raw_statue_type_list[statueIndex]],
                'TypeNumber': raw_statue_type_list[0],
                'ItemName': statueDetails['ItemName'],
                'Effect': statueDetails['Effect'],
                'BaseValue': statueDetails['BaseValue'],
                'Value': statueDetails['BaseValue'],  # Handled in _calculate_w1_statue_multi()
                'Farmer': statueDetails['Farmer'],
                'Target': statueDetails['Target'],
            }
        if account.statues[statueDetails['Name']]['TypeNumber'] >= len(statueTypeList) - 1:
            account.maxed_statues += 1


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

def _parse_w2_vials(account):
    account.alchemy_vials = {}
    manualVialsAdded = 0
    raw_alchemy_vials = safe_loads(account.raw_data.get("CauldronInfo", [0, 0, 0, 0, {}])[4])
    if "length" in raw_alchemy_vials:
        del raw_alchemy_vials["length"]
    while len(raw_alchemy_vials) < max_IndexOfVials:
        raw_alchemy_vials[int(max_IndexOfVials - manualVialsAdded)] = 0
        manualVialsAdded += 1
    if manualVialsAdded:
        logger.warning(f"Vials list shorter than expected by {manualVialsAdded}: Likely old data. Defaulted in level 0s for them all.")
    for vialKey, vialValue in raw_alchemy_vials.items():
        try:
            if int(vialKey) < max_IndexOfVials:
                account.alchemy_vials[getReadableVialNames(vialKey)] = {
                    'Level': int(vialValue),
                    'BaseValue': lavaFunc(
                        vialsDict[int(vialKey)]['funcType'],
                        int(vialValue),
                        vialsDict[int(vialKey)]['x1'],
                        vialsDict[int(vialKey)]['x2'],
                    ),
                    'Material': vialsDict[int(vialKey)]['Material'],
                    'Image': getItemDisplayName(vialsDict[int(vialKey)]['Material'])
                }
        except Exception as e:
            logger.warning(f"Alchemy Vial Parse error at vialKey {vialKey}: {e}. Defaulting to level 0")
            account.alchemy_vials[getReadableVialNames(vialKey)] = {
                'Level': 0,
                'BaseValue': 0,
                'Material': vialsDict[int(vialKey)]['Material'],
                'Image': getItemDisplayName(vialsDict[int(vialKey)]['Material'])
            }

    account.maxed_vials = 0
    for vial in account.alchemy_vials.values():
        if vial.get("Level", 0) >= max_VialLevel:
            account.maxed_vials += 1

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
        account.alchemy_cauldrons["OrangeBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["GreenBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["PurpleBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["YellowBoosts"]: [0, 0, 0, 0]
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
            {k:0 for k in range(0, max_IndexOfImplementedBubbles + 1)},  #+1 to compensate for range() stopping before max
            {k:0 for k in range(0, max_IndexOfImplementedBubbles + 1)},
            {k:0 for k in range(0, max_IndexOfImplementedBubbles + 1)},
            {k:0 for k in range(0, max_IndexOfImplementedBubbles + 1)},
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

    for cauldronIndex in bubblesDict:
        for bubbleIndex in bubblesDict[cauldronIndex]:
            if bubbleIndex <= max_IndexOfImplementedBubbles:  #Don't waste time calculating unimplemented bubbles
                try:
                    account.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']] = {
                        "CauldronIndex": cauldronIndex,
                        "BubbleIndex": bubbleIndex,
                        "Level": all_raw_bubbles[cauldronIndex][bubbleIndex],
                        "BaseValue": lavaFunc(
                            bubblesDict[cauldronIndex][bubbleIndex]["funcType"],
                            all_raw_bubbles[cauldronIndex][bubbleIndex],
                            bubblesDict[cauldronIndex][bubbleIndex]["x1"],
                            bubblesDict[cauldronIndex][bubbleIndex]["x2"]),
                        "Material": getItemDisplayName(bubblesDict[cauldronIndex][bubbleIndex]['Material'])
                    }
                except:
                    account.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']] = {
                        "CauldronIndex": cauldronIndex,
                        "BubbleIndex": bubbleIndex,
                        "Level": 0,
                        "BaseValue": 0.0,
                        "Material": getItemDisplayName(bubblesDict[cauldronIndex][bubbleIndex]['Material'])
                    }

def _parse_w2_p2w(account):
    account.alchemy_p2w = {
        "Sigils": copy.deepcopy(sigilsDict)
    }
    raw_p2w_list = safe_loads(account.raw_data.get("CauldronP2W", []))
    for subElementIndex, subElementValue in enumerate(raw_p2w_list):
        if not isinstance(subElementValue, list):
            raw_p2w_list[subElementIndex] = [subElementValue]
    try:
        account.alchemy_p2w["Cauldrons"] = raw_p2w_list[0]
    except:
        account.alchemy_p2w["Cauldrons"] = [0] * 12
    try:
        account.alchemy_p2w["Liquids"] = raw_p2w_list[1]
    except:
        account.alchemy_p2w["Liquids"] = [0] * 8
    try:
        account.alchemy_p2w["Vials"] = raw_p2w_list[2]
    except:
        account.alchemy_p2w["Vials"] = [0] * 2
    try:
        account.alchemy_p2w["Player"] = raw_p2w_list[3]
    except:
        account.alchemy_p2w["Player"] = [0] * 2

    for sigilName in account.alchemy_p2w["Sigils"]:
        try:
            account.alchemy_p2w["Sigils"][sigilName]["PlayerHours"] = float(raw_p2w_list[4][account.alchemy_p2w["Sigils"][sigilName]["Index"]])
            account.alchemy_p2w["Sigils"][sigilName]["Level"] = raw_p2w_list[4][account.alchemy_p2w["Sigils"][sigilName]["Index"] + 1] + 1
        except:
            pass  # Already defaulted to 0s in consts.sigilsDict
        
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
        'Royale Balls': safer_get(account.raw_optlacc_dict, 324, 0),
    }

    account.arcade = {}
    raw_arcade_upgrades = safe_loads(account.raw_data.get('ArcadeUpg', []))
    for upgrade_index, upgrade_details in arcadeBonuses.items():
        try:
            account.arcade[upgrade_index] = {
                'Level': raw_arcade_upgrades[upgrade_index],
                'Value': lavaFunc(
                    upgrade_details['funcType'],
                    min(arcade_max_level, raw_arcade_upgrades[upgrade_index]),
                    upgrade_details['x1'],
                    upgrade_details['x2']
                ),
                'MaxValue':(
                    2  #Royale
                    * 2  #Reindeer Companion
                    * lavaFunc(
                        upgrade_details['funcType'],
                        arcade_max_level,
                        upgrade_details['x1'],
                        upgrade_details['x2']
                    )
                ),
                'Royale': raw_arcade_upgrades[upgrade_index] > arcade_max_level,
                'Material': (
                    '' if raw_arcade_upgrades[upgrade_index] == 101
                    else 'arcade-royale-ball' if raw_arcade_upgrades[upgrade_index] == 100
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
                'Value': lavaFunc(
                    upgrade_details['funcType'],
                    0,
                    upgrade_details['x1'],
                    upgrade_details['x2']
                ),
                'MaxValue':(
                    2  #Royale
                    * 2  #Reindeer Companion
                    * lavaFunc(
                        upgrade_details['funcType'],
                        arcade_max_level,
                        upgrade_details['x1'],
                        upgrade_details['x2']
                    )
                ),
                'Royale': False,
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
    for buffIndex, buffValuesDict in ballotDict.items():
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
    }
    raw_owned_obols = []
    for jsonkey in [
        "ObolEqO1", "ObolEqO2", "ObolEqO0_0", "ObolEqO0_1", "ObolEqO0_2", "ObolEqO0_3", "ObolEqO0_4",
        "ObolEqO0_5", "ObolEqO0_6", "ObolEqO0_7", "ObolEqO0_8", "ObolEqO0_9"
    ]:
        raw_owned_obols += safe_loads(account.raw_data.get(jsonkey, []))
    raw_obol_inventory_list = safe_loads(account.raw_data.get("ObolInvOr"))
    for subdict in raw_obol_inventory_list:
        raw_owned_obols += subdict.values()
    for obol in raw_owned_obols:
        if obol not in ignorable_obols_list:
            obolBonusType = obolsDict.get(obol, {}).get('Bonus', 'Unknown')
            obolShape = obolsDict.get(obol, {}).get('Shape', 'Unknown')
            account.obols[obolBonusType][obolShape]['Total'] += 1
            if obol not in account.obols[obolBonusType][obolShape]:
                account.obols[obolBonusType][obolShape][obol] = {'Count': 1}
            else:
                account.obols[obolBonusType][obolShape][obol]['Count'] += 1

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

def _parse_w3_refinery(account):
    account.refinery = {}
    raw_refinery_list = safe_loads(account.raw_data.get("Refinery", []))
    for saltColor, saltDetails in refineryDict.items():
        try:
            account.refinery[saltColor] = {
                'Rank': raw_refinery_list[saltDetails[0]][1],
                'Running': raw_refinery_list[saltDetails[0]][3],
                'AutoRefine': raw_refinery_list[saltDetails[0]][4],
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
    for buildingIndex, buildingValuesDict in buildingsDict.items():
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
    account.apocalypse_character_Index = _parse_w3_apocalypse_BBIndex(account)
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
    if account.apocalypse_character_Index is not None:
        riftPresent = False
        for remainingMap in account.all_characters[account.apocalypse_character_Index].apoc_dict['MEOW']['Medium Extras']:
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
            for worldIndex in range(0, len(apocableMapIndexDict)):
                for mapIndex in apocableMapIndexDict[worldIndex]:
                    try:
                        account.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, characterKillsDict.get(mapIndex, [0])[0])
                    except:
                        account.enemy_maps[worldIndex][mapIndex].updateZOWDict(characterIndex, 0)

        # Regardless of class, for each map within each world, add this player's kills to EnemyMap's kill_count
        for worldIndex in range(1, len(apocableMapIndexDict)):
            for mapIndex in apocableMapIndexDict[worldIndex]:
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
                    for apocIndex, apocAmount in enumerate(apocAmountsList):
                        if kill_count < apocAmount:
                            # characterDict[barbCharacterIndex].apoc_dict[apocNamesList[apocIndex]][enemyMaps[worldIndex][enemy_map].zow_rating].append([
                            account.all_characters[barbCharacterIndex].addUnmetApoc(
                                apocNamesList[apocIndex],
                                account.enemy_maps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                                [
                                    account.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                    apocAmount - kill_count if apocIndex < 3 else kill_count,  # kills short of zow/chow/meow
                                    floor((kill_count / apocAmount) * 100),  # percent toward zow/chow/meow
                                    account.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                    worldIndex
                                ]
                            )
                        else:
                            account.all_characters[barbCharacterIndex].increaseApocTotal(apocNamesList[apocIndex])
                else:
                    # This condition can be hit when reviewing data from before a World release
                    # For example, JSON data from w5 before w6 is released hits this to populate 0% toward W6 kills
                    for apocIndex, apocAmount in enumerate(apocAmountsList):
                        account.all_characters[barbCharacterIndex].addUnmetApoc(
                            apocNamesList[apocIndex], account.enemy_maps[worldIndex][enemy_map].getRating(apocNamesList[apocIndex]),
                            [
                                account.enemy_maps[worldIndex][enemy_map].map_name,  # map name
                                apocAmountsList[apocIndex],  # kills short of zow/chow/meow
                                0,  # percent toward zow/chow/meow
                                account.enemy_maps[worldIndex][enemy_map].monster_image,  # monster image
                                worldIndex
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
        kill_count = raw_mb_kills[mb_index] if len(raw_mb_kills) >= mb_index+1 else 0
        skull_number = 0
        kills_to_next_skull = 0
        percent_to_next_skull = 0.0
        for requirement_index, skull_requirement in enumerate(dn_miniboss_skull_requirement_list):
            if kill_count >= skull_requirement:
                skull_number = requirement_index
            elif kill_count < skull_requirement and kills_to_next_skull == 0:
                kills_to_next_skull = skull_requirement - kill_count
                percent_to_next_skull = 100 * (kills_to_next_skull / skull_requirement)
        skull_mk_value = dnSkullValueList[skull_number] if len(dnSkullValueList) >= skull_number else 0
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
    for dreamNumber in dreamsThatUnlockNewBonuses:
        if account.equinox_dreams[dreamNumber] == True:
            account.total_equinox_bonuses_unlocked += 1
        else:
            account.remaining_equinox_dreams_unlocking_new_bonuses.append(dreamNumber)

def _parse_w3_equinox_bonuses(account):
    account.equinox_bonuses = {}
    raw_equinox_bonuses = safe_loads(account.raw_data.get("Dream", [0] * 30))
    for bonusIndex, bonusValueDict in equinoxBonusesDict.items():
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
                    buildingsDict[18 + shrineIndex]['ValueBase']
                    + (buildingsDict[18 + shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                    if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                ),
                "Value": (
                    buildingsDict[18 + shrineIndex]['ValueBase']
                    + (buildingsDict[18 + shrineIndex]['ValueIncrement'] * (int(raw_shrines_list[shrineIndex][3]) - 1))
                    if int(raw_shrines_list[shrineIndex][3]) > 0 else 0
                ),
                'Image': buildingsDict[18 + shrineIndex]['Image']
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
                'Image': buildingsDict[18 + shrineIndex]['Image']
            }

def _parse_w3_atom_collider(account):
    account.atom_collider = {
        'OnOffStatus': safer_get(account.raw_optlacc_dict, 132, False),
        'Magnesium Days': safer_get(account.raw_optlacc_dict, 363, 0)
    }
    try:
        account.atom_collider['StorageLimit'] = colliderStorageLimitList[safer_get(account.raw_optlacc_dict, 133, -1)]
    except:
        account.atom_collider['StorageLimit'] = colliderStorageLimitList[-1]
    try:
        account.atom_collider['Particles'] = account.raw_data.get("Divinity", {})[39]
    except:
        account.atom_collider['Particles'] = "Unknown"  # 0.0

    _parse_w3_atoms(account)

def _parse_w3_atoms(account):
    account.atom_collider['Atoms'] = {}
    raw_atoms_list = safe_loads(account.raw_data.get("Atoms", []))
    for atomIndex, atomInfoList in enumerate(atomsList):
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
    for prayerIndex, prayerValuesDict in prayersDict.items():
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
            account.prayers[prayerValuesDict['Name']]['BonusValue'] = lavaFunc(
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
            account.prayers[prayerValuesDict['Name']]['CurseValue'] = lavaFunc(
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
    for saltlickIndex, saltlickName in enumerate(saltLickList):
        try:
            account.saltlick[saltlickName] = int(raw_saltlick_list[saltlickIndex])
        except:
            account.saltlick[saltlickName] = 0


def _parse_w4(account):
    _parse_w4_cooking(account)
    _parse_w4_lab(account)
    _parse_w4_rift(account)
    _parse_w4_breeding(account)

def _parse_w4_cooking(account):
    account.cooking = {
        'MealsUnlocked': 0,
        'MealsUnder11': 0,
        'MealsUnder30': 0,
        'PlayerMaxPlateLvl': 30,  # 30 is the default starting point
        'PlayerTotalMealLevels': 0,
        'MaxTotalMealLevels': maxMealCount * maxMealLevel,
        'PlayerMissingPlateUpgrades': []
    }
    _parse_w4_cooking_tables(account)
    _parse_w4_cooking_meals(account)
    _parse_w4_cooking_ribbons(account)

def _parse_w4_cooking_tables(account):
    emptyTable = [0] * 11  # Some tables only have 10 fields, others have 11. Scary.
    emptyCooking = [emptyTable for table in range(maxCookingTables)]
    raw_cooking_list = safe_loads(account.raw_data.get("Cooking", emptyCooking))
    for sublistIndex, value in enumerate(raw_cooking_list):
        if isinstance(raw_cooking_list[sublistIndex], list):
            # Pads out the length of all tables to 11 entries, to be safe.
            while len(raw_cooking_list[sublistIndex]) < 11:
                raw_cooking_list[sublistIndex].append(0)
    account.cooking['Tables'] = raw_cooking_list
    account.cooking['Tables Owned'] = sum(1 for table in account.cooking['Tables'] if table[0] == 2)

def _parse_w4_cooking_meals(account):
    emptyMeal = [0] * maxMealCount
    # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
    emptyMeals = [emptyMeal for meal in range(4)]
    raw_meals_list = safe_loads(account.raw_data.get("Meals", emptyMeals))
    # Make the sublists maxMealCount long
    for sublistIndex, value in enumerate(raw_meals_list):
        if isinstance(raw_meals_list[sublistIndex], list):
            while len(raw_meals_list[sublistIndex]) < maxMealCount:
                raw_meals_list[sublistIndex].append(0)
            while len(raw_meals_list[sublistIndex]) > maxMealCount:
                raw_meals_list[sublistIndex].pop()

    account.meals = {}
    # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
    for index, mealLevel in enumerate(raw_meals_list[0]):
        # Create meal dict
        account.meals[cookingMealDict[index]['Name']] = {
            'Level': int(mealLevel),
            'Value': int(mealLevel) * cookingMealDict[index]['BaseValue'],  # Mealmulti applied in calculate section
            'BaseValue': cookingMealDict[index]['BaseValue'],
            'Effect': cookingMealDict[index]['Effect'],
            'Index': index,
            'Image': f"{cookingMealDict[index]['Name']}-meal"
        }

        if int(mealLevel) > 0:
            account.cooking['MealsUnlocked'] += 1
            account.cooking['PlayerTotalMealLevels'] += int(mealLevel)
            if int(mealLevel) < 11:
                account.cooking['MealsUnder11'] += 1
            if int(mealLevel) < 30:
                account.cooking['MealsUnder30'] += 1

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
    _parse_w4_lab_chips(account, raw_lab)
    _parse_w4_lab_bonuses(account, raw_lab)
    _parse_w4_jewels(account, raw_lab)

def _parse_w4_lab_chips(account, raw_lab):
    account.labChips = {}
    raw_labChips_list = raw_lab
    if len(raw_labChips_list) >= 15:
        raw_labChips_list = raw_labChips_list[15]
    for labChipIndex, labChip in labChipsDict.items():
        try:
            account.labChips[labChip["Name"]] = max(0, int(raw_labChips_list[labChipIndex]))
        except:
            account.labChips[labChip["Name"]] = 0

def _parse_w4_lab_bonuses(account, raw_lab):
    # TODO: Actually figure out lab :(
    account.labBonuses = {}
    for index, node in labBonusesDict.items():
        account.labBonuses[node["Name"]] = {
            "Enabled": True,
            "Owned": True,  # For W6 nodes
            "Value": node["BaseValue"],  # Currently no modifiers available, might change if the pure opal navette changes
            "BaseValue": node["BaseValue"]
        }

def _parse_w4_jewels(account, raw_lab):
    # TODO: Account for if the jewel is actually connected.

    account.labJewels = {}
    for jewelIndex, jewelInfo in labJewelsDict.items():
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
    for riftLevel, riftBonusDict in riftRewardsDict.items():
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
        account.gemshop['Royal Egg Cap']
        + account.breeding['Upgrades']['Egg Capacity']['Level']
        + account.merits[3][2]['Level']
    )

def _parse_w4_breeding_defaults(account):
    # Abilities defaulted to False
    for genetic in breedingGeneticsList:
        account.breeding["Genetics"][genetic] = False

    # Total Shiny Bonus Levels defaulted to 0
    # Grouped Bonus per Shiny Bonus defaulted to empty list
    for bonus in breedingShinyBonusList:
        account.breeding["Total Shiny Levels"][bonus] = 0
        account.breeding['Grouped Bonus'][bonus] = []

def _parse_w4_breeding_misc(account):
    # Highest Arena Wave
    try:
        account.breeding['ArenaMaxWave'] = int(account.raw_data["OptLacc"][89])
    except:
        pass

    # Number of Pet Slots Unlocked
    for requirement in slotUnlockWavesList:
        if account.breeding['ArenaMaxWave'] > requirement:
            account.breeding['PetSlotsUnlocked'] += 1

def _parse_w4_breeding_upgrades(account, rawBreeding):
    for upgradeIndex, upgradeValuesDict in breedingUpgradesDict.items():
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
    account.breeding["Highest Unlocked Territory Name"] = territoryNames[min(maxNumberOfTerritories, account.breeding["Highest Unlocked Territory Number"])]

    for territoryIndex in range(0, maxNumberOfTerritories):
        if territoryIndex < account.breeding["Highest Unlocked Territory Number"]:
            account.breeding['Territories'][territoryNames[territoryIndex + 1]] = {'Unlocked': True}

        else:
            account.breeding['Territories'][territoryNames[territoryIndex + 1]] = {'Unlocked': False}

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
    for worldIndex, worldPetsDict in breedingSpeciesDict.items():
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

    for index, valuesDict in gamingSuperbitsDict.items():
        try:
            account.gaming['SuperBits'][valuesDict['Name']] = {
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
    account.sailing = {"Artifacts": {}, "Boats": {}, "Captains": {}, "Islands": {}, 'IslandsDiscovered': 1, 'CaptainsOwned': 1, 'BoatsOwned': 1}
    raw_sailing_list = safe_loads(safe_loads(account.raw_data.get("Sailing", [])))  # Some users have needed to have data converted twice
    if not raw_sailing_list:
        logger.warning(f"Sailing data not present")
    try:
        account.sailing['CaptainsOwned'] += raw_sailing_list[2][0]
        account.sailing['BoatsOwned'] += raw_sailing_list[2][1]
        account.sum_artifact_tiers = sum(raw_sailing_list[3])
    except:
        account.sum_artifact_tiers = 0
    for islandIndex, islandValuesDict in sailingDict.items():
        try:
            account.sailing['Islands'][islandValuesDict['Name']] = {
                'Unlocked': True if raw_sailing_list[0][islandIndex] == -1 else False,
                'Distance': islandValuesDict['Distance'],
                'NormalTreasure': islandValuesDict['NormalTreasure'],
                'RareTreasure': islandValuesDict['RareTreasure']
            }
            account.sailing['IslandsDiscovered'] += 1 if account.sailing['Islands'][islandValuesDict['Name']]['Unlocked'] else 0
        except:
            account.sailing['Islands'][islandValuesDict['Name']] = {
                'Unlocked': False,
                'Distance': islandValuesDict['Distance'],
                'NormalTreasure': islandValuesDict['NormalTreasure'],
                'RareTreasure': islandValuesDict['RareTreasure']
            }
        for artifactIndex, artifactValuesDict in islandValuesDict['Artifacts'].items():
            try:
                account.sailing['Artifacts'][artifactValuesDict['Name']] = {
                    'Level': raw_sailing_list[3][artifactIndex]
                }
            except:
                account.sailing['Artifacts'][artifactValuesDict['Name']] = {
                    'Level': 0
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
                'TopBuff': captainBuffs[captainDetails[1]],
                'BottomBuff': captainBuffs[captainDetails[2]],
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
        'Divinities': copy.deepcopy(divinity_divinitiesDict),
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
            account.gemshop[f"Parallel Villagers {villager_data['Role']}"] = parallel_villagers[villager_index]
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
            account.gemshop[f"Parallel Villagers {villager_data['Role']}"] = 0

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
            if int(entry_value)+1 in divinity_divinitiesDict:
                account.caverns['PocketDivinityLinks'].append(divinity_divinitiesDict[int(entry_value)+1]['Name'])
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
                except Exception as e:
                    logger.warning(f"Error processing schematic {clean_name} at index {schematic_index}. Usually caused by HolesInfo[40] not being updated after new schematics were added!")
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
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = raw_caverns_list[11][0 + motherlode_offset] or 0
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = raw_caverns_list[11][1 + motherlode_offset] or 0
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
    for wish_index, wish_list in enumerate(lamp_wishes):
        account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index] = {
            'Name': wish_list[0],
            'BaseCost': wish_list[1],
            'CostIncreaser': wish_list[2],
            'Idk3': wish_list[3],
            'Description': wish_list[4],
            'Image': f'lamp-wish-{wish_index}',
            'BonusList': []
        }
        try:
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Unlocked'] = (
                    account.caverns['Villagers']['Polonai']['Level'] >= 7
                    and account.caverns['Caverns'][cavern_name]['WishTypesUnlocked'] > wish_index
                )
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level'] = raw_caverns_list[21][wish_index]
        except:
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Unlocked'] = False
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level'] = 0
        account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['NextCost'] = getWishCost(
            wish_index, account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level']
        )

        #If this is a World X stuff wish, calculate each Value into BonusList then update the Description
        if wish_list[0].startswith('World '):
            world_number = safer_convert(wish_list[0].split('World ')[1][0], 0)
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'] = [
                v * account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Level']
                for v in lamp_world_wish_values[world_number]
            ]
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '@', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][0]), 1))
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '#', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][1]), 1))
            account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'] = (
                account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['Description'].replace(
                    '$', str(account.caverns['Caverns'][cavern_name]['WishTypes'][wish_index]['BonusList'][2]), 1))

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
        pts_required = 2e3 + 1e3 * (bonus_index + 1) * (1 + bonus_index / 5) * pow(1.26, bonus_index)
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
    _parse_w6_sneaking(account)
    _parse_w6_farming(account)
    _parse_w6_summoning(account)

def _parse_w6_sneaking(account):
    account.sneaking = {
        "PristineCharms": {},
        "Gemstones": {},
        'Beanstalk': {},
        "JadeEmporium": {},
        'CurrentMastery': safer_get(account.raw_optlacc_dict, 231, 0),
        'MaxMastery': safer_get(account.raw_optlacc_dict, 232, 0),
    }
    raw_ninja_list = safe_loads(account.raw_data.get("Ninja", []))
    if not raw_ninja_list:
        logger.warning(f"Sneaking data not present{', as expected' if account.version < 200 else ''}.")
    _parse_w6_pristine_charms(account, raw_ninja_list)
    _parse_w6_gemstones(account, raw_ninja_list)
    _parse_w6_jade_emporium(account, raw_ninja_list)
    _parse_w6_beanstalk(account, raw_ninja_list)

def _parse_w6_pristine_charms(account, raw_ninja_list):
    raw_pristine_charms_list = raw_ninja_list[107] if raw_ninja_list else []
    for pristineCharmIndex, pristineCharmDict in enumerate(pristineCharmsList):
        try:
            account.sneaking["PristineCharms"][pristineCharmDict['Name']] = {
                'Obtained': bool(raw_pristine_charms_list[pristineCharmIndex]),
                'Image': pristineCharmDict['Image'],
                'Bonus': pristineCharmDict['Bonus'],
            }
        except:
            account.sneaking["PristineCharms"][pristineCharmDict['Name']] = {
                'Obtained': False,
                'Image': pristineCharmDict['Image'],
                'Bonus': pristineCharmDict['Bonus'],
            }

def _parse_w6_gemstones(account, raw_ninja_list):
    for gemstone_name, gemstone_values in sneaking_gemstones_all_values.items():
        level = safer_get(account.raw_optlacc_dict, gemstone_values['OptlAcc Index'], 0)
        account.sneaking['Gemstones'][gemstone_name] = {
            'Level': level,
            'Stat': gemstone_values['Stat'],
            'MaxValue': gemstone_values['Max Value'],
            'BaseValue': getGemstoneBaseValue(gemstone_name, level),
            'BoostedValue': 0.0,
            'Percent': 0
        }
        account.sneaking['Gemstones'][gemstone_name]['Percent'] = getGemstonePercent(
            gemstone_name,
            account.sneaking['Gemstones'][gemstone_name]['BaseValue']
        )

def _parse_w6_jade_emporium(account, raw_ninja_list):
    try:
        raw_emporium_purchases = list(raw_ninja_list[102][9])
    except:
        raw_emporium_purchases = [""]
    for upgradeIndex, upgradeDict in enumerate(jade_emporium):
        try:
            account.sneaking['JadeEmporium'][upgradeDict['Name']] = {
                'Obtained': upgradeDict['CodeString'] in raw_emporium_purchases,
                'Bonus': upgradeDict['Bonus']
            }
        except:
            continue

def _parse_w6_beanstalk(account, raw_ninja_list):
    raw_beanstalk_list = raw_ninja_list[104] if raw_ninja_list else []
    if not raw_beanstalk_list:
        logger.warning(f"Beanstalk data not present{', as expected' if account.version < 200 else ''}.")
    for gfoodIndex, gfoodName in enumerate(gfood_codes):
        try:
            account.sneaking['Beanstalk'][gfoodName] = {
                'Name': getItemDisplayName(gfoodName),
                'Beanstacked': raw_beanstalk_list[gfoodIndex] > 0,
                'SuperBeanstacked': raw_beanstalk_list[gfoodIndex] > 1,
            }
        except:
            account.sneaking['Beanstalk'][gfoodName] = {
                'Name': getItemDisplayName(gfoodName),
                'Beanstacked': False,
                'SuperBeanstacked': False,
            }

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
        + account.gemshop['Plot of Land']
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
    for bonusIndex, bonusDetails in cropDepotDict.items():
        account.farming['Depot'][bonusIndex] = {
            'BonusString': bonusDetails['BonusString'],
            'Image': bonusDetails['Image'],
            'ScalingType': bonusDetails['funcType'],
            'ScalingNumber': bonusDetails['x1'],
            'Unlocked': account.sneaking['JadeEmporium'][bonusDetails['EmporiumUnlockName']]['Obtained'],
            'BaseValue': lavaFunc(
                bonusDetails['funcType'],
                account.farming['CropsUnlocked'] if bonusIndex != 7 else max(0, account.farming['CropsUnlocked'] - 100),
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'BaseValuePlus1': lavaFunc(
                bonusDetails['funcType'],
                min(maxFarmingCrops, account.farming['CropsUnlocked'] + 1) if bonusIndex != 7 else min(maxFarmingCrops - 100, account.farming['CropsUnlocked'] + 1),
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'MaxValue': lavaFunc(
                bonusDetails['funcType'],
                maxFarmingCrops,
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
    for marketUpgradeIndex, marketUpgrade in enumerate(marketUpgradeDetails):
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
    for upgradeIndex, upgradeValuesDict in landrankDict.items():
        try:
            account.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                'Level': rawRanks[2][upgradeIndex],
                'BaseValue': upgradeValuesDict['Value'],
                'Value': (
                    (1.7 * upgradeValuesDict['Value'] * rawRanks[2][upgradeIndex]) / (rawRanks[2][upgradeIndex] + 80)
                    if upgradeIndex not in [4, 9, 14, 19]
                    else upgradeValuesDict['Value'] * rawRanks[2][upgradeIndex]
                )
            }
        except:
            account.farming['LandRankDatabase'][upgradeValuesDict['Name']] = {
                'Level': 0,
                'BaseValue': upgradeValuesDict['Value'],
                'Value': 0
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
                'Color': summoning_match_colors[int(upg_details[2])],
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
                'Color': summoning_match_colors[int(upg_details[2])],
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
    for color in summoningDict:
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

def _parse_w6_summoning_battles(account, rawBattles):
    safe_battles = [safer_convert(battle, '') for battle in rawBattles]
    regular_battles = [battle for battle in safe_battles if not battle.startswith('rift')]
    account.summoning['Battles']['NormalTotal'] = len(regular_battles)

    if account.summoning['Battles']['NormalTotal'] >= summoningBattleCountsDict["Normal"]:
        account.summoning["Battles"] = summoningBattleCountsDict
        account.summoning['AllBattlesWon'] = True
    else:
        account.summoning['AllBattlesWon'] = False
        for colorName, colorDict in summoningDict.items():
            account.summoning["Battles"][colorName] = 0
            for battleIndex, battleValuesDict in colorDict.items():
                if battleIndex + 1 >= account.summoning["Battles"][colorName] and battleValuesDict['EnemyID'] in rawBattles:
                    account.summoning["Battles"][colorName] = battleIndex + 1

    # Endless doesn't follow the same structure as the once-only battles
    account.summoning['Battles']['Endless'] = safer_get(account.raw_optlacc_dict, 319, 0)

    for colorName, colorDict in summoningDict.items():
        for battleIndex, battleValuesDict in colorDict.items():
            account.summoning["BattleDetails"][colorName][battleIndex + 1] = {
                'Defeated': battleValuesDict['EnemyID'] in rawBattles,
                'Image': battleValuesDict['Image'],
                'RewardType': battleValuesDict['RewardID'],
                'RewardQTY': battleValuesDict['RewardQTY'],
                'RewardBaseValue': battleValuesDict['RewardQTY'] * 3.5,
            }
            if account.summoning["BattleDetails"][colorName][battleIndex + 1]['RewardType'].startswith('+ '):
                account.summoning["BattleDetails"][colorName][battleIndex + 1]['Description'] = (
                    account.summoning["BattleDetails"][colorName][battleIndex + 1]['RewardType'].replace(
                        '+', f"+{account.summoning['BattleDetails'][colorName][battleIndex + 1]['RewardBaseValue']}")
                )
            elif account.summoning["BattleDetails"][colorName][battleIndex + 1]['RewardType'].startswith('%'):
                account.summoning["BattleDetails"][colorName][battleIndex + 1]['Description'] = (
                    f"{account.summoning['BattleDetails'][colorName][battleIndex + 1]['RewardBaseValue']}"
                    f"{account.summoning['BattleDetails'][colorName][battleIndex + 1]['RewardType']}"
                )
            elif account.summoning["BattleDetails"][colorName][battleIndex + 1]['RewardType'].startswith('x'):
                account.summoning["BattleDetails"][colorName][battleIndex + 1]['Description'] = (
                    f"{ValueToMulti(account.summoning['BattleDetails'][colorName][battleIndex + 1]['RewardBaseValue'])}"
                    f"{account.summoning['BattleDetails'][colorName][battleIndex + 1]['RewardType']}"
                )

def _parse_w6_summoning_battles_endless(account):
    account.summoning['Endless Bonuses'] = {}
    true_battle_index = 0
    while true_battle_index < max(40, account.summoning['Battles']['Endless'] + 20):
        image_index = min(4, true_battle_index // 20)
        endless_enemy_index = true_battle_index % 40
        this_battle = {
            'Defeated': true_battle_index < account.summoning['Battles']['Endless'],
            'Image': summoning_endlessEnemies.get(image_index, ''),
            'RewardType': summoning_endlessDict.get(endless_enemy_index, {}).get('RewardID', 'Unknown'),
            'Challenge': summoning_endlessDict.get(endless_enemy_index, {}).get('Challenge', 'Unknown'),
            # 'RewardQTY': summoning_endlessDict.get(endless_enemy_index, {}).get('RewardQTY', 0),
            'RewardBaseValue': (
                summoning_endlessDict.get(endless_enemy_index, {}).get('RewardQTY', 0)
            )
        }
        if this_battle['RewardType'].startswith('+'):
            this_battle['Description'] = this_battle['RewardType'].replace('+', f"+{this_battle['RewardBaseValue']}")
        elif this_battle['RewardType'].startswith('%'):
            this_battle['Description'] = f"+{this_battle['RewardBaseValue']}{this_battle['RewardType']}"
        elif this_battle['RewardType'].startswith('x'):
            this_battle['Description'] = f"{ValueToMulti(this_battle['RewardBaseValue'])}{this_battle['RewardType']}"
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
