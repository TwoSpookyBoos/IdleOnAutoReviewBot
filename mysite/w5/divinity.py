from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, divinity_progressionTiers, divinity_offeringsDict, divinity_stylesDict, getOfferingNameFromIndex, getStyleNameFromIndex, \
    getDivinityNameFromIndex

logger = get_logger(__name__)

divLevelReasonsDict = {
    0: "",
    2: "to activate Doot",
    40: "to unlock the TranQi Style.",
    50: "to unlock the Multitool Stamp from Poigu's quest."
}
divLinksDict = {
    0: [
        Advice(
            label="No Divinities unlocked to link to",
            picture_class=""
        )
    ],
    1: [
        Advice(
            label="No harm in linking everyone, as Snehebatu is your only choice",
            picture_class="snehebatu"
        )
    ],
    2: [
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        )
    ],
    3: [
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        )
    ],
    4: [
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        )
    ],
    5: [
        Advice(
            label="Move Meditators to Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        )
    ],
    6: [
        Advice(
            label="Move Meditators to Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        )
    ],
    7: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),

    ],
    8: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),
    ],
    9: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),
    ],
    10: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),
    ],
    11: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),
    ],
    12: [
        Advice(
            label="Beast Master, Voidwalker, or 3rd Archer are usual candidates",
            picture_class="purrmep"
        ),
        Advice(
            label="Meditators in Lab",
            picture_class="goharut"
        ),
        Advice(
            label="Lab bonuses fully online",
            picture_class="arctis"
        ),
        Advice(
            label="1 Map Pusher",
            picture_class="nobisect"
        ),
        Advice(
            label="Cooking BB generally wants Snake",
            picture_class="cooking-ladle"
        ),
        Advice(
            label="Extra characters can link to Snake if not Meditating",
            picture_class="snehebatu"
        ),
        Advice(
            label="Omniphau is a gamble. Refinery and 3D Printer rewards are nice- The other 4/6 are pretty meh.",
            picture_class="omniphau"
        ),
    ],

}

def getDivLevelReason(inputLevel: int) -> str:
    return divLevelReasonsDict.get(inputLevel, "")

