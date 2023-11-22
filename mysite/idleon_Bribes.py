import json
import progressionResults

def parseBribes(inputJSON):
    parsedBribes = inputJSON["BribeStatus"]
    #print(parsedBribes)
    bribeSetW1 = {
        'Insider Trading': parsedBribes[0],
        'Tracking Chips':parsedBribes[1],
        'Mandatory Fire Sale':parsedBribes[2],
        'Sleeping On the Job':parsedBribes[3],
        'Artificial Demand':parsedBribes[4],
        'The Art of the Deal':parsedBribes[5]
        }
    bribeSetW2 = {
        'Overstock Regulations':parsedBribes[6],
        'Double EXP Scheme':parsedBribes[7],
        'Tagged Indicators':parsedBribes[8],
        'Fossil Fuel Legislation':parsedBribes[9],
        'Fice Aces in the Deck':parsedBribes[10],
        'Fake Teleport Tickets':parsedBribes[11],
        'The Art of the Steal':parsedBribes[12]
        }
    bribeSetW3 = {
        'Counterfeit Telepassports':parsedBribes[13],
        'Weighted Marbles':parsedBribes[14],
        'Changing the Code':parsedBribes[15],
        'Taxidermied Cog Pouches':parsedBribes[16],
        'Guild VIP Fraud':parsedBribes[17],
        'Library Double Agent':parsedBribes[18],
        'The Art of the Fail':parsedBribes[19]
        }
    bribeSetW4 = {
        'Photoshopped Dmg Range':parsedBribes[20],
        'Glitched Acc Formula':parsedBribes[21],
        'Firewalled Defence':parsedBribes[22],
        'Bottomless Bags':parsedBribes[23],
        'AFKeylogging':parsedBribes[24],
        'Guild GP Hack':parsedBribes[25]
        }
    try:
        bribeSetTrashIsland = {
            'The Art of the Bail':parsedBribes[26],
            'Random Garbage':parsedBribes[27],
            'Godlier Creation':parsedBribes[28],
            'Fishermaster':parsedBribes[29],
            'Muscles on Muscles':parsedBribes[30],
            'Bottle Service':parsedBribes[31],
            'Star Scraper':parsedBribes[32],
            'The Art of the Grail':parsedBribes[33]
            }
    except:
        bribeSetTrashIsland = {}
    allBribesDict = {
        'W1':bribeSetW1,
        'W2':bribeSetW2,
        'W3':bribeSetW3,
        'W4':bribeSetW4,
        'Trash Island':bribeSetTrashIsland
        }
    #print(allBribesDict)
    return allBribesDict

def setBribesProgressionTier(inputJSON, progressionTiers):
    allBribesDict = parseBribes(inputJSON)
    tier_BribesPurchased = 0
    overall_BribesTier = 0
    advice_BribesPurchased = ""
    advice_BribesCombined = ""
    sum_allBribes = 0
    sum_bribeSetW1 = 0
    sum_bribeSetW2 = 0
    sum_bribeSetW3 = 0
    sum_bribeSetW4 = 0
    sum_bribeSetTrashIsland = 0
    for bribe in allBribesDict['W1']:
        if allBribesDict['W1'][bribe] != 0:
            sum_bribeSetW1 += allBribesDict['W1'][bribe]
            sum_allBribes += allBribesDict['W1'][bribe]
    for bribe in allBribesDict['W2']:
        if allBribesDict['W2'][bribe] != 0:
            sum_bribeSetW2 += allBribesDict['W2'][bribe]
            sum_allBribes += allBribesDict['W2'][bribe]
    for bribe in allBribesDict['W3']:
        if allBribesDict['W3'][bribe] != 0:
            sum_bribeSetW3 += allBribesDict['W3'][bribe]
            sum_allBribes += allBribesDict['W3'][bribe]
    for bribe in allBribesDict['W4']:
        if allBribesDict['W4'][bribe] != 0:
            sum_bribeSetW4 += allBribesDict['W4'][bribe]
            sum_allBribes += allBribesDict['W4'][bribe]
    for bribe in allBribesDict['Trash Island']:
        if allBribesDict['Trash Island'][bribe] != 0:
            sum_bribeSetTrashIsland += allBribesDict['Trash Island'][bribe]
            sum_allBribes += allBribesDict['Trash Island'][bribe]
    #print("Bribe sums: ", sum_allBribes, sum_bribeSetW1, sum_bribeSetW2, sum_bribeSetW3, sum_bribeSetW4, sum_bribeSetTrashIsland)
    #Assess Bribe Tier
    if sum_allBribes == 33: #Max as of v1.91
        tier_BribesPurchased = 5
        advice_BribesPurchased = "*Nada. You best <3"
    else:
        for tier in progressionTiers:
            if sum_bribeSetW1 < tier[1] or sum_bribeSetW2 < tier[2] or sum_bribeSetW3 < tier[3] or sum_bribeSetW4 < tier[4] or sum_bribeSetTrashIsland < tier[5]:
                advice_BribesPurchased = "*Finish purchasing Set " + str(tier_BribesPurchased+1) + " of Bribes. You should be able to afford them " + progressionTiers[tier_BribesPurchased+1][6]
            else:
                tier_BribesPurchased = tier[0]
    overall_BribesTier = min(5, tier_BribesPurchased)
    #Generate advice statement
    advice_BribesCombined = ["Best Bribe tier met: " + str(overall_BribesTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Bribe actions:", advice_BribesPurchased]
    bribesPR = progressionResults.progressionResults(overall_BribesTier, advice_BribesCombined, "")
    return bribesPR