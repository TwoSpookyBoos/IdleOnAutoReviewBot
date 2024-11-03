from consts import break_keep_it_up, trappingQuestsRequirementList
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.data_formatting import safe_loads, mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)
maxCritterTypes = 12

def getCritterName(inputNumber):
    reversedCritterIndexList = ["Tuttle", "Blobfish", "Honker", "Dung Beat", "Bunny", "Pingy", "Owlio", "Mousey", "Scorpie", "Crabbo", "Froge", "None"]
    try:
        return reversedCritterIndexList[inputNumber]
    except:
        return "UnknownCritterName"

def getUnlockedCritterStatus():
    if session_data.account.sneaking['JadeEmporium']["New Critter"]['Obtained']:
        return [
            12,  # Index of the highest unlocked critter
            maxCritterTypes,  # Index of the highest critter possible
            "Tuttle",  # Name of the highest unlocked critter
            "None"  # Name of the next critter to be unlocked
        ]
    else:
        reversedCritterIndexList = ["Blobfish", "Honker", "Dung Beat", "Bunny", "Pingy", "Owlio", "Mousey", "Scorpie", "Crabbo", "Froge", "None"]
        reversedQuestIndexList = ["Blobbo2","Lord_of_the_Hunt10", "Lord_of_the_Hunt9", "Lord_of_the_Hunt8", "Lord_of_the_Hunt7", "Lord_of_the_Hunt6", "Lord_of_the_Hunt5", "Lord_of_the_Hunt4", "Lord_of_the_Hunt3", "Lord_of_the_Hunt2"]
        reversedRequiredStatusQuestIndexList = [1,0,0,0,0,0,0,0,0,0,0]
        highestCritter = (len(reversedCritterIndexList)-1)
        #Critters available to be trapped can be found by quest status, except for the current last critter of Tuttles
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

        questIndex = 0
        for characterIndex in range(0, session_data.account.playerCount):
            try:
                questDict = session_data.account.all_quests[characterIndex]
                for questIndex in range(0, len(reversedQuestIndexList)):
                    if (questDict[reversedQuestIndexList[questIndex]] >= reversedRequiredStatusQuestIndexList[questIndex]
                    and questIndex < highestCritter):  #and the quest is better than what is already known to be the best
                        #print("Trapping.getUnlockedCritterStatus~ INFO New highest critter found on character", characterIndex, "! Changing from",highestCritter,"to",questIndex)
                        #logger.debug(f"New highest critter available from character {characterIndex}! Changing from {reversedCritterIndexList[highestCritter]} to {reversedCritterIndexList[questIndex]}")
                        highestCritter = questIndex
            except Exception as reason:
                logger.exception(f"Could not retrieve {reversedQuestIndexList[questIndex]} status on Character{characterIndex} because {reason}")
                #print("Trapping.getUnlockedCritterStatus~ EXCEPTION Could not retrieve quest status:", characterIndex, questIndex, reversedQuestIndexList[questIndex], reason)
            characterIndex += 1
            questIndex = 0
        #print("Trapping.getUnlockedCritterStatus~ OUTPUT highestCritter:",highestCritter, reversedCritterIndexList[highestCritter])
        try:
            return [
                (len(reversedCritterIndexList)-highestCritter),  # Index of the highest unlocked critter
                maxCritterTypes,  # Index of the highest critter possible
                reversedCritterIndexList[highestCritter],  #Name of the highest unlocked critter
                getCritterName(highestCritter)  #Name of the next critter to be unlocked
            ]
        except Exception as reason:
            print("Trapping.getUnlockedCritterStatus~ EXCEPTION Unable to return highestCritter name in reversedCritterIndexList at index",highestCritter,"because:",reason)
            return "UnknownCritter:"+str(highestCritter)

def getPlacedTrapsDict():
    placedTrapDict = {}
    for characterIndex in range(0, session_data.account.playerCount):
        try:
            placedTrapDict[characterIndex] = safe_loads(session_data.account.raw_data[f"PldTraps_{characterIndex}"])
        except:
            logger.exception(f"Unable to retrieve 'PldTraps_{characterIndex}'")
            placedTrapDict[characterIndex] = []
    return placedTrapDict

