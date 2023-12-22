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
        #print("ConsBuildings~ TYPE CHECK honkerVialLevel: ", type(honkerVialLevel), honkerVialLevel)
    except Exception as reason:
        honkerVialLevel = 0
        print("ConsBuildings~ EXCEPTION Unable to get honkerVialLevel: ", reason)

    #Boulder Roller level
    try:
        poisonicLevel = json.loads(inputJSON["Tower"])[16] #expected type of int
        #print("ConsBuildings~ TYPE CHECK poisonicLevel: ", type(poisonicLevel), poisonicLevel)
    except Exception as reason:
        poisonicLevel = 0
        print("ConsBuildings~ EXCEPTION Unable to get poisonicLevel: ", reason)

    #Other?
    consMastery = False
    atomCarbon = False
    try:
        highestCompletedRift = inputJSON["Rift"][0]
        if highestCompletedRift >= 41:
            consMastery = True
    except Exception as reason:
        print("ConsBuildings~ EXCEPTION: getBuffs Unable to find highest Rift level completed: ", reason)
    try:
        carbonLevel = inputJSON["Atoms"][5]
        if carbonLevel >= 1:
            atomCarbon = True
    except Exception as reason:
        print("ConsBuildings~ EXCEPTION: getBuffs Unable to find Atom Collider Carbon level: ", reason)
    results = [(consMastery and atomCarbon), honkerVialLevel, poisonicLevel]
    #print("ConsBuildings~ INFO getInfluencers.results: ", "BothBuffs:",results[0], ", Honker Vial Level:", results[1], ", Poisonic Tower Level:", results[2])
    return results

