import json
import progressionResults

def parseConsBuildingstoLists(inputJSON):
    consBuildingsList = json.loads(inputJSON["Tower"]) #expected type of list
    #print("ConsBuildings~ TYPE CHECK consBuildingsList: ", type(consBuildingsList), consBuildingsList)
    return consBuildingsList

def getBuildingNameFromIndex(inputNumber):
    towerList = ["3D Printer", "Talent Book Library", "Death Note", "Salt Lick", "Chest Space", "Cost Cruncher", "Trapper Drone", "Automation Arm", "Atom Collider", "Pulse Mage", "Fireball Lobber", "Boulder Roller", "Frozone Malone", "Stormcaller", "Party Starter", "Kraken Cosplayer", "Poisonic Elder", "Voidinator", "Woodular Shrine", "Isaccian Shrine", "Crystal Shrine", "Pantheon Shrine", "Clover Shrine", "Summereading Shrine", "Crescent Shrine", "Undead Shrine", "Primordial Shrine"]
    try:
        inputNumber = int(inputNumber)
        return towerList[inputNumber]
    except:
        return "UnknownBuilding"+str(inputNumber)

def getInfluencers(inputJSON):
    #Honker Vial level
    try:
        honkerVialLevel = inputJSON["CauldronInfo"][4]["40"] #expected type of int
        #print("ConsBuildings.getInfluencers~ TYPE CHECK honkerVialLevel: ", type(honkerVialLevel), honkerVialLevel)
    except Exception as reason:
        honkerVialLevel = 0
        print("ConsBuildings.getInfluencers~ EXCEPTION Unable to get honkerVialLevel: ", reason)

    #Boulder Roller level
    try:
        poisonicLevel = json.loads(inputJSON["Tower"])[16] #expected type of int
        #print("ConsBuildings~ TYPE CHECK poisonicLevel: ", type(poisonicLevel), poisonicLevel)
    except Exception as reason:
        poisonicLevel = 0
        print("ConsBuildings.getInfluencers~ EXCEPTION Unable to get poisonicLevel: ", reason)

    #Other?
    consMastery = False
    atomCarbon = False
    try:
        highestCompletedRift = inputJSON["Rift"][0]
        if highestCompletedRift >= 41:
            consMastery = True
    except Exception as reason:
        print("ConsBuildings.getInfluencers~ EXCEPTION: getBuffs Unable to find highest Rift level completed: ", reason)
    try:
        carbonLevel = inputJSON["Atoms"][5]
        if carbonLevel >= 1:
            atomCarbon = True
    except Exception as reason:
        print("ConsBuildings.getInfluencers~ EXCEPTION: getBuffs Unable to find Atom Collider Carbon level: ", reason)
    results = [(consMastery or atomCarbon), honkerVialLevel, poisonicLevel]
    #print("ConsBuildings.getInfluencers~ INFO results: ", "EitherBuff:",results[0], ", Honker Vial Level:", results[1], ", Poisonic Tower Level:", results[2])
    return results

