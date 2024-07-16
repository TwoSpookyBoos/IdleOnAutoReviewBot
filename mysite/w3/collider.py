from flask import g as session_data
from consts import colliderStorageLimitList, buildingsTowerMaxLevel, atoms_progressionTiers, maxTiersPerGroup, cookingCloseEnough
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
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
            picture_class="particles",
        )
    )

    if not session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked']:
        settings_advice['Information'].append(
            Advice(
                label=f"Purchasing the final SuperBit in Gaming will increase the max level of all Atoms from 20 to 30",
                picture_class='red-bits',
            )
        )

    for atomName, atomValues in colliderData['Atoms'].items():
        settings_advice['Information'].append(
            Advice(
                label=atomName,
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
                label=f"Collider switch status: {'On' if session_data.account.atom_collider['OnOffStatus'] else 'Off'}.<br>Recommended to select Off instead.",
                picture_class="collider-toggle",
            )
        )

    #Limit not set to 1050M
    if colliderData['StorageLimit'] != colliderStorageLimitList[-1]:
        settings_advice['Alerts'].append(
            Advice(
                label=f"Storage Limit: {session_data.account.atom_collider['StorageLimit']}M<br>Recommend to select {colliderStorageLimitList[-1]}M instead.",
                picture_class="",
                progression=session_data.account.atom_collider['StorageLimit'],
                goal=colliderStorageLimitList[-1],
                unit="M"
            )
        )

    #Sodium lower than Snail // 5
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

    #Neon would cheapen the next Helium upgrade
    for heliumLevel, neonLevel in {6: 0, 7: 2, 8: 10, 9: 21, 10: 30}.items():
        if colliderData['Atoms']['Helium - Talent Power Stacker']['Level'] == heliumLevel-1:
            if colliderData['Atoms']["Neon - Damage N' Cheapener"]['Level'] < neonLevel:
                settings_advice['Alerts'].append(
                    Advice(
                        label=f"Neon can be increased to {neonLevel} to cheapen Helium {heliumLevel}",
                        picture_class="neon",
                        progression=colliderData['Atoms']["Neon - Damage N' Cheapener"]['Level'],
                        goal=neonLevel
                    )
                )

    currentMaxedTowers = 0
    if colliderData['Atoms']["Carbon - Wizard Maximizer"]['Level'] < colliderData['Atoms']["Carbon - Wizard Maximizer"]['MaxLevel']:
        for buildingName, buildingValuesDict in session_data.account.construction_buildings.items():
            if buildingValuesDict['Type'] == 'Tower':
                if buildingValuesDict['Level'] == buildingValuesDict['MaxLevel'] and buildingValuesDict['MaxLevel'] < buildingsTowerMaxLevel:
                    currentMaxedTowers += 1

    if currentMaxedTowers > 0:
        settings_advice['Alerts'].append(
            Advice(
                label=f"{currentMaxedTowers} TD Tower{pl(currentMaxedTowers)} at max level."
                      f"<br>Level up Carbon to increase your max Tower levels by 2.",
                picture_class="carbon",
            )
        )

    settings_ag = AdviceGroup(
        tier="",
        pre_string="Collider Alerts and General Information",
        advices=settings_advice,
        post_string=f""
    )
    settings_ag.remove_empty_subgroups()
    return settings_ag

