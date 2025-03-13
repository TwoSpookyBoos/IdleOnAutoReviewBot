from math import ceil, floor, log2
from consts import (
    # General
    lavaFunc, ceilUpToBase, ValueToMulti, getNextESFamilyBreakpoint,
    base_crystal_chance,
    filter_recipes, filter_never,
    # Master Classes
    grimoire_stack_types,
    # W1
    vault_stack_types, grimoire_coded_stack_monster_order, decode_enemy_name,
    # W2
    fishingToolkitDict,
    islands_trash_shop_costs,
    killroy_dict,
    # W3
    arbitrary_shrine_goal, arbitrary_shrine_note,
    # W4
    nblbMaxBubbleCount, maxMealCount, maxMealLevel,  # W5
    numberOfArtifactTiers, divinity_offeringsDict, divinity_DivCostAfter3,
    # W6
    maxFarmingValue, summoning_rewards_that_dont_multiply_base_value,
    # Caverns
    caverns_conjuror_majiks, schematics_unlocking_buckets, monument_bonuses, getBellImprovementBonus, monument_names, released_monuments,
    infinity_string, schematics_unlocking_harp_strings, schematics_unlocking_harp_chords
)
from models.models import Advice
from utils.data_formatting import safe_loads, safer_get, safer_math_pow
from utils.logging import get_logger
from utils.text_formatting import getItemDisplayName, getItemCodeName

logger = get_logger(__name__)

def calculate_account(account):
    _calculate_wave_1(account)
    _calculate_wave_2(account)
    _calculate_wave_3(account)

def _calculate_wave_1(account):
    _calculate_caverns_majiks(account)
    _calculate_w6_summoning_winner_bonuses(account)

def _calculate_caverns_majiks(account):
    alt_pocket_div = {
        'BonusPerLevel': 15,
        'Description': '% All Stats'
    }
    for majik_type, majiks in caverns_conjuror_majiks.items():
        for majik_index, majik_data in enumerate(majiks):
            if majik_data['Name'] == 'Pocket Divinity' and account.doot_owned:
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
                f"{account.caverns['Majiks'][majik_data['Name']]['Value']}/{account.caverns['Majiks'][majik_data['Name']]['MaxValue']}"
                f"{account.caverns['Majiks'][majik_data['Name']]['Description']}"
            )
            # logger.debug(f"{majik_data['Name']} value set to {account.caverns['Majiks'][majik_data['Name']]['Value']}")

def _calculate_w6_summoning_winner_bonuses(account):
    mga = 1.3
    player_mga = 1.3 if account.sneaking['PristineCharms']['Crystal Comb']['Obtained'] else 1
    account.summoning['WinnerBonusesAdvice'].append(Advice(
        label=f"{{{{ Pristine Charm|#sneaking }}}}: Crystal Comb: "
              f"{player_mga}/1.3x",
        picture_class=account.sneaking['PristineCharms']['Crystal Comb']['Image'],
        progression=int(account.sneaking['PristineCharms']['Crystal Comb']['Obtained']),
        goal=1
    ))

    if not account.sneaking['JadeEmporium']['Brighter Lighthouse Bulb']['Obtained']:
        winzLanternPostString = ". Unlocked from {{ Jade Emporium|#sneaking }}"
    else:
        winzLanternPostString = ""

    mgb_partial = ValueToMulti(
        (25 * numberOfArtifactTiers)
        + account.merits[5][4]['MaxLevel']
        + 1  #int(account.achievements['Spectre Stars'])
        + 1  #int(account.achievements['Regalis My Beloved'])
    )
    mgb_full = ValueToMulti(
        (25 * numberOfArtifactTiers)
        + account.merits[5][4]['MaxLevel']
        + 1  #int(account.achievements['Spectre Stars'])
        + 1  #int(account.achievements['Regalis My Beloved'])
        + account.summoning['Endless Bonuses']['x Winner Bonuses']
    )
    player_mgb_partial = ValueToMulti(
        (25 * account.sailing['Artifacts']['The Winz Lantern']['Level'])
        + account.merits[5][4]['Level']
        + int(account.achievements['Spectre Stars']['Complete'])
        + int(account.achievements['Regalis My Beloved']['Complete'])
    )
    player_mgb_full = ValueToMulti(
        (25 * account.sailing['Artifacts']['The Winz Lantern']['Level'])
        + account.merits[5][4]['Level']
        + int(account.achievements['Spectre Stars']['Complete'])
        + int(account.achievements['Regalis My Beloved']['Complete'])
        + account.summoning['Endless Bonuses']['x Winner Bonuses']
    )

    account.summoning['WinnerBonusesAdvice'].append(Advice(
        label=f"{{{{ Artifact|#sailing }}}}: The Winz Lantern: "
              f"{1 + (.25 * account.sailing['Artifacts']['The Winz Lantern']['Level'])}/2x{winzLanternPostString}",
        picture_class="the-winz-lantern",
        progression=account.sailing['Artifacts']['The Winz Lantern']['Level'],
        goal=4
    ))
    account.summoning['WinnerBonusesAdvice'].append(Advice(
        label=f"W6 Larger Winner bonuses merit: "
              f"+{account.merits[5][4]['Level']}/{account.merits[5][4]['MaxLevel']}%",
        picture_class="merit-5-4",
        progression=account.merits[5][4]["Level"],
        goal=account.merits[5][4]["MaxLevel"]
    ))
    account.summoning['WinnerBonusesAdvice'].append(Advice(
        label=f"W6 Achievement: Spectre Stars: "
              f"+{int(account.achievements['Spectre Stars']['Complete'])}/1%",
        picture_class="spectre-stars",
        progression=int(account.achievements['Spectre Stars']['Complete']),
        goal=1
    ))
    account.summoning['WinnerBonusesAdvice'].append(Advice(
        label=f"W6 Achievement: Regalis My Beloved: "
              f"+{int(account.achievements['Regalis My Beloved']['Complete'])}/1%",
        picture_class="regalis-my-beloved",
        progression=account.summoning['SanctuaryTotal'] if not account.achievements['Regalis My Beloved']['Complete'] else 360,
        goal=360
    ))
    account.summoning['WinnerBonusesMultiPartial'] = max(1, player_mga * player_mgb_partial)
    account.summoning['WinnerBonusesMultiMaxPartial'] = max(1, mga * mgb_partial)
    account.summoning['WinnerBonusesSummaryPartial'] = Advice(
        label=f"Winner Bonuses Multi: {account.summoning['WinnerBonusesMultiPartial']:.3f}/{account.summoning['WinnerBonusesMultiMaxPartial']:.3f}x",
        picture_class="summoning",
        progression=f"{account.summoning['WinnerBonusesMultiPartial']:.3f}",
        goal=f"{account.summoning['WinnerBonusesMultiMaxPartial']:.3f}",
        #unit="x"
    )
    account.summoning['WinnerBonusesMultiFull'] = max(1, player_mga * player_mgb_full)
    account.summoning['WinnerBonusesMultiMaxFull'] = max(1, mga * mgb_full)
    account.summoning['WinnerBonusesSummaryFull'] = [
        Advice(
            label=f"Winner Bonuses multi from Endless Summoning: {account.summoning['Endless Bonuses']['x Winner Bonuses']}/{infinity_string}",
            picture_class='cyan-upgrade-13',
            progression=account.summoning['Endless Bonuses']['x Winner Bonuses'],
            goal=infinity_string,
            completed=True
        ),
        Advice(
            label=f"Winner Bonuses Multi: {account.summoning['WinnerBonusesMultiFull']:.3f}/{account.summoning['WinnerBonusesMultiMaxFull']:.3f}x",
            picture_class="summoning",
            progression=f"{account.summoning['WinnerBonusesMultiFull']:.3f}",
            goal=f"{account.summoning['WinnerBonusesMultiMaxFull']:.3f}",
            # unit="x"
        )
    ]

    for bonus_name, bonus_value in account.summoning['Endless Bonuses'].items():
        if bonus_name not in summoning_rewards_that_dont_multiply_base_value:
            if bonus_name.startswith('x'):
                account.summoning['Endless Bonuses'][bonus_name] = ValueToMulti(account.summoning['Endless Bonuses'][bonus_name] * account.summoning['WinnerBonusesMultiFull'])
            else:
                account.summoning['Endless Bonuses'][bonus_name] *= account.summoning['WinnerBonusesMultiFull']
        elif bonus_name in summoning_rewards_that_dont_multiply_base_value and bonus_name.startswith('x'):
            account.summoning['Endless Bonuses'][bonus_name] = ValueToMulti(account.summoning['Endless Bonuses'][bonus_name])
    #logger.debug(f"Final Endless Bonuses after {account.summoning['Battles']['Endless']} wins: {account.summoning['Endless Bonuses']}")

