from models.models import Advice, AdviceGroup, AdviceSection
from consts import smithing_progressionTiers
from flask import g as session_data
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

def getUnusedForgeSlotsCount():
    unusedForgeSlotsCount = 0
    oreSlotIndex = 0
    try:
        forgeOreSlotsPurchased = session_data.account.raw_data["ForgeLV"][0]
        forgeAllItemOrderList = session_data.account.raw_data["ForgeItemOrder"]
        while oreSlotIndex < len(forgeAllItemOrderList) and (oreSlotIndex/3)+1 <= forgeOreSlotsPurchased:
            if forgeAllItemOrderList[oreSlotIndex] == "Blank":
                unusedForgeSlotsCount += 1
            oreSlotIndex += 3
    except:
        logger.exception(f"Could not retrieve forge levels or items. Returning 0 unused slots.")
    #print("Smithing.getUnusedForgeSlotsCount~ OUTPUT unusedForgeSlotsCount/forgeOreSlotsPurchased:", unusedForgeSlotsCount, "/", forgeOreSlotsPurchased)
    return unusedForgeSlotsCount


def setSmithingProgressionTier() -> AdviceSection:
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

    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0
    max_tier = smithing_progressionTiers[-1][0]
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

    #Total up all the purchases across all current characters
    for character in session_data.account.safe_characters:
        try:
            playerCashPoints.append(int(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][1]))
            playerMonsterPoints.append(int(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][2]))
            sum_CashPoints += int(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][1])
            sum_MonsterPoints += int(session_data.account.raw_data[f"AnvilPAstats_{character.character_index}"][2])
        except:
            playerCashPoints.append(0)
            playerMonsterPoints.append(0)
            logger.exception(f"Unable to retrieve AnvilPAstats_{character.character_index}")

    #Total up all the forge purchases, including the stinky Forge EXP
    try:
        playerForgeUpgrades = session_data.account.raw_data["ForgeLV"]
        upgradeIndex = 0
        for upgradeIndex, upgrade in enumerate(playerForgeUpgrades):
            sum_ForgeUpgrades += int(upgrade)
            forgeUpgradesDict[upgradeIndex]["Purchased"] = upgrade
            if forgeUpgradesDict[upgradeIndex]["Purchased"] < forgeUpgradesDict[upgradeIndex]["MaxPurchases"]:
                if not forgeUpgradesDict[upgradeIndex]["UpgradeName"].startswith("Forge EXP Gain"):
                    smithing_AdviceDict["ForgeUpgrades"].append(
                        Advice(
                            label=forgeUpgradesDict[upgradeIndex]["UpgradeName"],
                            picture_class='forge-upgrades',
                            progression=forgeUpgradesDict[upgradeIndex]["Purchased"],
                            goal=forgeUpgradesDict[upgradeIndex]["MaxPurchases"])
                    )
    except:
        logger.exception("Unable to retrieve ForgeLv")

    #Work out each tier individual and overall tier
    for tier in smithing_progressionTiers:
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
                            label=session_data.account.all_characters[characterIndex].character_name,
                            picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
                            progression=upgradeCount,
                            goal=tier[1])
                    )
                characterIndex += 1
            if allRequirementsMet == True:
                tier_CashPoints = tier[0]
            else:
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
                            label=session_data.account.all_characters[characterIndex].character_name,
                            picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
                            progression=upgradeCount,
                            goal=tier[2])
                    )
                characterIndex += 1
            if allRequirementsMet == True:
                tier_MonsterPoints = tier[0]
            else:
                smithing_AdviceGroupDict["MonsterPoints"] = AdviceGroup(
                    tier=str(tier_MonsterPoints),
                    pre_string=f"Purchase the first {tier[2]} Anvil Points with Monster Materials on the following character{pl(smithing_AdviceDict['MonsterPoints'])}",
                    advices=smithing_AdviceDict["MonsterPoints"],
                    post_string=f"The final Monster Material for this tier is {tier[4]}"
                )

        #Forge Upgrades
        if tier_ForgeTotals == (tier[0]-1):  # Only check if they already met previous tier
            if sum_ForgeUpgrades >= tier[3]:
                tier_ForgeTotals = tier[0]
            else:
                smithing_AdviceGroupDict["ForgeUpgrades"] = AdviceGroup(
                    tier=str(tier_CashPoints),
                    pre_string=f"Purchase any {tier[3] - sum_ForgeUpgrades} additional Forge Upgrades",
                    advices=smithing_AdviceDict["ForgeUpgrades"],
                    post_string="As of v1.91, Forge EXP Gain does absolutely nothing. Feel free to skip it!"
                )

    #Check for any unused Forge slots
    unusedForgeSlots = getUnusedForgeSlotsCount()
    if unusedForgeSlots > 0:
        advice_UnusedForgeSlots = "Informational- You have " + str(unusedForgeSlots) + " empty ore slot in your Forge!"
        smithing_AdviceGroupDict["EmptyForgeSlots"] = AdviceGroup(
            tier="",
            pre_string=f"Informational - Fill the Forge",
            advices=[
                Advice(label=f"You have {unusedForgeSlots} empty ore slot{pl([''] * unusedForgeSlots)} in your Forge!",
                       picture_class="empty-forge-slot")
            ],
            post_string=""
        )

    #Print out all the final smithing info
    overall_SmithingTier = min(tier_CashPoints, tier_MonsterPoints, tier_ForgeTotals)
    tier_section = f"{overall_SmithingTier}/{max_tier}"
    smithing_AdviceSection.pinchy_rating = overall_SmithingTier
    smithing_AdviceSection.tier = tier_section
    smithing_AdviceSection.groups = smithing_AdviceGroupDict.values()
    if overall_SmithingTier == max_tier:
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}<br>You best ❤️"
    else:
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}"
    return smithing_AdviceSection
