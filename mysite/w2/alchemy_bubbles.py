

from consts.consts_autoreview import build_subgroup_label, break_you_best
from consts.consts_w2 import min_NBLB, max_NBLB, at_risk_basic_bubbles, atrisk_advanced_bubbles, atrisk_lithium_bubbles, atrisk_lithium_advanced_bubbles, \
    bubble_cauldron_color_list, nblb_skippable, nblb_max_index
from consts.consts_w4 import cooking_close_enough
from consts.w6.farming import max_farming_crops
from consts.progression_tiers import bubbles_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot


def getBubbleExclusions():
    exclusionsList = []
    #If all crops owned or Evolution GMO is level 10+, exclude the requirement for Cropius Mapper
    if session_data.account.farming.crops.unlocked >= max_farming_crops or session_data.account.farming.market['Evolution Gmo'].level > 20:
        exclusionsList.append('Cropius Mapper')

    #If cooking is nearly finished, exclude Diamond Chef
    if session_data.account.cooking['MaxRemainingMeals'] < cooking_close_enough:
        exclusionsList.append('Diamond Chef')

    return exclusionsList


def getAtRiskBubblesAdviceGroups() -> list[AdviceGroup]:
    low_skip = 150
    high_skip = 300
    standard_today = "Basic - In Today's Range"
    standard = 'Basic Skilling Resources'
    advanced_today = "Advanced - In Today's Range"
    advanced = 'Advanced Resources'
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
    sorted_bubbles_basic = [(k, v) for k, v in sorted_bubbles if min_NBLB <= v['Level'] < max_NBLB and v['BubbleIndex'] <= 14]
    basic_prestring = ''
    lithium_prestring = ''
    basic_poststring = ''
    if sorted_bubbles_basic and max(session_data.account.all_skills['Laboratory'], default=0) > 1:
        try:
            todays_lowest = sorted_bubbles_basic[0][1]['Level']
            todays_highest = sorted_bubbles_basic[nblbCount - 1][1]['Level']
        except:
            todays_lowest = sorted_bubbles_basic[0][1]['Level']
            todays_highest = sorted_bubbles_basic[-1][1]['Level']
        if len(sorted_bubbles_basic) > 1:
            basic_poststring = f"Today's W1-W3 NBLB range: {todays_lowest} - {todays_highest}"
        for bubbleName, bubbleValuesDict in sorted_bubbles_basic:
            if (
                bubbleValuesDict['Level'] < todays_highest + 20
                or todays_lowest >= low_skip
                or todays_highest >= high_skip
            ):
                if bubbleName in at_risk_basic_bubbles:
                    if bubbleValuesDict['Level'] <= todays_highest:
                        subgroupName = standard_today
                    else:
                        subgroupName = standard
                elif bubbleName in atrisk_advanced_bubbles:
                    if bubbleValuesDict['Level'] <= todays_highest:
                        subgroupName = advanced_today
                    else:
                        subgroupName = advanced
                else:
                    subgroupName = ''

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
            basic_prestring = f"\"Easy\" to obtain materials in W1-W3 bubbles"
            lithium_prestring = f"Slower to obtain materials in W4-W5 bubbles"
        else:
            basic_prestring = f"\"Easy\" to obtain materials in your {2 * nblbCount} lowest leveled W1-W3 bubbles"
            lithium_prestring = f"Slower to obtain materials in your {nblbCount} lowest leveled W4-W5 bubbles"

    atriskBasic_AG = AdviceGroup(
        tier='',
        pre_string=basic_prestring,
        advices=atriskBasic_AdviceList,
        post_string=basic_poststring,
        informational=True
    )

    #Same thing, but for Lithium Bubbles W4-W5 now
    #Lithium only works on W4 and W5 bubbles, indexes 15 through 24
    sorted_bubbles_lithium = [(k, v) for k, v in sorted_bubbles if min_NBLB <= v['Level'] < max_NBLB and 15 <= v['BubbleIndex'] <= 24]
    #lithium_prestring = ''
    lithium_poststring = ''
    if sorted_bubbles_lithium and max(session_data.account.all_skills['Laboratory'], default=0) > 1:
        try:
            todays_lowest_lithium = sorted_bubbles_lithium[0][1]['Level']
            todays_highest_lithium = sorted_bubbles_lithium[nblbCount - 1][1]['Level']
        except:
            todays_lowest_lithium = sorted_bubbles_lithium[0][1]['Level']
            todays_highest_lithium = sorted_bubbles_lithium[-1][1]['Level']
        lithium_poststring = f"Today's W4-W5 (Lithium) range: {todays_lowest_lithium} - {todays_highest_lithium}"
        for bubbleName, bubbleValuesDict in sorted_bubbles_lithium:
            if (
                bubbleValuesDict['Level'] < todays_highest_lithium + 10
                or len(atriskBasic_AdviceList) > 0
            ):
                if bubbleName in atrisk_lithium_bubbles:
                    if bubbleValuesDict['Level'] <= todays_highest_lithium:
                        subgroupName = standard_today
                    else:
                        subgroupName = standard
                elif bubbleName in atrisk_lithium_advanced_bubbles:
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
        tier='',
        pre_string=lithium_prestring,
        advices=atriskLithium_AdviceList if session_data.account.atom_collider['Atoms']['Lithium - Bubble Insta Expander']['Level'] >= 1 else [],
        post_string=lithium_poststring,
        informational=True
    )
    atriskBasic_AG.remove_empty_subgroups()
    atriskLithium_AG.remove_empty_subgroups()
    return [atriskBasic_AG, atriskLithium_AG]


