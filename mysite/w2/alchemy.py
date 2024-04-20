import json
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import safe_loads
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, bubbles_progressionTiers, vials_progressionTiers, max_IndexOfVials, getReadableBubbleNames, max_IndexOfBubbles

logger = get_logger(__name__)

def getBubbleColorFromName(inputName):
    match inputName:
        case "FMJ" | "Call Me Bob" | "Carpenter", "Shimmeron":
            return " (Orange"
        case "Hammer Hammer" | "Shaquracy":
            return " (Green"
        case "Cookin Roadkill", "All For Kill":
            return " (Purple"
        case "Prowesessary" | "Laaarrrryyyy" | "Startue Exp" | "Droppin Loads" | "Diamond Chef" | "Big P" | "Big Game Hunter" | "Mr Massacre" | "Grind Time":
            return " (Yellow"
        case _:
            return f" (Unknown- {inputName}"

def getSumUnlockedBubbles(colorDict, colorString):
    bubblesUnlocked = 0
    for bubble in colorDict:
        if not isinstance(colorDict[bubble], int):
            #logger.warning(f"Non-Integer Bubble value found. Attempting to convert: {colorString} {bubble} {type(colorDict[bubble])} {colorDict[bubble]}")
            try:
                colorDict[bubble] = int(round(float(colorDict[bubble])))
            except:
                logger.exception(f"Could not convert [{colorString} {bubble} {type(colorDict[bubble])} {colorDict[bubble]}] to int :( Setting bubble to level 0")
                colorDict[bubble] = 0
        if colorDict[bubble] > 0:
            bubblesUnlocked += 1
    return bubblesUnlocked

