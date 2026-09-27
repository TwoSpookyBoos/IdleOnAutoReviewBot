
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w5 import snail_max_possible_rank
from consts.consts_w3 import buildings_tower_max_level, collider_storage_limit_list
from consts.progression_tiers import atoms_progressionTiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger
from utils.text_formatting import pl

logger = get_logger(__name__)

def getColliderSettingsAdviceGroup() -> AdviceGroup:
    settings_advice = {
        'Alerts': [],
        'Information': [],
    }

    colliderData = session_data.account.atom_collider

    try:
        formatted_particlesOwned = f"{colliderData.particles:,.0f}"
    except:
        formatted_particlesOwned = f"{colliderData.particles}"

    settings_advice['Information'].append(
        Advice(
            label=f"Particles Owned: {formatted_particlesOwned}",
            picture_class='particles',
        )
    )

    for atom in colliderData.values():
        settings_advice['Information'].append(atom.get_advice(
            f"<br>{colliderData.magnesium_days}/100 days since last retrap"
            if atom.name == 'Magnesium - Trap Compounder' else ''
        ))

    #Alerts
    #Collider is not Off
    if colliderData.on == True:
        settings_advice['Alerts'].append(
            Advice(
                label=f"Collider switch status: {'On' if colliderData.on else 'Off'}.<br>Recommended to select Off instead to avoid nuking your storage from a single misclick.",
                picture_class='collider-toggle',
            )
        )

    #Limit not set to 1050M
    if colliderData.storage_limit != collider_storage_limit_list[-1]:
        settings_advice['Alerts'].append(
            Advice(
                label=f"Storage Limit: {colliderData.storage_limit}M<br>Recommend to select {collider_storage_limit_list[-1]}M instead.",
                picture_class='',
                progression=colliderData.storage_limit,
                goal=collider_storage_limit_list[-1],
                unit='M'
            )
        )

    #Sodium lower than Snail // 5
    if session_data.account.gaming.snail.rank < snail_max_possible_rank:
        if colliderData['Sodium - Snail Kryptonite'].level < session_data.account.gaming.snail.rank // 5:
            settings_advice['Alerts'].append(
                Advice(
                    label=f"Snail could reset from Rank {session_data.account.gaming.snail.rank}"
                          f" to {colliderData['Sodium - Snail Kryptonite'].level*5}!"
                          f"<br>Level Sodium to {session_data.account.gaming.snail.rank // 5}"
                          f" to protect Rank {5 * (session_data.account.gaming.snail.rank // 5)}.",
                    picture_class="sodium",
                    progression=colliderData['Sodium - Snail Kryptonite'].level,
                    goal=session_data.account.gaming.snail.rank // 5
                )
            )
            session_data.account.alerts_Advices['World 3'].append(Advice(
                    label=f"Snail could reset from Rank {session_data.account.gaming.snail.rank}"
                          f" to {colliderData['Sodium - Snail Kryptonite'].level * 5}!"
                          f"<br>Level {{{{ Sodium|#atom-collider }}}} to {session_data.account.gaming.snail.rank // 5}"
                          f" to protect Rank {5 * (session_data.account.gaming.snail.rank // 5)}.",
                    picture_class='sodium',
                    progression=colliderData['Sodium - Snail Kryptonite'].level,
                    goal=session_data.account.gaming.snail.rank // 5
            ))

    currentMaxedTowers = 0
    if colliderData["Carbon - Wizard Maximizer"].level < colliderData["Carbon - Wizard Maximizer"].max_level:
        for buildingName, buildingValuesDict in session_data.account.construction_buildings.items():
            if buildingValuesDict['Type'] == 'Tower':
                if buildingValuesDict['Level'] >= buildingValuesDict['MaxLevel'] and buildingValuesDict['MaxLevel'] < buildings_tower_max_level:
                    currentMaxedTowers += 1

    if currentMaxedTowers > 0:
        settings_advice['Alerts'].append(
            Advice(
                label=f"{currentMaxedTowers} TD Tower{pl(currentMaxedTowers)} at max level."
                      f"<br>Level up Carbon to increase your max Tower levels by 2.",
                picture_class='carbon',
            )
        )
        session_data.account.alerts_Advices['World 3'].append(Advice(
            label=f"{currentMaxedTowers} TD Tower{pl(currentMaxedTowers)} at max level."
                  f"<br>Level up {{{{ Carbon|#atom-collider }}}} to increase your max Tower levels by 2.",
            picture_class='carbon',
        ))

    for advice in settings_advice['Information']:
        advice.mark_advice_completed()

    settings_ag = AdviceGroup(
        tier='',
        pre_string='Collider Alerts and General Information',
        advices=settings_advice,
        informational=True
    )
    settings_ag.remove_empty_subgroups()
    return settings_ag


def getMaxLevelAdviceGroup() -> AdviceGroup:
    ml_advice = []

    sp_id = session_data.account.gaming.superbits['Isotope Discovery']
    ml_advice.append(
        Advice(
            label=f"Purchasing the final SuperBit in Gaming will increase the max level of all Atoms by 10",
            picture_class='red-bits',
            progression=int(sp_id.unlocked),
            goal=1
        )
    )

    ml_advice.append(session_data.account.compass.upgrades['Atomic Potential'].get_advice())

    hb = session_data.account.event_points_shop['Higgs Boson']
    ml_advice.append(hb.get_bonus_advice())

    for advice in ml_advice:
        advice.mark_advice_completed()

    ml_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Max Atom Levels',
        advices=ml_advice,
        informational=True
    )
    return ml_ag