def getCharactersWithUnplacedTraps(trappingLevelsList, placedTrapsDict):
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
    if session_data.account.alchemy_bubbles['Call Me Ash']['Level'] >= 1:
        bonusTrapSlot = 1
    #print("Trapping.getCharactersWithUnplacedTraps~ OUTPUT bonusTrapSlot = ",bonusTrapSlot, "because Call Me Ash level = ",inputJSON["CauldronInfo"][1]["11"])

    for characterIndex in range(0, session_data.account.playerCount):
        for trapListIndex in range(0, len(trapsetLevelRequirementList)):
            try:
                if len(playerMaxPlacableTrapsList) <= characterIndex and trappingLevelsList[characterIndex] >= trapsetLevelRequirementList[trapListIndex]:
                    playerMaxPlacableTrapsList.append(trapsetPlacableCountList[trapListIndex] + bonusTrapSlot)
            except:
                logger.exception(f"Unable to append to playerMaxPlacableTrapsList")
        if len(playerMaxPlacableTrapsList)-1 < characterIndex:
            playerMaxPlacableTrapsList.append(0)

    #Step 2 = Get number of placed traps
    if len(placedTrapsDict) > 0:
        for playerKey in placedTrapsDict:
            playerPlacedTraps = 0
            for setTrap in placedTrapsDict[playerKey]:
                if setTrap[0] != -1:
                    playerPlacedTraps += 1
            if playerMaxPlacableTrapsList[playerKey]-playerPlacedTraps > 0:
                playerUnsuedTrapsDict[playerKey] = [str(playerPlacedTraps), str(playerMaxPlacableTrapsList[playerKey])]
    return playerUnsuedTrapsDict

def getSecretClassTrapStatus(placedTrapsDict):
    secretCharacterNotUsingNatureTrapsDict = {}
    for character in session_data.account.all_characters:
        if character.base_class == "Journeyman" and character.trapping_level >= 25:  #the level required to wear Nature Traps
            for trapData in placedTrapsDict[character.character_index]:
                #print("Trapping.getSecretClassTrapStatus~ OUTPUT trapData:",trapData)
                if trapData[0] != -1 and trapData[5] != 3:
                    if character.character_index in secretCharacterNotUsingNatureTrapsDict.keys():
                        secretCharacterNotUsingNatureTrapsDict[character.character_index] += 1
                    else:
                        secretCharacterNotUsingNatureTrapsDict[character.character_index] = 1
    return secretCharacterNotUsingNatureTrapsDict

def getUnmaxedCritterVialStatus():
    unmaxedCritterVialsCount = 0
    critterVialIndexList = [
        23,  #Crabbo
        31,  #Mousey
        37,  #Bunny
        40,  #Honker
        47,  #Blobfish
        74,  #Tuttle
    ]
    for critterVialIndex in critterVialIndexList:
        try:
            if int(session_data.account.raw_data["CauldronInfo"][4][str(critterVialIndex)]) != 13:
                unmaxedCritterVialsCount += 1
        except:
            logger.warning(f"Unable to retrieve Vial level for critterVialIndex {critterVialIndex}")
            unmaxedCritterVialsCount += 1
    return unmaxedCritterVialsCount != 0

