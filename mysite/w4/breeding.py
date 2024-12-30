import copy
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl, notateNumber
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfArtifacts, numberOfArtifactTiers, breeding_progressionTiers, getReadableVialNames, territoryNames, break_you_best, \
    maxFarmingCrops, breedabilityDaysList, infinity_string

logger = get_logger(__name__)

def getShinyExclusions():
    shinyExclusionsDict = {
        "Infinite Star Signs": True,
        "Lower Minimum Travel Time for Sailing": False,
        "Higher Artifact Find Chance": False,
        "Base Critter Per Trap": False,
        "Faster Shiny Pet Lv Up Rate": False
        }

    # if Infinite Star Signs are unlocked, set False (as in False, the recommendation should NOT be excluded), otherwise default True
    if session_data.account.rift['InfiniteStars']:
        shinyExclusionsDict["Infinite Star Signs"] = False

    # if all artifacts are Eldritch tier, append True (as in True, the recommendation SHOULD be excluded), otherwise False
    if session_data.account.sum_artifact_tiers >= (numberOfArtifacts * numberOfArtifactTiers):
        shinyExclusionsDict["Lower Minimum Travel Time for Sailing"] = True
        shinyExclusionsDict["Higher Artifact Find Chance"] = True

    try:
        critterVialsList = [
            getReadableVialNames(23),  #Crabbo
            getReadableVialNames(31),  #Mousey
            getReadableVialNames(37),  #Bunny
            getReadableVialNames(40),  #Honker
            getReadableVialNames(47),  #Blobfish
            getReadableVialNames(74),  #Tuttle
        ]
        for vialName in critterVialsList:
            if session_data.account.alchemy_vials.get(vialName, {}).get("Level", 0) < 13:
                break
            elif vialName == critterVialsList[-1]:
                shinyExclusionsDict["Base Critter Per Trap"] = True
    except:
        logger.exception(f"Unable to get Critter Vials. Defaulting to INCLUDE Base Critter shiny pets.")

    shinyExclusionsDict["Faster Shiny Pet Lv Up Rate"] = session_data.account.sneaking['JadeEmporium']["Science Crayon"]['Obtained']

    return shinyExclusionsDict

def getTerritoryName(territoryIndex: int) -> str:
    try:
        return territoryNames[int(territoryIndex)]
    except:
        return f"Unknown Territory {territoryIndex}"

def getSpiceImage(territoryIndex: int) -> str:
    try:
        return f"{territoryNames[int(territoryIndex)]}-spice"
    except:
        return f"UnknownSpice{territoryIndex}"

def getShinySpeedSourcesAdviceGroup(fasterShinyPetTotalLevels) -> AdviceGroup:
    mga = "Multi Group A- Summoning Winner Bonus"
    mgb = "Multi Group B- Lamp Wish"
    mgc = "Multi Group C- Everything Else"
    sps_adviceDict = {
        mga: [],
        mgb: [],
        mgc: []
    }

