import copy
from consts import buildingsPostBuffs_progressionTiers, buildingsPreBuffs_progressionTiers
from flask import g as session_data
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger


logger = get_logger(__name__)

def getInfluencers():
    honkerVialLevel = session_data.account.alchemy_vials.get("Goosey Glug (Honker)", {}).get("Level", 0)
    poisonicLevel = session_data.account.construction_buildings['Poisonic Elder']['Level']
    consMastery = session_data.account.rift['ConstructionMastery']
    carbonUnlocked = session_data.account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'] >= 1
    results = [(consMastery or carbonUnlocked), honkerVialLevel, poisonicLevel]
    #logger.debug(f"Influencer results: EitherBuff: {results[0]}, Honker Vial Level: {results[1]}, Poisonic Tower Level: {results[2]}")
    return results

def setConsBuildingsProgressionTier():
    building_AdviceDict = {}
    building_AdviceGroupDict = {}
    building_AdviceSection = AdviceSection(
        name="Buildings",
        tier="",
        header="Priority Tiers for Trimmed Building Slots",
        picture="Construction_Table.gif",
        collapse=False,
        note="Buildings shift around in Priority Tiers after reaching particular levels or notable account progression points."
             " The goal levels displayed are only for that particular tier and may be beyond your personal max level.",
        unrated=True
    )
    if not session_data.account.hide_info:
        building_AdviceSection.note = (
            "Buildings shift around in Priority Tiers after reaching particular levels or notable account progression points."
            " The goal levels displayed are only for that particular tier and may be beyond your personal max level."
        )
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        building_AdviceSection.header = "Come back after unlocking the Construction skill in World 3!"
        building_AdviceSection.unreached = True
        return building_AdviceSection

    progressionTiersPreBuffs = copy.deepcopy(buildingsPreBuffs_progressionTiers)
    progressionTiersPostBuffs = copy.deepcopy(buildingsPostBuffs_progressionTiers)
    playerBuildings = session_data.account.construction_buildings
    influencers = getInfluencers()
    hasBuffs = influencers[0]
    if hasBuffs:
        maxLevelDict = {
            "3D Printer": 10, "Talent Book Library": 101, "Death Note": 51, "Salt Lick": 10, "Chest Space": 25,
            "Cost Cruncher": 60, "Trapper Drone": 20, "Automation Arm": 5, "Atom Collider": 200,
            "Pulse Mage": 70, "Fireball Lobber": 70, "Boulder Roller": 70, "Frozone Malone": 70, "Stormcaller": 90,
            "Party Starter": 70, "Kraken Cosplayer": 90, "Poisonic Elder": 90, "Voidinator": 40,
            "Woodular Shrine": 200, "Isaccian Shrine": 200, "Crystal Shrine": 200, "Pantheon Shrine": 200, "Clover Shrine": 200,
            "Summereading Shrine": 200, "Crescent Shrine": 200, "Undead Shrine": 200, "Primordial Shrine": 200
        }
    else:
        maxLevelDict = {
            "3D Printer": 10, "Talent Book Library": 101, "Death Note": 51, "Salt Lick": 10, "Chest Space": 25,
            "Cost Cruncher": 60, "Trapper Drone": 15, "Automation Arm": 5, "Atom Collider": 200,
            "Pulse Mage": 50, "Fireball Lobber": 50, "Boulder Roller": 50, "Frozone Malone": 50, "Stormcaller": 50,
            "Party Starter": 50, "Kraken Cosplayer": 50, "Poisonic Elder": 50, "Voidinator": 40,
            "Woodular Shrine": 100, "Isaccian Shrine": 100, "Crystal Shrine": 100, "Pantheon Shrine": 100, "Clover Shrine": 100,
            "Summereading Shrine": 100, "Crescent Shrine": 100, "Undead Shrine": 100, "Primordial Shrine": 100
        }

    # Make adjustments to tiers based on other influencers
    # 1) If any building is level 0, it gets promoted to SS tier
    for reccBuildingName, reccBuildingLevel in maxLevelDict.items():
        if playerBuildings[reccBuildingName]['Level'] == 0:
            maxLevelDict[reccBuildingName] = 1  #With a max recommended level of 1
            for tier in progressionTiersPostBuffs:
                if reccBuildingName in tier[2] and tier[1] != "SS":
                    tier[2].remove(reccBuildingName)  #Remove that building from any other non-SS tier.
                    progressionTiersPostBuffs[0][2].append(reccBuildingName)
                    #logger.debug(f"Level 0 building detected. Removing {reccBuildingName} from POSTBuff {tier[1]} and adding to SS with max level 1 instead.")
            for tier in progressionTiersPreBuffs:
                if reccBuildingName in tier[2] and tier[1] != "SS":
                    tier[2].remove(reccBuildingName)  #Remove that building from any other non-SS tier.
                    progressionTiersPreBuffs[0][2].append(reccBuildingName)
                    #logger.debug(f"Level 0 building detected. Removing {reccBuildingName} from PREBuff {tier[1]} and adding to SS with max level 1 instead.")

    # 2) Honker vial is 12+ OR Trapper Drone is 20+, drop Trapper Drone priority
    if influencers[1] >= 12 or playerBuildings['Trapper Drone']['Level'] >= 20:
        try:
            progressionTiersPostBuffs[2][2].remove('Trapper Drone')  #Remove Trapper Drone from S Tier
            progressionTiersPostBuffs[5][2].insert(1, 'Trapper Drone')  #Add Trapper Drone to C tier
            if hasBuffs:
                maxLevelDict['Trapper Drone'] = 50
            #logger.debug("Successfully moved Trapper Drone from PostBuff S to D tier and changed level from 20 to 50")
        except Exception as reason:
            logger.exception(f"Could not remove Trapper Drone from PostBuff S tier: {reason}")

    # 3) #Poisonic level 20+, drop Boulder Roller priority
    if influencers[2] >= 20:
        try:
            #PreBuffs
            progressionTiersPreBuffs[2][2].remove("Boulder Roller")  #Remove Boulder Roller from S tier
            progressionTiersPreBuffs[6][2].append("Boulder Roller")  #Add Boulder Roller to D tier
            #logger.debug("Successfully moved Boulder Roller from PreBuff S to D tier because Poisonic 20+")
            #PostBuffs
            progressionTiersPostBuffs[2][2].remove("Boulder Roller")  #Remove Boulder Roller from S tier
            progressionTiersPostBuffs[3][2].append("Boulder Roller")  #Add Boulder Roller to A tier
            #logger.debug("Successfully moved Boulder Roller from PostBuff S to A tier because Poisonic 20+")
        except Exception as reason:
            logger.exception(f"Could not move Boulder Roller from S tier in one or both tierlists: {reason}")

    # 4) Talent Library Book 101+, drop priority
    if playerBuildings['Talent Book Library']['Level'] >= 101:
        try:
            progressionTiersPostBuffs[2][2].remove("Talent Book Library")  #Remove from S tier
            progressionTiersPostBuffs[5][2].insert(1, "Talent Book Library")  #Add to C tier
            if hasBuffs:
                maxLevelDict["Talent Book Library"] = 201
            #logger.debug("Successfully moved 101+ Talent Library Book from PostBuff A to C tier.")
        except Exception as reason:
            logger.exception(f"Could not move 101+ Talent Library Book from PostBuff A tier to C tier: {reason}")

    # 5) #Basic Towers to 70, drop priority
    for towerName in ["Frozone Malone", "Party Starter", "Pulse Mage", "Fireball Lobber", "Boulder Roller"]:
        if playerBuildings[towerName]['Level'] >= 70:
            try:
                progressionTiersPostBuffs[3][2].remove(towerName)  #Remove from A tier
                progressionTiersPostBuffs[5][2].insert(3, towerName)  #Add to C tier
                if hasBuffs:
                    maxLevelDict[towerName] = 140
                #logger.info(f"Successfully moved 70+ basic tower from PostBuff A to C tier: {getBuildingNameFromIndex(towerIndex)})
            except Exception as reason:
                logger.exception(f"Could not move 70+ basic tower {towerName} from PostBuff A tier to C tier: {reason}")

    # 6) Fancy Towers to 90, drop priority
    for towerName in ["Kraken Cosplayer", "Poisonic Elder", "Stormcaller"]:
        if playerBuildings[towerName]['Level'] >= 90:
            for tierIndex in range(0, len(progressionTiersPostBuffs)):
                if towerName in progressionTiersPostBuffs[tierIndex][2]:
                    progressionTiersPostBuffs[tierIndex][2].remove(towerName)  #Remove from any existing tier (S for Kraken and Poison, A for Stormcaller)
            progressionTiersPostBuffs[3][2].append(towerName)  #Add to A tier
            if hasBuffs:
                maxLevelDict[towerName] = 140

    # 7) Voidinator to 40, drop priority
    if playerBuildings['Voidinator']['Level'] >= 40:  #Voidinator scaling is very bad
        try:
            progressionTiersPreBuffs[4][2].remove("Voidinator")  #Remove from PreBuff B tier
            progressionTiersPreBuffs[5][2].insert(0, "Voidinator")  #Add to C tier
            progressionTiersPostBuffs[3][2].remove("Voidinator")  #Remove from PostBuff A tier
            progressionTiersPostBuffs[5][2].insert(0, "Voidinator")  #Add to C tier
            if hasBuffs:
                maxLevelDict["Voidinator"] = 140
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
                if maxLevelDict.get(recommendedBuilding, 999) > playerBuildings.get(recommendedBuilding, {}).get('Level', 0):
                    if progressionTiersToUse[counter][1] == "Unlock":
                        building_AdviceDict[counter].append(Advice(
                                label=recommendedBuilding,
                                picture_class=playerBuildings.get(recommendedBuilding, {}).get('Image', '')
                        ))
                    else:
                        building_AdviceDict[counter].append(Advice(
                                label=recommendedBuilding,
                                picture_class=playerBuildings.get(recommendedBuilding, {}).get('Image', ''),
                                progression=playerBuildings.get(recommendedBuilding, {}).get('Level', 0),
                                goal=maxLevelDict.get(recommendedBuilding, 999)
                        ))
            except Exception as reason:
                logger.exception(f"ProgressionTier evaluation error. Counter = {counter}, recommendedBuilding = {recommendedBuilding}, Reason: {reason}")

    #Generate AdviceGroups
    for tierKey in building_AdviceDict.keys():
        if f"{str(tierNamesList[tierKey])}" == "Unlock":
            building_AdviceGroupDict[tierKey] = AdviceGroup(
                tier="",
                pre_string=f"Unlock All Buildings",
                advices=building_AdviceDict[tierKey],
                informational=True
            )
        else:
            building_AdviceGroupDict[tierKey] = AdviceGroup(
                tier="",
                pre_string=f"{str(tierNamesList[tierKey])} Tier",
                advices=building_AdviceDict[tierKey],
                informational=True
            )

    #Generate AdviceSection
    building_AdviceSection.groups = building_AdviceGroupDict.values()
    #building_AdviceSection.complete = len(building_AdviceSection.groups) == 0
    return building_AdviceSection
