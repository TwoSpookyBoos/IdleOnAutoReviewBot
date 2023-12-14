import json
import progressionResults
from idleon_CombatLevels import getHumanReadableClasses

def getUnlockedCritterStatus(inputJSON, playerCount):
    #critterIndexList = ["None", "Froge", "Crabbo", "Scorpie", "Mousey", "Owlio", "Pingy", "Bunny", "Dung Beat", "Honker", "Blobfish"]
    #questIndexList = ["Lord_of_the_Hunt2", "Lord_of_the_Hunt3", "Lord_of_the_Hunt4", "Lord_of_the_Hunt5", "Lord_of_the_Hunt6", "Lord_of_the_Hunt7", "Lord_of_the_Hunt8", "Lord_of_the_Hunt9", "Lord_of_the_Hunt10", "Blobbo2"]
    #requiredStatusQuestIndexList = [0,0,0,0,0,0,0,0,0,0,1]
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
                and questIndex < highestCritter): #and the quest is better than what is already known to be the best
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
        return ("UnknownCritter:"+str(highestCritter))

def getPlacedTrapsDict(inputJSON, playerCount):
    placedTrapDict = {}
    counter = 0
    try:
        while counter < playerCount:
            placedTrapDict[counter] = json.loads(inputJSON[("PldTraps_"+str(counter))])
            counter += 1
    except Exception as reason:
        print("Trapping~ EXCEPTION Unable to read PlacedTraps when counter=",counter,"and playerCount=",playerCount,"because:",reason)
    #print("Trapping~ OUTPUT placedTrapDict:", len(placedTrapDict), type(placedTrapDict), placedTrapDict)
    #list of lists per character in PldTraps_0 through 9, standard character indexing.
    #[0] I think this is critter id? -1 if no trap placed
    #[1] no idea
    #[2] looks like time elapsed since trap was placed
    #[3] critter type string if placed, otherwise int 0
    #[4] quantity of critters. My demo was 0 since it is a Nature Trap.
    #[5] trap type. I have a 3 there for nature traps. Other instances I see are 6 which are my Royal Traps. Guessing this is just trapset in order then. 0:Cardboard, 1:Silkskin, 2:Wooden, 3:Nature, 4:Steel, 5:Meaty, 6:Royal
    #[6] = trap duration in seconds. 72000 = 20hr
    #[7] =
    #[8] = Might be exp? All of my nature traps across my accounts have this same identical value. The other traps seem to increase based on higher and higher critters.
    #[9] =
    return placedTrapDict

def getTrappingLevelsList(inputJSON, playerCount):
    #Trapping level to determine traps they can wear is in [LV0_0]through [LV0_9] which I think is a list? Element 7 . Stored as an Int.
    trappingLevelsList = []
    counter = 0
    while counter < playerCount:
        playerTrappingLevel = inputJSON["Lv0_"+str(counter)][7]
        #print("Trapping.getTrappingLevelsList~ OUTPUT playerTrappingLevel=",playerTrappingLevel,"when player=",counter)
        trappingLevelsList.append(playerTrappingLevel)
        counter += 1
    #print("Trapping.getTrappingLevelsList~ OUTPUT trappingLevelsList:",trappingLevelsList)
    return trappingLevelsList

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
    #Egalitarian Royal does not give any extra slots, can be ignored.

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
                print("Trapping.getCharactersWithUnplacedTraps~ EXCEPTION Unable to append to playerMaxPlacableTrapsList:",reason)
            trapListsCounter += 1
        if len(playerMaxPlacableTrapsList)-1 < playerCounter:
            playerMaxPlacableTrapsList.append(0)
        playerCounter +=1
        trapListsCounter = 0
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT playerMaxPlacableTrapsList:",playerMaxPlacableTrapsList)

    #Step 2 = Get number of placed traps
    #placedTrapsDict = getPlacedTrapsDict(inputJSON, playerCount)
    if len(placedTrapsDict) > 0:
        for playerKey in placedTrapsDict:
            playerPlacedTraps = 0
            for setTrap in placedTrapsDict[playerKey]:
                if setTrap[0] != -1:
                    playerPlacedTraps += 1
            if playerMaxPlacableTrapsList[playerKey]-playerPlacedTraps > 0:
                playerUnsuedTrapsDict[playerKey] = "(" + str(playerPlacedTraps) + "/" + str(playerMaxPlacableTrapsList[playerKey]) + ")"
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT playerUnsuedTrapsDict:",playerUnsuedTrapsDict)
    return playerUnsuedTrapsDict

