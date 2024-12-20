from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl, getItemDisplayName
from utils.logging import get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, bubbles_progressionTiers, vials_progressionTiers, max_IndexOfVials, maxFarmingCrops, atrisk_basicBubbles, \
    atrisk_lithiumBubbles, cookingCloseEnough, break_you_best, sigils_progressionTiers, max_IndexOfSigils, max_VialLevel, numberOfArtifactTiers, stamp_maxes, \
    lavaFunc, vial_costs, min_NBLB, max_NBLB, nblb_skippable, nblb_max_index, ValueToMulti, atrisk_advancedBubbles, atrisk_lithiumAdvancedBubbles

logger = get_logger(__name__)

def getVialsProgressionTiersAdviceGroup():
    vial_AdviceDict = {
        "EarlyVials": {
        },
        "MaxVials": {
            "Total Maxed Vials": [],
            "Vials to max next": [],
        },
    }
    info_tiers = 1
    max_tier = vials_progressionTiers[-1][0] - info_tiers
    maxAdvicesPerGroup = 6
    tier_TotalVialsUnlocked = 0
    tier_TotalVialsMaxed = 0

    alchemyVialsDict = session_data.account.alchemy_vials
    virileVialsList = [vialName for vialName, vialValue in alchemyVialsDict.items() if vialValue['Level'] >= 4]
    maxExpectedVV = max_IndexOfVials - 4  # Exclude both pickle and both rare drop vials
    maxedVialsList = [vialName for vialName, vialValue in alchemyVialsDict.items() if vialValue['Level'] >= max_VialLevel]
    unmaxedVialsList = [vialName for vialName in alchemyVialsDict if vialName not in maxedVialsList]
    lockedVialsList = [vialName for vialName, vialValue in alchemyVialsDict.items() if vialValue['Level'] == 0]
    unlockedVials = sum(1 for vial in alchemyVialsDict.values() if vial['Level'] > 0)

    #Assess Tiers
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
                    goal = int(vial_costs[alchemyVialsDict[requiredVial]['Level']])
                    prog = 100 * (session_data.account.all_assets.get(alchemyVialsDict[requiredVial]['Material']).amount / max(1, goal))
                    # Generate Alerts
                    if prog >= 100 and alchemyVialsDict[requiredVial]['Level'] == max_VialLevel-1:
                        session_data.account.alerts_AdviceDict['World 2'].append(Advice(
                            label=f"{requiredVial} {{{{ Vial|#vials }}}} ready to be maxed!",
                            picture_class="vial-13"
                        ))
                    vial_AdviceDict["MaxVials"]["Vials to max next"].append(Advice(
                        label=f"{requiredVial} {'NEEDS TO BE UNLOCKED!' if alchemyVialsDict[requiredVial]['Level'] == 0 else ''}"
                              f"{'<br>Ready for level ' if prog >= 100 else ''}"
                              f"{alchemyVialsDict[requiredVial]['Level'] + 1 if prog >= 100 else ''}",
                        picture_class=getItemDisplayName(alchemyVialsDict[requiredVial]['Material']),
                        progression=f"{min(1000, prog):.1f}{'+' if min(1000, prog) == 1000 else ''}",
                        goal=100,
                        unit='%'
                    ))

    if len(virileVialsList) < maxExpectedVV:
        vial_AdviceDict["EarlyVials"]["Info - Shaman's Virile Vials"] = [
            Advice(
                label="Total level 4+ Vials",
                picture_class="vial-l4",
                progression=len(virileVialsList),
                goal=maxExpectedVV
            )
        ]

    #Generate AdviceGroups
    vial_AdviceGroupDict = {}
    vial_AdviceGroupDict["Total Unlocked Vials"] = AdviceGroup(
        tier=str(tier_TotalVialsUnlocked) if tier_TotalVialsUnlocked < max_tier else '',
        pre_string=f"{'Informational- ' if tier_TotalVialsUnlocked >= max_tier else ''}Early Vial Goals",
        post_string="",
        advices=vial_AdviceDict["EarlyVials"],
        informational=len(vial_AdviceDict["EarlyVials"]) == 1 and "Info - Shaman's Virile Vials" in vial_AdviceDict["EarlyVials"]
    )
    if len(vial_AdviceDict["EarlyVials"]) > 1:
        vial_AdviceGroupDict["Total Unlocked Vials"].post_string = "For the most unlock chances per day, rapidly drop multiple stacks of items on the cauldron!"

    vial_AdviceGroupDict["Total Maxed Vials"] = AdviceGroup(
        tier=f"{tier_TotalVialsMaxed if tier_TotalVialsMaxed < max_tier else ''}",
        pre_string=f"{'Informational- ' if tier_TotalVialsMaxed >= max_tier else ''}Late Vial Goals",
        post_string=advice_TrailingMaxedVials,
        advices=vial_AdviceDict["MaxVials"],
        informational=tier_TotalVialsMaxed >= max_tier
    )
    overall_SectionTier = min(tier_TotalVialsUnlocked + info_tiers, tier_TotalVialsMaxed)
    return vial_AdviceGroupDict, overall_SectionTier, max_tier

def getAlchemyVialsAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        vial_AdviceSection = AdviceSection(
            name="Vials",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Alchemy skill in World 2!",
            picture="Alchemy_Vial-level-1.png",
            unreached=True
        )
        return vial_AdviceSection

    #Generate AdviceGroups
    vial_AdviceGroupDict, overall_SectionTier, max_tier = getVialsProgressionTiersAdviceGroup()

    #Generate AdviceSection

    tier_section = f"{overall_SectionTier}/{max_tier}"
    vial_AdviceSection = AdviceSection(
        name="Vials",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Vial tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Alchemy_Vial-level-1.png",
        groups=vial_AdviceGroupDict.values()
    )
    return vial_AdviceSection

def getBubbleExclusions():
    exclusionsList = []
    #If all crops owned or Evolution GMO is level 10+, exclude the requirement for Cropius Mapper
    if session_data.account.farming["CropsUnlocked"] >= maxFarmingCrops or session_data.account.farming['MarketUpgrades']['Evolution Gmo']['Level'] > 20:
        exclusionsList.append("Cropius Mapper")

    #If cooking is nearly finished, exclude Diamond Chef
    if session_data.account.cooking['MaxRemainingMeals'] < cookingCloseEnough:
        exclusionsList.append("Diamond Chef")

    return exclusionsList

