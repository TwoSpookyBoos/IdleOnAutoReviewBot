import json
import progressionResults

def getReadablePrayerNames(inputNumber):
    match inputNumber:
        case 0:
            return "Big Brain Time (Forest Soul)"
        case 1:
            return "Skilled Dimwit (Forest Soul)"
        case 2:
            return "Unending Energy (Forest Soul)"
        case 3:
            return "Shiny Snitch (Forest Soul)"
        case 4:
            return "Zerg Rushogen (Forest Soul)"
        case 5:
            return "Tachion of the Titans (Dune Soul)"
        case 6:
            return "Balance of Precision (Dune Soul)"
        case 7:
            return "Midas Minded (Dune Soul)"
        case 8:
            return "Jawbreaker (Dune Soul)"
        case 9:
            return "The Royal Sampler (Rooted Soul)"
        case 10:
            return "Antifun Spirit (Rooted Soul)"
        case 11:
            return "Circular Criticals (Rooted Soul)"
        case 12:
            return "Ruck Sack (Rooted Soul)"
        case 13:
            return "Fibers of Absence (Frigid Soul)"
        case 14:
            return "Vacuous Tissue (Frigid Soul)"
        case 15:
            return "Beefy For Real (Frigid Soul)"
        case 16:
            return "Balance of Pain (Squishy Soul)"
        case 17:
            return "Balance of Proficiency (Squishy Soul)"
        case 18:
            return "Glitterbug (Squishy Soul)"
        case _:
            return ("UnknownPrayer"+str(inputNumber))

def parseJSONPrayers(inputJSON):
    worshipPrayersList = json.loads(inputJSON["PrayOwned"])
    #print(type(worshipPrayersList), worshipPrayersList)
    worshipPrayersDict = {}
    index = 0
    for prayer in worshipPrayersList:
        try:
            worshipPrayersDict[getReadablePrayerNames(index)] = worshipPrayersList[index]
        except Exception as reason:
            print("Unable to add prayer: " , index, reason)
        index += 1
    return worshipPrayersDict

def setWorshipPrayersProgressionTier(inputJSON, progressionTiers):
    worshipPrayersDict = parseJSONPrayers(inputJSON)
    tier_WorshipPrayers = 0
    overall_WorshipPrayersTier = 0
    advice_WorshipPrayers = ""
    try:
        advice_IgnorrablePrayers = progressionTiers[-1][2]
    except:
        advice_IgnorrablePrayers = ""

    for tier in progressionTiers:
        #tier[0] = int Tier
        #tier[1] = dict requiredPrayersDict
        #tier[2] = str Notes
        if tier[0] != progressionTiers[-1][0]:
            if tier_WorshipPrayers == (tier[0]-1):
                allPrayersLeveled = True
                for requiredPrayer in tier[1]:
                    if worshipPrayersDict[requiredPrayer] < tier[1][requiredPrayer]:
                        allPrayersLeveled = False
                        advice_WorshipPrayers += requiredPrayer + " (" + str(worshipPrayersDict[requiredPrayer]) + "/" + str(tier[1][requiredPrayer]) + "), "
                if allPrayersLeveled == True:
                    tier_WorshipPrayers = tier[0]

    if advice_WorshipPrayers == "":
        advice_WorshipPrayers = " * Nada. You best <3"
    else:
        advice_WorshipPrayers = " * Tier " + str(tier_WorshipPrayers) + "- Level the following prayers: " + advice_WorshipPrayers[:-2] + ". " + progressionTiers[tier_WorshipPrayers+1][2] #strip off the trailing comma and space"

    for badPrayer in progressionTiers[-1][1]:
        advice_IgnorrablePrayers += badPrayer + ", "
    advice_IgnorrablePrayers = advice_IgnorrablePrayers[:-2]

    overall_WorshipPrayersTier = min(progressionTiers[-3][0], tier_WorshipPrayers)
    advice_WorshipPrayersCombined = ["### Best Worship-Prayers tier met: " + str(overall_WorshipPrayersTier) + "/" + str(progressionTiers[-3][-0]) + ". Recommended Worship-Prayers actions:",advice_WorshipPrayers,advice_IgnorrablePrayers]
    worshipPrayersPR = progressionResults.progressionResults(overall_WorshipPrayersTier,advice_WorshipPrayersCombined,"")
    return worshipPrayersPR
