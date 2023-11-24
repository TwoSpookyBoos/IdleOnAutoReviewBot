import json
import progressionResults

def getReadablePrayerNames(inputNumber):
    match inputNumber:
        case 0:
            return "Big Brain Time"
        case 1:
            return "Skilled Dimwit"
        case 2:
            return "Unending Energy"
        case 3:
            return "Shiny Snitch"
        case 4:
            return "Zerg Rushogen"
        case 5:
            return "Tachion of the Titans"
        case 6:
            return "Balance of Precision"
        case 7:
            return "Midas Minded"
        case 8:
            return "Jawbreaker"
        case 9:
            return "The Royal Sampler"
        case 10:
            return "Antifun Spirit"
        case 11:
            return "Circular Criticals"
        case 12:
            return "Ruck Sack"
        case 13:
            return "Fibers of Absence"
        case 14:
            return "Vacuous Tissue"
        case 15:
            return "Beefy For Real"
        case 16:
            return "Balance of Pain"
        case 17:
            return "Balance of Proficiency"
        case 18:
            return "Glitterbug"
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
        advice_WorshipPrayers = "*Nada. You best <3"
    else:
        advice_WorshipPrayers = "*Level the following prayers: " + advice_WorshipPrayers[:-2] + ". " + progressionTiers[tier_WorshipPrayers+1][2] #strip off the trailing comma and space"

    for badPrayer in progressionTiers[-1][1]:
        advice_IgnorrablePrayers += badPrayer + ", "
    advice_IgnorrablePrayers = advice_IgnorrablePrayers[:-2]

    overall_WorshipPrayersTier = min(progressionTiers[-3][0], tier_WorshipPrayers)
    advice_WorshipPrayersCombined = ["Best Worship-Prayers tier met: " + str(overall_WorshipPrayersTier) + "/" + str(progressionTiers[-3][-0]) + ". Recommended Worship-Prayers actions:",advice_WorshipPrayers,advice_IgnorrablePrayers]
    worshipPrayersPR = progressionResults.progressionResults(overall_WorshipPrayersTier,advice_WorshipPrayersCombined,"")
    return worshipPrayersPR
