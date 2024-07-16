import copy
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import numberOfArtifacts, numberOfArtifactTiers, breeding_progressionTiers, getReadableVialNames, maxTiersPerGroup, territoryNames

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
    sps_adviceDict = {
        "Multi Group A- Summoning Winner Bonus": [],
        "Multi Group B- Everything Else": []
    }

    sps_adviceDict["Multi Group B- Everything Else"].append(Advice(
        label=f"Lab Jewel: Emerald Ulthurite",
        picture_class='emerald-ulthurite'
    ))
    sps_adviceDict["Multi Group B- Everything Else"].append(Advice(
        label=f"Faster Shiny Pet Lv Up Rate Shiny Pets: +{3 * fasterShinyPetTotalLevels}% total",
        picture_class='green-mushroom-shiny'
    ))
    sps_adviceDict["Multi Group B- Everything Else"].append(Advice(
        label=f"Star Sign: Breedabilli: +{15 * session_data.account.star_signs.get('Breedabilli', {}).get('Unlocked', False)}%",
        picture_class='breedabilli'
    ))
    sps_adviceDict["Multi Group B- Everything Else"].append(session_data.account.star_sign_extras['SeraphAdvice'])
    sps_adviceDict["Multi Group B- Everything Else"].append(session_data.account.star_sign_extras['SilkrodeNanoAdvice'])

    red8beat = session_data.account.summoning['Battles']['Red'] >= 8
    cyan13beat = session_data.account.summoning['Battles']['Cyan'] >= 13
    sps_adviceDict["Multi Group A- Summoning Winner Bonus"].append(Advice(
        label=f"Summoning match Red8: +{1.88 * red8beat}{'' if red8beat else '. Not yet beaten.'}",
        picture_class="citringe",
        progression=1 if red8beat else 0,
        goal=1
    ))
    sps_adviceDict["Multi Group A- Summoning Winner Bonus"].append(Advice(
        label=f"Summoning match Cyan13: +{3.45 * cyan13beat}{'' if cyan13beat else '. Not yet beaten.'}",
        picture_class="minichief-spirit",
        progression=1 if cyan13beat else 0,
        goal=1
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        sps_adviceDict["Multi Group A- Summoning Winner Bonus"].append(advice)

    sps_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Sources of Shiny Pet Level Rate",
        advices=sps_adviceDict)
    return sps_AdviceGroup

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
        label="Spinge Tingler Sniper: +12% respawn",
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
        picture_class="chocolatey-chip"
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Omega Nanochip: Top Left card doubler",
        picture_class="omega-nanochip"
    ))
    abm_adviceDict["Lab Chips"].append(Advice(
        label="Omega Motherboard: Bottom Right card doubler",
        picture_class="omega-motherboard"
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

    abm_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Info- Active BM setup for around 4-5x shiny progress",
        advices=abm_adviceDict
    )
    return abm_AdviceGroup

def setBreedingProgressionTier() -> AdviceSection:
    breeding_AdviceDict = {
        "UnlockedTerritories": {"Unlock more Spice Territories": [], "Recommended Territory Team (Left to Right)": []},
        "MaxArenaWave": {"Recommended Arena Team (Left to Right)": []},
        "ShinyLevels": {},
        "ShinyLevelsTierList": {}
    }
    breeding_AdviceGroupDict = {}
    breeding_AdviceSection = AdviceSection(
        name="Breeding",
        tier="Not Yet Evaluated",
        header="Best Breeding tier met: Not Yet Evaluated. Recommended breeding actions:",
        picture="Breeding.png",
        collapse=False
    )
    highestBreedingLevel = max(session_data.account.all_skills["Breeding"])
    if highestBreedingLevel < 1:
        breeding_AdviceSection.header = "Come back after unlocking the Breeding skill in World 4!"
        breeding_AdviceSection.collapse = True
        return breeding_AdviceSection

    progressionTiersBreeding = copy.deepcopy(breeding_progressionTiers)
    maxBreedingTier = max(progressionTiersBreeding.keys())
    tier_UnlockedTerritories = 0
    tier_MaxArenaWave = 0
    tier_ShinyLevels = 0
    overall_BreedingTier = 0
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
            #['Peapeapod or Rattler', 'Looter', 'Trasher (Manually click to delete enemy attacks!)', 'Refiller', 'Refiller', 'Lazarus or Filler'],
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

    breedingDict = session_data.account.breeding
    shinyExclusionsDict = getShinyExclusions()
    shinyTiersDisplayed = []
    if breedingDict == {}:
        breeding_AdviceSection.header = "Breeding info could not be read from your save data :( Please file a bug report if you have Breeding unlocked"
        return breeding_AdviceSection
    else:
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

        for tier in progressionTiersBreeding:
            #Unlocked Territories
            if tier_UnlockedTerritories >= (tier-1):
                if breedingDict["Highest Unlocked Territory Number"] >= progressionTiersBreeding[tier]["TerritoriesUnlocked"]:
                    tier_UnlockedTerritories = tier
                else:
                    for territoryIndex in range(breedingDict["Highest Unlocked Territory Number"]+1, progressionTiersBreeding[tier]["TerritoriesUnlocked"]+1):
                        breeding_AdviceDict["UnlockedTerritories"]["Unlock more Spice Territories"].append(
                            Advice(
                                label=getTerritoryName(territoryIndex),
                                picture_class=getSpiceImage(territoryIndex)
                            )
                        )
                    for petIndex in range(0, len(recommendedTerritoryCompsList[tier][0])):
                        breeding_AdviceDict["UnlockedTerritories"]["Recommended Territory Team (Left to Right)"].append(
                            Advice(
                                label=recommendedTerritoryCompsList[tier][0][petIndex],
                                picture_class=recommendedTerritoryCompsList[tier][1][petIndex]
                            )
                        )

            #Arena Waves to unlock Pet Slots
            if tier_MaxArenaWave >= (tier-1):
                if breedingDict["ArenaMaxWave"] >= progressionTiersBreeding[tier]["ArenaWaves"]:
                    tier_MaxArenaWave = tier
                else:
                    for petIndex in range(0, len(recommendedArenaCompsDict[tier_MaxArenaWave][0])):
                        breeding_AdviceDict["MaxArenaWave"]["Recommended Arena Team (Left to Right)"].append(
                            Advice(
                                label=recommendedArenaCompsDict[tier_MaxArenaWave][0][petIndex],
                                picture_class=recommendedArenaCompsDict[tier_MaxArenaWave][1][petIndex]
                            )
                        )

            #Shinies
            failedShinyRequirements = []
            failedShinyBonus = {}
            #if tier_ShinyLevels >= (tier-1):
            if len(progressionTiersBreeding[tier].get("Shinies", {})) == 0 and tier_ShinyLevels >= tier-1:
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
                if allRequirementsMet == True and tier_ShinyLevels >= tier-1:
                    tier_ShinyLevels = tier
                else:
                    if tier not in shinyTiersDisplayed and len(shinyTiersDisplayed) < maxTiersPerGroup-1:
                        shinyTiersDisplayed.append(tier)
                    if tier in shinyTiersDisplayed:
                        for failedRequirement in failedShinyRequirements:
                            shinySubgroup = f"Tier {tier} - {failedRequirement[0]}: {failedRequirement[1]}/{failedRequirement[2]}"
                            if failedRequirement[0] not in breeding_AdviceDict["ShinyLevels"]:
                                breeding_AdviceDict["ShinyLevels"][shinySubgroup] = []
                            for possibleShinyPet in failedShinyBonus[failedRequirement[0]]:
                                breeding_AdviceDict["ShinyLevels"][shinySubgroup].append(
                                    Advice(
                                        label=f"{possibleShinyPet[0]}: {possibleShinyPet[2]:.2f} base days to level",
                                        picture_class=possibleShinyPet[0],
                                        progression=possibleShinyPet[1],
                                        goal=failedRequirement[3]
                                    )
                                )

    overall_BreedingTier = min(maxBreedingTier, tier_UnlockedTerritories, tier_ShinyLevels)

    #Generate Advice Groups
    if tier_UnlockedTerritories < maxBreedingTier:
        breeding_AdviceGroupDict["UnlockedTerritories"] = AdviceGroup(
            tier=str(tier_UnlockedTerritories),
            pre_string=f"Unlock {progressionTiersBreeding[tier_UnlockedTerritories+1]['TerritoriesUnlocked'] - breedingDict['Highest Unlocked Territory Number']} more Spice Territor{pl(breeding_AdviceDict['UnlockedTerritories'], 'y', 'ies')}",
            advices=breeding_AdviceDict["UnlockedTerritories"],
            post_string=""
        )
    if tier_MaxArenaWave != maxBreedingTier:
        nextArenaWaveUnlock = progressionTiersBreeding[tier_MaxArenaWave+1]["ArenaWaves"]
    breeding_AdviceGroupDict["MaxArenaWave"] = AdviceGroup(
        tier=str(tier_MaxArenaWave),
        pre_string=f"Complete Arena Wave {nextArenaWaveUnlock} {pl(5-tier_MaxArenaWave, 'to unlock the final Arena bonus', 'to unlock another pet slot')}",
        advices=breeding_AdviceDict["MaxArenaWave"],
        post_string=""
    )

    if highestBreedingLevel >= 40:
        if tier_ShinyLevels < maxBreedingTier:
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
                post_string=""
            )
        breeding_AdviceGroupDict["ShinySpeedSources"] = getShinySpeedSourcesAdviceGroup(breedingDict['Total Shiny Levels']['Faster Shiny Pet Lv Up Rate'])
        breeding_AdviceGroupDict["ActiveBM"] = getActiveBMAdviceGroup()

    #Generate Advice Section
    tier_section = f"{overall_BreedingTier}/{maxBreedingTier}"
    breeding_AdviceSection.tier = tier_section
    breeding_AdviceSection.pinchy_rating = overall_BreedingTier
    breeding_AdviceSection.groups = breeding_AdviceGroupDict.values()
    if overall_BreedingTier >= maxBreedingTier:
        breeding_AdviceSection.header = f"Best Breeding tier met: {tier_section}<br>You best ❤️"
        breeding_AdviceSection.complete = True
    else:
        breeding_AdviceSection.header = f"Best Breeding tier met: {tier_section}"

    return breeding_AdviceSection
