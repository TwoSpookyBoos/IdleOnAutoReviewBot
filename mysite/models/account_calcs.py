from math import ceil, floor, log2, prod

from consts.consts_autoreview import ValueToMulti, EmojiType, MultiToValue, default_huge_number_replacement
from consts.consts_caverns import (
    caverns_cavern_names, schematics_unlocking_buckets, schematics_unlocking_harp_strings,
    schematics_unlocking_harp_chords,
    caverns_conjuror_majiks, caverns_measurer_scalars, monument_names, released_monuments, monument_bonuses,
    getBellImprovementBonus
)
from consts.consts_general import getNextESFamilyBreakpoint, vault_stack_types, storage_chests_item_slots_max, \
    greenstack_amount
from consts.idleon.consts_idleon import base_crystal_chance
from consts.idleon.lava_func import lava_func
from consts.consts_master_classes import grimoire_stack_types, grimoire_coded_stack_monster_order
from consts.consts_monster_data import decode_monster_name
from consts.consts_w1 import get_statue_type_index_from_name, get_seraph_cosmos_summ_level_goal, \
    get_seraph_cosmos_max_summ_level_goal, get_seraph_cosmos_multi, \
    get_seraph_stacks, seraph_max
from consts.consts_w1 import statues_dict
from consts.consts_w2 import fishing_toolkit_dict, islands_trash_shop_costs, killroy_dict
from consts.consts_w3 import arbitrary_shrine_goal, arbitrary_shrine_note, buildings_towers, buildings_shrines
from consts.consts_w4 import tomepct, max_meal_count, max_meal_level, max_nblb_bubbles, max_cooking_ribbon
from consts.consts_w5 import max_sailing_artifact_level, divinity_offerings_dict, divinity_DivCostAfter3, \
    filter_recipes, filter_never, filter_only_after_gstack
from consts.consts_w6 import summoning_rewards_that_dont_multiply_base_value
from consts.w6.farming import max_farming_value
from consts.progression_tiers import owl_bonuses_of_orion
from models.advice.advice import Advice
from models.advice.generators.general import get_upgrade_vault_advice
from utils.all_talentsDict import all_talentsDict
from utils.logging import get_logger
from utils.misc.has_companion import has_companion
from utils.safer_data_handling import safe_loads, safer_get, safer_convert, safer_math_pow, safer_math_log
from utils.text_formatting import getItemDisplayName, notateNumber
from utils.number_formatting import round_and_trim

logger = get_logger(__name__)

def calculate_account(account):
    _calculate_wave_1(account)
    _calculate_wave_2(account)
    _calculate_wave_3(account)
    _calculate_wave_4(account)


def _calculate_wave_1(account):
    # These numbers are used by formulas in _calculate_wave_2, so must be calculated first
    _calculate_caverns_majiks(account)
    _calculate_w3_armor_sets(account)
    _calculate_w2_arcade(account)
    _calculate_master_classes_tesseract_upgrades(account)
    _calculate_w6_emperor(account)
    _calculate_w6_summoning_winner_bonuses(account)
    _calculate_w6_summoning_regular_bonuses(account)
    _calculate_w6_summoning_endless_bonuses(account)
    _calculate_w4_tome(account)
    _calculate_w7_legend_talents(account)

def _calculate_caverns_majiks(account):
    alt_pocket_div = {
        'BonusPerLevel': 15,
        'Description': '% All Stats'
    }
    for majik_type, majiks in caverns_conjuror_majiks.items():
        for majik_index, majik_data in enumerate(majiks):
            if majik_data['Name'] == 'Pocket Divinity' and has_companion('King Doot'):
                #Replace linked Divinities with 15% all stat
                account.caverns['Majiks'][majik_data['Name']]['Description'] = alt_pocket_div['Description']
                account.caverns['Majiks'][majik_data['Name']]['Value'] = (
                    account.caverns['Majiks'][majik_data['Name']]['Level'] * alt_pocket_div['BonusPerLevel']
                )
                account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                        majik_data['MaxLevel'] * alt_pocket_div['BonusPerLevel']
                )
            elif majik_data['Scaling'] == 'add':
                try:
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = (
                            account.caverns['Majiks'][majik_data['Name']]['Level'] * majik_data['BonusPerLevel']
                    )
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                            majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                    )
                except:
                    logger.exception(f"Caverns Majik value calc error for level {account.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}")
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = 0
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                            majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                    )
            elif majik_data['Scaling'] == 'value':
                try:
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = (ValueToMulti(
                        account.caverns['Majiks'][majik_data['Name']]['Level'] * majik_data['BonusPerLevel']
                    ))
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (ValueToMulti(
                        majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                    ))
                except:
                    logger.exception(f"Caverns Majik value calc error for level {account.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}")
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = (ValueToMulti(
                        0 * majik_data['BonusPerLevel']
                    ))
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (ValueToMulti(
                        majik_data['MaxLevel'] * majik_data['BonusPerLevel']
                    ))
            elif majik_data['Scaling'] == 'multi':
                try:
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = (
                        # BonusPerLevel to the power of Level
                        majik_data['BonusPerLevel'] ** account.caverns['Majiks'][majik_data['Name']]['Level']
                    )
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                        # BonusPerLevel to the power of Level
                        majik_data['BonusPerLevel'] ** majik_data['MaxLevel']
                    )
                except:
                    logger.exception(f"Caverns Majik value calc error for level {account.caverns['Majiks'][majik_data['Name']]['Level']} {majik_data['Name']}")
                    account.caverns['Majiks'][majik_data['Name']]['Value'] = (
                        # BonusPerLevel to the power of Level
                        0
                    )
                    account.caverns['Majiks'][majik_data['Name']]['MaxValue'] = (
                        # BonusPerLevel to the power of Level
                        majik_data['BonusPerLevel'] ** majik_data['MaxLevel']
                    )
            account.caverns['Majiks'][majik_data['Name']]['Description'] = (
                f"{round(account.caverns['Majiks'][majik_data['Name']]['Value'], 2):g}"
                f"/{round(account.caverns['Majiks'][majik_data['Name']]['MaxValue'], 2):g}"
                f"{account.caverns['Majiks'][majik_data['Name']]['Description']}"
            )
            # logger.debug(f"{majik_data['Name']} value set to {account.caverns['Majiks'][majik_data['Name']]['Value']}")

def _calculate_w3_armor_sets(account):
    armor_set_multi = ValueToMulti(0)
    for set_name, set_details in account.armor_sets['Sets'].items():
        # Calculate the Total Value and Generate Description
        if '{' in account.armor_sets['Sets'][set_name]['Bonus Type']:
            account.armor_sets['Sets'][set_name]['Total Value'] = (
                account.armor_sets['Sets'][set_name]['Owned']
                * account.armor_sets['Sets'][set_name]['Base Value']
                * armor_set_multi
            )
            account.armor_sets['Sets'][set_name]['Description'] = account.armor_sets['Sets'][set_name]['Bonus Type'].replace(
                '{', f"{account.armor_sets['Sets'][set_name]['Total Value']}"
            )
        if '}' in account.armor_sets['Sets'][set_name]['Bonus Type']:
            account.armor_sets['Sets'][set_name]['Total Value'] = ValueToMulti(
                account.armor_sets['Sets'][set_name]['Owned']
                * account.armor_sets['Sets'][set_name]['Base Value']
                * armor_set_multi
            )
            account.armor_sets['Sets'][set_name]['Description'] = account.armor_sets['Sets'][set_name]['Bonus Type'].replace(
                '}', f"{account.armor_sets['Sets'][set_name]['Total Value']:.2f}"
            )

def _calculate_w6_emperor(account):
    # Dependency: _calculate_master_classes_tesseract_upgrades, sneaking, _calculate_w2_arcade, gemshop
    account.emperor.calculate_max_attempt(account.gemshop, account.sneaking.emporium)
    account.emperor.calculate_bonus_multi(account.arcade, account.tesseract)
    account.emperor.calculate_bonuses()


def _calculate_w6_summoning_winner_bonuses(account):
    # _customBlock_Summoning -> if ("WinBonus" == e)
    # Last updated in v2.48 Dec 9
    # The 'base' value of a normal match is multiplied by 3.5. This is handled by the match itself, not part of this function.
    # 3.5 * c.asNumber(a.engine.getGameAttribute("DNSM").h.SummWinBonus[0 | t])
    # The REASON this is handled by the match is Endless Summoning (20 <= t && 33 >= t) does NOT multiply by 3.5. Silly shit.
    # Below, we calculate the rest of the multiplier that will eventually multiply the Match's value
# Multi Group A: Pristine Charm - Crystal Comb
    # * (1 + m._customBlock_Ninja("PristineBon", 8, 0) / 100)
    max_mga = 1.3
    player_mga = ValueToMulti(account.sneaking.pristine_charms['Crystal Comb'].value)

# Multi Group B: Gem Shop - King of all Winners
    # * (1 + 10 * c.asNumber(a.engine.getGameAttribute("GemItemsPurchased")[11]) / 100)
    max_mgb = ValueToMulti(10 * account.gemshop['Purchases']['King Of All Winners']['MaxLevel'])
    player_mgb = ValueToMulti(10 * account.gemshop['Purchases']['King Of All Winners']['Owned'])

# Multi Group C: Summoning Winner Bonuses, some of which apply only to certain upgrades
    # * (1 +
    #       (m._customBlock_Sailing("ArtifactBonus", 32, 0)
    #       + (Math.min(10, c.asNumber(a.engine.getGameAttribute("Tasks")[2][5][4]))
    #       + (q._customBlock_AchieveStatus(379)
    #       + (q._customBlock_AchieveStatus(373)
    #       + (m._customBlock_Summoning("WinBonus", 31, 0)  IMPORTANT: THIS IS NOT PRESENT FOR LIBRARY
    #       + (m._customBlock_Thingies("EmperorBon", 8, 0)  IMPORTANT: THIS IS NOT PRESENT FOR LIBRARY
    #       + m._customBlock_GetSetBonus("GODSHARD_SET", "Bonus", 0, 0))))
    #   ) / 100)
    max_mgc_rest = ValueToMulti(
        (25 * max_sailing_artifact_level)
        + account.merits[5][4]['MaxLevel']  # World 6 Merit Shop
        + 1  # int(account.achievements['Spectre Stars'])
        + 1  # int(account.achievements['Regalis My Beloved'])
        + account.summoning['Endless Bonuses']['<x Winner Bonuses']
        + MultiToValue(account.armor_sets['Sets']['GODSHARD SET']['Total Value'])
        + account.emperor["Summoning Winner Bonuses"].value  # Technically infinite
    )
    max_mgc_library = ValueToMulti(
        # 19 == t ? Library bonus's index
        (25 * max_sailing_artifact_level)
        + account.merits[5][4]['MaxLevel']  #World 6 Merit Shop
        + 1  #int(account.achievements['Spectre Stars'])
        + 1  #int(account.achievements['Regalis My Beloved'])
        + MultiToValue(account.armor_sets['Sets']['GODSHARD SET']['Total Value'])
    )

    player_mgc_rest = ValueToMulti(
        (25 * account.sailing['Artifacts']['The Winz Lantern']['Level'])
        + account.merits[5][4]['Level']
        + int(account.achievements['Spectre Stars']['Complete'])
        + int(account.achievements['Regalis My Beloved']['Complete'])
        + account.summoning['Endless Bonuses']['<x Winner Bonuses']
        + MultiToValue(account.armor_sets['Sets']['GODSHARD SET']['Total Value'])
        + account.emperor["Summoning Winner Bonuses"].value
    )
    player_mgc_library = ValueToMulti(
        (25 * account.sailing['Artifacts']['The Winz Lantern']['Level'])
        + account.merits[5][4]['Level']
        + int(account.achievements['Spectre Stars']['Complete'])
        + int(account.achievements['Regalis My Beloved']['Complete'])
        + MultiToValue(account.armor_sets['Sets']['GODSHARD SET']['Total Value'])
    )

    # Library
    account.summoning['WinnerBonusesMultiLibrary'] = max(1, player_mga * player_mgb * player_mgc_library)
    account.summoning['WinnerBonusesMultiMaxLibrary'] = max(1, max_mga * max_mgb * max_mgc_library)
    account.summoning['WinnerBonusesSummaryLibrary'] = Advice(
        label=f"Winner Bonuses Multi: {account.summoning['WinnerBonusesMultiLibrary']:.3f}/{account.summoning['WinnerBonusesMultiMaxLibrary']:.3f}x",
        picture_class="summoning",
        progression=f"{account.summoning['WinnerBonusesMultiLibrary']:.3f}",
        goal=f"{account.summoning['WinnerBonusesMultiMaxLibrary']:.3f}",
        #unit="x"
    )
    # Not Library
    account.summoning['WinnerBonusesMulti'] = {}
    account.summoning['WinnerBonusesMulti']['Value'] = max(1, player_mga * player_mgb * player_mgc_rest)
    account.summoning['WinnerBonusesMulti']['MultiGroup'] = (player_mga, player_mgb, player_mgc_rest)
    account.summoning['WinnerBonusesMulti']['MultiGroupMax'] = (max_mga, max_mgb, max_mgc_rest)

def _calculate_w6_summoning_regular_bonuses(account):
    # Dependency: _calculate_w6_summoning_winner_bonuses
    bonus_list = account.summoning['Bonuses']
    win_multi = account.summoning['WinnerBonusesMulti']['Value']
    for bonus_name, bonus_value in bonus_list.items():
        bonus = bonus_list[bonus_name]
        if bonus_name == '+{ Library Max':
            libary_multi = account.summoning['WinnerBonusesMultiLibrary']
            bonus['Value'] = round(libary_multi * bonus['Value'])
            bonus['Max'] = round(libary_multi * bonus['Max'])
        else:
            if bonus_name.startswith('<x'):
                bonus['Value'] = ValueToMulti(bonus_list[bonus_name]['Value'] * win_multi)
                bonus['Max'] = ValueToMulti(bonus_list[bonus_name]['Max'] * win_multi)
            else:
                bonus['Value'] *= win_multi
                bonus['Max'] *= win_multi
    #logger.debug(f"Final Regular Bonuses: {account.summoning['Bonuses']}")

def _calculate_w6_summoning_endless_bonuses(account):
    # Dependency: _calculate_w6_summoning_winner_bonuses
    for bonus_name, bonus_value in account.summoning['Endless Bonuses'].items():
        if bonus_name not in summoning_rewards_that_dont_multiply_base_value:
            if bonus_name.startswith('<x'):
                account.summoning['Endless Bonuses'][bonus_name] = ValueToMulti(
                    account.summoning['Endless Bonuses'][bonus_name]
                    * account.summoning['WinnerBonusesMulti']['Value']
                )
            else:
                account.summoning['Endless Bonuses'][bonus_name] *= account.summoning['WinnerBonusesMulti']['Value']
        elif bonus_name in summoning_rewards_that_dont_multiply_base_value and bonus_name.startswith('<x'):
            account.summoning['Endless Bonuses'][bonus_name] = ValueToMulti(account.summoning['Endless Bonuses'][bonus_name])
    #logger.debug(f"Final Endless Bonuses after {account.summoning['Battles']['Endless']} wins: {account.summoning['Endless Bonuses']}")

def _calculate_w2_arcade(account):
    for upgrade_index, upgrade_details in account.arcade.items():
        account.arcade[upgrade_index]['Value'] *= (
            max(1, 2 * account.arcade[upgrade_index]['Cosmic'])
            * max(1, 2 * has_companion('Spirit Reindeer'))
        )

