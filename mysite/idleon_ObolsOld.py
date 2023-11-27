import json
import progressionResults
import idleon_CombatLevels

def parseObolValuestoDict(inputSection):
    obolsDict = json.loads(inputSection)
    return obolsDict

def getExpectedMiscRerollStatus(obolType):
    match obolType:
        case "ObolBronzePop" | "ObolSilverPop" | "ObolSilverLuck" | "ObolGoldLuck" | "ObolPlatinumLuck" | "ObolPinkLuck" | "ObolHyper0" | "ObolKnight":
            return {"UQ1val":1,"UQ1txt":"%_DROP_CHANCE"}
        case "ObolKruk":
            return {"UQ1val":1,"UQ1txt":"%_ALL_AFK_GAIN"}
        case "ObolTroll" | "ObolHyper1":
            return {"UQ1val":1,"UQ1txt":"%_ALL_STATS"}
        case "ObolChizoarA" | "ObolHyper2":
            return {"UQ1val":1,"UQ1txt":"%_TOTAL_DAMAGE"}
        case "ObolSlush":
            return {"UQ1val":1,"UQ1txt":"%_SKILL_EFFICIENCY"}
        case "ObolPlatinumChoppin" | "ObolPinkChoppin":
            return {"UQ1val":1,"UQ1txt":"%_CHOP_EFFICIENCY"}
        case "ObolPlatinumMining" | "ObolPinkMining":
            return {"UQ1val":1,"UQ1txt":"%_MINING_EFFICINCY"}
        case "ObolPlatinumFishing" | "ObolPinkFishing":
            return {"UQ1val":1,"UQ1txt":"%_FISHIN_EFFICINCY"}
        case "ObolPlatinumCatching" | "ObolPinkCatching":
            return {"UQ1val":1,"UQ1txt":"%_CATCH_EFFICINCY"}
        case "ObolBronzeCons" | "ObolSilverCons" | "ObolGoldCons" | "ObolPlatinumCons" | "ObolPinkCons":
            return {"UQ1val":1, "UQ1txt":"%_BUILD_SPD"}
        case _:
            return {}

def getDRObolNames():
    drObolNamesList = ["ObolBronzePop", "ObolSilverPop", "ObolSilverLuck", "ObolGoldLuck", "ObolPlatinumLuck", "ObolPinkLuck", "ObolHyper0", "ObolKnight"]
    drObolNamesAndTypesDict = {
        "ObolBronzePop":"Circle",
        "ObolSilverPop":"Circle",
        "ObolHyper0":"Circle",
        "ObolSilverLuck":"Square",
        "ObolGoldLuck":"Square",
        "ObolKnight":"Square",
        "ObolPlatinumLuck":"Hexagon",
        "ObolPinkLuck":"Sparkle"
        }
    return drObolNamesAndTypesDict

def getSkillObolsWithMiscRerollNames():
    return ["ObolPlatinumChoppin", "ObolPinkChoppin","ObolPlatinumMining", "ObolPinkMining","ObolPlatinumFishing", "ObolPinkFishing","ObolPlatinumCatching", "ObolPinkCatching"]

def getBossObolsWithValuableMiscRerollNames():
    return ["ObolSlush","ObolTroll","ObolHyper1","ObolKruk","ObolChizoarA","ObolHyper2"]

def getIgnorableObols():
    #Obols which can only reroll stats. Not trash, but not as important.
    return [""]

def getTrashObols():
    #This is going to include Obols you usually only make for Slab, then trash
    return [""]