def getStaticCritterTrapAdviceList(highestTrapset: int) -> dict[str, list[Advice]]:
    adviceDict = {
        "Efficiency for Manually Claimed traps": [],
    }
    if highestTrapset >= 6:
        listIndexManualAdvice = 6
    elif highestTrapset >= 5:
        listIndexManualAdvice = 5
    else:
        listIndexManualAdvice = 0

    if highestTrapset >= 6:
        listIndexVaccuumAdvice = 6
    elif highestTrapset >= 5:
        listIndexVaccuumAdvice = 5
    elif highestTrapset >= 2:
        listIndexVaccuumAdvice = 2
    else:
        listIndexVaccuumAdvice = 0

    manualCritterTrapsDict = {
        0: [["Cardboard 20 Minutes", "Cardboard 1 Hour", "Cardboard 8 Hours", "Cardboard 20 Hours"], ["3x/hr", "2x/hr", "1.25x/hr", "1x/hr"]],
        5: [["Cardboard 20 Minutes", "Meaty 1 Hour", "Meaty 10 Hours", "Cardboard 8 Hours", "Cardboard 20 Hours"], ["3x/hr", "3x/hr", "1.5x/hr", "1.25x/hr", "1x/hr"]],
        6: [["Royal 20 Minutes", "Royal 1 Hour", "Royal 10 Hours", "Royal 40 Hours"], ["6x/hr", "4x/hr", "2.1x/hr", "1.75x/hr"]]
    }
    vaccuumCritterTrapsDict = {
        0: [["Cardboard 20 Hours"], ["0.83x/hr"]],
        2: [["Wooden 5 Days", "Cardboard 20 Hours"], ["1.67x/hr", "0.83x/hr"]],
        5: [["Wooden 5 Days", "Meaty 8 Days", "Cardboard 20 Hours"],["1.67x/hr", "1.15x/hr", "0.83x/hr"]],
        6: [["Wooden 5 Days", "Royal 40 Hours", "Meaty 8 Days", "Royal 10 Hours"], ["1.67x/hr", "1.46x/hr", "1.15x/hr", "0.88x/hr"]]
    }

    for counter in range(0, len(manualCritterTrapsDict[listIndexManualAdvice][0])):
        adviceDict["Efficiency for Manually Claimed traps"].append(
            Advice(
                label=manualCritterTrapsDict[listIndexManualAdvice][0][counter],
                picture_class=f"{manualCritterTrapsDict[listIndexManualAdvice][0][counter].lower().split(' ')[0]}-traps",
                progression=manualCritterTrapsDict[listIndexManualAdvice][1][counter])
        )

    if session_data.account.rift['TrapBoxVacuum']:
        adviceDict["Efficiency for Rift's Daily traps"] = []
        for counter in range(0, len(vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0])):
            adviceDict["Efficiency for Rift's Daily traps"].append(
                Advice(
                    label=vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0][counter],
                    picture_class=f"{vaccuumCritterTrapsDict[listIndexVaccuumAdvice][0][counter].lower().split(' ')[0]}-traps",
                    progression=vaccuumCritterTrapsDict[listIndexVaccuumAdvice][1][counter])
            )

    return adviceDict

def getStaticShinyTrapAdviceList(highestTrapset: int) -> dict[str, list[Advice]]:
    adviceDict = {
        "Shiny Chance Multi for Manually Claimed traps": []
    }
    numOfVaccuumSuggestions = 2
    #"The highest Shiny chance increasing traps are: Royal 20min, Royal 1hr, Silkskin 20min, Silkskin 1hr, and Royal 10hrs."
    shinyTrapsLabelList = ["Royal 20 Minutes", "Royal 1 Hour", "Silkskin 20 Minutes", "Silkskin 1 Hour", "Royal 10 Hours", "Silkskin 20 Hours", "Royal 40 Hours"]
    shinyTrapsItemNameList = ["royal-traps", "royal-traps", "silkskin-traps", "silkskin-traps", "royal-traps", "silkskin-traps", "royal-traps"]
    shinyTrapsRequiredTrapIndexList = [6, 6, 1, 1, 6, 1, 6]
    shinyTrapsEffPerHourList = ["12x/hr", "8x/hr", "3x/hr", "2.1x/hr", "3.8x/hr", "1.25x/hr", "2.6x/hr"]
    for counter in range(0, len(shinyTrapsLabelList) - numOfVaccuumSuggestions):
        if highestTrapset >= shinyTrapsRequiredTrapIndexList[counter]:
            adviceDict["Shiny Chance Multi for Manually Claimed traps"].append(
                Advice(
                    label=shinyTrapsLabelList[counter],
                    picture_class=shinyTrapsItemNameList[counter],
                    progression=shinyTrapsEffPerHourList[counter])
            )

    if session_data.account.rift['TrapBoxVacuum']:
        adviceDict["Shiny Chance Multi for Rift's Daily traps"] = []
        for counter in range(len(shinyTrapsLabelList) - numOfVaccuumSuggestions, len(shinyTrapsLabelList)):
            if highestTrapset >= shinyTrapsRequiredTrapIndexList[counter]:
                adviceDict["Shiny Chance Multi for Rift's Daily traps"].append(
                    Advice(
                        label=shinyTrapsLabelList[counter],
                        picture_class=shinyTrapsItemNameList[counter],
                        progression=shinyTrapsEffPerHourList[counter])
                )
    return adviceDict