def _calculate_w4_tome(account):
    raw_tome_pcts = account.raw_data.get('serverVars', {}).get('TomePct')
    if raw_tome_pcts is not None:
        raw_tome_pcts = sorted(raw_tome_pcts)
        parsed_tome_pcts = {}
        for percent_index, percent in enumerate(tomepct.keys()):
            try:
                parsed_tome_pcts[percent] = raw_tome_pcts[percent_index]
            except:
                parsed_tome_pcts[percent] = 99999
        for percent, score in parsed_tome_pcts.items():
            if account.tome['Total Points'] > score:
                account.tome['Tome Percent'] = min(account.tome['Tome Percent'], percent)
    else:
        for percent, score in tomepct.items():
            if account.tome['Total Points'] > score:
                account.tome['Tome Percent'] = min(account.tome['Tome Percent'], percent)
    # logger.debug(f"{account.tome['Total Points']} tome points = Top {account.tome['Tome Percent']}%")


def _calculate_wave_2(account):
    _calculate_general(account)
    _calculate_master_classes(account)
    _calculate_w1(account)
    _calculate_w2(account)
    _calculate_master_classes_tesseract_tachyon_sources(account)
    _calculate_w3(account)
    _calculate_w4(account)
    _calculate_w5(account)
    _calculate_caverns(account)
    _calculate_w6(account)
    _calculate_w7(account)

def _calculate_general(account):
    _calculate_general_alerts(account)
    _calculate_general_item_filter(account)
    account.highest_world_reached = _calculate_general_highest_world_reached(account)
    _calculate_general_guild_bonuses(account)
    _calculate_general_storage_slots(account)

def _calculate_general_alerts(account):
    if account.stored_assets.get("Trophy2").amount >= 75 and account.equinox_dreams[17]:
        account.alerts_Advices['General'].append(Advice(
            label=f"You have {account.stored_assets.get('Trophy2').amount}/75 Lucky Lads to craft a Luckier Lad!",
            picture_class="luckier-lad"
        ))

