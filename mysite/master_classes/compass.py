from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed, safer_math_log
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string, compass_dusts_list, compass_path_ordering, compass_upgrades_list, compass_medallions, lavaFunc, ValueToMulti,
    arcade_max_level,
    # compass_progressionTiers
)
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    compass_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(compass_progressionTiers.keys(), default=0) - info_tiers
    tier_Compass = 0

    tiers_ag = AdviceGroup(
        tier=tier_Compass,
        pre_string="Progression Tiers",
        advices=compass_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Compass)
    return tiers_ag, overall_SectionTier, max_tier

def getCompassGeneralInfoAdviceGroup(compass):
    general_advices = []
    general_ag = AdviceGroup(
        tier='',
        pre_string="Compass Currencies",
        advices=general_advices
    )
    general_ag.remove_empty_subgroups()
    return general_ag

def getCompassCurrenciesAdviceGroup(compass):
    currencies_advices = {}

    #Basic Currencies
    currencies_advices['Currencies'] = [
        Advice(
            label=f"{dust_name}: {notateNumber('Basic', compass[f'Dust{dust_index}'], 3)}",
            picture_class=f'compass-dust-{dust_index-1}',
            informational=True,
            completed=True
        ) for dust_index, dust_name in enumerate(compass_dusts_list, start=1)
    ]
    currencies_advices['Currencies'].insert(0, Advice(
        label=f"Total Dusts Collected: {notateNumber('Basic', compass['Total Dust Collected'], 3)}",
        picture_class='dustwalker',
        informational=True,
        completed=True
    ))
    currencies_advices['Currencies'].insert(0, Advice(
        label=(
            f"""Daily Top of the Mornin' kills: """
            f"""{compass['Upgrades']["Top of the Mornin'"]['Total Value'] + compass['Upgrades']['Abomination Slayer XII']['Total Value']}"""
            f"""<br>Remaining: {compass["Top of the Mornin'"]}"""
        ),
        picture_class=compass['Upgrades']["Top of the Mornin'"]['Image'],
        progression=compass['Upgrades']["Top of the Mornin'"]['Total Value'] + compass['Upgrades']['Abomination Slayer XII']['Total Value'] - compass["Top of the Mornin'"],
        goal=compass['Upgrades']["Top of the Mornin'"]['Total Value'] + compass['Upgrades']['Abomination Slayer XII']['Total Value'],
        informational=True
    ))

    # Dust Multi calculation groups
    mga_label = f"Group A: {compass['Dust Calc']['mga']:.3f}x"
    currencies_advices[mga_label] = [
        Advice(
            label=f"{compass['Upgrades']['Mountains of Dust']['Path Name']}-{compass['Upgrades']['Mountains of Dust']['Path Ordering']}: "
                  f"Mountains of Dust: <br>{compass['Upgrades']['Mountains of Dust']['Description']}",
            picture_class=compass['Upgrades']['Mountains of Dust']['Image'],
            progression=compass['Upgrades']['Mountains of Dust']['Level'],
            goal=compass['Upgrades']['Mountains of Dust']['Max Level'],
            resource=compass['Upgrades']['Mountains of Dust']['Dust Image'],
        ),
        Advice(
            label=f"{compass['Upgrades']['Solardust Hoarding']['Path Name']}-{compass['Upgrades']['Solardust Hoarding']['Path Ordering']}: "
                  f"Solardust Hoarding: <br>{compass['Upgrades']['Solardust Hoarding']['Description']}"
                  f"<br>{safer_math_log(compass['Dust3'], 'Lava'):.2f} stacks = "
                  f"{compass['Upgrades']['Solardust Hoarding']['Total Value'] * safer_math_log(compass['Dust3'], 'Lava'):.2f}%",
            picture_class=compass['Upgrades']['Solardust Hoarding']['Image'],
            progression=compass['Upgrades']['Solardust Hoarding']['Level'],
            goal=compass['Upgrades']['Solardust Hoarding']['Max Level'],
            resource=compass['Upgrades']['Solardust Hoarding']['Dust Image'],
        ),
    ]

    mgb_label = f"Group B: {compass['Dust Calc']['mgb']:.2f}x"
    currencies_advices[mgb_label] = [
        Advice(
            label=f"{compass['Upgrades']['Spire of Dust']['Path Name']}-{compass['Upgrades']['Spire of Dust']['Path Ordering']}: "
                  f"Spire of Dust: <br>{compass['Upgrades']['Spire of Dust']['Description']}",
            picture_class=compass['Upgrades']['Spire of Dust']['Image'],
            progression=compass['Upgrades']['Spire of Dust']['Level'],
            goal=compass['Upgrades']['Spire of Dust']['Max Level'],
            resource=compass['Upgrades']['Spire of Dust']['Dust Image'],
        ),
    ]

    mgc_label = f"Group C: {compass['Dust Calc']['mgc']:.2f}x"
    currencies_advices[mgc_label] = [
        Advice(
            label=f"{{{{Sneaking|#sneaking}}}}: Pristine Charm: Twinkle Taffy"
                  f"<br>{session_data.account.sneaking['PristineCharms']['Twinkle Taffy']['Bonus']}",
            picture_class=session_data.account.sneaking['PristineCharms']['Twinkle Taffy']['Image'],
            progression=int(session_data.account.sneaking['PristineCharms']['Twinkle Taffy']['Obtained']),
            goal=1
        )
    ]

    mgd_label = f"Group D: {compass['Dust Calc']['mgd']:.2f}x"
    currencies_advices[mgd_label] = [
        Advice(
            label=f"Windwalker Hood: +25%",
            picture_class='windwalker-hood',
            progression=int(session_data.account.all_assets.get('EquipmentHats118').amount > 0),
            goal=1,
            resource='gem'
        ),
        Advice(
            label=f"Tempest Bow of Dust:"
                  f"<br>Base Range: 15 - 50%"
                  f"<br>Max + 5/5 10 PCT stones: 300%",
            picture_class='tempest-bow-of-dust',
            progression=int(session_data.account.all_assets.get('EquipmentBowsTempest0').amount > 0),
            goal=1,
            resource='tempest-bow-stone-10-pct',
        ),
        Advice(
            label=f"Tempest Ring of Gold:"
                  f"<br>Base Range: 20 - 50%"
                  f"<br>Max + 3/3 10 PCT stones: 125%",
            picture_class='tempest-ring-of-gold',
            progression=min(session_data.account.all_assets.get('EquipmentRingsTempest6').amount, 2),
            goal=2,
            resource='tempest-ring-stone-10-pct'
        )
    ]

    mge_label = f"Group E: {compass['Dust Calc']['mge']:.2f}x"
    currencies_advices[mge_label] = []
    ww_index = None
    eternal_hunt_preset_level = 100
    for ww in session_data.account.wws:
        if ww.current_preset_talents.get('423', 0) >= eternal_hunt_preset_level:
            ww_index = ww.character_index
            eternal_hunt_preset_level = ww.current_preset_talents.get('423', 0)
        if ww.secondary_preset_talents.get('423', 0) >= eternal_hunt_preset_level:
            ww_index = ww.character_index
            eternal_hunt_preset_level = ww.secondary_preset_talents.get('423', 0)
    ww_per_stack = lavaFunc(
        funcType='decay',
        level=eternal_hunt_preset_level + session_data.account.all_characters[ww_index].total_bonus_talent_levels,
        x1=3,
        x2=200
    )

    currencies_advices[mge_label].append(Advice(
        label=f"{eternal_hunt_preset_level}/{session_data.account.library['MaxBookLevel']} booked Eternal Hunt:"
              f"<br>Max Preset Level {eternal_hunt_preset_level + session_data.account.all_characters[ww_index].total_bonus_talent_levels} on "
              f"{session_data.account.all_characters[ww_index].character_name} including bonus talent levels",
        picture_class='eternal-hunt',
        progression=eternal_hunt_preset_level,
        goal=session_data.account.library['MaxBookLevel']
    ))
    currencies_advices[mge_label].append(Advice(
        label=f"<br>Per stack: +{ww_per_stack:.3f}%"
              f"<br>10 stacks: {ValueToMulti(10 * ww_per_stack):.3f}x"
              f"<br>20 stacks: {ValueToMulti(20 * ww_per_stack):.3f}x"
              f"<br>30 stacks: {ValueToMulti(30 * ww_per_stack):.3f}x"
              f"<br>40 stacks: {ValueToMulti(40 * ww_per_stack):.3f}x"
              f"<br>50 stacks: {ValueToMulti(50 * ww_per_stack):.3f}x",
        picture_class='eternal-hunt-grave',
        completed=True,
        informational=True
    ))

    mgf_label = f"Group F: {compass['Dust Calc']['mgf']:.2f}x"
    currencies_advices[mgf_label] = []
    ww_index = None
    compass_preset_level = 100
    for ww in session_data.account.wws:
        if ww_index is None:
            ww_index = ww.character_index
        if ww.current_preset_talents.get('421', 0) >= compass_preset_level:
            ww_index = ww.character_index
            compass_preset_level = ww.current_preset_talents.get('421', 0)
        if ww.secondary_preset_talents.get('421', 0) >= compass_preset_level:
            ww_index = ww.character_index
            compass_preset_level = ww.secondary_preset_talents.get('421', 0)
    bonus_talent_levels = session_data.account.all_characters[ww_index].total_bonus_talent_levels if ww_index is not None else 0
    compass_percent = lavaFunc(
        funcType='decay',
        level=compass_preset_level + bonus_talent_levels,
        x1=150,
        x2=300
    )
    currencies_advices[mgf_label].append(Advice(
        label=f"{compass_preset_level}/{session_data.account.library['MaxBookLevel']} booked Compass:"
              f"<br>Max Preset Level {compass_preset_level + bonus_talent_levels} on "
              f"{session_data.account.all_characters[ww_index].character_name} including bonus talent levels"
              f"<br>+{compass_percent:.3f}% boost to Dust found",
        picture_class='compass',
        progression=compass_preset_level,
        goal=session_data.account.library['MaxBookLevel']
    ))
    ab47 = session_data.account.arcade[47]
    currencies_advices[mgf_label].append(Advice(
        label=f"Arcade Bonus 47: {ab47['Display']}",
        picture_class=ab47['Image'],
        progression=ab47['Level'],
        goal=arcade_max_level + 1,
        resource=ab47['Material'],
    ))
    for bonus_name in [
        'De Dust I', 'De Dust II', 'De Dust III', 'De Dust IV', 'De Dust V',
        'Abomination Slayer IX', 'Abomination Slayer XXX', 'Abomination Slayer XXXIV'
    ]:
        currencies_advices[mgf_label].append(Advice(
            label=f"{compass['Upgrades'][bonus_name]['Path Name']}-{compass['Upgrades'][bonus_name]['Path Ordering']}: "
                  f"Spire of Dust: <br>{compass['Upgrades'][bonus_name]['Description']}",
            picture_class=compass['Upgrades'][bonus_name]['Image'],
            progression=compass['Upgrades'][bonus_name]['Level'],
            goal=compass['Upgrades'][bonus_name]['Max Level'],
            resource=compass['Upgrades'][bonus_name]['Dust Image'],
        ))
    for subgroup in currencies_advices:
        for advice in currencies_advices[subgroup]:
            mark_advice_completed(advice)

    currencies_ag = AdviceGroup(
        tier='',
        pre_string="Compass Currencies",
        advices=currencies_advices
    )
    currencies_ag.remove_empty_subgroups()
    return currencies_ag