def _calculate_wave_2(account):
    _calculate_general(account)
    _calculate_w1(account)
    _calculate_w2(account)
    _calculate_w3(account)
    _calculate_w4(account)
    _calculate_w5(account)
    _calculate_caverns(account)
    _calculate_w6(account)

def _calculate_general(account):
    _calculate_general_alerts(account)
    _calculate_general_item_filter(account)
    account.highestWorldReached = _calculate_general_highest_world_reached(account)
    _calculate_general_master_classes_grimoire(account)

def _calculate_general_alerts(account):
    if account.stored_assets.get("Trophy2").amount >= 75 and account.equinox_dreams[17]:
        account.alerts_AdviceDict['General'].append(Advice(
            label=f"You have {account.stored_assets.get('Trophy2').amount}/75 Lucky Lads to craft a Luckier Lad!",
            picture_class="luckier-lad"
        ))

def _calculate_general_item_filter(account):
    raw_fishing_toolkit_lures = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[0]
    raw_fishing_toolkit_lines = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[1]
    for filtered_codeName in account.item_filter:
        filtered_displayName = getItemDisplayName(filtered_codeName)
        if (
            filtered_codeName == 'Trophy2'  #Lucky Lad
            and 'Trophy20' not in account.registered_slab  #Luckier Lad
            and account.stored_assets.get("Trophy2").amount < 75
        ):
            account.alerts_AdviceDict['General'].append(Advice(
                label=f"Lucky filtered before 75 for Luckier Lad",
                picture_class="lucky-lad",
                resource="luckier-lad"
            ))
        elif filtered_displayName in filter_recipes:
            for itemName in filter_recipes[filtered_displayName]:
                if getItemCodeName(itemName) not in account.registered_slab:
                    account.alerts_AdviceDict['General'].append(Advice(
                        label=f"{filtered_displayName} filtered, {itemName} not in Slab",
                        picture_class=filtered_displayName,
                        resource=itemName
                    ))
        elif filtered_displayName in filter_never and account.autoloot:
            account.alerts_AdviceDict['General'].append(Advice(
                label=f"Why did you filter {filtered_displayName}???",
                picture_class=filtered_displayName,
            ))
        elif filtered_codeName not in account.registered_slab:
            account.alerts_AdviceDict['General'].append(Advice(
                label=f"{filtered_displayName} filtered, not in Slab",
                picture_class=filtered_displayName,
            ))
        elif filtered_displayName in fishingToolkitDict['Lures']:
            if fishingToolkitDict['Lures'].index(filtered_displayName) not in raw_fishing_toolkit_lures.values():
                account.alerts_AdviceDict['General'].append(Advice(
                    label=f"{filtered_displayName} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayName,
                ))
        elif filtered_displayName in fishingToolkitDict['Lines']:
            if fishingToolkitDict['Lines'].index(filtered_displayName) not in raw_fishing_toolkit_lines.values():
                account.alerts_AdviceDict['General'].append(Advice(
                    label=f"{filtered_displayName} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayName,
                ))