def getAtRiskBubblesAdviceGroups() -> list[AdviceGroup]:
    low_skip = 150
    high_skip = 300
    standard_today = "Basic - In Today's Range"
    standard = "Basic Skilling Resources"
    advanced_today = "Advanced - In Today's Range"
    advanced = "Advanced Resources"
    atriskBasic_AdviceList = {
        standard_today: [],
        standard: [],
        advanced_today: [],
        advanced: []
    }
    atriskLithium_AdviceList = {
        standard_today: [],
        standard: [],
        advanced_today: [],
        advanced: []
    }
    nblbCount = session_data.account.labBonuses['No Bubble Left Behind']['Value']
    #Create a sorted list of every bubble, including the janky placeholders
    sorted_bubbles = sorted(
        session_data.account.alchemy_bubbles.items(),
        key=lambda bubble: bubble[1]['Level'],
        reverse=False
    )
    #Basic NBLB: Remove any bubbles with index 15 or higher and level of 1 or lower
    sorted_bubbles_basic = [(k, v) for k, v in sorted_bubbles if v['Level'] >= min_NBLB and v['BubbleIndex'] <= 14]
    basic_prestring = ""
    lithium_prestring = ""
    basic_poststring = ""
    if sorted_bubbles_basic and max(session_data.account.all_skills['Lab'], default=0) > 1:
        try:
            todays_lowest = sorted_bubbles_basic[0][1]['Level']
            todays_highest = sorted_bubbles_basic[nblbCount - 1][1]['Level']
        except:
            todays_lowest = sorted_bubbles_basic[0][1]['Level']
            todays_highest = sorted_bubbles_basic[-1][1]['Level']
        if len(sorted_bubbles_basic) > 2 * nblbCount:
            basic_poststring = f"Today's W1-W3 NBLB range: {todays_lowest} - {todays_highest}"
        for bubbleName, bubbleValuesDict in sorted_bubbles_basic:
            if bubbleValuesDict['Level'] < max_NBLB and (
                    bubbleValuesDict['Level'] < todays_highest + 20
                    or todays_lowest >= low_skip
                    or todays_highest >= high_skip
            ):
                if bubbleName in atrisk_basicBubbles:
                    if bubbleValuesDict['Level'] <= todays_highest:
                        subgroupName = standard_today
                    else:
                        subgroupName = standard
                elif bubbleName in atrisk_advancedBubbles:
                    if bubbleValuesDict['Level'] <= todays_highest:
                        subgroupName = advanced_today
                    else:
                        subgroupName = advanced
                else:
                    subgroupName = ""

                if subgroupName:
                    if max(todays_highest + 20, bubbleValuesDict['Level'] + 20) < high_skip*2:
                        target = min(max_NBLB, max(todays_highest + 20, bubbleValuesDict['Level'] + 20))
                    else:
                        target = max_NBLB
                    atriskBasic_AdviceList[subgroupName].append(Advice(
                        label=f"{bubbleName}"
                              f"{' (Printing!)' if bubbleValuesDict['Material'] in session_data.account.printer['AllCurrentPrints'] else ''}",
                        picture_class=bubbleName,
                        progression=bubbleValuesDict['Level'],
                        goal=target,
                        resource=bubbleValuesDict['Material']
                    ))

        if todays_lowest >= low_skip:
            basic_prestring = f"Informational \"Easy\" to print materials in W1-W3 bubbles"
            lithium_prestring = f"Informational- Slower to print materials in W4-W5 bubbles"
        else:
            basic_prestring = f"Informational- \"Easy\" to print materials in your {2 * nblbCount} lowest leveled W1-W3 bubbles"
            lithium_prestring = f"Informational- Slower to print materials in your {nblbCount} lowest leveled W4-W5 bubbles"

    atriskBasic_AG = AdviceGroup(
        tier="",
        pre_string=basic_prestring,
        advices=atriskBasic_AdviceList,
        post_string=basic_poststring,
        informational=True
    )

    #Same thing, but for Lithium Bubbles W4-W5 now
    #Lithium only works on W4 and W5 bubbles, indexes 15 through 24
    sorted_bubbles_lithium = [(k, v) for k, v in sorted_bubbles if min_NBLB <= v['Level'] < max_NBLB and 15 <= v['BubbleIndex'] <= 24]
    #lithium_prestring = ""
    lithium_poststring = ""
    if sorted_bubbles_lithium and max(session_data.account.all_skills['Lab'], default=0) > 1:
        if len(sorted_bubbles_lithium) > nblbCount:
            try:
                todays_lowest_lithium = sorted_bubbles_lithium[0][1]['Level']
                todays_highest_lithium = sorted_bubbles_lithium[nblbCount - 1][1]['Level']
            except:
                todays_lowest_lithium = sorted_bubbles_lithium[0][1]['Level']
                todays_highest_lithium = sorted_bubbles_lithium[-1][1]['Level']
            lithium_poststring = f"Today's W4-W5 (Lithium) range: {todays_lowest_lithium} - {todays_highest_lithium}"
            for bubbleName, bubbleValuesDict in sorted_bubbles_lithium:
                if bubbleValuesDict['Level'] < max_NBLB and (
                        bubbleValuesDict['Level'] < todays_highest_lithium + 10
                        or len(atriskBasic_AdviceList) > 0
                ):
                    if bubbleName in atrisk_lithiumBubbles:
                        if bubbleValuesDict['Level'] <= todays_highest_lithium:
                            subgroupName = standard_today
                        else:
                            subgroupName = standard
                    elif bubbleName in atrisk_lithiumAdvancedBubbles:
                        if bubbleValuesDict['Level'] <= todays_highest_lithium:
                            subgroupName = advanced_today
                        else:
                            subgroupName = advanced
                    else:
                        subgroupName = ""

                    if subgroupName:
                        if max(todays_highest_lithium + 10, bubbleValuesDict['Level'] + 10) < 600:
                            target = min(max_NBLB, max(todays_highest_lithium + 10, bubbleValuesDict['Level'] + 10))
                        else:
                            target = max_NBLB
                        atriskLithium_AdviceList[subgroupName].append(Advice(
                            label=f"{bubbleName}{' (Printing!)' if bubbleValuesDict['Material'] in session_data.account.printer['AllCurrentPrints'] else ''}",
                            picture_class=bubbleName,
                            progression=bubbleValuesDict['Level'],
                            goal=target,
                            resource=bubbleValuesDict['Material']
                        ))

    atriskLithium_AG = AdviceGroup(
        tier="",
        pre_string=lithium_prestring,
        advices=atriskLithium_AdviceList if session_data.account.atom_collider['Atoms']['Lithium - Bubble Insta Expander']['Level'] >= 1 else [],
        post_string=lithium_poststring,
        informational=True
    )
    atriskBasic_AG.remove_empty_subgroups()
    atriskLithium_AG.remove_empty_subgroups()
    return [atriskBasic_AG, atriskLithium_AG]

