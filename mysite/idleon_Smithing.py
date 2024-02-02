from models import AdviceSection
from models import AdviceGroup
from models import Advice
import progressionResults
from utils import pl


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
        print("Smithing.getUnusedForgeSlotsCount~ EXCEPTION Could not retrieve forge levels or items:", reason)
    #print("Smithing.getUnusedForgeSlotsCount~ OUTPUT unusedForgeSlotsCount/forgeOreSlotsPurchased:", unusedForgeSlotsCount, "/", forgeOreSlotsPurchased)
    return unusedForgeSlotsCount


def setSmithingProgressionTier(inputJSON, progressionTiers, playerCount, characterDict):
    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0
    max_tier = progressionTiers[-1][0]
    overall_SmithingTier = 0
    playerCashPoints = []
    playerMonsterPoints = []
    playerForgeUpgrades = []
    forgeUpgradesDict = {
        0: {
            "UpgradeName": "New Forge Slot",
            "Purchased": 0,
            "MaxPurchases": 16
        },
        1: {
            "UpgradeName": "Ore Capacity Boost",
            "Purchased": 0,
            "MaxPurchases": 50
        },
        2: {
            "UpgradeName": "Forge Speed",
            "Purchased": 0,
            "MaxPurchases": 90
        },
        3: {
            "UpgradeName": "Forge EXP Gain (Does Nothing!)",
            "Purchased": 0,
            "MaxPurchases": 85
        },
        4: {
            "UpgradeName": "Bar Bonanza",
            "Purchased": 0,
            "MaxPurchases": 75
        },
        5: {
            "UpgradeName": "Puff Puff Go",
            "Purchased": 0,
            "MaxPurchases": 60
        }
    }

    sum_CashPoints = 0
    sum_MonsterPoints = 0
    sum_ForgeUpgrades = 0
    advice_CashPoints = ""
    advice_MonsterPoints = ""
    advice_ForgeUpgrades = ""
    advice_CombinedSmithing = ""
    advice_UnusedForgeSlots = ""

    smithing_AdviceDict = {
        "CashPoints": [],
        "MonsterPoints": [],
        "ForgeUpgrades": [],
        "EmptyForgeSlots": []
    }
    smithing_AdviceGroupDict = {}
    smithing_AdviceSection = AdviceSection(
        name="Smithing",
        tier="Not Yet Evaluated",
        header="Best Smithing tier met: Not Yet Evaluated. Recommended Smithing actions",
        picture="Smithing_Infinity_Hammer.png"
    )

    #Total up all of the purchases across all current characters
    counter = 0
    while counter < playerCount:
        try:
            playerCashPoints.append(int(inputJSON["AnvilPAstats_"+str(counter)][1]))
            playerMonsterPoints.append(int(inputJSON["AnvilPAstats_" + str(counter)][2]))
            sum_CashPoints += int(inputJSON["AnvilPAstats_"+str(counter)][1])
            sum_MonsterPoints += int(inputJSON["AnvilPAstats_"+str(counter)][2])
        except Exception as reason:
            playerCashPoints.append(0)
            playerMonsterPoints.append(0)
            print("Smithing.setSmithingProgressionTier~ EXCEPTION Unable to read Anvil stats for Character", counter, "because:", reason)
        counter += 1

    #Total up all of the forge purchases, including the stinky Forge EXP
    try:
        playerForgeUpgrades = inputJSON["ForgeLV"]
        upgradeIndex = 0
        for upgrade in playerForgeUpgrades:
            sum_ForgeUpgrades += int(upgrade)
            forgeUpgradesDict[upgradeIndex]["Purchased"] = upgrade
            if forgeUpgradesDict[upgradeIndex]["Purchased"] < forgeUpgradesDict[upgradeIndex]["MaxPurchases"]:
                if not forgeUpgradesDict[upgradeIndex]["UpgradeName"].startswith("Forge EXP Gain"):
                    smithing_AdviceDict["ForgeUpgrades"].append(
                        Advice(
                            label=forgeUpgradesDict[upgradeIndex]["UpgradeName"],
                            item_name=forgeUpgradesDict[upgradeIndex]["UpgradeName"],
                            progression=forgeUpgradesDict[upgradeIndex]["Purchased"],
                            goal=forgeUpgradesDict[upgradeIndex]["MaxPurchases"],
                            unit=""
                        )
                    )
            upgradeIndex += 1
    except Exception as reason:
        #forgeUpgradesDict[upgradeIndex]["Purchased"] is defaulted to 0 already
        print("Smithing.setSmithingProgressionTier~ EXCEPTION Unable to read Forge upgrades:", reason)

    #Work out each tier individual and overall tier
    for tier in progressionTiers:
        #tier[0] = int tier
        #tier[1] = int Cash Points Purchased
        #tier[2] = int Monster Points Purchased
        #tier[3] = int Forge Totals
        #tier[4] = str Notes

        #Cash Points
        if tier_CashPoints == (tier[0]-1):  # Only check if they already met previous tier
            # anyRequirementFailed = False in (upgradeCount >= tier[1] for upgradeCount in playerCashPoints)
            allRequirementsMet = True
            characterIndex = 0
            for upgradeCount in playerCashPoints:
                if upgradeCount < tier[1]:
                    allRequirementsMet = False
                    smithing_AdviceDict["CashPoints"].append(
                        Advice(
                            label=characterDict[characterIndex].character_name,
                            item_name=characterDict[characterIndex].class_name_icon,
                            progression=upgradeCount,
                            goal=tier[1],
                            unit=""
                        )
                    )
                characterIndex += 1
            if allRequirementsMet == True:
                tier_CashPoints = tier[0]
            else:
                advice_CashPoints = "Purchase the first " + str(tier[1]) + " cash points on all characters. You're currently at (total): " + str(sum_CashPoints) + "/" + str(tier[1]*playerCount)
                smithing_AdviceGroupDict["CashPoints"] = AdviceGroup(
                    tier=str(tier_CashPoints),
                    pre_string=f"Purchase the first {tier[1]} Anvil Points with Cash on the following character{pl(smithing_AdviceDict['CashPoints'])}",
                    advices=smithing_AdviceDict["CashPoints"],
                    post_string=""
                )


        #Monster Points
        if tier_MonsterPoints == (tier[0]-1):  # Only check if they already met previous tier
            allRequirementsMet = True
            characterIndex = 0
            for upgradeCount in playerMonsterPoints:
                if upgradeCount < tier[2]:
                    allRequirementsMet = False
                    smithing_AdviceDict["MonsterPoints"].append(
                        Advice(
                            label=characterDict[characterIndex].character_name,
                            item_name=characterDict[characterIndex].class_name_icon,
                            progression=upgradeCount,
                            goal=tier[2],
                            unit=""
                        )
                    )
                characterIndex += 1
            if allRequirementsMet == True:
                tier_MonsterPoints = tier[0]
            else:
                advice_MonsterPoints = ("Purchase the first " + str(tier[2]) + " monster points on all characters, which includes drops from "
                + tier[4] + " You're currently at (total): " + str(sum_MonsterPoints) + "/" + str(tier[2]*playerCount))
                smithing_AdviceGroupDict["MonsterPoints"] = AdviceGroup(
                    tier=str(tier_CashPoints),
                    pre_string=f"Purchase the first {tier[2]} Anvil Points with Monster Materials on the following character{pl(smithing_AdviceDict['MonsterPoints'])}",
                    advices=smithing_AdviceDict["MonsterPoints"],
                    post_string=f"The final Monster Material for this tier is {tier[4]}"
                )

        #Forge Upgrades
        if tier_ForgeTotals == (tier[0]-1):  # Only check if they already met previous tier
            if sum_ForgeUpgrades >= tier[3]:
                tier_ForgeTotals = tier[0]
            else:
                advice_ForgeUpgrades = ("Purchase " + str(tier[3] - sum_ForgeUpgrades) + " more Forge upgrades. You're currently at (total): "
                + str(sum_ForgeUpgrades) + "/" + str(tier[3]) + ". (As of v1.91, Forge EXP Gain does absolutely nothing. Feel free to avoid it!)")
                smithing_AdviceGroupDict["ForgeUpgrades"] = AdviceGroup(
                    tier=str(tier_CashPoints),
                    pre_string=f"Purchase any {tier[3] - sum_ForgeUpgrades} additional Forge Upgrades",
                    advices=smithing_AdviceDict["ForgeUpgrades"],
                    post_string="As of v1.91, Forge EXP Gain does absolutely nothing. Feel free to skip it!"
                )

    #Check for any unused Forge slots
    unusedForgeSlots = getUnusedForgeSlotsCount(inputJSON)
    if unusedForgeSlots > 0:
        advice_UnusedForgeSlots = "Informational- You have " + str(unusedForgeSlots) + " empty ore slot in your Forge!"
        smithing_AdviceGroupDict["EmptyForgeSlots"] = AdviceGroup(
            tier="",
            pre_string=f"Informational - Fill the Forge",
            advices=[
                Advice(
                    label=f"You have {unusedForgeSlots} empty ore slot{pl(['']*unusedForgeSlots)} in your Forge!",
                    item_name="forge"
                )
            ],
            post_string=""
        )

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
    overall_SmithingTier = min(tier_CashPoints, tier_MonsterPoints, tier_ForgeTotals)
    tier_section = f"{overall_SmithingTier}/{max_tier}"
    smithing_AdviceSection.tier = tier_section
    if overall_SmithingTier == max_tier:
        advice_CombinedSmithing = ["Best Smithing tier met: " + str(overall_SmithingTier) + "/" + str(max_tier) + ". Recommended Smithing actions:", "Nada. You best <3", "", "", advice_UnusedForgeSlots]
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}. You best ❤️"
    else:
        advice_CombinedSmithing = ["Best Smithing tier met: " + str(overall_SmithingTier) + "/" + str(max_tier) + ". Recommended Smithing actions:", advice_CashPoints, advice_MonsterPoints, advice_ForgeUpgrades, advice_UnusedForgeSlots]
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}. Recommended Smithing actions"
        smithing_AdviceSection.groups = smithing_AdviceGroupDict.values()
    smithingPR = progressionResults.progressionResults(overall_SmithingTier, advice_CombinedSmithing, "")
    return {"PR": smithingPR, "AdviceSection": smithing_AdviceSection}
