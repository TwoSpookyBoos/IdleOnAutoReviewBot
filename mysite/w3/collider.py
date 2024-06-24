from flask import g as session_data

from consts import colliderStorageLimitList
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger

logger = get_logger(__name__)

def getColliderSettingsAdviceGroup() -> AdviceGroup:
    settings_advice = []

    if session_data.account.atom_collider['OnOffStatus'] == True:
        settings_advice.append(
            Advice(
                label=f"Collider switch status: {'On' if session_data.account.atom_collider['OnOffStatus'] else 'Off'}",
                picture_class="",
            )
        )

    if session_data.account.atom_collider['StorageLimit'] != colliderStorageLimitList[-1]:
        settings_advice.append(
            Advice(
                label=f"Storage Limit: {session_data.account.atom_collider['StorageLimit']}M",
                picture_class="",
                progression=session_data.account.atom_collider['StorageLimit'],
                goal=colliderStorageLimitList[-1],
                unit="M"
            )
        )

    try:
        formatted_particlesOwned = f"{session_data.account.atom_collider['Particles']:,.0f}"
    except:
        formatted_particlesOwned = f"{session_data.account.atom_collider['Particles']}"

    settings_advice.append(
        Advice(
            label=f"Particles Owned: {formatted_particlesOwned}",
            picture_class="particles",
        )
    )

    settings_ag = AdviceGroup(
        tier="",
        pre_string="Sanity check for Collider Settings",
        advices=settings_advice,
        post_string=f"Off and {colliderStorageLimitList[-1]}M are the recommended settings. It would require clicking BOTH to cause any harm."
    )
    return settings_ag

def getAtomsAdviceGroup() -> AdviceGroup:
    atoms_advice = []
    goal_level = 20 + (10 * session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked'])
    for atomName, atomValues in session_data.account.atom_collider['Atoms'].items():
        atoms_advice.append(
            Advice(
                label=atomName,
                picture_class=atomName.split(' - ')[0],
                progression=atomValues['Level'],
                goal=goal_level
            )
        )
    atoms_ag = AdviceGroup(
        tier="",
        pre_string="Sanity check for Atom Upgrades",
        advices=atoms_advice
    )
    return atoms_ag

def getCostReductionAdviceGroup() -> AdviceGroup:
    cr_advice = []

    sum_cost_reduction = (1 +
                          (
                            7 * session_data.account.merits[4][6]['Level']
                            + ((session_data.account.construction_buildings['Atom Collider']-1) // 10)
                            + 1 * session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']
                            + 10 * session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked']
                            + session_data.account.alchemy_bubbles['Atom Split']['BaseValue']
                            + session_data.account.stamps['Atomic Stamp']['Value']
                          )
                          / 100
                          )

    cr_advice.append(Advice(
        label=f"W5 Taskboard Merit: {session_data.account.merits[4][6]['Level'] * 7}%<br>The in-game display is still wrong after a year. Blame Lava.",
        picture_class='merit-4-6',
        progression=session_data.account.merits[4][6]['Level'],
        goal=4
    ))

    cr_advice.append(Advice(
        label=f"""Neon - Damage N' Cheapener: {session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']}%""",
        picture_class="neon",
        progression=session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level'],
        goal=20 + (10 * session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked'])
    ))

    cr_advice.append(Advice(
        label=f"Superbit: Atom Redux: {10 * session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked']}%",
        picture_class="red-bits",
        progression=1 if session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked'] else 0,
        goal=1
    ))

    cr_advice.append(Advice(
        label=f"Atom Collider building: {((session_data.account.construction_buildings['Atom Collider']-1) // 10)}%",
        picture_class="atom-collider",
        progression=session_data.account.construction_buildings['Atom Collider'],
        goal=191
    ))

    cr_advice.append(Advice(
        label=f"Atom Split bubble: {session_data.account.alchemy_bubbles['Atom Split']['BaseValue']:.2f}%",
        picture_class="atom-split",
        progression=session_data.account.alchemy_bubbles['Atom Split']['Level'],
        resource=session_data.account.alchemy_bubbles['Atom Split']['Material']
    ))

    cr_advice.append(Advice(
        label=f"Atomic Stamp: {session_data.account.stamps['Atomic Stamp']['Value']:.3f}%",
        picture_class="atomic-stamp",
        progression=session_data.account.stamps['Atomic Stamp']['Level'],
        resource=session_data.account.stamps['Atomic Stamp']['Material'],
    ))

    # cr_advice.append(Advice(
    #     label=f"Total cost reduction: {sum_cost_reduction-1:.2f}",
    #     picture_class='particles',
    # ))
    #
    # cr_advice.append(Advice(
    #     label=f"Total cost divisor: {sum_cost_reduction:.2f}",
    #     picture_class='particles',
    # ))

    cr_advice.append(Advice(
        label=f"Remaining cost: {(1/sum_cost_reduction)*100:.2f}%",
        picture_class='particles',
    ))

    cr_advice.append(Advice(
        label=f"Total cost discount: {(1 - (1 / sum_cost_reduction)) * 100:.2f}% off",
        picture_class='particles',
    ))

    cr_ag = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Atom Collider Cost Reduction",
        advices=cr_advice
    )
    return cr_ag

def setColliderProgressionTier() -> AdviceSection:
    collider_AdviceDict = {}
    collider_AdviceGroupDict = {}
    collider_AdviceSection = AdviceSection(
        name="Atom Collider",
        tier="Not Yet Evaluated",
        header="",
        picture="Collider.png",
    )

    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        collider_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return collider_AdviceSection
    elif session_data.account.construction_buildings.get("Atom Collider", 0) < 1:
        collider_AdviceSection.header = "Come back after unlocking the Atom Collider within the Construction skill in World 3!"
        return collider_AdviceSection

    max_tier = 0
    tier_atomLevels = 0

    # Generate AdviceGroups
    collider_AdviceGroupDict['ColliderSettings'] = getColliderSettingsAdviceGroup()
    collider_AdviceGroupDict['AllAtoms'] = getAtomsAdviceGroup()
    collider_AdviceGroupDict['CostReduction'] = getCostReductionAdviceGroup()

    # Generate AdviceSection
    overall_ColliderTier = min(max_tier, tier_atomLevels)  # Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_ColliderTier}/{max_tier}"
    collider_AdviceSection.tier = tier_section
    collider_AdviceSection.pinchy_rating = overall_ColliderTier
    collider_AdviceSection.groups = collider_AdviceGroupDict.values()
    if overall_ColliderTier == max_tier:
        collider_AdviceSection.header = f"Best Collider tier met: {tier_section}<br>You best ❤️"
    else:
        collider_AdviceSection.header = f"Best Collider tier met: {tier_section}"
    return collider_AdviceSection
    