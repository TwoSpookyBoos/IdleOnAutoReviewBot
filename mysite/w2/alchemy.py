from math import floor

from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import safe_loads
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, bubbles_progressionTiers, vials_progressionTiers, max_IndexOfVials, maxFarmingCrops, atrisk_basicBubbles, \
    atrisk_lithiumBubbles, cookingCloseEnough

logger = get_logger(__name__)

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

    for vialName, vialValue in alchemyVialsDict.items():
        try:
            if int(vialValue.get("Level", 0)) == 0:
                lockedVialsList.append(vialName)
                #unmaxedVialsList.append(getReadableVialNames(vial))
                unmaxedVialsList.append(vialName)
            else:
                unlockedVials += 1
                if int(vialValue.get("Level", 0)) >= 4:
                    #virileVialsList.append(getReadableVialNames(vial))
                    virileVialsList.append(vialName)
                if int(vialValue.get("Level", 0)) >= 13:
                    #maxedVialsList.append(getReadableVialNames(vial))
                    maxedVialsList.append(vialName)
                else:
                    #unmaxedVialsList.append(getReadableVialNames(vial))
                    unmaxedVialsList.append(vialName)
        except:
            logger.exception(f"Could not coerce vial {vialName}'s level of {type(vialValue.get('Level', 0))} {vialValue.get('Level', 0)} to Int for Vial comparison")
            lockedVialsList.append(vialName)
            unmaxedVialsList.append(vialName)

    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0
    overall_AlchemyVialsTier = 0
    max_tier = vials_progressionTiers[-1][0]
    maxAdvicesPerGroup = 6

    if session_data.account.rift['VialMastery']:
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
        vial_AdviceSection.complete = True
    else:
        vial_AdviceSection.header = f"Best Vial tier met: {tier_section}"

    return vial_AdviceSection


def getBubbleExclusions():
    exclusionsList = []
    #If all crops owned or Evolution GMO is level 10+, exclude the requirement for Cropius Mapper
    if session_data.account.farming["CropsUnlocked"] >= maxFarmingCrops or session_data.account.farming["MarketUpgrades"].get("Evolution GMO", 0) > 20:
        exclusionsList.append("Cropius Mapper")

    #If cooking is nearly finished, exclude Diamond Chef
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        exclusionsList.append("Diamond Chef")

    return exclusionsList