def getStaticEXPTrapAdviceList(highestTrapset) -> dict[str, list[Advice]]:
    adviceDict = {
        "Best Experience for Manually Claimed traps": []
    }
    numOfVaccuumSuggestions = 1
    # The highest EXP traps are: Nature 8hrs and Nature 20hrs.
    expTrapsLabelList = ["Natural 8 Hours", "Natural 20 Hours"]
    expTrapsItemNameList = ["natural-traps", "natural-traps"]
    expTrapsRequiredTrapIndexList = [3, 3]
    expTrapsEffPerHourList = ["5x/hr", "3.12x/hr"]
    for counter in range(0, len(expTrapsLabelList) - numOfVaccuumSuggestions):
        if highestTrapset >= expTrapsRequiredTrapIndexList[counter]:
            adviceDict["Best Experience for Manually Claimed traps"].append(
                Advice(
                    label=expTrapsLabelList[counter],
                    picture_class=expTrapsItemNameList[counter],
                    progression=expTrapsEffPerHourList[counter])
            )

    if session_data.account.rift['TrapBoxVacuum']:
        adviceDict["Best Experience for Rift's Daily traps"] = []
        for counter in range(len(expTrapsLabelList) - numOfVaccuumSuggestions, len(expTrapsLabelList)):
            if highestTrapset >= expTrapsRequiredTrapIndexList[counter]:
                adviceDict["Best Experience for Rift's Daily traps"].append(
                    Advice(label=expTrapsLabelList[counter], picture_class=expTrapsItemNameList[counter], progression=expTrapsEffPerHourList[counter],
                           goal="", unit=""))
    return adviceDict

