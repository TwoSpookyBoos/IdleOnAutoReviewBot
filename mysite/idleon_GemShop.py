import json
import progressionResults

def getGemShopExclusions(inputJSON, playerCount):
    exclusionList = []
    sum_LabLevels = 0
    counter = 0
    while counter < playerCount: #not 0 based
        try:
            sum_LabLevels += int(inputJSON['Lv0_'+str(counter)][12])
        except Exception as reason:
            print("GemShop~ EXCEPTION Unable to get player lab level",counter,playerCount,reason)
        counter += 1
    if sum_LabLevels >= 180:
        exclusionList.append("Souped Up Tube")

    #0 through 95 are cogs placed on the board
    #96-98 are gray cog-making characters
    #99-101 are yellow cog-making
    #102-104 are red cog-making
    #105-106 are purple cog-making
    cogBlanks = 0
    cogList = inputJSON["CogO"][0:95] #expected to be a list
    for cog in cogList:
        if cog == "Blank":
            cogBlanks += 1
    if cogBlanks <= 60:
        exclusionList.append("Fluorescent Flaggies")

    try:
        autoArmLevel = json.loads(inputJSON["Tower"])[7]
    except Exception as reason:
        print("GemShop~ EXCEPTION Unable to get Automation Arm level",reason)
        autoArmLevel = 0
    if autoArmLevel >= 5:
        exclusionList.append("Burning Bad Books")

    currentArtifactsCount = 33  #as of w6 launch
    currentArtifactTiers = 4  #as of w6 launch

    try:
        sum_sailingArtifacts = sum(json.loads(inputJSON["Sailing"])[3])
        #print("GemShop.getGemShopExclusions~ OUTPUT sum_sailingArtifacts:",sum_sailingArtifacts)
        if sum_sailingArtifacts == (currentArtifactsCount*currentArtifactTiers): #30 artifacts times 3 tiers each = 90 for v1.91
            exclusionList.append("Chest Sluggo")
    except Exception as reason:
        print("GemShop~ EXCEPTION Unable to get Sailing Artifacts:",reason)

    return exclusionList

def getBonusSectionName(bonusName):
    match bonusName:
        case 'Item Backpack Space' | 'Storage Chest Space' | 'Carry Capacity' | 'Food Slot' | 'More Storage Space' | 'Card Presets':
            return "Inventory and Storage"

        case 'Daily Teleports' | 'Daily Minigame Plays':
            return "Dailies N' Resets"

        case 'Extra Card Slot':
            return "Cards"

        case 'Weekly Dungeon Boosters':
            return "Goods & Services"

        case 'Infinity Hammer' | 'Brimstone Forge Slot' | 'Ivory Bubble Cauldrons' | 'Bleach Liquid Cauldrons' | 'Obol Storage Space' | 'Sigil Supercharge':
            return "W1&2"

        case 'Crystal 3d Printer' | 'More Sample Spaces' | 'Burning Bad Books' | 'Prayer Slots' | 'Zen Cogs' | 'Cog Inventory Space' | 'Tower Building Slots' | 'Fluorescent Flaggies':
            return "W3"

        case 'Royal Egg Cap' | 'Richelin Kitchen' | 'Souped Up Tube' | 'Pet Storage' | 'Fenceyard Space':
            return "W4"

        case 'Chest Sluggo' | 'Divinity Sparkie' | 'Golden Sprinkler' | 'Lava Sprouts':
            return "W5"

        case 'W6-Placeholder1' | 'W6-Placeholder2' | 'W6-Placeholder3' | 'W6-Placeholder4' | 'W6-Placeholder5' | 'W6-Placeholder6' | 'W6-Placeholder7' | 'W6-Placeholder8':
            return "W6"

        case 'FOMO-1' | 'FOMO-2' | 'FOMO-3' | 'FOMO-4' | 'FOMO-5' | 'FOMO-6' | 'FOMO-7' | 'FOMO-8':
            return "Limited Shop"
        case _:
            return "UnknownShop"