def getCostReductionAdviceGroup() -> AdviceGroup:
    cr_advice = []



    cr_advice.append(Advice(
        label=f"W5 Taskboard Merit: {session_data.account.merits[4][6]['Level'] * 7}/28%"
              f"<br>The in-game display is incorrect. Don't @ me.",
        picture_class='merit-4-6',
        progression=session_data.account.merits[4][6]['Level'],
        goal=4
    ))

    cr_advice.append(Advice(
        label=f"""Neon - Damage N' Cheapener: {session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level']}/30%""",
        picture_class="neon",
        progression=session_data.account.atom_collider['Atoms']["Neon - Damage N' Cheapener"]['Level'],
        goal=20 + (10 * session_data.account.gaming['SuperBits']['Isotope Discovery']['Unlocked'])
    ))

    cr_advice.append(Advice(
        label=f"Superbit: Atom Redux: {10 * session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked']}/10%",
        picture_class="red-bits",
        progression=1 if session_data.account.gaming['SuperBits']['Atom Redux']['Unlocked'] else 0,
        goal=1
    ))

    cr_advice.append(Advice(
        label=f"Atom Collider building: {((session_data.account.construction_buildings['Atom Collider']['Level']-1) // 10)}/19%",
        picture_class="atom-collider",
        progression=session_data.account.construction_buildings['Atom Collider']['Level'],
        goal=191
    ))

    cr_advice.append(Advice(
        label=f"Atom Split bubble: {session_data.account.alchemy_bubbles['Atom Split']['BaseValue']:.2f}/14%",
        picture_class="atom-split",
        progression=session_data.account.alchemy_bubbles['Atom Split']['Level'],
        resource=session_data.account.alchemy_bubbles['Atom Split']['Material']
    ))

    cr_advice.append(Advice(
        label=f"Atomic Stamp: {session_data.account.stamps['Atomic Stamp']['Value']:.3f}/20%",
        picture_class="atomic-stamp",
        progression=session_data.account.stamps['Atomic Stamp']['Level'],
        resource=session_data.account.stamps['Atomic Stamp']['Material'],
    ))

    cr_advice.append(Advice(
        label=f"Remaining cost: {session_data.account.atom_collider['CostReductionMulti']*100:.2f}%",
              #f" / {(1 / session_data.account.atom_collider['CostReductionMax'])*100:.2f}%",
        picture_class='particles',
    ))

    cr_advice.append(Advice(
        label=f"Total discount: {session_data.account.atom_collider['CostDiscount']:.2f}% / "
              f"{session_data.account.atom_collider['CostDiscountMax']:.2f}% off",
        picture_class='particles',
    ))

    for advice in cr_advice:
        mark_advice_completed(advice)

    cr_ag = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Atom Collider Cost Reduction",
        advices=cr_advice
    )
    return cr_ag

def getAtomExclusionsList() -> list[str]:
    exclusionsList = []
    # If cooking is basically finished thanks to NMLB, exclude Fluoride's cooking speed
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        exclusionsList.append('Fluoride - Void Plate Chef')

    return exclusionsList

def setColliderProgressionTier() -> AdviceSection:
    collider_AdviceDict = {
        'Atoms': {}
    }
    collider_AdviceGroupDict = {}
    collider_AdviceSection = AdviceSection(
        name="Atom Collider",
        tier="Not Yet Evaluated",
        header="",
        picture="Collider.gif",
    )

    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        collider_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        return collider_AdviceSection
    elif session_data.account.construction_buildings['Atom Collider']['Level'] < 1:
        collider_AdviceSection.header = "Come back after unlocking the Atom Collider within the Construction skill in World 3!"
        return collider_AdviceSection

    max_tier = max(atoms_progressionTiers.keys())
    tier_atomLevels = 0
    pAtoms = session_data.account.atom_collider['Atoms']  #Player Atoms

    for tier, tierRequirements in atoms_progressionTiers.items():
        subgroupName = f"To reach Tier {tier}"
        #Atom levels
        for rAtom, rLevel in tierRequirements.get('Atoms', {}).items():
            if pAtoms[rAtom]['Level'] < rLevel:
                if subgroupName not in collider_AdviceDict['Atoms'] and len(collider_AdviceDict['Atoms']) < maxTiersPerGroup:
                    collider_AdviceDict['Atoms'][subgroupName] = []
                if subgroupName in collider_AdviceDict['Atoms']:
                    collider_AdviceDict['Atoms'][subgroupName].append(Advice(
                        label=rAtom,
                        picture_class=rAtom.split(' - ')[0],
                        progression=pAtoms[rAtom]['Level'],
                        goal=rLevel
                    ))
        if tier_atomLevels == tier-1 and subgroupName not in collider_AdviceDict['Atoms']:
            tier_atomLevels = tier

    # Generate AdviceGroups
    collider_AdviceGroupDict['ColliderSettings'] = getColliderSettingsAdviceGroup()
    collider_AdviceGroupDict['CostReduction'] = getCostReductionAdviceGroup()
    collider_AdviceGroupDict['Atoms'] = AdviceGroup(
        tier=tier_atomLevels,
        pre_string="Level Priority Atoms",
        advices=collider_AdviceDict['Atoms']
    )

    # Generate AdviceSection
    overall_ColliderTier = min(max_tier, tier_atomLevels)  # Looks silly, but may get more evaluations in the future
    tier_section = f"{overall_ColliderTier}/{max_tier}"
    collider_AdviceSection.tier = tier_section
    collider_AdviceSection.pinchy_rating = overall_ColliderTier
    collider_AdviceSection.groups = collider_AdviceGroupDict.values()
    if overall_ColliderTier >= max_tier:
        collider_AdviceSection.header = f"Best Collider tier met: {tier_section}<br>You best ❤️"
        collider_AdviceSection.complete = True
    else:
        collider_AdviceSection.header = f"Best Collider tier met: {tier_section}"
    return collider_AdviceSection
    