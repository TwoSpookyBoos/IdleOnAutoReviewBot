from math import ceil

from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import (maxTiersPerGroup, divinity_progressionTiers, divinity_offeringsDict, divinity_stylesDict,
                    getOfferingNameFromIndex, getStyleNameFromIndex, getDivinityNameFromIndex, divLevelReasonsDict, divinity_arctisBreakpoints, break_you_best)

logger = get_logger(__name__)


def getDivLevelReason(inputLevel: int) -> str:
    return divLevelReasonsDict.get(inputLevel, "")

def getOfferingsAdviceGroup():
    offerings_AdviceDict = {
        "Available Offerings": [],
        "Strategy": []
    }
    lowOffering = session_data.account.divinity['LowOffering']
    highOffering = session_data.account.divinity['HighOffering']
    divinityPoints = session_data.account.divinity['DivinityPoints']
    lowOfferingGoal = session_data.account.divinity['LowOfferingGoal']
    highOfferingGoal = session_data.account.divinity['HighOfferingGoal']

    offerings_AdviceDict["Available Offerings"].append(Advice(
        label=f"{divinity_offeringsDict.get(lowOffering, {}).get('Chance', 1)}% Offering: {getOfferingNameFromIndex(lowOffering)}",
        picture_class=divinity_offeringsDict.get(lowOffering, {}).get('Image', ''),
        progression=f"{divinityPoints / max(1, lowOfferingGoal):.2%}",
        #goal=lowOfferingGoal
    ))
    offerings_AdviceDict["Available Offerings"].append(Advice(
        label=f"{divinity_offeringsDict.get(highOffering, {}).get('Chance', 1)}% Offering: {getOfferingNameFromIndex(highOffering)}",
        picture_class=divinity_offeringsDict.get(highOffering, {}).get('Image', ''),
        progression=f"{divinityPoints / max(1, highOfferingGoal):.2%}",
        #goal=highOfferingGoal
    ))
    offerings_AdviceDict["Strategy"].append(Advice(
        label=f"Option 1: Choose the high offering if 100% Chance, otherwise choose low offering.",
        picture_class=divinity_offeringsDict.get(5, {}).get('Image', ''),
    ))
    offerings_AdviceDict["Strategy"].append(Advice(
        label=f"Option 2: Always choose low offering and pray 🙏",
        picture_class=divinity_offeringsDict.get(0, {}).get('Image', ''),
    ))
    offerings_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Offerings Information",
        advices=offerings_AdviceDict,
        informational=True
    )
    return offerings_AdviceGroup

def getBlessingsAdviceGroup():
    blessings_AdviceList = []

    for divDivinity in session_data.account.divinity['Divinities']:
        if session_data.account.divinity['Divinities'][divDivinity].get('Unlocked'):
            if session_data.account.divinity['Divinities'][divDivinity].get('BlessingLevel') < 100:
                blessings_AdviceList.append(Advice(
                    label=f"{session_data.account.divinity['Divinities'][divDivinity].get('Name')} Blessing",
                    picture_class=session_data.account.divinity['Divinities'][divDivinity].get('Name'),
                    progression=session_data.account.divinity['Divinities'][divDivinity].get('BlessingLevel'),
                    goal=100,
                    resource=session_data.account.divinity['Divinities'][divDivinity].get('BlessingMaterial')
                ))

    blessings_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Blessings Information",
        advices=blessings_AdviceList,
        informational=True
    )
    return blessings_AdviceGroup

