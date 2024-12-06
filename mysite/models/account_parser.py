import copy
from collections import defaultdict
from math import floor
from flask import g
from consts import (
    # General
    lavaFunc, ValueToMulti, items_codes_and_names,
    maxCharacters,
    gfood_codes,
    card_data,
    gemShopDict,
    guildBonusesList, familyBonusesDict, achievementsList, allMeritsDict, starsignsDict,
    event_points_shop_dict,
    npc_tokens,
    # W1
    stampsDict, stampTypes, bribesDict,
    forgeUpgradesDict,
    statuesDict, statueTypeList, statueCount,
    # W2
    bubblesDict,
    vialsDict, max_IndexOfVials, getReadableVialNames, max_VialLevel,
    sigilsDict,
    arcadeBonuses, arcade_max_level,
    ballotDict,
    obolsDict, ignorable_obols_list,
    islands_dict, killroy_dict,
    # W3
    refineryDict, buildingsDict, saltLickList, atomsList, colliderStorageLimitList, shrinesList, prayersDict,
    equinoxBonusesDict, maxDreams, dreamsThatUnlockNewBonuses,
    printerAllIndexesBeingPrinted,
    apocableMapIndexDict, apocAmountsList, apocNamesList,
    # W4
    riftRewardsDict,
    labJewelsDict, labBonusesDict, labChipsDict,
    maxMeals, maxMealLevel, cookingMealDict, maxCookingTables,
    maxNumberOfTerritories, territoryNames, slotUnlockWavesList, breedingUpgradesDict, breedingGeneticsList,
    breedingShinyBonusList, breedingSpeciesDict, getShinyLevelFromDays, getDaysToNextShinyLevel, getBreedabilityMultiFromDays, getBreedabilityHeartFromMulti,
    # W5
    sailingDict, captainBuffs,
    getStyleNameFromIndex, divinity_divinitiesDict, getDivinityNameFromIndex, gamingSuperbitsDict,
    # W6
    jade_emporium, pristineCharmsList, sneakingGemstonesFirstIndex, sneakingGemstonesList, sneakingGemstonesStatList,
    getMoissaniteValue, getGemstoneBaseValue, getGemstoneBoostedValue, getGemstonePercent,
    marketUpgradeDetails, landrankDict, cropDepotDict, maxFarmingCrops, summoningBattleCountsDict, summoningDict, summoning_endlessEnemies,
    summoning_endlessDict, max_summoning_upgrades,
    # Caverns
    caverns_villagers, caverns_conjuror_majiks, caverns_engineer_schematics, caverns_engineer_schematics_unlock_order, caverns_cavern_names,
    caverns_measurer_measurements, getCavernResourceImage, max_buckets, max_sediments, sediment_bars, getVillagerEXPRequired,
    monument_bonuses, bell_clean_improvements, bell_ring_bonuses, getBellExpRequired, getGrottoKills, lamp_wishes, key_cards, getWishCost,
    schematics_unlocking_harp_chords, harp_chord_effects, max_harp_notes
)
from models.models import Character, buildMaps, EnemyWorld, Card, Assets
from utils.data_formatting import getCharacterDetails, safe_loads, safer_get
from utils.logging import get_logger
from utils.text_formatting import getItemDisplayName

logger = get_logger(__name__)


def _make_cards(account):
    card_counts = safe_loads(account.raw_data.get(key_cards, {}))
    cards = [
        Card(codename, name, cardset, safer_get(card_counts, codename, 0), coefficient)
        for cardset, cards in card_data.items()
        for codename, (name, coefficient) in cards.items()
    ]

    return cards