def _calculate_general_item_filter(account):
    raw_fishing_toolkit_lures = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[0]
    raw_fishing_toolkit_lines = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[1]
    for filtered_item_codename in account.item_filter:
        filtered_displayname = getItemDisplayName(filtered_item_codename)
        if (
            filtered_item_codename == 'Trophy2'  #Lucky Lad
            and 'Trophy20' not in account.registered_slab  #Luckier Lad
            and account.stored_assets.get('Trophy2').amount < 75
        ):
            account.alerts_Advices['General'].append(Advice(
                label='Lucky Lad filtered before 75 for Luckier Lad',
                picture_class='lucky-lad',
                resource='luckier-lad'
            ))
        elif filtered_item_codename in filter_recipes:
            for craftable_item_codename in filter_recipes[filtered_item_codename]:
                if craftable_item_codename not in account.registered_slab:
                    account.alerts_Advices['General'].append(Advice(
                        label=f"{filtered_displayname} filtered, {getItemDisplayName(craftable_item_codename)} not in Slab",
                        picture_class=filtered_displayname,
                        resource=craftable_item_codename
                    ))
        elif filtered_item_codename in filter_never and account.autoloot:
            account.alerts_Advices['General'].append(Advice(
                label=f'Why did you filter {filtered_displayname}?',
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename in filter_only_after_gstack and account.autoloot and account.all_assets.get(filtered_item_codename).amount < greenstack_amount:
            account.alerts_Advices['General'].append(Advice(
                label=f'Unfilter {filtered_displayname} until Greenstacked',
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename not in account.registered_slab:
            account.alerts_Advices['General'].append(Advice(
                label=f"{filtered_displayname} filtered, not in Slab",
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename in fishing_toolkit_dict['Lures']:
            # index + 1 needed to account for the default lure which is not an Item registered in Slab
            if fishing_toolkit_dict['Lures'].index(filtered_item_codename) + 1 not in raw_fishing_toolkit_lures.values():
                account.alerts_Advices['General'].append(Advice(
                    label=f"{filtered_displayname} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayname,
                ))
        elif filtered_item_codename in fishing_toolkit_dict['Lines']:
            # index + 1 needed to account for the default line which is not an Item registered in Slab
            if fishing_toolkit_dict['Lines'].index(filtered_item_codename) + 1 not in raw_fishing_toolkit_lines.values():
                account.alerts_Advices['General'].append(Advice(
                    label=f"{filtered_displayname} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayname,
                ))

def _calculate_general_highest_world_reached(account):
    if (
        safer_get(account.raw_optlacc_dict, 408, 0) > 0
        # TODO: add Achievement as another condition once those exist
        or account.enemy_worlds[7].maps_dict[301].kill_count > 0
    ):
        return 7
    elif (
        safer_get(account.raw_optlacc_dict, 194, 0) > 0
        or account.achievements['Valley Visitor']['Complete']
        or account.enemy_worlds[6].maps_dict[251].kill_count > 0
    ):
        return 6
    elif (
        account.achievements['The Plateauourist']['Complete']
        or account.enemy_worlds[5].maps_dict[201].kill_count > 0
    ):
        return 5
    elif (
        account.achievements['Milky Wayfarer']['Complete']
        or account.enemy_worlds[4].maps_dict[151].kill_count > 0
    ):
        return 4
    elif (
        account.achievements['Snowy Wonderland']['Complete']
        or account.enemy_worlds[3].maps_dict[101].kill_count > 0
    ):
        return 3
    elif (
        account.achievements['Down by the Desert']['Complete']
        or account.enemy_worlds[2].maps_dict[51].kill_count > 0
    ):
        return 2
    else:
        return 1

def _calculate_general_guild_bonuses(account):
    for bonus_name, bonus in account.guild_bonuses.items():
        if '{' in bonus['Description']:
            bonus['Description'] = bonus['Description'].replace('{', f"{bonus['Value']:.2f}")
        if '}' in bonus['Description']:
            bonus['Description'] = bonus['Description'].replace('}',f"{100 - bonus['Value']:.2f}")
        if ']' in bonus['Description']:
            if bonus_name == 'Bonus GP for small guilds':
                bonus['Description'] = bonus['Description'].replace(']', f"{10 + bonus['Level']}")

def _calculate_general_storage_slots(account):
    #Dependencies: none
    #Event Shop bonuses only have a description in the source
    event_shop_bonuses = {
        'Storage Chest': 12,
        'Storage Vault': 16
    }
    vault_bonuses = ['Storage Slots']
    construction_buildings = {
        'Chest Space': 2
    }
    gem_shop_purchases = {
        'Storage Chest Space': {
            'Slots': 9,
        },
        'More Storage Space': {
            'Slots': 9,
        }
    }
    for name, slots in event_shop_bonuses.items():
        account.storage['Other Storage'][name] = {
            'Source': 'Event Shop',
            'Label': f"{{{{ Event Shop|#event-shop }}}}: {name}: {slots} slots",
            'Owned Slots': slots * account.event_points_shop['Bonuses'][name]['Owned'],
            'Max Slots': slots,
            'Progression': int(account.event_points_shop['Bonuses'][name]['Owned']),
            'Goal': 1,
            'Image': account.event_points_shop['Bonuses'][name]['Image'],
            'Resource': 'event-point'
        }
    for name in vault_bonuses:
        account.storage['Other Storage'][name] = {
            'Source': 'Vault',
            # Vault bonus Advice is standardized in get_upgrade_vault_advice. Extra entries not needed here.
            'Owned Slots': account.vault['Upgrades'][name]['Value Per Level'] * account.vault['Upgrades'][name]['Level'],
            'Max Slots': account.vault['Upgrades'][name]['Value Per Level'] * account.vault['Upgrades'][name]['Max Level'],
        }
    for name, slots_per_level in construction_buildings.items():
        account.storage['Other Storage'][name] = {
            'Source': 'Construction Building',
            'Label': f"{{{{ Construction Building|#buildings }}}}: {name}: {slots_per_level * (account.construction_buildings[name]['Level'] - 1)} total slots",
            'Owned Slots': slots_per_level * (account.construction_buildings[name]['Level'] - 1),
            'Max Slots': slots_per_level * (account.construction_buildings[name]['MaxLevel'] - 1),
            'Progression': account.construction_buildings[name]['Level'],
            'Goal': account.construction_buildings[name]['MaxLevel'],
            'Image': account.construction_buildings[name]['Image'],

        }
    for name, details in gem_shop_purchases.items():
        gs = account.gemshop['Purchases'][name]
        account.storage['Other Storage'][name] = {
            'Source': 'Gem Shop',
            'Label': f"{{{{ Gem Shop|#gem-shop }}}}: {name} ({gs['Subsection']}): "
                     f"{details['Slots'] * gs['Owned']}/{details['Slots'] * gs['MaxLevel']} total slots",
            'Owned Slots': details['Slots'] * gs['Owned'],
            'Max Slots': details['Slots'] * gs['MaxLevel'],
            'Progression': gs['Owned'],
            'Goal': gs['MaxLevel'],
            'Image': name,
            'Resource': 'gem'
        }

    #Calculate total storage slots
    account.storage['Other Slots Owned'] = sum([details['Owned Slots'] for details in account.storage['Other Storage'].values()])
    account.storage['Total Slots Owned'] = sum([
        account.storage['Used Chest Slots'],
        account.storage['Other Slots Owned']
    ])
    account.storage['Other Slots Max'] = sum([details['Max Slots'] for details in account.storage['Other Storage'].values()])
    account.storage['Total Slots Max'] = sum([
        storage_chests_item_slots_max,
        account.storage['Other Slots Max']
    ])


def _calculate_master_classes(account):
    _calculate_master_classes_grimoire_upgrades(account)
    # _calculate_master_classes_grimoire_bone_sources(account)  #Moved to wave3 as it relies on Caverns/Gambit
    _calculate_master_classes_compass_upgrades(account)
    _calculate_master_classes_compass_dust_sources(account)

def _calculate_master_classes_grimoire_upgrades(account):
    grimoire_multi = ValueToMulti(
        account.grimoire['Upgrades']['Writhing Grimoire']['Level']
        * account.grimoire['Upgrades']['Writhing Grimoire']['Value Per Level']
    )

    for upgrade_name, upgrade_details in account.grimoire['Upgrades'].items():
        # Update description with total value, stack counts, and scaling info
        if '{' in account.grimoire['Upgrades'][upgrade_name]['Description']:
            account.grimoire['Upgrades'][upgrade_name]['Total Value'] = (
                account.grimoire['Upgrades'][upgrade_name]['Level']
                * account.grimoire['Upgrades'][upgrade_name]['Value Per Level']
                * (grimoire_multi if upgrade_details['Scaling Value'] else 1)
            )
            account.grimoire['Upgrades'][upgrade_name]['Description'] = account.grimoire['Upgrades'][upgrade_name]['Description'].replace(
                '{', f"{account.grimoire['Upgrades'][upgrade_name]['Total Value']}"
            )
        if '}' in account.grimoire['Upgrades'][upgrade_name]['Description']:
            account.grimoire['Upgrades'][upgrade_name]['Total Value'] = ValueToMulti(
                account.grimoire['Upgrades'][upgrade_name]['Level']
                * account.grimoire['Upgrades'][upgrade_name]['Value Per Level']
                * (grimoire_multi if upgrade_details['Scaling Value'] else 1)
            )
            account.grimoire['Upgrades'][upgrade_name]['Description'] = account.grimoire['Upgrades'][upgrade_name]['Description'].replace(
                '}', f"{account.grimoire['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )
        if 'Target:$' in account.grimoire['Upgrades'][upgrade_name]['Description']:
            if upgrade_name.split('!')[0] in grimoire_stack_types:
                stack_type = upgrade_name.split('!')[0]
                if len(grimoire_coded_stack_monster_order) < account.grimoire.get(f'{stack_type} Stacks', '0'):
                    next_stack_target = "All done!"
                else:
                    try:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[account.grimoire.get(f'{stack_type} Stacks', '0')])
                    except:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[0])
                account.grimoire['Upgrades'][upgrade_name]['Description'] = account.grimoire['Upgrades'][upgrade_name]['Description'].replace(
                    'Target:$', f"Target: {next_stack_target}"
                )
        account.grimoire['Upgrades'][upgrade_name]['Description'] += (
            f"<br>({account.grimoire['Upgrades'][upgrade_name]['Value Per Level'] * (grimoire_multi if upgrade_details['Scaling Value'] else 1):.2f} per level"
            f"{' after Writhing Grimoire' if upgrade_details['Scaling Value'] else ': Not scaled by Writhing Grimoire'})"
        )

def _calculate_master_classes_grimoire_bone_sources(account):
    # if ("GrimoireBonesDropDEC" == e)
    grimoire_preset_level = 100
    tombstone_preset_level = 100

    for db in account.dbs:
        grimoire_preset_level = max(grimoire_preset_level, db.current_preset_talents.get('196', 0), db.secondary_preset_talents.get('196', 0))
        tombstone_preset_level = max(tombstone_preset_level, db.current_preset_talents.get('198', 0), db.secondary_preset_talents.get('198', 0))

    grimoire_percent = lava_func(
        funcType=all_talentsDict[196]['funcX'],
        level=grimoire_preset_level,
        x1=all_talentsDict[196]['x1'],
        x2=all_talentsDict[196]['x2'],
    )

    account.grimoire['Bone Calc'] = {
        'mga': ValueToMulti(account.sneaking.pristine_charms['Glimmerchain'].value),
        'mgb': ValueToMulti(grimoire_percent),
        'mgc': ValueToMulti(100 * account.caverns['Caverns']['Gambit']['Bonuses'][12]['Unlocked']),
        'mgd': ValueToMulti((25 * min(1, account.all_assets.get('EquipmentHats112').amount))),
        'mge': ValueToMulti(
            account.grimoire['Upgrades']["Bones o' Plenty"]['Total Value']
            + (account.grimoire['Upgrades']['Bovinae Hoarding']['Total Value'] * safer_math_log(account.grimoire['Bone4'], 'Lava'))
            + account.arcade[40]['Value']
            + account.labJewels['Deadly Wrath Jewel']['Value'] * account.labJewels['Deadly Wrath Jewel']['Enabled']
        ),
        'mgf': 1,
        'mgg': ValueToMulti(account.emperor["Deathbringer Extra Bones"].value)
    }
    account.grimoire['Bone Calc']['Total'] = prod(account.grimoire['Bone Calc'].values())

def _calculate_master_classes_compass_upgrades(account):
    compass_circle_multi = ValueToMulti(
        account.compass['Upgrades']['Circle Supremacy']['Base Value']
        + account.compass['Upgrades']['Abomination Slayer XXI']['Base Value']
    )

    for upgrade_name, upgrade_details in account.compass['Upgrades'].items():
        value = (
            account.compass['Upgrades'][upgrade_name]['Base Value']
            * (compass_circle_multi if upgrade_details['Shape'] == 'Circle' else 1)
            * (safer_math_pow(2, account.compass['Upgrades'][upgrade_name]['Level']//50) if upgrade_name == 'Moon of Sneak' else 1)
        )
        # Update description with total value, stack counts, and scaling info
        if '{' in account.compass['Upgrades'][upgrade_name]['Description']:
            account.compass['Upgrades'][upgrade_name]['Total Value'] = value
            account.compass['Upgrades'][upgrade_name]['Description'] = account.compass['Upgrades'][upgrade_name]['Description'].replace(
                '{', f"{account.compass['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )
        if '}' in account.compass['Upgrades'][upgrade_name]['Description']:
            account.compass['Upgrades'][upgrade_name]['Total Value'] = ValueToMulti(value)
            account.compass['Upgrades'][upgrade_name]['Description'] = account.compass['Upgrades'][upgrade_name]['Description'].replace(
                '}', f"{account.compass['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )
        account.compass['Upgrades'][upgrade_name]['Description'] += (
            f"<br>({account.compass['Upgrades'][upgrade_name]['Value Per Level'] * (compass_circle_multi if upgrade_details['Shape'] == 'Circle' else 1):.2f} per level"
            f"{' after Circle Multis' if upgrade_details['Shape'] == 'Circle' else ''})"
        )

def _calculate_master_classes_compass_dust_sources(account):
    # _customBlock_Windwalker if ("ExtraDust" == e)
    ww_preset_level = 100
    for ww in account.wws:
        if ww.current_preset_talents.get('421', 0) >= ww_preset_level:
            ww_preset_level = ww.current_preset_talents.get('421', 0)
        if ww.secondary_preset_talents.get('421', 0) >= ww_preset_level:
            ww_preset_level = ww.secondary_preset_talents.get('421', 0)
    compass_percent = lava_func(
        funcType=all_talentsDict[421]['funcX'],
        level=ww_preset_level,
        x1=all_talentsDict[421]['x1'],
        x2=all_talentsDict[421]['x2'],
    )
    account.compass['Dust Calc'] = {
        'mga': ValueToMulti(
            account.compass['Upgrades']['Mountains of Dust']['Total Value']
            + (account.compass['Upgrades']['Solardust Hoarding']['Total Value'] * safer_math_log(account.compass['Dust3'], 'Lava'))
        ),
        'mgb': account.compass['Upgrades']['Spire of Dust']['Total Value'],
        'mgc': ValueToMulti(account.sneaking.pristine_charms['Twinkle Taffy'].value),
        'mgd': ValueToMulti(
            (25 * min(1, account.all_assets.get('EquipmentHats118').amount))
        ),
        'mge': 1,
        'mgf': ValueToMulti(
            + compass_percent
            + account.arcade[47]['Value']
            + account.labJewels['North Winds Jewel']['Value'] * account.labJewels['North Winds Jewel']['Enabled']
            + account.compass['Upgrades']['De Dust I']['Total Value']
            + account.compass['Upgrades']['De Dust II']['Total Value']
            + account.compass['Upgrades']['De Dust III']['Total Value']
            + account.compass['Upgrades']['De Dust IV']['Total Value']
            + account.compass['Upgrades']['De Dust V']['Total Value']
            + account.compass['Upgrades']['Abomination Slayer IX']['Total Value']
            + account.compass['Upgrades']['Abomination Slayer XXX']['Total Value']
            + account.compass['Upgrades']['Abomination Slayer XXXIV']['Total Value']
        ),
        'mgg': ValueToMulti(account.emperor["Windwalker Extra Dust"].value)
    }
    account.compass['Dust Calc']['Total'] = prod(account.compass['Dust Calc'].values())

def _calculate_master_classes_tesseract_upgrades(account):
    for upgrade_name, upgrade_details in account.tesseract['Upgrades'].items():
        tesseract_multi = 1
        # Update description with total value, stack counts, and scaling info
        if '{' in account.tesseract['Upgrades'][upgrade_name]['Description']:
            account.tesseract['Upgrades'][upgrade_name]['Total Value'] = (
                    account.tesseract['Upgrades'][upgrade_name]['Level']
                    * account.tesseract['Upgrades'][upgrade_name]['Value Per Level']
                    * tesseract_multi
            )
            account.tesseract['Upgrades'][upgrade_name]['Description'] = account.tesseract['Upgrades'][upgrade_name]['Description'].replace(
                '{', f"{account.tesseract['Upgrades'][upgrade_name]['Total Value']}"
            )
        if '}' in account.tesseract['Upgrades'][upgrade_name]['Description']:
            account.tesseract['Upgrades'][upgrade_name]['Total Value'] = ValueToMulti(
                account.tesseract['Upgrades'][upgrade_name]['Level']
                * account.tesseract['Upgrades'][upgrade_name]['Value Per Level']
                * tesseract_multi
            )
            account.tesseract['Upgrades'][upgrade_name]['Description'] = account.tesseract['Upgrades'][upgrade_name]['Description'].replace(
                '}', f"{account.tesseract['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )

def _calculate_master_classes_tesseract_tachyon_sources(account):
    # Dependency: _calculate_w2_vials(account)
    # _customBlock_ArcaneType: "ExtraTachyon" == d
    tesseract_preset_level = 100
    backup_energy_preset_level = 100

    tesseract_talent_index = 586
    backup_energy_talent_index = 599

    for ac in account.acs:
        tesseract_preset_level = max(tesseract_preset_level, ac.current_preset_talents.get(str(tesseract_talent_index), 0), ac.secondary_preset_talents.get(str(tesseract_talent_index), 0))
        backup_energy_preset_level = max(backup_energy_preset_level, ac.current_preset_talents.get(str(backup_energy_talent_index), 0), ac.secondary_preset_talents.get(str(backup_energy_talent_index), 0))

    tesseract_talent_bonus_value = lava_func(
        funcType=all_talentsDict[tesseract_talent_index]['funcX'],
        level=tesseract_preset_level,
        x1=all_talentsDict[tesseract_talent_index]['x1'],
        x2=all_talentsDict[tesseract_talent_index]['x2'],
    )

    backup_energy_bonus_value = lava_func(
        funcType=all_talentsDict[backup_energy_talent_index]['funcX'],
        level=backup_energy_talent_index,
        x1=all_talentsDict[backup_energy_talent_index]['x1'],
        x2=all_talentsDict[backup_energy_talent_index]['x2'],
    )

    account.tesseract['Tachyon Calc'] = {
        'mga': ValueToMulti(
            account.tesseract['Upgrades']['Ripple in Spacetime']['Total Value']
            + tesseract_talent_bonus_value
            + account.tesseract['Upgrades']['Verdon Hoarding']['Total Value'] * safer_math_log(account.tesseract['Tachyon3'], 10)
            + account.tesseract['Upgrades']['Aurion Hoarding']['Total Value'] * safer_math_log(account.tesseract['Tachyon6'], 10)
            # + Extra Tachyon from Equipment
            + account.labJewels['Eternal Energy Jewel']['Value'] * account.labJewels['Eternal Energy Jewel']['Owned']
            + account.arcade[50]['Value']
        ),
        'mgb': ValueToMulti(
            account.emperor["Arcane Cultist Extra Tachyons"].value
            + account.alchemy_bubbles['Tachyon Bubble']['BaseValue']
        ),
        'mgc': ValueToMulti(account.sneaking.pristine_charms['Mystery Fizz'].value),
        'mgd': ValueToMulti(backup_energy_bonus_value),
        'mge': 1 + 0.2 * account.gemshop['Bundles']['bun_x']['Owned'],
        'mgf': ValueToMulti(account.alchemy_vials["Paper Pint (Chapter Three 'This is Gospel')"]['Value']),
        'mgg': 4 * has_companion('Balloonfish'),
    }
    account.tesseract['Tachyon Calc']['Total'] = prod(account.tesseract['Tachyon Calc'].values())


def _calculate_w1(account):
    _calculate_w1_upgrade_vault(account)
    _calculate_w1_starsigns(account)
    # _calculate_w1_statues(account)  #Moved to Wave 4 as it relies on Talent levels
    _calculate_w1_stamps(account)
    _calculate_w1_owl_bonuses(account)
    _calculate_w1_minigames(account)

def _calculate_w1_upgrade_vault(account):
    vault_multi = [
        ValueToMulti(
            account.vault['Upgrades']['Vault Mastery']['Level']
            * account.vault['Upgrades']['Vault Mastery']['Value Per Level']
        ),
        ValueToMulti(
            account.vault['Upgrades']['Vault Mastery II']['Level']
            * account.vault['Upgrades']['Vault Mastery II']['Value Per Level']
        )
    ]
    vault_multi_max = [
        ValueToMulti(
            account.vault['Upgrades']['Vault Mastery']['Max Level']
            * account.vault['Upgrades']['Vault Mastery']['Value Per Level']
        ),
        ValueToMulti(
            account.vault['Upgrades']['Vault Mastery II']['Max Level']
            * account.vault['Upgrades']['Vault Mastery II']['Value Per Level']
        )
    ]
    # logger.debug(f"{vault_multi = }")
    for upgrade_name, upgrade_details in account.vault['Upgrades'].items():
        upgrade_scaling_multiplier = vault_multi[upgrade_details['Vault Section'] - 1] if upgrade_details['Scaling Value'] else 1
        upgrade_scaling_multiplier_max = vault_multi_max[upgrade_details['Vault Section'] - 1] if upgrade_details['Scaling Value'] else 1
        upgrade_total_value = (
                account.vault['Upgrades'][upgrade_name]['Level']
                * account.vault['Upgrades'][upgrade_name]['Value Per Level']
                * upgrade_scaling_multiplier
        )
        upgrade_total_value_max = (
                account.vault['Upgrades'][upgrade_name]['Max Level']
                * account.vault['Upgrades'][upgrade_name]['Value Per Level']
                * upgrade_scaling_multiplier_max
        )
        # Update description with total value, stack counts, and scaling info
        if '{' in account.vault['Upgrades'][upgrade_name]['Description']:
            account.vault['Upgrades'][upgrade_name]['Total Value'] = upgrade_total_value
            account.vault['Upgrades'][upgrade_name]['Max Value'] = upgrade_total_value_max
            account.vault['Upgrades'][upgrade_name]['Description'] = account.vault['Upgrades'][upgrade_name]['Description'].replace(
                '{', f"{account.vault['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )
        if '}' in account.vault['Upgrades'][upgrade_name]['Description']:
            account.vault['Upgrades'][upgrade_name]['Total Value'] = ValueToMulti(upgrade_total_value)
            account.vault['Upgrades'][upgrade_name]['Max Value'] = ValueToMulti(upgrade_total_value_max)
            account.vault['Upgrades'][upgrade_name]['Description'] = account.vault['Upgrades'][upgrade_name]['Description'].replace(
                '}', f"{account.vault['Upgrades'][upgrade_name]['Total Value']:.2f}"
            )
        if 'Target:&' in account.vault['Upgrades'][upgrade_name]['Description']:
            if upgrade_name.split('!')[0] in vault_stack_types:
                stack_type = upgrade_name.split('!')[0]
                if len(grimoire_coded_stack_monster_order) < account.vault.get(f'{stack_type} Stacks', '0'):
                    next_stack_target = "All done!"
                else:
                    try:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[account.vault.get(f'{stack_type} Stacks', '0')])
                    except:
                        next_stack_target = decode_monster_name(grimoire_coded_stack_monster_order[0])
                account.vault['Upgrades'][upgrade_name]['Description'] = account.vault['Upgrades'][upgrade_name]['Description'].replace(
                    'Target:&', f"Target: {next_stack_target}"
                )
        account.vault['Upgrades'][upgrade_name]['Description'] += (
            f"<br>({account.vault['Upgrades'][upgrade_name]['Value Per Level'] * upgrade_scaling_multiplier:.2f} per level"
            f"{' after Vault Mastery ' if upgrade_details['Scaling Value'] else ': Not scaled by Vault Mastery '}"
            f"{upgrade_details['Vault Section']}"
            f")"
        )

def _calculate_w1_starsigns(account):
    seraph_summoning_player = get_seraph_cosmos_max_summ_level_goal(account.tesseract['Upgrades']['Astrology Cultism']['Level'])
    account.star_sign_extras['SeraphMulti'] = get_seraph_cosmos_multi(
        astrology_cultism_level=account.tesseract['Upgrades']['Astrology Cultism']['Level'],
        all_summoning_levels=account.all_skills['Summoning']
    )
    account.star_sign_extras['SeraphGoal'] = get_seraph_cosmos_summ_level_goal(
        astrology_cultism_level=account.tesseract['Upgrades']['Astrology Cultism']['Level'],
        all_summoning_levels=account.all_skills['Summoning']
    )
    min_level_stacks = get_seraph_stacks(min(account.all_skills['Summoning'], default=0))
    max_level_stacks = get_seraph_stacks(max(account.all_skills['Summoning'], default=0))
    inequality_notice = ' (Note: Some lower leveled characters have less)' if min_level_stacks != max_level_stacks else ''
    if account.star_signs['Seraph Cosmos']['Unlocked']:
        account.star_sign_extras['SeraphEval'] = f"Multis Passive signs by {round(account.star_sign_extras['SeraphMulti'], 3):g}/{seraph_max}x."
    else:
        account.star_sign_extras['SeraphEval'] = f"Locked. Would increase other Passive signs by {account.star_sign_extras['SeraphMulti']:.2f}/{seraph_max}x if unlocked.{inequality_notice}"
        account.star_sign_extras['SeraphMulti'] = 1
    if account.star_sign_extras['SeraphGoal'] < seraph_summoning_player:
        account.star_sign_extras['SeraphEval'] += f" Increases every 20 Summoning levels.{inequality_notice}"
    account.star_sign_extras['SeraphAdvice'] = Advice(
        label=f"{{{{ Star Sign|#star-signs }}}}: Seraph Cosmos: {account.star_sign_extras['SeraphEval']}",
        picture_class='seraph-cosmos',
        progression=max(account.all_skills['Summoning'], default=0),
        goal=account.star_sign_extras['SeraphGoal'],
        completed=(
            True if account.star_sign_extras['SeraphMulti'] == seraph_max
            else None
        )
    )

    if account.labChips.get('Silkrode Nanochip', 0) > 0:
        account.star_sign_extras['DoublerOwned'] = True
        account.star_sign_extras['SilkrodeNanoEval'] = f"{account.labChips.get('Silkrode Nanochip', 0)} owned. Doubles star signs when equipped."
        account.star_sign_extras['SilkrodeNanoMulti'] = 2
    else:
        account.star_sign_extras['DoublerOwned'] = False
        account.star_sign_extras['SilkrodeNanoEval'] = "None Owned. Would double other signs if equipped."
        account.star_sign_extras['SilkrodeNanoMulti'] = 1
    account.star_sign_extras['SilkrodeNanoAdvice'] = Advice(
        label=f"Lab Chip: Silkrode Nanochip: {account.star_sign_extras['SilkrodeNanoEval']}",
        picture_class="silkrode-nanochip",
        progression=1 if account.labChips.get('Silkrode Nanochip', 0) > 0 else 0,
        goal=1
    )


def _calculate_w1_stamps(account):
    # Dependency: _calculate_w7_legend_talents
    # `"StampDoubler" == d` in source. Last Updated in v2.43 Nov 6
    account.exalted_stamp_multi = ValueToMulti(
        100 #base
        + (
            account.atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Level']
            * account.atom_collider['Atoms']['Aluminium - Stamp Supercharger']['Value per Level']
        )
        + account.sneaking.pristine_charms['Jellypick'].value
        + account.compass['Upgrades']['Abomination Slayer XVII']['Total Value']
        + MultiToValue(account.armor_sets['Sets']['EMPEROR SET']['Total Value'])
        + (20 * account.event_points_shop['Bonuses']['Extra Exaltedness']['Owned'])
        # TODO: + Gaming Palette Bonus
        # TODO: + Exotic Market Bonus
        # TODO: + Spelunk Bonus
        + account.legend_talents['Talents']['Wowa Woowa']['Value']
    )

    for stamp_name, stamp in account.stamps.items():
        try:
            account.stamps[stamp_name].total_value = (
                stamp.value
                * (2 if account.labBonuses['Certified Stamp Book']['Enabled'] and stamp.stamp_type != 'Misc' else 1)
                * (ValueToMulti(account.sneaking.pristine_charms['Liqorice Rolle'].value) if stamp.stamp_type != 'Misc' else 1)
                * (account.exalted_stamp_multi if stamp.exalted else 1)
            )
        except:
            account.stamps[stamp_name].total_value = stamp.value
            logger.exception(f"Failed to calculate the Total Value of {stamp_name}")
            continue

def _calculate_w1_owl_bonuses(account):
    # Dependency: _calculate_w7_legend_talents
    bonuses_of_orion_num = len(owl_bonuses_of_orion)
    bonuses_of_orion_owned = account.owl['BonusesOfOrion']
    megafeathers_owned = account.owl['MegaFeathersOwned']
    legend_talent_multi = ValueToMulti(account.legend_talents['Talents']['Furry Friends Forever']['Value'])
    megafeather_mod = 0
    if megafeathers_owned >= 10:
        megafeather_mod = 6 + ((megafeathers_owned - 10) * 0.5)
    elif megafeathers_owned > 7:
        megafeather_mod = 5
    elif megafeathers_owned > 5:
        megafeather_mod = 4
    elif megafeathers_owned > 3:
        megafeather_mod = 3
    elif megafeathers_owned > 1:
        megafeather_mod = 2

    account.owl['Bonuses'] = {}
    for bonus_index, (bonus_name, bonus) in enumerate(owl_bonuses_of_orion.items()):
        bonus_base = bonus['BaseValue']
        if account.owl['Discovered']:
            bonus_num_unlocked = (floor(bonuses_of_orion_owned/bonuses_of_orion_num) + (1 if (bonuses_of_orion_owned % bonuses_of_orion_num) > bonus_index else 0))
        else:
            bonus_num_unlocked = 0
        bonus_value = bonus_base * bonus_num_unlocked * megafeather_mod * legend_talent_multi
        account.owl['Bonuses'][bonus_name] = {
            'BaseValue': bonus_base,
            'NumUnlocked': bonus_num_unlocked,
            'Value': safer_convert(bonus_value, 0)
        }

def _calculate_w1_minigames(account):
    _calculate_w1_basketball(account)
    _calculate_w1_darts(account)

def _calculate_w1_basketball(account):
    for upgrade in account.basketball['Upgrades'].values():
        if '{' in upgrade['Description']:
            upgrade['Value'] = upgrade['Level']
            upgrade['Description'] = upgrade['Description'].replace('{', str(upgrade['Value']))

def _calculate_w1_darts(account):
    for upgrade in account.darts['Upgrades'].values():
        if '{' in upgrade['Description']:
            upgrade['Value'] = upgrade['Level']
            upgrade['Description'] = upgrade['Description'].replace('{', str(upgrade['Value']))
        elif '}' in upgrade['Description']:
            upgrade['Value'] = ValueToMulti(upgrade['Level'])
            upgrade['Description'] = upgrade['Description'].replace('}', str(upgrade['Value']))

def _calculate_w2(account):
    _calculate_w2_vials(account)
    _calculate_w2_sigils(account)
    _calculate_w2_cauldrons(account)
    _calculate_w2_postOffice(account)
    _calculate_w2_ballot(account)
    _calculate_w2_islands_trash(account)
    _calculate_w2_killroy(account)

def _calculate_w2_vials(account):
    account.alchemy_vials_calcs = {
        'mga': (
            account.vault['Upgrades']['Vial Overtune']['Total Value']
            + ((account.maxed_vials * .02) if account.rift['VialMastery'] else 0)
        ),
        'mgb': account.labBonuses['My 1st Chemistry Set']['Value']
    }
    account.alchemy_vials_calcs['Total Multi'] = account.alchemy_vials_calcs['mga'] * account.alchemy_vials_calcs['mgb']
    for vial_name, vial_details in account.alchemy_vials.items():
        try:
            account.alchemy_vials[vial_name]['Value'] = account.alchemy_vials_calcs['Total Multi'] * account.alchemy_vials[vial_name]['BaseValue']
        except:
            logger.warning(f"Could not increase {vial_name} value")

def _calculate_w2_cauldrons(account):
    perCauldronBubblesUnlocked = [
        account.alchemy_cauldrons['OrangeUnlocked'],
        account.alchemy_cauldrons['GreenUnlocked'],
        account.alchemy_cauldrons['PurpleUnlocked'],
        account.alchemy_cauldrons['YellowUnlocked']
    ]
    bubbleUnlockListByWorld = [20, 0, 0, 0, 0, 0, 0, 0, 0]
    for bubbleColorCount in perCauldronBubblesUnlocked:
        worldCounter = 1
        while bubbleColorCount >= 5 and worldCounter <= len(bubbleUnlockListByWorld) - 1:
            bubbleUnlockListByWorld[worldCounter] += 5
            bubbleColorCount -= 5
            worldCounter += 1
        if bubbleColorCount > 0 and worldCounter <= len(bubbleUnlockListByWorld) - 1:
            bubbleUnlockListByWorld[worldCounter] += bubbleColorCount
    account.alchemy_cauldrons['BubblesPerWorld'] = bubbleUnlockListByWorld

    account.alchemy_cauldrons['NextWorldMissingBubbles'] = min(
        [cauldronValue // 5 for cauldronValue in perCauldronBubblesUnlocked],
        default=0
    ) + 1

def _calculate_w2_sigils(account):
    for sigilName in account.alchemy_p2w["Sigils"]:
        if account.alchemy_p2w["Sigils"][sigilName]["Level"] == 2:
            if account.sneaking.emporium['Ionized Sigils'].obtained:
                # If you have purchased Ionized Sigils, the numbers needed to Gold get subtracted from your hours already
                red_Hours = account.alchemy_p2w["Sigils"][sigilName]["Requirements"][2]
            else:
                # To precharge Red sigils before buying the upgreade, you need Gold + Red hours
                red_Hours = account.alchemy_p2w["Sigils"][sigilName]["Requirements"][1] + account.alchemy_p2w["Sigils"][sigilName]["Requirements"][2]
            if account.alchemy_p2w["Sigils"][sigilName]["PlayerHours"] >= red_Hours:
                account.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = 3
            else:
                account.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = account.alchemy_p2w["Sigils"][sigilName]["Level"]
        elif account.alchemy_p2w["Sigils"][sigilName]["Level"] == 3:
            account.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = 3
        else:
            account.alchemy_p2w["Sigils"][sigilName]["PrechargeLevel"] = account.alchemy_p2w["Sigils"][sigilName]["Level"]
        # Before the +1, -1 would mean not unlocked, 0 would mean Blue tier, 1 would be Yellow tier, and 2 would mean Red tier
        # After the +1, 0/1/2/3

def _calculate_w2_postOffice(account):
    account.postOffice['Total Boxes Earned'] = (
        account.postOffice['Completing Orders']
        + account.postOffice['Streak Bonuses']
        + account.postOffice['Miscellaneous']
        + account.postOffice['Upgrade Vault']
    )

def _calculate_w2_ballot(account):
    # Dependency: _calculate_w7_legend_talents
    # "VotingBonuszMulti" in source. Last update v2.48 Giftmas Event (December 8, 2025)
    account.ballot['BonusMulti'] = ValueToMulti(
        account.equinox_bonuses['Voter Rights']['CurrentLevel']
        + account.caverns['Majiks']['Voter Integrity']['Value']
        + account.summoning['Endless Bonuses']['+{% Ballot Bonus']
        + (17 * account.event_points_shop['Bonuses']['Gilded Vote Button']['Owned'])
        + (13 * account.event_points_shop['Bonuses']['Royal Vote Button']['Owned'])
        + (5 * has_companion('Mashed Potato'))
        + (40 * has_companion('Crystal Cuttlefish'))
        + account.legend_talents['Talents']['Democracy FTW']['Value']
    )
    for buffIndex, buffValuesDict in account.ballot['Buffs'].items():
        account.ballot['Buffs'][buffIndex]['Value'] *= account.ballot['BonusMulti']
        # Check for + or +x% replacements
        if "{" in buffValuesDict['Description']:
            account.ballot['Buffs'][buffIndex]['Description'] = buffValuesDict['Description'].replace("{", f"{account.ballot['Buffs'][buffIndex]['Value']:.3f}")
        # Check for multi replacements
        if "}" in buffValuesDict['Description']:
            account.ballot['Buffs'][buffIndex]['Description'] = buffValuesDict['Description'].replace("}", f"{ValueToMulti(account.ballot['Buffs'][buffIndex]['Value']):.3f}")

def _calculate_w2_islands_trash(account):
    for item in islands_trash_shop_costs:
        account.islands['Trash Island'][item] = {'Cost': islands_trash_shop_costs[item]}
    #Onetime purchases
    account.islands['Trash Island']['Skelefish Stamp']['Unlocked'] = account.stamps['Skelefish Stamp'].delivered or account.stored_assets.get('StampB47').amount > 0
    account.islands['Trash Island']['Amplestample Stamp']['Unlocked'] = account.stamps['Amplestample Stamp'].delivered or account.stored_assets.get('StampB32').amount > 0
    account.islands['Trash Island']['Golden Sixes Stamp']['Unlocked'] = account.stamps['Golden Sixes Stamp'].delivered or account.stored_assets.get('StampA38').amount > 0
    account.islands['Trash Island']['Stat Wallstreet Stamp']['Unlocked'] = account.stamps['Stat Wallstreet Stamp'].delivered or account.stored_assets.get('StampA39').amount > 0
    account.islands['Trash Island']['Unlock New Bribe Set']['Unlocked'] = account.bribes['Trash Island']['Random Garbage'] >= 0

    #Repeated purchases
    account.islands['Trash Island']['Garbage Purchases'] = safer_get(account.raw_optlacc_dict, 163, 0)
    account.islands['Trash Island']['Bottle Purchases'] = safer_get(account.raw_optlacc_dict, 164, 0)

def _calculate_w2_killroy(account):
    for upgradeName, upgradeDict in killroy_dict.items():
        if not account.killroy[upgradeName]['Available']:
            account.killroy[upgradeName]['Available'] = (
                safer_get(account.raw_optlacc_dict, 112, 0) >= upgradeDict['Required Fights']
                or account.killroy[upgradeName]['Upgrades'] > 0
            ) and account.equinox_bonuses['Shades of K']['CurrentLevel'] >= upgradeDict['Required Equinox']


def _calculate_w3(account):
    _calculate_w3_building_max_levels(account)
    _calculate_w3_collider_atoms(account)
    _calculate_w3_collider_base_costs(account)
    _calculate_w3_collider_cost_reduction(account)
    _calculate_w3_shrine_values(account)
    _calculate_w3_shrine_advices(account)

def _update_w3_building_max_levels(account, building_name: str, levels: int, note=''):
    if building_name == 'All Towers':
        for tower_name in buildings_towers:
            try:
                account.construction_buildings[tower_name]['MaxLevel'] += levels
            except:
                logger.warning(f"Could not increase max level of {tower_name}: {note if note else 'No note provided'}")
    elif building_name == 'All Shrines':
        for shrine_name in buildings_shrines:
            try:
                account.construction_buildings[shrine_name]['MaxLevel'] += levels
            except:
                logger.warning(f"Could not increase max level of {shrine_name}: {note if note else 'No note provided'}")
    else:
        try:
            account.construction_buildings[building_name]['MaxLevel'] += levels
        except:
            logger.warning(f"Could not increase max level of {building_name}: {note if note else 'No note provided'}")

def _calculate_w3_building_max_levels(account):
    if account.rift['SkillMastery']:
        totalLevel = sum(account.all_skills['Construction'])
        if totalLevel >= 500:
            _update_w3_building_max_levels(account, 'Trapper Drone', 35, '500 Construction Mastery')

        if totalLevel >= 1000:
            _update_w3_building_max_levels(account, 'Talent Book Library', 35, '1K Construction Mastery')

        if totalLevel >= 1500:
            _update_w3_building_max_levels(account, 'All Shrines', 30, '1.5K Construction Mastery')

        if totalLevel >= 2500:
            _update_w3_building_max_levels(account, 'All Towers', 30, '2.5K Construction Mastery')

    if account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'] > 0:
        _update_w3_building_max_levels(account, 'All Towers', 2 * account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'], 'Atom Collider - Carbon - Wizard Maximizer')

    #+100 levels from Gambit occurs in _calculate_caverns_gambit

def _calculate_w3_collider_atoms(account):
    for atom_name, atom_values in account.atom_collider['Atoms'].items():
        try:
            account.atom_collider['Atoms'][atom_name]['Value'] = (
                atom_values['Level'] * atom_values['Value per Level']
            )
            if '{' in atom_values['Description']:
                account.atom_collider['Atoms'][atom_name]['Description'] = atom_values['Description'].replace(
                    '{', f"{account.atom_collider['Atoms'][atom_name]['Value']}"
                )
            if '}' in atom_values['Description']:
                account.atom_collider['Atoms'][atom_name]['Description'] = atom_values['Description'].replace(
                    '}', f"{ValueToMulti(account.atom_collider['Atoms'][atom_name]['Value']):.3f}"
                )
        except:
            logger.exception(f"Failed to calculate Value and Description for {atom_name}")
            account.atom_collider['Atoms'][atom_name]['Value'] = 0

def _calculate_w3_collider_base_costs(account):
    #Formula for base cost: (AtomInfo[3] + AtomInfo[1] * AtomCurrentLevel) * POWER(AtomInfo[2], AtomCurrentLevel)
    for atomName, atomValuesDict in account.atom_collider['Atoms'].items():
        #Update max level +10 if Isotope Discovery unlocked
        if account.gaming['SuperBits']['Isotope Discovery']['Unlocked']:
            account.atom_collider['Atoms'][atomName]['MaxLevel'] += 10

        #Update max level if Wind Walker Compass > Atomic Potential is leveled
        if account.compass['Upgrades']['Atomic Potential']['Level'] > 0:
            account.atom_collider['Atoms'][atomName]['MaxLevel'] += account.compass['Upgrades']['Atomic Potential']['Total Value']

        #Update max level if Higgs Boson Event Shop bought
        if account.event_points_shop['Bonuses']['Higgs Boson']['Owned']:
            account.atom_collider['Atoms'][atomName]['MaxLevel'] += 20

        #If atom isn't already at max level:
        if atomValuesDict['Level'] < atomValuesDict['MaxLevel']:
            # Calculate base cost to upgrade to next level
            account.atom_collider['Atoms'][atomName]['BaseCostToUpgrade'] = (
                (atomValuesDict['AtomInfo3']
                    + (atomValuesDict['AtomInfo1'] * atomValuesDict['Level']))
                * safer_math_pow(atomValuesDict['AtomInfo2'], atomValuesDict['Level'])
            )
            # Calculate base cost to max level
            for level in range(account.atom_collider['Atoms'][atomName]['Level'], account.atom_collider['Atoms'][atomName]['MaxLevel']):
                account.atom_collider['Atoms'][atomName]['BaseCostToMax'] += (
                    (account.atom_collider['Atoms'][atomName]['AtomInfo3']
                        + (account.atom_collider['Atoms'][atomName]['AtomInfo1'] * level))
                    * safer_math_pow(account.atom_collider['Atoms'][atomName]['AtomInfo2'], level)
                )

def _calculate_w3_collider_cost_reduction(account):
    # Max was removed after DB and WW both introduced near-infinite scaling sources
    account.atom_collider['CostReductionRaw'] = ValueToMulti(
        7 * account.merits[4][6]['Level']
        + (account.construction_buildings['Atom Collider']['Level'] / 10)
        + 1 * account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']
        + 10 * account.gaming['SuperBits']['Atom Redux']['Unlocked']
        + account.alchemy_bubbles['Atom Split']['BaseValue']
        + account.stamps['Atomic Stamp'].total_value
        + account.grimoire['Upgrades']['Death of the Atom Price']['Total Value']
        + account.compass['Upgrades']['Atomic Cost Crash']['Total Value']
    )
    account.atom_collider['CostReductionMulti'] = 1 / account.atom_collider['CostReductionRaw']
    account.atom_collider['CostDiscount'] = (1 - (1 / account.atom_collider['CostReductionRaw'])) * 100

    for atomName, atomValuesDict in account.atom_collider['Atoms'].items():
        # Calculate base cost to upgrade to next level, if not max level
        if atomValuesDict['Level'] < atomValuesDict['MaxLevel']:
            account.atom_collider['Atoms'][atomName]['DiscountedCostToUpgrade'] = (
                account.atom_collider['Atoms'][atomName]['BaseCostToUpgrade']
                * account.atom_collider['CostReductionMulti']
            )
            account.atom_collider['Atoms'][atomName]['DiscountedCostToMax'] = (
                account.atom_collider['Atoms'][atomName]['BaseCostToMax']
                * account.atom_collider['CostReductionMulti']
            )

def _calculate_w3_shrine_values(account):
    cchizoar_multi = ValueToMulti(5 * (1 + next(c.getStars() for c in account.cards if c.name == 'Chaotic Chizoar')))
    for shrine in account.shrines:
        account.shrines[shrine]['Value'] *= cchizoar_multi

def _calculate_w3_shrine_advices(account):
    account.shrine_advices = {}
    for shrine_name in account.shrines:
        account.shrine_advices[shrine_name] = Advice(
            label=f"Level {account.shrines[shrine_name]['Level']} {shrine_name}:"
                  f" +{account.shrines[shrine_name]['Value']:.0f}%"
                  f"<br>{arbitrary_shrine_note}",
            picture_class=account.shrines[shrine_name]['Image'],
            progression=account.shrines[shrine_name]['Level'],
            goal=arbitrary_shrine_goal
        )
    cchizoar_multi = 1 + (5 * (1 + next(c.getStars() for c in account.cards if c.name == 'Chaotic Chizoar')) / 100)
    account.shrine_advices['Chaotic Chizoar Card'] = Advice(
        label=f"Chaotic Chizoar card to increase Shrine ({cchizoar_multi}x multi already included)",
        picture_class="chaotic-chizoar-card",
        progression=1 + next(c.getStars() for c in account.cards if c.name == "Chaotic Chizoar"),
        goal=6
    )


def _calculate_w4(account):
    _calculate_w4_cooking_max_plate_levels(account)
    _calculate_w4_jewel_multi(account)
    _calculate_w4_meal_multi(account)
    _calculate_w4_lab_bonuses(account)
    _calculate_w4_tome_bonuses(account)

def _calculate_w4_cooking_max_plate_levels(account):
    # Sailing Artifact Increases
    causticolumn_level = account.sailing['Artifacts'].get('Causticolumn', {}).get('Level', 0)
    account.cooking['PlayerMaxPlateLvl'] += 10 * int(causticolumn_level)
    if causticolumn_level < 1:
        account.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Base Causticolumn", "causticolumn", 0, 1))
    if causticolumn_level < 2:
        account.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Ancient Causticolumn", "causticolumn", 0, 1))
    if causticolumn_level < 3:
        if account.rift['EldritchArtifacts']:
            account.cooking['PlayerMissingPlateUpgrades'].append(("{{ Artifact|#sailing }}: Eldritch Causticolumn", "causticolumn", 0, 1))
        else:
            account.cooking['PlayerMissingPlateUpgrades'].append((
                "{{ Artifact|#sailing }}: Eldritch Causticolumn. Eldritch Artifacts are unlocked by completing {{ Rift|#rift }} 30",
                "eldritch-artifact",
                0,
                1
            ))
    if causticolumn_level < 4:
        if account.sneaking.emporium["Sovereign Artifacts"].obtained:
            account.cooking['PlayerMissingPlateUpgrades'].append((
                "{{ Artifact|#sailing }}: Sovereign Causticolumn",
                "causticolumn",
                0,
                1
            ))
        else:
            account.cooking['PlayerMissingPlateUpgrades'].append((
                "{{ Artifact|#sailing }}: Sovereign Causticolumn. Sovereign Artifacts unlock from {{ Jade Emporium|#sneaking }}",
                "sovereign-artifacts",
                0,
                1
            ))
    # Jade Emporium Increases
    if account.sneaking.emporium["Papa Blob's Quality Guarantee"].obtained:
        account.cooking['PlayerMaxPlateLvl'] += 10
    else:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Purchase \"Papa Blob's Quality Guarantee\" from {{ Jade Emporium|#sneaking }}",
            "papa-blobs-quality-guarantee",
            0,
            1
        ))
    if account.sneaking.emporium["Chef Geustloaf's Cutting Edge Philosophy"].obtained:
        account.cooking['PlayerMaxPlateLvl'] += 10
    else:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Purchase \"Chef Geustloaf's Cutting Edge Philosophy\" from {{ Jade Emporium|#sneaking }}",
            "chef-geustloafs-cutting-edge-philosophy",
            0,
            1
        ))
    # Grimoire Increases
    account.cooking['PlayerMaxPlateLvl'] += account.grimoire['Upgrades']['Supreme Head Chef Status']['Level']
    if account.grimoire['Upgrades']['Supreme Head Chef Status']['Level'] < account.grimoire['Upgrades']['Supreme Head Chef Status']['Max Level']:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Upgrade \"Supreme Head Chef Status\" within {{ The Grimoire|#the-grimoire }}",
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Image'],
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Level'],  #progress
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Max Level']  #goal
        ))
    # Spelunking Increases
    if account.spelunk['Cave Bonuses'][5]['Owned']:
        account.cooking['PlayerMaxPlateLvl'] += 30
    else:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Defeat the Boss of the Lunarheim Cave in {{Spelunking|#spelunking}}",
            account.spelunk['Cave Bonuses'][5]['Image'],
            0,
            1
        ))

    account.cooking['CurrentRemainingMeals'] = account.cooking['MaxTotalMealLevels'] - account.cooking['PlayerTotalMealLevels']
    account.cooking['MaxRemainingMeals'] = (max_meal_count * max_meal_level) - account.cooking['PlayerTotalMealLevels']
    account.cooking['NMLBDays'] = sum([
        ceil((max_meal_level - meal_details['Level']) / 3) for meal_details in account.meals.values()
    ])

def _calculate_w4_jewel_multi(account):
    jewelMulti = 1
    if account.labBonuses["Spelunker Obol"]["Enabled"]:
        jewelMulti = account.labBonuses["Spelunker Obol"]["Value"]
        if account.labJewels["Pure Opal Navette"]["Enabled"]:  # Nested since jewel does nothing without spelunker
            account.labBonuses["Spelunker Obol"]["Value"] += account.labJewels["Pure Opal Navette"]["BaseValue"] / 100
            jewelMulti += account.labJewels["Pure Opal Navette"]["BaseValue"] / 100  # The displayed value does nothing since the effect is used before spelunker obol is accounted for
    for jewel in account.labJewels:
        account.labJewels[jewel]["Value"] *= jewelMulti if jewel != 'Pure Opal Navette' else 1

def _calculate_w4_meal_multi(account):
    meal_multi = (
        ValueToMulti(
            (account.labJewels['Black Diamond Rhinestone']['Value'] * account.labJewels['Black Diamond Rhinestone']['Enabled'])
            + account.breeding['Total Shiny Levels']['Bonuses from All Meals']
        )
        * account.summoning['Endless Bonuses']['<x Meal Bonuses']
    )

    ribbon_multi_table = []
    # Last verified as of v2.37 Emperor
    # _customBlock_Summoning > "RibbonBonus"
    # 1 + (Math.floor(5 * t + Math.floor(t / 2) * (4 + 6.5 * Math.floor(t / 5))) + Math.floor(t / 4) * (n._customBlock_GetSetBonus("EMPEROR_SET", "Bonus", 0, 0) / 4)) / 100;
    for tier in range(0, max_cooking_ribbon + 1):
        ribbon_multi_table.append(ValueToMulti(
            floor(
                (5 * tier)
                + (floor(tier / 2) * (4 + 6.5 * floor(tier / 5)))
            )
            + (floor(tier / 4) * (MultiToValue(account.armor_sets['Sets']['EMPEROR SET']['Total Value']) / 4))
        ))

    for meal in account.meals:
        account.meals[meal]['RibbonMulti'] = ribbon_multi_table[min(len(ribbon_multi_table) - 1, account.meals[meal]['RibbonTier'])]
        account.meals[meal]['Value'] = float(account.meals[meal]['Value']) * meal_multi * account.meals[meal]['RibbonMulti']
        if '{' in account.meals[meal]['Effect']:
            account.meals[meal]['Description'] = account.meals[meal]['Effect'].replace('{', f"{account.meals[meal]['Value']:,.3f}")
        elif '}' in account.meals[meal]['Effect']:
            account.meals[meal]['Description'] = account.meals[meal]['Effect'].replace('}', f"{account.meals[meal]['Value']:,.3f}")
        else:
            account.meals[meal]['Description'] = account.meals[meal]['Effect']

def _calculate_w4_lab_bonuses(account):
    account.labBonuses['No Bubble Left Behind']['Value'] = 3

    account.labBonuses['No Bubble Left Behind']['Value'] += 1 * account.labJewels['Pyrite Rhinestone']['Enabled']  #Up to +1
    account.labBonuses['No Bubble Left Behind']['Value'] += 1 * account.sailing['Artifacts']['Amberite']['Level']  #Up to +4 as of 2.11
    account.labBonuses['No Bubble Left Behind']['Value'] += 1 * account.gaming['SuperBits']['Moar Bubbles']['Unlocked']  #20% chance at +1
    account.labBonuses['No Bubble Left Behind']['Value'] += 1 * account.gaming['SuperBits']['Even Moar Bubbles']['Unlocked']  #30% chance at +1
    account.labBonuses['No Bubble Left Behind']['Value'] += 1 * account.merits[3][6]['Level']  #Up to 3
    #Grand total: 3 + 1 + 4 + 1 + 1 + 3 = 13 possible. 11 guaranteed, 2 are chances

    #Reduce this down to 0 if the lab bonus isn't enabled
    account.labBonuses['No Bubble Left Behind']['Value'] *= account.labBonuses['No Bubble Left Behind']['Enabled']
    #Now for the bullshit: Lava has a hidden cap of 10 bubbles
    account.labBonuses['No Bubble Left Behind']['Value'] = min(max_nblb_bubbles, account.labBonuses['No Bubble Left Behind']['Value'])

def _calculate_w4_tome_bonuses(account):
    tome_bonus_multi = ValueToMulti(
        account.grimoire['Upgrades']['Grey Tome Book']['Level']
        + MultiToValue(account.armor_sets['Sets']['TROLL SET']['Total Value'])
    )
    # DMG

    # Skill Efficiency

    # Drop Rarity
    account.tome['Bonuses']['Drop Rarity']['Value'] = (
        account.tome['Red Pages Unlocked']  #Sets the whole value to 0 if player hasn't turned in Red Pages yet
        * 2
        * safer_math_pow(
            floor(
                max(0, account.tome['Total Points'] - 8000)
                / 100
            ),
            0.7
        )
    )
    for bonus_name, bonus_details in account.tome['Bonuses'].items():
        account.tome['Bonuses'][bonus_name]['Total Value'] = (
            bonus_details.get('Value', 0)
            * tome_bonus_multi
        )
    # logger.debug(f"{account.tome['Total Points']} Tome points = +{account.tome['Bonuses']['Drop Rarity']['Value']}% Drop Rate")


def _calculate_w5(account):
    account.divinity['AccountWideArctis'] = has_companion('King Doot') or 'Arctis' in account.caverns['PocketDivinityLinks']
    _calculate_w5_divinity_offering_costs(account)

def _calculate_w5_divinity_offering_costs(account):
    DivCostAfter3 = safer_get(account.raw_serverVars_dict, "DivCostAfter3", divinity_DivCostAfter3)
    account.divinity['LowOfferingGoal'] = divinityUpgradeCost(DivCostAfter3, account.divinity['LowOffering'], account.divinity['GodsUnlocked'] + account.divinity['GodRank'])
    account.divinity['HighOfferingGoal'] = divinityUpgradeCost(DivCostAfter3, account.divinity['HighOffering'], account.divinity['GodsUnlocked'] + account.divinity['GodRank'])

def divinityUpgradeCost(DivCostAfter3, offeringIndex, unlockedDivinity):
    try:
        cost = (20 * safer_math_pow(unlockedDivinity + 1.3, 2.3) * safer_math_pow(2.2, unlockedDivinity) + 60) * divinity_offerings_dict.get(offeringIndex, {}).get("Chance", 1) / 100
        if unlockedDivinity >= 3:
            cost = cost * safer_math_pow(min(1.8, max(1, 1 + DivCostAfter3 / 100)), unlockedDivinity - 2)
        return ceil(cost)
    except OverflowError:
        logger.exception(f"Could not calc Divinity Offering cost. Probably a cheater with a ridiculous number of Unlocked Divinity: {unlockedDivinity}. Returning {default_huge_number_replacement}")
        return default_huge_number_replacement


def _calculate_caverns(account):
    #_calculate_caverns_majiks(account)
    _calculate_caverns_measurements_base(account)
    _calculate_caverns_measurements_multis(account)
    _calculate_caverns_studies(account)
    _calculate_caverns_jar_collectibles(account)
    _calculate_caverns_the_well(account)
    _calculate_caverns_monuments(account)
    _calculate_caverns_motherlode_layers(account)
    _calculate_caverns_the_bell(account)
    _calculate_caverns_the_harp(account)
    _calculate_caverns_gambit(account)

def _calculate_caverns_measurements_base(account):
    # _customBlock_Holes > "MeasurementBaseBonus"  #Last verified as of 2.30 Companion Trading
    for measurement_index, measurement_values in account.caverns['Measurements'].items():
        try:
            if measurement_values['TOT']:
                account.caverns['Measurements'][measurement_index]['BaseValue'] = (
                    measurement_values['HI55']
                    * (measurement_values['Level'] / (100 + measurement_values['Level']))
                )
            else:
                account.caverns['Measurements'][measurement_index]['BaseValue'] = measurement_values['HI55'] * measurement_values['Level']
            account.caverns['Measurements'][measurement_index]['TotalBaseValue'] = (
                account.caverns['Measurements'][measurement_index]['BaseValue']
                * account.caverns['Majiks']['Lengthmeister']['Value']
            )
            account.caverns['Measurements'][measurement_index]['Value'] = account.caverns['Measurements'][measurement_index]['TotalBaseValue']
        except:
            logger.exception(f"Failed to calculate Measurement Base Value for {measurement_values['Description']}")
            account.caverns['Measurements'][measurement_index]['BaseValue'] = 0
            account.caverns['Measurements'][measurement_index]['TotalBaseValue'] = 0
            account.caverns['Measurements'][measurement_index]['Value'] = 0

def _calculate_caverns_measurements_multis(account):
    # Part 1: Retrieve the base value and prep into the version used for calculation, if any
    # _customBlock_Holes > "MeasurementQTYfound"  #Last verified as of 2.32 Gambit
    raw_holes = safe_loads(account.raw_data.get('Holes', []))
    account.caverns['MeasurementMultis'] = {}
    for entry_index, entry_string in enumerate(caverns_measurer_scalars):
        clean_entry_name = str(entry_string).replace('_', ' ').title()
        # I want to use a match/case here, but PyCharm doesn't let me collapse those blocks which is just annoying lmao
        if entry_index == 0:  #Gloomie Kills
            try:
                raw_gloomie_kills = safer_convert(raw_holes[11][28], 0.00) if raw_holes else 0
            except:
                raw_gloomie_kills = 0
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': raw_gloomie_kills,
                'PrettyRaw': notateNumber('Match', raw_gloomie_kills, 2, 'M'),
                'Prepped': safer_math_log(raw_gloomie_kills, 'Lava')  #In the source code, this is when 99 = i
            }
        elif entry_index == 1:  #Crops Found
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': account.farming.crops.unlocked,
                'PrettyRaw': f"{account.farming.crops.unlocked:,}",
                'Prepped': account.farming.crops.unlocked / 14  # In the source code, this is when 99 = i
            }
        elif entry_index == 2:  #Account Lv
            sum_combat_levels = sum(account.all_skills['Combat']) or 0
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': sum_combat_levels,
                'PrettyRaw': f"{sum_combat_levels:,}",
                'Prepped': sum_combat_levels / 500  # In the source code, this is when 99 = i
            }
        elif entry_index == 3:  #Tome Score
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': account.tome['Total Points'],
                'PrettyRaw': f"{account.tome['Total Points']:,}",
                'Prepped': account.tome['Total Points'] / 2500  # In the source code, this is when 99 = i
            }
        elif entry_index == 4:  #All Skill Lv
            total_skill_levels = 0
            for skill, skill_levels in account.all_skills.items():
                total_skill_levels += sum(skill_levels) if skill != 'Combat' else 0
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': total_skill_levels,
                'PrettyRaw': f"{total_skill_levels:,}",
                'Prepped': total_skill_levels / 5000 + max(0.0, (total_skill_levels - 18000) / 1500),  # In the source code, this is when 99 = i
            }
        # elif entry_index == 5:  #Unimplemented as of 2.32 Gambit, just returns 0. Default case can handle it.
        #     pass
        elif entry_index == 6:  #Deathnote Pts
            raw_pts = sum([account.enemy_worlds[world].total_mk for world in account.enemy_worlds]) + account.miniboss_deathnote['TotalMK']
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': raw_pts,
                'PrettyRaw': f"{raw_pts:,}",
                'Prepped': raw_pts / 125,  # In the source code, this is when 99 = i
            }
        elif entry_index == 7:  #Highest Dmg
            raw_tasks = safe_loads(account.raw_data.get('TaskZZ0', []))
            try:
                raw_damage = raw_tasks[1][0]
                raw_damage = float(raw_damage)
            except ValueError:
                logger.exception(f"Failed to cast Highest Damage of {raw_tasks[1][0]} from W2 Task. Defaulting to e20 idk")
                raw_damage = 1e20
            except IndexError:
                logger.exception(f"JSON doesn't contain TaskZZ0[1][0] to retrieve Highest Damage from W2 Tasks. Defaulting to 1")
                raw_damage = 1
            except:
                logger.exception(f"JSON has bad value for TaskZZ0[1][0] to retrieve Highest Damage from W2 Tasks. Defaulting to 1")
                raw_damage = 1
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': raw_damage,
                'PrettyRaw': notateNumber('Basic', raw_damage, 3),
                'Prepped': safer_math_log(raw_damage, 'Lava') / 2,  # In the source code, this is when 99 = i
            }
        elif entry_index == 8:  #Slab Items
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': len(account.registered_slab),
                'PrettyRaw': f"{len(account.registered_slab):,}",
                'Prepped': len(account.registered_slab) / 150,  # In the source code, this is when 99 = i
            }
        elif entry_index == 9:  #Studies Done
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': account.caverns['TotalStudies'],
                'PrettyRaw': f"{account.caverns['TotalStudies']:,}",
                'Prepped': account.caverns['TotalStudies'] / 6,  # In the source code, this is when 99 = i
            }
        elif entry_index == 10:  #Golem Kills
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': account.caverns['Caverns']['The Temple']['Golems Killed'],
                'PrettyRaw': f"{notateNumber('Match', account.caverns['Caverns']['The Temple']['Golems Killed'], 2, 'M')}",
                'Prepped': max(0, safer_math_log(account.caverns['Caverns']['The Temple']['Golems Killed'], 'Lava') - 2),  # In the source code, this is when 99 = i
            }
        else:
            #logger.exception(f"Unknown MeasurementMulti type: {clean_entry_name}")
            account.caverns['MeasurementMultis'][clean_entry_name] = {
                'Raw': 0,
                'PrettyRaw': 'IDK Sorry',
                'Prepped': 0,  # In the source code, this is when 99 = i
            }

        # Part 2: Calculate the Multi using one of two formulas depending on the Prepped value
        try:
            if 5 > account.caverns['MeasurementMultis'][clean_entry_name]['Prepped']:
                account.caverns['MeasurementMultis'][clean_entry_name]['Multi'] = ValueToMulti(
                    18 * account.caverns['MeasurementMultis'][clean_entry_name]['Prepped']
                )
            else:
                account.caverns['MeasurementMultis'][clean_entry_name]['Multi'] = ValueToMulti(
                    18 * account.caverns['MeasurementMultis'][clean_entry_name]['Prepped']
                    + 8 * (account.caverns['MeasurementMultis'][clean_entry_name]['Prepped'] - 5)
                )
        except:
            logger.exception(f"Failed to calculate {clean_entry_name}'s MeasurementMulti. Setting to 1.")
            account.caverns['MeasurementMultis'][clean_entry_name]['Multi'] = 1
        # logger.debug(f"{clean_entry_name} = {account.caverns['MeasurementMultis'][clean_entry_name]}")

    # Part 3: Apply the multis to the measurements
    for measurement_index, measurement_details in account.caverns['Measurements'].items():
        try:
            account.caverns['Measurements'][measurement_index]['Value'] *= account.caverns['MeasurementMultis'][measurement_details['ScalesWith']]['Multi']
        except:
            logger.warning(f"Couldn't apply {measurement_details['ScalesWith']} multi to Index{measurement_index}")

