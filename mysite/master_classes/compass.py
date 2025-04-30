from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string, compass_dusts_list, compass_path_ordering, compass_upgrades_list, compass_medallions,
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
    currencies_advices = [
        Advice(
            label=f"{dust_name}: {notateNumber('Basic', compass[f'Dust{dust_index}'], 3)}",
            picture_class=f'compass-dust-{dust_index-1}',
            informational=True,
            completed=True
        ) for dust_index, dust_name in enumerate(compass_dusts_list, start=1)
    ]
    currencies_advices.insert(0, Advice(
        label=f"Total Dusts Collected: {notateNumber('Basic', compass['Total Dust Collected'], 3)}",
        picture_class='dustwalker',
        informational=True,
        completed=True
    ))
    currencies_advices.insert(0, Advice(
        label=(
            f"""Daily Top of the Mornin' kills: """
            f"""{compass['Upgrades']["Top of the Mornin'"]['Total Value'] + compass['Upgrades']['Abomination Slayer XII']['Total Value']}"""
            f"""<br>Remaining: {compass["Top of the Mornin'"]}"""
        ),
        picture_class=compass['Upgrades']["Top of the Mornin'"]['Image'],
        informational=True,
        completed=True
    ))

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