def setAlchemyVialsProgressionTier() -> AdviceSection:
    vial_AdviceDict = {
        "EarlyVials": {
        },
        "MaxVials": {
            "Total Maxed Vials": [],
            "Vials to max next": [],
        },
    }
    vial_AdviceGroupDict = {}
    vial_AdviceSection = AdviceSection(
        name="Vials",
        tier="Not Yet Evaluated",
        header="Best Vial tier met: Not Yet Evaluated",
        picture="Alchemy_Vial-level-1.png"
    )
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        vial_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return vial_AdviceSection

    virileVialsList = []
    maxExpectedVV = max_IndexOfVials-4  # Exclude both pickle and both rare drop vials
    maxedVialsList = []
    unmaxedVialsList = []
    lockedVialsList = []
    alchemyVialsDict = session_data.account.alchemy_vials
    unlockedVials = 0

    for vial in alchemyVialsDict:
        try:
            if int(alchemyVialsDict[vial]) == 0:
                lockedVialsList.append(vial)
                #unmaxedVialsList.append(getReadableVialNames(vial))
                unmaxedVialsList.append(vial)
            else:
                unlockedVials += 1
                if int(alchemyVialsDict[vial]) >= 4:
                    #virileVialsList.append(getReadableVialNames(vial))
                    virileVialsList.append(vial)
                if int(alchemyVialsDict[vial]) >= 13:
                    #maxedVialsList.append(getReadableVialNames(vial))
                    maxedVialsList.append(vial)
                else:
                    #unmaxedVialsList.append(getReadableVialNames(vial))
                    unmaxedVialsList.append(vial)
        except:
            logger.exception(f"Could not coerce {type(alchemyVialsDict[vial])} {alchemyVialsDict[vial]} to Int for Vial comparison")
            lockedVialsList.append(vial)
            unmaxedVialsList.append(vial)

    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0
    overall_AlchemyVialsTier = 0
    max_tier = vials_progressionTiers[-1][0]
    maxAdvicesPerGroup = 6

    if session_data.account.vial_mastery_unlocked:
        if len(maxedVialsList) < 27:
            advice_TrailingMaxedVials = " 27 is the magic number needed to get the Snake Skin vial to 100% chance to double deposited statues :D (This also requires Snake Skin itself be maxed lol)"
        else:
            advice_TrailingMaxedVials = " Thanks to the Vial Mastery bonus in W4's Rift, every maxed vial increases the bonus of EVERY vial you have unlocked!"
    else:
        advice_TrailingMaxedVials = ""

    for tier in vials_progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalVialsUnlocked
        #tier[2] = int TotalVialsMaxed
        #tier[3] = list ParticularVialsMaxed
        #tier[4] = str Notes

        #Total Vials Unlocked
        if tier_TotalVialsUnlocked == (tier[0]-1):  # Only check if they already met previous tier
            if unlockedVials >= tier[1]:
                tier_TotalVialsUnlocked = tier[0]
            else:
                if f"To reach Tier {tier[0]}" not in vial_AdviceDict["EarlyVials"]:
                    vial_AdviceDict["EarlyVials"][f"To reach Tier {tier[0]}"] = []
                vial_AdviceDict["EarlyVials"][f"To reach Tier {tier[0]}"].append(
                    Advice(
                        label=f"Unlock {tier[1] - unlockedVials} more vial{pl(tier[1] - unlockedVials, '', 's')}",
                        picture_class="vials",
                        progression=str(unlockedVials),
                        goal=str(tier[1]))
                )

        #Total Vials Maxed
        if tier_TotalVialsMaxed == (tier[0]-1):  # Only check if they already met previous tier
            if len(maxedVialsList) >= tier[2]:
                tier_TotalVialsMaxed = tier[0]
            else:
                if tier_TotalVialsMaxed >= 20:
                    advice_TrailingMaxedVials += tier[4]
                vial_AdviceDict["MaxVials"]["Total Maxed Vials"].append(
                    Advice(label="Total Maxed Vials", picture_class="vial-max", progression=str(len(maxedVialsList)), goal=str(tier[2]))
                )

        #Particular Vials Maxed
        for requiredVial in tier[3]:
            if requiredVial in unmaxedVialsList:
                if len(vial_AdviceDict["MaxVials"]["Vials to max next"]) < maxAdvicesPerGroup:
                    vial_AdviceDict["MaxVials"]["Vials to max next"].append(
                        Advice(label=requiredVial, picture_class=requiredVial.split("(")[0].strip(), progression="", goal="")
                    )

    if len(virileVialsList) < maxExpectedVV:
        vial_AdviceDict["EarlyVials"]["Info - Shaman's Virile Vials"] = [
            Advice(label="Total level 4+ Vials", picture_class="vial-l4", progression=len(virileVialsList), goal=maxExpectedVV)
        ]

    #Generate AdviceGroups
    vial_AdviceGroupDict["Total Unlocked Vials"] = AdviceGroup(
        tier=str(tier_TotalVialsUnlocked),
        pre_string="Early Vial Goals",
        post_string="",
        advices=vial_AdviceDict["EarlyVials"]
    )
    if len(vial_AdviceDict["EarlyVials"]) > 1:
        vial_AdviceGroupDict["Total Unlocked Vials"].post_string = "For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!"

    vial_AdviceGroupDict["Total Maxed Vials"] = AdviceGroup(
        tier=str(tier_TotalVialsMaxed),
        pre_string="Late Vial Goals",
        post_string=advice_TrailingMaxedVials,
        advices=vial_AdviceDict["MaxVials"]  #["Total Maxed Vials"]
    )

    #Generate AdviceSection
    overall_AlchemyVialsTier = min(tier_TotalVialsUnlocked, tier_TotalVialsMaxed)  #, tier_ParticularVialsMaxed)
    tier_section = f"{overall_AlchemyVialsTier}/{max_tier}"
    vial_AdviceSection.tier = tier_section
    vial_AdviceSection.pinchy_rating = overall_AlchemyVialsTier
    vial_AdviceSection.groups = vial_AdviceGroupDict.values()
    if overall_AlchemyVialsTier == max_tier:
        vial_AdviceSection.header = f"Best Vial tier met: {tier_section}<br>You best ❤️"
    else:
        vial_AdviceSection.header = f"Best Vial tier met: {tier_section}"

    return vial_AdviceSection

