import json
from idleon_SkillLevels import getSpecificSkillLevelsList
from models import AdviceSection, AdviceGroup, Advice
from utils import pl

def getCritterName(inputNumber):
    reversedCritterIndexList = ["Blobfish", "Honker", "Dung Beat", "Bunny", "Pingy", "Owlio", "Mousey", "Scorpie", "Crabbo", "Froge", "None"]
    try:
        return reversedCritterIndexList[-inputNumber]
    except:
        return "UnknownCritterName"

def getUnlockedCritterStatus(inputJSON, playerCount):
    reversedCritterIndexList = ["Blobfish", "Honker", "Dung Beat", "Bunny", "Pingy", "Owlio", "Mousey", "Scorpie", "Crabbo", "Froge", "None"]
    reversedQuestIndexList = ["Blobbo2","Lord_of_the_Hunt10", "Lord_of_the_Hunt9", "Lord_of_the_Hunt8", "Lord_of_the_Hunt7", "Lord_of_the_Hunt6", "Lord_of_the_Hunt5", "Lord_of_the_Hunt4", "Lord_of_the_Hunt3", "Lord_of_the_Hunt2"]
    reversedRequiredStatusQuestIndexList = [1,0,0,0,0,0,0,0,0,0,0]
    highestCritter = (len(reversedCritterIndexList)-1)
    #Critters available to be trapped can be found by quest status.
    #["QuestComplete_0"] through _9 are dictionaries.
    #Keys are "Lord_of_the_Hunt2" through 10. Values are 1 for completed, 0 for in progress I think, and -1 for not started.
    #1 = buy a trap set quest, irrelevant
    #Lord_of_the_Hunt2 = Froge
    #3 = Crabbo
    #4 = Scorpie
    #5 = Mousey
    #6 = Owlio
    #7 = Pingy
    #8 = Bunny
    #9 = Dung Beat
    #10 = Honker when quest is STARTED (value of 0 or 1)
    #11 = the trophy quest, irrelevant
    #Blobfish are unlocked after "Blobbo2" quest is completed (value of 1)

    playerIndex = 0
    questIndex = 0
    while playerIndex < playerCount:
        try:
            questDict = json.loads(inputJSON[("QuestComplete_"+str(playerIndex))])
            while questIndex < len(reversedQuestIndexList):
                if (questDict[reversedQuestIndexList[questIndex]] >= reversedRequiredStatusQuestIndexList[questIndex]
                and questIndex < highestCritter):  #and the quest is better than what is already known to be the best
                    #print("Trapping.getUnlockedCritterStatus~ INFO New highest critter found on character", playerIndex, "! Changing from",highestCritter,"to",questIndex)
                    highestCritter = questIndex
                questIndex += 1
        except Exception as reason:
            print("Trapping.getUnlockedCritterStatus~ EXCEPTION Could not retrieve quest status:", playerIndex, questIndex, reversedQuestIndexList[questIndex], reason)
        playerIndex += 1
        questIndex = 0
    #print("Trapping.getUnlockedCritterStatus~ OUTPUT highestCritter:",highestCritter, reversedCritterIndexList[highestCritter])
    try:
        return [(len(reversedCritterIndexList)-highestCritter), len(reversedCritterIndexList), reversedCritterIndexList[highestCritter]]
    except Exception as reason:
        print("Trapping.getUnlockedCritterStatus~ EXCEPTION Unable to return highestCritter name in reversedCritterIndexList at index",highestCritter,"because:",reason)
        return "UnknownCritter:"+str(highestCritter)

def getPlacedTrapsDict(inputJSON, playerCount):
    placedTrapDict = {}
    counter = 0
    while counter < playerCount:
        try:
            placedTrapDict[counter] = json.loads(inputJSON[("PldTraps_"+str(counter))])
        except Exception as reason:
            print("Trapping~ EXCEPTION Unable to read PlacedTraps when counter=", counter, "and playerCount=", playerCount, "because:", reason)
            placedTrapDict[counter] = []
        counter += 1
    return placedTrapDict

