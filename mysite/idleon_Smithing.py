import progressionResults

def getUnusedForgeSlotsCount(inputJSON):
    unusedForgeSlotsCount = 0
    oreSlotIndex = 0
    try:
        forgeOreSlotsPurchased = inputJSON["ForgeLV"][0]
        #print("Smithing.getUnusedForgeSlotsCout~ OUTPUT forgeOreSlotsPurchased:", forgeOreSlotsPurchased)
        forgeAllItemOrderList = inputJSON["ForgeItemOrder"]
        while oreSlotIndex < len(forgeAllItemOrderList) and (oreSlotIndex/3)+1 <= forgeOreSlotsPurchased:
            if forgeAllItemOrderList[oreSlotIndex] == "Blank":
                unusedForgeSlotsCount += 1
            oreSlotIndex += 3
    except Exception as reason:
        print("Smithing.getUnusedForgeSlotsCout~ EXCEPTION Could not retrieve forge levels or items:", reason)
    #print("Smithing.getUnusedForgeSlotsCout~ OUTPUT unusedForgeSlotsCount/forgeOreSlotsPurchased:", unusedForgeSlotsCount, "/", forgeOreSlotsPurchased)
    return unusedForgeSlotsCount

def setSmithingProgressionTier(inputJSON, progressionTiers, playerCount):
    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0
    overall_SmithingTier = 0
    sum_CashPoints = 0
    sum_MonsterPoints = 0
    sum_ForgeUpgrades = 0
    advice_CashPoints = ""
    advice_MonsterPoints = ""
    advice_ForgeUpgrades = ""
    advice_CombinedSmithing = ""
    advice_UnusedForgeSlots = ""

    #Total up all of the purchases across all current characters
    counter = 0
    while counter < playerCount:
        try:
            sum_CashPoints += int(inputJSON["AnvilPAstats_"+str(counter)][1])
            sum_MonsterPoints += int(inputJSON["AnvilPAstats_"+str(counter)][2])
        except Exception as reason:
            print("Smithing.setSmithingProgressionTier~ EXCEPTION Unable to read Anvil stats for Character", counter, "because:", reason)
        counter += 1

    #Total up all of the forge purchases, including the stinky Forge EXP
    try:
        for upgrade in inputJSON["ForgeLV"]:
            sum_ForgeUpgrades += int(upgrade)
    except Exception as reason:
        print("Smithing.setSmithingProgressionTier~ EXCEPTION Unable to read Forge upgrades:", reason)

    #Work out each tier individual and overall tier
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int Cash Points Purchased
        #tier[2] = int Monster Points Purchased
        #tier[3] = int Forge Totals
        #tier[4] = str Notes
        if tier_CashPoints == (tier[0]-1): #Only check if they already met previous tier
            if sum_CashPoints >= (tier[1]*playerCount):
                tier_CashPoints = tier[0]
            else:
                advice_CashPoints = "Purchase the first " + str(tier[1]) + " cash points on all characters. You're currently at (total): " + str(sum_CashPoints) + "/" + str(tier[1]*playerCount)
        if tier_MonsterPoints == (tier[0]-1): #Only check if they already met previous tier
            if sum_MonsterPoints >= (tier[2]*playerCount):
                tier_MonsterPoints = tier[0]
            else:
                advice_MonsterPoints = ("Purchase the first " + str(tier[2]) + " monster points on all characters, which includes drops from "
                + tier[4] + " You're currently at (total): " + str(sum_MonsterPoints) + "/" + str(tier[2]*playerCount))
        if tier_ForgeTotals == (tier[0]-1): #Only check if they already met previous tier
            if sum_ForgeUpgrades >= tier[3]:
                tier_ForgeTotals = tier[0]
            else:
                advice_ForgeUpgrades = ("Purchase " + str(tier[3] - sum_ForgeUpgrades) + " more Forge upgrades. You're currently at (total): "
                + str(sum_ForgeUpgrades) + "/" + str(tier[3]) + ". (As of v1.91, Forge EXP Gain does absolutely nothing. Feel free to avoid it!)")
    overall_SmithingTier = min(tier_CashPoints, tier_MonsterPoints, tier_ForgeTotals)

    #Check for any unused Forge slots
    unusedForgeSlots = getUnusedForgeSlotsCount(inputJSON)
    if unusedForgeSlots == 1:
        advice_UnusedForgeSlots = "Informational- You have " + str(unusedForgeSlots) + " empty ore slot in your Forge!"
    elif unusedForgeSlots > 1:
        advice_UnusedForgeSlots = "Informational- You have " + str(unusedForgeSlots) + " empty ore slots in your Forge!"

    #Generate advice statement
    if advice_CashPoints != "":
        advice_CashPoints = "Tier " + str(tier_CashPoints) + "- " + advice_CashPoints
    if advice_MonsterPoints != "":
        advice_MonsterPoints = "Tier " + str(tier_MonsterPoints) + "- " + advice_MonsterPoints
    if advice_ForgeUpgrades != "":
        advice_ForgeUpgrades = "Tier " + str(tier_ForgeTotals) + "- " + advice_ForgeUpgrades

    #Print out all the final smithing info
    if overall_SmithingTier == progressionTiers[-1][-0]:
        advice_CombinedSmithing = ["Best Smithing tier met: " + str(overall_SmithingTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Smithing actions:", "Nada. You best <3", "", "", advice_UnusedForgeSlots]
    else:
        advice_CombinedSmithing = ["Best Smithing tier met: " + str(overall_SmithingTier) + "/" + str(progressionTiers[-1][-0]) + ". Recommended Smithing actions:",advice_CashPoints,advice_MonsterPoints,advice_ForgeUpgrades, advice_UnusedForgeSlots]
    #print("Determined lowest Smithing tier met to be: " + str(overall_SmithingTier) + "/" + str(highest_SmithingTier))
    #print("Recommended Smithing actions:\n" + advice_CombinedSmithing)
    #print(advice_CombinedSmithing)
    smithingPR = progressionResults.progressionResults(overall_SmithingTier, advice_CombinedSmithing, "")
    return smithingPR