def _all_stored_items(account) -> Assets:
    chest_keys = (("ChestOrder", "ChestQuantity"),)
    name_quantity_key_pairs = chest_keys + tuple(
        (f"InventoryOrder_{i}", f"ItemQTY_{i}") for i in account.safe_playerIndexes
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
    _parse_characters(account, run_type)
    _parse_general(account)
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
    elif account.raw_data.get("AutoLoot", 0) == 1:
        account.autoloot = True
        g.autoloot = True
    else:
        account.autoloot = False

    # consts.maxTiersPerGroup = 1 if g.one_tier else consts.maxTiersPerGroup

    # Companions
    account.sheepie_owned = g.sheepie
    account.doot_owned = g.doot
    account.riftslug_owned = g.riftslug
    # logger.debug(f"Switches alone: Doot={g.doot}, Slug={g.riftslug}, Sheepie={g.sheepie}")
    if not all([account.doot_owned, account.sheepie_owned, account.riftslug_owned]):
        # If the data comes from Toolbox, it'll be a dictionary called companion singular
        raw_companion = account.raw_data.get('companion', None)
        # If the data comes from Efficiency, it'll be a flat list of just companion ID: "companions": [7, 10, 4, 5, 9, 2, 3, 6]
        raw_companions = account.raw_data.get('companions', None)
        if raw_companion is not None:
            if isinstance(raw_companion, dict):
                for companionInfo in raw_companion.get('l', []):
                    companionID = int(companionInfo.split(',')[0])
                    if companionID == 0:
                        account.doot_owned = True
                        g.doot = True
                    if companionID == 1:
                        account.riftslug_owned = True
                        g.riftslug = True
                    if companionID == 4:
                        account.sheepie_owned = True
                        g.sheepie = True
        elif raw_companions is not None:
            # logger.debug(f"Efficiency Companions data found: {raw_companions}")
            try:
                account.doot_owned = g.doot or 0 in raw_companions
                g.doot = account.doot_owned
                account.riftslug_owned = g.riftslug or 1 in raw_companions
                g.riftslug = account.riftslug_owned
                account.sheepie_owned = g.sheepie or 4 in raw_companions
                g.sheepie = account.sheepie_owned
            except:
                logger.exception(f"Efficiency Companions parse error, raw_companions={raw_companions}")
        else:
            logger.warning(f"No companion data present in JSON")
    # logger.debug(f"Account model: Doot={account.doot_owned}, Slug={account.riftslug_owned}, Sheepie={account.sheepie_owned}")
    # logger.debug(f"Switches after: Doot={g.doot}, Slug={g.riftslug}, Sheepie={g.sheepie}")

def _parse_characters(account, run_type):
    playerCount, playerNames, playerClasses, characterDict, perSkillDict = getCharacterDetails(
        account.raw_data, run_type
    )
    account.names = playerNames
    account.playerCount = playerCount
    account.classes = playerClasses
    account.all_characters = [Character(account.raw_data, **char) for char in characterDict.values()]
    account.safe_characters = [char for char in account.all_characters if char]  # Use this if touching raw_data instead of all_characters
    account.safe_playerIndexes = [char.character_index for char in account.all_characters if char]
    account.all_skills = perSkillDict
    account.all_quests = [safe_loads(account.raw_data.get(f"QuestComplete_{i}", "{}")) for i in range(account.playerCount)]
    account.max_toon_count = max(maxCharacters, playerCount)  # OPTIMIZE: find a way to read this from somewhere
    _parse_character_class_lists(account)

def _parse_character_class_lists(account):
    account.beginners = [toon for toon in account.all_characters if "Beginner" in toon.all_classes or "Journeyman" in toon.all_classes]
    account.jmans = [toon for toon in account.all_characters if "Journeyman" in toon.all_classes]
    account.maestros = [toon for toon in account.all_characters if "Maestro" in toon.all_classes]
    account.vmans = [toon for toon in account.all_characters if "Voidwalker" in toon.all_classes]

    account.barbs = [toon for toon in account.all_characters if "Barbarian" in toon.all_classes]
    account.bbs = [toon for toon in account.all_characters if "Blood Berserker" in toon.all_classes]
    account.dks = [toon for toon in account.all_characters if "Divine Knight" in toon.all_classes]

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
    _parse_general_gemshop(account)
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

def _parse_general_gemshop(account):
    account.gemshop = {}
    raw_gem_items_purchased = safe_loads(account.raw_data.get("GemItemsPurchased", []))
    for purchaseName, purchaseIndex in gemShopDict.items():
        try:
            account.gemshop[purchaseName] = int(raw_gem_items_purchased[purchaseIndex])
        except:
            account.gemshop[purchaseName] = 0

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
            account.npc_tokens[tokenName] = int(raw_npc_tokens[tokenIndex])
        except:
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
            logger.exception(f"Error parsing Family Bonus for {className}")
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
    if raw_dungeon_upgrades:
        try:
            account.dungeon_upgrades["MaxWeapon"] = raw_dungeon_upgrades[3][0]
            account.dungeon_upgrades["MaxArmor"] = [
                raw_dungeon_upgrades[3][4], raw_dungeon_upgrades[3][5], raw_dungeon_upgrades[3][6], raw_dungeon_upgrades[3][7]
            ]
            account.dungeon_upgrades["MaxJewelry"] = [raw_dungeon_upgrades[3][8], raw_dungeon_upgrades[3][9]]
            account.dungeon_upgrades["FlurboShop"] = raw_dungeon_upgrades[5]
            account.dungeon_upgrades["CreditShop"] = raw_dungeon_upgrades[5]
        except:
            account.dungeon_upgrades["MaxWeapon"] = 0
            account.dungeon_upgrades["MaxArmor"] = [0, 0, 0, 0]
            account.dungeon_upgrades["MaxJewelry"] = [0, 0]
            account.dungeon_upgrades["FlurboShop"] = [0, 0, 0, 0, 0, 0, 0, 0]
            account.dungeon_upgrades["CreditShop"] = [0, 0, 0, 0, 0, 0, 0, 0]

def _parse_general_achievements(account):
    account.achievements = {}
    raw_reg_achieves = safe_loads(account.raw_data.get('AchieveReg', []))
    for achieveIndex, achieveData in enumerate(achievementsList):
        try:
            if achieveData[0].replace('_', ' ') != "FILLERZZZ ACH":
                account.achievements[achieveData[0].replace('_', ' ')] = {
                    'Complete': raw_reg_achieves[achieveIndex] == -1,
                    'Raw': raw_reg_achieves[achieveIndex]
                }
        except:
            account.achievements[achieveData[0].replace('_', ' ')] = {
                'Complete': False,
                'Raw': 0
            }

def _parse_general_merits(account):
    account.merits = copy.deepcopy(allMeritsDict)
    raw_merits_list = safe_loads(account.raw_data.get("TaskZZ2", []))
    for worldIndex in account.merits:
        for meritIndex in account.merits[worldIndex]:
            try:
                account.merits[worldIndex][meritIndex]["Level"] = int(raw_merits_list[worldIndex][meritIndex])
            except:
                continue  # Already defaulted to 0 in Consts

def _parse_general_guild_bonuses(account):
    account.guildBonuses = {}
    raw_guild = safe_loads(account.raw_data.get('Guild', [[]]))
    for bonusIndex, bonusName in enumerate(guildBonusesList):
        try:
            account.guildBonuses[bonusName] = raw_guild[0][bonusIndex]
        except:
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
    except:
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
                    logger.exception(f"failed on characterIndex '{sampleIndex // 7}', sampleIndex '{sampleIndex}', sampleItem '{sampleItem}'")
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
        if characterIndex < account.playerCount:
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
            account.colo_scores[coloIndex] = int(coloScore)
        except:
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
        except:
            account.event_points_shop['Bonuses'][bonusName] = {
                'Owned': False,
                'Cost': bonusDetails['Cost'],
                'Description': bonusDetails['Description'],
                'Image': bonusDetails['Image']
            }

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
            'Unlocked': False,
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
            account.star_signs[signValuesDict['Name']]['Unlocked'] = int(raw_star_signs[signValuesDict['Name'].replace(" ", "_")]) > 0
            if account.star_signs[signValuesDict['Name']]['Unlocked']:
                account.star_sign_extras['UnlockedSigns'] += 1
        except:
            pass

def _parse_w1_forge(account):
    account.forge_upgrades = copy.deepcopy(forgeUpgradesDict)
    raw_forge_upgrades = account.raw_data.get("ForgeLV", [])
    for upgradeIndex, upgrade in enumerate(raw_forge_upgrades):
        try:
            account.forge_upgrades[upgradeIndex]["Purchased"] = upgrade
        except:
            continue  # Already defaulted to 0 in Consts

def _parse_w1_bribes(account):
    account.bribes = {}
    raw_bribes_list = safe_loads(account.raw_data.get("BribeStatus", []))
    bribeIndex = 0
    for bribeSet in bribesDict:
        account.bribes[bribeSet] = {}
        for bribeName in bribesDict[bribeSet]:
            try:
                account.bribes[bribeSet][bribeName] = int(raw_bribes_list[bribeIndex])
            except:
                account.bribes[bribeSet][bribeName] = -1  # -1 means unavailable for purchase, 0 means available, and 1 means purchased
            bribeIndex += 1

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
                    "Index": int(stampIndex),
                    "Material": stampValuesDict['Material'],
                    "Level": int(floor(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                    "Max": int(floor(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                    "Delivered": int(floor(raw_stamp_max_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))) > 0,
                    "StampType": stampType,
                    "Value": lavaFunc(
                        stampValuesDict['funcType'],
                        int(floor(raw_stamps_dict.get(stampTypes.index(stampType), {}).get(stampIndex, 0))),
                        stampValuesDict['x1'],
                        stampValuesDict['x2'],
                    )
                }
                account.stamp_totals["Total"] += account.stamps[stampValuesDict['Name']]["Level"]
                account.stamp_totals[stampType] += account.stamps[stampValuesDict['Name']]["Level"]
            except:
                account.stamps[stampValuesDict['Name']] = {
                    "Index": stampIndex,
                    "Level": 0,
                    "Max": 0,
                    "Delivered": False,
                    "StampType": stampType,
                    "Value": 0
                }

def _parse_w1_owl(account):
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
        except:
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
        except:
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
    for vialKey, vialValue in raw_alchemy_vials.items():
        try:
            if int(vialKey) < max_IndexOfVials:
                account.alchemy_vials[getReadableVialNames(vialKey)] = {
                    'Level': int(vialValue),
                    'Value': lavaFunc(
                        vialsDict[int(vialKey)]['funcType'],
                        int(vialValue),
                        vialsDict[int(vialKey)]['x1'],
                        vialsDict[int(vialKey)]['x2'],
                    ),
                    'Material': vialsDict[int(vialKey)]['Material']
                }
        except:
            try:
                account.alchemy_vials[getReadableVialNames(vialKey)] = {"Level": 0, "Value": 0, 'Material': vialsDict[int(vialKey)]['Material']}
            except:
                continue
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
            raw_cauldron_upgrades[0],
            raw_cauldron_upgrades[1],
            raw_cauldron_upgrades[2],
            raw_cauldron_upgrades[3],
        ]
        account.alchemy_cauldrons["GreenBoosts"] = [
            raw_cauldron_upgrades[4],
            raw_cauldron_upgrades[5],
            raw_cauldron_upgrades[6],
            raw_cauldron_upgrades[7],
        ]
        account.alchemy_cauldrons["PurpleBoosts"] = [
            raw_cauldron_upgrades[8],
            raw_cauldron_upgrades[9],
            raw_cauldron_upgrades[10],
            raw_cauldron_upgrades[11],
        ]
        account.alchemy_cauldrons["PurpleBoosts"] = [
            raw_cauldron_upgrades[12],
            raw_cauldron_upgrades[13],
            raw_cauldron_upgrades[14],
            raw_cauldron_upgrades[15],
        ]
    except:
        account.alchemy_cauldrons["OrangeBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["GreenBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["PurpleBoosts"]: [0, 0, 0, 0]
        account.alchemy_cauldrons["YellowBoosts"]: [0, 0, 0, 0]
    try:
        account.alchemy_cauldrons["WaterDroplets"] = [raw_cauldron_upgrades[18], raw_cauldron_upgrades[19]]
        account.alchemy_cauldrons["LiquidNitrogen"] = [raw_cauldron_upgrades[22], raw_cauldron_upgrades[23]]
        account.alchemy_cauldrons["TrenchSeawater"] = [raw_cauldron_upgrades[26], raw_cauldron_upgrades[27]]
        account.alchemy_cauldrons["ToxicMercury"] = [raw_cauldron_upgrades[30], raw_cauldron_upgrades[31]]
    except:
        account.alchemy_cauldrons["WaterDroplets"] = [0, 0]
        account.alchemy_cauldrons["LiquidNitrogen"] = [0, 0]
        account.alchemy_cauldrons["TrenchSeawater"] = [0, 0]
        account.alchemy_cauldrons["ToxicMercury"] = [0, 0]

def _parse_w2_bubbles(account):
    account.alchemy_bubbles = {}

    # Set defaults to 0
    for cauldronIndex in bubblesDict:
        for bubbleIndex in bubblesDict[cauldronIndex]:
            account.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']] = {
                "CauldronIndex": cauldronIndex,
                "BubbleIndex": bubbleIndex,
                "Level": 0,
                "BaseValue": 0,
                "Material": getItemDisplayName(bubblesDict[cauldronIndex][bubbleIndex]['Material'])
            }

    # Try to read player levels and calculate base value
    try:
        all_raw_bubbles = [account.raw_data["CauldronInfo"][0], account.raw_data["CauldronInfo"][1], account.raw_data["CauldronInfo"][2],
                           account.raw_data["CauldronInfo"][3]]
        for cauldronIndex in bubblesDict:
            for bubbleIndex in bubblesDict[cauldronIndex]:
                try:
                    account.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']]['Level'] = int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)])
                    account.alchemy_bubbles[bubblesDict[cauldronIndex][bubbleIndex]['Name']]['BaseValue'] = lavaFunc(
                        bubblesDict[cauldronIndex][bubbleIndex]["funcType"],
                        int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)]),
                        bubblesDict[cauldronIndex][bubbleIndex]["x1"],
                        bubblesDict[cauldronIndex][bubbleIndex]["x2"])
                    if int(all_raw_bubbles[cauldronIndex][str(bubbleIndex)]) > 0:
                        account.alchemy_cauldrons['TotalUnlocked'] += 1
                        # Keep track of cauldron counts
                        if cauldronIndex == 0:
                            account.alchemy_cauldrons['OrangeUnlocked'] += 1
                        elif cauldronIndex == 1:
                            account.alchemy_cauldrons['GreenUnlocked'] += 1
                        elif cauldronIndex == 2:
                            account.alchemy_cauldrons['PurpleUnlocked'] += 1
                        elif cauldronIndex == 3:
                            account.alchemy_cauldrons['YellowUnlocked'] += 1
                except:
                    continue  # Level and BaseValue already defaulted to 0 above
    except:
        pass

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