def getCharactersWithUnplacedTraps(inputJSON, trappingLevelsList, placedTrapsDict, playerCount):
    playerUnsuedTrapsDict = {}
    playerMaxPlacableTrapsList = []
    trapsetLevelRequirementList = [48,40,35,25,15,5,1]
    trapsetPlacableCountList = [7,6,5,4,3,2,1]
    #Equipped trap set is in EquipOrder_0 through 9, standard character indexing again, dictionary of 1, element of 4. Stored as a string.
    #Required trap levels for each increased set that gives another slot:
    #Cardboard = Lv1, 1 slot
    #Silkskin = Lv5, 2 slots
    #Wooden = Lv15, 3 slots
    #Nature = Lv25, 4 slots
    #Steel = Lv35, 5 slots
    #Meaty = Lv40, 6 slots
    #Royal = LV48, 7 slots
    #Egalitarian Royal Traps do not give any extra slots, can be ignored.
    #Forbidden Traps do not give any extra slots, can be ignored.
    #Containment of the Zrgyios does not give any extra slots, can be ignored.

    #Step 1 = Get number of expected traps
    #Bonus trap slot comes from the Call Me Ash bubble, which is an Int stored at ["CauldronInfo"][1][11]. If it is level 1 or higher, the extra trap slot is always given. Does not need to be equipped.
    bonusTrapSlot = 0
    if inputJSON["CauldronInfo"][1]["11"] >= 1:
        bonusTrapSlot = 1
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT bonusTrapSlot = ",bonusTrapSlot, "because Call Me Ash level = ",inputJSON["CauldronInfo"][1]["11"])

    playerCounter = 0
    trapListsCounter = 0
    while playerCounter < playerCount:
        while trapListsCounter < len(trapsetLevelRequirementList):
            try:
                if len(playerMaxPlacableTrapsList) <= playerCounter and trappingLevelsList[playerCounter] >= trapsetLevelRequirementList[trapListsCounter]:
                    playerMaxPlacableTrapsList.append(trapsetPlacableCountList[trapListsCounter] + bonusTrapSlot)
            except Exception as reason:
                print("Trapping.getCharactersWithUnplacedTraps~ EXCEPTION Unable to append to playerMaxPlacableTrapsList:", reason)
            trapListsCounter += 1
        if len(playerMaxPlacableTrapsList)-1 < playerCounter:
            playerMaxPlacableTrapsList.append(0)
        playerCounter += 1
        trapListsCounter = 0
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT playerMaxPlacableTrapsList:", playerMaxPlacableTrapsList)

    #Step 2 = Get number of placed traps
    #placedTrapsDict = getPlacedTrapsDict(inputJSON, playerCount)
    if len(placedTrapsDict) > 0:
        for playerKey in placedTrapsDict:
            playerPlacedTraps = 0
            for setTrap in placedTrapsDict[playerKey]:
                if setTrap[0] != -1:
                    playerPlacedTraps += 1
            if playerMaxPlacableTrapsList[playerKey]-playerPlacedTraps > 0:
                playerUnsuedTrapsDict[playerKey] = [str(playerPlacedTraps), str(playerMaxPlacableTrapsList[playerKey])]
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT playerUnsuedTrapsDict:", playerUnsuedTrapsDict)
    return playerUnsuedTrapsDict

def getSecretClassTrapStatus(inputJSON, placedTrapsDict, characterDict):
    secretCharacterNotUsingNatureTrapsDict = {}
    for characterIndex in range(0, len(characterDict)):
        if characterDict[characterIndex].base_class == "Journeyman" and characterDict[characterIndex].trapping_level >= 25:  #the level required to wear Nature Traps
            for trapData in placedTrapsDict[characterIndex]:
                #print("Trapping.getSecretClassTrapStatus~ OUTPUT trapData:",trapData)
                if trapData[0] != -1 and trapData[5] != 3:
                    if characterIndex in secretCharacterNotUsingNatureTrapsDict.keys():
                        secretCharacterNotUsingNatureTrapsDict[characterIndex] += 1
                    else:
                        secretCharacterNotUsingNatureTrapsDict[characterIndex] = 1
    return secretCharacterNotUsingNatureTrapsDict

