from models.models import Advice, AdviceGroup, AdviceSection
from consts import maxTiersPerGroup, statueTypeList, statues_progressionTiers, statueCount, max_VialLevel, stamp_maxes, statueExclusionsDict
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getStatueTypeAdviceGroup() -> AdviceGroup:
    type_AdviceList = []
    depositable_statues = 0
    for statueName, statueDetails in session_data.account.statues.items():
        if statueDetails['Type'] != statueTypeList[-1]:
            type_AdviceList.append(Advice(
                label=f"{statueName}: {statueDetails['Farmer']}",  #: {statueDetails['Type']}",
                picture_class=statueName,
                progression=session_data.account.assets.get(statueDetails['ItemName']).amount,
                goal=20000,
                resource=statueDetails['Target']
            ))
            if session_data.account.assets.get(statueDetails['ItemName']).amount >= 20000:  # and statueDetails['Type'] != statueTypeList[-1]:
                depositable_statues += 1

    if depositable_statues > 0:
        session_data.account.alerts_AdviceDict['World 1'].append(Advice(
            label=f"You can upgrade {depositable_statues} {{{{ Statues|#statues }}}} to {statueTypeList[-1]}!",
            picture_class="town-marble"
        ))

    for advice in type_AdviceList:
        mark_advice_completed(advice)

    type_AG = AdviceGroup(
        tier="",
        pre_string=f"Raise all statues to {statueTypeList[-1]}",
        advices=type_AdviceList
    )
    return type_AG