def _parse_w2_arcade(account):
    account.arcade_currency = {
        'Balls': safer_get(account.raw_optlacc_dict, 74, 0),
        'Gold Balls': safer_get(account.raw_optlacc_dict, 75, 0),
        'Royale Balls': safer_get(account.raw_optlacc_dict, 324, 0),
    }

    account.arcade = {}
    raw_arcade_upgrades = safe_loads(account.raw_data.get("ArcadeUpg", []))
    for upgradeIndex, upgradeDetails in arcadeBonuses.items():
        try:
            account.arcade[upgradeIndex] = {
                'Level': raw_arcade_upgrades[upgradeIndex],
                'Value': lavaFunc(
                    upgradeDetails.get("funcType"),
                    min(arcade_max_level, raw_arcade_upgrades[upgradeIndex]),
                    upgradeDetails.get("x1"),
                    upgradeDetails.get("x2")
                ),
                'Royale': raw_arcade_upgrades[upgradeIndex] > arcade_max_level
            }
            if account.arcade[upgradeIndex]['Royale']:
                account.arcade[upgradeIndex]['Value'] *= 2
            account.arcade[upgradeIndex]["Display"] = (
                f"+{account.arcade[upgradeIndex]['Value']:.2f}{upgradeDetails['displayType']} {upgradeDetails['Stat']}"
            )
        except:
            account.arcade[upgradeIndex] = {
                'Level': 0,
                'Value': lavaFunc(
                    upgradeDetails.get("funcType"),
                    0,
                    upgradeDetails.get("x1"),
                    upgradeDetails.get("x2")
                ),
                'Royale': False
            }
            account.arcade[upgradeIndex]["Display"] = (
                f"+{account.arcade[upgradeIndex]['Value']:.2f}{arcadeBonuses[upgradeIndex]['displayType']} {arcadeBonuses[upgradeIndex]['Stat']}"
            )
    # for entry_name, entry_details in account.arcade.items():
    #     logger.debug(f"{entry_name}: {entry_details}")

