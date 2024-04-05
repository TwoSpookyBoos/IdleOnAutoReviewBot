import json
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import divinity_progressionTiers

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
    0: {
        "Name": "Snehebatu",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    1: {
        "Name": "Arctis",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    2: {
        "Name": "Nobisect",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    3: {
        "Name": "Harriep",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    4: {
        "Name": "Goharut",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    5: {
        "Name": "Omniphau",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    6: {
        "Name": "Purrmep",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    7: {
        "Name": "Flutterbis",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    8: {
        "Name": "Kattlekruk",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
    9: {
        "Name": "Bagur",
        "Unlocked": False,
        "BlessingLevel": 0,
    },
}

def getOfferingNameFromIndex(inputValue):
    return offeringsDict.get(inputValue, {"Name": f"UnknownOffering{inputValue}"}).get("Name")

def getStyleNameFromIndex(inputValue):
    return stylesDict.get(inputValue, {"Name": f"UnknownStyle{inputValue}"}).get("Name")

def getDivinityNameFromIndex(inputValue):
    return divinitiesDict.get(inputValue, {"Name": f"UnknownDivinity{inputValue}"}).get("Name")

def parseJSONtoList():
    rawDivinity = session_data.account.raw_data.get("Divinity", [])
    if isinstance(rawDivinity, str):
        rawDivinity = json.loads(rawDivinity)
    while len(rawDivinity) < 40:
        rawDivinity.append(0)
    return rawDivinity

def setDivinityProgressionTier():
    divinity_AdviceDict = {
        "OfferingsTester": [],
        "StyleTester": [],
        "DivinityTester": [],
    }
    divinity_AdviceGroupDict = {}
    divinity_AdviceSection = AdviceSection(
        name="Divinity",
        tier="0",
        pinchy_rating=0,
        header="Best Divinity tier met: Not Yet Evaluated",
        picture=""
    )
    highestDivinitySkillLevel = max(session_data.account.all_skills.get("Divinity", [0]))
    if highestDivinitySkillLevel < 1:
        divinity_AdviceSection.header = "Come back after unlocking the Divinity skill in W5!"
        return divinity_AdviceSection

    lowestDivinitySkillLevel = min(session_data.account.all_skills.get("Divinity", [0]))
    tier_Divinity = 0
    max_tier = max(divinity_progressionTiers.keys())
    playerDivinityList = parseJSONtoList()
    godRank = playerDivinityList[25]-10 if playerDivinityList[25] > 10 else 0

    for divinityIndex in divinitiesDict:
        #playerDivinityList[25] = total number of gods unlocked. God Ranks are also included here. 13 would mean 10 gods + 3 god rank
        if playerDivinityList[25] > divinityIndex:
            divinitiesDict[divinityIndex]["Unlocked"] = True
        #Snake has a divinityIndex of 0, Blessing level stored in 28
        divinitiesDict[divinityIndex]["BlessingLevel"] = playerDivinityList[divinityIndex+28]
    for character in session_data.account.safe_characters:
        try:
            character.setDivinityStyle(getStyleNameFromIndex(playerDivinityList[character.character_index]))
            character.setDivinityLink(getDivinityNameFromIndex(playerDivinityList[character.character_index+12]))
        except Exception as reason:
            logger.warning(f"Could not retrieve Divinity Style for Character{character.character_index} because {reason}")

    for offering in offeringsDict:
        divinity_AdviceDict["OfferingsTester"].append(Advice(
            label=f"{offeringsDict[offering].get('Chance', 0)}% Offering: {getOfferingNameFromIndex(offering)}",
            picture_class=offeringsDict[offering].get('Image'),
        ))

    for divStyle in stylesDict:
        divinity_AdviceDict["StyleTester"].append(Advice(
            label=getStyleNameFromIndex(divStyle),
            picture_class=getStyleNameFromIndex(divStyle),
        ))

    for divDivinity in divinitiesDict:
        if divinitiesDict[divDivinity].get('Unlocked'):
            status = f"Blessing Level: {divinitiesDict[divDivinity].get('BlessingLevel')}/100"
        else:
            status = "Locked"
        divinity_AdviceDict["DivinityTester"].append(Advice(
            label=f"{divinitiesDict[divDivinity].get('Name')} {status}",
            picture_class=divinitiesDict[divDivinity].get('Name')
        ))
    divinity_AdviceDict["DivinityTester"].append(Advice(
        label=f"God Rank: {godRank}",
        picture_class="gods-chosen-children"
    ))

    #Generate AdviceGroups
    divinity_AdviceGroupDict["OfferingsTester"] = AdviceGroup(
        tier="",
        pre_string="Offerings Tester",
        advices=divinity_AdviceDict["OfferingsTester"]
    )
    divinity_AdviceGroupDict["StyleTester"] = AdviceGroup(
        tier="",
        pre_string="Style Tester",
        advices=divinity_AdviceDict["StyleTester"]
    )
    divinity_AdviceGroupDict["DivinityTester"] = AdviceGroup(
        tier="",
        pre_string="Divinity Tester",
        advices=divinity_AdviceDict["DivinityTester"]
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