def _calculate_caverns_studies(account):
    for study_index, study_details in account.caverns['Studies'].items():
        match study_index:
            case 3:
                value_cap = 32
                base_value = 12
                total_value = min(value_cap, base_value + (study_details['Level'] * study_details['ScalingValue']))
                max_level = ceil((value_cap - base_value) / study_details['ScalingValue'])
                base_note = f"<br>12 base +{study_details['ScalingValue']} per level, capped at {value_cap}%"
            case 9:
                base_value = 50
                total_value = base_value + (study_details['Level'] * study_details['ScalingValue'])
                max_level = EmojiType.INFINITY.value
                base_note = f"<br>{base_value} base +{study_details['ScalingValue']} per level"
            case _:
                total_value = study_details['Level'] * study_details['ScalingValue']
                max_level = EmojiType.INFINITY.value
                if '}' in study_details['Description']:
                    base_note = f"<br>No base, +{ValueToMulti(study_details['ScalingValue']) - 1:.2f} per level"
                else:
                    base_note = f"<br>No base, +{study_details['ScalingValue']} per level"

        account.caverns['Studies'][study_index]['Value'] = total_value
        account.caverns['Studies'][study_index]['MaxLevel'] = max_level
        try:
            if '{' in study_details['Description']:
                account.caverns['Studies'][study_index]['Description'] = study_details['Description'].replace(
                    '{', f"{account.caverns['Studies'][study_index]['Value']}"
                )
            elif '}' in study_details['Description']:
                account.caverns['Studies'][study_index]['Description'] = study_details['Description'].replace(
                    '}', f"{ValueToMulti(account.caverns['Studies'][study_index]['Value'])}"
                )
            account.caverns['Studies'][study_index]['Description'] += base_note
        except:
            logger.exception(f"Unable to update Cavern Study {study_index}'s description: {account.caverns['Studies'][study_index]['Description']}")

