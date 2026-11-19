from math import ceil

from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.text_formatting import pl, notateNumber
from utils.logging import get_logger

from consts.consts_autoreview import (
    break_you_best, EmojiType
)
from consts.w5.divinity import (
    divinity_arctis_breakpoints,
    divinity_level_reasons,
    divinity_offerings,
)
from consts.progression_tiers import divinity_progressionTiers, true_max_tiers

logger = get_logger(__name__)


def getDivLevelReason(inputLevel: int) -> str:
    return divinity_level_reasons.get(inputLevel, "")

def getOfferingsAdviceGroup():
    offerings_Advices = {
        'Available Offerings': [],
        'Strategy': []
    }
    divinity = session_data.account.divinity
    divinity_points = divinity.points

    try:
        offerings_Advices['Available Offerings'].append(Advice(
            label=f"Divinity Points: {notateNumber('Basic', divinity_points, 2)}",
            picture_class='divinity'
        ))
    except:
        pass

    offerings_Advices["Available Offerings"].extend(divinity.get_offering_advices())
    offerings_Advices["Strategy"].append(
        Advice(
            label="Option 1: Choose the high offering if 100% Chance, "
            "otherwise choose low offering.",
            picture_class=divinity_offerings[5]["Image"],
        )
    )
    offerings_Advices["Strategy"].append(
        Advice(
            label=f"Option 2: Always choose low offering and pray "
            f"{EmojiType.PRAY.value}",
            picture_class=divinity_offerings[0]["Image"],
        )
    )

    for subgroup in offerings_Advices:
        for advice in offerings_Advices[subgroup]:
            advice.mark_advice_completed()

    offerings_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Offerings',
        advices=offerings_Advices,
        informational=True,
        completed=session_data.account.divinity.gods_unlocked >= 10
    )
    return offerings_AdviceGroup

def getBlessingsAdviceGroup():
    blessings_AdviceList = []

    for god in session_data.account.divinity.values():
        if god.unlocked and god.blessing.level < 100:
            blessings_AdviceList.append(god.blessing.get_advice())

    blessings_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Unmaxed Blessings',
        advices=blessings_AdviceList,
        informational=True
    )
    return blessings_AdviceGroup

def getStylesInfoAdviceGroup(highest_divinity_level: int) -> AdviceGroup:
    styles_AdviceDict = session_data.account.divinity.get_style_advices(
        highest_divinity_level
    )
    styles_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Unlocked Styles',
        advices=styles_AdviceDict,
        informational=True,
        completed=True
    )
    return styles_AdviceGroup

def getDootChecksAdviceGroups(lowest_divinity_level: int, highest_divinity_level: int):
    doot_Advices = []
    if not session_data.account.companions.has('King Doot'):
        if session_data.account.divinity[2].unlocked:
            # If you don't own Doot but do have Arctis unlocked, generate Alert if any char has no divinity link
            for char in session_data.account.characters:
                if char.divinity_link == 'Unlinked':
                    session_data.account.alerts_Advices['World 5'].append(Advice(
                        label=f"{char.character_name} isn't linked to a {{{{ Divinity|#divinity }}}}",
                        picture_class=char.class_name_icon,
                        completed=False
                    ))
    else:
        doot_Advices.append(Advice(
            label='Doot owned. Congrats',
            picture_class='king-doot',
            completed=True
        ))
        if lowest_divinity_level < 2:
            for char in session_data.account.characters.safe:
                if char.divinity_level < 2:
                    doot_Advices.append(Advice(
                        label=f"{char.character_name} needs to level their Divinity once to get Doot's bonus!",
                        picture_class=char.class_name_icon,
                        completed=False
                    ))

        if session_data.account.divinity[7].unlocked:
            purrmep_assigned_to_any_highest_character = False
            div_level_of_purrmep_linked_character = 0
            highest_characters_not_assigned_to_purrmep = []
            for char in session_data.account.characters.safe:
                if char.divinity_link == 'Purrmep':
                    div_level_of_purrmep_linked_character = char.divinity_level
                    if char.divinity_level == highest_divinity_level:
                        purrmep_assigned_to_any_highest_character = True
            if not purrmep_assigned_to_any_highest_character:
                for char in session_data.account.characters.safe:
                    if char.divinity_level == highest_divinity_level and char.divinity_link != "Purrmep":
                        highest_characters_not_assigned_to_purrmep.append(char)
            if not purrmep_assigned_to_any_highest_character:
                if highest_divinity_level < 100 and highest_divinity_level - div_level_of_purrmep_linked_character >= 10:
                    doot_Advices.append(Advice(
                        label=(
                            f"""Relink to {pl(highest_characters_not_assigned_to_purrmep,
                                              f'{highest_characters_not_assigned_to_purrmep[0].character_name}',
                                              'one of these characters')}"""
                              f" to maximize Purrmep's Minor Link bonus by {highest_divinity_level - div_level_of_purrmep_linked_character} "
                              f"levels{pl(highest_characters_not_assigned_to_purrmep, '.', ':')}"
                        ),
                        picture_class='purrmep'
                    ))
                    if len(highest_characters_not_assigned_to_purrmep) > 1:
                        for char in highest_characters_not_assigned_to_purrmep:
                            doot_Advices.append(Advice(
                                label=char.character_name,
                                picture_class=char.class_name_icon,
                                completed=False
                            ))
        if len(doot_Advices) == 1:
            # If the only Advice in the list is the sarcastic "Grats for owning Doot", don't show this group
            doot_Advices = []


    doot_AdviceGroup = AdviceGroup(
        tier='',
        pre_string='Doot-Specific Checks',
        advices=doot_Advices,
        informational=True
    )

    return doot_AdviceGroup