def getStylesInfoAdviceGroup(highestDivinitySkillLevel: int) -> AdviceGroup:
    styles_AdviceDict = {
        "Highest Points per hour": [],
        "Highest EXP per hour": []
    }
    # Points Styles Info
    for divStyle in [7, 6, 2, 4, 1, 0]:
        if highestDivinitySkillLevel >= divinity_stylesDict[divStyle].get('UnlockLevel', 0):
            styles_AdviceDict["Highest Points per hour"].append(Advice(
                label=f"{divinity_stylesDict[divStyle].get('Points', 0)}/hr: {getStyleNameFromIndex(divStyle)}",
                picture_class=getStyleNameFromIndex(divStyle),
            ))

    # EXP Styles Info
    for divStyle in [7, 6, 4, 5, 1, 3, 2, 0]:
        if highestDivinitySkillLevel >= divinity_stylesDict[divStyle].get('UnlockLevel', 0):
            styles_AdviceDict["Highest EXP per hour"].append(Advice(
                label=f"{divinity_stylesDict[divStyle].get('Exp', 0)}/hr: {getStyleNameFromIndex(divStyle)} {divinity_stylesDict[divStyle].get('Notes', '')}",
                picture_class=getStyleNameFromIndex(divStyle),
            ))

    styles_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Styles Information",
        advices=styles_AdviceDict,
        informational=True,
        completed=True
    )
    return styles_AdviceGroup

def getDootChecksAdviceGroups(lowestDivinitySkillLevel: int, highestDivinitySkillLevel: int):
    doot_AdviceList = []
    if not session_data.account.doot_owned:
        if session_data.account.divinity['Divinities'][2].get("Unlocked", False):
            # If you don't own Doot but do have Arctis unlocked, generate Alert if any character has no divinity link
            for character in session_data.account.all_characters:
                if character.divinity_link == "Unlinked":
                    session_data.account.alerts_AdviceDict['World 5'].append(Advice(
                        label=f"{character.character_name} isn't linked to a {{{{ Divinity|#divinity }}}}",
                        picture_class=character.class_name_icon,
                        completed=False
                    ))
    #     doot_AdviceList.append(Advice(
    #         label=f"Doot not owned, bummer 💔",
    #         picture_class="king-doot"
    #     ))
    else:
        doot_AdviceList.append(Advice(
            label=f"Doot owned. Congrats 🙄",
            picture_class="king-doot",
            completed=True
        ))
        if lowestDivinitySkillLevel < 2:
            for character in session_data.account.safe_characters:
                if character.divinity_level < 2:
                    doot_AdviceList.append(Advice(
                        label=f"{character.character_name} needs to level their Divinity once to get Doot's bonus!",
                        picture_class=character.class_name_icon,
                        completed=False
                    ))
        # else:
        #     doot_AdviceList.append(Advice(
        #         label=f"All current characters have 2+ Divinity. Doot's bonus is active for all current characters!",
        #         picture_class="divinity"
        #     ))

        if session_data.account.divinity['Divinities'][7].get("Unlocked", False):
            purrmepAssignedToAnyHighestCharacter = False
            divLevelOfPurrmepLinkedCharacter = 0
            highestCharactersNotAssignedToPurrmep = []
            for character in session_data.account.safe_characters:
                if character.divinity_link == "Purrmep":
                    divLevelOfPurrmepLinkedCharacter = character.divinity_level
                    if character.divinity_level == highestDivinitySkillLevel:
                        purrmepAssignedToAnyHighestCharacter = True
            if not purrmepAssignedToAnyHighestCharacter:
                for character in session_data.account.safe_characters:
                    if character.divinity_level == highestDivinitySkillLevel and character.divinity_link != "Purrmep":
                        highestCharactersNotAssignedToPurrmep.append(character)
            if not purrmepAssignedToAnyHighestCharacter:
                if highestDivinitySkillLevel < 100 and highestDivinitySkillLevel - divLevelOfPurrmepLinkedCharacter >= 10:
                    doot_AdviceList.append(Advice(
                        label=f"""Relink to {pl(highestCharactersNotAssignedToPurrmep,
                                                f'{highestCharactersNotAssignedToPurrmep[0].character_name}',
                                                'one of these characters')}"""
                              f" to maximize Purrmep's Minor Link bonus by {highestDivinitySkillLevel - divLevelOfPurrmepLinkedCharacter} "
                              f"levels{pl(highestCharactersNotAssignedToPurrmep, '.', ':')}",
                        picture_class="purrmep"
                    ))
                    if len(highestCharactersNotAssignedToPurrmep) > 1:
                        for character in highestCharactersNotAssignedToPurrmep:
                            doot_AdviceList.append(Advice(
                                label=character.character_name,
                                picture_class=character.class_name_icon,
                                completed=False
                            ))
        if len(doot_AdviceList) == 1:
            # If the only Advice in the list is the sarcastic "Grats for owning Doot", don't show this group
            doot_AdviceList = []
            # doot_AdviceList.append(Advice(
            #     label=f"No Doot-related issues found. Way to be a responsible Doot owner!",
            #     picture_class=""
            # ))

    doot_AdviceGroup = AdviceGroup(
        tier="",
        pre_string="Doot-Specific Checks",
        advices=doot_AdviceList,
        informational=True
    )

    return doot_AdviceGroup