def getAtRiskAdviceGroups() -> list[AdviceGroup]:
    atriskBasic_AdviceList = []
    atriskLithium_AdviceList = []
    nblbCount = session_data.account.labBonuses['No Bubble Left Behind']['Value']
    #Create a sorted list of every bubble, including the janky placeholders
    sorted_bubbles = sorted(
        session_data.account.alchemy_bubbles.items(),
        key=lambda bubble: bubble[1]['Level'],
        reverse=False
    )
    #Basic NBLB: Remove any bubbles with index 15 or higher and level of 1 or lower
    sorted_bubbles_basic = [(k, v) for k, v in sorted_bubbles if v['Level'] > 1 and v['BubbleIndex'] <= 14]
    if len(sorted_bubbles_basic) > 2 * nblbCount:
        basic_ps = f"Highest level for NBLB today: {sorted_bubbles_basic[nblbCount-1][1]['Level']}"
        atriskBasic_AdviceList.extend([
            Advice(
                label=bubbleName,
                picture_class=bubbleName,
                progression=bubbleValuesDict['Level'],
                goal=max(sorted_bubbles_basic[2 * nblbCount][1]['Level'], bubbleValuesDict['Level'] + 20),
                resource=bubbleValuesDict['Material']
            )
            for bubbleName, bubbleValuesDict in sorted_bubbles_basic
                if bubbleName in atrisk_basicBubbles
                and bubbleValuesDict['Level'] < sorted_bubbles_basic[2 * nblbCount][1]['Level']
        ])
    else:
        basic_ps = ""
    atriskBasic_AG = AdviceGroup(
        tier="",
        pre_string=f"Informational- \"Easy\" to print materials in your {2 * nblbCount} lowest leveled W1-W3 bubbles",
        advices=atriskBasic_AdviceList,
        post_string=basic_ps
    )

    #Same thing, but for Lithium Bubbles W4-W5 now
    #Lithium only works on W4 and W5 bubbles, indexes 15 through 24
    sorted_bubbles_lithium = [(k, v) for k, v in sorted_bubbles if 1 < v['Level'] < 1500 and 15 <= v['BubbleIndex'] <= 24]
    if len(sorted_bubbles_lithium) > nblbCount:
        lithium_ps = f"Highest level for Lithium today: {sorted_bubbles_lithium[nblbCount-1][1]['Level']}"

        atriskLithium_AdviceList.extend([
            Advice(
                label=bubbleName,
                picture_class=bubbleName,
                progression=bubbleValuesDict['Level'],
                goal=max(sorted_bubbles_lithium[nblbCount][1]['Level'], bubbleValuesDict['Level'] + 10),
                resource=bubbleValuesDict['Material']
            )
            for bubbleName, bubbleValuesDict in sorted_bubbles_lithium
                if bubbleName in atrisk_lithiumBubbles
                and bubbleValuesDict['Level'] < sorted_bubbles_lithium[nblbCount][1]['Level']
        ])
    else:
        lithium_ps = f""
    atriskLithium_AG = AdviceGroup(
        tier="",
        pre_string=f"Informational- Slower to print materials in your {nblbCount} lowest leveled W4-W5 bubbles",
        advices=atriskLithium_AdviceList if session_data.account.atom_collider['Atoms']['Lithium - Bubble Insta Expander']['Level'] >= 1 else [],
        post_string=lithium_ps
    )
    return [atriskBasic_AG, atriskLithium_AG]

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
    sum_TotalBubblesUnlocked = 0
    tier_OrangeSampleBubbles = 0
    tier_GreenSampleBubbles = 0
    tier_PurpleSampleBubbles = 0
    tier_UtilityBubbles = 0
    infoTiers = 3
    max_tier = bubbles_progressionTiers[-(1 + infoTiers)][0]  #Final 3 tiers are Informational
    overall_alchemyBubblesTier = 0

    exclusionsList = getBubbleExclusions()

    perCauldronBubblesUnlocked = [
        session_data.account.alchemy_cauldrons['OrangeUnlocked'],
        session_data.account.alchemy_cauldrons['GreenUnlocked'],
        session_data.account.alchemy_cauldrons['PurpleUnlocked'],
        session_data.account.alchemy_cauldrons['YellowUnlocked']
    ]
    sum_TotalBubblesUnlocked = session_data.account.alchemy_cauldrons['TotalUnlocked']
    nextWorldMissingBubbles = session_data.account.alchemy_cauldrons['NextWorldMissingBubbles']

    requirementsMet = [True, True, True, True]
    bubbleTypeList = ["OrangeSampleBubbles", "GreenSampleBubbles", "PurpleSampleBubbles", "UtilityBubbles"]
    adviceCountsDict = {bubbleType: 0 for bubbleType in bubbleTypeList}
    bubbleTiers = [0, 0, 0, 0]

    #Assess tiers
    for tier in bubbles_progressionTiers:
        #tier[0] = int tier
        #tier[1] = int TotalBubblesUnlocked
        #tier[2] = dict {OrangeSampleBubbles}
        #tier[3] = dict {GreenSampleBubbles}
        #tier[4] = dict {PurpleSampleBubbles}
        #tier[5] = dict {UtilityBubbles}
        #tier[6] = str BubbleValuePercentage
        #tier[7] = str Orange, Green, Purple Notes
        #tier[8] = str Utility Notes (Not used atm)

        #tier_TotalBubblesUnlocked
        if tier_TotalBubblesUnlocked == (tier[0]-1):  # Only check if they already met the previous tier
            if sum_TotalBubblesUnlocked >= tier[1]:
                tier_TotalBubblesUnlocked = tier[0]
            else:
                colorList = ["Orange", "Green", "Purple", "Yellow"]
                imagenameList = ["cauldron-o", "cauldron-g", "cauldron-p", "cauldron-y"]
                for cauldronIndex, cauldronBubblesUnlocked in enumerate(perCauldronBubblesUnlocked):
                    if cauldronBubblesUnlocked < (5 * nextWorldMissingBubbles):
                        bubbles_AdviceDict["TotalBubblesUnlocked"].append(
                            Advice(
                                label=f"{colorList[cauldronIndex]} Bubbles Unlocked",
                                picture_class=imagenameList[cauldronIndex],
                                progression=str(cauldronBubblesUnlocked - (5 * (nextWorldMissingBubbles - 1))),
                                goal=5)
                        )

        #Orange, Green, Purple, and Utility bubbles
        for typeIndex, bubbleType in enumerate(bubbleTypeList):
            for requiredBubble in tier[typeIndex+2]:
                if requiredBubble not in exclusionsList:
                    if session_data.account.alchemy_bubbles.get(requiredBubble, {}).get('Level', 0) < tier[typeIndex+2][requiredBubble]:
                        requirementsMet[typeIndex] = False
                        subgroupName = (f"To reach {'Informational ' if tier[0] > max_tier else ''}Tier {tier[0]}"
                                        f"{' (' if bubbleType != 'UtilityBubbles' else ''}"
                                        f"{tier[6] if bubbleType != 'UtilityBubbles' else ''}"
                                        f"{')' if bubbleType != 'UtilityBubbles' else ''}")
                        if subgroupName not in bubbles_AdviceDict[bubbleType] and len(bubbles_AdviceDict[bubbleType]) < maxTiersPerGroup:
                            bubbles_AdviceDict[bubbleType][subgroupName] = []
                        if subgroupName in bubbles_AdviceDict[bubbleType]:
                            adviceCountsDict[bubbleType] += 1
                            bubbles_AdviceDict[bubbleType][subgroupName].append(Advice(
                                label=str(requiredBubble),
                                picture_class=str(requiredBubble),
                                progression=str(session_data.account.alchemy_bubbles.get(requiredBubble, {}).get('Level', 0)),
                                goal=str(tier[typeIndex+2][requiredBubble]),
                                resource=str(session_data.account.alchemy_bubbles.get(requiredBubble, {}).get('Material', '')))),
            if bubbleTiers[typeIndex] == (tier[0] - 1) and requirementsMet[typeIndex] == True:  # Only update if they already met the previous tier
                bubbleTiers[typeIndex] = tier[0]

    overall_alchemyBubblesTier = min(max_tier + infoTiers, tier_TotalBubblesUnlocked,
                                     bubbleTiers[0], bubbleTiers[1], bubbleTiers[2], bubbleTiers[3])
    #Generate AdviceGroups
    agdNames = ["TotalBubblesUnlocked", "OrangeSampleBubbles", "GreenSampleBubbles", "PurpleSampleBubbles", "UtilityBubbles"]
    agdTiers = [tier_TotalBubblesUnlocked, bubbleTiers[0], bubbleTiers[1], bubbleTiers[2], bubbleTiers[3]]
    agdPre_strings = [
        f"Continue unlocking W{nextWorldMissingBubbles} bubbles",
        f"Level Orange sample-boosting bubbles",
        f"Level Green sample-boosting bubbles",
        f"Level Purple sample-boosting bubbles",
        f"Level Utility bubbles",
    ]
    for counter in range(0, len(agdNames)):
        bubbles_AdviceGroupDict[agdNames[counter]] = AdviceGroup(
            tier=f"{agdTiers[counter] if agdTiers[counter] < 22 else ''}",
            pre_string=f"{'Informational- ' if agdTiers[counter] >= 22 else ''}{agdPre_strings[counter]}",
            advices=bubbles_AdviceDict[agdNames[counter]]
        )
    bubbles_AdviceGroupDict['AtRiskBasic'], bubbles_AdviceGroupDict['AtRiskLithium'] = getAtRiskAdviceGroups()

    #Generate AdviceSection
    tier_section = f"{overall_alchemyBubblesTier}/{max_tier}"
    bubbles_AdviceSection.tier = tier_section
    bubbles_AdviceSection.pinchy_rating = overall_alchemyBubblesTier
    bubbles_AdviceSection.groups = bubbles_AdviceGroupDict.values()
    if overall_alchemyBubblesTier >= max_tier:
        bubbles_AdviceSection.header = f"Best Bubbles tier met: {tier_section}<br>You best ❤️"
        bubbles_AdviceSection.complete = True
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

    liquidCauldronSum = 0
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
    bubbleCauldronSum = sum(session_data.account.alchemy_p2w.get("Cauldrons"))
    vialsSum = sum(session_data.account.alchemy_p2w.get("Vials"))
    playerSum = sum(session_data.account.alchemy_p2w.get("Player"))
    if isinstance(session_data.account.alchemy_p2w.get("Liquids"), list):
        for liquidEntry in session_data.account.alchemy_p2w.get("Liquids"):  # Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
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

    if p2wSum < p2wMax:
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
            session_data.account.alerts_AdviceDict['World 2'].append(Advice(
                label=f"{{{{ P2W|#pay2win }}}} Player upgrades can be leveled",
                picture_class="p2w-player",
            ))
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
        p2w_AdviceSection.header = f"You've purchased all {p2wMax} upgrades in Alchemy's Pay 2 Win tab!<br>You best ❤️"
        p2w_AdviceSection.complete = True
    else:
        p2w_AdviceSection.header = f"You've purchased {tier_section} upgrades in Alchemy's Pay 2 Win tab.<br>Try to purchase the basic upgrades before Mid W5, and Player upgrades after each Alchemy level up!"
    return p2w_AdviceSection

