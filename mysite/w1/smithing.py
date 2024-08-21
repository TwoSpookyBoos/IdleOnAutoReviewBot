import math
from models.models import Advice, AdviceGroup, AdviceSection
from consts import smithing_progressionTiers, break_you_best
from flask import g as session_data
from utils.data_formatting import mark_advice_completed
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
    return unusedForgeSlotsCount

def getForgeCapacityAdviceGroup() -> list[AdviceGroup]:
    cap_Advices = {
        "Static Sources": [],
        "Scaling Sources": []
    }
    bar_Advices = {
        "Total Capacity": [],
        "Bars per Forge Slot": []
    }
    #Static Sources
    #Achievement value of -1 means completed
    achievement = session_data.account.achievements.get("Vitamin D-licious", False)
    cap_Advices["Static Sources"].append(Advice(
        label=f"W5 Achievement: Vitamin D-licious: +{50 if achievement else 0}/50%",
        picture_class='vitamin-d-licious',
        progression="1" if achievement else "0",
        goal="1"
    ))

    #Bribe value of 1 means purchased
    bribe = session_data.account.bribes["W6"].get("Forge Cap Smuggling", -1) == 1
    bribeValue = 1.3 if bribe else 1
    cap_Advices["Static Sources"].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Forge Cap Smuggling: {bribeValue}/1.3x",
        picture_class='forge-cap-smuggling',
        progression="1" if bribe else "0",
        goal="1"
    ))

    #Verify Skill Mastery itself is unlocked from The Rift
    cap_Advices["Static Sources"].append(Advice(
        label="{{ Rift|#rift }} 16: Skill Mastery unlocked",
        picture_class='skill-mastery',
        progression="1" if session_data.account.rift['SkillMastery'] else "0",
        goal="1"
    ))
    #Account-wide total smithing levels of 300 needed to unlock the bonus
    totalSmithingLevels = sum(session_data.account.all_skills.get("Smithing", [0]))
    skillMasteryBonusBool = session_data.account.rift['SkillMastery'] and totalSmithingLevels >= 300
    cap_Advices["Static Sources"].append(Advice(
        label=f"Skill Mastery at 300 Smithing: +{25 * skillMasteryBonusBool * session_data.account.rift['SkillMastery']}/25%",
        picture_class='smithing',
        progression=totalSmithingLevels,
        goal=300
    ))

    #Scaling Sources
    #Forge Upgrade purchased at the forge itself with coins
    forge_upgrades = (2 + 0.5 * (session_data.account.forge_upgrades[1]["Purchased"] - 1)) * session_data.account.forge_upgrades[1]["Purchased"] * 10
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"Forge Upgrade: {session_data.account.forge_upgrades[1]['UpgradeName']}: +{int(forge_upgrades)}/13250",
        picture_class='forge-upgrades',
        progression=session_data.account.forge_upgrades[1]["Purchased"],
        goal=session_data.account.forge_upgrades[1]["MaxPurchases"]
    ))

    #Godshard Ore card
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"Godshard Ore card: {30 * (1 + next(c.getStars() for c in session_data.account.cards if c.name == 'Godshard Ore'))}/180%",
        picture_class="godshard-ore-card",
        progression=1 + next(c.getStars() for c in session_data.account.cards if c.name == "Godshard Ore"),
        goal=6
    ))

    cap_Advices["Scaling Sources"].append(Advice(
        label=f"{{{{ Forge Stamp|#stamps }}}}: +{session_data.account.stamps.get('Forge Stamp', {}).get('Value', 0):.2f}/57.50%",
        picture_class="forge-stamp",
        progression=session_data.account.stamps.get("Forge Stamp", {}).get("Level", 0),
        goal=230  #Forge Stamp currently has a max of 230, unless it gets increased by the Sacred Methods bundle.
    ))

    #Arcade Bonus 26 gives Forge Ore Capacity
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"Arcade Bonus: {session_data.account.arcade.get(26, {}).get('Value', 0):.2f}/50%",
        picture_class="arcade-bonus-26",
        progression=session_data.account.arcade.get(26, {}).get("Level", 0),
        goal=100
    ))

    for group_name in cap_Advices:
        for advice in cap_Advices[group_name]:
            mark_advice_completed(advice)

    groupA = 1 + (((session_data.account.arcade.get(26, {}).get("Value", 0)) + (30 * (next(c.getStars() for c in session_data.account.cards if c.name == 'Godshard Ore')+1)))/100)
    groupB = 1 + session_data.account.stamps.get('Forge Stamp', {}).get('Value', 0) / 100
    groupC = bribeValue
    groupD = 1 + (50 * achievement + 25 * skillMasteryBonusBool) / 100

    final_forgeCapacity = math.ceil(min(2e9, (20 + forge_upgrades) * groupA * groupB * groupC * groupD))
    bar_Advices["Total Capacity"].append(Advice(
        label=f"Total Capacity: {final_forgeCapacity:,}",
        picture_class="empty-forge-slot"
    ))
    barDict = {
        "Godshard Bar": 15000,
        "Marble Bar": 4000,
        "Dreadlo Bar": 1000,
        "Starfire Bar": 500,
        "Lustre Bar": 250,
        "Void Bar": 100,
        "Dementia Bar": 40,
        "Platinum Bar": 16,
        "Gold Bar": 7,
        "Iron Bar": 4,
        "Copper Bar": 2
    }
    for barName, oreCost in barDict.items():
        nextBar = oreCost - (final_forgeCapacity % oreCost) if final_forgeCapacity % oreCost > 0 else oreCost
        bar_Advices["Bars per Forge Slot"].append(Advice(
            label=f"{math.floor(final_forgeCapacity / oreCost):,} {barName}s. {nextBar:,} capacity to next bar",
            picture_class=barName,
            progression=oreCost-nextBar,
            goal=oreCost
        ))

    cap_AdviceGroups = [
        AdviceGroup(
        tier='',
        pre_string="Info- Sources of Forge Ore Capacity",
        advices=cap_Advices),
        AdviceGroup(
        tier='',
        pre_string="Info- Total Capacity and Bar thresholds",
        advices=bar_Advices,
        post_string="Note: Partial stacks round up to whole bars when claiming AFK")
    ]
    return cap_AdviceGroups

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
        picture="Smithing_Infinity_Hammer.gif"
    )

    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0
    max_tier = smithing_progressionTiers[-1][0]
    overall_SmithingTier = 0
    playerCashPoints = []
    playerMonsterPoints = []
    sum_CashPoints = 0
    sum_MonsterPoints = 0
    sum_ForgeUpgrades = 0

    #Total up all the purchases across all current characters
    #TODO: Move this parsing to Account
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
    for upgradeIndex, upgradeData in session_data.account.forge_upgrades.items():
        sum_ForgeUpgrades += int(upgradeData["Purchased"])
        if upgradeData["Purchased"] < upgradeData["MaxPurchases"]:
            if not upgradeData["UpgradeName"].startswith("Forge EXP Gain"):
                smithing_AdviceDict["ForgeUpgrades"].append(
                    Advice(
                        label=upgradeData["UpgradeName"],
                        picture_class='forge-upgrades',
                        progression=upgradeData["Purchased"],
                        goal=upgradeData["MaxPurchases"])
                )

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
                            goal=tier[2],
                            resource=tier[4]
                        ))
                characterIndex += 1
            if allRequirementsMet == True:
                tier_MonsterPoints = tier[0]
            else:
                smithing_AdviceGroupDict["MonsterPoints"] = AdviceGroup(
                    tier=str(tier_MonsterPoints),
                    pre_string=f"Purchase the first {tier[2]} Anvil Points with Monster Materials on the following character{pl(smithing_AdviceDict['MonsterPoints'])}",
                    advices=smithing_AdviceDict["MonsterPoints"],
                    post_string=f"The final Monster Material for this tier is shown above.",
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
        session_data.account.alerts_AdviceDict['World 1'].append(Advice(
            label=f"You have {unusedForgeSlots} empty ore slot{pl([''] * unusedForgeSlots)} in your {{{{ Forge|#smithing }}}}!",
            picture_class="empty-forge-slot"
        ))

    #Forge Capacity calculations
    smithing_AdviceGroupDict["OreCapacity"], smithing_AdviceGroupDict["Bars"] = getForgeCapacityAdviceGroup()

    #Print out all the final smithing info
    overall_SmithingTier = min(tier_CashPoints, tier_MonsterPoints, tier_ForgeTotals)
    tier_section = f"{overall_SmithingTier}/{max_tier}"
    smithing_AdviceSection.pinchy_rating = overall_SmithingTier
    smithing_AdviceSection.tier = tier_section
    smithing_AdviceSection.groups = smithing_AdviceGroupDict.values()
    if overall_SmithingTier >= max_tier:
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}{break_you_best}"
        smithing_AdviceSection.complete = True
    else:
        smithing_AdviceSection.header = f"Best Smithing tier met: {tier_section}"
    return smithing_AdviceSection