def getArctisAdviceGroup(lowest_divinity_level: int, highest_divinity_level: int) -> AdviceGroup:
    arctis_Advices = {
        'Current Values': []
    }
    current_big_p = session_data.account.alchemy_bubbles['Big P'].level

    # Find the lowest minor link bonus from Arctis across all characters, as if they were linked
    current_lowest_arctis_value = 0
    current_highest_arctis_value = 0
    for char in session_data.account.characters:
        char_arctis = ceil(15 * session_data.account.alchemy_bubbles['Big P'].base_value * (char.divinity_level / (char.divinity_level + 60)))
        if current_lowest_arctis_value == 0:  #First character being evaluated
            current_lowest_arctis_value = char_arctis
            current_highest_arctis_value = char_arctis
        else:
            current_lowest_arctis_value = min(current_lowest_arctis_value, char_arctis)
            current_highest_arctis_value = max(current_highest_arctis_value, char_arctis)

    # Populate the Current Values list with Arctis, Div levels, and Big P bubble so players know their starting points
    arctis_Advices['Current Values'].append(Advice(
        label=f"Arctis minor link ranges: +{current_lowest_arctis_value} - +{current_highest_arctis_value}",
        picture_class='arctis',
        completed=True
    ))
    arctis_Advices["Current Values"].append(Advice(
        label=f"Divinity level ranges: {lowest_divinity_level} - {highest_divinity_level}",
        picture_class='divinity',
        completed=True
    ))
    arctis_Advices["Current Values"].append(Advice(
        label=f"Big P bubble level: {current_big_p}",
        picture_class='big-p',
        completed=True
    ))

    for arctis_breakpoint, requirementsDict in divinity_arctis_breakpoints.items():
        any_completed_big_p_goal = False
        for div_level, big_p_level in requirementsDict.items():
            if arctis_breakpoint > current_lowest_arctis_value:  #At least 1 above their minimum
                if (
                    (div_level == max(requirementsDict.keys(), default=1) and f"Arctis +{arctis_breakpoint}" not in arctis_Advices)
                    or (div_level >= lowest_divinity_level and big_p_level >= current_big_p)
                    or (not any_completed_big_p_goal and big_p_level <= current_big_p)
                ):
                    if (
                        f"Arctis +{arctis_breakpoint}" not in arctis_Advices
                        and (
                            arctis_breakpoint <= current_highest_arctis_value + 1
                            or arctis_breakpoint == min(divinity_arctis_breakpoints.keys())
                        )
                    ):  #No more than 1 above their max, unless they're still under the lowest breakpoint I entered
                        arctis_Advices[f"Arctis +{arctis_breakpoint}"] = []
                    if f"Arctis +{arctis_breakpoint}" in arctis_Advices and not any_completed_big_p_goal:
                        arctis_Advices[f"Arctis +{arctis_breakpoint}"].append(Advice(
                            label=f"{div_level} Divinity and {big_p_level} Big P",
                            picture_class='arctis',
                            progression=current_big_p,
                            goal=big_p_level
                        ))
                        if big_p_level <= current_big_p:
                            any_completed_big_p_goal = True

    for subgroup in arctis_Advices:
        for advice in arctis_Advices[subgroup]:
            advice.mark_advice_completed()

    arctis_AdviceGroup = AdviceGroup(
        tier='',
        pre_string=f"Upcoming Arctis minor link bonus breakpoints"
                   f" (+# Talent LV for all talents above Lv 1)",
        post_string='Note: Bonus talent levels are rounded up to a whole number. +11.01 will truly give you +12',
        advices=arctis_Advices,
        informational=True
    )
    arctis_AdviceGroup.remove_empty_subgroups()

    return arctis_AdviceGroup

