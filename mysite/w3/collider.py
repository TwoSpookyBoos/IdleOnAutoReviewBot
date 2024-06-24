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
    