def getBubblesProgressionTiersAdviceGroup():
    bubbles_AdviceDict = {
        'UnlockAndLevel': {
            "Unlock All Bubbles": [],
            'No Bubble Left Behind': []
        },
        "PurpleSampleBubbles": {},
        "OrangeSampleBubbles": {},
        "GreenSampleBubbles": {},
        "UtilityBubbles": {},
    }
    bubbles_AdviceGroupDict = {}

    infoTiers = 3
    max_tier = bubbles_progressionTiers[-1][0] - infoTiers  # Final 3 tiers are Informational
    tier_TotalBubblesUnlocked = 0
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

    # Assess tiers
    for tier in bubbles_progressionTiers:
        # tier[0] = int tier
        # tier[1] = int TotalBubblesUnlocked
        # tier[2] = dict {OrangeSampleBubbles}
        # tier[3] = dict {GreenSampleBubbles}
        # tier[4] = dict {PurpleSampleBubbles}
        # tier[5] = dict {UtilityBubbles}
        # tier[6] = str BubbleValuePercentage
        # tier[7] = str Orange, Green, Purple Notes
        # tier[8] = str Utility Notes (Not used atm)

        # tier_TotalBubblesUnlocked
        if tier_TotalBubblesUnlocked == (tier[0] - 1):  # Only check if they already met the previous tier
            if sum_TotalBubblesUnlocked >= tier[1]:
                tier_TotalBubblesUnlocked = tier[0]
            else:
                colorList = ["Orange", "Green", "Purple", "Yellow"]
                imagenameList = ["cauldron-o", "cauldron-g", "cauldron-p", "cauldron-y"]
                for cauldronIndex, cauldronBubblesUnlocked in enumerate(perCauldronBubblesUnlocked):
                    if cauldronBubblesUnlocked < (5 * nextWorldMissingBubbles):
                        bubbles_AdviceDict['UnlockAndLevel']["Unlock All Bubbles"].append(
                            Advice(
                                label=f"W{nextWorldMissingBubbles} {colorList[cauldronIndex]} Bubbles Unlocked",
                                picture_class=imagenameList[cauldronIndex],
                                progression=str(cauldronBubblesUnlocked - (5 * (nextWorldMissingBubbles - 1))),
                                goal=5)
                        )

        # Orange, Green, Purple, and Utility bubbles
        for typeIndex, bubbleType in enumerate(bubbleTypeList):
            for requiredBubble in tier[typeIndex + 2]:
                if requiredBubble not in exclusionsList:
                    if session_data.account.alchemy_bubbles[requiredBubble]['Level'] < tier[typeIndex + 2][requiredBubble]:
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
                                label=f"{requiredBubble}{' (Printing!)' if session_data.account.alchemy_bubbles[requiredBubble]['Material'] in session_data.account.printer['AllCurrentPrints'] else ''}",
                                picture_class=str(requiredBubble),
                                progression=str(session_data.account.alchemy_bubbles[requiredBubble]['Level']),
                                goal=str(tier[typeIndex + 2][requiredBubble]),
                                resource=str(session_data.account.alchemy_bubbles[requiredBubble]['Material']))),
            if bubbleTiers[typeIndex] == (tier[0] - 1) and requirementsMet[typeIndex] == True:  # Only update if they already met the previous tier
                bubbleTiers[typeIndex] = tier[0]

    for bubbleName, bubbleDetails in session_data.account.alchemy_bubbles.items():
        if (
                0 < bubbleDetails['Level'] < min_NBLB
                and bubbleName not in nblb_skippable
                and bubbleDetails['BubbleIndex'] <= nblb_max_index
        ):
            bubbles_AdviceDict['UnlockAndLevel']['No Bubble Left Behind'].append(
                Advice(
                    label=bubbleName,
                    picture_class=bubbleName,
                    progression=bubbleDetails['Level'],
                    goal=min_NBLB,
                    resource=bubbleDetails['Material'],
                ))

    # Generate AdviceGroups
    agdNames = ["UnlockAndLevel", "OrangeSampleBubbles", "GreenSampleBubbles", "PurpleSampleBubbles", "UtilityBubbles"]
    agdTiers = [tier_TotalBubblesUnlocked, bubbleTiers[0], bubbleTiers[1], bubbleTiers[2], bubbleTiers[3]]
    agdPre_strings = [
        f"Continue unlocking W{nextWorldMissingBubbles} bubbles and bringing worthwhile bubbles into No Bubble Left Behind range",
        f"Level Orange sample-boosting bubbles",
        f"Level Green sample-boosting bubbles",
        f"Level Purple sample-boosting bubbles",
        f"Level Utility bubbles",
    ]
    for counter, value in enumerate(agdNames):
        bubbles_AdviceGroupDict[value] = AdviceGroup(
            tier=f"{agdTiers[counter] if agdTiers[counter] < max_tier else ''}",
            pre_string=f"{'Informational- ' if agdTiers[counter] >= max_tier else ''}{agdPre_strings[counter]}",
            advices=bubbles_AdviceDict[value],
            informational=True if agdTiers[counter] >= max_tier else False
        )
        bubbles_AdviceGroupDict[value].remove_empty_subgroups()

    overall_SectionTier = min(
        max_tier + infoTiers, tier_TotalBubblesUnlocked,
        bubbleTiers[0], bubbleTiers[1], bubbleTiers[2], bubbleTiers[3]
    )
    return bubbles_AdviceGroupDict, overall_SectionTier, max_tier

def getAlchemyBubblesAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        bubbles_AdviceSection = AdviceSection(
            name="Bubbles",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Alchemy skill in World 2!",
            picture="Alchemy_Bubble_all.gif",
            unreached=True
        )
        return bubbles_AdviceSection

    #Generate AdviceGroups
    bubbles_AdviceGroupDict, overall_SectionTier, max_tier = getBubblesProgressionTiersAdviceGroup()
    bubbles_AdviceGroupDict['AtRiskBasic'], bubbles_AdviceGroupDict['AtRiskLithium'] = getAtRiskBubblesAdviceGroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    bubbles_AdviceSection = AdviceSection(
        name="Bubbles",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Bubbles tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Alchemy_Bubble_all.gif",
        groups=bubbles_AdviceGroupDict.values(),
    )

    return bubbles_AdviceSection