def getCostReductionAdviceGroup() -> AdviceGroup:
    cr_advice = []

    cr_advice.append(Advice(
        label=f"W5 Taskboard Merit: {session_data.account.merits[4][6].level * 7}/{session_data.account.merits[4][6].max_level * 7}%"
              f"<br>The in-game display is incorrect. Don't @ me.",
        picture_class='merit-4-6',
        progression=session_data.account.merits[4][6].level,
        goal=session_data.account.merits[4][6].max_level
    ))

    cr_advice.append(Advice(
        label=f"""Neon - Damage N' Cheapener: {session_data.account.atom_collider["Neon - Damage N' Cheapener"].level}"""
        f"""/{session_data.account.atom_collider["Neon - Damage N' Cheapener"].max_level}%""",
        picture_class='neon',
        progression=session_data.account.atom_collider["Neon - Damage N' Cheapener"].level,
        goal=session_data.account.atom_collider["Neon - Damage N' Cheapener"].max_level
    ))

    cr_advice.append(Advice(
        label=f"Superbit: Atom Redux: {10 * session_data.account.gaming.superbits['Atom Redux'].unlocked}/10%",
        picture_class='red-bits',
        progression=int(session_data.account.gaming.superbits['Atom Redux'].unlocked),
        goal=1
    ))

    cr_advice.append(Advice(
        label=f"Atom Collider building: {session_data.account.construction_buildings['Atom Collider']['Level'] / 10:.1f}"
              f"/{session_data.account.construction_buildings['Atom Collider']['MaxLevel'] / 10:.1f}%",
        picture_class='atom-collider',
        progression=session_data.account.construction_buildings['Atom Collider']['Level'],
        goal=session_data.account.construction_buildings['Atom Collider']['MaxLevel']
    ))

    cr_advice.append(session_data.account.alchemy_bubbles['Atom Split'].get_advice(
        f" bubble: {session_data.account.alchemy_bubbles['Atom Split'].base_value:.2f}/14%"
    ))

    cr_advice.append(session_data.account.stamps['Atomic Stamp'].get_advice())

    cr_advice.append(session_data.account.grimoire.upgrades['Death of the Atom Price'].get_advice(
        session_data.account.grimoire.total_upgrades
    ))

    cr_advice.append(session_data.account.compass.upgrades['Atomic Cost Crash'].get_advice())

    cr_advice.append(Advice(
        label=f"Remaining cost: {session_data.account.atom_collider.cost_reduction_multi*100:.2f}%",
        picture_class='particles',
    ))

    cr_advice.append(Advice(
        label=f"Total discount: {session_data.account.atom_collider.cost_discount:.2f}% off",
        picture_class='particles',
    ))

    for advice in cr_advice:
        advice.mark_advice_completed()

    cr_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Atom Collider Cost Reduction',
        advices=cr_advice,
        informational=True
    )
    return cr_ag

def getAtomExclusionsList() -> list[str]:
    exclusionsList = []
    # If cooking is basically finished thanks to NMLB, exclude Fluoride's cooking speed
    if session_data.account.cooking.close_enough:
        exclusionsList.append('Fluoride - Void Plate Chef')

    return exclusionsList

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    collider_AdviceDict = {
        'Atoms': {},
    }

    optional_tiers = 1
    true_max = max(atoms_progressionTiers.keys())
    max_tier = true_max - optional_tiers
    tier_atomLevels = 0

    player_atoms = session_data.account.atom_collider  # Player Atoms
    exclusionsList = getAtomExclusionsList()

    # Assess Tiers
    for tier_number, requirements in atoms_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        #Atom levels
        for atom_name, level in requirements.get('Atoms', {}).items():
            if atom_name not in exclusionsList and player_atoms[atom_name].level < level:
                add_subgroup_if_available_slot(collider_AdviceDict['Atoms'], subgroup_label)
                if subgroup_label in collider_AdviceDict['Atoms']:
                    collider_AdviceDict['Atoms'][subgroup_label].append(player_atoms[atom_name].get_tier_advice(level))
        if subgroup_label not in collider_AdviceDict['Atoms'] and tier_atomLevels == tier_number - 1:
            tier_atomLevels = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_atomLevels,
        pre_string='Level Priority Atoms',
        advices=collider_AdviceDict['Atoms'],
    )
    tiers_ag.remove_empty_subgroups()

    overall_ColliderTier = min(true_max, tier_atomLevels)
    return tiers_ag, overall_ColliderTier, max_tier, true_max

def getColliderAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['Atom Collider']['Level'] < 1:
        collider_AdviceSection = AdviceSection(
            name='Atom Collider',
            tier='Not Yet Evaluated',
            header='"Come back after unlocking the Atom Collider within the Construction skill in World 3!',
            picture='Collider.gif',
            unreached=True
        )
        return collider_AdviceSection

    # Generate AdviceGroups
    collider_AdviceGroupDict = {}
    collider_AdviceGroupDict['Atoms'], overall_ColliderTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    collider_AdviceGroupDict['ColliderSettings'] = getColliderSettingsAdviceGroup()
    collider_AdviceGroupDict['MaxLevel'] = getMaxLevelAdviceGroup()
    collider_AdviceGroupDict['CostReduction'] = getCostReductionAdviceGroup()

    # Generate AdviceSection

    tier_section = f"{overall_ColliderTier}/{max_tier}"
    collider_AdviceSection = AdviceSection(
        name='Atom Collider',
        tier=tier_section,
        pinchy_rating=overall_ColliderTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Collider tier met: {tier_section}{break_you_best if overall_ColliderTier >= max_tier else ''}",
        picture='Collider.gif',
        groups=collider_AdviceGroupDict.values()
    )
    return collider_AdviceSection