def getBubblesProgressionTiersAdviceGroup():
    bubble_Advices = {
        'Unlock And Level': {
            # 'No Bubble Left Behind': []
        },
        'Purple Sample Bubbles': {},
        'Orange Sample Bubbles': {},
        'Green Sample Bubbles': {},
        'Utility Bubbles': {},
    }
    bubbles_AdviceGroupDict = {}

    optional_tiers = 3
    true_max = true_max_tiers['Bubbles']
    max_tier = true_max - optional_tiers
    tier_TotalBubblesUnlocked = 0
    exclusions_list = getBubbleExclusions()

    per_cauldron_bubbles_unlocked = [
        session_data.account.alchemy_cauldrons['OrangeUnlocked'],
        session_data.account.alchemy_cauldrons['GreenUnlocked'],
        session_data.account.alchemy_cauldrons['PurpleUnlocked'],
        session_data.account.alchemy_cauldrons['YellowUnlocked']
    ]
    sum_total_bubbles_unlocked = session_data.account.alchemy_cauldrons['TotalUnlocked']
    next_world_missing_bubbles = session_data.account.alchemy_cauldrons['NextWorldMissingBubbles']

    requirementsMet = [True, True, True, True]
    bubble_type_list = ['Orange Sample Bubbles', 'Green Sample Bubbles', 'Purple Sample Bubbles', 'Utility Bubbles']
    bubble_tiers = [0, 0, 0, 0]
    cauldron_images = [f"cauldron-{_[0]}" for _ in bubble_cauldron_color_list]

    # Assess tiers
    for tier in bubbles_progressionTiers:
        # tier[0] = int tier
        # tier[1] = int TotalBubblesUnlocked
        # tier[2] = dict {Orange Sample Bubbles}
        # tier[3] = dict {Green Sample Bubbles}
        # tier[4] = dict {Purple Sample Bubbles}
        # tier[5] = dict {Utility Bubbles}
        # tier[6] = str BubbleValuePercentage
        # tier[7] = str Orange, Green, Purple Notes
        # tier[8] = str Utility Notes (Not used atm)

        subgroup_label = build_subgroup_label(tier[0], max_tier)

        # tier_TotalBubblesUnlocked
        if sum_total_bubbles_unlocked < tier[1]:
            if (
                subgroup_label not in bubble_Advices['Unlock And Level']
                and len(bubble_Advices['Unlock And Level']) < session_data.account.max_subgroups
            ):
                bubble_Advices['Unlock And Level'][subgroup_label] = [(
                    Advice(
                        label=f"Unlock {tier[1]} total bubbles",
                        picture_class='alchemy',
                        progression=sum_total_bubbles_unlocked,
                        goal=tier[1]
                    )
                )]
            if subgroup_label in bubble_Advices['Unlock And Level']:
                for cauldron_index, unlocked_bubbles in enumerate(per_cauldron_bubbles_unlocked):
                    if unlocked_bubbles < (5 * next_world_missing_bubbles):
                        bubble_Advices['Unlock And Level'][subgroup_label].append(Advice(
                            label=f"W{next_world_missing_bubbles} {bubble_cauldron_color_list[cauldron_index]} Bubbles Unlocked",
                            picture_class=cauldron_images[cauldron_index],
                            progression=unlocked_bubbles - (5 * (next_world_missing_bubbles - 1)),
                            goal=5
                        ))
        if subgroup_label not in bubble_Advices['Unlock And Level'] and tier_TotalBubblesUnlocked == tier[0] - 1:
            tier_TotalBubblesUnlocked = tier[0]

        # Orange, Green, Purple, and Utility bubbles
        for type_index, bubble_type in enumerate(bubble_type_list):
            for required_bubble in tier[type_index + 2]:
                if required_bubble not in exclusions_list:
                    if session_data.account.alchemy_bubbles[required_bubble]['Level'] < tier[type_index + 2][required_bubble]:
                        requirementsMet[type_index] = False
                        subgroup_including_percent_label = f"{subgroup_label}{f' ({tier[6]})' if bubble_type != 'Utility Bubbles' else ''}"
                        add_subgroup_if_available_slot(bubble_Advices[bubble_type], subgroup_including_percent_label)
                        if subgroup_including_percent_label in bubble_Advices[bubble_type]:
                            printing = session_data.account.alchemy_bubbles[required_bubble]['Material'] in session_data.account.printer['AllCurrentPrints']
                            bubble_Advices[bubble_type][subgroup_including_percent_label].append(Advice(
                                label=f"{required_bubble}{' (Printing!)' if printing else ''}",
                                picture_class=required_bubble,
                                progression=session_data.account.alchemy_bubbles[required_bubble]['Level'],
                                goal=tier[type_index + 2][required_bubble],
                                resource=session_data.account.alchemy_bubbles[required_bubble]['Material']
                            )),
            if bubble_tiers[type_index] == (tier[0] - 1) and requirementsMet[type_index] == True:  # Only update if they already met the previous tier
                bubble_tiers[type_index] = tier[0]
    
    # Check for any bubbles below min_NBLB range that ought to be bumped into range
    bubble_Advices['Unlock And Level']['No Bubble Left Behind'] = []
    for bubbleName, bubbleDetails in session_data.account.alchemy_bubbles.items():
        if (
            0 < bubbleDetails['Level'] < min_NBLB
            and bubbleName not in nblb_skippable
            and bubbleDetails['BubbleIndex'] <= nblb_max_index
        ):
            bubble_Advices['Unlock And Level']['No Bubble Left Behind'].append(Advice(
                label=bubbleName,
                picture_class=bubbleName,
                progression=bubbleDetails['Level'],
                goal=min_NBLB,
                resource=bubbleDetails['Material'],
            ))

    # Generate AdviceGroups
    ag_names = ['Unlock And Level', 'Orange Sample Bubbles', 'Green Sample Bubbles', 'Purple Sample Bubbles', 'Utility Bubbles']
    agd_tiers = [tier_TotalBubblesUnlocked, bubble_tiers[0], bubble_tiers[1], bubble_tiers[2], bubble_tiers[3]]
    agd_pre_strings = [
        f'Continue unlocking W{next_world_missing_bubbles} bubbles and bringing worthwhile bubbles into No Bubble Left Behind range',
        'Level Orange sample-boosting bubbles',
        'Level Green sample-boosting bubbles',
        'Level Purple sample-boosting bubbles',
        'Level Utility bubbles',
    ]
    for counter, value in enumerate(ag_names):
        bubbles_AdviceGroupDict[value] = AdviceGroup(
            tier=agd_tiers[counter],
            pre_string=agd_pre_strings[counter],
            advices=bubble_Advices[value],
        )
        bubbles_AdviceGroupDict[value].remove_empty_subgroups()

    overall_SectionTier = min(
        true_max, tier_TotalBubblesUnlocked,
        bubble_tiers[0], bubble_tiers[1], bubble_tiers[2], bubble_tiers[3]
    )
    return bubbles_AdviceGroupDict, overall_SectionTier, max_tier, true_max


def getAlchemyBubblesAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills["Alchemy"])
    if highestAlchemyLevel < 1:
        bubbles_AdviceSection = AdviceSection(
            name='Bubbles',
            tier="Not Yet Evaluated",
            header="Come back after unlocking the Alchemy skill in World 2!",
            picture="Alchemy_Bubble_all.gif",
            unreached=True
        )
        return bubbles_AdviceSection

    #Generate AdviceGroups
    bubbles_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getBubblesProgressionTiersAdviceGroup()
    bubbles_AdviceGroupDict['AtRiskBasic'], bubbles_AdviceGroupDict['AtRiskLithium'] = getAtRiskBubblesAdviceGroups()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    bubbles_AdviceSection = AdviceSection(
        name='Bubbles',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Bubbles tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Alchemy_Bubble_all.gif',
        groups=bubbles_AdviceGroupDict.values(),
    )

    return bubbles_AdviceSection
