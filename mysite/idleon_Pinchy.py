import json
from models import Advice
from utils import pl


def getHighestPrint(inputJSON):
    awfulPrinterList = json.loads(inputJSON["Print"])
    # print("Pinchy~ OUTPUT awfulPrinterList: ", type(awfulPrinterList), awfulPrinterList)
    goodPrinterList = [p for p in awfulPrinterList if isinstance(p, int)]
    highestPrintFound = max(goodPrinterList)
    # print("Pinchy~ OUTPUT Final highest print value found: ", highestPrintFound)

    return highestPrintFound


def setPinchyList(inputJSON, playerCount, dictOfPRs):
    highestPrint = getHighestPrint(inputJSON)
    sortedResultsListofLists = [
        [],  # [0] = w1/placeholder
        [], [], [],  # [1] = early w2, [2] = mid w2, [3] = late w2
        [], [], [],  # [4] = early w3, [5] = mid w3, [6] = late w3
        [], [], [],  # [7] = early w4, [8] = mid w4, [9] = late w4
        [], [], [],  # [10] = early w5, [11] = mid w5, [12] = late w5
        [], [], [],  # [13] = Early W6 Prep, [14] = Solid W6 Prep, [15] = w6 waiting room
        [], []  # [16] = max for v1.91, [17] = placeholder
    ]
    progressionNamesList = ["W1", "Early W2", "Mid W2", "Late W2", "Early W3",
                            "Mid W3", "Late W3", "Early W4", "Mid W4", "Late W4",
                            "Early W5", "Mid W5", "Late W5", "Early W6 Prep", "Solid W6 Prep",
                            "W6 Waiting Room", "Max for v1.91", "Placeholder"]
    maxWorldTiers = len(progressionNamesList) - 1
    maxExpectedIndexFromMaps = 13  # 13 is the highest map evaluated, Tremor Wurms.
    progressionTiersVsWorlds = {
        # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,99] #template
        #                           W1/W2           W3              W4              W5              W6              Max/Placeholder
        "Combat Levels":            [0, 3, 7, 8,    10, 14, 15,     16, 17, 18,     19, 21, 23,     25, 27, 28,     29, 99],
        "Stamps":                   [0, 1, 2, 3,    4, 5, 6,        7, 8, 9,        10, 11, 15,     22, 28, 34,     36, 99],
        "Bribes":                   [0, 1, 1, 1,    2, 2, 3,        3, 3, 3,        4, 4, 4,        5, 5, 5,        5, 99],
        "Smithing":                 [0, 0, 0, 0,    0, 0, 0,        0, 0, 0,        1, 2, 3,        4, 5, 6,        6, 99],
        "Alchemy-Bubbles":          [0, 0, 0, 1,    1, 1, 1,        2, 2, 2,        3, 4, 5,        7, 12, 18,      23, 99],
        "Alchemy-Vials":            [0, 0, 0, 0,    0, 0, 0,        1, 2, 3,        4, 5, 6,        7, 16, 19,      20, 99],
        "Construction Refinery":    [0, 0, 0, 0,    0, 0, 0,        0, 0, 0,        1, 1, 2,        3, 4, 5,        6, 99],
        "Construction Salt Lick":   [0, 0, 0, 0,    0, 0, 0,        0, 0, 1,        2, 3, 4,        5, 6, 7,        10, 99],
        "Worship Prayers":          [0, 0, 0, 0,    0, 0, 1,        1, 2, 3,        3, 4, 5,        5, 6, 7,        7, 99],
        "Construction Death Note":  [0, 0, 0, 0,    0, 0, 0,        0, 0, 0,        0, 4, 5,        12, 15, 19,     23, 99]
    }
    for name, pinchy_tier in dictOfPRs.items():
        tiers = progressionTiersVsWorlds[name][:-1]
        i, tier_next = next(((i - 1, tier_next) for i, tier_next in enumerate(tiers) if pinchy_tier < tier_next), (-1, 99))

        # if pinchy review tier has reached final threshold tier
        if i == -1:
            # print(f"Placing '{name}' into final tier because {pinchy_level} >= {tiers[i]}")
            text = name
        else:
            # print(name, pinchy_tier, tiers[i], tier_next)
            text = f"{name} (Next: Tier {tier_next})"

        sortedResultsListofLists[i].append(text)

    # find lowest and highest index with an entry
    lowestIndex = next((i for i, lst in enumerate(sortedResultsListofLists) if lst != []), 0)
    highestIndex = next((maxWorldTiers - i for i, lst in enumerate(reversed(sortedResultsListofLists)) if lst != []), maxWorldTiers)

    # find highest enemy killed or world unlocked to compare to
    # https://idleon.wiki/wiki/Portal_Requirements
    # W2 Sandy Pots = [51][0], starts at 250
    # W2 Mafiosos = [57][0], starts at 1200
    # W2 Tysons = [62][0], starts at 3000
    # W3 Sheepies = [101][0], starts at 1000
    # W3 Mamooths = [106][0], starts at 6000
    # W3 Quenchies = [110][0], starts at 18000
    # W4 Purp Mushroom = [151][0], starts at 5000
    # W4 Soda Can = [155][0], starts at 40000
    # W4 Clammies = [160][0], starts at 190000
    # W5 Suggma = [201][0], starts at 25000
    # W5 Stiltmole = [205][0], starts at 125000
    # W5 Fire Spirit = [210][0], starts at 3000000
    # W5 Tremor Wurms = [213][0], starts at 60000
    # Until W6 drops, Solid W6 prep = DeathNote tier 15+
    # Until W6 drops, W6 waiting room = DeathNote tier 19+
    # Until W6 drops, Max = 1b+ sample
    monsterPortalKills = [
        (13, (213, 60000)),
        (12, (210, 3000000)),
        (11, (205, 125000)),
        (10, (201, 25000)),
        (9, (160, 190000)),
        (8, (155, 40000)),
        (7, (151, 5000)),
        (6, (110, 18000)),
        (5, (106, 6000)),
        (4, (101, 1000)),
        (3, (62, 3000)),
        (2, (57, 1200)),
        (1, (51, 250)),
    ]
    expectedIndex = 0
    if highestPrint >= 999000000:
        expectedIndex = 16
    elif dictOfPRs["Construction Death Note"] >= 19:
        expectedIndex = 15
    elif dictOfPRs["Construction Death Note"] >= 15:
        expectedIndex = 14
    else:
        # print(f"Pinchy.setPinchyList~ INFO Starting to review map kill counts per player because expectedIndex still 0: {dictOfPRs["Construction Death Note"]}")
        for playerCounter in range(0, playerCount):
            playerKillsList = json.loads(inputJSON['KLA_' + str(playerCounter)])  # String pretending to be a list of lists yet again
            # print(type(playerKillsList), playerKillsList)  # Expected to be a list
            mobKills = [
                (i, playerKillsList[monster][0] < portalKC if len(playerKillsList) > monster else False)
                for i, (monster, portalKC)
                in monsterPortalKills
            ]
            expectedIndex = next((index for index, portalOpened in mobKills if portalOpened), 0)
            if expectedIndex >= maxExpectedIndexFromMaps:
                break

    # Generate advice based on catchup
    equalSnippet = ""
    if lowestIndex >= expectedIndex:
        equalSnippet = "Your lowest sections are roughly equal with (or better than!) your highest enemy map. Keep up the good work!"

    lowSectionName = progressionNamesList[lowestIndex]
    lowSections = sortedResultsListofLists[lowestIndex]
    pinchyAdvice = (f"{lowSectionName} rated section{pl(lowSectionName)}: {', '.join(lowSections)}. "
                    f"You can find detailed advice below in the section's World.")

    # Generate sneak peek advice
    peekList = []
    for peekIndex, peekSections in enumerate(sortedResultsListofLists[lowestIndex + 1:-1], start=lowestIndex + 1):
        try:
            peekSectionName = progressionNamesList[peekIndex]

            if peekSections:
                peekAdvice = f"Sneak peek: {peekSectionName} rated section{pl(peekSections)}: {', '.join(peekSections)}."
                peekList.append(peekAdvice)

        except IndexError as reason:
            print("Pinchy.setPinchyList~ EXCEPTION Unable to generate Pinchy Peek advice: ", reason)

    if expectedIndex == maxWorldTiers:
        pinchyHeader = ("Huh. Something went a little wrong here. You landed in the Placeholder tier somehow. "
                        "If you weren't expecting this, tell Scoli about it! O.o")
    else:
        pinchyHeader = f"Expected Progression, based on highest enemy map: {progressionNamesList[expectedIndex]}."
    pinchyMin = f"Minimum Progression, based on weakest ranked review: {progressionNamesList[lowestIndex]}."

    return [pinchyHeader, pinchyMin, [equalSnippet, pinchyAdvice], peekList]