def _calculate_caverns_the_well(account):
    account.caverns['Caverns']['The Well']['BucketsUnlocked'] = 1 + sum(
        [
            1 for schematic_name in schematics_unlocking_buckets if account.caverns['Schematics'][schematic_name]['Purchased']
        ]
    )
    account.caverns['Caverns']['The Well']['Buckets'] = safe_loads(account.raw_data.get('Holes', {}))

def _calculate_caverns_monuments(account):
    cosmos_value = (account.caverns['Majiks']['Monumental Vibes']['Value'] - 1) * 100
    for monument_index, monument_name in enumerate(monument_names):
        if monument_index < released_monuments:
            # The 9th bonus multiplies other bonuses, but not itself. Must be calculated first.
            ninth = account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]
            ninth_value = (
                0.1 * ceil(
                    (ninth['Level'] / (250 + ninth['Level']))
                    * 10
                    * ninth['ScalingValue']
                )
            )
            try:
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value'] = ValueToMulti(ninth_value)
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['BaseValue'] = ninth_value
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'] = (
                    account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'].replace(
                        '}', f"{account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value']:,.3f}")
                )
            except:
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Value'] = 1
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['BaseValue'] = 0
                account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'] = (
                    account.caverns['Caverns'][monument_name]['Bonuses'][9 + (10 * monument_index)]['Description'].replace('}', '1')
                )
            for bonus_index, bonus_details in monument_bonuses[monument_name].items():
                if bonus_index % 10 != 9:
                    if bonus_details['ScalingValue'] < 30:
                        base_result = (
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']
                            * account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['ScalingValue']
                        )
                        final_result = base_result * ValueToMulti(cosmos_value + ninth_value)
                    else:
                        base_result = (
                            0.1 * ceil(
                                (account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']
                                 / (250 + account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']))
                                * 10
                                * account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['ScalingValue']
                            )
                        )
                        final_result = (
                            0.1 * ceil(
                                (account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']
                                 / (250 + account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']))
                                * 10
                                * account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['ScalingValue']
                                * ValueToMulti(cosmos_value + ninth_value)
                            )
                        )
                    if bonus_details['ValueType'] == 'Percent':
                        try:
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = final_result
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['BaseValue'] = base_result
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace(
                                    '{', f"{account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value']:,.2f}")
                            )
                        except:
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = 0
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['BaseValue'] = 0
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace('{', '0')
                            )
                    elif bonus_details['ValueType'] == 'Multi':
                        try:
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = ValueToMulti(final_result)
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['BaseValue'] = base_result
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace(
                                    '}', f"{account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value']:,.3f}")
                            )
                        except:
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Value'] = 1
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['BaseValue'] = 0
                            account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'] = (
                                account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description'].replace('}', '1')
                            )
                # logger.debug(f"{monument_name} Bonus {bonus_index}: "
                #              f"Level {account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Level']} = "
                #              f"{account.caverns['Caverns'][monument_name]['Bonuses'][bonus_index]['Description']}")
    _calculate_caverns_monuments_bravery(account)
    _calculate_caverns_monuments_justice(account)