def getArctisAdviceGroup(lowestDivinitySkillLevel: int, highestDivinitySkillLevel: int) -> AdviceGroup:
    arctis_AdviceDict = {"Current Values": []}
    current_big_p = session_data.account.alchemy_bubbles['Big P']['Level']

    # Find the lowest minor link bonus from Arctis across all characters, as if they were linked
    currentLowestArctisValue = 0
    currentHighestArctisValue = 0
    for char in session_data.account.all_characters:
        char_arctis = ceil(15 * session_data.account.alchemy_bubbles['Big P']['BaseValue'] * (char.divinity_level / (char.divinity_level + 60)))
        if currentLowestArctisValue == 0:  #First character being evaluated
            currentLowestArctisValue = char_arctis
            currentHighestArctisValue = char_arctis
        else:
            currentLowestArctisValue = min(currentLowestArctisValue, char_arctis)
            currentHighestArctisValue = max(currentHighestArctisValue, char_arctis)

    # Populate the Current Values list with Arctis, Div levels, and Big P bubble so players know their starting points
    arctis_AdviceDict["Current Values"].append(Advice(
        label=f"Arctis minor link ranges: +{currentLowestArctisValue} - +{currentHighestArctisValue}",
        picture_class="arctis"
    ))
    arctis_AdviceDict["Current Values"].append(Advice(
        label=f"Divinity level ranges: {lowestDivinitySkillLevel} - {highestDivinitySkillLevel}",
        picture_class="divinity"
    ))
    arctis_AdviceDict["Current Values"].append(Advice(
        label=f"Big P bubble level: {current_big_p}",
        picture_class="big-p"
    ))

    for arctis_breakpoint, requirementsDict in divinity_arctisBreakpoints.items():
        any_completed_big_p_goal = False
        for div_level, big_p_level in requirementsDict.items():
            if arctis_breakpoint > currentLowestArctisValue:  #At least 1 above their minimum
                if (
                    (div_level == max(requirementsDict.keys(), default=1) and f"Arctis +{arctis_breakpoint}" not in arctis_AdviceDict)
                    or (div_level >= lowestDivinitySkillLevel and big_p_level >= current_big_p)
                    or (not any_completed_big_p_goal and big_p_level <= current_big_p)
                ):
                    if (
                        f"Arctis +{arctis_breakpoint}" not in arctis_AdviceDict
                        and (
                            arctis_breakpoint <= currentHighestArctisValue + 1
                            or arctis_breakpoint == min(divinity_arctisBreakpoints.keys())
                        )
                    ):  #No more than 1 above their max, unless they're still under the lowest breakpoint I entered
                        arctis_AdviceDict[f"Arctis +{arctis_breakpoint}"] = []
                    if f"Arctis +{arctis_breakpoint}" in arctis_AdviceDict and not any_completed_big_p_goal:
                        arctis_AdviceDict[f"Arctis +{arctis_breakpoint}"].append(Advice(
                            label=f"{div_level} Divinity and {big_p_level} Big P",
                            picture_class="arctis",
                            progression=current_big_p,
                            goal=big_p_level
                        ))
                        if big_p_level <= current_big_p:
                            any_completed_big_p_goal = True

    for subgroupAL in arctis_AdviceDict.values():
        for advice in subgroupAL:
            mark_advice_completed(advice)

    arctis_AdviceGroup = AdviceGroup(
        tier="",
        pre_string=f"Upcoming Arctis minor link bonus breakpoints"
                   f" (+# Talent LV for all talents above Lv 1)",
        advices=arctis_AdviceDict,
        informational=True,
        completed=len(arctis_AdviceDict) == 1  #When Current Values is the only subgroup
    )
    arctis_AdviceGroup.remove_empty_subgroups()

    return arctis_AdviceGroup