def getCompassAbominationsAdviceGroup(compass):
    abom_advices = []

    for abom_name, abom_details in compass['Abominations'].items():
        if abom_details['Defeated']:
            abom_advices.append(Advice(
                label=f"{abom_name} defeated in W{abom_details['World']}"
                      f"<br>Weakness: {abom_details['Weakness']}",
                picture_class=abom_details['Image'] if abom_details['Defeated'] else 'placeholder',
                progression=1,
                goal=1
            ))
        else:
            abom_advices.append(Advice(
                label=f"{abom_name[:3]}... undefeated in W{abom_details['World']}"
                      f"<br>Weakness: {abom_details['Weakness']}",
                picture_class='placeholder',
                progression=0,
                goal=1
            ))

    for advice in abom_advices:
        mark_advice_completed(advice)

    abom_ag = AdviceGroup(
        tier='',
        pre_string="Abominations",
        advices=abom_advices
    )
    abom_ag.remove_empty_subgroups()
    return abom_ag

def getCompassMedallionsAdviceGroup(compass):
    medallion_advice = []

    medallion_advice.append(Advice(
        label=f"Total Medallions Collected: {compass['Total Medallions']}/{len(compass_medallions)}",
        picture_class='wind-walker-medallion',
        progression=compass['Total Medallions'],
        goal=len(compass_medallions)
    ))

    for code_name, enemy_details in compass['Medallions'].items():
        medallion_advice.append(Advice(
            label=f"{enemy_details['Enemy Name']}",
            picture_class=f"{enemy_details['Image']}",
            progression=int(enemy_details['Obtained']),
            goal=1
        ))

    for advice in medallion_advice:
        mark_advice_completed(advice)

    medallion_ag = AdviceGroup(
        tier='',
        pre_string="Medallions",
        advices=medallion_advice
    )
    medallion_ag.remove_empty_subgroups()
    return medallion_ag