def getGemShopDict(inputJSON):
    parsedList = json.loads(inputJSON["GemItemsPurchased"])
    gemShopDict = {
        #Inventory and Storage
            'Item Backpack Space': 0,
            'Storage Chest Space': 0,
            'Carry Capacity': 0,
            'Food Slot': 0,
            'More Storage Space': 0,
            'Card Presets': 0,

            #Dailies N' Resets
            'Daily Teleports': 0,
            'Daily Minigame Plays': 0,

            #Cards
            'Extra Card Slot': 0,

            #Goods & Services
            'Weekly Dungeon Boosters': 0,

            #World 1&2
            'Infinity Hammer': 0,
            'Brimstone Forge Slot': 0,
            'Ivory Bubble Cauldrons': 0,
            'Bleach Liquid Cauldrons': 0,
            'Obol Storage Space': 0,
            'Sigil Supercharge': 0,

            #World 3
            'Crystal 3d Printer': 0,
            'More Sample Spaces': 0,
            'Burning Bad Books': 0,
            'Prayer Slots': 0,
            'Zen Cogs': 0,
            'Cog Inventory Space': 0,
            'Tower Building Slots': 0,
            'Fluorescent Flaggies': 0,

            #World 4
            'Royal Egg Cap': 0,
            'Richelin Kitchen': 0,
            'Souped Up Tube': 0,
            'Pet Storage': 0,
            'Fenceyard Space': 0,

            #World 5
            'Chest Sluggo': 0,
            'Divinity Sparkie': 0,
            'Golden Sprinkler': 0,
            'Lava Sprouts': 0,

            #World 6
            'W6-Placeholder1': 0,
            'W6-Placeholder2': 0,
            'W6-Placeholder3': 0,
            'W6-Placeholder4': 0,
            'W6-Placeholder5': 0,
            'W6-Placeholder6': 0,
            'W6-Placeholder7': 0,
            'W6-Placeholder8': 0,

            #Fomo
            'FOMO-1': 0,
            'FOMO-2': 0,
            'FOMO-3': 0,
            'FOMO-4': 0,
            'FOMO-5': 0,
            'FOMO-6': 0,
            'FOMO-7': 0,
            'FOMO-8': 0
            } #Default 0s
    try:
        gemShopDict = {
            #Inventory and Storage
            'Item Backpack Space': parsedList[55],
            'Storage Chest Space': parsedList[56],
            'Carry Capacity': parsedList[58],
            'Food Slot': parsedList[59],
            'More Storage Space': parsedList[109],
            'Card Presets': parsedList[66],

            #Dailies N' Resets
            'Daily Teleports': parsedList[71],
            'Daily Minigame Plays': parsedList[72],

            #Cards
            'Extra Card Slot': parsedList[63],

            #Goods & Services
            'Weekly Dungeon Boosters': parsedList[84],

            #World 1&2
            'Infinity Hammer': parsedList[103],
            'Brimstone Forge Slot': parsedList[104],
            'Ivory Bubble Cauldrons': parsedList[105],
            'Bleach Liquid Cauldrons': parsedList[106],
            'Obol Storage Space': parsedList[57],
            'Sigil Supercharge': parsedList[110],

            #World 3
            'Crystal 3d Printer': parsedList[111],
            'More Sample Spaces': parsedList[112],
            'Burning Bad Books': parsedList[113],
            'Prayer Slots': parsedList[114],
            'Zen Cogs': parsedList[115],
            'Cog Inventory Space': parsedList[116],
            'Tower Building Slots': parsedList[117],
            'Fluorescent Flaggies': parsedList[118],

            #World 4
            'Royal Egg Cap': parsedList[119],
            'Richelin Kitchen': parsedList[120],
            'Souped Up Tube': parsedList[123],
            'Pet Storage': parsedList[124],
            'Fenceyard Space': parsedList[125],

            #World 5
            'Chest Sluggo': parsedList[129],
            'Divinity Sparkie': parsedList[130],
            'Golden Sprinkler': parsedList[131],
            'Lava Sprouts': parsedList[133],

            #World 6
            'W6-Placeholder1': 0,
            'W6-Placeholder2': 0,
            'W6-Placeholder3': 0,
            'W6-Placeholder4': 0,
            'W6-Placeholder5': 0,
            'W6-Placeholder6': 0,
            'W6-Placeholder7': 0,
            'W6-Placeholder8': 0,

            #Fomo
            'FOMO-1': parsedList[87],
            'FOMO-2': parsedList[88],
            'FOMO-3': parsedList[89],
            'FOMO-4': parsedList[90],
            'FOMO-5': parsedList[91],
            'FOMO-6': parsedList[92],
            'FOMO-7': parsedList[93],
            'FOMO-8': parsedList[94]
            }
    except Exception as reason:
        print("GemShop~ EXCEPTION Unable to parse Gem Shop: " , reason)
    #print(gemShopDict)
    return gemShopDict

