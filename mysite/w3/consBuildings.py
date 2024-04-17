import copy
from consts import buildingsPostBuffs_progressionTiers, buildingsPreBuffs_progressionTiers
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from utils.data_formatting import safe_loads


logger = get_logger(__name__)

def parseConsBuildingstoLists():
    consBuildingsList = safe_loads(session_data.account.raw_data["Tower"])  #expected type of list
    #logger.debug(f"TYPE CHECK consBuildingsList: {type(consBuildingsList)}: {consBuildingsList}")
    return consBuildingsList

def getBuildingNameFromIndex(inputNumber):
    towerList = [
        "3D Printer", "Talent Book Library", "Death Note", "Salt Lick", "Chest Space", "Cost Cruncher", "Trapper Drone", "Automation Arm", "Atom Collider",
        "Pulse Mage", "Fireball Lobber", "Boulder Roller", "Frozone Malone", "Stormcaller", "Party Starter", "Kraken Cosplayer", "Poisonic Elder", "Voidinator",
        "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Clover Shrine", "Summereading Shrine", "Crescent Shrine", "Undead Shrine", "Primordial Shrine"]
    try:
        inputNumber = int(inputNumber)
        return towerList[inputNumber]
    except:
        return f"UnknownBuilding{inputNumber}"

def getBuildingImageNameFromIndex(inputNumber):
    towerImageNameList = ["three-d-printer", "talent-book-library", "death-note", "salt-lick", "chest-space", "cost-cruncher", "critter-drone",
                          "automation-arm", "atom-collider", "pulse-mage", "fireball-lobber", "boulder-roller", "frozone-malone", "stormcaller",
                          "party-starter", "kraken-cosplayer", "poisonic-elder", "voidinator", "woodular-shrine", "isaccian-shrine", "crystal-shrine",
                          "pantheon-shrine", "clover-shrine", "summereading-shrine", "crescent-shrine", "undead-shrine", "primordial-shrine"]
    try:
        inputNumber = int(inputNumber)
        return towerImageNameList[inputNumber]
    except:
        return f"UnknownBuilding{inputNumber}"

def getInfluencers():
    #Honker Vial level
    try:
        honkerVialLevel = session_data.account.raw_data["CauldronInfo"][4]["40"]  #expected type of int
        #logger.debug(f"TYPE CHECK honkerVialLevel: {type(honkerVialLevel)}: {honkerVialLevel}")
    except Exception as reason:
        honkerVialLevel = 0
        logger.exception(f"Unable to retrieve honkerVialLevel: {reason}")

    #Boulder Roller level
    try:
        poisonicLevel = safe_loads(session_data.account.raw_data["Tower"])[16]  #expected type of int
        #logger.debug(f"TYPE CHECK poisonicLevel: {type(poisonicLevel)}: poisonicLevel")
    except Exception as reason:
        poisonicLevel = 0
        logger.exception(f"Unable to retrieve poisonicLevel: {reason}")

    #Other?
    if session_data.account.construction_mastery_unlocked:
        consMastery = True
    else:
        consMastery = False

    atomCarbon = False
    try:
        carbonLevel = session_data.account.raw_data["Atoms"][5]
        if carbonLevel >= 1:
            atomCarbon = True
    except Exception as reason:
        logger.exception(f"Unable to find Atom Collider Carbon level: {reason}")
    results = [(consMastery or atomCarbon), honkerVialLevel, poisonicLevel]
    #logger.debug(f"Influencer results: EitherBuff: {results[0]}, Honker Vial Level: {results[1]}, Poisonic Tower Level: {results[2]}")
    return results