def setTrappingProgressionTier(inputJSON, characterDict):
    trapping_AdviceDict = {
        "UnlockCritters": [],
        "UnplacedTraps": [],
        "BeginnerNatures": [],
        "NonMetaTraps": []
    }
    trapping_AdviceGroupDict = {}
    trapping_AdviceSection = AdviceSection(
        name="Trapping",
        tier="",
        header="Recommended trapping actions",
        picture="Trapping_Cardboard_Traps.png"
    )
    trappingLevelsList = getSpecificSkillLevelsList(inputJSON, len(characterDict), "Trapping")
    if max(trappingLevelsList) < 1:
        trapping_AdviceSection.header = "Come back after unlocking the Trapping skill in World 3!"
        return trapping_AdviceSection

    highestUnlockedCritter = getUnlockedCritterStatus(inputJSON, len(characterDict))
    placedTrapsDict = getPlacedTrapsDict(inputJSON, len(characterDict))
    unplacedTrapsDict = getCharactersWithUnplacedTraps(inputJSON, trappingLevelsList, placedTrapsDict, len(characterDict))
    secretCharacterNotUsingNatureTrapsDict = getSecretClassTrapStatus(inputJSON, placedTrapsDict, characterDict)

    #UnlockCritters
    tier_unlockCritters = highestUnlockedCritter[0] + 1
    if highestUnlockedCritter[0] != highestUnlockedCritter[1]:  #placed vs placable
        trapping_AdviceDict["UnlockCritters"].append(Advice(
            label=highestUnlockedCritter[2],
            item_name=highestUnlockedCritter[2],
            progression="",  #str(highestUnlockedCritter[0]+1),
            goal=""  #str(highestUnlockedCritter[1]+1)
            )
        )

    #UnusedTraps
    if len(unplacedTrapsDict) > 0:
        for characterIndex in unplacedTrapsDict:
            trapping_AdviceDict["UnplacedTraps"].append(Advice(
                label=str(characterDict[characterIndex]),
                item_name=characterDict[characterIndex].class_name_icon,
                progression=unplacedTrapsDict[characterIndex][0],
                goal=unplacedTrapsDict[characterIndex][1]
                )
            )

    #BeginnerNatures
    if len(secretCharacterNotUsingNatureTrapsDict) > 0:
        for characterIndex in secretCharacterNotUsingNatureTrapsDict:
            trapping_AdviceDict["BeginnerNatures"].append(Advice(
                label=str(characterDict[characterIndex]),
                item_name=characterDict[characterIndex].class_name_icon,
                progression=secretCharacterNotUsingNatureTrapsDict[characterIndex],
                goal=0
                )
            )

    # #NonMetaTraps
    # advice_nonMetaTraps = ""
    # advice_MetaCritterTraps = ""
    # advice_MetaShinyTraps = ""
    # advice_MetaEXPTraps = ""
    # advice_Disclaimer = ""
    # goodTrapTypeList = [0,1,3,6]
    # goodTrapDurationList = [1200,3600,28800,36000,72000,144000,604800]
    # nonMetaTrapDict = {}
    # for playerIndex in placedTrapsDict:
    #     for trapData in placedTrapsDict[playerIndex]:
    #         if trapData[0] != -1 and (trapData[5] not in goodTrapTypeList or trapData[6] not in goodTrapDurationList):
    #             if playerIndex in nonMetaTrapDict.keys():
    #                 nonMetaTrapDict[playerIndex] += 1
    #             else:
    #                 nonMetaTrapDict[playerIndex] = 1
    # if len(nonMetaTrapDict) > 0:
    #     #print("Trapping.setTrappingProgressionTier~ OUTPUT nonMetaTrapDict:",nonMetaTrapDict)
    #     if len(nonMetaTrapDict) == 1:
    #         advice_nonMetaTraps = "The following character has placed traps that aren't of a recommended Trap Type or Duration: "
    #     else:
    #         advice_nonMetaTraps = "The following characters have placed traps that aren't of a recommended Trap Type or Duration: "
    #     for characterIndex in nonMetaTrapDict:
    #         advice_nonMetaTraps += str(characterDict[characterIndex]) + " (" + str(nonMetaTrapDict[characterIndex]) + "), "
    #     advice_nonMetaTraps = advice_nonMetaTraps[:-2] + "."
    #     advice_MetaCritterTraps = "For the highest Critter gains, Set traps with your Beast Master equipped with as much Trapping Efficiency as possible. The most efficient Critter traps for MANUAL CLAIMS are: Royal 20min, Royal 1hr, Cardboard 20min, Royal 10hrs, Cardboard 1hr, Cardboard 8hrs. If you want to let the Rift Trap Vaccuum handle all trap collections, the recommended traps are Royal 40hrs, Royal 10hrs, or Cardboard 20hrs if you don't have Royals unlocked. You could even use Royal 7day traps for minor critter gains, but you'll get less than half as many Cards."
    #     advice_MetaShinyTraps = "Shiny chance is calculated when Collecting traps, not Setting them. The only way to increase the number of Shiny critters per trap is by equipping the Shiny Snitch prayer when Collecting. The highest Shiny chance increasing traps are: Royal 20min, Royal 1hr, Silkskin 20min, Silkskin 1hr, and Royal 10hrs."
    #     advice_MetaEXPTraps = "For the highest pure EXP gains, Set Nature traps with your Maestro/Voidwalker equipped with as much Trapping EXP as possible. Efficiency doesn't matter at all for Nature Traps! The highest EXP traps are: Nature 8hrs and Nature 20hrs."
    #     advice_Disclaimer = "If you are intentionally using a different combination to suite your playstyle, feel free to ignore the below recommendations! They require an active playstyle that isn't for everyone."

    #Generate Advice Groups
    agd_unlockcritters_post_stringsList = [
        "",
        "",
        "Froge critters are unlocked after completing Lord of the Hunt's quest: Pelt for the Pelt God",
        "Crabbo critters are unlocked after completing Lord of the Hunt's quest: Frogecoin to the MOON!",
        "Scorpie critters are unlocked after completing Lord of the Hunt's quest: Yet another Cartoon Reference",
        "Mousey critters are unlocked after completing Lord of the Hunt's quest: Small Stingers, Big Owie",
        "Owlio critters are unlocked after completing Lord of the Hunt's quest: The Mouse n the Molerat",
        "Pingy critters are unlocked after completing Lord of the Hunt's quest: Happy Tree Friend",
        "Bunny critters are unlocked after completing Lord of the Hunt's quest: Noot Noot!",
        "Dung Beat critters are unlocked after completing Lord of the Hunt's quest: Bunny you Should Say That!",
        "Honker critters are unlocked after completing Lord of the Hunt's quest: Rollin' Thunder",
        "Blobfish critters are unlocked after completing Blobbo's quest: Glitter Critter",
    ]
    trapping_AdviceGroupDict["UnlockCritters"] = AdviceGroup(
        tier=highestUnlockedCritter[0]+1,
        pre_string=f"{pl((['UnlockRemaining']*(12-highestUnlockedCritter[0])), 'Unlock the final Critter type', 'Continue unlocking new Critter types from quests')}",
        advices=trapping_AdviceDict["UnlockCritters"],
        post_string=agd_unlockcritters_post_stringsList[highestUnlockedCritter[0]]
    )
    trapping_AdviceGroupDict["UnplacedTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Place unused trap{pl(trapping_AdviceDict['UnplacedTraps'])} (may require better Trap Set!)",
        advices=trapping_AdviceDict["UnplacedTraps"],
        post_string=""
    )
    trapping_AdviceGroupDict["BeginnerNatures"] = AdviceGroup(
        tier="",
        pre_string=f"Place only Nature Traps on your {pl(trapping_AdviceDict['BeginnerNatures'], 'Beginner', 'Beginners')}",
        advices=trapping_AdviceDict["BeginnerNatures"],
        post_string="Nature EXP-only traps are recommended for Maestro's Right Hand of Action and Voidwalker's Species Epoch talents. You will get ZERO critters from Nature Traps, but the bonus critters from those 2 talents more than make up for this loss!"
    )

    #Generate AdviceSection
    max_tier = 12
    overall_TrappingTier = min(max_tier, tier_unlockCritters)
    tier_section = f"{overall_TrappingTier}/{max_tier}"
    trapping_AdviceSection.tier = tier_section
    trapping_AdviceSection.groups = trapping_AdviceGroupDict.values()
    if overall_TrappingTier == max_tier:
        trapping_AdviceSection.header = f"Best Trapping tier met: {tier_section}. Keep it up! You're on the right track! ❤️"
    else:
        trapping_AdviceSection.header = f"Best Trapping tier met: {tier_section}. Recommended Trapping actions"

    return trapping_AdviceSection
