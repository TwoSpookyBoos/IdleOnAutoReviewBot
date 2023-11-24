import json
import progressionResults

def parseConsRefinery(inputJSON):
    refineryList = json.loads(inputJSON["Refinery"])
    meritList = json.loads(inputJSON["TaskZZ2"])
    consRefineryDict = {
        #Combustion = Tab1
        'Red Rank': refineryList[3][1],
        'Red AutoRefine' : refineryList[3][4],
        'Orange Rank' : refineryList[4][1],
        'Orange AutoRefine' : refineryList[4][4],
        'Blue Rank' : refineryList[5][1],
        'Blue AutoRefine' : refineryList[5][4],

        #Synthesis = Tab2
        'Green Rank' : refineryList[6][1],
        'Green AutoRefine' : refineryList[6][4],
        'Purple Rank' : refineryList[7][1],
        'Purple AutoRefine' : refineryList[7][4],
        'Nullo Rank' : refineryList[8][1],
        'Nullo AutoRefine' : refineryList[8][4],

        # = Tab3
        'Tab3-1 Rank' : refineryList[9][1],
        'Tab3-1 AutoRefine' : refineryList[9][4],
        'Tab3-2 Rank' : refineryList[10][1],
        'Tab3-2 AutoRefine' : refineryList[10][4],
        'Tab3-3 Rank' : refineryList[11][1],
        'Tab3-3 AutoRefine' : refineryList[11][4],

        # = Tab4
        'Tab4-1 Rank' : refineryList[12][1],
        'Tab4-1 AutoRefine' : refineryList[12][4],
        'Tab4-2 Rank' : refineryList[13][1],
        'Tab4-2 AutoRefine' : refineryList[13][4],
        'Tab4-3 Rank' : refineryList[14][1],
        'Tab4-3 AutoRefine' : refineryList[14][4],

        # = Tab5
        'Tab5-1 Rank' : refineryList[15][1],
        'Tab5-1 AutoRefine' : refineryList[15][4],
        'Tab5-2 Rank' : refineryList[16][1],
        'Tab5-2 AutoRefine' : refineryList[16][4],
        'Tab5-3 Rank' : refineryList[17][1],
        'Tab5-3 AutoRefine' : refineryList[17][4],

        # = Tab6
        'Tab6-1 Rank' : refineryList[18][1],
        'Tab6-1 AutoRefine' : refineryList[18][4],
        'Tab6-2 Rank' : refineryList[19][1],
        'Tab6-2 AutoRefine' : refineryList[19][4],
        'Tab6-3 Rank' : refineryList[20][1],
        'Tab6-3 AutoRefine' : refineryList[20][4],

        # = Tab7
        'Tab7-1 Rank' : refineryList[21][1],
        'Tab7-1 AutoRefine' : refineryList[21][4],
        'Tab7-2 Rank' : refineryList[22][1],
        'Tab7-2 AutoRefine' : refineryList[22][4],
        'Tab7-3 Rank' : refineryList[23][1],
        'Tab7-3 AutoRefine' : refineryList[23][4],

        #W3 Merit
        'Salt Merit' : meritList[2][6]
    }
    consRefineryDict['Combustion AutoRefine'] = consRefineryDict['Red AutoRefine'] + consRefineryDict['Orange AutoRefine'] + consRefineryDict['Blue AutoRefine']
    consRefineryDict['Synthesis AutoRefine'] = consRefineryDict['Green AutoRefine'] + consRefineryDict['Purple AutoRefine'] + consRefineryDict['Nullo AutoRefine']
    #consRefineryDict['Tab3 AutoRefine'] = consRefineryDict['Tab3-1 AutoRefine'] + consRefineryDict['Tab3-2 AutoRefine'] + consRefineryDict['Tab3-3 AutoRefine']
    #consRefineryDict['Tab4 AutoRefine'] = consRefineryDict['Tab4-1 AutoRefine'] + consRefineryDict['Tab4-2 AutoRefine'] + consRefineryDict['Tab4-3 AutoRefine']
    #consRefineryDict['Tab5 AutoRefine'] = consRefineryDict['Tab5-1 AutoRefine'] + consRefineryDict['Tab5-2 AutoRefine'] + consRefineryDict['Tab5-3 AutoRefine']
    #consRefineryDict['Tab6 AutoRefine'] = consRefineryDict['Tab6-1 AutoRefine'] + consRefineryDict['Tab6-2 AutoRefine'] + consRefineryDict['Tab6-3 AutoRefine']
    #consRefineryDict['Tab7 AutoRefine'] = consRefineryDict['Tab7-1 AutoRefine'] + consRefineryDict['Tab7-2 AutoRefine'] + consRefineryDict['Tab7-3 AutoRefine']
    consRefineryDict['Sum AutoRefine'] = consRefineryDict['Combustion AutoRefine'] + consRefineryDict['Synthesis AutoRefine'] #+ consRefineryDict['Tab3 AutoRefine']
    #print(consRefineryDict)
    return consRefineryDict