def _parse_w2_ballot(account):
    account.ballot = {
        "CurrentBuff": safer_get(account.raw_serverVars_dict, 'voteCategories', ["Unknown"])[0],
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
    account.meowBBIndex = _parse_w3_meowBBIndex(account)
    account.rift_meowed = _parse_w3_deathnote_rift_meowed(account)
    _parse_w3_deathnote_kills(account)

def _parse_w3_meowBBIndex(account):
    if len(account.bbCharactersIndexList) == 1:
        return account.bbCharactersIndexList[0]
    elif len(account.bbCharactersIndexList) >= 2:
        return account.bbCharactersIndexList[1]
    else:
        return None

def _parse_w3_deathnote_rift_meowed(account):
    if account.meowBBIndex is not None:
        riftPresent = False
        for remainingMap in account.all_characters[account.meowBBIndex].apoc_dict['MEOW']['Medium Extras']:
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

def _parse_w3_equinox_dreams(account):
    account.equinox_unlocked = account.achievements['Equinox Visitor']['Complete']
    account.equinox_dreams = [True]  # d_0 in the code is Dream 1. By padding the first slot, we can get Dream 1 by that same index: equinox_dreams[1]
    raw_equinox_dreams = safe_loads(account.raw_data.get("WeeklyBoss", {}))
    account.equinox_dreams += [
        float(raw_equinox_dreams.get(f'd_{i}', 0)) == -1
        for i in range(maxDreams)
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
    for shrineIndex, shrineName in enumerate(shrinesList):
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
        'OnOffStatus': safer_get(account.raw_optlacc_dict, 132, True),
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
                'AtomInfo4': atomInfoList[4],
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
                'AtomInfo4': atomInfoList[4],
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
        'MaxTotalMealLevels': maxMeals * maxMealLevel,
        'PlayerMissingPlateUpgrades': []
    }
    _parse_w4_cooking_tables(account)
    _parse_w4_cooking_meals(account)

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
    emptyMeal = [0] * maxMeals
    # Meals contains 4 lists of lists. The first 3 are as long as the number of plates. The 4th is general shorter.
    emptyMeals = [emptyMeal for meal in range(4)]
    raw_meals_list = safe_loads(account.raw_data.get("Meals", emptyMeals))
    # Make the sublists maxMeals long
    for sublistIndex, value in enumerate(raw_meals_list):
        if isinstance(raw_meals_list[sublistIndex], list):
            while len(raw_meals_list[sublistIndex]) < maxMeals:
                raw_meals_list[sublistIndex].append(0)
            while len(raw_meals_list[sublistIndex]) > maxMeals:
                raw_meals_list[sublistIndex].pop()

    account.meals = {}
    # Count the number of unlocked meals, unlocked meals under 11, and unlocked meals under 30
    for index, mealLevel in enumerate(raw_meals_list[0]):
        # Create meal dict
        account.meals[cookingMealDict[index]["Name"]] = {
            "Level": int(mealLevel),
            "Value": int(mealLevel) * cookingMealDict[index]["BaseValue"],  # Mealmulti applied in calculate section
            "BaseValue": cookingMealDict[index]["BaseValue"]
        }

        if int(mealLevel) > 0:
            account.cooking['MealsUnlocked'] += 1
            account.cooking['PlayerTotalMealLevels'] += int(mealLevel)
            if int(mealLevel) < 11:
                account.cooking['MealsUnder11'] += 1
            if int(mealLevel) < 30:
                account.cooking['MealsUnder30'] += 1

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
        try:
            account.breeding['Breedability Days'][f"W{index - 12}"] = [float(v) for v in rawBreeding[index]]
        except:
            continue  # Already default to [] during initialization

    # Shiny Days
    for index in range(22, 30):
        try:
            account.breeding['Shiny Days'][f"W{index - 21}"] = rawBreeding[index]
        except:
            continue  # Already defaulted to [] during initialization

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
    raw_gaming_list = safe_loads(account.raw_data.get("Gaming", []))
    if raw_gaming_list:
        # Bits Owned sometimes Float, sometimes String
        try:
            account.gaming['BitsOwned'] = float(raw_gaming_list[0])
        except:
            pass

        try:
            account.gaming['FertilizerValue'] = raw_gaming_list[1]
            account.gaming['FertilizerSpeed'] = raw_gaming_list[2]
            account.gaming['FertilizerCapacity'] = raw_gaming_list[3]
            account.gaming['MutationsUnlocked'] = raw_gaming_list[4]
            account.gaming['DNAOwned'] = raw_gaming_list[5]
            account.gaming['EvolutionChance'] = raw_gaming_list[7]
            account.gaming['Nugget'] = raw_gaming_list[8]
            account.gaming['Acorns'] = raw_gaming_list[9]
            account.gaming['EvolutionChance'] = raw_gaming_list[10]
            account.gaming['LogbookString'] = raw_gaming_list[11]
            account.gaming['SuperBitsString'] = str(raw_gaming_list[12])
            account.gaming['Envelopes'] = raw_gaming_list[13]
        except:
            pass

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
                'SnailRank': raw_gaming_sprout_list[32][1]
            }
        }
    except:
        account.gaming['Imports'] = {
            'Snail': {
                'SnailRank': 0
            }
        }

