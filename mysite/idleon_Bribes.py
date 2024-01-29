from models import AdviceSection
from models import AdviceGroup
from models import Advice
import progressionResults

def pl(_list: list, suffix_singular: str = "", suffix_plural: str = 's') -> str:
    """Pluralize"""
    return suffix_plural if len(_list) > 1 else suffix_singular

def parseBribes(inputJSON):
    parsedBribes = inputJSON["BribeStatus"]
    #print(parsedBribes)
    bribeSetW1 = {
        'Insider Trading': parsedBribes[0],
        'Tracking Chips': parsedBribes[1],
        'Mandatory Fire Sale': parsedBribes[2],
        'Sleeping On the Job': parsedBribes[3],
        'Artificial Demand': parsedBribes[4],
        'The Art of the Deal': parsedBribes[5]
        }
    bribeSetW2 = {
        'Overstock Regulations': parsedBribes[6],
        'Double EXP Scheme': parsedBribes[7],
        'Tagged Indicators': parsedBribes[8],
        'Fossil Fuel Legislation': parsedBribes[9],
        'Five Aces in the Deck': parsedBribes[10],
        'Fake Teleport Tickets': parsedBribes[11],
        'The Art of the Steal': parsedBribes[12]
        }
    bribeSetW3 = {
        'Counterfeit Telepassports': parsedBribes[13],
        'Weighted Marbles': parsedBribes[14],
        'Changing the Code': parsedBribes[15],
        'Taxidermied Cog Pouches': parsedBribes[16],
        'Guild VIP Fraud': parsedBribes[17],
        'Library Double Agent': parsedBribes[18],
        'The Art of the Fail': parsedBribes[19]
        }
    bribeSetW4 = {
        'Photoshopped Dmg Range': parsedBribes[20],
        'Glitched Acc Formula': parsedBribes[21],
        'Firewalled Defence': parsedBribes[22],
        'Bottomless Bags': parsedBribes[23],
        'AFKeylogging': parsedBribes[24],
        'Guild GP Hack': parsedBribes[25]
        }
    try:
        bribeSetTrashIsland = {
            'The Art of the Bail': parsedBribes[26],
            'Random Garbage': parsedBribes[27],
            'Godlier Creation': parsedBribes[28],
            'Fishermaster': parsedBribes[29],
            'Muscles on Muscles': parsedBribes[30],
            'Bottle Service': parsedBribes[31],
            'Star Scraper': parsedBribes[32],
            'The Art of the Grail': parsedBribes[33]
            }
    except Exception as reason:
        print("Bribes.parseBribes~ EXCEPTION Unable to retrieve Trash Island Bribes. Defaulting to unpurchased:", reason)
        bribeSetTrashIsland = {
            'The Art of the Bail': 0,
            'Random Garbage': 0,
            'Godlier Creation': 0,
            'Fishermaster': 0,
            'Muscles on Muscles': 0,
            'Bottle Service': 0,
            'Star Scraper': 0,
            'The Art of the Grail': 0
        }
    allBribesDict = {
        'W1': bribeSetW1,
        'W2': bribeSetW2,
        'W3': bribeSetW3,
        'W4': bribeSetW4,
        'Trash Island': bribeSetTrashIsland
        }
    #print(allBribesDict)
    return allBribesDict