def getCompassUpgradesAdviceGroups(compass):
    upgrades_AdviceDict = {}
    upgrades_AdviceGroups = []

    for path_name in compass_path_ordering:
        upgrades_AdviceDict[f'{path_name} Path Upgrades'] = []
        for compass_upgrade_index in compass_path_ordering[path_name]:
            clean_name = compass_upgrades_list[compass_upgrade_index][0].replace('(Tap_for_more_info)', '').replace('製', '').replace('_', ' ').rstrip()
            upgrade_details = compass['Upgrades'][clean_name]
            if path_name == 'Abomination':
                if 'Titan doesnt exist' not in upgrade_details['Description']:  #Filter out placeholders for future Titans/Abominations
                    abom = compass['Abominations'].get(upgrade_details['Abomination Name'], {'World': '?'})
                    if upgrade_details['Unlocked']:
                        upgrades_AdviceDict[f'{path_name} Path Upgrades'].append(Advice(
                            label=(
                                f"{upgrade_details['Path Name']}-{upgrade_details['Path Ordering']}: {clean_name}:"
                                f"<br>{upgrade_details['Description']}"
                            ),
                            picture_class=upgrade_details['Image'],
                            progression=upgrade_details['Level'],
                            goal=upgrade_details['Max Level'],
                            resource=upgrade_details['Dust Image']
                        ))
                    else:
                        upgrades_AdviceDict[f'{path_name} Path Upgrades'].append(Advice(
                            label=(
                                f"{upgrade_details['Path Name']}-{upgrade_details['Path Ordering']}: {clean_name}:"
                                f"<br>Defeat {upgrade_details['Abomination Name'][:3]}... in W{abom['World']} to reveal!"
                            ),
                            picture_class='placeholder',
                            progression=upgrade_details['Level'],
                            goal=upgrade_details['Max Level'],
                            resource=upgrade_details['Dust Image']
                        ))
            else:
                upgrades_AdviceDict[f'{path_name} Path Upgrades'].append(Advice(
                    label=(
                        f"{upgrade_details['Path Name']}-{upgrade_details['Path Ordering']}: "
                        f"{clean_name}: <br>{upgrade_details['Description']}"
                        f"<br>{'This upgrade is Locked!' if not upgrade_details['Unlocked'] else ''}"
                    ),
                    picture_class=upgrade_details['Image'],
                    progression=upgrade_details['Level'],
                    goal=upgrade_details['Max Level'],
                    resource=upgrade_details['Dust Image']
                ))
    upgrades_AdviceDict['Default Path Upgrades'].insert(0, Advice(
        label=f"Total Compass Upgrades: {compass['Total Upgrades']:,}",
        picture_class='compass',
    ))
    upgrades_AdviceDict['Abomination Path Upgrades'].insert(0, Advice(
        label=f"Total Abominations Slain: {compass['Total Abominations Slain']:,}",
        picture_class='slayer-abominator',
    ))

    for subgroup in upgrades_AdviceDict:
        for advice in upgrades_AdviceDict[subgroup]:
            mark_advice_completed(advice)

    for path_name, path_advice in upgrades_AdviceDict.items():
        upgrades_AdviceGroups.append(AdviceGroup(
            tier='',
            pre_string=f"Informational- {path_name}",
            advices=upgrades_AdviceDict[path_name],
            informational=True
        ))

    for ag in upgrades_AdviceGroups:
        ag.remove_empty_subgroups()
    return upgrades_AdviceGroups


def getCompassAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if 'Wind Walker' not in session_data.account.classes:
        compass_AdviceSection = AdviceSection(
            name="The Compass",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Wind Walker in World 6!",
            picture='customized/Compass_NoBG.png',
            unrated=True,
            unreached=session_data.account.highestWorldReached < 6,
            completed=False
        )
        return compass_AdviceSection

    compass = session_data.account.compass

    #Generate Alert Advice

    #Generate AdviceGroups
    compass_AdviceGroupDict = {}
    compass_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    compass_AdviceGroupDict['General'] = getCompassGeneralInfoAdviceGroup(compass)
    compass_AdviceGroupDict['Currencies'] = getCompassCurrenciesAdviceGroup(compass)
    compass_AdviceGroupDict['Abominations'] = getCompassAbominationsAdviceGroup(compass)
    compass_AdviceGroupDict['Medallions'] = getCompassMedallionsAdviceGroup(compass)
    upgrades_ags = getCompassUpgradesAdviceGroups(compass)
    for ag in upgrades_ags:
        compass_AdviceGroupDict[ag.pre_string] = ag

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    compass_AdviceSection = AdviceSection(
        name="The Compass",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Wind Walker and Compass Information",  #tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Compass_NoBG.png',
        groups=compass_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return compass_AdviceSection
