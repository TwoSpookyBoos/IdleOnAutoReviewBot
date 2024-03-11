import json
import idleon_CombatLevels

def parseObolValuestoDict(inputSection):
    obolsDict = json.loads(inputSection)
    return obolsDict

def getExpectedRerollStatus(obolType):
    match obolType:
        case "ObolBronzePop" | "ObolSilverPop" | "ObolSilverLuck" | "ObolGoldLuck" | "ObolPlatinumLuck" | "ObolPinkLuck" | "ObolHyper0" | "ObolKnight":
            return {"UQ1val":1,"UQ1txt":"%_DROP_CHANCE"}
        case "ObolKruk":
            return {"UQ1val":1,"UQ1txt":"%_ALL_AFK_GAIN"}
        case "ObolTroll" | "ObolHyper1":
            return {"UQ1val":1,"UQ1txt":"%_ALL_STATS"}
        case "ObolChizoarA" | "ObolHyper2":
            return {"UQ1val":1,"UQ1txt":"%_TOTAL_DAMAGE"}
        case "ObolHyper3":
            return {"UQ1val":1,"UQ1txt":"%_MULTIKILL_PER_TIER"}
        case "ObolBronzeKill" | "ObolSilverKill" | "ObolGoldKill" | "ObolPlatinumKill" | "ObolPinkKill":
            return {"UQ1val":1,"UQ1txt":"%_MULTIKILL"}
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
        case "ObolBronzeChoppin" | "ObolSilverChoppin" | "ObolGoldChoppin" | "ObolBronzeWorship" | "ObolSilverWorship" | "ObolGoldWorship" | "ObolPlatinumWorship" | "ObolPinkWorship" | "ObolBronze2" | "ObolSilver2" | "ObolGold2" | "ObolPlatinum2" | "ObolPink2":
            return {"WIS":1}
        case "ObolBronzeMining" | "ObolSilverMining" | "ObolGoldMining" | "ObolBronzeFishing" | "ObolSilverFishing" | "ObolGoldFishing" | "ObolBronze0" | "ObolSilver0" | "ObolGold0" | "ObolPlatinum0" | "ObolPink0":
            return {"STR":1}
        case "ObolBronzeCatching" | "ObolSilverCatching" | "ObolGoldCatching" | "ObolBronzeTrapping" | "ObolSilverTrapping" | "ObolGoldTrapping" | "ObolPlatinumTrapping" | "ObolPinkTrapping" | "ObolBronze1" | "ObolSilver1" | "ObolGold1" | "ObolPlatinum1" | "ObolPink1":
            return {"AGI":1}
        case "ObolBronze3" | "ObolSilver3" | "ObolGold3" | "ObolPlatinum3" | "ObolPink3":
            return {"LUK":1}
        case "ObolBronzeDamage" | "ObolSilverDamage" | "ObolGoldDamage" | "ObolPlatinumDamage" | "ObolPinkDamage":
            return {"UQ1val":1, "UQ1txt":"_BASE_DAMAGE"}
        case _:
            #Known obols I am not currently returning:
            #Def, Money, Card, EXP, AmarokA,
            print("Obols.getExpectedRerollStatus~ Unknown Obol found:",obolType)
            return {"Unknown":9999}

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
    everyObolDict = {}
    unrolledObolDict = {}
    properlyRolledObolsDict = {}
    badRolledObolsDict = {}
    expectedRerollDict = {}
    obolSaveDataNamesList = ["ObolEqO1","ObolEqO2", "ObolEqO0_0", "ObolEqO0_1", "ObolEqO0_2", "ObolEqO0_3", "ObolEqO0_4", "ObolEqO0_5", "ObolEqO0_6", "ObolEqO0_7", "ObolEqO0_8", "ObolEqO0_9"]
    obolSaveDataValuesList = ["ObolEqMAPz1", "ObolEqMAPz2", "ObolEqMAP_0", "ObolEqMAP_1", "ObolEqMAP_2", "ObolEqMAP_3", "ObolEqMAP_4", "ObolEqMAP_5", "ObolEqMAP_6", "ObolEqMAP_7", "ObolEqMAP_8", "ObolEqMAP_9"]
    obolLogging = []
    obolExceptions = []
    obolIndex = -4
    #while obolIndex < 0: #testing inventory only
    while obolIndex < len(obolSaveDataNamesList):
        if obolIndex < 0: #4 inventories
            ###obolLogging.append(["Loading Obol data from inventory:",obolIndex+4])
            obolValuesDict = parseObolValuestoDict(inputJSON["ObolInvMAP_"+str(obolIndex+4)]) #expected type of dict
            obolNamesDict = inputJSON["ObolInvOr"][obolIndex+4] #expected type of dict
            #Lexagraphical sorting issue (1,11,12,2,23,3,etc.) in names, but not in values. To make them match, I'm intentionally doing the same bad sorting in values.
            obolValuesDict = dict(sorted(obolValuesDict.items()))
            ###obolLogging.append(["Sorted Values Dict:",obolNamesDict])
            obolNamesList = []
            for key in obolNamesDict:
                ###obolLogging.append(["Checking for key",key,"in obolValuesDict"])
                if key != "length" and obolNamesDict[key] != "Blank" and not obolNamesDict[key].startswith("LockedInvSpace"): #and key in obolValuesDict.keys():
                    obolNamesList.append(obolNamesDict[key])
                #else:
                    ###obolLogging.append([key,"either equals length or not found in obolValuesDict.keys() because it isn't rerolled"])
            ###obolLogging.append(["Inventory ObolNamesList:",obolNamesList])
        else: #0 and above looks through the Family, Reroll, and player equipped slots
            if obolIndex < playerCount:
                obolValuesDict = parseObolValuestoDict(inputJSON[obolSaveDataValuesList[obolIndex]]) #expected type of dict
                obolValuesDict = dict(sorted(obolValuesDict.items()))
                defaultObolNamesList = inputJSON[obolSaveDataNamesList[obolIndex]] #expected type of list, includes Blanks and Locks
                obolNamesList = []
                for name in defaultObolNamesList:
                    if name != "length" and name != "Blank" and not name.startswith("ObolLocked"): #and key in obolValuesDict.keys():
                        obolNamesList.append(name)

        #track every obol found
        if len(obolNamesList) > 0:
            for obol in obolNamesList:
                if obol in everyObolDict:
                    everyObolDict[obol] += 1
                else:
                    everyObolDict[obol] = 1

        indexCounter = 0
        if len(obolValuesDict.keys()) > 0:
            while indexCounter < len(obolValuesDict):
                ###obolLogging.append(["ObolNamesList:",obolNamesList])
                if str(obolNamesList[indexCounter]).startswith("Obol") and not str(obolNamesList[indexCounter]).startswith("ObolLocked") and not str(obolNamesList[indexCounter]).startswith("Locked") and not str(obolNamesList[indexCounter]).startswith("Blank"):
                    ###obolLogging.append(["Fetching expected reroll status for list(obolValuesDict.keys())[indexCounter]:",indexCounter])
                    expectedRerollDict[list(obolValuesDict.keys())[indexCounter]] = getExpectedRerollStatus(obolNamesList[indexCounter])
                indexCounter += 1
            #Lexagraphical sorting issue (1,11,12,2,23,3,etc.) in names, but not in values. To make them match, I'm intentionally doing the same bad sorting in values.
            #expectedRerollDict = dict(sorted(expectedRerollDict.items()))
        obolLogging.append(["Loaded ObolNames from (-4 through -1 are inventory)",obolIndex,":",obolNamesList])
        obolLogging.append(["Loaded ObolValues:",obolValuesDict])
        obolLogging.append(["Loaded Sorted Expected Reroll Dict:",expectedRerollDict])

        valuesCounter = 0
        namesCounter = 0
        if len(expectedRerollDict.keys()) > 0:
            maxValueIndexInt = 0
            for key in expectedRerollDict.keys():
                if int(key) >= maxValueIndexInt:
                    maxValueIndexInt = int(key)
            while valuesCounter <= maxValueIndexInt:
                rerollStatusCount = 0
                ###obolLogging.append(expectedRerollDict.keys())
                if str(valuesCounter) in expectedRerollDict.keys():
                    ###obolLogging.append(expectedRerollDict)
                    if len(expectedRerollDict[str(valuesCounter)]) > 0:
                        ###obolLogging.append(["NameCounter:",namesCounter,"ValuesCounter:",valuesCounter])
                        for expectation in expectedRerollDict[str(valuesCounter)]:
                            ####obolLogging.append("Expectation:",expectation)
                            ####obolLogging.append("expectedRerollDict[valuesCounter]:", expectedRerollDict[valuesCounter])
                            ####obolLogging.append("obolValuesDict:",obolValuesDict)
                            ####obolLogging.append("obolValuesDict[str(valuesCounter)]:",obolValuesDict[str(valuesCounter)])
                            if expectation in obolValuesDict[str(valuesCounter)]:
                                ###obolLogging.append([obolNamesList[namesCounter],"Stat:",expectation,"Player Obol Value:",obolValuesDict[str(valuesCounter)][expectation],"Expected Value:",expectedRerollDict[str(valuesCounter)][expectation]])
                                #print([obolNamesList[namesCounter],"Stat:",expectation,"Player Obol Value:",obolValuesDict[str(valuesCounter)][expectation],"Expected Value:",expectedRerollDict[str(valuesCounter)][expectation]])
                                try:
                                    if obolValuesDict[str(valuesCounter)][expectation] >= expectedRerollDict[str(valuesCounter)][expectation]:
                                        ###obolLogging.append(["Found GOOD reroll on",obolNamesList[namesCounter],obolValuesDict[str(valuesCounter)][expectation]," >=",expectedRerollDict[str(valuesCounter)][expectation]])
                                        rerollStatusCount += 1
                                    else:
                                        rerollStatusCount -= 1
                                        ###obolLogging.append(["Found BAD reroll on",obolNamesList[namesCounter],obolValuesDict[str(valuesCounter)][expectation],"not >=",expectedRerollDict[str(valuesCounter)][expectation]])
                                except Exception as reason:
                                    rerollStatusCount -= 10
                                    obolExceptions.append(["Obols.getAllObols~ EXCEPTION: Unable to compare obol actual value to expected value:",reason,[obolNamesList[namesCounter],"Stat:",expectation,"Player Obol Value:",obolValuesDict[str(valuesCounter)][expectation],"Expected Value:",expectedRerollDict[str(valuesCounter)][expectation]]])
                    if rerollStatusCount > 0:
                        obolLogging.append(["NamesCounter:",namesCounter,"ValuesCounter:",valuesCounter,"Name:",obolNamesList[namesCounter],"Status: Good Reroll"])
                        if obolNamesList[namesCounter] in properlyRolledObolsDict:
                            properlyRolledObolsDict[obolNamesList[namesCounter]] += 1
                        else:
                            properlyRolledObolsDict[obolNamesList[namesCounter]] = 1
                    else: #not properly rerolled
                        obolLogging.append(["NamesCounter:",namesCounter,"ValuesCounter:",valuesCounter,"Name:",obolNamesList[namesCounter],"Status: Bad Reroll"])
                        if obolNamesList[namesCounter] in badRolledObolsDict:
                            badRolledObolsDict[obolNamesList[namesCounter]] += 1
                        else:
                            badRolledObolsDict[obolNamesList[namesCounter]] = 1
                    namesCounter += 1
                valuesCounter += 1
        expectedRerollDict = {}
        obolIndex += 1

    #decipher unrolled obols = every - proper - bad
    unrolledObolDict = everyObolDict
    for obol in properlyRolledObolsDict:
        unrolledObolDict[obol] -= properlyRolledObolsDict[obol]
    for obol in badRolledObolsDict:
        unrolledObolDict[obol] -= badRolledObolsDict[obol]

    ####obolLogging.append(type(familyObolNames), type(familyObolValues))
    obolLogging.append(["properlyRolledObolsDict:",properlyRolledObolsDict])
    obolLogging.append(["badRolledObolsDict:",badRolledObolsDict])
    obolLogging.append(["unrolledObolsDict:",unrolledObolDict])

    #Troubleshooting Output
    #print("Obols.obolLogging~",obolLogging)
    with open("./logging/obolLogging.txt","w") as outfile:
        for item in obolLogging:
            outfile.writelines(str(item))
        outfile.write("\n")
    outfile.close()

    if len(obolExceptions)>0:
        print("Obols.obolExceptions~",obolExceptions)
    return [properlyRolledObolsDict, badRolledObolsDict, unrolledObolDict]