def _calculate_caverns_motherlode_layers(account):
    collectible_bonus = account.caverns['Collectibles']['Amethyst Heartstone']['Value']
    account.caverns['MotherlodeResourceDiscount'] = ValueToMulti(
        collectible_bonus
        + (account.caverns['Studies'][1]['Value'] * account.caverns['Caverns']['Motherlode']['LayersDestroyed'])
        + (account.caverns['Studies'][7]['Value'] * account.caverns['Caverns']['The Hive']['LayersDestroyed'])
        + (account.caverns['Studies'][11]['Value'] * account.caverns['Caverns']['Evertree']['LayersDestroyed'])
        # Trench not implemented as of v2.31
        # + (account.caverns['Studies'][]['Value'] * account.caverns['Caverns']['The Trench']['LayersDestroyed'])
    )
    account.caverns['MotherlodeResourceDiscountAdvice'] = Advice(
        label=f"Resource Divisor from Amethyst Heartstone Collectible + Bolaia Studies: {account.caverns['MotherlodeResourceDiscount']:.3f}",
        picture_class='bolaia'
    )

    for cavern_name in ['Motherlode', 'The Hive', 'Evertree']:
        base_requirement = ceil(200 * safer_math_pow(2.2, 1 + account.caverns['Caverns'][cavern_name]['LayersDestroyed']))
        account.caverns['Caverns'][cavern_name]['ResourcesRemaining'] = base_requirement / max(1, account.caverns['MotherlodeResourceDiscount'])

def _calculate_caverns_monuments_bravery(account):
    monument_name = 'Bravery Monument'
    account.caverns['Caverns'][monument_name]['Sword Count'] = (
        min(
            9,
            3  # Starting amount
            + (2 * (account.caverns['Caverns'][monument_name]['Hours'] >= 80))
            + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 750))
            + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 5000))
            + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 24000))
        )
    )
    account.caverns['Caverns'][monument_name]['Max Swords'] = (
            min(9, 3 + 2 + 1 + 1 + 1)
    )
    account.caverns['Caverns'][monument_name]['Sword Min'] = (
        3
        + (1 * floor(account.caverns['Caverns'][monument_name]['Hours'] / 6) * account.caverns['Schematics']['The Story Changes Over Time...']['Purchased'])
    )
    account.caverns['Caverns'][monument_name]['Sword Max'] = (
        (25 + (10 * floor(account.caverns['Caverns'][monument_name]['Hours'] / 6)
               * account.caverns['Schematics']['The Story Changes Over Time...']['Purchased']))
        * ValueToMulti(account.caverns['Measurements'][1]['Value'])
    )
    account.caverns['Caverns'][monument_name]['Rethrows'] = (
        0
        + (5 * (account.caverns['Caverns'][monument_name]['Hours'] >= 300))
        + (10 * (account.caverns['Caverns'][monument_name]['Hours'] >= 10000))
    )
    account.caverns['Caverns'][monument_name]['Max Rethrows'] = (
        5 + 10
    )
    account.caverns['Caverns'][monument_name]['Retellings'] = (
        1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 2000)
    )
    account.caverns['Caverns'][monument_name]['Max Retellings'] = (
        1
    )

