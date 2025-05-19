from models.models import Advice, AdviceGroup, AdviceSection
from consts import statueTypeList, statues_progressionTiers, statueCount, max_VialLevel, break_you_best
from utils.data_formatting import mark_advice_completed, safer_get
from utils.logging import get_logger
from flask import g as session_data

from utils.text_formatting import pl

logger = get_logger(__name__)


def getPreOnyxAdviceGroup() -> AdviceGroup:
    crystal_AdviceList = []
    deposit_AdviceList = []

    if not session_data.account.onyx_statues_unlocked:
        crystal_AdviceList.append(Advice(
            label="Complete the Monolith NPC's questline to unlock Onyx Statues",
            picture_class="monolith",
            resource="onyx-tools",
            progression=0,
            goal=1
        ))
    crystal_AdviceList.append(Advice(
        label="Chocco Chip for more Crystal Mobs",
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    cards = ['Demon Genie', 'Poop']
    for card_name in cards:
        crystal_AdviceList.append(next(c for c in session_data.account.cards if c.name == card_name).getAdvice('Minimum 3 star'))

    crystal_AdviceList.append(Advice(
        label=f"Minimum 100 Crystallin Stamp: {session_data.account.stamps['Crystallin']['Level']} (+{session_data.account.stamps['Crystallin']['Total Value']:.3f}%)",
        picture_class='crystallin',
        progression=session_data.account.stamps['Crystallin']['Level'],
        goal=100  #stamp_maxes['Crystallin']
    ))
    crystal_AdviceList.append(Advice(
        label=f"Star Talent 'Crystals 4 Dayys' obtained by completing Picnic Stowaway's quest: \"The Last Supper, at Least for Today\"",
        picture_class="crystals-4-dayys",
        progression=int(any([char.max_talents.get('619', 0) > 0 for char in session_data.account.all_characters])),
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Moai Head artifact to apply Shrines everywhere",
        picture_class="moai-head",
        progression=session_data.account.sailing['Artifacts']['Moai Head']['Level'],
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label=f"Minimum 1% (1 in 100) {{{{ Crystal Spawn Chance|#active }}}} on Non-Jman:"
              f"<br>{session_data.account.highest_crystal_spawn_chance*100:.4f}%"
              f" (1 in {100/(session_data.account.highest_crystal_spawn_chance*100):.2f})",
        picture_class="crystal-carrot",
        progression=f"{session_data.account.highest_crystal_spawn_chance * 100:.4f}",
        goal=1,
        unit="%"
    ))
    bestOrbBook = 0
    for dk in session_data.account.dks:
        bestOrbBook = max(bestOrbBook, dk.max_talents.get("168", 0))
    crystal_AdviceList.append(Advice(
        label=f"Level {bestOrbBook}/{session_data.account.library['MaxBookLevel']} booked Orb of Remembrance talent (Divine Knight only)",
        picture_class="orb-of-remembrance",
        progression=bestOrbBook,
        goal=session_data.account.library['MaxBookLevel']
    ))
    tome_DropChance = safer_get(session_data.account.raw_optlacc_dict, 200, 1)
    crystal_AdviceList.append(Advice(
        label=f"Minimum 10x Drop Rate (per Tome): {tome_DropChance:.2f}x",
        picture_class="drop-rate",
        progression=f"{tome_DropChance:.2f}",
        goal=10,
    ))

    #Statue Value
    deposit_AdviceList.append(Advice(
        label=f"Startue Exp bubble: "
              f"{session_data.account.alchemy_bubbles['Startue Exp']['BaseValue']:.3f}/20%+ minimum",
        picture_class="startue-exp",
        progression=session_data.account.alchemy_bubbles['Startue Exp']['Level'],
        goal=240,
        resource=session_data.account.alchemy_bubbles['Startue Exp']['Material']
    ))

    vialValue = session_data.account.alchemy_vials['Skinny 0 Cal (Snake Skin)']['Value']

    deposit_AdviceList.append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Skinny 0 Cal (Snake Skin) to level {max_VialLevel}",
        picture_class="snake-skin",
        progression=session_data.account.alchemy_vials['Skinny 0 Cal (Snake Skin)']['Level'],
        goal=max_VialLevel
    ))
    deposit_AdviceList.append(Advice(
        label="Total Vial value (100% hardcap)",
        picture_class="vials",
        progression=f"{min(100, vialValue):.2f}",
        goal=100,
    ))

    for advicelist in [crystal_AdviceList, deposit_AdviceList]:
        for advice in advicelist:
            mark_advice_completed(advice)

    crystal_AG = AdviceGroup(
        tier="",
        pre_string="Info- To-Do list before dedicated Onyx Statue farming",
        advices={'Crystal Chance and Drop Rate': crystal_AdviceList, 'Statue Value': deposit_AdviceList},
        informational=True
    )
    return crystal_AG

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    statues_AdviceDict = {
        "Tiers": {}
    }
    infoTiers = 0
    max_tier = max(statues_progressionTiers.keys()) - infoTiers
    tier_Statues = 0
    depositable_statues = 0

    # Assess Tiers
    for tierNumber, tierRequirements in statues_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        for statueName, statueDetails in session_data.account.statues.items():
            # Trying to futureproof new tiers- If at least Gold, but not the max tier
            farmDetails = f": {statueDetails['Farmer']}" if 0 <= statueDetails['TypeNumber'] < len(statueTypeList) else ""
            farmResource = statueDetails['Target'] if 0 <= statueDetails['TypeNumber'] < len(statueTypeList) else ""
            if 'SpecificLevels' in tierRequirements:
                if statueName in tierRequirements['SpecificLevels']:
                    if statueDetails['Level'] < tierRequirements['SpecificLevels'][statueName]:
                        if subgroupName not in statues_AdviceDict["Tiers"] and len(statues_AdviceDict["Tiers"]) < session_data.account.maxSubgroupsPerGroup:
                            statues_AdviceDict["Tiers"][subgroupName] = []
                        if subgroupName in statues_AdviceDict["Tiers"]:
                            statues_AdviceDict['Tiers'][subgroupName].append(Advice(
                                label=f"Level up {statueName}{farmDetails}",
                                picture_class=statueName,
                                progression=statueDetails['Level'],
                                goal=tierRequirements['SpecificLevels'][statueName],
                                resource=farmResource
                            ))
            if 'SpecificTypes' in tierRequirements:
                if statueName in tierRequirements['SpecificTypes']:
                    if statueDetails['TypeNumber'] < tierRequirements.get('MinStatueTypeNumber', 0):
                        if subgroupName not in statues_AdviceDict["Tiers"] and len(statues_AdviceDict["Tiers"]) < session_data.account.maxSubgroupsPerGroup:
                            statues_AdviceDict["Tiers"][subgroupName] = []
                        if subgroupName in statues_AdviceDict["Tiers"]:
                            statues_AdviceDict['Tiers'][subgroupName].append(Advice(
                                label=f"Raise {statueName} to {tierRequirements.get('MinStatueType', 'UnknownStatueType')}"
                                      f"{farmDetails if tierRequirements.get('MinStatueType', 'UnknownStatueType') != 'Gold' else ''}"
                                      f"{'<br>Reminder: You need to raise this statue to Gold first!' if tierRequirements.get('MinStatueType', 'UnknownStatueType') == 'Onyx' and statueDetails['Level'] == 0 else ''}",
                                picture_class=statueName,
                                progression=statueDetails['TypeNumber'] if statueDetails['TypeNumber'] < 1 else session_data.account.stored_assets.get(
                                    statueDetails['ItemName']).amount,
                                goal=20000 if tierRequirements.get('MinStatueType', 'UnknownStatueType') == 'Onyx' else tierRequirements.get(
                                    'MinStatueTypeNumber', 0),
                                resource="coins" if tierRequirements.get('MinStatueType', 'UnknownStatueType') == 'Gold' else farmResource
                            ))
                        if session_data.account.stored_assets.get(statueDetails['ItemName']).amount >= 20000 and statueDetails['Type'] != statueTypeList[-1]:
                            depositable_statues += 1
        if subgroupName not in statues_AdviceDict["Tiers"] and tier_Statues == tierNumber - 1:
            tier_Statues = tierNumber

    # Generate Alerts
    if depositable_statues > 0 and session_data.account.onyx_statues_unlocked:
        session_data.account.alerts_AdviceDict['World 1'].append(Advice(
            label=f"You can upgrade {depositable_statues} {{{{ Statue{pl(depositable_statues)}|#statues }}}} to {statueTypeList[-1]}!",
            picture_class="town-marble"
        ))

    tiers_ag = AdviceGroup(
        tier=tier_Statues,
        pre_string="Beef up those statues",
        advices=statues_AdviceDict["Tiers"]
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_Statues)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + infoTiers

def getStatuesAdviceSection() -> AdviceSection:
    # Generate AdviceGroups
    statues_AdviceGroupDict = {}
    statues_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    if session_data.account.maxed_statues < statueCount:
        statues_AdviceGroupDict['Crystals'] = getPreOnyxAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    statues_AdviceSection = AdviceSection(
        name="Statues",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Statues tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Town_Marble.gif',
        groups=statues_AdviceGroupDict.values()
    )

    return statues_AdviceSection
