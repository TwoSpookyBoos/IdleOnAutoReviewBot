from consts.consts import break_you_best, build_subgroup_label
from consts.progression_tiers import vault_progressionTiers
from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    vault_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Upgrade Vault']
    max_tier = true_max - optional_tiers
    tier_Vault = 0

    upgrades = session_data.account.vault['Upgrades']

    for tier_number, requirements in vault_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        if 'Include' in requirements:
            for upgrade_name in requirements['Include']:
                if upgrades[upgrade_name]['Level'] < upgrades[upgrade_name]['Max Level']:
                    if (
                        subgroup_label not in vault_AdviceDict['Tiers']
                        and len(vault_AdviceDict['Tiers']) < session_data.account.max_subgroups
                    ):
                        vault_AdviceDict['Tiers'][subgroup_label] = []
                    if subgroup_label in vault_AdviceDict['Tiers']:
                        vault_AdviceDict['Tiers'][subgroup_label].append(Advice(
                            label=(
                                f"Max {upgrade_name}"
                                f"<br>Requires {upgrades[upgrade_name]['Unlock Requirement'] - session_data.account.vault['Total Upgrades']} more Upgrades to unlock"
                                if not upgrades[upgrade_name]['Unlocked'] else
                                f"{upgrade_name}: {upgrades[upgrade_name]['Description']}"
                            ),
                            picture_class=upgrades[upgrade_name]['Image'],
                            progression=upgrades[upgrade_name]['Level'],
                            goal=upgrades[upgrade_name]['Max Level'],
                        ))
        elif 'Exclude' in requirements:
            for upgrade_name, upgrade_details in session_data.account.vault['Upgrades'].items():
                if upgrade_name not in requirements['Exclude']:
                    if upgrade_details['Level'] < upgrade_details['Max Level']:
                        if (
                            subgroup_label not in vault_AdviceDict['Tiers']
                            and len(vault_AdviceDict['Tiers']) < session_data.account.max_subgroups
                        ):
                            vault_AdviceDict['Tiers'][subgroup_label] = []
                        if subgroup_label in vault_AdviceDict['Tiers']:
                            vault_AdviceDict['Tiers'][subgroup_label].append(Advice(
                                label=(
                                    f"Max {upgrade_name}"
                                    f"<br>Requires {upgrade_details['Unlock Requirement'] - session_data.account.vault['Total Upgrades']} more Upgrades to unlock"
                                    if not upgrade_details['Unlocked'] else
                                    f"{upgrade_name}: {upgrade_details['Description']}"
                                ),
                                picture_class=upgrade_details['Image'],
                                progression=upgrade_details['Level'],
                                goal=upgrade_details['Max Level'],
                            ))

        if subgroup_label not in vault_AdviceDict['Tiers'] and tier_Vault == tier_number - 1:
            tier_Vault = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_Vault,
        pre_string='Progression Tiers',
        advices=vault_AdviceDict['Tiers']
    )

    overall_SectionTier = min(true_max, tier_Vault)
    return tiers_ag, overall_SectionTier, max_tier, true_max


def getVaultUpgradesAdviceGroup():
    upgrades_AdviceDict = {}

    #Upgrades
    upgrades_AdviceDict['Upgrades'] = [
        Advice(
            label=(
                f"{upgrade_name}: {upgrade_details['Description']}"
                f"<br>Requires {upgrade_details['Unlock Requirement'] - session_data.account.vault['Total Upgrades']} more Upgrades to unlock"
                if not upgrade_details['Unlocked'] else
                f"{upgrade_name}: {upgrade_details['Description']}"
            ),
            picture_class=upgrade_details['Image'],
            progression=upgrade_details['Level'],
            goal=upgrade_details['Max Level'],
        ) for upgrade_name, upgrade_details in session_data.account.vault['Upgrades'].items()
    ]
    upgrades_AdviceDict['Upgrades'].insert(0, Advice(
        label=f"Total Vault Upgrades: {session_data.account.vault['Total Upgrades']:,}",
        picture_class='upgrade-vault',
    ))

    for subgroup in upgrades_AdviceDict:
        for advice in upgrades_AdviceDict[subgroup]:
            mark_advice_completed(advice)

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Vault Upgrades',
        advices=upgrades_AdviceDict,
        informational=True
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def getVaultAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    vault_AdviceGroupDict = {}
    vault_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    vault_AdviceGroupDict['Upgrades'] = getVaultUpgradesAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    vault_AdviceSection = AdviceSection(
        name='Upgrade Vault',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Upgrade Vault tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/VaultBut.png',
        groups=vault_AdviceGroupDict.values(),
    )

    return vault_AdviceSection
