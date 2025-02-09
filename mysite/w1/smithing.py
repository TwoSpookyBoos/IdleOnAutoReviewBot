import math
from models.models import Advice, AdviceGroup, AdviceSection
from consts import smithing_progressionTiers, break_you_best, ValueToMulti, arcade_max_level
from flask import g as session_data
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger


logger = get_logger(__name__)

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
    achievement = session_data.account.achievements['Vitamin D-licious']['Complete']
    cap_Advices["Static Sources"].append(Advice(
        label=f"W5 Achievement: Vitamin D-licious: +{50 if achievement else 0}/50%",
        picture_class='vitamin-d-licious',
        progression="1" if achievement else "0",
        goal="1"
    ))

    #Bribe value of 1 means purchased
    bribe = session_data.account.bribes["W6"].get("Forge Cap Smuggling", -1) == 1
    bribe_value = 30 if bribe else 0
    bribe_multi = 1.3 if bribe else 1
    cap_Advices["Static Sources"].append(Advice(
        label=f"{{{{ Bribe|#bribes }}}}: Forge Cap Smuggling: {bribe_multi}/1.3x",
        picture_class='forge-cap-smuggling',
        progression="1" if bribe else "0",
        goal="1"
    ))

    #Verify Skill Mastery itself is unlocked from The Rift
    cap_Advices["Static Sources"].append(Advice(
        label="{{ Rift|#rift }} 16: Skill Mastery unlocked",
        picture_class='skill-mastery',
        progression=int(session_data.account.rift['SkillMastery']),
        goal=1
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
        label=f"{{{{ Forge Stamp|#stamps }}}}: +{session_data.account.stamps['Forge Stamp']['Value']:.2f}/57.50%",
        picture_class="forge-stamp",
        progression=session_data.account.stamps['Forge Stamp']['Level'],
        goal=230  #Forge Stamp currently has a max of 230, unless it gets increased by the Sacred Methods bundle.
    ))

    #Arcade Bonus 26 gives Forge Ore Capacity
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"{{{{Arcade|#arcade}}}} Bonus: "
              f"{session_data.account.arcade[26]['Value']:.2f}/"
              f"{session_data.account.arcade[26]['MaxValue']:.0f}%",
        picture_class=session_data.account.arcade[26]['Image'],
        progression=session_data.account.arcade[26]['Level'],
        goal=arcade_max_level+1,
        resource=session_data.account.arcade[26]['Material']
    ))

    #Cosmos > IdleOn Majik #2 Beeg Beeg Forge
    majik_beeg_forge = session_data.account.caverns['Majiks']['Beeg Beeg Forge']
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"Beeg Beeg Forge {{{{ Cavern Majik|#villagers }}}}: {majik_beeg_forge['Description']}",
        picture_class=f"{majik_beeg_forge['MajikType']}-majik-{'un' if majik_beeg_forge['Level'] == 0 else ''}purchased",
        progression=majik_beeg_forge['Level'],
        goal=majik_beeg_forge['MaxLevel']
    ))

    # Upgrade Vault > Beeg Forge
    beeg_forge = session_data.account.vault['Upgrades']['Beeg Forge']
    cap_Advices["Scaling Sources"].append(Advice(
        label=f"{{{{ Vault|#upgrade-vault }}}}: Beeg Forge: {beeg_forge['Description'].split('<')[0]}"
              f"<br>(Additive with Bribe)",
        picture_class=beeg_forge['Image'],
        progression=beeg_forge['Level'],
        goal=beeg_forge['Max Level']
    ))

    for group_name in cap_Advices:
        for advice in cap_Advices[group_name]:
            mark_advice_completed(advice)

    groupA = ValueToMulti((session_data.account.arcade[26]['Value'] + (30 * (next(c.getStars() for c in session_data.account.cards if c.name == 'Godshard Ore')+1))))
    groupB = ValueToMulti(session_data.account.stamps['Forge Stamp']['Value'])
    groupC = ValueToMulti(bribe_value + beeg_forge['Total Value'])
    groupD = ValueToMulti((50 * achievement) + (25 * skillMasteryBonusBool))
    groupE = majik_beeg_forge['Value']

    final_forgeCapacity = math.ceil(min(2e9, (20 + forge_upgrades) * groupA * groupB * groupC * groupD * groupE))
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

    sources_ag = AdviceGroup(
        tier='',
        pre_string="Info- Sources of Forge Ore Capacity",
        advices=cap_Advices,
        informational=True,
    )
    sources_ag.check_for_completeness()
    total_ag = AdviceGroup(
            tier='',
            pre_string="Info- Total Capacity and Bar thresholds",
            advices=bar_Advices,
            post_string="Note: Partial stacks round up to whole bars when claiming AFK",
            informational=True,
            completed=sources_ag.completed
        )
    cap_AdviceGroups = [sources_ag, total_ag]
    return cap_AdviceGroups

def getProgressionTiersAdviceGroup():
    smithing_AdviceDict = {
        "CashPoints": [],
        "MonsterPoints": [],
        "ForgeUpgrades": [],
        "EmptyForgeSlots": []
    }
    info_tiers = 0
    max_tier = smithing_progressionTiers[-1][0] - info_tiers
    tier_CashPoints = 0
    tier_MonsterPoints = 0
    tier_ForgeTotals = 0

    playerCashPoints = []
    playerMonsterPoints = []
    sum_CashPoints = 0
    sum_MonsterPoints = 0
    sum_ForgeUpgrades = 0
    # Total up all the purchases across all current characters
    # TODO: Move this parsing to Account
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

    # Total up all the forge purchases, including the stinky Forge EXP
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

    #Assess Tiers
    # TODO: Redo all of this in the new format, such as using maxTiersPerGroup and subgrouping AdviceGroups
    smithing_AdviceGroupDict = {}
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
                    post_string="As of v2.12, Forge EXP Gain does absolutely nothing. Feel free to skip it!"
                )
    overall_SectionTier = min(tier_CashPoints + info_tiers, tier_MonsterPoints, tier_ForgeTotals)
    return smithing_AdviceGroupDict, overall_SectionTier, max_tier

def getSmithingAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    smithing_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()
    smithing_AdviceGroupDict["OreCapacity"], smithing_AdviceGroupDict["Bars"] = getForgeCapacityAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    smithing_AdviceSection = AdviceSection(
        name="Smithing",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Smithing tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Smithing_Infinity_Hammer.gif",
        groups=smithing_AdviceGroupDict.values()
    )

    return smithing_AdviceSection