def getDivinityProgressionTierAdviceGroups(lowestDivinitySkillLevel, highestDivinitySkillLevel):
    divinity_AdviceDict = {
        "TieredProgress": {},
    }
    divinity_AdviceGroupDict = {}
    tier_Divinity = 0
    info_tiers = 0
    max_tier = max(divinity_progressionTiers.keys()) - info_tiers

    # Assess Tiers
    for tierLevel, tierRequirements in divinity_progressionTiers.items():
        anyRequirementFailed = False
        subgroupName = f"To reach Tier {tierLevel}"
        if session_data.account.divinity['GodsUnlocked'] < tierRequirements.get('GodsUnlocked', 0):
            anyRequirementFailed = True
            if subgroupName not in divinity_AdviceDict['TieredProgress'] and len(divinity_AdviceDict['TieredProgress']) < maxTiersPerGroup:
                divinity_AdviceDict['TieredProgress'][subgroupName] = []
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Unlock {getDivinityNameFromIndex(tierRequirements.get('GodsUnlocked', 0))}",
                    picture_class=getDivinityNameFromIndex(tierRequirements.get('GodsUnlocked', 0)),
                    progression=0,
                    goal=1
                ))
        if highestDivinitySkillLevel < tierRequirements.get('MaxDivLevel', 0):
            anyRequirementFailed = True
            if subgroupName not in divinity_AdviceDict['TieredProgress'] and len(divinity_AdviceDict['TieredProgress']) < maxTiersPerGroup:
                divinity_AdviceDict['TieredProgress'][subgroupName] = []
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Raise any character's Divinity level to {tierRequirements.get('MaxDivLevel', 0)} {getDivLevelReason(tierRequirements.get('MaxDivLevel', 0))}",
                    picture_class="divinity",
                    completed=False
                ))
        if lowestDivinitySkillLevel < tierRequirements.get('MinDivLevel', 0):
            anyRequirementFailed = True
            if subgroupName not in divinity_AdviceDict['TieredProgress'] and len(divinity_AdviceDict['TieredProgress']) < maxTiersPerGroup:
                divinity_AdviceDict['TieredProgress'][subgroupName] = []
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                for character in session_data.account.safe_characters:
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
    divinity_AdviceGroupDict["Dooted"] = getDootChecksAdviceGroups(lowestDivinitySkillLevel, highestDivinitySkillLevel)

    overall_SectionTier = min(max_tier + info_tiers, tier_Divinity)
    return divinity_AdviceGroupDict, overall_SectionTier, max_tier

def getDivinityAdviceSection() -> AdviceSection:
    highestDivinitySkillLevel = max(session_data.account.all_skills.get("Divinity", [0]))
    lowestDivinitySkillLevel = min(session_data.account.all_skills.get("Divinity", [0]))
    if highestDivinitySkillLevel < 1:
        divinity_AdviceSection = AdviceSection(
            name="Divinity",
            tier="",
            pinchy_rating=0,
            header="Come back after unlocking the Divinity skill in W5!",
            picture="Divinity.png",
            unreached=True
        )
        return divinity_AdviceSection

    # Generate AdviceGroups
    divinity_AdviceGroupDict, overall_SectionTier, max_tier = getDivinityProgressionTierAdviceGroups(lowestDivinitySkillLevel, highestDivinitySkillLevel)
    divinity_AdviceGroupDict["Offerings"] = getOfferingsAdviceGroup()
    divinity_AdviceGroupDict["Blessings"] = getBlessingsAdviceGroup()
    divinity_AdviceGroupDict["Styles"] = getStylesInfoAdviceGroup(highestDivinitySkillLevel)
    divinity_AdviceGroupDict["Arctis"] = getArctisAdviceGroup(lowestDivinitySkillLevel, highestDivinitySkillLevel)

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    divinity_AdviceSection = AdviceSection(
        name="Divinity",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Divinity tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Divinity.png",
        groups=divinity_AdviceGroupDict.values()
    )
    return divinity_AdviceSection