def _calculate_caverns_monuments_justice(account):
    monument_name = 'Justice Monument'
    account.caverns['Caverns'][monument_name]['Mental Health'] = (
        1  #Starting amount
        + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 80))
        + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 2000))
        + (2 * (account.caverns['Caverns'][monument_name]['Hours'] >= 24000))
    )
    account.caverns['Caverns'][monument_name]['Max Mental Health'] = (
        1 + 1 + 1 + 2
    )
    if account.caverns['Caverns'][monument_name]['Hours'] > 0:
        schematic_bonus = log2(account.caverns['Caverns'][monument_name]['Hours']) * account.caverns['Schematics']['Compound Interest']['Purchased']
    else:
        #log2(0) throws a ValueError
        schematic_bonus = 0
    account.caverns['Caverns'][monument_name]['Coins'] = round(
        (
            5  #Starting amount
            + schematic_bonus
        )
        * (
            1
            + (0.5 * (account.caverns['Caverns'][monument_name]['Hours'] >= 750))
            + (1.5 * (account.caverns['Caverns'][monument_name]['Hours'] >= 10000))
        )
    )
    account.caverns['Caverns'][monument_name]['Max Coins'] = EmojiType.INFINITY.value
    account.caverns['Caverns'][monument_name]['Popularity'] = (
        3  #Starting amount
        + (7 * (account.caverns['Caverns'][monument_name]['Hours'] >= 5000))
    )
    account.caverns['Caverns'][monument_name]['Max Popularity'] = (
        0 + 10
    )
    account.caverns['Caverns'][monument_name]['Dismissals'] = (
        0
        + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 300))
        + (1 * (account.caverns['Caverns'][monument_name]['Hours'] >= 2000))
        + (2 * (account.caverns['Caverns'][monument_name]['Hours'] >= 24000))
    )
    account.caverns['Caverns'][monument_name]['Max Dismissals'] = (
        0 + 1 + 1 + 2
    )

def _calculate_caverns_the_bell(account):
    cavern_name = 'The Bell'
    account.caverns['Caverns'][cavern_name]['Total Improvements'] = sum(
        [ci_details['Level'] for ci_details in account.caverns['Caverns'][cavern_name]['Improvements'].values()]
    )
    account.caverns['Caverns'][cavern_name]['Stack Size'] = 25
    account.caverns['Caverns'][cavern_name]['Total Stacks'] = (
            account.caverns['Caverns'][cavern_name]['Total Improvements'] // account.caverns['Caverns'][cavern_name]['Stack Size']
    )
    for ci_index, ci_details in account.caverns['Caverns'][cavern_name]['Improvements'].items():
        try:
            account.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value'] = getBellImprovementBonus(
                ci_index,
                ci_details['Level'],
                account.caverns['Caverns'][cavern_name]['Total Stacks'],
                account.caverns['Schematics']["Improvement Stackin'"]['Purchased']
            )
        except:
            account.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value'] = 0
        account.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Description'] = (
            account.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Description'].replace(
                '{', f"{account.caverns['Caverns'][cavern_name]['Improvements'][ci_index]['Value']:,.0f}"
            )
        )

def _calculate_caverns_the_harp(account):
    cavern_name = 'The Harp'
    account.caverns['Caverns'][cavern_name]['Strings'] = (
        1
        + sum([1 for schematic in schematics_unlocking_harp_strings if account.caverns['Schematics'][schematic]['Purchased']])
        + account.caverns['Majiks']['String is Strung']['Level']
    )
    account.caverns['Caverns'][cavern_name]['Max Strings'] = (
        1
        + len(schematics_unlocking_harp_strings)
        + account.caverns['Majiks']['String is Strung']['MaxLevel']
    )
    account.caverns['Caverns'][cavern_name]['ChordsUnlocked'] = [
        chord for chord in account.caverns['Caverns'][cavern_name]['Chords'] if account.caverns['Caverns'][cavern_name]['Chords'][chord]['Unlocked']
    ]
    account.caverns['Caverns'][cavern_name]['ChordsUnlockedCount'] = len(account.caverns['Caverns'][cavern_name]['ChordsUnlocked'])
    account.caverns['Caverns'][cavern_name]['Max Chords'] = 2 + len(schematics_unlocking_harp_chords)  #C and D available by default

def _calculate_caverns_jar_collectibles(account):
    # Dependency: _calculate_w7_legend_talents
    legend_talent_multi = ValueToMulti(account.legend_talents['Talents']['Whats in your Jar?']['Value'])
    for collectible_name, collectible_details in account.caverns['Collectibles'].items():
        try:
            account.caverns['Collectibles'][collectible_name]['Value'] = (
                collectible_details['Level'] * collectible_details['ScalingValue']
                * legend_talent_multi
            )
            if '{' in collectible_details['Description']:
                scaling_note = (
                    f"<br>+{account.caverns['Collectibles'][collectible_name]['ScalingValue']}"
                    f"{'%' if '%' in collectible_details['Description'] else ''} per level"
                )
                account.caverns['Collectibles'][collectible_name]['Description'] = collectible_details['Description'].replace(
                    '{', f"{round_and_trim(account.caverns['Collectibles'][collectible_name]['Value'])}"
                )

            elif '}' in collectible_details['Description']:
                scaling_note = f"<br>{round_and_trim(ValueToMulti(account.caverns['Collectibles'][collectible_name]['ScalingValue']) - 1)} per level"
                account.caverns['Collectibles'][collectible_name]['Description'] = collectible_details['Description'].replace(
                    '}', f"{round_and_trim(ValueToMulti(account.caverns['Collectibles'][collectible_name]['Value']))}"
                )
            else:
                scaling_note = ''
            account.caverns['Collectibles'][collectible_name]['Description'] += scaling_note
        except:
            logger.exception(f"Unable to update description for Collectible: {collectible_name}")
            continue  #Already defaulted to 0 during parsing

def _calculate_caverns_gambit(account):
    cavern_name = caverns_cavern_names[14]

    #PTS Multi
    account.caverns['Caverns'][cavern_name]['PtsMulti'] = ValueToMulti(
        account.caverns['Measurements'][13]['Value']  # Measurement
        + account.caverns['Studies'][13]['Value']  # + Gambit Study bonus
        + (10 * account.caverns['Schematics']['The Sicilian']['Purchased'])  # + The Sicilian schematic
        + account.caverns['Caverns']['Wisdom Monument']['Bonuses'][27]['Value']  # + Wisdom Monument bonus
        + account.caverns['Collectibles']['Deep Blue Square']['Value']
        + account.caverns['Collectibles']['Murky Fabrege Egg']['Value']
    )

    #Total PTS
    account.caverns['Caverns'][cavern_name]['TotalPts'] = (
        account.caverns['Caverns'][cavern_name]['BasePts']
        * account.caverns['Caverns'][cavern_name]['PtsMulti']
    )

    #Bonuses
    for bonus_index, bonus_details in account.caverns['Caverns'][cavern_name]['Bonuses'].items():
        #Update Unlocked status
        account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Unlocked'] = (
            account.caverns['Caverns'][cavern_name]['TotalPts'] >= bonus_details['PtsRequired']
        )

        #Calculate Value
        if bonus_index == 0:
            account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value'] = (
                 max(1 if account.caverns['Caverns'][cavern_name]['TotalPts'] > 0 else 0, ceil(
                     safer_math_log(account.caverns['Caverns'][cavern_name]['TotalPts'], 2)
                     - 8
                     + (safer_math_log(account.caverns['Caverns'][cavern_name]['TotalPts'], 'Lava') - 1)
                     ))
            )
        else:
            if bonus_details['ScalesWithPts']:
                account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value'] = (
                    bonus_details['ScalingValue'] * safer_math_log(account.caverns['Caverns'][cavern_name]['TotalPts'], 'Lava')
                )
            else:
                account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value'] = bonus_details['ScalingValue']

        #Substitute Value into Description
        if '{' in bonus_details['Name']:
            if bonus_index == 0 or not bonus_details['ScalesWithPts']:
                account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Name'] = bonus_details['Name'].replace(
                    '{', f"{account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value']}"
                )
            else:
                #bonus_details['ScalesWithPts']
                account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Name'] = bonus_details['Name'].replace(
                    '{', f"{account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value']:.2f}"
                )

        elif '}' in bonus_details['Name']:
            account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Name'] = bonus_details['Name'].replace(
                '}', f"{ValueToMulti(account.caverns['Caverns'][cavern_name]['Bonuses'][bonus_index]['Value']):.3f}x"
            )

    # I hate this being here, but ordering matters. Unlocked status isn't accurate until after this calculation
    if account.caverns['Caverns']['Gambit']['Bonuses'][9]['Unlocked']:
        _update_w3_building_max_levels(account, 'All Towers', 100, 'Gambit Cavern upgrade Index 9')


def _calculate_w6(account):
    # _calculate_w6_farming(account)  # Runs in wave3 due to Land Rank multi from Talents
    _calculate_w6_summoning(account)


def _calculate_w6_sneaking_gemstones(account):
    # TODO: Move to Talent class and calculate by Talent.as_multi
    generational_gemstones_level = account.get_current_max_talent("Generational Gemstones")
    gemstone_multi = lava_func("decayMulti", max(0, generational_gemstones_level), 3, 300)
    account.sneaking.calculate_gemstones_values(
        generational_gemstones_level, gemstone_multi
    )


def _calculate_w6_farming(account):
    # Runs in wave3 due to Land Rank multi from Talents
    _calculate_w6_farming_land_ranks(account)
    _calculate_w6_farming_crop_depot(account)
    _calculate_w6_farming_markets(account)
    account.farming.calculate_crop_value_multi(account.ballot)
    _calculate_w6_farming_crop_evo(account)
    account.farming.calculate_crop_speed(account)
    account.farming.calculate_bean_bonus(account)
    account.farming.calculate_og(account)


def _calculate_w6_farming_land_ranks(account):
    # TODO: Move to Talent class and calculate by Talent.as_multi
    dank_rank_level = account.get_current_max_talent("Dank Rank")
    dank_rank_multi = lava_func(
        all_talentsDict[207]['funcX'],
        dank_rank_level,
        all_talentsDict[207]['x1'],
        all_talentsDict[207]['x2']
    )
    account.farming.calculate_land_rank_bonus(dank_rank_multi)


def _calculate_w6_farming_crop_depot(account):
    # Dependency: Lab, Grimoire, Emporium
    lab_multi = ValueToMulti(
        (account.labBonuses['Depot Studies PhD']['Value'] + account.labJewels['Pure Opal Rhombol']['Value']) * account.labBonuses['Depot Studies PhD']['Enabled']
    )
    grimoire_multi = account.grimoire['Upgrades']['Superior Crop Research']['Total Value']  #Grimoire 22: Superior Crop Research already a Multi
    account.farming.calculate_crop_depot_bonus(
        lab_multi, grimoire_multi, account.sneaking.emporium
    )


def _calculate_w6_farming_markets(account):
    # Dependency: Gemshop, Merit
    bought_plot = (
        account.gemshop['Purchases']['Plot Of Land']['Owned']
        + min(3, account.merits[5][2]['Level'])
    )
    account.farming.calculate_market_bonus(bought_plot)


def _calculate_w6_farming_crop_evo(account):
    # Dependency: _calculate_w6_summoning_regular_bonuses
    # Alchemy
    farming = account.farming
    map_opened = 0
    mama_trolls_map_open = False
    for char in account.all_characters:
        for mapIndex in range(251, 264):  # Clearing the fake portal at Samurai Guardians doesn't count
            try:
                if int(float(char.kill_dict.get(mapIndex, [1])[0])) <= 0:
                    map_opened += 1
                    mama_trolls_map_open = mama_trolls_map_open or mapIndex == 257
            except:
                continue
    farming.magic_bean_unlocked = mama_trolls_map_open
    account.farming.calculate_crop_evo_multi(map_opened, account)


def _calculate_w6_summoning(account):
    _calculate_w6_summoning_doublers(account)

def _calculate_w6_summoning_doublers(account):
    account.summoning['Total Doublers Owned'] = (
        account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value']
        + (10 * account.event_points_shop['Bonuses']['Summoning Star']['Owned'])
    )


def _calculate_wave_3(account):
    _calculate_w3_library_max_book_levels(account)
    _calculate_w3_equinox_max_levels(account)
    _calculate_general_character_bonus_talent_levels(account)
    _calculate_general_crystal_spawn_chance(account)
    _calculate_w6_sneaking_gemstones(account)
    _calculate_master_classes_grimoire_bone_sources(account)
    _calculate_class_unique_kill_stacks(account)
    _calculate_w6_farming(account)

def _calculate_w3_library_max_book_levels(account):
    # Dependency: _calculate_w6_summoning_regular_bonuses
    account.library['StaticSum'] = (
        0
        + (25 * (0 < account.construction_buildings['Talent Book Library']['Level']))
        + (5 * account.achievements['Checkout Takeout']['Complete'])
        + (10 * (0 < account.atom_collider['Atoms']['Oxygen - Library Booker']['Level']))
        + (25 * account.sailing['Artifacts']['Fury Relic']['Level'])
    )
    account.library['ScalingSum'] = (
        0
        + 2 * account.merits[2][2]['Level']
        + 2 * account.saltlick.get('Max Book', 0)
    )
    account.library['MaxBookLevel'] = (
        100 + account.library['StaticSum'] + account.library['ScalingSum']
        + account.summoning['Bonuses']['+{ Library Max']['Value']
    )

def _calculate_w3_equinox_max_levels(account):
    bonus_equinox_levels = (
        account.summoning['Endless Bonuses'].get('+{ Equinox Max LV', 0)
        + (10 * account.gaming['SuperBits']['Equinox Unending']['Unlocked'])
    )
    if bonus_equinox_levels > 0:
        for bonus, bonus_details in account.equinox_bonuses.items():
            if bonus_details['SummoningExpands']:
                account.equinox_bonuses[bonus]['PlayerMaxLevel'] += bonus_equinox_levels
                account.equinox_bonuses[bonus]['FinalMaxLevel'] += bonus_equinox_levels