def _parse_w5_slab(account):
    account.registered_slab = safe_loads(account.raw_data.get("Cards1", []))

def _parse_w5_sailing(account):
    account.sailing = {"Artifacts": {}, "Boats": {}, "Captains": {}, "Islands": {}, 'IslandsDiscovered': 1, 'CaptainsOwned': 1, 'BoatsOwned': 1}
    raw_sailing_list = safe_loads(safe_loads(account.raw_data.get("Sailing", [])))  # Some users have needed to have data converted twice
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
        'Caverns': {},
        'CavernsUnlocked': 0,
        'Schematics': {},
        'TotalSchematics': 0,
        'Majiks': {},
        'TotalMajiks': 0,
        'Measurements': {},
    }
    raw_caverns_list: list[list] = safe_loads(account.raw_data.get('Holes', []))
    while len(raw_caverns_list) < 24:
        raw_caverns_list.append([])
    _parse_caverns_villagers(account, raw_caverns_list[1], raw_caverns_list[2], raw_caverns_list[3], raw_caverns_list[23])
    _parse_caverns_actual_caverns(account, raw_caverns_list[7])
    _parse_caverns_majiks(account, raw_caverns_list[4], raw_caverns_list[5], raw_caverns_list[6], raw_caverns_list[11])
    _parse_caverns_schematics(account, raw_caverns_list[13])
    _parse_caverns_measurements(account, raw_caverns_list[22])
    _parse_caverns_biome1(account, raw_caverns_list)
    _parse_caverns_biome2(account, raw_caverns_list)

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
                'LevelPercent': 100 * (float(villager_exp[villager_index]) / getVillagerEXPRequired(villager_index, villager_levels[villager_index])),
            }
            account.gemshop[f"Parallel Villagers {villager_data['Role']}"] = parallel_villagers[villager_index]
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
                'OpalsFound': 0 if cavern_name == 'Camp' else opals_per_cavern[cavern_index - 1],
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
                    'Level': raw_majiks[majik_type][majik_index],
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
        raw_pocket_div_links = [int(v) for v in extras[29:31]]
    except ValueError:
        raw_pocket_div_links = [-1, -1]
        logger.exception(f"Could not cast Pocket Divinity link values to ints: {extras[29:31]}. Defaulting to no links.")
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
        pass
    for schematic_index, schematic_details in enumerate(caverns_engineer_schematics):
        clean_name = schematic_details[0].replace("_", " ")
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
            #logger.warning(f"Error processing schematic {clean_name} at index {schematic_index}")
            account.caverns['Schematics'][clean_name] = {
                'Purchased': False,
                'Image': f'engineer-schematic-{schematic_index}',
                'Description': schematic_details[5].replace("_", " "),
                'UnlockOrder': caverns_engineer_schematics_unlock_order.index(schematic_index) + 1,
                'Resource': resource_type
            }

