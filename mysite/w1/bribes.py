from models.models import Advice, AdviceGroup, AdviceSection
from utils.text_formatting import pl
from utils.logging import get_logger
from consts import bribes_progressionTiers, unpurchasableBribes, break_you_best, bribesDict
from flask import g as session_data

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup():
    bribe_AdviceDict = {
        "W1Bribes": [],
        "W2Bribes": [],
        "W3Bribes": [],
        "W4Bribes": [],
        "TrashIslandBribes": [],
        "W6Bribes": [],
    }
    info_tiers = 0
    max_tier = bribes_progressionTiers[-1][0] - info_tiers
    tier_BribesPurchased = 0
    sum_allBribes = 0
    sum_bribeSetW1 = 0
    sum_bribeSetW2 = 0
    sum_bribeSetW3 = 0
    sum_bribeSetW4 = 0
    sum_bribeSetTrashIsland = 0
    sum_bribeSetW6 = 0
    max_allBribes = sum([len(v) for v in bribesDict.values()]) - len(unpurchasableBribes)  # 40 as of v2.12

    #Assess Tiers
    allBribesDict = session_data.account.bribes
    bribe_AdviceGroupDict = {}
    # W1 Bribes
    for bribe in allBribesDict['W1']:
        if allBribesDict['W1'][bribe] > 0:
            sum_bribeSetW1 += allBribesDict['W1'][bribe]
            sum_allBribes += allBribesDict['W1'][bribe]
        elif allBribesDict['W1'][bribe] <= 0 and bribe not in unpurchasableBribes:
            bribe_AdviceDict["W1Bribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
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
        elif allBribesDict['W2'][bribe] <= 0 and bribe not in unpurchasableBribes:
            bribe_AdviceDict["W2Bribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
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
        elif allBribesDict['W3'][bribe] <= 0 and bribe not in unpurchasableBribes:
            bribe_AdviceDict["W3Bribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
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
            bribe_AdviceDict["W4Bribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
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
            bribe_AdviceDict["TrashIslandBribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
    bribe_AdviceGroupDict['Trash Island'] = AdviceGroup(
        tier="4",
        pre_string=f"Purchase the remaining Trash Island Bribe{pl(bribe_AdviceDict['TrashIslandBribes'])}",
        advices=bribe_AdviceDict['TrashIslandBribes'],
        post_string="You should be able to afford them by the end of W5, after unlocking the Bribes from Trash Island."
    )

    # W6 Bribes
    for bribe in allBribesDict['W6']:
        if allBribesDict['W6'][bribe] > 0:
            sum_bribeSetW6 += allBribesDict['W6'][bribe]
            sum_allBribes += allBribesDict['W6'][bribe]
        elif allBribesDict['W6'][bribe] <= 0 and bribe not in unpurchasableBribes:
            bribe_AdviceDict["W6Bribes"].append(Advice(
                label=bribe,
                picture_class=bribe
            ))
    bribe_AdviceGroupDict['W6'] = AdviceGroup(
        tier="5",
        pre_string=f"Purchase the remaining W6 Bribe{pl(bribe_AdviceDict['W6Bribes'])}",
        advices=bribe_AdviceDict['W6Bribes'],
        post_string="You should be able to afford them by the end of W6, after unlocking them from Jade Emporium."
    )
    # Assess Overall Bribe Tier
    if sum_allBribes >= max_allBribes:
        tier_BribesPurchased = max_tier
    else:
        # all_sums = [sum_allBribes, sum_bribeSetW1, sum_bribeSetW2, sum_bribeSetW3, sum_bribeSetW4, sum_bribeSetTrashIsland, sum_bribeSetW6]
        for tier in bribes_progressionTiers:
            if (sum_bribeSetW1 >= tier[1] and sum_bribeSetW2 >= tier[2] and sum_bribeSetW3 >= tier[3]
                    and sum_bribeSetW4 >= tier[4] and sum_bribeSetTrashIsland >= tier[5] and sum_bribeSetW6 >= tier[6]):
                tier_BribesPurchased = tier[0]

    overall_SectionTier = min(max_tier + info_tiers, tier_BribesPurchased)
    return bribe_AdviceGroupDict, overall_SectionTier, max_tier

def getBribesAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    bribe_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    bribe_AdviceSection = AdviceSection(
        name="Bribes",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Bribe tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Bribes.png',
        groups=bribe_AdviceGroupDict.values()
    )

    return bribe_AdviceSection
