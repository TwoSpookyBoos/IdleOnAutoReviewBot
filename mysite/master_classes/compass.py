from consts.progression_tiers import true_max_tiers, compass_progressionTiers
from models.general.session_data import session_data

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.advice_group_tabbed import TabbedAdviceGroup, TabbedAdviceGroupTab

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.misc.add_tabbed_advice_group_or_spread_advice_group_list import add_tabbed_advice_group_or_spread_advice_group_list
from utils.logging import get_logger

from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.idleon.master_classes.compass import compass_path_tab_images
from utils.text_formatting import pl

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
                compass_Advices['Abominations'][subgroup_label].append(
                    compass.get_abominations_slain_advice(required_abominations)
                )
        if subgroup_label not in compass_Advices['Abominations'] and tier_Abominations == tier_number - 1:
            tier_Abominations = tier_number

        required_medallions = requirements.get('Medallions', 0)
        if compass.total_medallions < required_medallions:
            add_subgroup_if_available_slot(compass_Advices['Medallions'], subgroup_label)
            if subgroup_label in compass_Advices['Medallions']:
                compass_Advices['Medallions'][subgroup_label].append(
                    compass.get_medallions_collected_advice(required_medallions)
                )
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

    currency_advices['Currencies'].append(compass.get_top_of_the_mornin_advice())
    currency_advices['Currencies'].append(compass.get_total_dust_collected_advice())
    currency_advices['Currencies'].append(compass.get_aethermoon_advice())
    currency_advices['Currencies'].extend(compass.get_dust_advices())

    # Dust Multi calculation groups
    currency_advices['Currencies'].append(compass.get_dust_multi_advice())

    mga_label = f"Dust Multi Group A: {compass.dust_multi.mga:.3f}x"
    solardust_stacks_text = compass.get_solardust_stacks_text()
    currency_advices[mga_label] = [
        compass.upgrades['Mountains of Dust'].get_advice(),
        compass.upgrades['Solardust Hoarding'].get_advice(solardust_stacks_text),
    ]

    mgb_label = f"Dust Multi Group B: {compass.dust_multi.mgb:.2f}x"
    currency_advices[mgb_label] = [
        compass.upgrades['Spire of Dust'].get_advice(),
    ]

    mgc_label = f"Dust Multi Group C: {compass.dust_multi.mgc:.2f}x"
    currency_advices[mgc_label] = [
        session_data.account.sneaking.pristine_charms[
            'Twinkle Taffy'
        ].get_obtained_advice()
    ]

    mgd_label = f"Dust Multi Group D: {compass.dust_multi.mgd:.2f}x"
    currency_advices[mgd_label] = [
        compass.get_windwalker_hood_advice(),
        compass.get_tempest_bow_advice(),
        compass.get_tempest_ring_advice(),
    ]

    mge_label = f"Dust Multi Group E: {compass.dust_multi.mge:.2f}x"
    currency_advices[mge_label] = [
        compass.get_eternal_hunt_advice(),
        compass.get_eternal_hunt_stacks_advice(),
    ]

    mgf_label = f"Dust Multi Group F: {compass.dust_multi.mgf:.2f}x"
    currency_advices[mgf_label] = [compass.get_compass_talent_advice()]
    currency_advices[mgf_label].append(session_data.account.arcade[47].get_advice())

    currency_advices[mgf_label].append(
        session_data.account.lab_jewels['North Winds Jewel'].get_bonus_advice()
    )

    # Compass Upgrades
    for bonus_name in [
        'De Dust I', 'De Dust II', 'De Dust III', 'De Dust IV', 'De Dust V',
        'Abomination Slayer IX', 'Abomination Slayer XXX', 'Abomination Slayer XXXIV'
    ]:
        currency_advices[mgf_label].append(compass.upgrades[bonus_name].get_advice())

    mgg_label = f"Dust Multi Group G: {compass.dust_multi.mgg:.2f}x"
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

    medallion_advice.append(compass.get_total_medallions_advice())

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
    upgrades_AdviceDict['Default'].insert(0, compass.get_total_upgrades_advice())
    upgrades_AdviceDict['Abomination'].insert(0, compass.get_total_abominations_advice())

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
    if 'Wind Walker' not in session_data.account.characters.classes:
        compass_AdviceSection = AdviceSection(
            name="Compass",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Wind Walker in World 6!",
            picture='customized/Compass_NoBG.png',
            unrated=True,
            unreached=session_data.account.world_progress.highest_reached < 6,
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