def getProgressionTiersAdviceGroup(trappingLevelsList: list[int]):
    trapping_AdviceDict = {
        "UnlockCritters": [],
        "UnplacedTraps": [],
        "BeginnerNatures": [],
        "NonMetaTraps": [],
        "CritterTraps": [],
        "ShinyTraps": [],
        "EXPTraps": []
    }
    trapping_AdviceGroupDict = {}
    highestUnlockedCritter = getUnlockedCritterStatus()
    info_tiers = 0
    max_tier = highestUnlockedCritter[1] - info_tiers

    highestWearableTrapset = 0
    trapsetLevelRequirementList = [1, 5, 15, 25, 35, 40, 48]
    for index in range(0, len(trapsetLevelRequirementList)):
        if max(trappingLevelsList) >= trapsetLevelRequirementList[index]:
            highestWearableTrapset = index

    placedTrapsDict = getPlacedTrapsDict()
    unplacedTrapsDict = getCharactersWithUnplacedTraps(trappingLevelsList, placedTrapsDict)
    secretCharacterNotUsingNatureTrapsDict = getSecretClassTrapStatus(placedTrapsDict)

    # UnlockCritters
    agd_unlockcritters_post_stringsList = [
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
        "Tuttle critters are unlocked in W6 Jade Emporium",
        ""
    ]
    tier_unlockCritters = highestUnlockedCritter[0]
    if tier_unlockCritters != maxCritterTypes:  # unlocked not equal to the max possible to unlock.
        trapping_AdviceDict["UnlockCritters"].append(
            Advice(
                label=agd_unlockcritters_post_stringsList[highestUnlockedCritter[0]],
                picture_class=highestUnlockedCritter[3],
                progression=0,
                goal=1
            )
        )
        if 2 <= tier_unlockCritters < 11:  # Show only the quests with Critter requirement
            for requiredItemCodeName, requiredQuantity in trappingQuestsRequirementList[tier_unlockCritters - 2]['RequiredItems'].items():
                #logger.debug(f"requiredItemCodeName = {requiredItemCodeName}")
                item_asset = session_data.account.all_assets.get(requiredItemCodeName)
                trapping_AdviceDict["UnlockCritters"].append(Advice(
                    label=item_asset.name,
                    picture_class=item_asset.name,
                    progression=item_asset.amount,
                    goal=requiredQuantity
                ))
    for advice in trapping_AdviceDict["UnlockCritters"]:
        mark_advice_completed(advice)

    # UnusedTraps
    if len(unplacedTrapsDict) > 0:
        for characterIndex in unplacedTrapsDict:
            trapping_AdviceDict["UnplacedTraps"].append(
                Advice(
                    label=session_data.account.all_characters[characterIndex].character_name,
                    picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
                    progression=unplacedTrapsDict[characterIndex][0],
                    goal=unplacedTrapsDict[characterIndex][1])
            )

    # BeginnerNatures
    if len(secretCharacterNotUsingNatureTrapsDict) > 0:
        for characterIndex in secretCharacterNotUsingNatureTrapsDict:
            trapping_AdviceDict["BeginnerNatures"].append(
                Advice(
                    label=session_data.account.all_characters[characterIndex].character_name,
                    picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
                    progression=secretCharacterNotUsingNatureTrapsDict[characterIndex],
                    goal=0)
            )

    # NonMetaTraps
    hasUnmaxedCritterVial = getUnmaxedCritterVialStatus()
    goodTrapDict = {
        0: [1200, 3600, 28800, 72000],  # Cardboard Traps
        1: [1200, 3600, 28800, 72000],  # Silkskin Traps. 14400 is excluded.
        2: [432000],  # Wooden Traps. Only 5 days 0xp is good, and only if they still have Vials to complete
        3: [28800, 72000],  # Natural Traps. 8hr and 20hr are good, other options are bad.
        6: [1200, 3600, 36000, 144000, 604800]  # Royal Traps. All but the 28day are good.
    }
    if max(trappingLevelsList) < 48:
        goodTrapDict[5] = [3600, 36000, 108000]  # Before being able to wear Royals, Meaty traps give more critter efficiency than Cardboard
    nonMetaTrapDict = {}
    for characterIndex in placedTrapsDict:
        badTrapCount = 0
        for trapData in placedTrapsDict[characterIndex]:
            if trapData[0] != -1:  # -1 is an unplaced trap
                if trapData[5] not in goodTrapDict.keys():  # Bad trap sets don't appear in goodTrapDict
                    badTrapCount += 1
                elif trapData[6] not in goodTrapDict[trapData[5]]:  # Bad trap set + duration combos don't appear in goodTrapDict
                    badTrapCount += 1
                elif int(trapData[5]) == 2 and int(trapData[6]) == 432000 and int(trapData[7]) != 0 and hasUnmaxedCritterVial is False:
                    # Using a 5day Wooden Trap that isn't the 0exp variety without a Critter Vial to max. Would be better using Royal/Natures in this scenario.
                    badTrapCount += 1
        if badTrapCount != 0:
            nonMetaTrapDict[characterIndex] = badTrapCount

    for characterIndex in nonMetaTrapDict:
        trapping_AdviceDict["NonMetaTraps"].append(
            Advice(
                label=session_data.account.all_characters[characterIndex].character_name,
                picture_class=session_data.account.all_characters[characterIndex].class_name_icon,
                progression=str(nonMetaTrapDict[characterIndex]),
                goal=0)
        )

    # if len(trapping_AdviceDict["NonMetaTraps"]) > 0:  #Several requests came in to always show this information
    trapping_AdviceDict["CritterTraps"] = getStaticCritterTrapAdviceList(highestWearableTrapset)
    trapping_AdviceDict["ShinyTraps"] = getStaticShinyTrapAdviceList(highestWearableTrapset)
    trapping_AdviceDict["EXPTraps"] = getStaticEXPTrapAdviceList(highestWearableTrapset)

    # Generate Advice Groups

    trapping_AdviceGroupDict["UnlockCritters"] = AdviceGroup(
        tier=highestUnlockedCritter[0],
        pre_string=f"{pl((['UnlockRemaining'] * (maxCritterTypes - highestUnlockedCritter[0])), 'Unlock the final Critter type', 'Continue unlocking new Critter types')}",
        advices=trapping_AdviceDict["UnlockCritters"],
    )
    trapping_AdviceGroupDict["UnplacedTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Place unused trap{pl(trapping_AdviceDict['UnplacedTraps'])} (may require better Trap Set!)",
        advices=trapping_AdviceDict["UnplacedTraps"],
        post_string="",
        informational=True
    )
    trapping_AdviceGroupDict["BeginnerNatures"] = AdviceGroup(
        tier="",
        pre_string=f"Place only Nature Traps on your Beginner{pl(trapping_AdviceDict['BeginnerNatures'])}",
        advices=trapping_AdviceDict["BeginnerNatures"],
        post_string=f"Nature EXP-only traps are recommended for Maestro's Right Hand of Action and Voidwalker's Species Epoch talents."
                    f" You will get ZERO critters from Nature Traps, but the bonus critters from those 2 talents more than make up for this loss!",
        informational=True,
        completed=min([vman.trapping_level for vman in session_data.account.vmans], default=0) >= 120 or len(trapping_AdviceDict["BeginnerNatures"]) == 0
    )
    trapping_AdviceGroupDict["NonMetaTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Inefficient Trap Types or Durations",
        advices=trapping_AdviceDict["NonMetaTraps"],
        post_string="",
        informational=True
    )
    trapping_AdviceGroupDict["CritterTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Best Critter-Focused traps",
        advices=trapping_AdviceDict["CritterTraps"],
        post_string="Set critter traps with your Beast Master after maximizing Trapping Efficiency",
        informational=True,
        completed=True
    )
    trapping_AdviceGroupDict["ShinyTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Best Shiny Chance-Focused traps",
        advices=trapping_AdviceDict["ShinyTraps"],
        post_string="Wear the Shiny Snitch prayer when Collecting. Shorter trap durations will earn more total Shiny Critters per day",
        informational=True,
        completed=True
    )
    trapping_AdviceGroupDict["EXPTraps"] = AdviceGroup(
        tier="",
        pre_string=f"Best EXP-Focused traps",
        advices=trapping_AdviceDict["EXPTraps"],
        post_string="Set EXP traps with your Mman/Vman after maximizing Trapping EXP",
        informational=True,
        completed=True
    )
    overall_SectionTier = min(max_tier, tier_unlockCritters)
    return trapping_AdviceGroupDict, overall_SectionTier, max_tier

def getTrappingAdviceSection() -> AdviceSection:
    trappingLevelsList = session_data.account.all_skills["Trapping"]
    if max(trappingLevelsList) < 1:
        trapping_AdviceSection = AdviceSection(
            name="Trapping",
            tier="",
            header="Come back after unlocking the Trapping skill in World 3!",
            picture="Trapping_Cardboard_Traps.png",
            unreached=True
        )
        return trapping_AdviceSection

    #Generate AdviceGroups
    trapping_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceGroup(trappingLevelsList)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    trapping_AdviceSection = AdviceSection(
        name="Trapping",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Trapping tier met: {tier_section}{break_keep_it_up if overall_SectionTier >= max_tier else ''}",
        picture="Trapping_Cardboard_Traps.png",
        groups=trapping_AdviceGroupDict.values()
    )

    return trapping_AdviceSection