#Multi Group A
    red8beat = session_data.account.summoning['Battles']['Red'] >= 8
    cyan13beat = session_data.account.summoning['Battles']['Cyan'] >= 13
    sps_adviceDict[mga].append(Advice(
        label=f"Summoning match Red8: "
              f"+{1.88 * red8beat}/1.88{'' if red8beat else '. Not yet beaten.'}",
        picture_class="citringe",
        progression=1 if red8beat else 0,
        goal=1
    ))
    sps_adviceDict[mga].append(Advice(
        label=f"Summoning match Cyan13: "
              f"+{3.45 * cyan13beat}/3.45{'' if cyan13beat else '. Not yet beaten.'}",
        picture_class="minichief-spirit",
        progression=1 if cyan13beat else 0,
        goal=1
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        sps_adviceDict[mga].append(advice)
    sps_adviceDict[mga].extend(session_data.account.summoning['WinnerBonusesSummaryFull'])

#Multi Group B
    lamp_cavern = session_data.account.caverns['Caverns']['The Lamp']
    sps_adviceDict[mgb].append(Advice(
        label=f"{{{{Lamp|#glowshroom-tunnels}}}} Wish: World 4 Stuff: +{lamp_cavern['WishTypes'][4]['BonusList'][1]}%",
        picture_class=f"cavern-{lamp_cavern['CavernNumber']}",
        progression=lamp_cavern['WishTypes'][4]['BonusList'][1],
        goal=infinity_string
    ))

#Multi Group C
    sps_adviceDict[mgc].append(Advice(
        label=f"Total Farming crops discovered: {session_data.account.farming['CropsUnlocked']}/{maxFarmingCrops}",
        picture_class='crop-depot',
        progression=session_data.account.farming['CropsUnlocked'],
        goal=maxFarmingCrops
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"{{{{Science Crayon|#farming}}}} Total: {session_data.account.farming['Depot'][5]['Value']:,.2f}",
        picture_class=session_data.account.farming['Depot'][5]['Image'],
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"Lab Jewel: Emerald Ulthurite",
        picture_class='emerald-ulthurite',
        progression=1 if session_data.account.labJewels["Emerald Ulthurite"]["Enabled"] else 0,
        goal=1
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"Faster Shiny Pet Lv Up Rate Shiny Pets: "
              f"+{3 * fasterShinyPetTotalLevels}% total",
        picture_class='green-mushroom-shiny'
    ))
    sps_adviceDict[mgc].append(Advice(
        label=f"Grand Martial of Shinytown: "
              f"+{session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['Value']}%",
        picture_class='breeding-bonus-11',
        progression=session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['Level'],
        goal=session_data.account.breeding['Upgrades']['Grand Martial of Shinytown']['MaxLevel'],
    ))

    sps_adviceDict[mgc].append(Advice(
        label=f"Star Sign: Breedabilli: "
              f"+{15 * session_data.account.star_signs.get('Breedabilli', {}).get('Unlocked', False)}/15%",
        picture_class='breedabilli',
        progression=1 if session_data.account.star_signs.get('Breedabilli', {}).get('Unlocked', False) else 0,
        goal=1
    ))
    sps_adviceDict[mgc].append(session_data.account.star_sign_extras['SeraphAdvice'])
    sps_adviceDict[mgc].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])

    for group_name in sps_adviceDict:
        for advice in sps_adviceDict[group_name]:
            mark_advice_completed(advice)

    sps_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Shiny Pet Level Rate",
        advices=sps_adviceDict,
        informational=True
    )
    return sps_AdviceGroup

def getBreedabilityAdviceGroup():
    b_advices = []
    all_breedability = {
        k:v
        for worldIndex in session_data.account.breeding['Species'].keys()
        for k,v in session_data.account.breeding['Species'][worldIndex].items()
    }
    sorted_breedability = sorted(
        all_breedability.items(),
        key=lambda pet: pet[1]['BreedabilityDays'],
        reverse=True
    )
    for pet in sorted_breedability:
        b_advices.append(Advice(
            label=f"{pet[0]}"
                  f"<br>Breedability Multi: {pet[1]['BreedabilityMulti']:.3f}x"
                  f"<br>Heart VII: {notateNumber('Match', pet[1]['BreedabilityDays'], 0, 'K' if pet[1]['BreedabilityDays'] >= 1000 else '')} / "
                  f"{notateNumber('Match', breedabilityDaysList[-4], 0, 'K')}",
            picture_class=pet[0],
            progression=f"{pet[1]['BreedabilityDays'] / breedabilityDaysList[-4]:.2%}",
            resource=pet[1]['BreedabilityHeart']
        ))

    for advice in b_advices:
        mark_advice_completed(advice)
    
    b_ag = AdviceGroup(
        tier='',
        pre_string="Informational- Breedability Multi and Heart VII Progress",
        advices=b_advices,
        informational=True
    )
    return b_ag