def setGemShopProgressionTier(inputJSON, progressionTiers, playerCount):
    gemShopDict = getGemShopDict(inputJSON)
    gemShopExclusions = getGemShopExclusions(inputJSON, playerCount)
    if len(gemShopExclusions) > 0:
        for exclusion in gemShopExclusions:
            try:
                gemShopDict[exclusion] += 99
            except Exception as reason:
                print("Gemshop~ EXCEPTION: Unable to handle Exclusion",exclusion,reason)
    tier_GemShopPurchases = 0
    overall_GemShopTier = 0
    advice_SS = ""
    advice_S = ""
    advice_A = ""
    advice_B = ""
    advice_C = ""
    advice_D = ""
    advice_PracticalMax = ""
    advice_TrueMax = ""
    advice_TiersCombined = []
    advice_nextTier1 = ""
    advice_nextTier2 = ""
    advice_nextTier3 = ""
    #Review all tiers
    #progressionTiers[tier][0] = int tier
    #progressionTiers[tier][1] = str tierName
    #progressionTiers[tier][2] = dict recommendedPurchases
    #progressionTiers[tier][3] = str notes
    for recommendedPurchase in progressionTiers[1][2]:
        if progressionTiers[1][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_SS += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[1][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[2][2]:
        if progressionTiers[2][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_S += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[2][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[3][2]:
        if progressionTiers[3][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_A += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[3][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[4][2]:
        if progressionTiers[4][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_B += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[4][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[5][2]:
        if progressionTiers[5][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_C += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[5][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[6][2]:
        if progressionTiers[6][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_D += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[6][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[7][2]:
        if progressionTiers[7][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_PracticalMax += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[7][2][recommendedPurchase]) + "), "
    for recommendedPurchase in progressionTiers[8][2]:
        if progressionTiers[8][2][recommendedPurchase] > float(gemShopDict[recommendedPurchase]):
            advice_TrueMax += getBonusSectionName(recommendedPurchase) + "-" + str(recommendedPurchase) + " (" + str(gemShopDict[recommendedPurchase]) + "/" + str(progressionTiers[8][2][recommendedPurchase]) + "), "
    #Fix up advice statements
    if advice_SS != "":
        advice_SS = "SS: " + advice_SS[:-2] + progressionTiers[1][3]
    if advice_S != "":
        advice_S = "S: " + advice_S[:-2] + progressionTiers[2][3]
    if advice_A != "":
        advice_A = "A: " + advice_A[:-2] + progressionTiers[3][3]
    if advice_B != "":
        advice_B = "B: " + advice_B[:-2] + progressionTiers[4][3]
    if advice_C != "":
        advice_C = "C: " + advice_C[:-2] + progressionTiers[5][3]
    if advice_D != "":
        advice_D = "D: " + advice_D[:-2] + progressionTiers[6][3]
    if advice_PracticalMax != "":
        advice_PracticalMax = "Practical Max: " + advice_PracticalMax[:-2] + progressionTiers[7][3]
    if advice_TrueMax != "":
        advice_TrueMax = "True Max: " + advice_TrueMax[:-2] + progressionTiers[8][3]
    #Find highest 3 tiers not met, copy them to nextTier advices.
    advice_TiersCombined = [advice_SS, advice_S, advice_A, advice_B, advice_C, advice_D, advice_PracticalMax, advice_TrueMax]
    for advice in advice_TiersCombined:
        if advice != "":
            if advice_nextTier1 == "":
                advice_nextTier1 = advice
            elif advice_nextTier2 == "":
                advice_nextTier2 = advice
            elif advice_nextTier3 == "":
                advice_nextTier3 = advice
            #if all 3 next tiers are already filled, move on without any action
    overall_GemShopTier = min(progressionTiers[-1][-0], tier_GemShopPurchases)
    if advice_nextTier1 != "":
        advice_OverallGemShopCombined = ["DISCLAIMER: Recommended Gem Shop purchases are listed in their World order. All purchases within the same Ranking are approximately the same priority. Remember that items in the Limited Shop section could be more important than these always-available upgrades! Check the Limited Shop after each new patch/update.", "Recommended Permanent/Non-Gamba Gem Shop purchases (up to 3 tiers shown to account for personal preferences):",advice_nextTier1, advice_nextTier2, advice_nextTier3]
    else:
        advice_OverallGemShopCombined = ["", "", "", "", ""]
    gemShopPR = progressionResults.progressionResults(overall_GemShopTier,advice_OverallGemShopCombined,"")
    #print(gemShopPR.nTR)
    return gemShopPR