def getSecretClassTrapStatus(inputJSON, trappingLevelsList, placedTrapsDict, playerCount):
    secretCharacterNotUsingNatureTrapsDict = {}
    expectedSecretClassNumber = [2,3,4]
    characterIndex = 0
    while characterIndex < playerCount:
        if inputJSON['CharacterClass_'+str(characterIndex)] in expectedSecretClassNumber:
            if trappingLevelsList[characterIndex] >= 25: #the level required to wear Nature Traps
                for trapData in placedTrapsDict[characterIndex]:
                    #print("Trapping.getSecretClassTrapStatus~ OUTPUT trapData:",trapData)
                    if trapData[0] != -1 and trapData[5] != 3:
                        if characterIndex in secretCharacterNotUsingNatureTrapsDict.keys():
                            secretCharacterNotUsingNatureTrapsDict[characterIndex] += 1
                        else:
                            secretCharacterNotUsingNatureTrapsDict[characterIndex] = 1
        characterIndex += 1
    #print("Trapping.getSecretClassTrapStatus~ OUTPUT secretCharacterNotUsingNatureTrapsDict:",secretCharacterNotUsingNatureTrapsDict)
    return secretCharacterNotUsingNatureTrapsDict

def setTrappingProgressionTier(inputJSON, playerCount, playerNames, fromPublicIEBool):
    trappingLevelsList = getTrappingLevelsList(inputJSON, playerCount)
    if max(trappingLevelsList) < 1:
        trappingPR = progressionResults.progressionResults(0,["### Recommended Trapping actions:","Come back after unlocking the Trapping skill in World 3!"],"")
        return trappingPR
    highestUnlockedCritter = getUnlockedCritterStatus(inputJSON, playerCount)
    placedTrapsDict = getPlacedTrapsDict(inputJSON, playerCount)
    unplacedTrapsDict = getCharactersWithUnplacedTraps(inputJSON, trappingLevelsList, placedTrapsDict, playerCount)
    secretCharacterNotUsingNatureTrapsDict = getSecretClassTrapStatus(inputJSON, trappingLevelsList, placedTrapsDict, playerCount)

    advice_UnlockCritters = ""
    if highestUnlockedCritter[0] != highestUnlockedCritter[1]: #playerHighest vs current highest possible
        advice_UnlockCritters = " * Continue unlocking new critter types from quests (" + str(highestUnlockedCritter[0]) + "/" + str(highestUnlockedCritter[1])+ ")! Check the Wiki for exact unlock requirements."
        #print("Trapping.setTrappingProgressionTier~ OUTPUT advice_UnlockCritters:",advice_UnlockCritters)

    advice_UnusedTrapSlots = ""
    if len(unplacedTrapsDict) > 0:
        advice_UnusedTrapSlots = " * Place remaining Traps (may require equipping a better trap tool!): "
        for characterIndex in unplacedTrapsDict:
            if fromPublicIEBool:
                advice_UnusedTrapSlots += playerNames[characterIndex] + " " + unplacedTrapsDict[characterIndex] + ", "
            else:
                advice_UnusedTrapSlots += "Character" + str(characterIndex) + " " + unplacedTrapsDict[characterIndex] + ", "
        advice_UnusedTrapSlots = advice_UnusedTrapSlots[:-2] #trim off trailing comma and space
    #print("Trapping.setTrappingProgressionTier~ OUTPUT advice_UnusedTrapSlots:",advice_UnusedTrapSlots)

    advice_BeginnerNatures = ""
    if len(secretCharacterNotUsingNatureTrapsDict) > 0:
        advice_BeginnerNatures = " * "
        for characterIndex in secretCharacterNotUsingNatureTrapsDict:
            if fromPublicIEBool:
                advice_BeginnerNatures += playerNames[characterIndex] + " has " + str(secretCharacterNotUsingNatureTrapsDict[characterIndex]) + " non-Nature traps, "
            else:
                advice_BeginnerNatures += "Character" + str(characterIndex) + " " + secretCharacterNotUsingNatureTrapsDict[characterIndex] + ", "
        advice_BeginnerNatures = advice_BeginnerNatures[:-2] + ". Nature EXP-only traps are recommended because the Maestro and Voidwalker classes both get important buffs based on their Trapping level. You will get ZERO critters from Nature Traps, but the bonus EXP is worth it!" #trim off trailing comma and space
    #print("Trapping.setTrappingProgressionTier~ OUTPUT advice_BeginnerNatures:",advice_BeginnerNatures)

    advice_nonMetaTraps = ""
    advice_MetaCritterTraps = ""
    advice_MetaShinyTraps = ""
    advice_MetaEXPTraps = ""
    advice_Disclaimer = ""
    goodTrapTypeList = [0,1,3,6]
    goodTrapDurationList = [1200,3600,28800,36000,72000,144000]
    nonMetaTrapDict = {}
    for playerIndex in placedTrapsDict:
        for trapData in placedTrapsDict[playerIndex]:
            if trapData[0] != -1 and (trapData[5] not in goodTrapTypeList or trapData[6] not in goodTrapDurationList):
                if playerIndex in nonMetaTrapDict.keys():
                    nonMetaTrapDict[playerIndex] += 1
                else:
                    nonMetaTrapDict[playerIndex] = 1
    if len(nonMetaTrapDict) > 0:
        #print("Trapping.setTrappingProgressionTier~ OUTPUT nonMetaTrapDict:",nonMetaTrapDict)
        if len(nonMetaTrapDict) == 1:
            advice_nonMetaTraps = " * The following character has placed traps that aren't of a recommended Trap Type or Duration: "
        else:
            advice_nonMetaTraps = " * The following characters have placed traps that aren't of a recommended Trap Type or Duration: "
        for characterIndex in nonMetaTrapDict:
            if fromPublicIEBool:
                advice_nonMetaTraps += playerNames[characterIndex] + " (" + str(nonMetaTrapDict[characterIndex]) + "), "
            else:
                advice_nonMetaTraps += "Character" + str(characterIndex) + " (" + str(nonMetaTrapDict[characterIndex]) + "), "
        advice_nonMetaTraps = advice_nonMetaTraps[:-2] + "."
        advice_MetaCritterTraps = " * For the highest Critter gains, Set traps with your Beast Master equipped with as much Trapping Efficiency as possible. The most efficient Critter traps in order are: Royal 20min, Royal 1hr, Cardboard 20min, Royal 10hrs, Cardboard 1hr, and Royal 40hrs."
        advice_MetaShinyTraps = " * Shiny chance is calculated when Collecting traps, not Setting them. The only way to increase the number of Shiny critters per trap is by equipping the Shiny Snitch prayer when Collecting. The highest Shiny chance increasing traps are: Royal 20min, Royal 1hr, Silkskin 20min, Silkskin 1hr, and Royal 10hrs."
        advice_MetaEXPTraps = " * For the highest pure EXP gains, Set Nature traps with your Maestro/Voidwalker equipped with as much Trapping EXP as possible. Efficiency doesn't matter at all for Nature Traps! The highest EXP traps are: Nature 8hrs and Nature 20hrs."
        advice_Disclaimer = " * If you are intentionally using a different combination to suite your playstyle, feel free to ignore the below recommendations! They require an active playstyle that isn't for everyone."

    advice_TrappingTarget = ""

    if advice_UnlockCritters == "" and advice_UnusedTrapSlots == "" and advice_BeginnerNatures == "" and advice_TrappingTarget == "" and advice_Disclaimer == "":
        advice_UnlockCritters = " * Nada. You look like you're on the right track! :D"
    advice_TrappingCombined = ["### Recommended Trapping actions:", advice_UnlockCritters, advice_UnusedTrapSlots, advice_BeginnerNatures, advice_Disclaimer, advice_nonMetaTraps, advice_MetaCritterTraps, advice_MetaShinyTraps, advice_MetaEXPTraps]
    trappingPR = progressionResults.progressionResults(0,advice_TrappingCombined,"")
    return trappingPR