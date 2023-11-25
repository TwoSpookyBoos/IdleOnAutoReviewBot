import json
import progressionResults

def parseObolValuestoDict(inputSection):
    obolsDict = json.loads(inputSection)
    return obolsDict

def getAllObols(inputJSON, playerCount):
    properlyRolledObolsDict = {}
    notRolledObolsDict = {}
    familyObolNames = inputJSON["ObolEqO1"]
    familyObolValues = parseObolValuestoDict(inputJSON["ObolEqMAPz1"])
    #print(type(familyObolNames), type(familyObolValues))
    return [properlyRolledObolsDict, notRolledObolsDict]

def setObolsProgressionTier(inputJSON, playerCount, progressionTiers):
    allObols = getAllObols(inputJSON, playerCount)
    tier_Obols = 0
    overall_ObolsTier = 0
    advice_Obols1 = ""
    overall_ObolsTier = min(progressionTiers[-1][-0], tier_Obols)
    advice_ObolsCombined = ["Best Obols tier met: " + str(overall_ObolsTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Obols actions:",advice_Obols1]
    obolsPR = progressionResults.progressionResults(overall_ObolsTier,advice_ObolsCombined,"")
    return obolsPR
