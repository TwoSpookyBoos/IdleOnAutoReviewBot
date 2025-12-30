
from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w5 import snail_max_possible_rank
from consts.consts_w4 import cooking_close_enough
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
        formatted_particlesOwned = f"{colliderData['Particles']:,.0f}"
    except:
        formatted_particlesOwned = f"{colliderData['Particles']}"

    settings_advice['Information'].append(
        Advice(
            label=f"Particles Owned: {formatted_particlesOwned}",
            picture_class='particles',
        )
    )

    for atomName, atomValues in colliderData['Atoms'].items():
        settings_advice['Information'].append(
            Advice(
                label=(
                    f"{atomName}: {atomValues['Description']}"
                    f"<br>({atomValues['Value per Level']} per level)"
                    if atomName != 'Magnesium - Trap Compounder' else
                    f"{atomName}: {atomValues['Description']}"
                    f"<br>{colliderData['Magnesium Days']}/100 days since last retrap"
                    f"<br>({atomValues['Value per Level']} per level)"
                ),
                picture_class=atomName.split(' - ')[0],
                progression=atomValues['Level'],
                goal=atomValues['MaxLevel']
            )
        )

    #Alerts
    #Collider is not Off
    if colliderData['OnOffStatus'] == True:
        settings_advice['Alerts'].append(
            Advice(
                label=f"Collider switch status: {'On' if session_data.account.atom_collider['OnOffStatus'] else 'Off'}.<br>Recommended to select Off instead to avoid nuking your storage from a single misclick.",
                picture_class='collider-toggle',
            )
        )

    #Limit not set to 1050M
    if colliderData['StorageLimit'] != collider_storage_limit_list[-1]:
        settings_advice['Alerts'].append(
            Advice(
                label=f"Storage Limit: {session_data.account.atom_collider['StorageLimit']}M<br>Recommend to select {collider_storage_limit_list[-1]}M instead.",
                picture_class='',
                progression=session_data.account.atom_collider['StorageLimit'],
                goal=collider_storage_limit_list[-1],
                unit='M'
            )
        )

    #Sodium lower than Snail // 5
    if session_data.account.gaming['Imports']['Snail']['SnailRank'] < snail_max_possible_rank:
        if colliderData['Atoms']['Sodium - Snail Kryptonite']['Level'] < session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5:
            settings_advice['Alerts'].append(
                Advice(
                    label=f"Snail could reset from Rank {session_data.account.gaming['Imports']['Snail']['SnailRank']}"
                          f" to {colliderData['Atoms']['Sodium - Snail Kryptonite']['Level']*5}!"
                          f"<br>Level Sodium to {session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5}"
                          f" to protect Rank {5 * (session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5)}.",
                    picture_class="sodium",
                    progression=colliderData['Atoms']['Sodium - Snail Kryptonite']['Level'],
                    goal=session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5
                )
            )
            session_data.account.alerts_Advices['World 3'].append(Advice(
                    label=f"Snail could reset from Rank {session_data.account.gaming['Imports']['Snail']['SnailRank']}"
                          f" to {colliderData['Atoms']['Sodium - Snail Kryptonite']['Level'] * 5}!"
                          f"<br>Level {{{{ Sodium|#atom-collider }}}} to {session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5}"
                          f" to protect Rank {5 * (session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5)}.",
                    picture_class='sodium',
                    progression=colliderData['Atoms']['Sodium - Snail Kryptonite']['Level'],
                    goal=session_data.account.gaming['Imports']['Snail']['SnailRank'] // 5
            ))

    currentMaxedTowers = 0
    if colliderData['Atoms']["Carbon - Wizard Maximizer"]['Level'] < colliderData['Atoms']["Carbon - Wizard Maximizer"]['MaxLevel']:
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

    sp_id = session_data.account.gaming['SuperBits']['Isotope Discovery']
    ml_advice.append(
        Advice(
            label=f"Purchasing the final SuperBit in Gaming will increase the max level of all Atoms by 10",
            picture_class='red-bits',
            progression=int(sp_id['Unlocked']),
            goal=1
        )
    )

    ap = session_data.account.compass['Upgrades']['Atomic Potential']
    ml_advice.append(
        Advice(
            label=f"{{{{Compass|#the-compass}}}}: {ap['Path Name']}-{ap['Path Ordering']}: Atomic Potential: "
                  f"+{ap['Level']}/{ap['Max Level']} max Atom levels",
            picture_class=ap['Image'],
            progression=ap['Level'],
            goal=ap['Max Level']
        )
    )

    hb = session_data.account.event_points_shop['Bonuses']['Higgs Boson']
    ml_advice.append(
        Advice(
            label=f"{{{{Event Shop|#event-shop}}}}: Higgs Boson: {hb['Description']}",
            picture_class=hb['Image'],
            progression=int(hb['Owned']),
            goal=1
        )
    )

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
        label=f"W5 Taskboard Merit: {session_data.account.merits[4][6]['Level'] * 7}/{session_data.account.merits[4][6]['Level'] * 7}%"
              f"<br>The in-game display is incorrect. Don't @ me.",
        picture_class='merit-4-6',
        progression=session_data.account.merits[4][6]['Level'],
        goal=session_data.account.merits[4][6]['MaxLevel']
    ))

    cr_advice.append(Advice(
        label=f"""Neon - Damage N' Cheapener: {session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']}"""
        f"""/{session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['MaxLevel']}%""",
        picture_class='neon',
        progression=session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level'],
        goal=session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['MaxLevel']
    ))

    cr_advice.append(Advice(
        label=f"Superbit: Atom Redux: {10 * session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked']}/10%",
        picture_class='red-bits',
        progression=int(session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked']),
        goal=1
    ))

    cr_advice.append(Advice(
        label=f"Atom Collider building: {session_data.account.construction_buildings['Atom Collider']['Level'] / 10:.1f}"
              f"/{session_data.account.construction_buildings['Atom Collider']['MaxLevel'] / 10:.1f}%",
        picture_class='atom-collider',
        progression=session_data.account.construction_buildings['Atom Collider']['Level'],
        goal=session_data.account.construction_buildings['Atom Collider']['MaxLevel']
    ))

    cr_advice.append(Advice(
        label=f"Atom Split bubble: {session_data.account.alchemy_bubbles['Atom Split']['BaseValue']:.2f}/14%",
        picture_class='atom-split',
        progression=session_data.account.alchemy_bubbles['Atom Split']['Level'],
        resource=session_data.account.alchemy_bubbles['Atom Split']['Material']
    ))

    cr_advice.append(session_data.account.stamps['Atomic Stamp'].get_advice())

    cr_advice.append(Advice(
        label=f"{{{{Grimoire|#the-grimoire}}}}: Death of the Atom Price: {session_data.account.grimoire['Upgrades']['Death of the Atom Price']['Total Value']}%",
        picture_class=session_data.account.grimoire['Upgrades']['Death of the Atom Price']['Image'],
        progression=session_data.account.grimoire['Upgrades']['Death of the Atom Price']['Level'],
        goal=session_data.account.grimoire['Upgrades']['Death of the Atom Price']['Max Level']
    ))

    acc = session_data.account.compass['Upgrades']['Atomic Cost Crash']
    cr_advice.append(Advice(
        label=f"{{{{Compass|#the-compass}}}}: {acc['Path Name']}-{acc['Path Ordering']}: Atomic Cost Crash: {acc['Total Value']}%",
        picture_class=session_data.account.compass['Upgrades']['Atomic Cost Crash']['Image'],
        progression=session_data.account.compass['Upgrades']['Atomic Cost Crash']['Level'],
        goal=session_data.account.compass['Upgrades']['Atomic Cost Crash']['Max Level']
    ))

    cr_advice.append(Advice(
        label=f"Remaining cost: {session_data.account.atom_collider['CostReductionMulti']*100:.2f}%",
        picture_class='particles',
    ))

    cr_advice.append(Advice(
        label=f"Total discount: {session_data.account.atom_collider['CostDiscount']:.2f}% off",
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
    if session_data.account.cooking['MaxRemainingMeals'] < cooking_close_enough:
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

    player_atoms = session_data.account.atom_collider['Atoms']  # Player Atoms
    exclusionsList = getAtomExclusionsList()

    # Assess Tiers
    for tier_number, requirements in atoms_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)
        #Atom levels
        for atom_name, level in requirements.get('Atoms', {}).items():
            if atom_name not in exclusionsList and player_atoms[atom_name]['Level'] < level:
                add_subgroup_if_available_slot(collider_AdviceDict['Atoms'], subgroup_label)
                if subgroup_label in collider_AdviceDict['Atoms']:
                    collider_AdviceDict['Atoms'][subgroup_label].append(Advice(
                        label=atom_name,
                        picture_class=atom_name.split(' - ')[0],
                        progression=player_atoms[atom_name]['Level'],
                        goal=level
                    ))
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