def _calculate_general_character_bonus_talent_levels(account):
    account.bonus_talents = {
        'Kattelkruk Set': {
            'Value': account.armor_sets['Sets']['KATTLEKRUK SET']['Total Value'],
            'Image': account.armor_sets['Sets']['KATTLEKRUK SET']['Image'],
            'Label': f"{{{{Set bonus|#armor-sets}}}}: Kattlekruk Set: "
                     f"+{account.armor_sets['Sets']['KATTLEKRUK SET']['Total Value']:g}"
                     f"/{account.armor_sets['Sets']['KATTLEKRUK SET']['Base Value']:g}",
            'Progression': int(account.armor_sets['Sets']['KATTLEKRUK SET']['Owned']),
            'Goal': 1
        },
        'Rift Slug': {
            'Value': 25 * has_companion('Rift Slug'),
            'Image': 'rift-slug',
            'Label': f"Companion: Rift Slug: "
                     f"+{25 * has_companion('Rift Slug')}/25",
            'Progression': int(has_companion('Rift Slug')),
            'Goal': 1
        },
        'ES Family': {
            'Value': floor(account.family_bonuses["Elemental Sorcerer"]['Value']),
            'Image': 'elemental-sorcerer-icon',
            'Label': f"ES Family Bonus: "
                     f"+{floor(account.family_bonuses['Elemental Sorcerer']['Value'])}.<br>"
                     f"Next increase at Class Level: ",
            'Progression': account.family_bonuses['Elemental Sorcerer']['Level'],
            'Goal': getNextESFamilyBreakpoint(account.family_bonuses['Elemental Sorcerer']['Level'])
        },
        'Equinox Symbols': {
            'Value': account.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
            'Image': 'equinox-symbols',
            'Label': f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: "
                     f"+{account.equinox_bonuses['Equinox Symbols']['CurrentLevel']}/{account.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']}",
            'Progression': account.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
            'Goal': account.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']
        },
        'Maroon Warship': {
            'Value': 1 * account.achievements['Maroon Warship']['Complete'],
            'Image': 'maroon-warship',
            'Label': f"W5 Achievement: Maroon Warship: "
                     f"+{1 * account.achievements['Maroon Warship']['Complete']}/1",
            'Progression': 1 if account.achievements['Maroon Warship']['Complete'] else 0,
            'Goal': 1
        },
        'Sneaking Mastery': {
            'Value': 5 if account.sneaking.unlocked_mastery >= 3 else 0,
            'Image': 'sneaking-mastery',
            'Label': f"{{{{ Rift|#rift }}}}: Sneaking Mastery: "
                     f"+{5 if account.sneaking.unlocked_mastery >= 3 else 0}/5 (Mastery III)",
            'Progression': account.sneaking.unlocked_mastery,
            'Goal': 3
        },
        'Grimoire': {
            'Value': account.grimoire['Upgrades']['Skull of Major Talent']['Level'],
            'Image': account.grimoire['Upgrades']['Skull of Major Talent']['Image'],
            'Label': f"{{{{Grimoire|#the-grimoire}}}}: Skull of Major Talent: "
                     f"+{account.grimoire['Upgrades']['Skull of Major Talent']['Level']}"
                     f"/{account.grimoire['Upgrades']['Skull of Major Talent']['Max Level']}",
            'Progression': account.grimoire['Upgrades']['Skull of Major Talent']['Level'],
            'Goal': account.grimoire['Upgrades']['Skull of Major Talent']['Max Level']
        }
    }
    account.sum_account_wide_bonus_talents = 0
    for bonusName, bonusValuesDict in account.bonus_talents.items():
        try:
            account.sum_account_wide_bonus_talents += int(bonusValuesDict.get('Value', 0))
        except:
            continue

    for char in account.safe_characters:
        character_specific_bonuses = 0

        # Arctis minor link
        if account.divinity['AccountWideArctis'] or char.isArctisLinked():
            arctis_base = 15
            bigp_value = account.alchemy_bubbles['Big P']['BaseValue']
            div_minorlink_value = char.divinity_level / (char.divinity_level + 60)
            final_arctis_result = ceil(arctis_base * bigp_value * div_minorlink_value)
            character_specific_bonuses += final_arctis_result

        # Symbols of Beyond = 1 + 1 per 20 levels
        if any([elite in char.all_classes for elite in ["Blood Berserker", "Divine Knight"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("149", 0) // 20)  # Symbols of Beyond - Red
        elif any([elite in char.all_classes for elite in ["Siege Breaker", "Beast Master"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("374", 0) // 20)  # Symbols of Beyond - Green
        elif any([elite in char.all_classes for elite in ["Elemental Sorcerer", "Bubonic Conjuror"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("539", 0) // 20)  # Symbols of Beyond - Purple
        character_specific_bonuses += char.symbols_of_beyond

        char.total_bonus_talent_levels = account.sum_account_wide_bonus_talents + character_specific_bonuses
        char.max_talents_over_books = account.library['MaxBookLevel'] + char.total_bonus_talent_levels

        # If they're an ES, use max level of Family Guy to calculate floor(ES Family Value * Family Guy)
        if char.class_name == 'Elemental Sorcerer':
            try:
                #TODO: Move one-off talent value calculation
                family_guy_bonus = lava_func(
                    'decay',
                    char.max_talents_over_books + char.max_talents.get('374', 0),
                    40,
                    100
                )
                family_guy_multi = ValueToMulti(family_guy_bonus)
                final_fg_value = (
                    floor(account.family_bonuses['Elemental Sorcerer']['Value'] * family_guy_multi)
                    - floor(account.family_bonuses['Elemental Sorcerer']['Value'])
                )
                char.max_talents_over_books += final_fg_value
                char.setFamilyGuyBonus(final_fg_value)
            except:
                pass

def _calculate_general_crystal_spawn_chance(account):
    #This assumes you have the Shrine bonus and the Star Talent maxed
    poop_value = 10 * (1 + next(c.getStars() for c in account.cards if c.name == 'Poop'))
    genie_value = 15 * (1 + next(c.getStars() for c in account.cards if c.name == 'Demon Genie'))

    # If they have both doublers, add together and 2x
    if account.labChips['Omega Nanochip'] and account.labChips['Omega Motherboard']:
        total_card_chance = 2 * (poop_value + genie_value)
    # If they only have 1 doubler, double whichever is stronger
    elif account.labChips['Omega Nanochip'] or account.labChips['Omega Motherboard']:
        total_card_chance = (2 * max(poop_value, genie_value)) + min(poop_value, genie_value)
    # If they have neither doubler, use base values only
    else:
        total_card_chance = poop_value + genie_value

    account_wide = (
        base_crystal_chance
        * ValueToMulti(account.stamps['Crystallin'].total_value)
        * ValueToMulti(total_card_chance)
    )

    for char in account.all_characters:
        cmon_out_crystals_multi = max(1, ValueToMulti(lava_func(
            'decay',
            char.max_talents_over_books if char.max_talents.get("26", 0) > 0 else 0,  #This is an assumption that Cmon Out Crystals is max booked
            300,
            100
        )))
        crystals_4_dayys_multi = max(1, ValueToMulti(lava_func(
            'decay',
            char.max_talents.get("619", 0),
            174,
            50
        )))
        shrine_and_po = ValueToMulti(char.po_boxes_invested['Non Predatory Loot Box']['Bonus3Value'] + account.shrines['Crescent Shrine']['Value'])
        try:
            character_influenced = (
                shrine_and_po
                * cmon_out_crystals_multi
                * crystals_4_dayys_multi
            )
        except:
            logger.exception(f"Character Specific crystal spawn chance calc exception for {char.character_name}")
            character_influenced = 1
        char.setCrystalSpawnChance(account_wide * character_influenced)
    account.highest_crystal_spawn_chance = max(
        [char.crystal_spawn_chance for char in account.all_characters if "Journeyman" not in char.all_classes], default=base_crystal_chance
    )
    account.highest_jman_crystal_spawn_chance = max(
        [char.crystal_spawn_chance for char in account.all_characters if "Journeyman" in char.all_classes], default=base_crystal_chance
    )

def _calculate_class_unique_kill_stacks(account):
    abc = {
        'King of the Remembered': {
            'Talent Number': 178,
            'Class List': account.dks,
            'Bonus': 'Printer Output',
        },
        'Archlord of the Pirates': {
            'Talent Number': 328,
            'Class List': account.sbs,
            'Bonus': 'Drop Rate and Class EXP',
        },
        'Wormhole Emperor': {
            'Talent Number': 508,
            'Class List': account.sorcs,
            'Bonus': 'Damage',
        }
    }
    for talent_name, talent_details in abc.items():
        talent_levels = []
        for char in talent_details['Class List']:
            talent_levels.append(char.current_preset_talents.get(f"{talent_details['Talent Number']}", 0) + char.total_bonus_talent_levels)
            talent_levels.append(char.secondary_preset_talents.get(f"{talent_details['Talent Number']}", 0) + char.total_bonus_talent_levels)

        account.class_kill_talents[talent_name]['Bonus Type'] = abc[talent_name]['Bonus']
        account.class_kill_talents[talent_name]['funcType'] = all_talentsDict[talent_details['Talent Number']]['funcX']
        account.class_kill_talents[talent_name]['x1'] = all_talentsDict[talent_details['Talent Number']]['x1']
        account.class_kill_talents[talent_name]['x2'] = all_talentsDict[talent_details['Talent Number']]['x2']
        account.class_kill_talents[talent_name]['Highest Preset Level'] = max(talent_levels, default=0)
        account.class_kill_talents[talent_name]['Talent Value'] = lava_func(
            funcType=account.class_kill_talents[talent_name]['funcType'],
            level=account.class_kill_talents[talent_name]['Highest Preset Level'],
            x1=account.class_kill_talents[talent_name]['x1'],
            x2=account.class_kill_talents[talent_name]['x2']
        )
        account.class_kill_talents[talent_name]['Kill Stacks'] = safer_math_log(account.class_kill_talents[talent_name]['Kills'], 'Lava')
        account.class_kill_talents[talent_name]['Total Value'] = (
            account.class_kill_talents[talent_name]['Talent Value'] * account.class_kill_talents[talent_name]['Kill Stacks']
        )
        # logger.debug(f"{account.class_kill_talents[talent_name] = }")

def _calculate_wave_4(account):
    # Mostly stuff that relies on Talent Level calculations that happen in Wave 3
    _calculate_w1_statues(account)
    _calculate_w6_beanstalk(account)

def _calculate_w1_statues(account):
    voodoo_statufication_multi = [
        lava_func(
            all_talentsDict[56]['funcX'],
            char.max_talents.get('56', 0),
            all_talentsDict[56]['x1'],
            all_talentsDict[56]['x2']
        ) for char in account.vmans
    ]

    voodoo_statufication_multi = ValueToMulti(max(voodoo_statufication_multi, default=0))

    vault_multi = account.vault['Upgrades']['Statue Bonanza']['Total Value']
    vault_statues = [statues_dict[i]['Name'] for i in [0, 1, 2, 6]]

    onyx_multi = 2 + (0.3 * account.sailing['Artifacts']['The Onyx Lantern']['Level'])
    onyx_typenumber = get_statue_type_index_from_name('Onyx')

    event_shop_multi = ValueToMulti(30 * account.event_points_shop['Bonuses']['Smiley Statue']['Owned'])

    # The value of Dragon Statue is used to increase other statues so must be calculated first
    account.statues['Dragon Statue']['Value'] = (
        account.statues['Dragon Statue']['BaseValue']
        * account.statues['Dragon Statue']['Level']
        * (onyx_multi if account.statues['Dragon Statue']['TypeNumber'] >= onyx_typenumber else 1)
        * (vault_multi if 'Dragon Statue' in vault_statues else 1)  #It isn't currently, but, y'know.. maybe one day
        * voodoo_statufication_multi
        * event_shop_multi
    )
    dragon_multi = ValueToMulti(account.statues['Dragon Statue']['Value'])
    # logger.debug(f"{vault_multi = }, {voodoo_statufication_multi = }, {onyx_multi = }, {dragon_multi = }, {event_shop_multi = }")

    for statue_name, statue_details in account.statues.items():
        if statue_name != 'Dragon Statue':
            account.statues[statue_name]['Value'] = (
                account.statues[statue_name]['BaseValue']
                * account.statues[statue_name]['Level']
                * (onyx_multi if statue_details['TypeNumber'] >= onyx_typenumber else 1)
                * (vault_multi if statue_name in vault_statues else 1)
                * voodoo_statufication_multi
                * dragon_multi
                * event_shop_multi
            )

    account.statue_effect_advice = [
        Advice(
            label=f"Voidwalker {{{{talent|#library}}}}: Voodoo Statufication: {round(voodoo_statufication_multi, 2):g}x",
            picture_class='voodoo-statufication'
        ),
        Advice(
            label=f"Onyx base bonus: {2 * account.onyx_statues_unlocked}/2x"
                  f"<br>Total including {{{{The Onyx Lantern |  #sailing}}}}: {round(onyx_multi, 1):g}/"
                  f"{2 + (0.3 * max_sailing_artifact_level)}x",
            picture_class='onyx-tools',
            progression=account.sailing['Artifacts']['The Onyx Lantern']['Level'],
            goal=max_sailing_artifact_level,
            resource='the-onyx-lantern'
        ),
        Advice(
            label=f"{{{{Event Shop|#event-shop}}}}: Smiley Statue: {round(event_shop_multi, 2):g}/1.3x",
            picture_class=account.event_points_shop['Bonuses']['Smiley Statue']['Image'],
            progression=int(account.event_points_shop['Bonuses']['Smiley Statue']['Owned']),
            goal=1
        ),
        Advice(
            label=f"Level {account.statues['Dragon Statue']['Level']} Dragon Statue: {round(dragon_multi, 3):g}x",
            picture_class=account.statues['Dragon Statue']['Image']
        ),
        get_upgrade_vault_advice('Statue Bonanza'),
        Advice(
            label=f"Total Multi for all statues: {round(voodoo_statufication_multi * onyx_multi * dragon_multi * event_shop_multi, 2):g}x"
                  f"<br>Vault statues: {round(voodoo_statufication_multi * onyx_multi * dragon_multi * event_shop_multi * vault_multi, 2):g}x",
            picture_class='town-marble'
        )
    ]


def _calculate_w6_beanstalk(account):
    # Dependency: Emporium
    account.beanstalk.calculate_unlocked_tier(account.sneaking.emporium)
    account.beanstalk.calculate_golden_food_multi()
    account.beanstalk.calculate_bonuses()


def _calculate_w7(account):
    _calculate_w7_advice_for_money(account)
    _calculate_w7_coral_reef(account)

def _calculate_w7_advice_for_money(account):
    for bonus_name, bonus_details in account.advice_for_money['Upgrades'].items():
        bonus_details["Value"] = bonus_details["Level"] / (bonus_details["Level"] + 100) * bonus_details["Bonus"]
        if "{" in bonus_details["Effect"]:
            bonus_details["Effect"] = bonus_details["Effect"].replace("{", f"{bonus_details['Value']:.2f}")
        elif "}" in bonus_details["Effect"]:
            bonus_details["Value"] = ValueToMulti(bonus_details["Value"])
            bonus_details["Effect"] = bonus_details["Effect"].replace("}", f"{bonus_details['Value']:.4f}")

def _calculate_w7_coral_reef(account):
    for coral_details in account.coral_reef['Reef Corals'].values():
        coral_details['Next Cost'] = int(coral_details['Coefficient'] * safer_math_pow(coral_details['Exponent Base'], coral_details['Level'], 0))

def _calculate_w7_legend_talents(account):
    for legend_name, legend_details in account.legend_talents['Talents'].items():
        legend_details['Value'] = legend_details['Base Value'] * legend_details['Level']
        next_value = legend_details['Base Value'] * (legend_details['Level'] + 1)
        if '{' in legend_details['Description']:
            legend_details['Description'] = legend_details['Description'].replace('{', f"{legend_details['Value']}")
        if '}' in legend_details['Description']:
            legend_details['Description'] = legend_details['Description'].replace('}', f"{ValueToMulti(legend_details['Value'])}")
        if '$' in legend_details['Description']:
            if legend_name == 'Double Aint Enough':
                legend_details['Description'] = legend_details['Description'].replace('$', f"{2 + legend_details['Value'] / 100}")
            elif legend_name == 'Super Talent Points':
                legend_details['Description'] = legend_details['Description'].replace('$', f"{50 + account.legend_talents['Talents']['Super Duper Talents']['Value']}")
            elif legend_name == 'Inevitable Builder':
                legend_details['Description'] = legend_details['Description'].replace(' for a total bonus speed of $x', '')
            elif legend_name == "6 O'Clock Crystals":
                legend_details['Description'] = legend_details['Description'].replace('$ ', '')
            else:
                legend_details['Description'] = legend_details['Description'].replace('$', f"{legend_details['Value']}")
        if '{' in legend_details['Bonus']:
            legend_details['Bonus'] = legend_details['Bonus'].replace('{', f"{next_value}")
        if '}' in legend_details['Bonus']:
            legend_details['Bonus'] = legend_details['Bonus'].replace('}', f"{ValueToMulti(next_value)}")
        if '$' in legend_details['Bonus']:
            if legend_name == 'Double Aint Enough':
                legend_details['Bonus'] = legend_details['Bonus'].replace('$', f"{2 + next_value / 100}")
            else:
                legend_details['Bonus'] = legend_details['Bonus'].replace('$', f"{next_value}")
