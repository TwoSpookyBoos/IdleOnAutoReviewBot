from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.logging import get_logger

from consts.idleon.master_classes.royal_armory import royal_armory_orblet_market_glorification_index

logger = get_logger(__name__)


def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    royal_armory_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Royal Armory']
    max_tier = true_max - optional_tiers
    tier_RoyalArmory = 0

    tiers_ag = AdviceGroup(
        tier=tier_RoyalArmory,
        pre_string='Progression Tiers',
        advices=royal_armory_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_RoyalArmory)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getRoyalArmoryUpgradesAdviceGroup(royal_armory) -> AdviceGroup:
    upgrades_AdviceDict = {
        'Upgrades': [Advice(
            label=f"Total Armory Upgrade Levels: {royal_armory.total_levels:,}",
            picture_class='royal-armory-upgrade-0',
        )],
    }
    upgrades_AdviceDict['Upgrades'] += [
        upgrade.get_advice(royal_armory.total_levels) for upgrade in royal_armory.upgrades.values()
    ]

    for advice in upgrades_AdviceDict['Upgrades']:
        advice.mark_advice_completed()

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Armory Upgrades',
        advices=upgrades_AdviceDict,
        informational=True,
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def getRoyalArmoryStatuesAdviceGroup(royal_armory) -> AdviceGroup:
    statue_advices = [statue.get_advice() for statue in royal_armory.statues]

    for advice in statue_advices:
        advice.mark_advice_completed()

    statues_ag = AdviceGroup(
        tier='',
        pre_string='Royal Statues',
        advices=statue_advices,
        informational=True,
    )
    statues_ag.remove_empty_subgroups()
    return statues_ag


def getRoyalArmoryStatueFlairAdviceGroup(royal_armory) -> AdviceGroup:
    flair_advices = [
        flair.get_advice(session_data.account.statues[flair.statue_name]['Image'])
        for flair in royal_armory.statue_flairs
    ]

    for advice in flair_advices:
        advice.mark_advice_completed()

    flair_ag = AdviceGroup(
        tier='',
        pre_string='Statue Flair',
        advices=flair_advices,
        informational=True,
    )
    flair_ag.remove_empty_subgroups()
    return flair_ag


def getRoyalArmoryOrbletMarketAdviceGroup(royal_armory) -> AdviceGroup:
    # GLORIFICATION isn't a leveled upgrade, so it's shown as a built/Glorified count instead, in its
    # real shop position (`royal_armory.orblet_market` is already in real display order).
    orblet_advices = []
    for slot_upgrade in royal_armory.orblet_market.values():
        if slot_upgrade.index == royal_armory_orblet_market_glorification_index:
            orblet_advices.append(royal_armory.get_outposts_glorified_advice())
        else:
            orblet_advices.append(slot_upgrade.get_advice())

    for advice in orblet_advices:
        advice.mark_advice_completed()

    orblet_ag = AdviceGroup(
        tier='',
        pre_string="Lil' Orblet Shop",
        advices=orblet_advices,
        informational=True,
    )
    orblet_ag.remove_empty_subgroups()
    return orblet_ag


def getRoyalArmoryAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if 'Royal Guardian' not in session_data.account.classes:
        royal_armory_AdviceSection = AdviceSection(
            name="Royal Armory",
            tier="Not Yet Evaluated",
            header="Come back after unlocking a Royal Guardian (Divine Knight's master class)!",
            picture='extracted_sprites/OrbOfVerisimilitude.gif',
            unrated=True,
            unreached=session_data.account.highest_world_reached < 6,
            completed=False
        )
        return royal_armory_AdviceSection

    royal_armory = session_data.account.royal_armory
    royal_armory.calculate_upgrades()

    #Generate AdviceGroups
    royal_armory_AdviceGroupDict = {}
    royal_armory_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    royal_armory_AdviceGroupDict['Upgrades'] = getRoyalArmoryUpgradesAdviceGroup(royal_armory)
    royal_armory_AdviceGroupDict['Statues'] = getRoyalArmoryStatuesAdviceGroup(royal_armory)
    royal_armory_AdviceGroupDict['Statue Flair'] = getRoyalArmoryStatueFlairAdviceGroup(royal_armory)
    royal_armory_AdviceGroupDict["Orblet Market"] = getRoyalArmoryOrbletMarketAdviceGroup(royal_armory)

    #Generate AdviceSection
    royal_armory_AdviceSection = AdviceSection(
        name='Royal Armory',
        tier='',
        header='Royal Guardian and Royal Armory Information',
        picture='extracted_sprites/OrbOfVerisimilitude.gif',
        groups=royal_armory_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return royal_armory_AdviceSection