def setAlchemyBubblesProgressionTier() -> AdviceSection:
    bubbles_AdviceDict = {
        "TotalBubblesUnlocked": [],
        "PurpleSampleBubbles": {},
        "OrangeSampleBubbles": {},
        "GreenSampleBubbles": {},
        "UtilityBubbles": {}
    }
    bubbles_AdviceGroupDict = {}
    bubbles_AdviceSection = AdviceSection(
        name="Bubbles",
        tier="Not Yet Evaluated",
        header="Best Bubbles tier met: Not Yet Evaluated. Recommended Bubbles actions:",
        picture="Alchemy_Bubble_all.gif"
    )
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        bubbles_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return bubbles_AdviceSection

    tier_TotalBubblesUnlocked = 0
    orangeBubblesUnlocked = 0
    greenBubblesUnlocked = 0
    purpleBubblesUnlocked = 0
    yellowBubblesUnlocked = 0
    sum_TotalBubblesUnlocked = 0
    tier_OrangeSampleBubbles = 0
    tier_GreenSampleBubbles = 0
    tier_PurpleSampleBubbles = 0
    tier_UtilityBubbles = 0
    max_tier = bubbles_progressionTiers[-1][0]
    overall_alchemyBubblesTier = 0
    adviceCountsDict = {"PurpleSampleBubbles": 0, "OrangeSampleBubbles": 0, "GreenSampleBubbles": 0, "UtilityBubbles": 0}

    #Get the bubble data and remove the length element
    raw_orange_alchemyBubblesDict = session_data.account.raw_data["CauldronInfo"][0]
    raw_orange_alchemyBubblesDict.pop('length', None)
    raw_green_alchemyBubblesDict = session_data.account.raw_data["CauldronInfo"][1]
    raw_green_alchemyBubblesDict.pop('length', None)
    raw_purple_alchemyBubblesDict = session_data.account.raw_data["CauldronInfo"][2]
    raw_purple_alchemyBubblesDict.pop('length', None)
    raw_yellow_alchemyBubblesDict = session_data.account.raw_data["CauldronInfo"][3]
    raw_yellow_alchemyBubblesDict.pop('length', None)

    #Replace the bubble numbers with their names for readable evaluation against the progression tiers
    named_all_alchemyBubblesDict = {}
    for bubble in raw_orange_alchemyBubblesDict:
        if int(bubble) <= max_IndexOfBubbles:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Orange")] = int(raw_orange_alchemyBubblesDict[bubble])
    for bubble in raw_green_alchemyBubblesDict:
        if int(bubble) <= max_IndexOfBubbles:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Green")] = int(raw_green_alchemyBubblesDict[bubble])
    for bubble in raw_purple_alchemyBubblesDict:
        if int(bubble) <= max_IndexOfBubbles:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Purple")] = int(raw_purple_alchemyBubblesDict[bubble])
    for bubble in raw_yellow_alchemyBubblesDict:
        if int(bubble) <= max_IndexOfBubbles:
            named_all_alchemyBubblesDict[getReadableBubbleNames(bubble, "Yellow")] = int(raw_yellow_alchemyBubblesDict[bubble])

    #Sum up unlocked bubbles (level > 0)
    orangeBubblesUnlocked = getSumUnlockedBubbles(raw_orange_alchemyBubblesDict, "Orange")
    greenBubblesUnlocked = getSumUnlockedBubbles(raw_green_alchemyBubblesDict, "Green")
    purpleBubblesUnlocked = getSumUnlockedBubbles(raw_purple_alchemyBubblesDict, "Purple")
    yellowBubblesUnlocked = getSumUnlockedBubbles(raw_yellow_alchemyBubblesDict, "Yellow")
    sum_TotalBubblesUnlocked += orangeBubblesUnlocked + greenBubblesUnlocked + purpleBubblesUnlocked + yellowBubblesUnlocked

    bubbleUnlockListByWorld = [20,0,0,0,0,0,0,0,0]
    combined_BubblesList = [orangeBubblesUnlocked, greenBubblesUnlocked, purpleBubblesUnlocked, yellowBubblesUnlocked]
    for bubbleColorCount in combined_BubblesList:
        worldCounter = 1
        while bubbleColorCount >= 5 and worldCounter <= len(bubbleUnlockListByWorld)-1:
            bubbleUnlockListByWorld[worldCounter] += 5
            bubbleColorCount -= 5
            worldCounter += 1
        if bubbleColorCount > 0 and worldCounter <= len(bubbleUnlockListByWorld)-1:
            bubbleUnlockListByWorld[worldCounter] += bubbleColorCount
            bubbleColorCount = 0
    nextWorldMissingBubbles = 0
    for world in range(0, len(bubbleUnlockListByWorld)):
        if bubbleUnlockListByWorld[world] == 20:
            nextWorldMissingBubbles += 1

    #Assess tiers
    for tier in bubbles_progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalBubblesUnlocked
        #tier[2] = dict {OrangeSampleBubbles}
        #tier[3] = dict {GreenSampleBubbles}
        #tier[4] = dict {PurpleSampleBubbles}
        #tier[5] = dict {UtilityBubbles}
        #tier[6] = str BubbleValuePercentage
        #tier[7] = str Notes

        #tier_TotalBubblesUnlocked
        if tier_TotalBubblesUnlocked == (tier[0]-1):  # Only check if they already met the previous tier
            if sum_TotalBubblesUnlocked >= tier[1]:
                tier_TotalBubblesUnlocked = tier[0]
            else:
                advice_TotalBubblesUnlocked = "Tier " + str(tier_TotalBubblesUnlocked)
                advice_TotalBubblesUnlocked += "- You have unlocked " + str(bubbleUnlockListByWorld[nextWorldMissingBubbles]) + "/20 of W" + str(nextWorldMissingBubbles) + " bubbles."
                bubbleUnlockCountList = [orangeBubblesUnlocked, greenBubblesUnlocked, purpleBubblesUnlocked, yellowBubblesUnlocked]
                colorList = ["Orange", "Green", "Purple", "Yellow"]
                imagenameList = ["cauldron-o", "cauldron-g", "cauldron-p", "cauldron-y"]
                for counter in range(0, len(bubbleUnlockCountList)):
                    if bubbleUnlockCountList[counter] < (5 * nextWorldMissingBubbles):
                        bubbles_AdviceDict["TotalBubblesUnlocked"].append(
                            Advice(
                                label=f"{colorList[counter]} Bubbles Unlocked",
                                picture_class=imagenameList[counter],
                                progression=str(bubbleUnlockCountList[counter] - (5 * (nextWorldMissingBubbles - 1))),
                                goal=5)
                        )

        #tier_OrangeSampleBubbles
        all_orangeRequirementsMet = True
        for requiredBubble in tier[2]:
            #requiredBubble = name of the bubble
            #tier[2][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict.get(requiredBubble,0) = level of the player's bubble
            if named_all_alchemyBubblesDict.get(requiredBubble,0) < tier[2][requiredBubble]:
                all_orangeRequirementsMet = False
                subgroupName = f"To reach Tier {tier[0]} ({tier[6]} max value)"
                if subgroupName not in bubbles_AdviceDict["OrangeSampleBubbles"] and len(bubbles_AdviceDict["OrangeSampleBubbles"]) < maxTiersPerGroup:
                    bubbles_AdviceDict["OrangeSampleBubbles"][subgroupName] = []
                if subgroupName in bubbles_AdviceDict["OrangeSampleBubbles"]:
                    adviceCountsDict["OrangeSampleBubbles"] += 1
                    bubbles_AdviceDict["OrangeSampleBubbles"][subgroupName].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict.get(requiredBubble,0)),
                            goal=str(tier[2][requiredBubble]))
                    )
        if tier_OrangeSampleBubbles == (tier[0]-1) and all_orangeRequirementsMet == True:  # Only update if they already met the previous tier
            tier_OrangeSampleBubbles = tier[0]

        #tier_GreenSampleBubbles
        all_greenRequirementsMet = True
        for requiredBubble in tier[3]:
            #requiredBubble = name of the bubble
            #tier[2][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict.get(requiredBubble,0) = level of the player's bubble
            if named_all_alchemyBubblesDict.get(requiredBubble,0) < tier[3][requiredBubble]:
                all_greenRequirementsMet = False
                subgroupName = f"To reach Tier {tier[0]} ({tier[6]} max value)"
                if subgroupName not in bubbles_AdviceDict["GreenSampleBubbles"] and len(bubbles_AdviceDict["GreenSampleBubbles"]) < maxTiersPerGroup:
                    bubbles_AdviceDict["GreenSampleBubbles"][subgroupName] = []
                if subgroupName in bubbles_AdviceDict["GreenSampleBubbles"]:
                    adviceCountsDict["GreenSampleBubbles"] += 1
                    bubbles_AdviceDict["GreenSampleBubbles"][subgroupName].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict.get(requiredBubble,0)),
                            goal=str(tier[3][requiredBubble]))
                    )
        if tier_GreenSampleBubbles == (tier[0]-1) and all_greenRequirementsMet == True:  # Only update if they already met the previous tier
            tier_GreenSampleBubbles = tier[0]

        #tier_PurpleSampleBubbles
        all_purpleRequirementsMet = True
        for requiredBubble in tier[4]:
            #requiredBubble = name of the bubble
            #tier[3][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict.get(requiredBubble,0) = level of the player's bubble
            if named_all_alchemyBubblesDict.get(requiredBubble,0) < tier[4][requiredBubble]:
                all_purpleRequirementsMet = False
                subgroupName = f"To reach Tier {tier[0]} ({tier[6]} max value)"
                if subgroupName not in bubbles_AdviceDict["PurpleSampleBubbles"] and len(bubbles_AdviceDict["PurpleSampleBubbles"]) < maxTiersPerGroup:
                    bubbles_AdviceDict["PurpleSampleBubbles"][subgroupName] = []
                if subgroupName in bubbles_AdviceDict["PurpleSampleBubbles"]:
                    adviceCountsDict["PurpleSampleBubbles"] += 1
                    bubbles_AdviceDict["PurpleSampleBubbles"][subgroupName].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict.get(requiredBubble,0)),
                            goal=str(tier[4][requiredBubble]))
                    )
        if tier_PurpleSampleBubbles == (tier[0]-1) and all_purpleRequirementsMet == True:  # Only update if they already met the previous tier
            tier_PurpleSampleBubbles = tier[0]

        #tier_UtilityBubbles
        all_utilityRequirementsMet = True
        for requiredBubble in tier[5]:
            #requiredBubble = name of the bubble
            #tier[3][requiredBubble] = level of the bubble in the requirement
            #named_all_alchemyBubblesDict.get(requiredBubble,0) = level of the player's bubble
            if named_all_alchemyBubblesDict.get(requiredBubble,0) < tier[5][requiredBubble]:
                all_utilityRequirementsMet = False
                subgroupName = f"To reach Tier {tier[0]}"
                if subgroupName not in bubbles_AdviceDict["UtilityBubbles"] and len(bubbles_AdviceDict["UtilityBubbles"]) < maxTiersPerGroup:
                    bubbles_AdviceDict["UtilityBubbles"][subgroupName] = []
                if subgroupName in bubbles_AdviceDict["UtilityBubbles"]:
                    adviceCountsDict["UtilityBubbles"] += 1
                    bubbles_AdviceDict["UtilityBubbles"][subgroupName].append(
                        Advice(
                            label=str(requiredBubble),
                            picture_class=str(requiredBubble),
                            progression=str(named_all_alchemyBubblesDict.get(requiredBubble,0)),
                            goal=str(tier[5][requiredBubble]))
                    )
        if tier_UtilityBubbles == (tier[0]-1) and all_utilityRequirementsMet == True:
            tier_UtilityBubbles = tier[0]

    overall_alchemyBubblesTier = min(max_tier, tier_TotalBubblesUnlocked, tier_OrangeSampleBubbles, tier_GreenSampleBubbles, tier_PurpleSampleBubbles, tier_UtilityBubbles)

    #Generate AdviceGroups
    agdNames = ["TotalBubblesUnlocked", "OrangeSampleBubbles", "GreenSampleBubbles", "PurpleSampleBubbles", "UtilityBubbles"]
    agdTiers = [tier_TotalBubblesUnlocked, tier_OrangeSampleBubbles, tier_GreenSampleBubbles, tier_PurpleSampleBubbles, tier_UtilityBubbles]
    agdPre_strings = [
        f"Continue unlocking W{nextWorldMissingBubbles} bubbles",
        f"Level Orange sample-boosting bubbles",
        f"Level Green sample-boosting bubbles",
        f"Level Purple sample-boosting bubbles",
        f"Level Utility bubbles",
    ]
    agdPost_strings = [
        "", "", "",
        "Choppin Log samples are the largest producers of Atom Particles and should be given priority.",
        "",
    ]
    if tier_UtilityBubbles == max_tier:
        agdPost_strings.append(bubbles_progressionTiers[tier_UtilityBubbles][7])
    else:
        agdPost_strings.append(bubbles_progressionTiers[tier_UtilityBubbles+1][7])
    for counter in range(0, len(agdNames)):
        bubbles_AdviceGroupDict[agdNames[counter]] = AdviceGroup(
            tier=agdTiers[counter],
            pre_string=agdPre_strings[counter],
            post_string="",  #agdPost_strings[counter],
            advices=bubbles_AdviceDict[agdNames[counter]]
        )

    #Generate AdviceSection
    tier_section = f"{overall_alchemyBubblesTier}/{max_tier}"
    bubbles_AdviceSection.tier = tier_section
    bubbles_AdviceSection.pinchy_rating = overall_alchemyBubblesTier
    bubbles_AdviceSection.groups = bubbles_AdviceGroupDict.values()
    if overall_alchemyBubblesTier == max_tier:
        bubbles_AdviceSection.header = f"Best Bubbles tier met: {tier_section}<br>You best ❤️"
    else:
        bubbles_AdviceSection.header = f"Best Bubbles tier met: {tier_section}"

    return bubbles_AdviceSection