def getPreOnyxAdviceGroup() -> AdviceGroup:
    crystal_AdviceList = []
    deposit_AdviceList = []

    if not session_data.account.onyx_statues_unlocked:
        crystal_AdviceList.append(Advice(
            label="Complete the Monolith NPC's questline to unlock Onyx Statues",
            picture_class="monolith",
            resource="onyx-tools"
        ))
    crystal_AdviceList.append(Advice(
        label=f"W4 Demon Genie card: +{15 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Demon Genie'))}"
              f"/90% Crystal Mob Spawn Chance",
        picture_class="demon-genie-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Demon Genie"),
        goal=6
    ))
    crystal_AdviceList.append(Advice(
        label=f"W1 Poop card: +{10 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Poop'))}"
              f"/60% Crystal Mob Spawn Chance",
        picture_class="poop-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Poop"),
        goal=6
    ))
    crystal_AdviceList.append(Advice(
        label="Omega Nanochip: Top Left card doubler",
        picture_class="omega-nanochip",
        progression=session_data.account.labChips.get('Omega Nanochip', 0),
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label="Omega Motherboard: Bottom Right card doubler",
        picture_class="omega-motherboard",
        progression=session_data.account.labChips.get('Omega Motherboard', 0),
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label="Chocco Chip for more Crystal Mobs",
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label=f"Minimum 210 Crystallin Stamp: {session_data.account.stamps['Crystallin']['Level']} (+{session_data.account.stamps['Crystallin']['Value']:.3f}%)",
        picture_class="crystallin",
        progression=session_data.account.stamps['Crystallin']['Level'],
        goal=210  #stamp_maxes['Crystallin']
    ))
    crystal_AdviceList.append(Advice(
        label="Crystals 4 Dayys star talent",
        picture_class="crystals-4-dayys",
    ))
    bestCrystalBook = 0
    for jman in session_data.account.jmans:
        bestCrystalBook = max(bestCrystalBook, jman.max_talents.get("26", 0))
    crystal_AdviceList.append(Advice(
        label="Cmon Out Crystals (Jman only)",
        picture_class="cmon-out-crystals",
        progression=bestCrystalBook,
        goal=session_data.account.library['MaxBookLevel']
    ))
    crystal_AdviceList.append(Advice(
        label="Crescent Shrine",
        picture_class="crescent-shrine",
        progression=session_data.account.shrines.get("Crescent Shrine", {}).get("Level", 0),
        goal="∞"
    ))
    crystal_AdviceList.append(Advice(
        label="Chaotic Chizoar card increases Crescent Shrine",
        picture_class="chaotic-chizoar-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Chaotic Chizoar"),
        goal=6
    ))
    crystal_AdviceList.append(Advice(
        label=f"{{{{ Sailing|#sailing }}}}: Moai Head artifact to apply Shrines everywhere",
        picture_class="moai-head",
        progression=session_data.account.sailing['Artifacts']['Moai Head']['Level'],
        goal=1
    ))
    crystal_AdviceList.append(Advice(
        label=f"Minimum 1% Crystal Spawn Chance (per Tome): {session_data.account.raw_optlacc_dict[202] * 100:.3f}%",
        picture_class="crystal-carrot",
        progression=f"{session_data.account.raw_optlacc_dict[202]*100:.3f}",
        goal=3,
        unit="%"
    ))
    crystal_AdviceList.append(Advice(
        label=f"Minimum 10x Drop Rate (per Tome): {session_data.account.raw_optlacc_dict[200]:.2f}x",
        picture_class="drop-rate",
        progression=f"{session_data.account.raw_optlacc_dict[200]:.2f}",
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
    if session_data.account.labBonuses.get("My 1st Chemistry Set", {}).get("Enabled", False):
        vialValue *= 2
    vialValue *= session_data.account.vialMasteryMulti

    deposit_AdviceList.append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Skinny 0 Cal (Snake Skin) to level {max_VialLevel}",
        picture_class="snake-skin",
        progression=session_data.account.alchemy_vials['Skinny 0 Cal (Snake Skin)']['Level'],
        goal=max_VialLevel
    ))
    deposit_AdviceList.append(Advice(
        label=f"{{{{ Rift|#rift }}}} Bonus: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}/1.54x",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
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
        advices={'Crystal Chance and Drop Rate': crystal_AdviceList, 'Statue Value': deposit_AdviceList}
    )
    return crystal_AG

def setStatuesProgressionTier() -> AdviceSection:
    statues_AdviceDict = {
        "Tiers": {}
    }
    statues_AdviceGroupDict = {}
    statues_AdviceSection = AdviceSection(
        name="Statues",
        tier="Not Yet Evaluated",
        header="Best Statues tier met: Not Yet Evaluated. Recommended Star Sign actions",
        picture='Town_Marble.gif'
    )

    infoTiers = 0
    max_tier = max(statues_progressionTiers.keys()) - infoTiers
    tier_Statues = 0

    # Generate Advice
    for tierNumber, tierRequirements in statues_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        for statueName, statueDetails in session_data.account.statues.items():
            if statueName not in statueExclusionsDict[tierRequirements.get('Exclusions', 'None')]:
                #Trying to futureproof new tiers- If at least Gold, but not the max tier
                farmDetails = f": {statueDetails['Farmer']}" if 1 <= statueDetails['TypeNumber'] < len(statueTypeList) else ""
                farmResource = statueDetails['Target'] if 1 <= statueDetails['TypeNumber'] < len(statueTypeList) else ""
                if statueDetails['Level'] < tierRequirements.get('MinStatueLevel', 0):
                    if subgroupName not in statues_AdviceDict["Tiers"] and len(statues_AdviceDict["Tiers"]) < maxTiersPerGroup:
                        statues_AdviceDict["Tiers"][subgroupName] = []
                    if subgroupName in statues_AdviceDict["Tiers"]:
                        statues_AdviceDict['Tiers'][subgroupName].append(Advice(
                            label=f"Level up {statueName}{farmDetails}",
                            picture_class=statueName,
                            progression=statueDetails['Level'],
                            goal=tierRequirements.get('MinStatueLevel', 0),
                            resource=farmResource
                        ))
                if statueDetails['TypeNumber'] < tierRequirements.get('MinStatueTypeNumber', 0):
                    if subgroupName not in statues_AdviceDict["Tiers"] and len(statues_AdviceDict["Tiers"]) < maxTiersPerGroup:
                        statues_AdviceDict["Tiers"][subgroupName] = []
                    if subgroupName in statues_AdviceDict["Tiers"]:
                        statues_AdviceDict['Tiers'][subgroupName].append(Advice(
                            label=f"Raise {statueName} to {tierRequirements.get('MinStatueType', 'UnknownStatueType')}{farmDetails}",
                            picture_class=statueName,
                            progression=statueDetails['TypeNumber'] if statueDetails['TypeNumber'] < 1 else session_data.account.assets.get(statueDetails['ItemName']).amount,
                            goal=tierRequirements.get('MinStatueTypeNumber', 0) if statueDetails['TypeNumber'] < 1 else 20000,
                            resource=farmResource
                        ))
        if subgroupName not in statues_AdviceDict["Tiers"] and tier_Statues == tierNumber-1:
            tier_Statues = tierNumber

    # Generate AdviceGroups
    if session_data.account.maxed_statues < statueCount:
        statues_AdviceGroupDict['Crystals'] = getPreOnyxAdviceGroup()
    statues_AdviceGroupDict['Tiers'] = AdviceGroup(
        tier=tier_Statues,
        pre_string="Beef up those statues",
        advices=statues_AdviceDict["Tiers"]
    )

    #statues_AdviceGroupDict['Types'] = getStatueTypeAdviceGroup()

    # Generate AdviceSection
    overall_StatuesTier = min(max_tier + infoTiers, tier_Statues)
    tier_section = f"{overall_StatuesTier}/{max_tier}"
    statues_AdviceSection.pinchy_rating = overall_StatuesTier
    statues_AdviceSection.tier = tier_section
    statues_AdviceSection.groups = statues_AdviceGroupDict.values()
    if overall_StatuesTier >= max_tier:
        statues_AdviceSection.header = f"Best Statues tier met: {tier_section}<br>You best ❤️"
        statues_AdviceSection.complete = True
    else:
        statues_AdviceSection.header = f"Best Statues tier met: {tier_section}"

    return statues_AdviceSection