def _parse_caverns_measurements(account, raw_measurements_list):
    for measurement_index, measurement_details in enumerate(caverns_measurer_measurements):
        try:
            account.caverns['Measurements'][measurement_index] = {
                'Level': raw_measurements_list[measurement_index],
                'Unit': measurement_details[0],
                'Description': measurement_details[1],
                'ScalesWith': measurement_details[2],
                'Image': f"measurement-{measurement_index}",
                'Resource': measurement_details[3],
                'MeasurementNumber': measurement_index + 1
            }
        except:
            account.caverns['Measurements'][measurement_index] = {
                'Level': 0,
                'Unit': measurement_details[0],
                'Description': measurement_details[1],
                'ScalesWith': measurement_details[2],
                'Image': f"measurement-{measurement_index}",
                'Resource': measurement_details[3],
                'MeasurementNumber': measurement_index + 1
            }

def _parse_caverns_biome1(account, raw_caverns_list):
    _parse_caverns_the_well(account, raw_caverns_list)
    _parse_caverns_motherlode(account, raw_caverns_list)
    _parse_caverns_the_den(account, raw_caverns_list)
    _parse_caverns_bravery_monument(account, raw_caverns_list)
    _parse_caverns_the_bell(account, raw_caverns_list)

def _parse_caverns_the_well(account, raw_caverns_list):
    try:
        account.caverns['Caverns']['The Well']['BucketTargets'] = [int(entry) for entry in raw_caverns_list[10][:max_buckets]]
    except:
        account.caverns['Caverns']['The Well']['BucketTargets'] = [0] * max_buckets
    try:
        account.caverns['Caverns']['The Well']['SedimentsOwned'] = [int(entry) for entry in raw_caverns_list[9][:max_sediments]]
    except:
        # Gravel starts at 0, the rest are Negative
        account.caverns['Caverns']['The Well']['SedimentsOwned'] = [entry * -1 for entry in sediment_bars]
    try:
        account.caverns['Caverns']['The Well']['SedimentLevels'] = raw_caverns_list[8]
    except:
        account.caverns['Caverns']['The Well']['SedimentLevels'] = [0] * max_sediments
    try:
        account.caverns['Caverns']['The Well']['BarExpansion'] = raw_caverns_list[11][10]
    except:
        account.caverns['Caverns']['The Well']['BarExpansion'] = False
    try:
        account.caverns['Caverns']['The Well']['Holes-11-9'] = raw_caverns_list[11][9]
    except:
        account.caverns['Caverns']['The Well']['Holes-11-9'] = 0