def setConsBuildingsProgressionTier(inputJSON, progressionTiersPreBuffs, progressionTiersPostBuffs, playerCount):
    playerBuildings = parseConsBuildingstoLists(inputJSON)
    influencers = getInfluencers(inputJSON)
    hasBuffs = influencers[0]
    if hasBuffs:
        #maxLevelList = [10, 201, 51, 10, 25, 60, 45, 5, 200,    140, 140, 140, 140, 140, 140, 140, 140, 140,   200, 200, 200, 200, 200, 200, 200, 200, 200] #these are true max, not recommended max
        maxLevelList = [10, 101, 51, 10, 25, 60, 20, 5, 200,    70, 70, 70, 70, 70, 70, 75, 75, 30,             200, 200, 200, 200, 200, 200, 200, 200, 200] #the old recommended maxes
        #print("ConsBuildings~ INFO Both Construction Mastery and Wizard Atom found. Setting maxLevelList to PostBuff.")
    else:
        maxLevelList = [10, 101, 51, 10, 25, 60, 15, 5, 200,    50, 50, 50, 50, 50, 50, 50, 50, 30,             100, 100, 100, 100, 100, 100, 100, 100, 100]
        #print("ConsBuildings~ INFO Setting maxLevelList to PreBuff.")

    #make adjustments to tiers based on other influencers
    if influencers[1] >= 12 or playerBuildings[6] >= 20: #Honker vial is 12+ OR Trapper Drone is 20+
        try:
            progressionTiersPostBuffs[2][2].remove(6) #Remove Trapper Drone from S Tier
            progressionTiersPostBuffs[5][2].append(6) #Add Trapper Drone to C tier
            if hasBuffs:
                maxLevelList[6] = 45
            #print("ConsBuildings~ INFO Successfully moved Trapper Drone from PostBuff S to C tier and changed level from 20 to 45")
        except Exception as reason:
            print("ConsBuildings~ EXCEPTION Could not remove Trapper Drone from PostBuff S tier:",reason)
    if influencers[2] >= 20: #Poisonic level 20+
        try:
            #PreBuffs
            progressionTiersPreBuffs[2][2].remove(11) #Remove Boulder Roller from S tier
            progressionTiersPreBuffs[6][2].append(11) #Add Boulder Roller to D tier
            #print("ConsBuildings~ INFO Successfully moved Boulder Roller from PreBuff S to D tier because Poisonic 20+")
            #PostBuffs
            progressionTiersPostBuffs[2][2].remove(11) #Remove Boulder Roller from S tier
            progressionTiersPostBuffs[3][2].append(11) #Add Boulder Roller to A tier
            #print("ConsBuildings~ INFO Successfully moved Boulder Roller from PostBuff S to A tier because Poisonic 20+")
        except Exception as reason:
            print("ConsBuildings~ EXCEPTION Could not move Boulder Roller from S tier in one or both tierlists:",reason)
    if playerBuildings[1] >= 101:
        try:
            progressionTiersPostBuffs[2][2].remove(1) #Remove from S tier
            progressionTiersPostBuffs[5][2].append(1) #Add to C tier
            if hasBuffs:
                maxLevelList[1] = 201
            #print("ConsBuildings~ INFO Successfully moved 101+ Talent Library Book from PostBuff A to C tier.")
        except Exception as reason:
            print("ConsBuildings~ EXCEPTION Could not move 101+ Talent Library Book from PostBuff A tier to C tier:",reason)

    for towerIndex in [9,10,11,12,13,14]: #Basic Towers to 70
        if playerBuildings[towerIndex] >= 70:
            try:
                progressionTiersPostBuffs[3][2].remove(towerIndex) #Remove from A tier
                progressionTiersPostBuffs[5][2].append(towerIndex) #Add to C tier
                if hasBuffs:
                    maxLevelList[towerIndex] = 140
                #print("ConsBuildings~ INFO Successfully moved 70+ basic tower from PostBuff A to C tier:",getBuildingNameFromIndex(towerIndex))
            except Exception as reason:
                print("ConsBuildings~ EXCEPTION Could not move 70+ basic tower from PostBuff A tier to C tier:",getBuildingNameFromIndex(towerIndex),reason)
    for towerIndex in [15,16]: #Fancy Towers
        if playerBuildings[towerIndex] >= 75:
            try:
                progressionTiersPostBuffs[2][2].remove(towerIndex) #Remove from S tier
                progressionTiersPostBuffs[5][2].append(towerIndex) #Add to C tier
                if hasBuffs:
                    maxLevelList[towerIndex] = 140
                #print("ConsBuildings~ INFO Successfully moved 75+ fancy tower from PostBuff S to C tier:",getBuildingNameFromIndex(towerIndex))
            except Exception as reason:
                print("ConsBuildings~ EXCEPTION Could not move 75+ fancy tower from PostBuff S tier to C tier:",getBuildingNameFromIndex(towerIndex),reason)
    if playerBuildings[17] >= 30: #Voidinator scaling is very bad
        try:
            progressionTiersPreBuffs[4][2].remove(17) #Remove from PreBuff B tier
            progressionTiersPreBuffs[5][2].append(17) #Add to C tier
            progressionTiersPostBuffs[3][2].remove(17) #Remove from PostBuff A tier
            progressionTiersPostBuffs[5][2].append(17) #Add to C tier
            if hasBuffs:
                maxLevelList[17] = 140
            #print("ConsBuildings~ INFO Successfully moved 30+ Voidinator from A/B to C tier in both tierlists")
        except Exception as reason:
            print("ConsBuildings~ EXCEPTION Could not move 30+ Voidinator from A/B to C tier in both tierlists:",reason)
    #decide which tierset to use
    if influencers[0] == True: #Has both Construction Mastery and the Wizard atom
        progressionTiers = progressionTiersPostBuffs
        #print("ConsBuildings~ INFO Both Construction Mastery and Wizard Atom found. Setting ProgressionTiers to PostBuff.")
    else:
        progressionTiers = progressionTiersPreBuffs
        #print("ConsBuildings~ INFO Setting ProgressionTiers to PreBuff.")

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
                #print("ConsBuildings~ ", recommendedBuilding, getBuildingNameFromIndex(recommendedBuilding), playerBuildings[recommendedBuilding], maxLevelList[recommendedBuilding], "Cleared=", (maxLevelList[recommendedBuilding] <= playerBuildings[recommendedBuilding]))
                if maxLevelList[recommendedBuilding] > playerBuildings[recommendedBuilding]:
                    adviceComboList[counter] += getBuildingNameFromIndex(recommendedBuilding) + " (" + str(playerBuildings[recommendedBuilding]) + "/" + str(maxLevelList[recommendedBuilding]) + "), "
        except Exception as reason:
            print("ConsBuildings~ EXCEPTION ProgressionTier evaluation error. Counter = ", counter, ", recommendedBuilding = ", recommendedBuilding, ", and Reason:", reason)
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