def getP2WProgressionTiersAdviceGroup(highestAlchemyLevel):
    p2w_AdviceDict = {
        "Pay2Win": []
    }
    p2w_AdviceGroupDict = {}
    info_tiers = 0
    max_tier = 1 - info_tiers
    tier_P2WUpgrades = 0
    liquidCauldronSum = 0
    liquidCauldronsUnlocked = 1

    if highestAlchemyLevel >= 80:
        liquidCauldronsUnlocked = 4  # includes Toxic HG
    elif highestAlchemyLevel >= 35:
        liquidCauldronsUnlocked = 3  # includes Trench Seawater
    elif highestAlchemyLevel >= 20:
        liquidCauldronsUnlocked = 2  # includes Liquid Nitrogen

    bubbleCauldronMax = 4 * 375  # 4 cauldrons, 375 upgrades each
    liquidCauldronMax = 180 * liquidCauldronsUnlocked
    vialsMax = 15 + 45  # 15 attempts, 45 RNG
    bubbleCauldronSum = sum(session_data.account.alchemy_p2w['Cauldrons'])
    vialsSum = sum(session_data.account.alchemy_p2w['Vials'])
    playerSum = sum(session_data.account.alchemy_p2w['Player'])
    if isinstance(session_data.account.alchemy_p2w.get("Liquids"), list):
        # Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
        for liquidEntry in session_data.account.alchemy_p2w.get("Liquids"):
            if liquidEntry != -1:
                liquidCauldronSum += liquidEntry

    p2wSum = bubbleCauldronSum + liquidCauldronSum + vialsSum + playerSum
    p2wMax = bubbleCauldronMax + liquidCauldronMax + vialsMax + (highestAlchemyLevel * 2)
    p2wSumWithoutPlayer = bubbleCauldronSum + liquidCauldronSum + vialsSum
    p2wMaxWithoutPlayer = bubbleCauldronMax + liquidCauldronMax + vialsMax

    tier_P2WUpgrades = int(p2wSumWithoutPlayer >= p2wMaxWithoutPlayer)

    if p2wSum < p2wMax:
        if bubbleCauldronSum < bubbleCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(Advice(
                label="Bubble Cauldron Upgrades",
                picture_class="cauldron-a",
                progression=str(bubbleCauldronSum),
                goal=str(bubbleCauldronMax)
            ))
        if liquidCauldronSum < liquidCauldronMax:
            p2w_AdviceDict["Pay2Win"].append(Advice(
                label="Liquid Cauldron Upgrades",
                picture_class="bleach-liquid-cauldrons",
                progression=str(liquidCauldronSum),
                goal=str(liquidCauldronMax)
            ))
        if vialsSum < vialsMax:
            p2w_AdviceDict["Pay2Win"].append(Advice(
                label="Vial Upgrades",
                picture_class="vials",
                progression=str(vialsSum),
                goal=str(vialsMax)
            ))
        if playerSum < highestAlchemyLevel * 2:
            p2w_AdviceDict["Pay2Win"].append(Advice(
                label="Player Upgrades",
                picture_class="p2w-player",
                progression=str(playerSum),
                goal=str(highestAlchemyLevel * 2)
            ))
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
    overall_SectionTier = min(max_tier + info_tiers, tier_P2WUpgrades)
    return p2w_AdviceGroupDict, overall_SectionTier, max_tier, p2wSum, p2wMax

def getAlchemyP2WAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        p2w_AdviceSection = AdviceSection(
            name="Pay2Win",
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Alchemy skill in World 2!",
            picture="pay2win.png",
            unreached=True
        )
        return p2w_AdviceSection

    #Generate AdviceGroups
    p2w_AdviceGroupDict, overall_SectionTier, max_tier, p2wSum, p2wMax = getP2WProgressionTiersAdviceGroup(highestAlchemyLevel)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    header_upgrades = f"{p2wSum}/{p2wMax}"
    p2w_AdviceSection = AdviceSection(
        name="Pay2Win",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=(
            f"You've purchased all {p2wMax} upgrades in Alchemy's Pay 2 Win tab!{break_you_best}"
            if p2wSum >= p2wMax else (
                f"You've purchased {header_upgrades} upgrades in Alchemy's Pay 2 Win tab."
                f"<br>Try to purchase the basic upgrades before Mid W5, and Player upgrades after each Alchemy level up!"
            )
        ),
        picture="pay2win.png",
        groups=p2w_AdviceGroupDict.values()
    )
    return p2w_AdviceSection