def _parse_caverns_motherlode(account, raw_caverns_list):
    cavern_name = 'Motherlode'
    motherlode_offset = 0
    try:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = raw_caverns_list[11][0 + motherlode_offset]
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = raw_caverns_list[11][1 + motherlode_offset]
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
    try:
        account.caverns['Caverns'][cavern_name]['Charges'] = {
            'Ring': [raw_caverns_list[18][0], raw_caverns_list[18][1], getBellExpRequired(0, raw_caverns_list[18][1])],
            'Ping': [raw_caverns_list[18][2], raw_caverns_list[18][3], getBellExpRequired(1, raw_caverns_list[18][3])],
            'Clean': [raw_caverns_list[18][4], raw_caverns_list[18][5], getBellExpRequired(2, raw_caverns_list[18][5])],
            'Renew': [raw_caverns_list[18][6], raw_caverns_list[18][7], getBellExpRequired(3, raw_caverns_list[18][7])],
        }
    except:
        account.caverns['Caverns'][cavern_name]['Charges'] = {
            'Ring': [0, 0, getBellExpRequired(0, 0)],
            'Ping': [0, 0, getBellExpRequired(1, 0)],
            'Clean': [0, 0, getBellExpRequired(2, 0)],
            'Renew': [0, 0, getBellExpRequired(3, 0)],
        }

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
        account.caverns['Caverns'][cavern_name]['NotesOwned'] = [int(entry) for entry in raw_caverns_list[9][max_sediments:max_sediments+max_harp_notes]]
    except:
        account.caverns['Caverns'][cavern_name]['NotesOwned'] = [0] * max_harp_notes

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

