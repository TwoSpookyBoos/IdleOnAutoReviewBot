import json
import progressionResults
from models import AdviceSection, AdviceGroup, Advice
from utils import pl

def parseConsRefinery(inputJSON):
    refineryList = json.loads(inputJSON["Refinery"])
    meritList = json.loads(inputJSON["TaskZZ2"])
    consRefineryDict = {
        #Combustion = Tab1
        'Red Rank': refineryList[3][1],
        'Red AutoRefine': refineryList[3][4],
        'Orange Rank': refineryList[4][1],
        'Orange AutoRefine': refineryList[4][4],
        'Blue Rank': refineryList[5][1],
        'Blue AutoRefine': refineryList[5][4],

        #Synthesis = Tab2
        'Green Rank': refineryList[6][1],
        'Green AutoRefine': refineryList[6][4],
        'Purple Rank': refineryList[7][1],
        'Purple AutoRefine': refineryList[7][4],
        'Nullo Rank': refineryList[8][1],
        'Nullo AutoRefine': refineryList[8][4],

        # = Tab3
        'Tab3-1 Rank': refineryList[9][1],
        'Tab3-1 AutoRefine': refineryList[9][4],
        'Tab3-2 Rank': refineryList[10][1],
        'Tab3-2 AutoRefine': refineryList[10][4],
        'Tab3-3 Rank': refineryList[11][1],
        'Tab3-3 AutoRefine': refineryList[11][4],

        # = Tab4
        'Tab4-1 Rank': refineryList[12][1],
        'Tab4-1 AutoRefine': refineryList[12][4],
        'Tab4-2 Rank': refineryList[13][1],
        'Tab4-2 AutoRefine': refineryList[13][4],
        'Tab4-3 Rank': refineryList[14][1],
        'Tab4-3 AutoRefine': refineryList[14][4],

        # = Tab5
        'Tab5-1 Rank': refineryList[15][1],
        'Tab5-1 AutoRefine': refineryList[15][4],
        'Tab5-2 Rank': refineryList[16][1],
        'Tab5-2 AutoRefine': refineryList[16][4],
        'Tab5-3 Rank': refineryList[17][1],
        'Tab5-3 AutoRefine': refineryList[17][4],

        # = Tab6
        'Tab6-1 Rank': refineryList[18][1],
        'Tab6-1 AutoRefine': refineryList[18][4],
        'Tab6-2 Rank': refineryList[19][1],
        'Tab6-2 AutoRefine': refineryList[19][4],
        'Tab6-3 Rank': refineryList[20][1],
        'Tab6-3 AutoRefine': refineryList[20][4],

        # = Tab7
        'Tab7-1 Rank': refineryList[21][1],
        'Tab7-1 AutoRefine': refineryList[21][4],
        'Tab7-2 Rank': refineryList[22][1],
        'Tab7-2 AutoRefine': refineryList[22][4],
        'Tab7-3 Rank': refineryList[23][1],
        'Tab7-3 AutoRefine': refineryList[23][4],

        #W3 Merit
        'Salt Merit': meritList[2][6]
    }
    consRefineryDict['Combustion AutoRefine'] = consRefineryDict['Red AutoRefine'] + consRefineryDict['Orange AutoRefine'] + consRefineryDict['Blue AutoRefine']
    consRefineryDict['Synthesis AutoRefine'] = consRefineryDict['Green AutoRefine'] + consRefineryDict['Purple AutoRefine'] + consRefineryDict['Nullo AutoRefine']
    #consRefineryDict['Tab3 AutoRefine'] = consRefineryDict['Tab3-1 AutoRefine'] + consRefineryDict['Tab3-2 AutoRefine'] + consRefineryDict['Tab3-3 AutoRefine']
    #consRefineryDict['Tab4 AutoRefine'] = consRefineryDict['Tab4-1 AutoRefine'] + consRefineryDict['Tab4-2 AutoRefine'] + consRefineryDict['Tab4-3 AutoRefine']
    #consRefineryDict['Tab5 AutoRefine'] = consRefineryDict['Tab5-1 AutoRefine'] + consRefineryDict['Tab5-2 AutoRefine'] + consRefineryDict['Tab5-3 AutoRefine']
    #consRefineryDict['Tab6 AutoRefine'] = consRefineryDict['Tab6-1 AutoRefine'] + consRefineryDict['Tab6-2 AutoRefine'] + consRefineryDict['Tab6-3 AutoRefine']
    #consRefineryDict['Tab7 AutoRefine'] = consRefineryDict['Tab7-1 AutoRefine'] + consRefineryDict['Tab7-2 AutoRefine'] + consRefineryDict['Tab7-3 AutoRefine']
    consRefineryDict['Sum AutoRefine'] = consRefineryDict['Combustion AutoRefine'] + consRefineryDict['Synthesis AutoRefine']  #+ consRefineryDict['Tab3 AutoRefine']
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
    advice_AutoRefine = ""
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
        if tier_Tab1 == (tier[0]-1):  #Only check if they already met previous tier
            required_Tab1 = tier[1]
            all_Tab1 = True
            for key, value in required_Tab1.items():
                if consRefineryDict[key] < required_Tab1[key]:
                    all_Tab1 = False
                    advice_Tab1 = ""  #TODO
            if all_Tab1 == True:
                tier_Tab1 = tier[0]

        #Tab2 checks
        if tier_Tab2 == (tier[0]-1):  #Only check if they already met previous tier
            required_Tab2 = tier[2]
            all_Tab2 = True
            for key, value in required_Tab2.items():
                if consRefineryDict[key] < required_Tab2[key]:
                    all_Tab2 = False
            if all_Tab2 == True:
                tier_Tab2 = tier[0]

        #Tab3 checks
        if tier_Tab3 == (tier[0]-1):  #Only check if they already met previous tier
            required_Tab3 = tier[3]
            all_Tab3 = True
            for key, value in required_Tab3.items():
                if consRefineryDict[key] < required_Tab3[key]:
                    all_Tab3 = False
                    advice_Tab3 = ""  #TODO
            if all_Tab3 == True:
                tier_Tab3 = tier[0]
        #Tab4 checks
        #Tab5 checks
        #Tab6 checks
        #Tab7 checks

        #AutoRefine checks
        if tier_AutoRefine == (tier[0]-1):  #Only check if they already met previous tier
            required_AutoRefine = tier[4]
            all_AutoRefine = True
            for key, value in required_AutoRefine.items():
                if consRefineryDict[key] != required_AutoRefine[key]:  #This is the only comparison we want to make sure is exactly equal
                    all_AutoRefine = False
                    if consRefineryDict['Red AutoRefine'] > 0 or consRefineryDict['Green AutoRefine'] > 0:
                        advice_AutoRefine = "Tier 0- The first salt per tab should always be ranking up (aka auto-refine at 0%)! Setting max tier to 0 until this is fixed :("
                else:
                    all_AutoRefine = True  #for clarity lol. Being equal is the desired outcome. This value should already be true from before. Being unequal is the bad outcome that would result in it turning False.
            if all_AutoRefine == True:
                tier_AutoRefine = tier[0]

        #W3 Merits check
        if tier_W3Merits == (tier[0]-1):
            required_W3Merits = tier[5]
            if consRefineryDict['Salt Merit'] >= required_W3Merits:
                tier_W3Merits = tier[0]

    #Generate all the advice
    overall_ConsRefineryTier = min(progressionTiers[-1][0], tier_AutoRefine, tier_W3Merits, tier_Tab1, tier_Tab2, tier_Tab3)
        #tier_Tab4, tier_Tab5, tier_Tab6, tier_Tab7) #future updates may add more tabs!

    #W3Merits Advice
    sum_SaltsRank2Plus = 0
    if consRefineryDict['Orange Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Blue Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Green Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Purple Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Nullo Rank'] >= 2:
        sum_SaltsRank2Plus += 1
    if consRefineryDict['Salt Merit'] < sum_SaltsRank2Plus:
        advice_W3Merits = "Tier " + str(tier_W3Merits) + "- Invest more points into the W3 Salt Merit to reduce your salt consumption! Currently " + str(consRefineryDict['Salt Merit']) + "/" + str(sum_SaltsRank2Plus)

    #Tab1 Advice
    if consRefineryDict['Combustion AutoRefine'] > 0:
        if tier_Tab1 < 16:
            #Red Salt
            advice_Tab1 = ("Tier " + str(tier_Tab1) + "- Next Tab1 Balanced tier needs "
            + "Red: " + str(consRefineryDict['Red Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Red Rank']))
            #Orange Salt
            if (consRefineryDict['Orange Rank'] > progressionTiers[tier_Tab1+1][1]['Orange Rank']) and progressionTiers[tier_Tab1+1][1]['Orange Rank'] != 0:
                advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank']) + " (Overleveled!)"
            else:
                advice_Tab1 += ", Orange: " + str(consRefineryDict['Orange Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Orange Rank'])
            #Blue Salt
            if (consRefineryDict['Blue Rank'] > progressionTiers[tier_Tab1+1][1]['Blue Rank']) and progressionTiers[tier_Tab1+1][1]['Blue Rank'] != 0:
                advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank']) + " (Overleveled!)"
            else:
                advice_Tab1 += ", Blue: " + str(consRefineryDict['Blue Rank']) + "/" + str(progressionTiers[tier_Tab1+1][1]['Blue Rank'])
            #Tab1 trailing auto-refine
            if tier_Tab1 >= 8:
                if consRefineryDict['Red Rank'] < 22:
                    advice_Tab1 += ". After your Red Salt reaches rank 22, consider setting all of Tab1 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab1 to Tier 17+. This style isn't for everyone though!)"
                else:
                    advice_Tab1 += ". Now that your Red Salt is rank 22+, consider setting all of Tab1 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab1 to Tier 17+. This style isn't for everyone though!)"
        elif tier_Tab1 >= 17:
            advice_Tab1 = "Tier " + str(tier_Tab1) + "- " + progressionTiers[17][6]
    elif consRefineryDict['Combustion AutoRefine'] == 0:
        if consRefineryDict['Red Rank'] >= 22:
            tier_Tab1 = progressionTiers[-1][0]  #19 currently
            advice_Tab1 += "Tier " + str(tier_Tab1) + "- Red is already rank 22+ where ranks become faster instead of slower, and all Tab1 salts are set to 0% AutoRefine. Tab1 should be relatively smooth sailing ❤️"

        else:
            tier_Tab1 = progressionTiers[-3][0]  #17 currently
            advice_Tab1 += "Tier " + str(tier_Tab1) + "- Tab1 still has scaling time because Red Salt's rank is under 22, and all Tab1 salts are set to 0% AutoRefine :( Pay attention to Tab1 salt requirements for upcoming crafting and building in advance to avoid long delays."

    #Tab2 Advice
    if consRefineryDict['Synthesis AutoRefine'] > 0:
        if tier_Tab2 < 16:
            advice_Tab2 = ("Tier " + str(tier_Tab2) + "- Next Tab2 Balanced tier needs "
            + "Green: " + str(consRefineryDict['Green Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Green Rank']))
            if (consRefineryDict['Purple Rank'] > progressionTiers[tier_Tab2+1][2]['Purple Rank']) and progressionTiers[tier_Tab2+1][2]['Purple Rank'] != 0:
                advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank']) + " (Overleveled!)"
            else:
                advice_Tab2 += ", Purple: " + str(consRefineryDict['Purple Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Purple Rank'])
            if (consRefineryDict['Nullo Rank'] > progressionTiers[tier_Tab2+1][2]['Nullo Rank']) and progressionTiers[tier_Tab2+1][2]['Nullo Rank'] != 0:
                advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank']) + " (Overleveled!)"
            else:
                advice_Tab2 += ", Nullo: " + str(consRefineryDict['Nullo Rank']) + "/" + str(progressionTiers[tier_Tab2+1][2]['Nullo Rank'])
            if tier_Tab2 >= 9:
                if consRefineryDict['Green Rank'] < 22:
                    advice_Tab2 += ". After your Green Salt reaches rank 22, consider setting all of Tab2 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab2 to Tier 18+. This style isn't for everyone though!)"
                else:
                    advice_Tab2 += ". Now that your Green Salt is rank 22+, consider setting all of Tab2 to 0% auto-refine and infinitely ranking up! (I recommend this and will bump your Tab2 to Tier 18+. This style isn't for everyone though!)"
        elif tier_Tab2 >= 17:
            advice_Tab2 = "Tier " + str(tier_Tab2) + "- " + progressionTiers[18][6]
    elif consRefineryDict['Synthesis AutoRefine'] == 0:
        if consRefineryDict['Green Rank'] >= 22:
            tier_Tab2 = progressionTiers[-1][0]  #19 currently
            advice_Tab2 += "Tier " + str(tier_Tab2) + "- Green is already rank 22+ where ranks become faster instead of slower, and all Tab2 salts are set to 0% AutoRefine. Tab2 should be relatively smooth sailing ❤️"

        else:
            tier_Tab2 = progressionTiers[-2][0]  #18 currently
            advice_Tab2 += "Tier " + str(tier_Tab2) + "- Tab2 still has scaling time because Green Salt's rank is under 22, and all Tab2 salts are set to 0% AutoRefine :( Pay attention to Tab2 salt requirements for upcoming crafting and building in advance to avoid long delays."

    #AutoRefine advice
    if tier_AutoRefine == progressionTiers[-1][0] and consRefineryDict['Red Rank'] >= 2:
        overall_ConsRefineryTier = tier_AutoRefine  #Rank 19 is full yolo, but only if they already have Red Salts to level 2 or higher to prevent this triggering on pre-w3 accounts
        advice_AutoRefine = "Tier " + str(tier_AutoRefine) + "- You've got all Salts set to 0% auto-refine, the infinite-scaling portion of Refinery."
        #Another comment for clarity. I only want AutoRefine advice to show up in the extreme cases of Tier0 or Max tier. Anything inbetween doesn't need advice.
        if tier_Tab1 == progressionTiers[-1][0] and tier_Tab2 == progressionTiers[-1][0]:
            advice_AutoRefine += " You best ❤️"

    #Tab3 Advice
    #Tab4 Advice
    #Tab5 Advice
    #Tab6 Advice
    #Tab7 Advice
    #Generate advice statement
    advice_ConsRefineryCombined = ["Best Refinery tier met: " + str(overall_ConsRefineryTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended refinery actions:", advice_AutoRefine, advice_W3Merits, advice_Tab1, advice_Tab2]
    #TODO
    #print("Tiers: Overall",overall_ConsRefineryTier, ", AutoRefine", tier_AutoRefine, ", Merits", tier_W3Merits, ", Tab1", tier_Tab1, ", Tab2", tier_Tab2, ", Tab3", tier_Tab3)
    #print("Determined lowest refinery tier met to be: " + str(overall_ConsRefineryTier) + "/19")
    #print(advice_ConsRefineryCombined)
    consRefineryPR = progressionResults.progressionResults(overall_ConsRefineryTier,advice_ConsRefineryCombined,"")
    return consRefineryPR