def getAllObols(inputJSON, playerCount):
    properlyRolledObolsDict = {}
    notRolledObolsDict = {}
    expectedRerollDict = {}
    obolSaveDataNamesList = ["ObolEqO1","ObolEqO2", "ObolEqO0_0", "ObolEqO0_1", "ObolEqO0_2", "ObolEqO0_3", "ObolEqO0_4", "ObolEqO0_5", "ObolEqO0_6", "ObolEqO0_7", "ObolEqO0_8", "ObolEqO0_9"]
    obolSaveDataValuesList = ["ObolEqMAPz1", "ObolEqMAPz2", "ObolEqMAP_0", "ObolEqMAP_1", "ObolEqMAP_2", "ObolEqMAP_3", "ObolEqMAP_4", "ObolEqMAP_5", "ObolEqMAP_6", "ObolEqMAP_7", "ObolEqMAP_8", "ObolEqMAP_9"]
    obolIndex = -4
    while obolIndex < len(obolSaveDataNamesList):
        #ISSUE: SOMETHING WRONG HERE. THE NAMES AND VALUES DON'T ALWAYS MATCH UP.
        #Lexagraphical sorting issue: (1,11,12,2,23,3,etc.)
        if obolIndex < 0:
            print("Loading Obol data from inventory:",obolIndex+4)
            obolValuesDict = parseObolValuestoDict(inputJSON["ObolInvMAP_"+str(obolIndex+4)]) #expected type of dict
            obolNamesDict = inputJSON["ObolInvOr"][obolIndex+4] #expected type of dict
            #print("Found data of type:", type(obolNamesDict))
            obolNamesList = []
            for key in obolNamesDict:
                if key != "length" and key in obolValuesDict.keys():
                    obolNamesList.append(obolNamesDict[key])
                else:
                    print(key,"either equals length or not found in obolValuesDict.keys() because it isn't rerolled")
            #print("Inventory ObolNamesList:",obolNamesList)
        else:
            obolValuesDict = parseObolValuestoDict(inputJSON[obolSaveDataValuesList[obolIndex]]) #expected type of dict
            obolNamesList = inputJSON[obolSaveDataNamesList[obolIndex]] #expected type of list

        print("Loaded ObolNames:",obolNamesList)
        print("Loaded ObolValues:",obolValuesDict)
        indexCounter = 0
        while indexCounter < len(obolNamesList):
            #print("ObolNamesList:",obolNamesList)
            if str(obolNamesList[indexCounter]).startswith("Obol") and not str(obolNamesList[indexCounter]).startswith("ObolLocked"):
                #print("Fetching expected reroll status for obolNamesList[indexCounter]:",obolNamesList[indexCounter])
                expectedRerollDict[indexCounter] = getExpectedMiscRerollStatus(obolNamesList[indexCounter])
                rerollStatusCount = 0
                #print(obolValuesDict.keys())
                if str(indexCounter) in obolValuesDict.keys():
                    for expectation in expectedRerollDict[indexCounter]:
                        #print("Expectation:",expectation)
                        #print("expectedRerollDict[indexCounter]:", expectedRerollDict[indexCounter])
                        #print("obolValuesDict:",obolValuesDict)
                        #print("obolValuesDict[str(indexCounter)]:",obolValuesDict[str(indexCounter)])
                        if expectation in obolValuesDict[str(indexCounter)]:
                            print(obolNamesList[indexCounter],"Stat:",expectation,"Player Obol Value:",obolValuesDict[str(indexCounter)][expectation],"Expected Value:",expectedRerollDict[indexCounter][expectation])
                            if obolValuesDict[str(indexCounter)][expectation] >= expectedRerollDict[indexCounter][expectation]:
                                rerollStatusCount += 1
                            else:
                                print("Found reroll, but bad value:",obolValuesDict[str(indexCounter)][expectation],"not >=",expectedRerollDict[indexCounter][expectation])
                    if rerollStatusCount == 2:
                        #print("Index:",indexCounter,"Name:",obolNamesList[indexCounter],"Status: Properly Rerolled")
                        if obolNamesList[indexCounter] in properlyRolledObolsDict:
                            properlyRolledObolsDict[obolNamesList[indexCounter]] += 1
                        else:
                            properlyRolledObolsDict[obolNamesList[indexCounter]] = 1
                    else: #not properly rerolled
                        print("Index:",indexCounter,"Name:",obolNamesList[indexCounter],"Status: Not Properly Rerolled")
                        if obolNamesList[indexCounter] in notRolledObolsDict:
                            notRolledObolsDict[obolNamesList[indexCounter]] += 1
                        else:
                            notRolledObolsDict[obolNamesList[indexCounter]] = 1
            indexCounter += 1
        obolIndex += 1
    #print(type(familyObolNames), type(familyObolValues))
    print("properlyRolledObolsDict:",properlyRolledObolsDict)
    print("notRolledObolsDict:",notRolledObolsDict)
    return [properlyRolledObolsDict, notRolledObolsDict]

def setObolsProgressionTier(inputJSON, playerCount, progressionTiers, fromPublicIEBool):
    allObols = getAllObols(inputJSON, playerCount)
    drObolNamesDict = getDRObolNames()
    personalAndFamilyDropRateSetActualCounts = {"Circle":0,"Square":0,"Hexagon":0,"Sparkle":0}
    personalAndFamilyDropRateSetMaxCounts = {"Circle":24,"Square":10,"Hexagon":6,"Sparkle":5}
    for obol in allObols[0]: #properly rolled obols only
        #print("Looking for",obol,"within DR Names")
        if obol in drObolNamesDict.keys():
            print(obol,"found within DR Names. Increase its shape (",drObolNamesDict[obol],") count by",allObols[0][obol])
            personalAndFamilyDropRateSetActualCounts[drObolNamesDict[obol]] += allObols[0][obol]
    print("Properly Rolled DR Set Counts:",personalAndFamilyDropRateSetActualCounts)
    tier_Obols = 0
    overall_ObolsTier = 0
    advice_Obols1 = " * TBD Obol Advice placeholder"
    overall_ObolsTier = min(progressionTiers[-1][-0], tier_Obols)
    advice_ObolsCombined = ["### Best Obols tier met: " + str(overall_ObolsTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Obols actions:", advice_Obols1]
    obolsPR = progressionResults.progressionResults(overall_ObolsTier,advice_ObolsCombined,"")
    return obolsPR