def _parse_caverns_the_hive(account, raw_caverns_list):
    cavern_name = 'The Hive'
    motherlode_offset = 2
    try:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = raw_caverns_list[11][0 + motherlode_offset]
    except:
        account.caverns['Caverns'][cavern_name]['ResourcesCollected'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = raw_caverns_list[11][1 + motherlode_offset]
    except:
        account.caverns['Caverns'][cavern_name]['LayersDestroyed'] = 0

def _parse_caverns_grotto(account, raw_caverns_list):
    cavern_name = 'Grotto'
    try:
        account.caverns['Caverns'][cavern_name]['PlayerKills'] = raw_caverns_list[11][27]
    except:
        account.caverns['Caverns'][cavern_name]['PlayerKills'] = 0
    try:
        account.caverns['Caverns'][cavern_name]['KillsRequired'] = getGrottoKills(account.caverns['Caverns'][cavern_name]['OpalsFound'])
    except:
        account.caverns['Caverns'][cavern_name]['KillsRequired'] = getGrottoKills(0)
    account.caverns['Caverns'][cavern_name]['KillsRemaining'] = (
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
    _parse_w6_gemstones(account, raw_ninja_list)
    _parse_w6_jade_emporium(account, raw_ninja_list)
    _parse_w6_beanstalk(account, raw_ninja_list)

def _parse_w6_gemstones(account, raw_ninja_list):
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
    for gemstoneIndex, gemstoneName in enumerate(sneakingGemstonesList):
        account.sneaking["Gemstones"][gemstoneName] = {
            "Level": safer_get(account.raw_optlacc_dict, sneakingGemstonesFirstIndex + gemstoneIndex, 0),
            "BaseValue": 0,
            "BoostedValue": 0.0,
            "Percent": 0,
            "Stat": ''
        }
        try:
            account.sneaking["Gemstones"][gemstoneName]["Stat"] = sneakingGemstonesStatList[gemstoneIndex]
        except:
            continue
    try:
        account.sneaking["Gemstones"]["Moissanite"]["BaseValue"] = getMoissaniteValue(account.sneaking["Gemstones"]["Moissanite"]["Level"])
    except:
        pass  # Already defaulted to 0
    for gemstoneName in sneakingGemstonesList[0:-1]:
        try:
            account.sneaking["Gemstones"][gemstoneName]["BaseValue"] = getGemstoneBaseValue(
                gemstoneName,
                account.sneaking["Gemstones"][gemstoneName]["Level"],
            )
            account.sneaking["Gemstones"][gemstoneName]["BoostedValue"] = getGemstoneBoostedValue(
                account.sneaking["Gemstones"][gemstoneName]["BaseValue"],
                account.sneaking["Gemstones"]["Moissanite"]["BaseValue"]
            )
        except:
            continue  # Already defaulted to 0
    for gemstoneName in sneakingGemstonesList:
        try:
            account.sneaking["Gemstones"][gemstoneName]["Percent"] = getGemstonePercent(
                gemstoneName,
                account.sneaking["Gemstones"][gemstoneName]["BaseValue"]
            )
        except:
            continue

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
    _parse_w6_farming_crops(account, raw_farmcrop_dict)
    _parse_w6_farming_crop_depot(account)

    raw_farmupg_list = safe_loads(account.raw_data.get("FarmUpg", []))
    _parse_w6_farming_markets(account, raw_farmupg_list)

    raw_farmrank_list = safe_loads(account.raw_data.get("FarmRank", [[0] * 36]))
    _parse_w6_farming_land_ranks(account, raw_farmrank_list)

    account.farming['Total Plots'] = (
            1
            + account.farming['MarketUpgrades']['Land Plots']['Level']
            + account.gemshop['Plot of Land']
            + min(3, account.merits[5][2]['Level'])
    )

def _parse_w6_farming_crops(account, rawCrops):
    if isinstance(rawCrops, dict):
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
                account.farming['CropsUnlocked'],
                bonusDetails['x1'],
                bonusDetails['x2']
            ),
            'BaseValuePlus1': lavaFunc(
                bonusDetails['funcType'],
                min(maxFarmingCrops, account.farming['CropsUnlocked'] + 1),
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
    while len(raw_summoning_list) < 5:
        raw_summoning_list.append([])

    # raw_summoning_list[0] = Upgrades
    if raw_summoning_list[0]:
        account.summoning["Upgrades"] = raw_summoning_list[0]
    else:
        account.summoning["Upgrades"] = [0] * max_summoning_upgrades

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
    try:
        _parse_w6_summoning_sanctuary(account, raw_summoning_list[4])
    except:
        _parse_w6_summoning_sanctuary(account, [])

    # Used later to create a list of Advices for Winner Bonuses. Can be added directly into an AdviceGroup as the advices attribute
    account.summoning['WinnerBonusesAdvice'] = []

def _parse_w6_summoning_battles(account, rawBattles):
    regular_battles = [battle for battle in rawBattles if not battle.startswith('rift')]
    try:
        account.summoning['Battles']['NormalTotal'] = len(regular_battles)
    except:
        account.summoning['Battles']['NormalTotal'] = 0

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
    while true_battle_index < max(40, account.summoning['Battles']['Endless'] + 5):
        image_index = (true_battle_index % 100) // 20
        endless_enemy_index = true_battle_index % 40
        this_battle = {
            'Defeated': true_battle_index < account.summoning['Battles']['Endless'],
            'Image': summoning_endlessEnemies.get(image_index, ''),
            'RewardType': summoning_endlessDict.get(endless_enemy_index, {}).get('RewardID', 'Unknown'),
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
    if rawSanctuary:
        try:
            # [2,3,2,1,1,0,0,0,0,0,0,0,0,0]
            account.summoning['SanctuaryTotal'] = int(rawSanctuary[0])  # Gray Slimes
            account.summoning['SanctuaryTotal'] += 3 * int(rawSanctuary[1])  # Vrumbi
            account.summoning['SanctuaryTotal'] += 12 * int(rawSanctuary[2])  # Bloomie
            account.summoning['SanctuaryTotal'] += 60 * int(rawSanctuary[3])  # Tonka
            account.summoning['SanctuaryTotal'] += 360 * int(rawSanctuary[4])  # Regalis
            # account.summoning['SanctuaryTotal'] += 2520 * int(raw_summoning_list[4][5])  #Sparkie
        except:
            pass