def getDivinityProgressionTierAdviceGroups(lowest_divinity_level, highest_divinity_level):
    divinity_AdviceDict = {
        'TieredProgress': {},
    }
    divinity_AdviceGroupDict = {}
    tier_Divinity = 0
    optional_tiers = 0
    true_max = true_max_tiers['Divinity']
    max_tier = true_max - optional_tiers

    # Assess Tiers
    for tierLevel, tierRequirements in divinity_progressionTiers.items():
        anyRequirementFailed = False
        subgroupName = f"To reach Tier {tierLevel}"
        if session_data.account.divinity.gods_unlocked < tierRequirements.get('GodsUnlocked', 0):
            anyRequirementFailed = True
            add_subgroup_if_available_slot(divinity_AdviceDict['TieredProgress'], subgroupName)
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                god = session_data.account.divinity[tierRequirements['GodsUnlocked']]
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Unlock {god.name}",
                    picture_class=god.name,
                    progression=0,
                    goal=1
                ))
        if highest_divinity_level < tierRequirements.get('MaxDivLevel', 0):
            anyRequirementFailed = True
            add_subgroup_if_available_slot(divinity_AdviceDict['TieredProgress'], subgroupName)
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Raise any character's Divinity level to {tierRequirements.get('MaxDivLevel', 0)} {getDivLevelReason(tierRequirements.get('MaxDivLevel', 0))}",
                    picture_class="divinity",
                    completed=False
                ))
        if lowest_divinity_level < tierRequirements.get('MinDivLevel', 0):
            anyRequirementFailed = True
            add_subgroup_if_available_slot(divinity_AdviceDict['TieredProgress'], subgroupName)
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                for character in session_data.account.characters.safe:
                    if character.divinity_level < tierRequirements.get('MinDivLevel', 0):
                        divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                            label=f"Raise {character.character_name}'s Divinity level to {tierRequirements.get('MinDivLevel', 0)} {getDivLevelReason(tierRequirements.get('MinDivLevel', 0))}",
                            picture_class=f"{character.class_name_icon}",
                            completed=False
                        ))
        if not anyRequirementFailed and tier_Divinity == tierLevel - 1:
            tier_Divinity = tierLevel

    # Generate AdviceGroups
    divinity_AdviceGroupDict["TieredProgress"] = AdviceGroup(
        tier=str(tier_Divinity),
        pre_string="Complete objectives to reach the next Divinity tier",
        advices=divinity_AdviceDict["TieredProgress"]
    )
    divinity_AdviceGroupDict["Dooted"] = getDootChecksAdviceGroups(lowest_divinity_level, highest_divinity_level)

    overall_SectionTier = min(true_max, tier_Divinity)
    return divinity_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getDivinityAdviceSection() -> AdviceSection:
    highest_divinity_level = max(session_data.account.characters.all_skills.get('Divinity', [0]))
    lowest_divinity_level = min(session_data.account.characters.all_skills.get('Divinity', [0]))
    if highest_divinity_level < 1:
        divinity_AdviceSection = AdviceSection(
            name='Divinity',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking the Divinity skill in W5!',
            picture='Divinity.png',
            unreached=True
        )
        return divinity_AdviceSection

    # Generate AdviceGroups
    divinity_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getDivinityProgressionTierAdviceGroups(lowest_divinity_level, highest_divinity_level)
    divinity_AdviceGroupDict['Offerings'] = getOfferingsAdviceGroup()
    divinity_AdviceGroupDict['Blessings'] = getBlessingsAdviceGroup()
    divinity_AdviceGroupDict['Styles'] = getStylesInfoAdviceGroup(highest_divinity_level)
    divinity_AdviceGroupDict['Arctis'] = getArctisAdviceGroup(lowest_divinity_level, highest_divinity_level)

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    divinity_AdviceSection = AdviceSection(
        name='Divinity',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Divinity tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Divinity.png',
        groups=divinity_AdviceGroupDict.values()
    )
    return divinity_AdviceSection