def setAlchemyP2W() -> AdviceSection:
    p2w_AdviceDict = {
        "Pay2Win": []
    }
    p2w_AdviceGroupDict = {}
    p2w_AdviceSection = AdviceSection(
        name="Pay2Win",
        tier="Not Yet Evaluated",
        header="Best P2W tier met: Not Yet Evaluated. Recommended P2W actions:",
        picture="pay2win.png"
    )

    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        p2w_AdviceSection.header = "Come back after unlocking the Alchemy skill in World 2!"
        return p2w_AdviceSection

    alchemyP2WList = safe_loads(session_data.account.raw_data["CauldronP2W"])
    for subElementIndex, subElementValue in enumerate(alchemyP2WList):
        if not isinstance(subElementValue, list):
            alchemyP2WList[subElementIndex] = [subElementValue]

    bubbleCauldronSum = 0
    liquidCauldronSum = 0
    vialsSum = 0
    playerSum = 0
    p2wSum = 0
    liquidCauldronsUnlocked = 1

    if highestAlchemyLevel >= 80:
        liquidCauldronsUnlocked = 4  #includes Toxic HG
    elif highestAlchemyLevel >= 35:
        liquidCauldronsUnlocked = 3  # includes Trench Seawater
    elif highestAlchemyLevel >= 20:
        liquidCauldronsUnlocked = 2  # includes Liquid Nitrogen

    bubbleCauldronMax = 4 * 375  # 4 cauldrons, 375 upgrades each
    liquidCauldronMax = 180 * liquidCauldronsUnlocked
    vialsMax = 15 + 45  # 15 attempts, 45 RNG
    bubbleCauldronSum = sum(alchemyP2WList[0])
    vialsSum = sum(alchemyP2WList[2])
    playerSum = sum(alchemyP2WList[3])
    if isinstance(alchemyP2WList[1], list):
        for liquidEntry in alchemyP2WList[1]:  # Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
            if liquidEntry != -1:
                liquidCauldronSum += liquidEntry

    p2wSum = bubbleCauldronSum + liquidCauldronSum + vialsSum + playerSum
    p2wMax = bubbleCauldronMax + liquidCauldronMax + vialsMax + (highestAlchemyLevel*2)
    p2wSumWithoutPlayer = bubbleCauldronSum + liquidCauldronSum + vialsSum
    p2wMaxWithoutPlayer = bubbleCauldronMax + liquidCauldronMax + vialsMax

    if p2wSumWithoutPlayer >= p2wMaxWithoutPlayer:
        p2w_AdviceSection.pinchy_rating = 1
        p2w_AdviceSection.tier = '1/1'
    else:
        p2w_AdviceSection.pinchy_rating = 0
        p2w_AdviceSection.tier = '0/1'

    if p2wSum >= p2wMax:
        p2w_AdviceSection.header = f"You've purchased all {p2wMax} upgrades in Alchemy-P2W! You best ❤️"
    else:
        if bubbleCauldronSum < bubbleCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Bubble Cauldron Upgrades", picture_class="cauldron-a", progression=str(bubbleCauldronSum), goal=str(bubbleCauldronMax))
            )
        if liquidCauldronSum < liquidCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Liquid Cauldron Upgrades", picture_class="bleach-liquid-cauldrons", progression=str(liquidCauldronSum),
                       goal=str(liquidCauldronMax))
            )
        if vialsSum < vialsMax:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Vial Upgrades", picture_class="vials", progression=str(vialsSum), goal=str(vialsMax))
            )
        if playerSum < highestAlchemyLevel*2:
            p2w_AdviceDict["Pay2Win"].append(
                Advice(label="Player Upgrades", picture_class="p2w-player", progression=str(playerSum), goal=str(highestAlchemyLevel * 2))
            )
    p2w_AdviceGroupDict["Pay2Win"] = AdviceGroup(
        tier="",
        pre_string="Remaining Pay2Win upgrades to purchase",
        post_string="",
        advices=p2w_AdviceDict["Pay2Win"]
    )

    #Generate AdviceSection
    tier_section = f"{p2wSum}/{p2wMax}"
    p2w_AdviceSection.tier = tier_section
    p2w_AdviceSection.groups = p2w_AdviceGroupDict.values()
    if p2wSum >= p2wMax:
        p2w_AdviceSection.header = f"You've purchased all {p2wMax} upgrades in Alchemy-P2W! You best ❤️"
    else:
        p2w_AdviceSection.header = f"You've purchased {tier_section} upgrades in Alchemy P2W. Try to purchase the basic upgrades before Mid W5, and Player upgrades after each level up!"
    return p2w_AdviceSection