def getActiveBMAdviceGroup() -> AdviceGroup:
    abm_adviceDict = {
        "Prerequisites": [],
        "Equipment": [],
        "Cards": [],
        "Lab Chips": [],
        "Active Fight": []
    }
    # Active BM Prerequisites
    abm_adviceDict["Prerequisites"].append(Advice(
        label="Have a Voidwalker in your family",
        picture_class="voidwalker-icon",
        progression=f"{1 if 'Voidwalker' in session_data.account.classes else 0}",
        goal=1
    ))
    abm_adviceDict["Prerequisites"].append(Advice(
        label="Voidwalker: Enhancement Eclipse talent leveled to 150+",
        picture_class="enhancement-eclipse",
        progression=max([vman.max_talents.get("49", 0) for vman in session_data.account.vmans], default=0),
        goal=150
    ))
    abm_adviceDict["Prerequisites"].append(Advice(
        label="Have a Beast Master in your family",
        picture_class="beast-master-icon",
        progression=f"{1 if 'Beast Master' in session_data.account.classes else 0}",
        goal=1
    ))
    abm_adviceDict["Prerequisites"].append(Advice(
        label="All ACTIVE-ONLY kills with your Beast Master now have a 50% chance to speed up progress for the Fenceyard, Spice collection, and Egg production! Crystal Mobs count 😄",
        picture_class="whale-wallop"))

    # Equipment
    abm_adviceDict["Equipment"].append(Advice(
        label="Respawn Keychains: +6% respawn per roll (Or +10% from FOMO shop)",
        picture_class="negative-7-chain"
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label="The Divine Scarf: +20% respawn",
        picture_class="the-divine-scarf"
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label="Spine Tingler Sniper: +12% respawn",
        picture_class="spine-tingler-sniper"
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label="Serrated Chest of the Divine: +8% respawn",
        picture_class="serrated-chest-of-the-divine"
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label="Spiked Leggings of the Divine: +4% respawn",
        picture_class="spiked-leggings-of-the-divine"
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label=f"Star Sign: Breedabilli: +15% Shiny Pet Level Speed",
        picture_class='breedabilli'
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label=f"Star Sign: Grim Reaper Major: +4% respawn",
        picture_class='grim-reaper-major'
    ))
    abm_adviceDict["Equipment"].append(Advice(
        label=f"Star Sign: Grim Reaper: +2% respawn",
        picture_class='grim-reaper'
    ))

    # Cards
    abm_adviceDict["Cards"].append(Advice(
        label=f"W4 Demon Genie card: +15% Crystal Mob Spawn Chance per rank",
        picture_class="demon-genie-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Demon Genie"),
        goal=6
    ))
    abm_adviceDict["Cards"].append(Advice(
        label=f"W1 Poop card: +10% Crystal Mob Spawn Chance per rank",
        picture_class="poop-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Poop"),
        goal=6
    ))
    abm_adviceDict["Cards"].append(Advice(
        label=f"Fill the rest with: Drop Rate, Active EXP, or Damage if needed.",
        picture_class="locked-card"))

    # Lab Chips
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Chocco Chip for more Crystal Mobs",
        picture_class="chocolatey-chip",
        progression=session_data.account.labChips.get('Chocolatey Chip', 0),
        goal=1
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Omega Nanochip: Top Left card doubler",
        picture_class="omega-nanochip",
        progression=session_data.account.labChips.get('Omega Nanochip', 0),
        goal=1
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Omega Motherboard: Bottom Right card doubler",
        picture_class="omega-motherboard",
        progression=session_data.account.labChips.get('Omega Motherboard', 0),
        goal=1
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Silkrode Software aka Keychain Doubler ONLY IF your top Keychain gives more than 10% total respawn",
        picture_class="silkrode-software"
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Silkrode Processor aka Pendant Doubler ONLY IF your Pendant gives more than 10% total respawn",
        picture_class="silkrode-processor"
    ))
    abm_adviceDict["Lab Chips"].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Fill any remaining slots with Galvanic Nanochip: +10% respawn per chip",
        picture_class="galvanic-nanochip"
    ))

    # Active play
    abm_adviceDict["Active Fight"].append(Advice(
        label="Place UwU Rawrrr first on your attack talent bar. The order of the other attacks doesn't seem to matter.",
        picture_class="uwu-rawrrr"))
    abm_adviceDict["Active Fight"].append(Advice(
        label="Finally, Auto against Samurai Guardians",
        picture_class="samurai-guardian"))
    abm_adviceDict["Active Fight"].append(Advice(
        label=f"W6 Taskboard Merit: +10% W6 respawn if fighting Samurai Guardians",
        picture_class='merit-5-1',
        progression=session_data.account.merits[5][1]["Level"],
        goal=10
    ))

    abm_adviceDict["Active Fight"].append(Advice(
        label="Auto against Tremor Wurms instead if not ready for Samurai Guardians",
        picture_class="tremor-wurm"))
    abm_adviceDict["Active Fight"].append(Advice(
        label=f"W5 Taskboard Merit: +20% W5 respawn if fighting Tremor Wurms",
        picture_class='merit-4-1',
        progression=session_data.account.merits[4][1]["Level"],
        goal=10
    ))

    for subgroupName in abm_adviceDict:
        for advice in abm_adviceDict[subgroupName]:
            mark_advice_completed(advice)

    abm_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Active BM setup earns around 4-6x Breeding progress",
        advices=abm_adviceDict,
        informational=True
    )
    return abm_AdviceGroup