def setBribesProgressionTier(inputJSON, progressionTiers):
    allBribesDict = parseBribes(inputJSON)
    tier_BribesPurchased = 0
    sum_allBribes = 0
    sum_bribeSetW1 = 0
    sum_bribeSetW2 = 0
    sum_bribeSetW3 = 0
    sum_bribeSetW4 = 0
    sum_bribeSetTrashIsland = 0
    max_allBribes = 33  # Max as of v1.91
    unpurchasableBribes = ["The Art of the Grail"]  # These bribes are in the game, but cannot be purchased as of v1.91
    max_tier = progressionTiers[-1][0]
    advice_BribesPurchased = []
    bribe_AdviceDict = {
        "W1Bribes": [],
        "W2Bribes": [],
        "W3Bribes": [],
        "W4Bribes": [],
        "TrashIslandBribes": []
    }
    bribe_AdviceGroupDict = {}
    bribe_AdviceSection = AdviceSection(
        name="Bribes",
        tier="Not Yet Evaluated",
        header="Best Bribe tier met: Not Yet Evaluated. Recommended Bribe actions",
        picture="Stat_Graph_Stamp.png"
    )

    # W1 Bribes
    for bribe in allBribesDict['W1']:
        if allBribesDict['W1'][bribe] > 0:
            sum_bribeSetW1 += allBribesDict['W1'][bribe]
            sum_allBribes += allBribesDict['W1'][bribe]
        elif allBribesDict['W1'][bribe] <= 0:
            bribe_AdviceDict["W1Bribes"].append(
                Advice(
                    label=bribe,
                    item_name=bribe,
                    progression="",
                    goal="",
                    unit=""
                )
            )
    bribe_AdviceGroupDict['W1'] = AdviceGroup(
        tier="0",
        pre_string=f"Purchase the remaining W1 Bribe{pl(bribe_AdviceDict['W1Bribes'])}",
        advices=bribe_AdviceDict['W1Bribes'],
        post_string="You should be able to afford them by the end of W1."
    )

    # W2 Bribes
    for bribe in allBribesDict['W2']:
        if allBribesDict['W2'][bribe] > 0:
            sum_bribeSetW2 += allBribesDict['W2'][bribe]
            sum_allBribes += allBribesDict['W2'][bribe]
        elif allBribesDict['W2'][bribe] <= 0:
            bribe_AdviceDict["W2Bribes"].append(
                Advice(
                    label=bribe,
                    item_name=bribe,
                    progression="",
                    goal="",
                    unit=""
                )
            )
    bribe_AdviceGroupDict['W2'] = AdviceGroup(
        tier="1",
        pre_string=f"Purchase the remaining W2 Bribe{pl(bribe_AdviceDict['W2Bribes'])}",
        advices=bribe_AdviceDict['W2Bribes'],
        post_string="You should be able to afford them by the end of W2."
    )

    # W3 Bribes
    for bribe in allBribesDict['W3']:
        if allBribesDict['W3'][bribe] > 0:
            sum_bribeSetW3 += allBribesDict['W3'][bribe]
            sum_allBribes += allBribesDict['W3'][bribe]
        elif allBribesDict['W3'][bribe] <= 0:
            bribe_AdviceDict["W3Bribes"].append(
                Advice(
                    label=bribe,
                    item_name=bribe,
                    progression="",
                    goal="",
                    unit=""
                )
            )
    bribe_AdviceGroupDict['W3'] = AdviceGroup(
        tier="2",
        pre_string=f"Purchase the remaining W3 Bribe{pl(bribe_AdviceDict['W3Bribes'])}",
        advices=bribe_AdviceDict['W3Bribes'],
        post_string="You should be able to afford them by the end of W3."
    )

    # W4 Bribes
    for bribe in allBribesDict['W4']:
        if allBribesDict['W4'][bribe] > 0:
            sum_bribeSetW4 += allBribesDict['W4'][bribe]
            sum_allBribes += allBribesDict['W4'][bribe]
        elif allBribesDict['W4'][bribe] <= 0:
            bribe_AdviceDict["W4Bribes"].append(
                Advice(
                    label=bribe,
                    item_name=bribe,
                    progression="",
                    goal="",
                    unit=""
                )
            )
    bribe_AdviceGroupDict['W4'] = AdviceGroup(
        tier="3",
        pre_string=f"Purchase the remaining W4 Bribe{pl(bribe_AdviceDict['W4Bribes'])}",
        advices=bribe_AdviceDict['W4Bribes'],
        post_string="You should be able to afford them by the end of W4."
    )

    # Trash Island
    for bribe in allBribesDict['Trash Island']:
        if allBribesDict['Trash Island'][bribe] > 0:
            sum_bribeSetTrashIsland += allBribesDict['Trash Island'][bribe]
            sum_allBribes += allBribesDict['Trash Island'][bribe]
        elif allBribesDict['Trash Island'][bribe] <= 0 and bribe not in unpurchasableBribes:
            bribe_AdviceDict["TrashIslandBribes"].append(
                Advice(
                    label=bribe,
                    item_name=bribe,
                    progression="",
                    goal="",
                    unit=""
                )
            )
    bribe_AdviceGroupDict['Trash Island'] = AdviceGroup(
        tier="4",
        pre_string=f"Purchase the remaining Trash Island Bribe{pl(bribe_AdviceDict['TrashIslandBribes'])}",
        advices=bribe_AdviceDict['TrashIslandBribes'],
        post_string="You should be able to afford them by the end of W5, after unlocking the Bribes from Trash Island."
    )
    #print("Bribe sums: ", sum_allBribes, sum_bribeSetW1, sum_bribeSetW2, sum_bribeSetW3, sum_bribeSetW4, sum_bribeSetTrashIsland)

    #Assess Overall Bribe Tier
    if sum_allBribes == max_allBribes:
        tier_BribesPurchased = max_tier
        advice_BribesPurchased = "Nada. You best <3"
    else:
        for tier in progressionTiers:
            if sum_bribeSetW1 < tier[1] or sum_bribeSetW2 < tier[2] or sum_bribeSetW3 < tier[3] or sum_bribeSetW4 < tier[4] or sum_bribeSetTrashIsland < tier[5]:
                advice_BribesPurchased = ("Finish purchasing Set " + str(tier_BribesPurchased + 1)
                                          + " of Bribes. You should be able to afford them "
                                          + progressionTiers[tier_BribesPurchased + 1][6])
            else:
                tier_BribesPurchased = tier[0]

    overall_BribesTier = min(max_tier, tier_BribesPurchased)
    tier_section = f"{overall_BribesTier}/{max_tier}"
    bribe_AdviceSection.tier = tier_section
    #Generate advice statement
    advice_BribesCombined = ["Best Bribe tier met: " + str(overall_BribesTier) + "/" + str(max_tier)
                             + ". Recommended Bribe actions:", advice_BribesPurchased]
    if overall_BribesTier == max_tier:
        bribe_AdviceSection.header = f"Best Bribe tier met: {tier_section}. You best <3"
    else:
        bribe_AdviceSection.header = f"Best Bribe tier met: {tier_section}. Recommended Bribe actions"
        bribe_AdviceSection.groups = [
            bribe_AdviceGroupDict.get('W1'),
            bribe_AdviceGroupDict.get('W2'),
            bribe_AdviceGroupDict.get('W3'),
            bribe_AdviceGroupDict.get('W4'),
            bribe_AdviceGroupDict.get('Trash Island')
        ]

    bribesPR = progressionResults.progressionResults(overall_BribesTier, advice_BribesCombined, "")
    return {"PR": bribesPR, "AdviceSection": bribe_AdviceSection}