# def setAlchemySigils() -> AdviceSection:
#     sigils_AdviceDict = {
#         "S": [], "A": [], "B": [], "C": [], "D": [], "F": []
#     }
#     sigils_AdviceGroupDict = {}
#     sigils_AdviceSection = AdviceSection(
#         name="Sigils",
#         tier="Not Yet Evaluated",
#         header="Best sigils tier met: Not Yet Evaluated. Recommended sigils actions:",
#         picture="Sigils.png"
#     )
#
#     highestLabLevel = max(session_data.account.all_skills["Laboratory"])
#     if highestLabLevel < 1:
#         sigils_AdviceSection.header = "Come back after unlocking the Laboratory skill in World 4!"
#         return sigils_AdviceSection
#
#     alchemy_sigilsList = session_data.account.alchemy_p2w["Sigils"]
#     sigils_AdviceDict["S"].append(Advice(
#         label="Jade Emporium: Ionized Sigils",
#         picture_class="ionized-sigils",
#         progression=f"{1 if 'Ionized Sigils' in session_data.account.jade_emporium_purchases else 0}",
#         goal=1
#     ))
#
#     # for tierIndex, tierContents in sigils_progressionTiers.items():
#     #     for sigilName in tierContents.get("Sigils", []):
#     #         if alchemy_sigilsList.get(sigilName, {}).get("PrechargeLevel") < max_IndexOfSigils:
#     #
#     #
#     # #Generate AdviceSection
#     return sigils_AdviceSection