def setObolsProgressionTier(inputJSON, playerCount, progressionTiers, fromPublicIEBool):
    allObols = getAllObols(inputJSON, playerCount)
    drObolNamesDict = getDRObolNames()
    goodDropRateSetActualCounts = {"Circle":0,"Square":0,"Hexagon":0,"Sparkle":0}
    badDropRateSetActualCounts = {"Circle":0,"Square":0,"Hexagon":0,"Sparkle":0}
    unrolledDropRateSetActualCounts = {"Circle":0,"Square":0,"Hexagon":0,"Sparkle":0}
    personalAndFamilyDropRateSetMaxCounts = {"Circle":24,"Square":10,"Hexagon":6,"Sparkle":5}
    for obol in allObols[0]: #properly rolled obols only
        #print("Obols.setObolsProgressionTier~ Looking for",obol,"within DR Names")
        if obol in drObolNamesDict.keys():
            #print("Obols.setObolsProgressionTier~ ",obol,"found within DR Names. Increase its shape (",drObolNamesDict[obol],") count by",allObols[0][obol])
            goodDropRateSetActualCounts[drObolNamesDict[obol]] += allObols[0][obol]
    for obol in allObols[1]: #badly rolled obols only
        if obol in drObolNamesDict.keys():
            badDropRateSetActualCounts[drObolNamesDict[obol]] += allObols[1][obol]
    for obol in allObols[2]: #unrolled obols only
        if obol in drObolNamesDict.keys():
            unrolledDropRateSetActualCounts[drObolNamesDict[obol]] += allObols[2][obol]
    print("Obols.setObolsProgressionTier~ Properly Rolled DR Set Counts:",goodDropRateSetActualCounts)
    print("Obols.setObolsProgressionTier~ Badly Rolled DR Set Counts:",badDropRateSetActualCounts)
    print("Obols.setObolsProgressionTier~ Unrolled DR Set Counts:",unrolledDropRateSetActualCounts)
    tier_Obols = 0
    overall_ObolsTier = 0
    advice_GoodDropRateObols = " * Good DR Obol Placeholder"
    advice_BadDropRateObols = " * Bad DR Obol Placeholder"
    advice_UnrolledDropRateObols = " * Unrolled DR Obol Placeholder"
    advice_GoodDropRateObols = (" * For Drop Rate, you have properly rerolled " +
        str(goodDropRateSetActualCounts["Circle"]) + "/" + str(personalAndFamilyDropRateSetMaxCounts["Circle"]) + " Circles, " +
        str(goodDropRateSetActualCounts["Square"]) + "/" + str(personalAndFamilyDropRateSetMaxCounts["Square"]) + " Squares, " +
        str(goodDropRateSetActualCounts["Hexagon"]) + "/" + str(personalAndFamilyDropRateSetMaxCounts["Hexagon"]) + " Hexagons, and " +
        str(goodDropRateSetActualCounts["Sparkle"]) + "/" + str(personalAndFamilyDropRateSetMaxCounts["Sparkle"]) + " Sparkles for a max-slot Personal and Family set."
        )
    advice_BadDropRateObols = (" * For Drop Rate, you have badly rerolled " +
        str(badDropRateSetActualCounts["Circle"]) +  " Circles, " + str(badDropRateSetActualCounts["Square"]) +  " Squares, " +
        str(badDropRateSetActualCounts["Hexagon"]) + " Hexagons, and " + str(badDropRateSetActualCounts["Sparkle"]) + " Sparkles"
        )
    advice_UnrolledDropRateObols = (" * For Drop Rate, you have not attempted to reroll " +
        str(unrolledDropRateSetActualCounts["Circle"]) +  " Circles, " + str(unrolledDropRateSetActualCounts["Square"]) +  " Squares, " +
        str(unrolledDropRateSetActualCounts["Hexagon"]) + " Hexagons, and " + str(unrolledDropRateSetActualCounts["Sparkle"]) + " Sparkles"
        )
    advice_Obols1 = " * TBD Obol Advice placeholder"
    overall_ObolsTier = min(progressionTiers[-1][-0], tier_Obols)
    #advice_ObolsCombined = ["### Best Obols tier met: " + str(overall_ObolsTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Obols actions:", advice_GoodDropRateObols,advice_BadDropRateObols]
    advice_ObolsCombined = ["### Obols Header placeholder! Wow, such holding. Very place. 5/7.", advice_GoodDropRateObols,advice_BadDropRateObols,advice_UnrolledDropRateObols]
    #obolsPR = progressionResults.progressionResults(overall_ObolsTier,advice_ObolsCombined,"")
    #return obolsPR
