from consts.progression_tiers import true_max_tiers, compass_progressionTiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.advice_group_tabbed import TabbedAdviceGroup, TabbedAdviceGroupTab

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import add_tabbed_advice_group_or_spread_advice_group_list
from utils.safer_data_handling import safer_math_log
from utils.logging import get_logger

from consts.consts_autoreview import (
    break_you_best, build_subgroup_label,
    ValueToMulti, EmojiType,
)
from consts.idleon.lava_func import lava_func
from consts.idleon.master_classes.compass import compass_dusts_list, compass_medallions, compass_path_tab_images
from utils.text_formatting import notateNumber, pl

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup(compass) -> tuple[dict[str, AdviceGroup], int, int, int]:
    compass_Advices = {
        'Specific Upgrades': {},
        'Abominations': {},
        'Medallions': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Compass']
    max_tier = true_max - optional_tiers
    tier_SpecificUpgrades = 0
    tier_Abominations = 0
    tier_Medallions = 0

    for tier_number, requirements in compass_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        for upgrade_name, required_level in requirements.get('Specific Upgrades', {}).items():
            upgrade_details = compass.upgrades.get(upgrade_name)
            if upgrade_details and upgrade_details.level < required_level:
                add_subgroup_if_available_slot(compass_Advices['Specific Upgrades'], subgroup_label)
                if subgroup_label in compass_Advices['Specific Upgrades']:
                    compass_Advices['Specific Upgrades'][subgroup_label].append(
                        upgrade_details.get_advice(goal=required_level)
                    )
        if subgroup_label not in compass_Advices['Specific Upgrades'] and tier_SpecificUpgrades == tier_number - 1:
            tier_SpecificUpgrades = tier_number

        required_abominations = requirements.get('Abominations', 0)
        if compass.total_abominations_slain < required_abominations:
            add_subgroup_if_available_slot(compass_Advices['Abominations'], subgroup_label)
            if subgroup_label in compass_Advices['Abominations']:
                compass_Advices['Abominations'][subgroup_label].append(Advice(
                    label="Abominations Slain",
                    picture_class='slayer-abominator',
                    progression=compass.total_abominations_slain,
                    goal=required_abominations
                ))
        if subgroup_label not in compass_Advices['Abominations'] and tier_Abominations == tier_number - 1:
            tier_Abominations = tier_number

        required_medallions = requirements.get('Medallions', 0)
        if compass.total_medallions < required_medallions:
            add_subgroup_if_available_slot(compass_Advices['Medallions'], subgroup_label)
            if subgroup_label in compass_Advices['Medallions']:
                compass_Advices['Medallions'][subgroup_label].append(Advice(
                    label="Medallions Collected",
                    picture_class='wind-walker-medallion',
                    progression=compass.total_medallions,
                    goal=required_medallions
                ))
        if subgroup_label not in compass_Advices['Medallions'] and tier_Medallions == tier_number - 1:
            tier_Medallions = tier_number

    compass_AdviceGroupDict = {}
    compass_AdviceGroupDict['Specific Upgrades'] = AdviceGroup(
        tier=tier_SpecificUpgrades,
        pre_string=f"Level up the following Compass Upgrade{pl(compass_Advices['Specific Upgrades'])}",
        advices=compass_Advices['Specific Upgrades'],
        post_string='Path levels unlock the upgrades further along that Path',
    )
    compass_AdviceGroupDict['Abominations'] = AdviceGroup(
        tier=tier_Abominations,
        pre_string='Slay more Abominations',
        advices=compass_Advices['Abominations'],
    )
    compass_AdviceGroupDict['Medallions'] = AdviceGroup(
        tier=tier_Medallions,
        pre_string='Collect more Medallions',
        advices=compass_Advices['Medallions'],
        post_string='Medallions only drop while in Tempest Form',
    )

    overall_SectionTier = min(true_max, tier_SpecificUpgrades, tier_Abominations, tier_Medallions)
    return compass_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getCompassGeneralInfoAdviceGroup():
    general_advices = []
    general_ag = AdviceGroup(
        tier='',
        pre_string='Compass Currencies',
        advices=general_advices,
        informational=True
    )
    general_ag.remove_empty_subgroups()
    return general_ag

def getCompassCurrenciesAdviceGroup(compass):
    currency_advices = {}

    #Basic Currencies
    currency_advices['Currencies'] = []

    currency_advices['Currencies'].append(Advice(
        label=(
            f"""Daily Top of the Mornin' kills: """
            f"""{compass.upgrades["Top of the Mornin'"].total_value + compass.upgrades['Abomination Slayer XII'].total_value}"""
            f"""<br>Remaining: {compass.top_of_the_mornin}"""
        ),
        picture_class=compass.upgrades["Top of the Mornin'"].image,
        progression=compass.upgrades["Top of the Mornin'"].total_value + compass.upgrades['Abomination Slayer XII'].total_value - compass.top_of_the_mornin,
        goal=compass.upgrades["Top of the Mornin'"].total_value + compass.upgrades['Abomination Slayer XII'].total_value,
        informational=True
    ))

    currency_advices['Currencies'].append(Advice(
        label=f"Total Dusts Collected: {notateNumber('Basic', compass.total_dust_collected, 3)}",
        picture_class='dustwalker',
        informational=True,
        completed=True
    ))

    if compass.aethermoons_enabled:
        currency_advices['Currencies'].append(Advice(
            label=f"Aethermoons Enabled! Collect 1 per two full AFK hour while fighting on a Wind Walker. Maximize your /hr display "
                  f"within AFK Info screen before consuming!",
            picture_class='aethermoon',
            progression=1,
            goal=1
        ))
    else:
        currency_advices['Currencies'].append(Advice(
            label=f"Fight with Tempest Form enabled to collect 1,000 Aether Fragments, then use the stack. "
                  f"This enables AFK Fighting on Wind Walkers to produce 1 Aethermoon per two hours!",
            picture_class='aether-fragment',
            progression=min(1000, session_data.account.all_assets.get('Quest100').amount),
            goal=1000
        ))

    currency_advices['Currencies'].extend([Advice(
        label=f"{dust_name}: {notateNumber('Basic', compass.dusts[dust_index], 3)}",
        picture_class=f'compass-dust-{dust_index}',
        informational=True,
        completed=True
    ) for dust_index, dust_name in enumerate(compass_dusts_list)])

    # Dust Multi calculation groups
    currency_advices['Currencies'].append(Advice(
        label=f"Total Dust multi: {compass.dust_calc['Total']:.3f}x",
        picture_class='compass'
    ))

    mga_label = f"Dust Multi Group A: {compass.dust_calc['mga']:.3f}x"
    solardust_stacks_text = (
        f"<br>{safer_math_log(compass.dusts[2], 'Lava'):.3f} stacks = "
        f"{compass.upgrades['Solardust Hoarding'].total_value * safer_math_log(compass.dusts[2], 'Lava'):.3f}% total"
    )
    currency_advices[mga_label] = [
        compass.upgrades['Mountains of Dust'].get_advice(),
        compass.upgrades['Solardust Hoarding'].get_advice(solardust_stacks_text),
    ]

    mgb_label = f"Dust Multi Group B: {compass.dust_calc['mgb']:.2f}x"
    currency_advices[mgb_label] = [
        compass.upgrades['Spire of Dust'].get_advice(),
    ]

    mgc_label = f"Dust Multi Group C: {compass.dust_calc['mgc']:.2f}x"
    currency_advices[mgc_label] = [
        session_data.account.sneaking.pristine_charms[
            'Twinkle Taffy'
        ].get_obtained_advice()
    ]

    mgd_label = f"Dust Multi Group D: {compass.dust_calc['mgd']:.2f}x"
    currency_advices[mgd_label] = [
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

    mge_label = f"Dust Multi Group E: {compass.dust_calc['mge']:.2f}x"
    currency_advices[mge_label] = []
    ww_index = None
    eternal_hunt_preset_level = 100
    for ww in session_data.account.wws:
        if ww_index is None:
            ww_index = ww.character_index
        if ww.current_preset_talents.get('423', 0) >= eternal_hunt_preset_level:
            ww_index = ww.character_index
            eternal_hunt_preset_level = ww.current_preset_talents.get('423', 0)
        if ww.secondary_preset_talents.get('423', 0) >= eternal_hunt_preset_level:
            ww_index = ww.character_index
            eternal_hunt_preset_level = ww.secondary_preset_talents.get('423', 0)
    bonus_talent_levels = session_data.account.all_characters[ww_index].total_bonus_talent_levels if ww_index is not None else 0
    ww_per_stack = lava_func(
        funcType='decay',
        level=eternal_hunt_preset_level + bonus_talent_levels,
        x1=3,
        x2=200
    )

    currency_advices[mge_label].append(Advice(
        label=f"{eternal_hunt_preset_level}/{session_data.account.library.max_book_level} booked Eternal Hunt:"
              f"<br>Max Preset Level {eternal_hunt_preset_level + session_data.account.all_characters[ww_index].total_bonus_talent_levels} on "
              f"{session_data.account.all_characters[ww_index].character_name} including bonus talent levels",
        picture_class='eternal-hunt',
        progression=eternal_hunt_preset_level,
        goal=session_data.account.library.max_book_level
    ))
    currency_advices[mge_label].append(Advice(
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

    mgf_label = f"Dust Multi Group F: {compass.dust_calc['mgf']:.2f}x"
    currency_advices[mgf_label] = []
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
    compass_percent = lava_func(
        funcType='decay',
        level=compass_preset_level + bonus_talent_levels,
        x1=150,
        x2=300
    )
    currency_advices[mgf_label].append(Advice(
        label=f"{compass_preset_level}/{session_data.account.library.max_book_level} booked Compass:"
              f"<br>Max Preset Level {compass_preset_level + bonus_talent_levels} on "
              f"{session_data.account.all_characters[ww_index].character_name} including bonus talent levels"
              f"<br>+{compass_percent:.3f}% boost to Dust found",
        picture_class='compass',
        progression=compass_preset_level,
        goal=session_data.account.library.max_book_level
    ))
    currency_advices[mgf_label].append(session_data.account.arcade[47].get_advice())

    lab_jewel = session_data.account.labJewels['North Winds Jewel']
    lab_jewel_active = lab_jewel['Enabled']
    currency_advices[mgf_label].append(Advice(
        label=f"Lab Jewel 'North Winds Jewel': +{lab_jewel['Value'] * lab_jewel_active}/{lab_jewel['Value']}%",
        picture_class='north-winds-jewel',
        progression=int(lab_jewel_active),
        goal=1
    ))

    # Compass Upgrades
    for bonus_name in [
        'De Dust I', 'De Dust II', 'De Dust III', 'De Dust IV', 'De Dust V',
        'Abomination Slayer IX', 'Abomination Slayer XXX', 'Abomination Slayer XXXIV'
    ]:
        currency_advices[mgf_label].append(compass.upgrades[bonus_name].get_advice())

    mgg_label = f"Dust Multi Group G: {compass.dust_calc['mgg']:.2f}x"
    currency_advices[mgg_label] = [
        session_data.account.emperor["Windwalker Extra Dust"].get_bonus_advice()
    ]

    for subgroup in currency_advices:
        for advice in currency_advices[subgroup]:
            advice.mark_advice_completed()

    currencies_ag = AdviceGroup(
        tier='',
        pre_string="Compass Currencies",
        advices=currency_advices,
        informational=True
    )
    currencies_ag.remove_empty_subgroups()
    return currencies_ag

def getCompassAbominationsAdviceGroup(compass):
    abom_advices = []

    for abomination in compass.abominations.values():
        abom_advices.append(abomination.get_advice())

    for advice in abom_advices:
        advice.mark_advice_completed()

    abom_ag = AdviceGroup(
        tier='',
        pre_string="Abominations",
        advices=abom_advices,
        informational=True
    )
    abom_ag.remove_empty_subgroups()
    return abom_ag

def getCompassMedallionsAdviceGroup(compass):
    medallion_advice = []

    medallion_advice.append(Advice(
        label=f"Total Medallions Collected: {compass.total_medallions}/{len(compass_medallions)}",
        picture_class='wind-walker-medallion',
        progression=compass.total_medallions,
        goal=len(compass_medallions)
    ))

    for medallion in compass.medallions.values():
        medallion_advice.append(medallion.get_advice())

    for advice in medallion_advice:
        advice.mark_advice_completed()

    medallion_ag = AdviceGroup(
        tier='',
        pre_string='Medallions',
        advices=medallion_advice,
        informational=True
    )
    medallion_ag.remove_empty_subgroups()
    return medallion_ag

def getCompassUpgradesTabbed(compass) -> TabbedAdviceGroup:
    upgrades_AdviceDict = {}

    # compass.upgrades is already populated in path-then-path-ordering order (see Compass.__init__),
    # so grouping by upgrade_details.path_name here preserves the same path/ordering layout as before.
    for upgrade_details in compass.upgrades.values():
        path_name = upgrade_details.path_name
        upgrades_AdviceDict.setdefault(path_name, [])
        if path_name == 'Abomination':
            if 'Titan doesnt exist' not in upgrade_details.description:  #Filter out placeholders for future Titans/Abominations
                if upgrade_details.unlocked:
                    upgrades_AdviceDict[path_name].append(upgrade_details.get_advice())
                else:
                    abomination = compass.abominations.get(upgrade_details.abomination_name)
                    abom_world = abomination.world if abomination else '?'
                    upgrades_AdviceDict[path_name].append(
                        upgrade_details.get_abomination_locked_advice(abom_world)
                    )
        else:
            locked_text = f"<br>{'This upgrade is Locked!' if not upgrade_details.unlocked else ''}"
            upgrades_AdviceDict[path_name].append(upgrade_details.get_advice(locked_text))
    upgrades_AdviceDict['Default'].insert(0, Advice(
        label=f"Total Compass Upgrades: {compass.total_upgrades:,}",
        picture_class='compass',
    ))
    upgrades_AdviceDict['Abomination'].insert(0, Advice(
        label=f"Total Abominations Slain: {compass.total_abominations_slain:,}",
        picture_class='slayer-abominator',
    ))

    upgrades_tabbed = {}
    for path_name, path_advices in upgrades_AdviceDict.items():
        path_upgrade = compass.upgrades.get(f'{path_name} Path')
        tab_image = path_upgrade.image if path_upgrade else compass_path_tab_images[path_name]
        upgrades_tabbed[path_name] = (
            TabbedAdviceGroupTab(tab_image, f''),
            AdviceGroup(
                tier='',
                pre_string=f'{path_name} Path Upgrades',
                advices=path_advices,
                informational=True
            )
        )

    for (_, advice_group) in upgrades_tabbed.values():
        advice_group.mark_advice_completed()
        advice_group.remove_empty_subgroups()
    return TabbedAdviceGroup(upgrades_tabbed)


def getCompassAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if 'Wind Walker' not in session_data.account.classes:
        compass_AdviceSection = AdviceSection(
            name="Compass",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Wind Walker in World 6!",
            picture='customized/Compass_NoBG.png',
            unrated=True,
            unreached=session_data.account.highest_world_reached < 6,
            completed=False
        )
        return compass_AdviceSection

    compass = session_data.account.compass

    #Generate Alert Advice

    #Generate AdviceGroups
    compass_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(compass)
    compass_AdviceGroupDict['General'] = getCompassGeneralInfoAdviceGroup()
    compass_AdviceGroupDict['Currencies'] = getCompassCurrenciesAdviceGroup(compass)
    compass_AdviceGroupDict['Abominations Info'] = getCompassAbominationsAdviceGroup(compass)
    compass_AdviceGroupDict['Medallions Info'] = getCompassMedallionsAdviceGroup(compass)
    add_tabbed_advice_group_or_spread_advice_group_list(
        compass_AdviceGroupDict, getCompassUpgradesTabbed(compass), 'Upgrades'
    )

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    compass_AdviceSection = AdviceSection(
        name="Compass",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Compass tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='customized/Compass_NoBG.png',
        groups=compass_AdviceGroupDict.values(),
        completed=None,
    )

    return compass_AdviceSection
