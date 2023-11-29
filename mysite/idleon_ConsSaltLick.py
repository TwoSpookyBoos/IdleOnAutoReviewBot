import json
import progressionResults

def parseConsSaltLick(inputJSON):
    saltLickList = json.loads(inputJSON["SaltLick"])
    saltLickDict = {
        'Printer Sample Size':saltLickList[0],
        'Obol Storage':saltLickList[1],
        'Refinery Speed':saltLickList[2],
        'EXP':saltLickList[3],
        'Max Book':saltLickList[4],
        'Alchemy Liquids':saltLickList[5],
        'TD Points':saltLickList[6],
        'Movespeed':saltLickList[7],
        'Multikill':saltLickList[8],
        'Damage':saltLickList[9]
        #'Tab3-1':saltLickList[10] #Not Yet Implemented
        #'Tab3-2':saltLickList[11] #Not Yet Implemented
        #'Tab3-3':saltLickList[12] #Not Yet Implemented
        #'Tab3-4':saltLickList[13] #Not Yet Implemented
        #'Tab3-5':saltLickList[14] #Not Yet Implemented
        #'Tab4-1':saltLickList[15] #Not Yet Implemented
        #'Tab4-2':saltLickList[16] #Not Yet Implemented
        #'Tab4-3':saltLickList[17] #Not Yet Implemented
        #'Tab4-4':saltLickList[18] #Not Yet Implemented
        #'Tab4-5':saltLickList[19] #Not Yet Implemented
        }
    #print(saltLickDict)
    return saltLickDict

def setConsSaltLickProgressionTier(inputJSON, progressionTiers):
    saltLickDict = parseConsSaltLick(inputJSON)
    #print(saltLickDict)
    tier_RequiredSaltLickUpgrades = 0
    sum_TotalMaxedSaltLickUpgrades = 0
    overall_ConsSaltLickTier = 0
    advice_RequiredSaltLickUpgrades = ""
    advice_ConsSaltLickCombined = ""
    #Assess tiers
    for tier in progressionTiers:
        #int tier, #dict RequiredSaltLickUpgrades, str Notes
        requiredSaltLickUpgrades = tier[1]
        all_RequiredSaltLickUpgrades = True
        for key, value in requiredSaltLickUpgrades.items():
            #print("If ",saltLickDict[key]," < ",requiredSaltLickUpgrades[key]," - ", (saltLickDict[key] < requiredSaltLickUpgrades[key]))
            if saltLickDict[key] < requiredSaltLickUpgrades[key]:
                all_RequiredSaltLickUpgrades = False
                if advice_RequiredSaltLickUpgrades == "":
                    advice_RequiredSaltLickUpgrades = (" * The next best/cheapest bonus to max is probably " + str(key) + " which requires " + tier[2])
                #else #don't write out new advice, only want the lowest.
            if all_RequiredSaltLickUpgrades == True:
                sum_TotalMaxedSaltLickUpgrades += 1
            if tier_RequiredSaltLickUpgrades == (tier[0]-1) and all_RequiredSaltLickUpgrades == True:
                tier_RequiredSaltLickUpgrades = tier[0]
    overall_ConsSaltLickTier = min(10, sum_TotalMaxedSaltLickUpgrades) #Looks silly, but may get more evaluations in the future
    #Generate advice statement
    if overall_ConsSaltLickTier == 10:
        advice_RequiredSaltLickUpgrades = " * Nada. You best <3"
    advice_ConsSaltLickCombined = ["### Maxed Salt Lick Upgrades: " + str(overall_ConsSaltLickTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Salt Lick action:", advice_RequiredSaltLickUpgrades]
    #Print fun stuff
    #print(advice_ConsSaltLickCombined)
    consSaltLickPR = progressionResults.progressionResults(overall_ConsSaltLickTier,advice_ConsSaltLickCombined,"")
    return consSaltLickPR