def setDivinityProgressionTier():
    divinity_AdviceDict = {
        "TieredProgress": {},
        "Offerings": {"Available Offerings": [], "Strategy": []},
        "Styles": {"Highest Points per hour": [], "Highest EXP per hour": []},
        "Divinities": [],
        "DivinityLinks": [],
        "Dooted": [],
        "ArctisPoints": {}
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
    #playerDivinityList = session_data.account.divinity
    lowOffering = session_data.account.divinity['LowOffering']
    highOffering = session_data.account.divinity['HighOffering']

    #Assess Tiers
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
    for divDivinity in session_data.account.divinity['Divinities']:
        if session_data.account.divinity['Divinities'][divDivinity].get('Unlocked'):
            if session_data.account.divinity['Divinities'][divDivinity].get('BlessingLevel') < 100:
                divinity_AdviceDict["Divinities"].append(Advice(
                    label=f"{session_data.account.divinity['Divinities'][divDivinity].get('Name')} Blessing",
                    picture_class=session_data.account.divinity['Divinities'][divDivinity].get('Name'),
                    progression=session_data.account.divinity['Divinities'][divDivinity].get('BlessingLevel'),
                    goal=100
                ))

    #Offerings Info
    divinity_AdviceDict["Offerings"]["Available Offerings"].append(Advice(
        label=f"{divinity_offeringsDict.get(lowOffering, {}).get('Chance', 0)}% Offering: {getOfferingNameFromIndex(lowOffering)}",
        picture_class=divinity_offeringsDict.get(lowOffering, {}).get('Image', ''),
    ))
    divinity_AdviceDict["Offerings"]["Available Offerings"].append(Advice(
        label=f"{divinity_offeringsDict.get(highOffering, {}).get('Chance', 0)}% Offering: {getOfferingNameFromIndex(highOffering)}",
        picture_class=divinity_offeringsDict.get(highOffering, {}).get('Image', ''),
    ))
    divinity_AdviceDict["Offerings"]["Strategy"].append(Advice(
        label=f"Option 1: Choose the high offering if 100% Chance, otherwise choose low offering.",
        picture_class=divinity_offeringsDict.get(5, {}).get('Image', ''),
    ))
    divinity_AdviceDict["Offerings"]["Strategy"].append(Advice(
        label=f"Option 2: Always choose low offering and pray 🙏",
        picture_class=divinity_offeringsDict.get(0, {}).get('Image', ''),
    ))

    #Points Styles Info
    for divStyle in [7, 6, 2, 4, 1, 0]:
        if highestDivinitySkillLevel >= divinity_stylesDict[divStyle].get('UnlockLevel', 0):
            divinity_AdviceDict["Styles"]["Highest Points per hour"].append(Advice(
                label=f"{divinity_stylesDict[divStyle].get('Points', 0)}/hr: {getStyleNameFromIndex(divStyle)}",
                picture_class=getStyleNameFromIndex(divStyle),
            ))

    #EXP Styles Info
    for divStyle in [7, 6, 4, 5, 1, 3, 2, 0]:
        if highestDivinitySkillLevel >= divinity_stylesDict[divStyle].get('UnlockLevel', 0):
            divinity_AdviceDict["Styles"]["Highest EXP per hour"].append(Advice(
                label=f"{divinity_stylesDict[divStyle].get('Exp', 0)}/hr: {getStyleNameFromIndex(divStyle)} {divinity_stylesDict[divStyle].get('Notes','')}",
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
    else:
        divinity_AdviceDict["DivinityLinks"] = divLinksDict.get(int(tier_Divinity), [])
    #     divinity_AdviceDict["Dooted"].append(Advice(
    #         label=f"Doot not owned, bummer 💔",
    #         picture_class="king-doot"
    #     ))

    #Big P + Divinity level thresholds for Arctis minor link
    bigPBreakpointsList = [540, 940, 1440, 1940, 2440, 2940, 5940]
    arctisCombosDict = {
        540:  {90: 14,  109: 15},
        940:  {87: 14,  105: 15,  128: 16},
        1440: {85: 14,  103: 15,  126: 16, 156: 17, 197: 18},
        1940:          {102: 15,  124: 16, 153: 17, 194: 18},
        2440:          {101: 15,  123: 16, 152: 17, 193: 18},
        2940:                    {123: 16, 152: 17, 192: 18},
        5940:                    {122: 16, 150: 17, 189: 18}
    }
    lowestBigPToShow = 540
    currentLowestArctisValue = 0
    #Find the lowest Big P threshold the account has already reached. This will be the first entry shown
    for bigPLevel in arctisCombosDict:
        if session_data.account.alchemy_bubbles['Big P']['Level'] >= bigPLevel:
            lowestBigPToShow = bigPLevel
    #Find the next Big P threshold they could meet
    if lowestBigPToShow <= session_data.account.alchemy_bubbles['Big P']['Level']:
        try:
            nextBigPTarget = bigPBreakpointsList[bigPBreakpointsList.index(lowestBigPToShow)+1]
        except:
            nextBigPTarget = 0
    else:
        nextBigPTarget = lowestBigPToShow

    for bigPLevel in arctisCombosDict:
        if bigPLevel >= lowestBigPToShow:
            divinity_AdviceDict["ArctisPoints"][f"Big P level {bigPLevel}"] = []  #Create subgroup
            #Find the Arctis Value of the lowest div-level character in the account. Don't show entries below or equal to this.
            for divinityLevel in arctisCombosDict[bigPLevel]:
                if lowestDivinitySkillLevel >= divinityLevel and bigPLevel <= session_data.account.alchemy_bubbles['Big P']['Level']:
                    if arctisCombosDict[bigPLevel][divinityLevel] > currentLowestArctisValue:
                        currentLowestArctisValue = arctisCombosDict[bigPLevel][divinityLevel]
    for bigPLevel in arctisCombosDict:
        subgroupName = f"Big P level {bigPLevel}"
        if subgroupName in divinity_AdviceDict["ArctisPoints"]:
            if bigPLevel == lowestBigPToShow and nextBigPTarget != 0:
                divinity_AdviceDict["ArctisPoints"][subgroupName].append(Advice(
                    label=f"Current Big P bubble level",
                    picture_class='big-p',
                    progression=session_data.account.alchemy_bubbles['Big P']['Level'],
                    goal=nextBigPTarget
                ))
            for divinityLevel in arctisCombosDict[bigPLevel]:
                if arctisCombosDict[bigPLevel][divinityLevel] > currentLowestArctisValue:  #Strictly greater than
                    divinity_AdviceDict["ArctisPoints"][subgroupName].append(Advice(
                        label=f"+{arctisCombosDict[bigPLevel][divinityLevel]} at Divinity Level {divinityLevel}",
                        picture_class='divinity',
                        progression=lowestDivinitySkillLevel,
                        goal=divinityLevel
                    ))
    #Generate AdviceGroups
    divinity_AdviceGroupDict["TieredProgress"] = AdviceGroup(
        tier=str(tier_Divinity),
        pre_string="Complete objectives to reach the next Divinity tier",
        advices=divinity_AdviceDict["TieredProgress"]
    )
    divinity_AdviceGroupDict["Offerings"] = AdviceGroup(
        tier="",
        pre_string="Offerings Information",
        advices=divinity_AdviceDict["Offerings"]
    )
    divinity_AdviceGroupDict["DivinityLinks"] = AdviceGroup(
        tier="",
        pre_string="Possible Divinity Link Setups",
        advices=divinity_AdviceDict["DivinityLinks"]
    )
    divinity_AdviceGroupDict["Divinities"] = AdviceGroup(
        tier="",
        pre_string="Blessings Information",
        advices=divinity_AdviceDict["Divinities"]
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
    divinity_AdviceGroupDict["Dooted"] = AdviceGroup(
        tier="",
        pre_string="Arctis minor link bonus (+# Talent LV for all talents above Lv 1) breakpoints. Progress shown is your LOWEST divinity level",
        advices=divinity_AdviceDict["ArctisPoints"]
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