def setConsBuildingsProgressionTier():
    building_AdviceDict = {}
    building_AdviceGroupDict = {}
    building_AdviceSection = AdviceSection(
        name="Buildings",
        tier="",
        header="Recommended Construction Buildings priorities for Trimmed Slots",
        picture="Construction_Table.gif",
        collapse=False
    )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        building_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        building_AdviceSection.collapse = True
        return building_AdviceSection

    progressionTiersPreBuffs = copy.deepcopy(buildingsPreBuffs_progressionTiers)
    progressionTiersPostBuffs = copy.deepcopy(buildingsPostBuffs_progressionTiers)
    maxBuildingsPerGroup = 10
    playerBuildings = parseConsBuildingstoLists()
    influencers = getInfluencers()
    hasBuffs = influencers[0]
    if hasBuffs:
        #maxLevelList = [10, 201, 51, 10, 25, 60, 45, 5, 200,    140, 140, 140, 140, 140, 140, 140, 140, 140,   200, 200, 200, 200, 200, 200, 200, 200, 200]  # these are true max, not recommended max
        maxLevelList = [10, 101, 51, 10, 25, 60, 20, 5, 200,    70, 70, 70, 70, 90, 70, 90, 90, 40,             200, 200, 200, 200, 200, 200, 200, 200, 200]  # the recommended maxes
        #logger.debug(" Either Construction Mastery and Wizard Atom found. Setting maxLevelList to PostBuff.")
    else:
        maxLevelList = [10, 101, 51, 10, 25, 60, 15, 5, 200,    50, 50, 50, 50, 50, 50, 50, 50, 40,             100, 100, 100, 100, 100, 100, 100, 100, 100]
        #logger.debug("ConsBuildings.setConsBuildingsProgressionTier~ INFO Setting maxLevelList to PreBuff.")

    # Make adjustments to tiers based on other influencers
    # 1) If any building is level 0, it gets promoted to SS tier
    for buildingCounter in range(0, len(maxLevelList)):
        #logger.debug(f"Is player level {playerBuildings[buildingCounter]} equal to 0 for Tower {buildingCounter} ({getBuildingNameFromIndex(buildingCounter)}): {playerBuildings[buildingCounter] == 0}")
        if playerBuildings[buildingCounter] == 0:
            maxLevelList[buildingCounter] = 1  #With a max recommended level of 1
            for tier in progressionTiersPostBuffs:
                if buildingCounter in tier[2] and tier[1] != "SS":
                    tier[2].remove(buildingCounter)  #Remove that building from any other non-SS tier.
                    progressionTiersPostBuffs[0][2].append(buildingCounter)
                    logger.debug(f"Level 0 building detected. Removing {getBuildingNameFromIndex(buildingCounter)} from POSTBuff {tier[1]} and adding to SS with max level 1 instead.")
            for tier in progressionTiersPreBuffs:
                if buildingCounter in tier[2] and tier[1] != "SS":
                    tier[2].remove(buildingCounter)  #Remove that building from any other non-SS tier.
                    progressionTiersPreBuffs[0][2].append(buildingCounter)
                    logger.debug(f"Level 0 building detected. Removing {getBuildingNameFromIndex(buildingCounter)} from PREBuff {tier[1]} and adding to SS with max level 1 instead.")

    # 2) Honker vial is 12+ OR Trapper Drone is 20+, drop Trapper Drone priority
    if influencers[1] >= 12 or playerBuildings[6] >= 20:
        try:
            progressionTiersPostBuffs[2][2].remove(6)  #Remove Trapper Drone from S Tier
            progressionTiersPostBuffs[6][2].append(6)  #Add Trapper Drone to D tier
            if hasBuffs:
                maxLevelList[6] = 50
            #logger.debug("Successfully moved Trapper Drone from PostBuff S to D tier and changed level from 20 to 50")
        except Exception as reason:
            logger.exception(f"Could not remove Trapper Drone from PostBuff S tier: {reason}")

    # 3) #Poisonic level 20+, drop Boulder Roller priority
    if influencers[2] >= 20:
        try:
            #PreBuffs
            progressionTiersPreBuffs[2][2].remove(11)  #Remove Boulder Roller from S tier
            progressionTiersPreBuffs[6][2].append(11)  #Add Boulder Roller to D tier
            #logger.debug("Successfully moved Boulder Roller from PreBuff S to D tier because Poisonic 20+")
            #PostBuffs
            progressionTiersPostBuffs[2][2].remove(11)  #Remove Boulder Roller from S tier
            progressionTiersPostBuffs[3][2].append(11)  #Add Boulder Roller to A tier
            #logger.debug("Successfully moved Boulder Roller from PostBuff S to A tier because Poisonic 20+")
        except Exception as reason:
            logger.exception(f"Could not move Boulder Roller from S tier in one or both tierlists: {reason}")

    # 4) Talent Library Book 101+, drop priority
    if playerBuildings[1] >= 101:
        try:
            progressionTiersPostBuffs[2][2].remove(1)  #Remove from S tier
            progressionTiersPostBuffs[5][2].append(1)  #Add to C tier
            if hasBuffs:
                maxLevelList[1] = 201
            #logger.debug("Successfully moved 101+ Talent Library Book from PostBuff A to C tier.")
        except Exception as reason:
            logger.exception(f"Could not move 101+ Talent Library Book from PostBuff A tier to C tier: {reason}")

    # 5) #Basic Towers to 70, drop priority
    for towerIndex in [12,14,9,10,11]:
        if playerBuildings[towerIndex] >= 70:
            try:
                progressionTiersPostBuffs[3][2].remove(towerIndex)  #Remove from A tier
                progressionTiersPostBuffs[5][2].append(towerIndex)  #Add to C tier
                if hasBuffs:
                    maxLevelList[towerIndex] = 140
                #logger.info(f"Successfully moved 70+ basic tower from PostBuff A to C tier: {getBuildingNameFromIndex(towerIndex)})
            except Exception as reason:
                logger.exception(f"Could not move 70+ basic tower {getBuildingNameFromIndex(towerIndex)} from PostBuff A tier to C tier: {reason}")

    # 6) Fancy Towers to 90, drop priority
    for towerIndex in [15,16,13]:
        if playerBuildings[towerIndex] >= 90:
            for tierIndex in range(0, len(progressionTiersPostBuffs)):
                if towerIndex in progressionTiersPostBuffs[tierIndex][2]:
                    progressionTiersPostBuffs[tierIndex][2].remove(towerIndex)  #Remove from any existing tier (S for Kraken and Poison, A for Stormcaller)
            progressionTiersPostBuffs[3][2].append(towerIndex)  #Add to A tier
            if hasBuffs:
                maxLevelList[towerIndex] = 140

    # 7) Voidinator to 40, drop priority
    if playerBuildings[17] >= 40:  #Voidinator scaling is very bad
        try:
            progressionTiersPreBuffs[4][2].remove(17)  #Remove from PreBuff B tier
            progressionTiersPreBuffs[5][2].append(17)  #Add to C tier
            progressionTiersPostBuffs[3][2].remove(17)  #Remove from PostBuff A tier
            progressionTiersPostBuffs[5][2].append(17)  #Add to C tier
            if hasBuffs:
                maxLevelList[17] = 140
            #logger.debug("Successfully moved 30+ Voidinator from A/B to C tier in both tierlists")
        except Exception as reason:
            logger.exception(f"Could not move 30+ Voidinator from A/B to C tier in both tierlists: {reason}")

    # Decide which tierset to use
    if influencers[0] == True:  #Has either Construction Mastery or the Wizard atom
        progressionTiersToUse = progressionTiersPostBuffs
        #logger.debug("Either Construction Mastery or Wizard Atom found. Setting ProgressionTiers to PostBuff.")
    else:
        progressionTiersToUse = progressionTiersPreBuffs
        #logger.debug("Setting ProgressionTiers to PreBuff.")

    #tier[0] = int tier
    #tier[1] = str Tier name
    #tier[2] = list of ints of tower indexes
    #tier[3] = str tower notes
    #tier[4] = str tier notes
    tierNamesList = []
    for counter in range(0, len(progressionTiersToUse)):
        building_AdviceDict[counter] = []
        tierNamesList.append(progressionTiersToUse[counter][1])
        for recommendedBuilding in progressionTiersToUse[counter][2]:
            try:
                if maxLevelList[recommendedBuilding] > playerBuildings[recommendedBuilding]:
                    if len(building_AdviceDict[counter]) < maxBuildingsPerGroup:
                        if progressionTiersToUse[counter][1] == "Unlock":
                            building_AdviceDict[counter].append(
                                Advice(
                                    label=getBuildingNameFromIndex(recommendedBuilding),
                                    picture_class=getBuildingImageNameFromIndex(recommendedBuilding))
                            )
                        else:
                            building_AdviceDict[counter].append(
                                Advice(
                                    label=getBuildingNameFromIndex(recommendedBuilding),
                                    picture_class=getBuildingImageNameFromIndex(recommendedBuilding),
                                    progression=str(playerBuildings[recommendedBuilding]),
                                    goal=str(maxLevelList[recommendedBuilding]))
                            )
                else:
                    #logger.debug(f"{progressionTiers[counter][1]} Tier: Max met for {getBuildingNameFromIndex(recommendedBuilding)}, not generating Advice")
                    continue
            except Exception as reason:
                logger.exception(f"ProgressionTier evaluation error. Counter = {counter}, recommendedBuilding = {recommendedBuilding}, Reason: {reason}")

    #Generate AdviceGroups
    for tierKey in building_AdviceDict.keys():
        if f"{str(tierNamesList[tierKey])}" == "Unlock":
            building_AdviceGroupDict[tierKey] = AdviceGroup(
                tier="",
                pre_string=f"Unlock All Buildings",
                advices=building_AdviceDict[tierKey],
                post_string=""
            )
            #for building_Advice in building_AdviceGroupDict[f"{str(tierNamesList[tierKey])}"]:

        else:
            building_AdviceGroupDict[tierKey] = AdviceGroup(
                tier="",
                pre_string=f"{str(tierNamesList[tierKey])} Tier",
                advices=building_AdviceDict[tierKey],
                post_string=""
            )
        if len(building_AdviceDict[tierKey]) == maxBuildingsPerGroup:
            building_AdviceGroupDict[tierKey].post_string = f"Up to {maxBuildingsPerGroup} remaining buildings shown"

    #Generate AdviceSection
    building_AdviceSection.groups = building_AdviceGroupDict.values()
    return building_AdviceSection
