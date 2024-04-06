import json
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import divinity_progressionTiers, maxTiersPerGroup

logger = get_logger(__name__)
offeringsDict = {
    0: {
        "Name":"Olive Branch",
        "Image":"offering-1",
        "Chance":1,
    },
    1: {
        "Name": "Incense",
        "Image": "offering-5",
        "Chance": 5,
    },
    2: {
        "Name": "Giftbox",
        "Image": "offering-10",
        "Chance": 10,
    },
    3: {
        "Name": "Tithe",
        "Image": "offering-25",
        "Chance": 25,
    },
    4: {
        "Name": "Hearty Meal",
        "Image": "offering-50",
        "Chance": 50,
    },
    5: {
        "Name": "Sacrifice",
        "Image": "offering-100",
        "Chance": 100,
    },
}
stylesDict = {
    0: {
        "Name": "Kinesis",
        "UnlockLevel": 1,
        "Points": 1,
        "Exp": 1,
    },
    1: {
        "Name": "Chakra",
        "UnlockLevel": 5,
        "Points": 2,
        "Exp": 2,
    },
    2: {
        "Name": "Focus",
        "UnlockLevel": 10,
        "Points": 4,
        "Exp": 1,
    },
    3: {
        "Name": "Mantra",
        "UnlockLevel": 15,
        "Points": 0,
        "Exp": 1,
        "Notes": "(To all characters)"
    },
    4: {
        "Name": "Vitalic",
        "UnlockLevel": 25,
        "Points": 2,
        "Exp": 7,
    },
    5: {
        "Name": "TranQi",
        "UnlockLevel": 40,
        "Points": 0,
        "Exp": 3,
        "Notes": "(Even when not Meditating)"
    },
    6: {
        "Name": "Zen",
        "UnlockLevel": 60,
        "Points": 8,
        "Exp": 8,
    },
    7: {
        "Name": "Mindful",
        "UnlockLevel": 80,
        "Points": 15,
        "Exp": 10,
    },
}
divinitiesDict = {
    1: {
        "Name": "Snehebatu",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    2: {
        "Name": "Arctis",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    3: {
        "Name": "Nobisect",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    4: {
        "Name": "Harriep",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    5: {
        "Name": "Goharut",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    6: {
        "Name": "Omniphau",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    7: {
        "Name": "Purrmep",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    8: {
        "Name": "Flutterbis",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    9: {
        "Name": "Kattlekruk",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    10: {
        "Name": "Bagur",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
}
divLevelReasonsDict = {
    0: "",
    2: "to activate Doot",
    40: "to unlock the TranQi Style.",
    50: "to unlock the Multitool Stamp from Poigu's quest."
}

def getOfferingNameFromIndex(inputValue):
    return offeringsDict.get(inputValue, {"Name": f"UnknownOffering{inputValue}"}).get("Name")

def getStyleNameFromIndex(inputValue: int) -> str:
    return stylesDict.get(inputValue, {"Name": f"UnknownStyle{inputValue}"}).get("Name")

def getDivinityNameFromIndex(inputValue: int) -> str:
    return divinitiesDict.get(inputValue, {"Name": f"UnknownDivinity{inputValue}"}).get("Name")

def getDivLevelReason(inputLevel: int) -> str:
    return divLevelReasonsDict.get(inputLevel, "")

def parseJSONtoList():
    rawDivinity = session_data.account.raw_data.get("Divinity", [])
    if isinstance(rawDivinity, str):
        rawDivinity = json.loads(rawDivinity)
    while len(rawDivinity) < 40:
        rawDivinity.append(0)
    return rawDivinity

def setDivinityProgressionTier():
    divinity_AdviceDict = {
        "TieredProgress": {},
        "Offerings": {"Available Offerings": [], "Strategy": []},
        "Styles": {"Highest Points per hour": [], "Highest EXP per hour": []},
        "Divinities": [],
        "Dooted": [],
    }
    divinity_AdviceGroupDict = {}
    divinity_AdviceSection = AdviceSection(
        name="Divinity",
        tier="0",
        pinchy_rating=0,
        header="Best Divinity tier met: Not Yet Evaluated",
        picture="Divinity.png"
    )
    highestDivinitySkillLevel = max(session_data.account.all_skills.get("Divinity", [0]))
    if highestDivinitySkillLevel < 1:
        divinity_AdviceSection.header = "Come back after unlocking the Divinity skill in W5!"
        return divinity_AdviceSection

    lowestDivinitySkillLevel = min(session_data.account.all_skills.get("Divinity", [0]))
    tier_Divinity = 0
    max_tier = max(divinity_progressionTiers.keys())
    playerDivinityList = parseJSONtoList()
    godsUnlocked = min(10, playerDivinityList[25])
    godRank = playerDivinityList[25]-10 if playerDivinityList[25] > 10 else 0
    lowOffering = playerDivinityList[26]
    highOffering = playerDivinityList[27]

    for divinityIndex in divinitiesDict:
        #playerDivinityList[25] = total number of gods unlocked. God Ranks are also included here. 13 would mean 10 gods + 3 god rank
        if playerDivinityList[25] >= divinityIndex:
            divinitiesDict[divinityIndex]["Unlocked"] = True
        #Snake has a divinityIndex of 0, Blessing level stored in 28
        divinitiesDict[divinityIndex]["BlessingLevel"] = playerDivinityList[divinityIndex+27]
    for character in session_data.account.safe_characters:
        try:
            character.setDivinityStyle(getStyleNameFromIndex(playerDivinityList[character.character_index]))
            character.setDivinityLink(getDivinityNameFromIndex(playerDivinityList[character.character_index+12]))
        except Exception as reason:
            logger.warning(f"Could not retrieve Divinity Style for Character{character.character_index} because {reason}")

    #Assess Tiers
    for tierLevel, tierRequirements in divinity_progressionTiers.items():
        anyRequirementFailed = False
        subgroupName = f"To reach Tier {tierLevel}"
        if godsUnlocked < tierRequirements.get('GodsUnlocked', 0):
            anyRequirementFailed = True
            if subgroupName not in divinity_AdviceDict['TieredProgress'] and len(divinity_AdviceDict['TieredProgress']) < maxTiersPerGroup:
                divinity_AdviceDict['TieredProgress'][subgroupName] = []
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Unlock {getDivinityNameFromIndex(tierRequirements.get('GodsUnlocked', 0))}",
                    picture_class=getDivinityNameFromIndex(tierRequirements.get('GodsUnlocked', 0)),
                ))
        if highestDivinitySkillLevel < tierRequirements.get('MaxDivLevel', 0):
            anyRequirementFailed = True
            if subgroupName not in divinity_AdviceDict['TieredProgress'] and len(divinity_AdviceDict['TieredProgress']) < maxTiersPerGroup:
                divinity_AdviceDict['TieredProgress'][subgroupName] = []
            if subgroupName in divinity_AdviceDict['TieredProgress']:
                divinity_AdviceDict['TieredProgress'][subgroupName].append(Advice(
                    label=f"Raise any character's Divinity level to {tierRequirements.get('MaxDivLevel', 0)} {getDivLevelReason(tierRequirements.get('MaxDivLevel', 0))}",
                    picture_class="divinity",
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
                        ))
        if not anyRequirementFailed and tier_Divinity == tierLevel-1:
            tier_Divinity = tierLevel

    # Divinities Info
    for divDivinity in divinitiesDict:
        if divinitiesDict[divDivinity].get('Unlocked'):
            if divinitiesDict[divDivinity].get('BlessingLevel') < 100:
                status = f"Blessing Level: {divinitiesDict[divDivinity].get('BlessingLevel')}/100"
                divinity_AdviceDict["Divinities"].append(Advice(
                    label=f"{divinitiesDict[divDivinity].get('Name')} Blessing",
                    picture_class=divinitiesDict[divDivinity].get('Name'),
                    progression=divinitiesDict[divDivinity].get('BlessingLevel'),
                    goal=100
                ))
        # else:
        #     status = "Locked"
    # if godsUnlocked >= 10:
    #     divinity_AdviceDict["Divinities"].append(Advice(
    #         label=f"God Rank: {godRank}",
    #         picture_class="gods-chosen-children"
    #     ))

    #Offerings Info
    divinity_AdviceDict["Offerings"]["Available Offerings"].append(Advice(
        label=f"{offeringsDict[lowOffering].get('Chance', 0)}% Offering: {getOfferingNameFromIndex(lowOffering)}",
        picture_class=offeringsDict[lowOffering].get('Image'),
    ))
    divinity_AdviceDict["Offerings"]["Available Offerings"].append(Advice(
        label=f"{offeringsDict[highOffering].get('Chance', 0)}% Offering: {getOfferingNameFromIndex(highOffering)}",
        picture_class=offeringsDict[highOffering].get('Image'),
    ))
    divinity_AdviceDict["Offerings"]["Strategy"].append(Advice(
        label=f"Option 1: Choose the high offering if 100% Chance, otherwise choose low offering.",
        picture_class=offeringsDict[5].get('Image'),
    ))
    divinity_AdviceDict["Offerings"]["Strategy"].append(Advice(
        label=f"Option 2: Always choose low offering and pray 🙏",
        picture_class=offeringsDict[0].get('Image'),
    ))

    #Points Styles Info
    for divStyle in [7, 6, 2, 4, 1, 0]:
        if highestDivinitySkillLevel >= stylesDict[divStyle].get('UnlockLevel', 0):
            divinity_AdviceDict["Styles"]["Highest Points per hour"].append(Advice(
                label=f"{stylesDict[divStyle].get('Points', 0)}/hr: {getStyleNameFromIndex(divStyle)}",
                picture_class=getStyleNameFromIndex(divStyle),
            ))

    #EXP Styles Info
    for divStyle in [7, 6, 4, 5, 1, 3, 2, 0]:
        if highestDivinitySkillLevel >= stylesDict[divStyle].get('UnlockLevel', 0):
            divinity_AdviceDict["Styles"]["Highest EXP per hour"].append(Advice(
                label=f"{stylesDict[divStyle].get('Exp', 0)}/hr: {getStyleNameFromIndex(divStyle)} {stylesDict[divStyle].get('Notes','')}",
                picture_class=getStyleNameFromIndex(divStyle),
            ))

    #Doot Checks Info
    if session_data.account.doot_owned:
        divinity_AdviceDict["Dooted"].append(Advice(
            label=f"Doot owned. Congrats 🙄",
            picture_class="king-doot"
        ))
        if lowestDivinitySkillLevel < 2:
            for character in session_data.account.safe_characters:
                if character.divinity_level < 2:
                    divinity_AdviceDict["Dooted"].append(Advice(
                        label=f"{character.character_name} needs to level their Divinity once to get Doot's bonus!",
                        picture_class=character.class_name_icon
                    ))
        # else:
        #     divinity_AdviceDict["Dooted"].append(Advice(
        #         label=f"All current characters have 2+ Divinity. Doot's bonus is active for all current characters!",
        #         picture_class="divinity"
        #     ))
        if divinitiesDict[6].get("Unlocked", False):
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
                if highestDivinitySkillLevel < 120 and highestDivinitySkillLevel - divLevelOfPurrmepLinkedCharacter >= 10:
                    divinity_AdviceDict["Dooted"].append(Advice(
                        label=f"Relink to {pl(highestCharactersNotAssignedToPurrmep, f'{highestCharactersNotAssignedToPurrmep[0].character_name}', 'one of these characters')} to maximize Purrmep's Minor Link bonus by {highestDivinitySkillLevel - divLevelOfPurrmepLinkedCharacter} levels{pl(highestCharactersNotAssignedToPurrmep, '.', ':')}",
                        picture_class="purrmep"
                    ))
                if len(highestCharactersNotAssignedToPurrmep) > 1:
                    for character in highestCharactersNotAssignedToPurrmep:
                        divinity_AdviceDict["Dooted"].append(Advice(
                            label=character.character_name,
                            picture_class=character.class_name_icon
                        ))
        if len(divinity_AdviceDict["Dooted"]) == 1:
            divinity_AdviceDict["Dooted"] = []
            # divinity_AdviceDict["Dooted"].append(Advice(
            #     label=f"No Doot-related issues found. Way to be a responsible Doot owner",
            #     picture_class=""
            # ))
    # else:
    #     divinity_AdviceDict["Dooted"].append(Advice(
    #         label=f"Doot not owned, bummer 💔",
    #         picture_class="king-doot"
    #     ))

    #Generate AdviceGroups
    divinity_AdviceGroupDict["TieredProgress"] = AdviceGroup(
        tier=str(tier_Divinity),
        pre_string="Complete objectives to reach the next Divinity tier",
        advices=divinity_AdviceDict["TieredProgress"]
    )
    divinity_AdviceGroupDict["Divinities"] = AdviceGroup(
        tier="",
        pre_string="Blessings Information",
        advices=divinity_AdviceDict["Divinities"]
    )
    divinity_AdviceGroupDict["Offerings"] = AdviceGroup(
        tier="",
        pre_string="Offerings Information",
        advices=divinity_AdviceDict["Offerings"]
    )
    divinity_AdviceGroupDict["Styles"] = AdviceGroup(
        tier="",
        pre_string="Styles Information",
        advices=divinity_AdviceDict["Styles"]
    )

    divinity_AdviceGroupDict["Dooted"] = AdviceGroup(
        tier="",
        pre_string="Doot-Specific Checks",
        advices=divinity_AdviceDict["Dooted"]
    )
    
    #Generate AdviceSection
    overall_DivinityTier = min(max_tier, tier_Divinity)
    tier_section = f"{overall_DivinityTier}/{max_tier}"
    divinity_AdviceSection.tier = tier_section
    divinity_AdviceSection.pinchy_rating = overall_DivinityTier
    divinity_AdviceSection.groups = divinity_AdviceGroupDict.values()
    if overall_DivinityTier == max_tier:
        divinity_AdviceSection.header = f"Best Divinity tier met: {tier_section}<br>You best ❤️"
    else:
        divinity_AdviceSection.header = f"Best Divinity tier met: {tier_section}"

    return divinity_AdviceSection
