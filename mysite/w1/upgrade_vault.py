from consts import vault_progressionTiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
# from consts import (
#     break_you_best, infinity_string,
#     # vault_progressionTiers
# )
# from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    vault_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 1
    max_tier = max(vault_progressionTiers.keys(), default=0) - info_tiers
    tier_Vault = 0

    upgrades = session_data.account.vault['Upgrades']

    maxed_upgrades = []

    for tier, requirements in vault_progressionTiers.items():
        subgroup_label = f"To reach {'Informational ' if tier > max_tier else ''}Tier {tier}"
        vault_AdviceDict['Tiers'][subgroup_label] = []
        if 'Include' in requirements:
            for upgrade_name in requirements['Include']:
                if upgrades[upgrade_name]['Level'] < upgrades[upgrade_name]['Max Level']:
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
                else:
                    maxed_upgrades.append(upgrade_name)
        elif 'Exclude' in requirements:
            for upgrade_name, upgrade_details in session_data.account.vault['Upgrades'].items():
                if upgrade_name not in requirements['Exclude']:
                    if upgrade_details['Level'] < upgrade_details['Max Level']:
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

        if len(vault_AdviceDict['Tiers'][subgroup_label]) == 0 and tier_Vault == tier - 1:
            tier_Vault = tier

    #logger.debug(maxed_upgrades)

    tiers_ag = AdviceGroup(
        tier=tier_Vault,
        pre_string="Progression Tiers",
        advices=vault_AdviceDict['Tiers']
    )
    tiers_ag.remove_empty_subgroups()

    overall_SectionTier = min(max_tier + info_tiers, tier_Vault)
    return tiers_ag, overall_SectionTier, max_tier


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
        pre_string="Vault Upgrades info",
        advices=upgrades_AdviceDict
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def getVaultAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    vault_AdviceGroupDict = {}
    vault_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    vault_AdviceGroupDict['Upgrades'] = getVaultUpgradesAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    vault_AdviceSection = AdviceSection(
        name="Upgrade Vault",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Upgrade Vault Information",  #tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/VaultBut.png',
        groups=vault_AdviceGroupDict.values(),
        completed=None,
    )

    return vault_AdviceSection