def setConsRefineryProgressionTier(inputJSON, progressionTiers):
    tier_Tab1 = 0
    tier_Tab2 = 0
    tier_Tab3 = 0
    #tier_Tab4 = 0
    #tier_Tab5 = 0
    #tier_Tab6 = 0
    #tier_Tab7 = 0
    tier_AutoRefine = 0
    tier_W3Merits = 0
    advice_Tab1 = ""
    advice_Tab2 = ""
    advice_Tab3 = ""
    advice_Tab4 = ""
    advice_Tab5 = ""
    advice_Tab6 = ""
    advice_Tab7 = ""
    advice_AutoRefine= ""
    advice_W3Merits = ""
    advice_ConsRefineryCombined = ""
    consRefineryDict = parseConsRefinery(inputJSON)
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = dict Tab1 Ranks
        #tier[2] = dict Tab2 Ranks
        #tier[3] = dict Tab3 Ranks
        #tier[4] = dict All-tab AutoRefine
        #tier[5] = int W3Merits purchased
        #tier[6] = str Notes
        #Tab1 checks
        if tier_Tab1 == (tier[0]-1): #Only check if they already met previous tier
            required_Tab1 = tier[1]
            all_Tab1 = True
            for key, value in required_Tab1.items():
                if consRefineryDict[key] < required_Tab1[key]:
                    all_Tab1 = False
                    advice_Tab1 = "" #TODO
            if all_Tab1 == True:
                tier_Tab1 = tier[0]
        #Tab2 checks
        if tier_Tab2 == (tier[0]-1): #Only check if they already met previous tier
            required_Tab2 = tier[2]
            all_Tab2 = True
            for key, value in required_Tab2.items():
                if consRefineryDict[key] < required_Tab2[key]:
                    all_Tab2 = False
            if all_Tab2 == True:
                tier_Tab2 = tier[0]
        #Tab3 checks
        if tier_Tab3 == (tier[0]-1): #Only check if they already met previous tier
            required_Tab3 = tier[3]
            all_Tab3 = True
            for key, value in required_Tab3.items():
                if consRefineryDict[key] < required_Tab3[key]:
                    all_Tab3 = False
                    advice_Tab3 = "" #TODO
            if all_Tab3 == True:
                tier_Tab3 = tier[0]
        #Tab4 checks
        #Tab5 checks
        #Tab6 checks
        #Tab7 checks
        #AutoRefine checks
        if tier_AutoRefine == (tier[0]-1): #Only check if they already met previous tier
            required_AutoRefine = tier[4]
            all_AutoRefine = True
            for key, value in required_AutoRefine.items():
                if consRefineryDict[key] != required_AutoRefine[key]: #This is the only comparison we want to make sure is exactly equal
                    all_AutoRefine = False
                    if consRefineryDict['Red AutoRefine'] > 0 or consRefineryDict['Green AutoRefine'] > 0:
                        advice_AutoRefine = "*The first salt per tab should always be ranking up (aka auto-refine at 0%)! Setting max tier to 0 until this is fixed :("
            if all_AutoRefine == True:
                tier_AutoRefine = tier[0]
        #W3 Merits check
        if tier_W3Merits == (tier[0]-1):
            required_W3Merits = tier[5]
            if consRefineryDict['Salt Merit'] >= required_W3Merits:
                    tier_W3Merits = tier[0]

    #Generate all the advice
    overall_ConsRefineryTier = min(tier_AutoRefine, tier_W3Merits, tier_Tab1, tier_Tab2, tier_Tab3)
        #tier_Tab4, tier_Tab5, tier_Tab6, tier_Tab7) #future updates may add more tabs!
    #AutoRefine advice
    if (tier_AutoRefine >= progressionTiers[-3][0] and tier_Tab1 >= progressionTiers[-3][0]) or (tier_AutoRefine >= progressionTiers[-2][0] and tier_Tab2 >= progressionTiers[-2][0]):
        overall_ConsRefineryTier = tier_AutoRefine #Ranks 17 and 18 are hybrid
        advice_AutoRefine = "*" + progressionTiers[tier_AutoRefine][6]
    elif tier_AutoRefine == progressionTiers[-1][0] and tier_Tab1 >= 1:
        overall_ConsRefineryTier = tier_AutoRefine #Rank 19 is full yolo, but only if they already have Red Salts to level 2 or higher to prevent this triggering on pre-w3 accounts
        advice_AutoRefine = "*" + progressionTiers[tier_AutoRefine][6]
    elif (tier_AutoRefine >= progressionTiers[-3][0] and tier_Tab1 < progressionTiers[-3][0]):
        advice_AutoRefine = "*" + "Review your AutoRefine settings if you are trying to follow the balanced approach. (If you are in the process of intentionally leveling up Orange, Blue, Purple, or Nullo Salts, you can probably ignore this warning.)"
    #W3Merits Advice
    sum_SaltsRank2Plus = 0
    if (consRefineryDict['Orange Rank'] >=2):
        sum_SaltsRank2Plus += 1
    if (consRefineryDict['Blue Rank'] >=2):
        sum_SaltsRank2Plus += 1
    if (consRefineryDict['Green Rank'] >=2):
        sum_SaltsRank2Plus += 1
    if (consRefineryDict['Purple Rank'] >=2):
        sum_SaltsRank2Plus += 1
    if (consRefineryDict['Nullo Rank'] >=2):
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Salt Merit'] < sum_SaltsRank2Plus:
        advice_W3Merits = "Invest more points into the W3 Salt Merit to reduce your salt consumption! Currently " + str(consRefineryDict['Salt Merit']) + "/" + str(sum_SaltsRank2Plus)
    #Tab1 Advice
    if tier_Tab1 < 16 and tier_AutoRefine < 19:
        advice_Tab1 = ("*Next Tab1 Balanced tier needs "
        + "Red: " + str(consRefineryDict['Red Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Red Rank']))
        if (consRefineryDict['Orange Rank'] > progressionTiers[tier_Tab1+1][1]['Orange Rank']) and progressionTiers[tier_Tab1+1][1]['Orange Rank'] != 0:
            advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank']) + " (Overleveled!)"
        else:
            advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank'])
        if (consRefineryDict['Blue Rank'] > progressionTiers[tier_Tab1+1][1]['Blue Rank']) and progressionTiers[tier_Tab1+1][1]['Blue Rank'] != 0:
            advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank']) + " (Overleveled!)"
        else:
            advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank'])
    #Tab2 Advice
    if tier_Tab2 < 16 and tier_AutoRefine < 19 :
        advice_Tab2 = ("*Next Tab2 Balanced tier needs "
        + "Green: " + str(consRefineryDict['Green Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Green Rank']))
        if (consRefineryDict['Purple Rank'] > progressionTiers[tier_Tab2+1][2]['Purple Rank']) and progressionTiers[tier_Tab2+1][2]['Purple Rank'] != 0:
            advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank']) + " (Overleveled!)"
        else:
            advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank'])
        if (consRefineryDict['Nullo Rank'] > progressionTiers[tier_Tab2+1][2]['Nullo Rank']) and progressionTiers[tier_Tab2+1][2]['Nullo Rank'] != 0:
            advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank']) + " (Overleveled!)"
        else:
            advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank'])
    #Tab3 Advice
    #Tab4 Advice
    #Tab5 Advice
    #Tab6 Advice
    #Tab7 Advice
    #Generate advice statement
    advice_ConsRefineryCombined = ["Best Refinery tier met: " + str(overall_ConsRefineryTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended refinery actions:", advice_AutoRefine, advice_W3Merits, advice_Tab1, advice_Tab2]
#TODO
    #print("Test print:", progressionTiers[tier_Tab1+1][1]['Red Rank'])
    #print("Ranks for AutoRefine, Merits, Tab1, Tab2, Tab3: ", tier_AutoRefine, tier_W3Merits, tier_Tab1, tier_Tab2, tier_Tab3)
    #print("Determined lowest refinery tier met to be: " + str(overall_ConsRefineryTier) + "/19")
    #print(advice_ConsRefineryCombined)
    consRefineryPR = progressionResults.progressionResults(overall_ConsRefineryTier,advice_ConsRefineryCombined,"")
    return consRefineryPR