def _calculate_general_highest_world_reached(account):
    if (
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

def _calculate_general_master_classes_grimoire(account):
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
                        next_stack_target = decode_enemy_name(grimoire_coded_stack_monster_order[account.grimoire.get(f'{stack_type} Stacks', '0')])
                    except:
                        next_stack_target = decode_enemy_name(grimoire_coded_stack_monster_order[0])
                account.grimoire['Upgrades'][upgrade_name]['Description'] = account.grimoire['Upgrades'][upgrade_name]['Description'].replace(
                    'Target:$', f"Target: {next_stack_target}"
                )
        account.grimoire['Upgrades'][upgrade_name]['Description'] += (
            f"<br>({account.grimoire['Upgrades'][upgrade_name]['Value Per Level'] * (grimoire_multi if upgrade_details['Scaling Value'] else 1):.2f} per level"
            f"{' after Writhing Grimoire)' if upgrade_details['Scaling Value'] else ': Not scaled by Writhing Grimoire)'}"
        )


def _calculate_w1(account):
    _calculate_w1_upgrade_vault(account)
    _calculate_w1_starsigns(account)
    _calculate_w1_statues(account)

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
    # logger.debug(f"{vault_multi = }")
    for upgrade_name, upgrade_details in account.vault['Upgrades'].items():
        # Update description with total value, stack counts, and scaling info
        if '{' in account.vault['Upgrades'][upgrade_name]['Description']:
            account.vault['Upgrades'][upgrade_name]['Total Value'] = (
                account.vault['Upgrades'][upgrade_name]['Level']
                * account.vault['Upgrades'][upgrade_name]['Value Per Level']
                * (vault_multi[upgrade_details['Vault Section']-1] if upgrade_details['Scaling Value'] else 1)
            )
            account.vault['Upgrades'][upgrade_name]['Description'] = account.vault['Upgrades'][upgrade_name]['Description'].replace(
                '{', f"{account.vault['Upgrades'][upgrade_name]['Total Value']}"
            )
        if '}' in account.vault['Upgrades'][upgrade_name]['Description']:
            account.vault['Upgrades'][upgrade_name]['Total Value'] = ValueToMulti(
                account.vault['Upgrades'][upgrade_name]['Level']
                * account.vault['Upgrades'][upgrade_name]['Value Per Level']
                * (vault_multi[upgrade_details['Vault Section']-1] if upgrade_details['Scaling Value'] else 1)
            )
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
                        next_stack_target = decode_enemy_name(grimoire_coded_stack_monster_order[account.vault.get(f'{stack_type} Stacks', '0')])
                    except:
                        next_stack_target = decode_enemy_name(grimoire_coded_stack_monster_order[0])
                account.vault['Upgrades'][upgrade_name]['Description'] = account.vault['Upgrades'][upgrade_name]['Description'].replace(
                    'Target:&', f"Target: {next_stack_target}"
                )
        account.vault['Upgrades'][upgrade_name]['Description'] += (
            f"<br>({account.vault['Upgrades'][upgrade_name]['Value Per Level'] * (vault_multi[upgrade_details['Vault Section']-1] if upgrade_details['Scaling Value'] else 1):.2f} per level"
            f"{' after Vault Mastery ' if upgrade_details['Scaling Value'] else ': Not scaled by Vault Mastery '}"
            f"{upgrade_details['Vault Section']}"
            f")"
        )

def _calculate_w1_starsigns(account):
    account.star_sign_extras['SeraphMulti'] = min(3, 1.1 ** ceil((max(account.all_skills['Summoning'], default=0) + 1) / 20))
    account.star_sign_extras['SeraphGoal'] = min(220, ceilUpToBase(max(account.all_skills['Summoning'], default=0), 20))
    min_level_stacks = ceil((min(account.all_skills['Summoning'], default=0) + 1) / 20)
    max_level_stacks = ceil((max(account.all_skills['Summoning'], default=0) + 1) / 20)
    inequality_notice = ' (Note: Some characters lower leveled)' if min_level_stacks != max_level_stacks else ''
    if bool(account.star_signs.get("Seraph Cosmos", {}).get('Unlocked', False)):
        account.star_sign_extras['SeraphEval'] = f"Multis signs by {account.star_sign_extras['SeraphMulti']:.2f}x."
    else:
        account.star_sign_extras['SeraphEval'] = f"Locked. Would increase other signs by {account.star_sign_extras['SeraphMulti']:.2f}x if unlocked.{inequality_notice}"
        account.star_sign_extras['SeraphMulti'] = 1
    if account.star_sign_extras['SeraphGoal'] < 240:
        account.star_sign_extras['SeraphEval'] += f" Increases every 20 Summoning levels.{inequality_notice}"
    account.star_sign_extras['SeraphAdvice'] = Advice(
        label=f"{{{{ Star Sign|#star-signs }}}}: Seraph Cosmos: {account.star_sign_extras['SeraphEval']}",
        picture_class="seraph-cosmos",
        progression=max(account.all_skills['Summoning'], default=0),
        goal=account.star_sign_extras['SeraphGoal'])

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

def _calculate_w1_statues(account):
    voodooStatuficationMulti = []
    for char in account.safe_characters:
        if char.class_name == "Voidwalker":
            voodooStatuficationMulti.append(
                lavaFunc(
                    'decay',
                    char.max_talents_over_books + char.max_talents.get("56", 0),
                    200,
                    200
                )
            )
    voodooStatuficationMulti = 1 + max(voodooStatuficationMulti, default=0)

    onyxMulti = 2 + 0.3 * account.sailing['Artifacts'].get('The Onyx Lantern', {}).get('Level', 0)

    for statueName, statueDetails in account.statues.items():
        if statueDetails['Type'] == "Onyx":
            account.statues[statueName]["Value"] *= onyxMulti
        account.statues[statueName]["Value"] *= voodooStatuficationMulti

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
            if account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']:
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
    account.postOffice["Total Boxes Earned"] = (
            account.postOffice['Completing Orders']
            + account.postOffice['Streak Bonuses']
            + account.postOffice['Miscellaneous']
    )
    
def _calculate_w2_ballot(account):
    account.event_points_shop['BonusMulti'] = ValueToMulti(
        account.equinox_bonuses['Voter Rights']['CurrentLevel']
        + account.caverns['Majiks']['Voter Integrity']['Value']
        + account.summoning['Endless Bonuses']["% Ballot Bonus"]
        + (17 * account.event_points_shop['Bonuses']['Gilded Vote Button']['Owned'])
    )
    for buffIndex, buffValuesDict in account.ballot['Buffs'].items():
        account.ballot['Buffs'][buffIndex]['Value'] *= account.event_points_shop['BonusMulti']
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
    account.islands['Trash Island']['Skelefish Stamp']['Unlocked'] = account.stamps['Skelefish Stamp']['Delivered'] or account.stored_assets.get('StampB47').amount > 0
    account.islands['Trash Island']['Amplestample Stamp']['Unlocked'] = account.stamps['Amplestample Stamp']['Delivered'] or account.stored_assets.get('StampB32').amount > 0
    account.islands['Trash Island']['Golden Sixes Stamp']['Unlocked'] = account.stamps['Golden Sixes Stamp']['Delivered'] or account.stored_assets.get('StampA38').amount > 0
    account.islands['Trash Island']['Stat Wallstreet Stamp']['Unlocked'] = account.stamps['Stat Wallstreet Stamp']['Delivered'] or account.stored_assets.get('StampA39').amount > 0
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
    _calculate_w3_collider_base_costs(account)
    _calculate_w3_collider_cost_reduction(account)
    _calculate_w3_shrine_values(account)
    _calculate_w3_shrine_advices(account)

def _calculate_w3_building_max_levels(account):
    # Placed towers here since it's used for both Construction mastery and atom levels
    towers = [towerName for towerName, towerValuesDict in account.construction_buildings.items() if towerValuesDict['Type'] == 'Tower']
    if account.rift['SkillMastery']:
        totalLevel = sum(account.all_skills['Construction'])
        if totalLevel >= 500:
            account.construction_buildings["Trapper Drone"]['MaxLevel'] += 35

        if totalLevel >= 1000:
            account.construction_buildings["Talent Book Library"]['MaxLevel'] += 100

        if totalLevel >= 1500:
            shrines = [shrineName for shrineName, shrineValuesDict in account.construction_buildings.items() if shrineValuesDict['Type'] == 'Shrine']
            for shrineName in shrines:
                try:
                    account.construction_buildings[shrineName]['MaxLevel'] += 30
                except:
                    continue

        if totalLevel >= 2500:
            for towerName in towers:
                try:
                    account.construction_buildings[towerName]['MaxLevel'] += 30
                except:
                    continue

    if account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'] > 0:
        for towerName in towers:
            try:
                account.construction_buildings[towerName]['MaxLevel'] += 2 * account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level']
            except:
                continue

def _calculate_w3_collider_base_costs(account):
    #Formula for base cost: (AtomInfo[3] + AtomInfo[1] * AtomCurrentLevel) * POWER(AtomInfo[2], AtomCurrentLevel)
    for atomName, atomValuesDict in account.atom_collider['Atoms'].items():
        #Update max level from 20 to 30, if Isotope Discovery unlocked
        if account.gaming['SuperBits']['Isotope Discovery']['Unlocked']:
            account.atom_collider['Atoms'][atomName]['MaxLevel'] += 10

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
    account.atom_collider['CostReductionMax'] = ValueToMulti(
        7 * 4  #Max merit
        + 1 * 20  #Max Atom Collider building
        + 1 * 30  #Max Neon
        + 10  #Superbit
        + 14  #Atom Split bubble
        + 20  #Stamp
    )
    account.atom_collider['CostReductionRaw'] = ValueToMulti(
        7 * account.merits[4][6]['Level']
        + (account.construction_buildings['Atom Collider']['Level'] / 10)
        + 1 * account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']
        + 10 * account.gaming['SuperBits']['Atom Redux']['Unlocked']
        + account.alchemy_bubbles['Atom Split']['BaseValue']
        + account.stamps['Atomic Stamp']['Value']
    )
    account.atom_collider['CostReductionMulti'] = 1 / account.atom_collider['CostReductionRaw']
    account.atom_collider['CostReductionMulti1Higher'] = 1 / (account.atom_collider['CostReductionRaw'] + 0.01)
    account.atom_collider['CostDiscount'] = (1 - (1 / account.atom_collider['CostReductionRaw'])) * 100
    account.atom_collider['CostDiscountMax'] = (1 - (1 / account.atom_collider['CostReductionMax'])) * 100

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
        if account.sneaking['JadeEmporium']["Sovereign Artifacts"]['Obtained']:
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
    if account.sneaking['JadeEmporium']["Papa Blob's Quality Guarantee"]['Obtained']:
        account.cooking['PlayerMaxPlateLvl'] += 10
    else:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Purchase \"Papa Blob's Quality Guarantee\" from {{ Jade Emporium|#sneaking }}",
            "papa-blobs-quality-guarantee",
            0,
            1
        ))
    if account.sneaking['JadeEmporium']["Chef Geustloaf's Cutting Edge Philosophy"]['Obtained']:
        account.cooking['PlayerMaxPlateLvl'] += 10
    else:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Purchase \"Chef Geustloaf's Cutting Edge Philosophy\" from {{ Jade Emporium|#sneaking }}",
            "chef-geustloafs-cutting-edge-philosophy",
            0,
            1
        ))
    account.cooking['PlayerMaxPlateLvl'] += account.grimoire['Upgrades']['Supreme Head Chef Status']['Level']
    if account.grimoire['Upgrades']['Supreme Head Chef Status']['Level'] < account.grimoire['Upgrades']['Supreme Head Chef Status']['Max Level']:
        account.cooking['PlayerMissingPlateUpgrades'].append((
            "Upgrade \"Supreme Head Chef Status\" within {{ The Grimoire|#the-grimoire }}",
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Image'],
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Level'],  #progress
            account.grimoire['Upgrades']['Supreme Head Chef Status']['Max Level']  #goal
        ))

    account.cooking['CurrentRemainingMeals'] = account.cooking['MaxTotalMealLevels'] - account.cooking['PlayerTotalMealLevels']
    account.cooking['MaxRemainingMeals'] = (maxMealCount * maxMealLevel) - account.cooking['PlayerTotalMealLevels']
    account.cooking['NMLBDays'] = sum([
        ceil((maxMealLevel - meal_details['Level']) / 3) for meal_details in account.meals.values()
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
    mealMulti = (
        ValueToMulti(
            (account.labJewels['Black Diamond Rhinestone']['Value'] * account.labJewels['Black Diamond Rhinestone']['Enabled'])
            + account.breeding['Total Shiny Levels']['Bonuses from All Meals']
        )
        * account.summoning['Endless Bonuses']['x Meal Bonuses']
    )
    for meal in account.meals:
        # _customBlock_Summoning > "RibbonBonus": 1 + Math.floor(5 * t + Math.floor(t / 2) * (4 + 6.5 * Math.floor(t / 5))) / 100;
        # Last verified as of v2.30 Companion Trading
        account.meals[meal]['RibbonMulti'] = ValueToMulti(floor(
            5 * account.meals[meal]['RibbonTier'] + floor(account.meals[meal]['RibbonTier'] / 2) * (4 + 6.5 * floor(account.meals[meal]['RibbonTier'] / 5))
        ))
        account.meals[meal]['Value'] = float(account.meals[meal]['Value']) * mealMulti * account.meals[meal]['RibbonMulti']
        if '{' in account.meals[meal]['Effect']:
            account.meals[meal]['Description'] = account.meals[meal]['Effect'].replace('{', f"{account.meals[meal]['Value']:.3f}")
        elif '}' in account.meals[meal]['Effect']:
            account.meals[meal]['Description'] = account.meals[meal]['Effect'].replace('}', f"{account.meals[meal]['Value']:.3f}")
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
    account.labBonuses['No Bubble Left Behind']['Value'] = min(nblbMaxBubbleCount, account.labBonuses['No Bubble Left Behind']['Value'])

def _calculate_w5(account):
    account.divinity['AccountWideArctis'] = account.doot_owned or 'Arctis' in account.caverns['PocketDivinityLinks']
    _calculate_w5_divinity_offering_costs(account)

def _calculate_w5_divinity_offering_costs(account):
    DivCostAfter3 = safer_get(account.raw_serverVars_dict, "DivCostAfter3", divinity_DivCostAfter3)
    account.divinity['LowOfferingGoal'] = divinityUpgradeCost(DivCostAfter3, account.divinity['LowOffering'], account.divinity['GodsUnlocked'] + account.divinity['GodRank'])
    account.divinity['HighOfferingGoal'] = divinityUpgradeCost(DivCostAfter3, account.divinity['HighOffering'], account.divinity['GodsUnlocked'] + account.divinity['GodRank'])

def divinityUpgradeCost(DivCostAfter3, offeringIndex, unlockedDivinity):
    try:
        cost = (20 * safer_math_pow(unlockedDivinity + 1.3, 2.3) * safer_math_pow(2.2, unlockedDivinity) + 60) * divinity_offeringsDict.get(offeringIndex, {}).get("Chance", 1) / 100
        if unlockedDivinity >= 3:
            cost = cost * safer_math_pow(min(1.8, max(1, 1 + DivCostAfter3 / 100)), unlockedDivinity - 2)
        return ceil(cost)
    except OverflowError:
        logger.exception(f"Could not calc Divinity Offering cost. Probably a cheater with a ridiculous number of Unlocked Divinity: {unlockedDivinity}")
        return 1e100

def _calculate_caverns(account):
    #_calculate_caverns_majiks(account)
    _calculate_caverns_measurements_base(account)
    _calculate_caverns_measurements_multis(account)
    _calculate_caverns_studies(account)
    _calculate_caverns_the_well(account)
    _calculate_caverns_monuments(account)
    _calculate_caverns_the_bell(account)
    _calculate_caverns_the_harp(account)

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
        except:
            logger.exception(f"Failed to calculate Measurement Base Value for {measurement_values['Description']}")
            account.caverns['Measurements'][measurement_index]['BaseValue'] = 0

def _calculate_caverns_measurements_multis(account):
    # _customBlock_Holes > "MeasurementMulti"  #Last verified as of 2.30 Companion Trading
    total_skill_levels = 0
    for skill, skill_levels in account.all_skills.items():
        total_skill_levels += sum(skill_levels) if skill != 'Combat' else 0
    fake_multi = total_skill_levels / 5000 + max(0, (total_skill_levels - 18000) / 1500)
    if 5 > fake_multi:
        real_multi = 1 + (18 * fake_multi / 100)
    else:
        real_multi = 1 + (18 * fake_multi + 8 * (fake_multi - 5)) / 100
    account.caverns['Measurements'][1]['Value'] = (
        2 * account.caverns['Measurements'][1]['Level']
        * account.caverns['Majiks']['Lengthmeister']['Value']
        * real_multi
    )

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
                max_level = infinity_string
                base_note = f"<br>{base_value} base +{study_details['ScalingValue']} per level"
            case _:
                total_value = study_details['Level'] * study_details['ScalingValue']
                max_level = infinity_string
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

def _calculate_caverns_monuments_bravery(account):
    monument_name = 'Bravery Monument'
    account.caverns['Caverns'][monument_name]['Sword Count'] = (
        min(9, 3  # Starting amount
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
    account.caverns['Caverns'][monument_name]['Max Coins'] = infinity_string
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



def _calculate_w6(account):
    _calculate_w6_farming(account)

def _calculate_w6_farming(account):
    _calculate_w6_farming_crop_depot(account)
    _calculate_w6_farming_markets(account)
    _calculate_w6_farming_crop_value(account)
    _calculate_w6_farming_crop_evo(account)
    _calculate_w6_farming_crop_speed(account)
    _calculate_w6_farming_bean_bonus(account)
    _calculate_w6_farming_og(account)

def _calculate_w6_farming_crop_depot(account):
    lab_multi = ValueToMulti(
        (account.labBonuses['Depot Studies PhD']['Value'] + account.labJewels['Pure Opal Rhombol']['Value']) * account.labBonuses['Depot Studies PhD']['Enabled']
    )
    grimoire_multi = account.grimoire['Upgrades']['Superior Crop Research']['Total Value']  #Grimoire 22: Superior Crop Research already a Multi
    for bonusName, bonusDetails in account.farming['Depot'].items():
        account.farming['Depot'][bonusName]['Value'] = account.farming['Depot'][bonusName]['BaseValue'] * lab_multi * grimoire_multi
        account.farming['Depot'][bonusName]['ValuePlus1'] = account.farming['Depot'][bonusName]['BaseValuePlus1'] * lab_multi * grimoire_multi

def _calculate_w6_farming_markets(account):
    super_multi_current_stacks = ValueToMulti(account.farming['MarketUpgrades']['Super Gmo']['Value'] * account.farming['CropStacks']['Super Gmo'])
    #super_multi_max_stacks = ValueToMulti(account.farming['MarketUpgrades']['Super Gmo']['Value'] * maxFarmingCrops)
    #logger.debug(f"models._calculate_w6_farming_day_market super_multi = {super_multi}")
    for name, details in account.farming['MarketUpgrades'].items():
        try:
            if "}" in details['Description']:  #Multiplicative
                val = ValueToMulti(details['Value'])
                account.farming['MarketUpgrades'][name]['Description'] = details['Description'].replace("}", f"{val:.3g}")
            else:
                account.farming['MarketUpgrades'][name]['Description'] = details['Description'].replace("{", f"{details['Value']:g}")
            if name in account.farming['CropStacks']:
                if name == 'Super Gmo':
                    account.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks
                    account.farming['MarketUpgrades'][name]['Description'] += (
                        f".<br>{account.farming['CropStacks'][name]} stacks = "
                        f"{super_multi_current_stacks:,.4g}x"
                    )
                elif name == 'Evolution Gmo':
                    account.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks * safer_math_pow(ValueToMulti(details['Value']), account.farming['CropStacks'][name])
                    account.farming['MarketUpgrades'][name]['Description'] += (
                        f".<br>{account.farming['CropStacks'][name]} stacks = "
                        f"{account.farming['MarketUpgrades'][name]['StackedValue']:,.4g}x"
                    )
                else:
                    account.farming['MarketUpgrades'][name]['StackedValue'] = super_multi_current_stacks * (ValueToMulti(details['Value'] * account.farming['CropStacks'][name]))
                    account.farming['MarketUpgrades'][name]['Description'] += (
                        f".<br>{account.farming['CropStacks'][name]} stacks = "
                        f"{account.farming['MarketUpgrades'][name]['StackedValue']:,.5g}x"
                    )
        except:
            logger.exception(f"Exception substituting value for {name}")
            continue

def _calculate_w6_farming_crop_value(account):
    #if ("CropsBonusValue" == e)
    #return Math.min(100, Math.round(Math.max(1, Math.floor(1 + (c.randomFloat() + q._customBlock_FarmingStuffs("BasketUpgQTY", 0, 5) / 100))) * (1 + q._customBlock_FarmingStuffs("LandRankUpgBonusTOTAL", 1, 0) / 100) * (1 + (q._customBlock_FarmingStuffs("LankRankUpgBonus", 1, 0) * c.asNumber(a.engine.getGameAttribute("FarmRank")[0][0 | t]) + q._customBlock_Summoning("VotingBonusz", 29, 0)) / 100)));
    account.farming['Value'] = {}
    account.farming['Value']['Doubler Multi'] = floor(ValueToMulti(account.farming['MarketUpgrades']['Product Doubler']['Value']))
    account.farming['Value']['Mboost Sboost Multi'] = ValueToMulti(
        account.farming['LandRankDatabase']['Production Megaboost']['Value'] + account.farming['LandRankDatabase']['Production Superboost']['Value']
    )
    account.farming['Value']['Value GMO Current'] = account.farming['MarketUpgrades']['Value Gmo']['StackedValue']

    #Calculate with the Min Plot Rank
    account.farming['Value']['Pboost Ballot Multi Min'] = ValueToMulti(
        (account.farming['LandRankDatabase']['Production Boost']['Value']) * account.farming.get('LandRankMinPlot', 0)  #Value of PBoost * Lowest Plot Rank
        + (account.ballot['Buffs'][29]['Value'] * int(account.ballot['CurrentBuff'] == 29))  #Plus value of Ballot Buff * Active status
    )
    account.farming['Value']['BeforeCapMin'] = round(
        max(1, account.farming['Value']['Doubler Multi'])  #end of max
        * account.farming['Value']['Mboost Sboost Multi']
        * account.farming['Value']['Pboost Ballot Multi Min']
        * account.farming['Value']['Value GMO Current']
        )  #end of round

    #Now calculate with the Max Plot Rank
    account.farming['Value']['Pboost Ballot Multi Max'] = ValueToMulti(
        (account.farming['LandRankDatabase']['Production Boost']['Value']) * account.farming.get('LandRankMaxPlot', 0)  # Value of PBoost * Highest Plot Rank
        + (account.ballot['Buffs'][29]['Value'] * int(account.ballot['CurrentBuff'] == 29))  # Plus value of Ballot Buff * Active status
    )
    account.farming['Value']['BeforeCapMax'] = round(
        max(1, account.farming['Value']['Doubler Multi'])  # end of max
        * account.farming['Value']['Mboost Sboost Multi']
        * account.farming['Value']['Pboost Ballot Multi Max']
        * account.farming['Value']['Value GMO Current']
    )  # end of round
    account.farming['Value']['FinalMin'] = min(maxFarmingValue, account.farming['Value']['BeforeCapMin'])
    account.farming['Value']['FinalMax'] = min(maxFarmingValue, account.farming['Value']['BeforeCapMax'])
    #logger.debug(f"models._calculate_w6_farming_crop_value CropValue BEFORE cap = {account.farming['Value']['BeforeCap']}")
    #logger.debug(f"models._calculate_w6_farming_crop_value CropValue AFTER cap = {account.farming['Value']['Final']}")

def _calculate_w6_farming_crop_evo(account):
    # Alchemy
    account.farming['Mama Trolls Unlocked'] = False
    account.farming['Evo'] = {}
    account.farming['Evo']['Maps Opened'] = 0
    for char in account.all_characters:
        for mapIndex in range(251, 264):  # Clearing the fake portal at Samurai Guardians doesn't count
            try:
                if int(float(char.kill_dict.get(mapIndex, [1])[0])) <= 0:
                    account.farming['Evo']['Maps Opened'] += 1
                    if mapIndex == 257 and not account.farming['Mama Trolls Unlocked']:
                        account.farming['Mama Trolls Unlocked'] = True
            except:
                continue
    account.farming['Evo']['Cropius Final Value'] = account.farming['Evo']['Maps Opened'] * account.alchemy_bubbles['Cropius Mapper']['BaseValue']
    account.farming['Evo']['Vial Value'] = account.alchemy_vials['Flavorgil (Caulifish)']['Value']
    account.farming['Evo']['Alch Multi'] = (
        ValueToMulti(account.farming['Evo']['Cropius Final Value'])
        # * ValueToMulti(session_data.account.alchemy_bubbles['Crop Chapter']['BaseValue'])
        * ValueToMulti(account.farming['Evo']['Vial Value'])
    )
    # Stamp
    account.farming['Evo']['Stamp Value'] = (
            max(1, 2 * account.labBonuses['Certified Stamp Book']['Enabled'])
            * max(1, 1.25 * account.sneaking['PristineCharms']['Liqorice Rolle']['Obtained'])
            * account.stamps['Crop Evo Stamp']['Value']
    )
    account.farming['Evo']['Stamp Multi'] = ValueToMulti(account.farming['Evo']['Stamp Value'])
    # Meals
    account.farming['Evo']['Nyan Stacks'] = ceil((max(account.all_skills['Summoning'], default=0) + 1) / 50)
    account.farming['Evo']['Meals Multi'] = (
            ValueToMulti(account.meals['Bill Jack Pepper']['Value'])
            * ValueToMulti(account.meals['Nyanborgir']['Value'] * account.farming['Evo']['Nyan Stacks'])
    )
    # Markets
    account.farming['Evo']['Farm Multi'] = ValueToMulti(account.farming['MarketUpgrades']['Biology Boost']['Value']) * account.farming['MarketUpgrades']['Evolution Gmo']['StackedValue']
    # Land Ranks
    account.farming['Evo']['LR Multi'] = (
            ValueToMulti(account.farming['LandRankDatabase']['Evolution Boost']['Value'] * account.farming['LandRankMinPlot'])
            * ValueToMulti(account.farming['LandRankDatabase']['Evolution Megaboost']['Value'])
            * ValueToMulti(account.farming['LandRankDatabase']['Evolution Superboost']['Value'])
            * ValueToMulti(account.farming['LandRankDatabase']['Evolution Ultraboost']['Value'])
    )
    # Summoning
    account.farming['Evo']['Summ Battles'] = {
        'Yellow': [9],
        'Blue': [14],
        'Red': [5]
    }
    battle_reward_total = 0
    for color, battlesList in account.farming['Evo']['Summ Battles'].items():
        for battle in battlesList:
            if account.summoning['Battles'][color] >= battle:
                battle_reward_total += account.summoning["BattleDetails"][color][battle]['RewardBaseValue']
    account.farming['Evo']['Summon Multi'] = ValueToMulti(account.summoning['WinnerBonusesMultiFull'] * battle_reward_total)
    # Starsign
    account.farming['Evo']['Starsign Final Value'] = (
            3 * account.star_signs['Cropiovo Minor']['Unlocked']
            * max(account.all_skills['Farming'], default=0)
            * account.star_sign_extras['SilkrodeNanoMulti']
            * account.star_sign_extras['SeraphMulti']
    )
    account.farming['Evo']['SS Multi'] = ValueToMulti(account.farming['Evo']['Starsign Final Value'])
    # Misc
    account.farming['Evo']['Total Farming Levels'] = sum(account.all_skills['Farming'])
    account.farming['Evo']['Skill Mastery Bonus Bool'] = account.rift['SkillMastery'] and account.farming['Evo']['Total Farming Levels'] >= 300
    account.farming['Evo']['Ballot Active'] = account.ballot['CurrentBuff'] == 29
    if account.farming['Evo']['Ballot Active']:
        account.farming['Evo']['Ballot Status'] = "is Active"
    elif not account.farming['Evo']['Ballot Active'] and account.ballot['CurrentBuff'] != 0:
        account.farming['Evo']['Ballot Status'] = "is Inactive"
    else:
        account.farming['Evo']['Ballot Status'] = "status is not available in provided data"
    account.farming['Evo']['Ballot Multi Max'] = ValueToMulti(account.ballot['Buffs'][29]['Value'])
    account.farming['Evo']['Ballot Multi Current'] = max(1, account.farming['Evo']['Ballot Multi Max'] * account.farming['Evo']['Ballot Active'])
    account.farming['Evo']['Misc Multi'] = (
            ValueToMulti(5 * account.achievements["Lil' Overgrowth"]['Complete'])
            * account.killroy_skullshop['Crop Multi']
            * ValueToMulti(15 * account.farming['Evo']['Skill Mastery Bonus Bool'] * account.rift['SkillMastery'])
            * account.farming['Evo']['Ballot Multi Current']
    )
    account.farming['Evo']['Wish Multi'] = ValueToMulti(account.caverns['Caverns']['The Lamp']['WishTypes'][8]['BonusList'][0])
    # subtotal doesn't include Crop Chapter
    account.farming['Evo']['Subtotal Multi'] = (
        account.farming['Evo']['Alch Multi']
        * account.farming['Evo']['Stamp Multi']
        * account.farming['Evo']['Meals Multi']
        * account.farming['Evo']['Farm Multi']
        * account.farming['Evo']['LR Multi']
        * account.farming['Evo']['Summon Multi']
        * account.farming['Evo']['SS Multi']
        * account.farming['Evo']['Misc Multi']
        * account.farming['Evo']['Wish Multi']
    )

def _calculate_w6_farming_crop_speed(account):
    account.farming['Speed'] = {}
    # Summoning
    account.farming['Speed']['Summ Battles'] = {
        'White': [3, 9],
        'Green': [7, 13],
        'Yellow': [7],
        'Purple': [4],
        'Red': [10],
        'Cyan': [12]
    }
    battle_reward_total = 0
    for color, battlesList in account.farming['Speed']['Summ Battles'].items():
        for battle in battlesList:
            if account.summoning['Battles'][color] >= battle:
                battle_reward_total += account.summoning["BattleDetails"][color][battle]['RewardBaseValue']
    account.farming['Speed']['Summon Multi'] = ValueToMulti(account.summoning['WinnerBonusesMultiFull'] * battle_reward_total)
    # Vial and Day Market
    account.farming['Speed']['Vial Value'] = account.alchemy_vials['Ricecakorade (Rice Cake)']['Value']
    account.farming['Speed']['VM Multi'] = ValueToMulti(account.farming['Speed']['Vial Value'] + account.farming['MarketUpgrades']['Nutritious Soil']['Value'])
    # Night Market
    account.farming['Speed']['NM Multi'] = account.farming['MarketUpgrades']['Speed Gmo']['StackedValue']
    # Total
    account.farming['Speed']['Total Multi'] = account.farming['Speed']['Summon Multi'] * account.farming['Speed']['VM Multi'] * account.farming['Speed']['NM Multi']

def _calculate_w6_farming_bean_bonus(account):
    account.farming['Bean'] = {}
    account.farming['Bean']['mga'] = ValueToMulti(account.farming['MarketUpgrades']['More Beenz']['Value'])
    account.farming['Bean']['mgb'] = ValueToMulti(
        (25 * account.sneaking['JadeEmporium']['Deal Sweetening']['Obtained'])
        + (5 * account.achievements['Crop Flooding']['Complete'])
    )
    account.farming['Bean']['Total Multi'] = account.farming['Bean']['mga'] * account.farming['Bean']['mgb']

def _calculate_w6_farming_og(account):
    # Fun calculations
    account.farming['OG'] = {}
    account.farming['OG']['Ach Multi'] = ValueToMulti(15 * account.achievements['Big Time Land Owner']['Complete'])
    account.farming['OG']['Starsign Final Value'] = (
            15 * account.star_signs['O.G. Signalais']['Unlocked']
            * account.star_sign_extras['SilkrodeNanoMulti']
            * account.star_sign_extras['SeraphMulti']
    )
    account.farming['OG']['SS Multi'] = ValueToMulti(account.farming['OG']['Starsign Final Value'])
    account.farming['OG']['NM Multi'] = ValueToMulti(account.farming['MarketUpgrades']['Og Fertilizer']['Value'])
    account.farming['OG']['Merit Multi'] = ValueToMulti(2 * account.merits[5][2]['Level'])
    account.farming['OG']['LR Multi'] = (ValueToMulti(
        account.farming['LandRankDatabase']['Overgrowth Boost']['Value']
        + account.farming['LandRankDatabase']['Overgrowth Megaboost']['Value']
        + account.farming['LandRankDatabase']['Overgrowth Superboost']['Value']
    ))
    account.farming['OG']['Pristine Multi'] = ValueToMulti(50 * account.sneaking['PristineCharms']['Taffy Disc']['Obtained'])
    account.farming['OG']['Total Multi'] = (
            account.farming['OG']['Ach Multi']
            * account.farming['OG']['SS Multi']
            * account.farming['OG']['NM Multi']
            * account.farming['OG']['Merit Multi']
            * account.farming['OG']['LR Multi']
            * account.farming['OG']['Pristine Multi']
    )

def _calculate_wave_3(account):
    _calculate_w3_library_max_book_levels(account)
    _calculate_w3_equinox_max_levels(account)
    _calculate_general_character_over_books(account)
    _calculate_general_crystal_spawn_chance(account)

def _calculate_w3_library_max_book_levels(account):
    account.library['StaticSum'] = (
        0
        + (25 * (0 < account.construction_buildings['Talent Book Library']['Level']))
        + (5 * account.achievements['Checkout Takeout']['Complete'])
        + (10 * (0 < account.atom_collider['Atoms']['Oxygen - Library Booker']['Level']))
        + (25 * account.sailing['Artifacts'].get('Fury Relic', {}).get('Level', 0))
    )
    account.library['ScalingSum'] = (
        0
        + 2 * account.merits[2][2]['Level']
        + 2 * account.saltlick.get('Max Book', 0)
    )
    # summGroupA = (1 + (.25 * account.sailing['Artifacts'].get('The Winz Lantern', {}).get('Level', 0))
    #               + .01 * account.merits[5][4]['Level']
    #               + .01 * (0 < account.achievements.get('Spectre Stars', False))
    #               + .01 * (0 < account.achievements.get('Regalis My Beloved', False))
    #               )
    # summGroupB = 1 + (.3 * account.sneaking.get('PristineCharms', {}).get('Crystal Comb', 0))
    account.library['SummoningSum'] = round(
        10.5 * (account.summoning['Battles']['Cyan'] >= 14)
        * account.summoning['WinnerBonusesMultiPartial']
    )
    account.library['MaxBookLevel'] = 100 + account.library['StaticSum'] + account.library['ScalingSum'] + account.library['SummoningSum']

def _calculate_w3_equinox_max_levels(account):
    bonus_equinox_levels = account.summoning['Endless Bonuses'].get('+ Equinox Max LV', 0)
    if bonus_equinox_levels > 0:
        for bonus, bonus_details in account.equinox_bonuses.items():
            if bonus_details['SummoningExpands']:
                account.equinox_bonuses[bonus]['PlayerMaxLevel'] += bonus_equinox_levels
                account.equinox_bonuses[bonus]['FinalMaxLevel'] += bonus_equinox_levels

def _calculate_general_character_over_books(account):
    account.bonus_talents = {
        "Rift Slug": {
            "Value": 25 * account.riftslug_owned,
            "Image": "rift-slug",
            "Label": f"Companion: Rift Slug: "
                     f"+{25 * account.riftslug_owned}/25",
            "Progression": 1 if account.riftslug_owned else 0,
            "Goal": 1
        },
        "ES Family": {
            "Value": floor(account.family_bonuses["Elemental Sorcerer"]['Value']),
            "Image": 'elemental-sorcerer-icon',
            "Label": f"ES Family Bonus: "
                     f"+{floor(account.family_bonuses['Elemental Sorcerer']['Value'])}.<br>"
                     f"Next increase at Class Level: ",
            "Progression": account.family_bonuses['Elemental Sorcerer']['Level'],
            "Goal": getNextESFamilyBreakpoint(account.family_bonuses['Elemental Sorcerer']['Level'])
        },
        "Equinox Symbols": {
            "Value": account.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
            "Image": 'equinox-symbols',
            "Label": f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: "
                     f"+{account.equinox_bonuses['Equinox Symbols']['CurrentLevel']}/{account.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']}",
            "Progression": account.equinox_bonuses['Equinox Symbols']['CurrentLevel'],
            "Goal": account.equinox_bonuses['Equinox Symbols']['FinalMaxLevel']
        },
        "Maroon Warship": {
            "Value": 1 * account.achievements['Maroon Warship']['Complete'],
            "Image": "maroon-warship",
            "Label": f"W5 Achievement: Maroon Warship: "
                     f"+{1 * account.achievements['Maroon Warship']['Complete']}/1",
            "Progression": 1 if account.achievements['Maroon Warship']['Complete'] else 0,
            "Goal": 1
        },
        "Sneaking Mastery": {
            "Value": 5 if account.sneaking['MaxMastery'] >= 3 else 0,
            "Image": "sneaking-mastery",
            "Label": f"{{{{ Rift|#rift }}}}: Sneaking Mastery: "
                     f"+{5 if account.sneaking['MaxMastery'] >= 3 else 0}/5 (Mastery III)",
            "Progression": account.sneaking['MaxMastery'],
            "Goal": 3
        },
    }
    account.bonus_talents_account_wide_sum = 0
    for bonusName, bonusValuesDict in account.bonus_talents.items():
        try:
            account.bonus_talents_account_wide_sum += bonusValuesDict.get('Value', 0)
        except:
            continue

    for char in account.safe_characters:
        character_specific_bonuses = 0

        # Arctis minor link
        if account.divinity['AccountWideArctis'] or char.isArctisLinked():
            arctis_base = 15
            bigp_value = account.alchemy_bubbles['Big P']['BaseValue']
            div_minorlink_value = char.divinity_level / (char.divinity_level + 60)
            final_result = ceil(arctis_base * bigp_value * div_minorlink_value)
            character_specific_bonuses += ceil(arctis_base * account.alchemy_bubbles['Big P']['BaseValue'] * (char.divinity_level / (char.divinity_level + 60)))

        # Symbols of Beyond = 1 + 1 per 20 levels
        if any([elite in char.all_classes for elite in ["Blood Berserker", "Divine Knight"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("149", 0) // 20)  # Symbols of Beyond - Red
        elif any([elite in char.all_classes for elite in ["Siege Breaker", "Beast Master"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("374", 0) // 20)  # Symbols of Beyond - Green
        elif any([elite in char.all_classes for elite in ["Elemental Sorcerer", "Bubonic Conjuror"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("539", 0) // 20)  # Symbols of Beyond - Purple
        character_specific_bonuses += char.symbols_of_beyond

        char.max_talents_over_books = account.library['MaxBookLevel'] + account.bonus_talents_account_wide_sum + character_specific_bonuses

        # If they're an ES, use max level of Family Guy to calculate floor(ES Family Value * Family Guy)
        if char.class_name == "Elemental Sorcerer":
            try:
                #TODO: Move one-off talent value calculation
                family_guy_bonus = lavaFunc(
                    'decay',
                    char.max_talents_over_books + char.max_talents.get("374", 0),
                    40,
                    100
                )
                family_guy_multi = ValueToMulti(family_guy_bonus)
                char.max_talents_over_books += floor((account.family_bonuses["Elemental Sorcerer"]['Value'] * family_guy_multi) - account.family_bonuses["Elemental Sorcerer"]['Value'])
                char.setFamilyGuyBonus(
                    floor(account.family_bonuses["Elemental Sorcerer"]['Value'] * family_guy_multi)
                    - floor(account.family_bonuses["Elemental Sorcerer"]['Value']))
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
        * ValueToMulti(account.stamps['Crystallin']['Value'])
        * ValueToMulti(total_card_chance)
    )

    for char in account.all_characters:
        cmon_out_crystals_multi = max(1, ValueToMulti(lavaFunc(
            'decay',
            char.max_talents_over_books if char.max_talents.get("26", 0) > 0 else 0,  #This is an assumption that Cmon Out Crystals is max booked
            300,
            100
        )))
        crystals_4_dayys_multi = max(1, ValueToMulti(lavaFunc(
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