def getSigilSpeedAdviceGroup() -> AdviceGroup:

    # 1 + (achievement, 0 or 20) + (Pea Pod sigil times Chilled Yarn artifact) + (20 * Gem Shop purchases) + (Willow Sippy (Equinox Log) vial * vialMastery) + (Sigil Stamp)
    # * multi(Summoning Winner Bonus: Green9 + Yellow5 + Blue5 + Purple7 + Cyan3)
    # * multi(Tuttle vial * vialMastery)
    # * multi(Bonus Ballot)

    # Multi Group A = several
    peapod_values = [0, 25, 50, 100]
    chilled_yarn_multi = [1, 2, 3, 4, 5]
    player_peapod_value = (
        peapod_values[session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']]
        * chilled_yarn_multi[session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']]
    )
    willow_vial_value = (
        session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']['Value']
        * session_data.account.vialMasteryMulti
        * session_data.account.labBonuses['My 1st Chemistry Set']['Value']
    )

    player_sigil_stamp_value = session_data.account.stamps['Sigil Stamp']['Value']
    goal_sigil_stamp_value = lavaFunc('decay', stamp_maxes['Sigil Stamp'], 40, 150)
    # The Sigil Stamp is a MISC stamp, thus isn't multiplied by the Lab bonus or Pristine Charm
    # if session_data.account.labBonuses['Certified Stamp Book']['Enabled']:
    #     player_sigil_stamp_value *= 2
    # if session_data.account.sneaking["PristineCharms"]["Liqorice Rolle"]:
    #     player_sigil_stamp_value *= 1.25

    mga = ValueToMulti(
        (20 * session_data.account.achievements['Vial Junkee']['Complete'])
        + (20 * session_data.account.gemshop['Sigil Supercharge'])
        + player_peapod_value
        + willow_vial_value
        + player_sigil_stamp_value
    )
    mga_label = f"Multi Group A: {mga:.3f}x"

    # Multi Group B = Summoning Winner Bonuses
    bd = session_data.account.summoning['BattleDetails']
    player_matches_total = (
        bd['Green'][9]['RewardBaseValue'] * bd['Green'][9]['Defeated']
        + bd['Yellow'][5]['RewardBaseValue'] * bd['Yellow'][5]['Defeated']
        + bd['Blue'][5]['RewardBaseValue'] * bd['Blue'][5]['Defeated']
        + bd['Purple'][7]['RewardBaseValue'] * bd['Green'][7]['Defeated']
        + bd['Cyan'][3]['RewardBaseValue'] * bd['Green'][3]['Defeated']
    )
    matches_total = (
        bd['Green'][9]['RewardBaseValue']
        + bd['Yellow'][5]['RewardBaseValue']
        + bd['Blue'][5]['RewardBaseValue']
        + bd['Purple'][7]['RewardBaseValue']
        + bd['Cyan'][3]['RewardBaseValue']
    )
    mgb = ValueToMulti(matches_total * session_data.account.summoning['WinnerBonusesMultiFull'])
    mgb_label = f"Multi Group B: {mgb:.3f}x"

    # Multi Group C = Tuttle Vial
    tuttle_vial_multi = ValueToMulti(
        session_data.account.alchemy_vials['Turtle Tisane (Tuttle)']['Value']
        * session_data.account.vialMasteryMulti
        * session_data.account.labBonuses['My 1st Chemistry Set']['Value']
    )
    mgc = tuttle_vial_multi
    mgc_label = f"Multi Group C: {mgc:.3f}x"

    # Multi Group D = Bonus Ballot
    ballot_active = session_data.account.ballot['CurrentBuff'] == 17
    if ballot_active:
        ballot_status = "is Active"
    elif not ballot_active and session_data.account.ballot['CurrentBuff'] != 0:
        ballot_status = "is Inactive"
    else:
        ballot_status = "status is not available in provided data"
    ballot_multi = ValueToMulti(session_data.account.ballot['Buffs'][17]['Value'])
    ballot_multi_active = max(1, ballot_multi * ballot_active)

    mgd = ballot_multi_active
    mgd_label = f"Multi Group D: {mgd:.3f}x"

    total_multi = max(1, mga * mgb * mgc * mgd)

    speed_Advice = {
        mga_label: [],
        mgb_label: [],
        mgc_label: [],
        mgd_label: [],
    }

    # Multi Group A
    speed_Advice[mga_label].append(Advice(
        label=f"W2 Achievement: Vial Junkee: "
              f"+{20 * session_data.account.achievements['Vial Junkee']['Complete']}/20%",
        picture_class="vial-junkee",
        progression=int(session_data.account.achievements['Vial Junkee']['Complete']),
        goal=1
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Gem Shop|#gem-shop }}}}: Sigil Supercharge: "
              f"+{20 * session_data.account.gemshop['Sigil Supercharge']}/{20 * 10}%",
        picture_class="sigil-supercharge",
        progression=session_data.account.gemshop['Sigil Supercharge'],
        goal=10
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"Sigil: Level {session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level']}"
              f" Pea Pod: +{player_peapod_value}/{peapod_values[-1] * chilled_yarn_multi[-1]}%",
        picture_class="pea-pod",
        progression=session_data.account.alchemy_p2w['Sigils']['Pea Pod']['Level'],
        goal=max_IndexOfSigils
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Artifact|#sailing}}}}: Chilled Yarn: {chilled_yarn_multi[session_data.account.sailing['Artifacts']['Chilled Yarn']['Level']]}"
              f"/{chilled_yarn_multi[-1]}x"
              f"<br>(Already applied to Pea Pod Sigil above)",
        picture_class="chilled-yarn",
        progression=session_data.account.sailing['Artifacts']['Chilled Yarn']['Level'],
        goal=numberOfArtifactTiers
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Willow Sippy (Willow Logs): +{willow_vial_value:.3f}",
        picture_class="willow-logs",
        progression=session_data.account.alchemy_vials['Willow Sippy (Willow Logs)']['Level'],
        goal=max_VialLevel
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"Lab Bonus: My 1st Chemistry Set: {session_data.account.labBonuses['My 1st Chemistry Set']['Value']}x"
              f"<br>(Already applied to Vial above)",
        picture_class="my-1st-chemistry-set",
        progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
        goal=1
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"{{{{ Rift|#rift }}}} Bonus: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}x"
              f"<br>(Already applied to Vial above)",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
    ))
    speed_Advice[mga_label].append(Advice(
        label=f"Sigil Stamp: +{player_sigil_stamp_value:.3f}/{goal_sigil_stamp_value:.3f}%",
        picture_class="sigil-stamp",
        progression=session_data.account.stamps['Sigil Stamp']['Level'],
        goal=stamp_maxes['Sigil Stamp'],
        resource=session_data.account.stamps['Sigil Stamp']['Material'],
    ))

    # Multi Group B
    for color, battleNumber in {"Green": 9, "Yellow": 5, "Blue": 5, "Purple": 7, "Cyan": 3}.items():
        speed_Advice[mgb_label].append(Advice(
            label=f"Summoning match {color} {battleNumber}: "
                  f"+{session_data.account.summoning['BattleDetails'][color][battleNumber]['RewardBaseValue'] * session_data.account.summoning['BattleDetails'][color][battleNumber]['Defeated']}"
                  f"/{session_data.account.summoning['BattleDetails'][color][battleNumber]['RewardBaseValue']}",
            picture_class=session_data.account.summoning['BattleDetails'][color][battleNumber]['Image'],
            progression=1 if session_data.account.summoning['BattleDetails'][color][battleNumber]['Defeated'] else 0,
            goal=1
        ))
    speed_Advice[mgb_label].append(Advice(
        label=f"Summoning matches total: +{player_matches_total}/{matches_total}",
        picture_class="summoning",
        progression=player_matches_total,
        goal=matches_total
    ))
    for advice in session_data.account.summoning['WinnerBonusesAdvice']:
        speed_Advice[mgb_label].append(advice)
    speed_Advice[mgb_label].extend(session_data.account.summoning['WinnerBonusesSummaryFull'])

    # Multi Group C
    speed_Advice[mgc_label].append(Advice(
        label=f"{{{{ Vial|#vials }}}}: Turtle Tisane (Tuttle): {tuttle_vial_multi:.3f}x",
        picture_class="tuttle",
        progression=session_data.account.alchemy_vials['Turtle Tisane (Tuttle)']['Level'],
        goal=max_VialLevel
    ))
    speed_Advice[mgc_label].append(Advice(
        label=f"Lab Bonus: My 1st Chemistry Set: {session_data.account.labBonuses['My 1st Chemistry Set']['Value']}x"
              f"<br>(Already applied to Vial above)",
        picture_class="my-1st-chemistry-set",
        progression=int(session_data.account.labBonuses['My 1st Chemistry Set']['Enabled']),
        goal=1
    ))
    speed_Advice[mgc_label].append(Advice(
        label=f"{{{{ Rift|#rift }}}} Bonus: Vial Mastery: {session_data.account.vialMasteryMulti:.2f}x"
              f"<br>(Already applied to Vial above)",
        picture_class="vial-mastery",
        progression=f"{1 if session_data.account.rift['VialMastery'] else 0}",
        goal=1
    ))

    # Multi Group D
    speed_Advice[mgd_label].append(Advice(
        label=f"Weekly {{{{ Ballot|#bonus-ballot }}}}: {ballot_multi_active:.3f}/{ballot_multi:.3f}x"
              f"<br>(Buff {ballot_status})",
        picture_class="ballot-17",
        progression=int(ballot_active),
        goal=1
    ))

    for group_name in speed_Advice:
        for advice in speed_Advice[group_name]:
            mark_advice_completed(advice)

    speed_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Info- Sources of Sigil Charging Speed. Grand total: {total_multi:.3f}x",
        advices=speed_Advice,
        informational=True,
    )
    return speed_AdviceGroup

def getSigilsProgressionTiersAdviceGroup():
    sigils_AdviceDict = {
        'Sigils': {}
    }
    infoTiers = 6
    max_tier = max(sigils_progressionTiers.keys()) - infoTiers
    tier_Sigils = 0
    account_sigils = session_data.account.alchemy_p2w['Sigils']

    # Assess Tiers
    for tierNumber, tierContents in sigils_progressionTiers.items():
        subgroupName = f"To reach {'Informational ' if tierNumber > max_tier else ''}Tier {tierNumber}"
        if 'Ionized Sigils' in tierContents.get('Other', {}) and not session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']:
            if subgroupName not in sigils_AdviceDict['Sigils'] and len(sigils_AdviceDict['Sigils']) < maxTiersPerGroup:
                sigils_AdviceDict['Sigils'][subgroupName] = []
            if subgroupName in sigils_AdviceDict['Sigils']:
                sigils_AdviceDict['Sigils'][subgroupName].append(Advice(
                    label=f"{{{{ Jade Emporium|#sneaking }}}}: Purchase Ionized Sigils to unlock Red sigils",
                    picture_class='ionized-sigils',
                    progression=int(session_data.account.sneaking['JadeEmporium']['Ionized Sigils']['Obtained']),
                    goal=1
                ))
        # Unlock new Sigils
        for requiredSigil, requiredLevel in tierContents.get('Unlock', {}).items():
            if account_sigils[requiredSigil]['PrechargeLevel'] < requiredLevel:
                if subgroupName not in sigils_AdviceDict['Sigils'] and len(sigils_AdviceDict['Sigils']) < maxTiersPerGroup:
                    sigils_AdviceDict['Sigils'][subgroupName] = []
                if subgroupName in sigils_AdviceDict['Sigils']:
                    sigils_AdviceDict['Sigils'][subgroupName].append(Advice(
                        label=f"Unlock {requiredSigil}",
                        picture_class=requiredSigil,
                        progression=f"{account_sigils[requiredSigil]['PlayerHours']:.2f}",
                        goal=f"{account_sigils[requiredSigil]['Requirements'][requiredLevel - 1]}"
                    ))
        # Level Up unlocked Sigils
        for requiredSigil, requiredLevel in tierContents.get('LevelUp', {}).items():
            if account_sigils[requiredSigil]['PrechargeLevel'] < requiredLevel:
                if subgroupName not in sigils_AdviceDict['Sigils'] and len(sigils_AdviceDict['Sigils']) < maxTiersPerGroup:
                    sigils_AdviceDict['Sigils'][subgroupName] = []
                if subgroupName in sigils_AdviceDict['Sigils']:
                    if account_sigils[requiredSigil]['PlayerHours'] < 100:
                        prog = f"{account_sigils[requiredSigil]['PlayerHours']:.2f}"
                    else:
                        prog = f"{account_sigils[requiredSigil]['PlayerHours']:.0f}"
                    sigils_AdviceDict['Sigils'][subgroupName].append(Advice(
                        label=f"Level up {requiredSigil}"
                              f"{'. Go look at the Sigils screen to redeem your level!' if account_sigils[requiredSigil]['PlayerHours'] > account_sigils[requiredSigil]['Requirements'][requiredLevel - 1] else ''}",
                        picture_class=f"{requiredSigil}-{requiredLevel}",
                        progression=f"{0 if requiredLevel > account_sigils[requiredSigil]['PrechargeLevel'] + 1 else prog}",
                        goal=f"{account_sigils[requiredSigil]['Requirements'][requiredLevel - 1]}"
                    ))
        if tier_Sigils == tierNumber - 1 and subgroupName not in sigils_AdviceDict['Sigils']:
            tier_Sigils = tierNumber

    # Generate AdviceGroups
    sigils_AdviceGroupDict = {}
    sigils_AdviceGroupDict['Sigils'] = AdviceGroup(
        tier=f"{tier_Sigils if tier_Sigils < max_tier else ''}",
        pre_string=f"{'Informational- ' if tier_Sigils >= max_tier else ''}"
                   f"Unlock and level {'all' if tier_Sigils >= max_tier else 'important'} Sigils",
        advices=sigils_AdviceDict['Sigils'],
        informational=tier_Sigils >= max_tier
    )
    overall_SectionTier = min(max_tier + infoTiers, tier_Sigils)
    return sigils_AdviceGroupDict, overall_SectionTier, max_tier

def getAlchemySigilsAdviceSection() -> AdviceSection:
    highestLabLevel = max(session_data.account.all_skills["Lab"])
    if highestLabLevel < 1:
        sigils_AdviceSection = AdviceSection(
            name='Sigils',
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Laboratory skill in World 4!",
            picture="Sigils.png",
            unreached=True
        )
        return sigils_AdviceSection
    sigils_AdviceGroupDict, overall_SectionTier, max_tier = getSigilsProgressionTiersAdviceGroup()
    sigils_AdviceGroupDict['Speed'] = getSigilSpeedAdviceGroup()

    # #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    sigils_AdviceSection = AdviceSection(
        name='Sigils',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Sigils tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Sigils.png",
        groups=sigils_AdviceGroupDict.values()
    )
    return sigils_AdviceSection