def getBreedingProgressionTiersAdviceGroups(breedingDict):
    breeding_AdviceDict = {
        "UnlockedTerritories": {"Unlock more Spice Territories": [], "Recommended Territory Team (Left to Right)": []},
        "MaxArenaWave": {"Recommended Arena Team (Left to Right)": []},
        "ShinyLevels": {},
        "ShinyLevelsTierList": {}
    }
    breeding_AdviceGroupDict = {}

    progressionTiersBreeding = copy.deepcopy(breeding_progressionTiers)
    info_tiers = 0
    max_tier = max(progressionTiersBreeding.keys()) - info_tiers
    tier_UnlockedTerritories = 0
    tier_MaxArenaWave = 0
    tier_ShinyLevels = 0
    nextArenaWaveUnlock = 0
    recommendedTerritoryCompsList: dict[int, list[list[str]]] = {
        0: [
            [],
            []],
        1: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        2: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        3: [
            ['Rattler or Mercenary', 'Cursory', 'Refiller', 'Defender'],
            ['rattler', 'cursory', 'refiller', 'defender']],
        4: [
            ['Rattler', 'Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['rattler', 'monolithic', 'refiller', 'defender', 'refiller']],
        5: [
            ['Rattler', 'Looter', 'Monolithic', 'Refiller', 'Defender', 'Refiller'],
            ['rattler', 'looter', 'monolithic', 'refiller', 'defender', 'refiller']],
        6: [
            # ['Peapeapod or Rattler', 'Looter', 'Trasher (Manually click to delete enemy attacks!)', 'Refiller', 'Refiller', 'Lazarus or Filler'],
            # ['peapeapod', 'looter', 'trasher', 'refiller', 'refiller', 'lazarus']]
            ['Peapeapod or Rattler', 'Peapeapod or Rattler', 'Looter', 'Defender', 'Refiller', 'Refiller'],
            ['peapeapod', 'peapeapod', 'looter', 'defender', 'refiller', 'refiller']]
    }
    recommendedArenaCompsDict: dict[int, list[list[str]]] = {
        # 2-pet comp used to beat Wave 3
        0: [
            ['Mercenary or Fighter', 'Next Highest Power'],
            ['mercenary', 'fighter']],
        # 3-pet comp used to beat Wave 15
        1: [
            ['Mercenary', 'Cursory', 'Defender or Highest Power'],
            ['mercenary', 'cursory', 'defender']],
        # 4-pet comp used to beat Wave 50
        2: [
            ['Rattler', 'Monolithic', 'Refiller', 'Borger or Defender'],
            ['rattler', 'monolithic', 'refiller', 'borger']],
        # 5-pet comp used to beat Wave 125
        3: [
            ['Rattler', 'Looter', 'Badumdum', 'Refiller', 'Borger'],
            ['rattler', 'looter', 'badumdum', 'refiller', 'borger']],
        # 6-pet comp used to beat Wave 200
        4: [
            ['Rattler', 'Defender', 'Looter', 'Refiller', 'Badumdum', 'Borger'],
            ['rattler', 'defender', 'looter', 'refiller', 'badumdum', 'borger']]
    }

    shinyPetsTierList = {
        "S": ['Bonuses from All Meals', 'Base Efficiency for All Skills', 'Drop Rate'],
        "A": ['Base Critter Per Trap', 'Faster Refinery Speed', 'Multikill Per Tier', 'Infinite Star Signs'],
        "B": ['Summoning EXP', 'Farming EXP', 'Faster Shiny Pet Lv Up Rate'],
        "C": ['Lower Minimum Travel Time for Sailing', 'Higher Artifact Find Chance', 'Skill EXP', 'Base WIS', 'Base STR', 'Base AGI', 'Base LUK'],
        "D": ['Sail Captain EXP Gain', 'Total Damage', 'Any Tab Talent Pts'],
        "F": ['Class EXP', 'Line Width in Lab']
    }
    shinyTiersDisplayed = []
    shinyExclusionsDict = getShinyExclusions()
    if shinyExclusionsDict:
        if shinyExclusionsDict["Lower Minimum Travel Time for Sailing"] == True:
            for tierName, tierList in shinyPetsTierList.items():
                if "Lower Minimum Travel Time for Sailing" in tierList:
                    shinyPetsTierList[tierName].remove("Lower Minimum Travel Time for Sailing")
            shinyPetsTierList["F"].append("Lower Minimum Travel Time for Sailing")

        if shinyExclusionsDict["Higher Artifact Find Chance"] == True:
            for tierName, tierList in shinyPetsTierList.items():
                if "Higher Artifact Find Chance" in tierList:
                    shinyPetsTierList[tierName].remove("Higher Artifact Find Chance")
            shinyPetsTierList["F"].append("Higher Artifact Find Chance")

        if shinyExclusionsDict["Base Critter Per Trap"] == True:
            for tierName, tierList in shinyPetsTierList.items():
                if "Base Critter Per Trap" in tierList:
                    shinyPetsTierList[tierName].remove('Base Critter Per Trap')
            shinyPetsTierList["B"].append('Base Critter Per Trap')

        if shinyExclusionsDict["Faster Shiny Pet Lv Up Rate"] == True:
            for tierName, tierList in shinyPetsTierList.items():
                if "Faster Shiny Pet Lv Up Rate" in tierList:
                    shinyPetsTierList[tierName].remove('Faster Shiny Pet Lv Up Rate')
            shinyPetsTierList["C"].append('Faster Shiny Pet Lv Up Rate')

    #Assess Tiers
    for tier in progressionTiersBreeding:
        # Unlocked Territories
        if tier_UnlockedTerritories >= (tier - 1):
            if breedingDict["Highest Unlocked Territory Number"] >= progressionTiersBreeding[tier]["TerritoriesUnlocked"]:
                tier_UnlockedTerritories = tier
            else:
                for territoryIndex in range(breedingDict["Highest Unlocked Territory Number"] + 1,
                                            progressionTiersBreeding[tier]["TerritoriesUnlocked"] + 1):
                    breeding_AdviceDict["UnlockedTerritories"]["Unlock more Spice Territories"].append(
                        Advice(
                            label=getTerritoryName(territoryIndex),
                            picture_class=getSpiceImage(territoryIndex),
                            completed=False
                        )
                    )
                for petIndex in range(0, len(recommendedTerritoryCompsList[tier][0])):
                    breeding_AdviceDict["UnlockedTerritories"]["Recommended Territory Team (Left to Right)"].append(
                        Advice(
                            label=recommendedTerritoryCompsList[tier][0][petIndex],
                            picture_class=recommendedTerritoryCompsList[tier][1][petIndex],
                            completed=False
                        )
                    )

        # Arena Waves to unlock Pet Slots
        if tier_MaxArenaWave >= (tier - 1):
            if breedingDict["ArenaMaxWave"] >= progressionTiersBreeding[tier]["ArenaWaves"]:
                tier_MaxArenaWave = tier
            else:
                for petIndex in range(0, len(recommendedArenaCompsDict[tier_MaxArenaWave][0])):
                    breeding_AdviceDict["MaxArenaWave"]["Recommended Arena Team (Left to Right)"].append(
                        Advice(
                            label=recommendedArenaCompsDict[tier_MaxArenaWave][0][petIndex],
                            picture_class=recommendedArenaCompsDict[tier_MaxArenaWave][1][petIndex],
                            completed=False
                        )
                    )

        # Shinies
        failedShinyRequirements = []
        failedShinyBonus = {}
        # if tier_ShinyLevels >= (tier-1):
        if len(progressionTiersBreeding[tier].get("Shinies", {})) == 0 and tier_ShinyLevels >= tier - 1:
            # free pass
            tier_ShinyLevels = tier
        else:
            # if there are actual level requirements
            allRequirementsMet = True
            for requiredShinyBonusType in progressionTiersBreeding[tier]["Shinies"]:
                if breedingDict["Total Shiny Levels"][requiredShinyBonusType] < progressionTiersBreeding[tier]["Shinies"][requiredShinyBonusType][0]:
                    if shinyExclusionsDict.get(requiredShinyBonusType, False) == False:
                        allRequirementsMet = False
                    else:
                        continue
                    failedShinyRequirements.append([
                        requiredShinyBonusType,
                        breedingDict["Total Shiny Levels"][requiredShinyBonusType],
                        progressionTiersBreeding[tier]["Shinies"][requiredShinyBonusType][0],
                        progressionTiersBreeding[tier]["Shinies"][requiredShinyBonusType][1]],
                    )
                    failedShinyBonus[requiredShinyBonusType] = breedingDict["Grouped Bonus"][requiredShinyBonusType]
            if allRequirementsMet == True and tier_ShinyLevels >= tier - 1:
                tier_ShinyLevels = tier
            else:
                if tier not in shinyTiersDisplayed and len(shinyTiersDisplayed) < session_data.account.maxSubgroupsPerGroup - 1:
                    shinyTiersDisplayed.append(tier)
                if tier in shinyTiersDisplayed:
                    for failedRequirement in failedShinyRequirements:
                        shinySubgroup = f"Tier {tier} - {failedRequirement[0]}: {failedRequirement[1]}/{failedRequirement[2]}"
                        if failedRequirement[0] not in breeding_AdviceDict["ShinyLevels"]:
                            breeding_AdviceDict["ShinyLevels"][shinySubgroup] = []
                        for possibleShinyPet in failedShinyBonus[failedRequirement[0]]:
                            breeding_AdviceDict["ShinyLevels"][shinySubgroup].append(
                                Advice(
                                    label=f"{possibleShinyPet[0]}: {possibleShinyPet[2]:,.2f} base days to level",
                                    picture_class=possibleShinyPet[0],
                                    progression=possibleShinyPet[1],
                                    goal=max(failedRequirement[3], possibleShinyPet[1]),
                                    completed=False
                                )
                            )

    overall_SectionTier = min(max_tier + info_tiers, tier_MaxArenaWave, tier_UnlockedTerritories, tier_ShinyLevels)

    # Generate Advice Groups
    if tier_UnlockedTerritories < max_tier:
        breeding_AdviceGroupDict["UnlockedTerritories"] = AdviceGroup(
            tier=str(tier_UnlockedTerritories),
            pre_string=f"Unlock {progressionTiersBreeding[tier_UnlockedTerritories + 1]['TerritoriesUnlocked'] - breedingDict['Highest Unlocked Territory Number']} more Spice Territor{pl(breeding_AdviceDict['UnlockedTerritories'], 'y', 'ies')}",
            advices=breeding_AdviceDict["UnlockedTerritories"],
            post_string=""
        )
    if tier_MaxArenaWave != max_tier:
        nextArenaWaveUnlock = progressionTiersBreeding[tier_MaxArenaWave + 1]["ArenaWaves"]
    breeding_AdviceGroupDict["MaxArenaWave"] = AdviceGroup(
        tier=str(tier_MaxArenaWave),
        pre_string=f"Complete Arena Wave {nextArenaWaveUnlock} {pl(5 - tier_MaxArenaWave, 'to unlock the final Arena bonus', 'to unlock another pet slot')}",
        advices=breeding_AdviceDict["MaxArenaWave"],
        post_string=""
    )

    if max(session_data.account.all_skills["Breeding"]) >= 40:
        if tier_ShinyLevels < max_tier:
            breeding_AdviceGroupDict["ShinyLevels"] = AdviceGroup(
                tier=str(tier_ShinyLevels),
                pre_string=f"Level the following Shiny {pl(breeding_AdviceDict['ShinyLevels'], 'Bonus', 'Bonuses')}",
                advices=breeding_AdviceDict["ShinyLevels"],
                post_string=""
            )
        else:
            for shinyTier in shinyPetsTierList:
                if shinyTier not in breeding_AdviceDict["ShinyLevelsTierList"]:
                    breeding_AdviceDict["ShinyLevelsTierList"][shinyTier] = []
                for shinyPet in shinyPetsTierList[shinyTier]:
                    breeding_AdviceDict["ShinyLevelsTierList"][shinyTier].append(Advice(label=shinyPet, picture_class=""))
            breeding_AdviceGroupDict["ShinyLevelsTierList"] = AdviceGroup(
                tier="",
                pre_string="Advance Shiny levels per your desires",
                advices=breeding_AdviceDict["ShinyLevelsTierList"],
                post_string="",
                informational=True
            )

    return breeding_AdviceGroupDict, overall_SectionTier, max_tier

def getBreedingAdviceSection() -> AdviceSection:
    highestBreedingLevel = max(session_data.account.all_skills["Breeding"])
    if highestBreedingLevel < 1:
        breeding_AdviceSection = AdviceSection(
            name="Breeding",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Breeding skill in World 4!",
            picture="Breeding.png",
            unreached=True
        )
        return breeding_AdviceSection

    breedingDict = session_data.account.breeding
    #Generate AdviceGroups
    breeding_AdviceGroupDict, overall_SectionTier, max_tier = getBreedingProgressionTiersAdviceGroups(breedingDict)
    breeding_AdviceGroupDict["ShinySpeedSources"] = getShinySpeedSourcesAdviceGroup(breedingDict['Total Shiny Levels']['Faster Shiny Pet Lv Up Rate'])
    breeding_AdviceGroupDict["ActiveBM"] = getActiveBMAdviceGroup()
    breeding_AdviceGroupDict['Breedability'] = getBreedabilityAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    breeding_AdviceSection = AdviceSection(
        name="Breeding",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Breeding tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Breeding.png",
        groups = breeding_AdviceGroupDict.values()
    )
    return breeding_AdviceSection