def setConsBuildingsProgressionTier(inputJSON, progressionTiersPreBuffs, progressionTiersPostBuffs, playerCount):
    playerBuildings = parseConsBuildingstoLists(inputJSON)
    influencers = getInfluencers(inputJSON)
    hasBuffs = influencers[0]
    if hasBuffs:
        #maxLevelList = [10, 201, 51, 10, 25, 60, 45, 5, 200,    140, 140, 140, 140, 140, 140, 140, 140, 140,   200, 200, 200, 200, 200, 200, 200, 200, 200] # these are true max, not recommended max
        maxLevelList = [10, 101, 51, 10, 25, 60, 20, 5, 200,    70, 70, 70, 70, 70, 70, 75, 75, 30,             200, 200, 200, 200, 200, 200, 200, 200, 200] # the recommended maxes
        #print("ConsBuilding.setConsBuildingsProgressionTiers~ INFO Both Construction Mastery and Wizard Atom found. Setting maxLevelList to PostBuff.")
    else:
        maxLevelList = [10, 101, 51, 10, 25, 60, 15, 5, 200,    50, 50, 50, 50, 50, 50, 50, 50, 30,             100, 100, 100, 100, 100, 100, 100, 100, 100]
        #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Setting maxLevelList to PreBuff.")

    # Make adjustments to tiers based on other influencers
    # 1) If any building is level 0, it gets promoted to SS tier
    buildingCounter = 0
    while buildingCounter < len(maxLevelList):
        if playerBuildings[buildingCounter] == 0:
            maxLevelList[buildingCounter] = 1 #With a max recommended level of 1
            for tier in progressionTiersPostBuffs:
                if buildingCounter in tier[2] and tier[1] != "SS":
                    tier[2].remove(buildingCounter) #Remove that building from any other non-SS tier.
                    progressionTiersPostBuffs[1][2].append(buildingCounter)
                    #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Level 0 building detected. Removing",getBuildingNameFromIndex(buildingCounter),"from PostBuff",tier[1],"and adding to SS with max level 1 instead.")
            for tier in progressionTiersPreBuffs:
                if buildingCounter in tier[2] and tier[1] != "SS":
                    tier[2].remove(buildingCounter) #Remove that building from any other non-SS tier.
                    progressionTiersPreBuffs[1][2].append(buildingCounter)
                    #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Level 0 building detected. Removing",getBuildingNameFromIndex(buildingCounter),"from PreBuff",tier[1],"and adding to SS with max level 1 instead.")
        buildingCounter += 1

    # 2) Honker vial is 12+ OR Trapper Drone is 20+, drop Trapper Drone priority
    if influencers[1] >= 12 or playerBuildings[6] >= 20:
        try:
            progressionTiersPostBuffs[2][2].remove(6) #Remove Trapper Drone from S Tier
            progressionTiersPostBuffs[5][2].append(6) #Add Trapper Drone to C tier
            if hasBuffs:
                maxLevelList[6] = 50
            #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved Trapper Drone from PostBuff S to C tier and changed level from 20 to 45")
        except Exception as reason:
            print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not remove Trapper Drone from PostBuff S tier:",reason)

    # 3) #Poisonic level 20+, drop Boulder Roller priority
    if influencers[2] >= 20:
        try:
            #PreBuffs
            progressionTiersPreBuffs[2][2].remove(11) #Remove Boulder Roller from S tier
            progressionTiersPreBuffs[6][2].append(11) #Add Boulder Roller to D tier
            #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved Boulder Roller from PreBuff S to D tier because Poisonic 20+")
            #PostBuffs
            progressionTiersPostBuffs[2][2].remove(11) #Remove Boulder Roller from S tier
            progressionTiersPostBuffs[3][2].append(11) #Add Boulder Roller to A tier
            #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved Boulder Roller from PostBuff S to A tier because Poisonic 20+")
        except Exception as reason:
            print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not move Boulder Roller from S tier in one or both tierlists:",reason)

    # 4) Talent Library Book 101+, drop priority
    if playerBuildings[1] >= 101:
        try:
            progressionTiersPostBuffs[2][2].remove(1) #Remove from S tier
            progressionTiersPostBuffs[5][2].append(1) #Add to C tier
            if hasBuffs:
                maxLevelList[1] = 201
            #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved 101+ Talent Library Book from PostBuff A to C tier.")
        except Exception as reason:
            print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not move 101+ Talent Library Book from PostBuff A tier to C tier:",reason)

    # 5) #Basic Towers to 70, drop priority
    for towerIndex in [9,10,11,12,13,14]:
        if playerBuildings[towerIndex] >= 70:
            try:
                progressionTiersPostBuffs[3][2].remove(towerIndex) #Remove from A tier
                progressionTiersPostBuffs[5][2].append(towerIndex) #Add to C tier
                if hasBuffs:
                    maxLevelList[towerIndex] = 140
                #print("ConsBuildings~ INFO Successfully moved 70+ basic tower from PostBuff A to C tier:",getBuildingNameFromIndex(towerIndex))
            except Exception as reason:
                print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not move 70+ basic tower from PostBuff A tier to C tier:",getBuildingNameFromIndex(towerIndex),reason)

    # 6) Fancy Towers to 75, drop priority
    for towerIndex in [15,16]:
        if playerBuildings[towerIndex] >= 75:
            try:
                progressionTiersPostBuffs[2][2].remove(towerIndex) #Remove from S tier
                progressionTiersPostBuffs[5][2].append(towerIndex) #Add to C tier
                if hasBuffs:
                    maxLevelList[towerIndex] = 140
                #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved 75+ fancy tower from PostBuff S to C tier:",getBuildingNameFromIndex(towerIndex))
            except Exception as reason:
                print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not move 75+ fancy tower from PostBuff S tier to C tier:",getBuildingNameFromIndex(towerIndex),reason)

    # 7) Voidinator to 30, drop priority
    if playerBuildings[17] >= 30: #Voidinator scaling is very bad
        try:
            progressionTiersPreBuffs[4][2].remove(17) #Remove from PreBuff B tier
            progressionTiersPreBuffs[5][2].append(17) #Add to C tier
            progressionTiersPostBuffs[3][2].remove(17) #Remove from PostBuff A tier
            progressionTiersPostBuffs[5][2].append(17) #Add to C tier
            if hasBuffs:
                maxLevelList[17] = 140
            #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Successfully moved 30+ Voidinator from A/B to C tier in both tierlists")
        except Exception as reason:
            print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION Could not move 30+ Voidinator from A/B to C tier in both tierlists:",reason)

    # Decide which tierset to use
    if influencers[0] == True: #Has either Construction Mastery or the Wizard atom
        progressionTiers = progressionTiersPostBuffs
        #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Either Construction Mastery or Wizard Atom found. Setting ProgressionTiers to PostBuff.")
    else:
        progressionTiers = progressionTiersPreBuffs
        #print("ConsBuildings.setConsBuildingsProgressionTier~ INFO Setting ProgressionTiers to PreBuff.")

    #advice_SS = "" #replaced as adviceComboList[1]
    #advice_S = "" #replaced as adviceComboList[2]
    #advice_A = "" #replaced as adviceComboList[3]
    #advice_B = "" #replaced as adviceComboList[4]
    #advice_C = "" #replaced as adviceComboList[5]
    #advice_D = "" #replaced as adviceComboList[6]
    #advice_F = "" #replaced as adviceComboList[7]
    adviceComboList = ["","","","","","","",""] #[0] = placeholder/default tier, unused
    #tier[0] = int tier
    #tier[1] = str Tier name
    #tier[2] = list of ints of tower indexes
    #tier[3] = str tower notes
    #tier[4] = str tier notes
    counter = 0
    while counter < len(progressionTiers):
        try:
            for recommendedBuilding in progressionTiers[counter][2]:
                #print("ConsBuildings.setConsBuildingsProgressionTier~ ", recommendedBuilding, getBuildingNameFromIndex(recommendedBuilding), playerBuildings[recommendedBuilding], maxLevelList[recommendedBuilding], "Cleared=", (maxLevelList[recommendedBuilding] <= playerBuildings[recommendedBuilding]))
                if maxLevelList[recommendedBuilding] > playerBuildings[recommendedBuilding]:
                    adviceComboList[counter] += getBuildingNameFromIndex(recommendedBuilding) + " (" + str(playerBuildings[recommendedBuilding]) + "/" + str(maxLevelList[recommendedBuilding]) + "), "
        except Exception as reason:
            print("ConsBuildings.setConsBuildingsProgressionTier~ EXCEPTION ProgressionTier evaluation error. Counter = ", counter, ", recommendedBuilding = ", recommendedBuilding, ", and Reason:", reason)
        counter += 1

    for adviceString in adviceComboList:
        if adviceString != "":
            index = adviceComboList.index(adviceString)
            adviceComboList[index] = progressionTiers[index][1] + " Tier: " + adviceComboList[index][:-2] #trim off final comma and space

    tier_ConsBuildings = 0
    overall_ConsBuildingsTier = 0
    advice_ConsBuildings1 = ""
    overall_ConsBuildingsTier = min(progressionTiers[-1][-0], tier_ConsBuildings)
    advice_ConsBuildingsCombined = ["Recommended Construction Buildings priorities for Trimmed Slots:", adviceComboList[1], adviceComboList[2], adviceComboList[3], adviceComboList[4], adviceComboList[5], adviceComboList[6], adviceComboList[7]]
    consBuildingsPR = progressionResults.progressionResults(overall_ConsBuildingsTier,advice_ConsBuildingsCombined,"")
    return consBuildingsPR
