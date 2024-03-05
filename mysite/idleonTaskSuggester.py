#idleonTaskSuggester.py
import datetime

from flask import g

from data_formatting import logger, getJSONfromAPI, getJSONfromText, getLastUpdatedTime, getCharacterDetails, HeaderData
#general stuff that makes this file too big if I include directly
from models import AdviceWorld, WorldName, Account, Character
from consts import progressionTiers


#general autoreview
import idleon_Pinchy
import idleon_CombatLevels
import idleon_Consumables
import idleon_GemShop
import idleon_Greenstacks
import idleon_MaestroHands
import idleon_Cards

from idleon_Pinchy import Placements

#w1
import idleon_Stamps
import idleon_Bribes
import idleon_Smithing

#w2
import idleon_Alchemy
#import idleon_Obols

#w3
#import idleon_Sampling
import idleon_ConsRefinery
import idleon_ConsSaltLick
import idleon_ConsDeathNote
import idleon_ConsBuildings
import idleon_Worship
import idleon_Trapping

#w4
import idleon_Breeding


#Global variables


#Step 1: Retrieve data from public IdleonEfficiency website or from file


def getRoastableStatus(playerNames):
    roastworthyList = ["scoli", "weebgasm", "herusx", "rashaken", "trickzbunny", "redpaaaaanda"]
    return next((name.lower() in roastworthyList for name in playerNames), False)


def main(inputData, runType="web"):
    bannedAccountsList = ["thedyl", "wooddyl", "3boyy", "4minez", "5arch5", "6knight6", "7maestro7", "bowboy8", "8barb8", "10es10", "favicon.ico", "robots.txt"]
    empty = ""
    emptyList = [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    banned = "This account has been banned from lookups."
    bannedList = [banned,empty,empty,empty,empty,empty,empty,empty,empty,empty]
    bannedListofLists = [
        [bannedList,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #general placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w1 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w2 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w3 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w4 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w5 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w6 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w7 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty],  #w8 placeholder
        [empty,empty,empty,empty,empty,empty,empty,empty,empty,empty]  #pinchy placeholder
    ]

    if isinstance(inputData, str):
        inputData = inputData.strip()  # remove leading and trailing whitespaces

    headerData = HeaderData()
    #Step 1: Retrieve data from public IdleonEfficiency website or from file
    if len(inputData) < 16 and isinstance(inputData, str):
        #print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for", inputData, "~~~~~~~~~~~~~~~")
        inputData = inputData.replace(" ", "_")  # IE expects underscores instead of spaces in names
        #print("inputData:'" + inputData + "' found in the banned list?", (inputData in bannedAccountsList))
        if inputData.lower() in bannedAccountsList:
            if runType == "web":
                print("idleonTaskSuggester~ PETTY BITCH MODE ACTIVATED. Banned name entered:", inputData)
                return bannedListofLists
            elif runType == "consoleTest":
                return "Banned"
        else:
            parsedJSON = getJSONfromAPI(runType, "https://" + inputData + ".idleonefficiency.com/raw-data")
            if parsedJSON == "PublicIEProfileNotFound" and runType == "consoleTest":
                return "PublicIEProfileNotFound"
            headerData.ie_link = f"https://{inputData.lower()}.idleonefficiency.com"
            headerData.link_text = f"{inputData.lower()}.idleonefficiency.com"
    else:
        if runType == "web":
            print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for direct web JSON input.~~~~~~~~~~~~~~~")
        parsedJSON = getJSONfromText(runType, inputData)
        headerData.direct_json = " direct JSON paste"

    if isinstance(parsedJSON, str):
        if parsedJSON.startswith("JSONParseFail"):
            return parsedJSON
    elif parsedJSON is None:
        if runType == "web":
            raise ValueError(f"data for {inputData} not found")
        elif runType == "consoleTest":
            return "JSONParseFail-NoneType"
    elif parsedJSON == []:
        if runType == "web":
            raise ValueError(f"data for {inputData} not found")
            # return errorListofLists
        elif runType == "consoleTest":
            return "JSONParseFail-EmptyList"
        #raise ValueError(f"data for {inputData} not found")

    #Step 2: Make account data available throughout the session
    g.data = Account(parsedJSON)

    #Step 3: Send that data off to all the different analyzers
    playerCount, playerNames, playerClasses, characterDict = getCharacterDetails(parsedJSON, runType)
    characterDict = {index: Character(**character) for index, character in characterDict.items()}
    for name in playerNames:
        #print("Checking for name in bannedAccountsList:", name.lower(),  (name.lower() in bannedAccountsList))
        if name.lower() in bannedAccountsList:
            if runType == "web":
                print("idleonTaskSuggester~ WARNING! PETTY BITCH MODE ACTIVATED. Banned name entered:", name)
                return bannedListofLists
            elif runType == "consoleTest":
                return "Banned"
    roastworthyBool = getRoastableStatus(playerNames)

    if headerData.direct_json:
        if playerNames[0] == "Character1":
            headerData.json_error = "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
        else:
            headerData.first_name = playerNames[0]

    #General
    headerData.last_update = getLastUpdatedTime(parsedJSON)

    if runType == "web":
        logger.info(f'{headerData.last_update = }')

    section_combatLevels = idleon_CombatLevels.setCombatLevelsProgressionTier(parsedJSON, progressionTiers['Combat Levels'], playerCount, playerNames, playerClasses)
    section_consumables = idleon_Consumables.parseConsumables(parsedJSON, playerCount, playerNames)
    section_gemShop = idleon_GemShop.setGemShopProgressionTier(parsedJSON, progressionTiers['Gem Shop'], playerCount)
    sections_quest_gstacks, section_regular_gstacks = idleon_Greenstacks.setGStackProgressionTier(parsedJSON, playerCount)
    section_maestro = idleon_MaestroHands.getHandsStatus(parsedJSON, playerCount, playerNames)
    section_cards = idleon_Cards.getCardSetReview()

    #World 1
    stamps_AdviceSection = idleon_Stamps.setStampProgressionTier(parsedJSON, progressionTiers['Stamps'])
    bribes_AdviceSection = idleon_Bribes.setBribesProgressionTier(parsedJSON, progressionTiers['Bribes'])
    smithing_AdviceSection = idleon_Smithing.setSmithingProgressionTier(parsedJSON, progressionTiers['Smithing'], playerCount, characterDict)

    #World 2
    alchBubbles_AdviceSection = idleon_Alchemy.setAlchemyBubblesProgressionTier(parsedJSON, progressionTiers['Alchemy Bubbles'], characterDict)
    alchVials_AdviceSection = idleon_Alchemy.setAlchemyVialsProgressionTier(parsedJSON, progressionTiers['Alchemy Vials'], characterDict)
    alchP2W_AdviceSection = idleon_Alchemy.setAlchemyP2W(parsedJSON, characterDict)
    #obols_AdviceSection = idleon_Obols.setObolsProgressionTier(parsedJSON, playerCount, progressionTiers['Obols'], fromPublicIEBool)

    #World 3
    refinery_AdviceSection = idleon_ConsRefinery.setConsRefineryProgressionTier(parsedJSON, progressionTiers['Construction Refinery'], characterDict)
    saltlick_AdviceSection = idleon_ConsSaltLick.setConsSaltLickProgressionTier(parsedJSON, progressionTiers['Construction Salt Lick'], characterDict)
    deathnote_AdviceSection = idleon_ConsDeathNote.setConsDeathNoteProgressionTier(parsedJSON, progressionTiers['Construction Death Note'], characterDict)
    buildings_AdviceSection = idleon_ConsBuildings.setConsBuildingsProgressionTier(parsedJSON, progressionTiers['Construction Buildings Pre-Buffs'], progressionTiers['Construction Buildings Post-Buffs'], characterDict)
    prayers_AdviceSection = idleon_Worship.setWorshipPrayersProgressionTier(parsedJSON, progressionTiers['Worship Prayers'], characterDict)
    trapping_AdviceSection = idleon_Trapping.setTrappingProgressionTier(parsedJSON, characterDict)
    #collider_AdviceSection =
    #worship_AdviceSection =
    #printer_AdviceSection =

    #World 4
    breeding_AdviceSection = idleon_Breeding.setBreedingProgressionTier(parsedJSON, progressionTiers['Breeding'], characterDict)
    #cooking_AdviceSection =
    #lab_AdviceSection =

    #World 5
    #sailing_AdviceSection =
    #gaming_AdviceSection =
    #divinity_AdviceSection =

    #w6list = [["w6 mechanic 1 placeholder"], ["w6 mechanic 2 placeholder"], ["w6 mechanic 3 placeholder"]]
    #w7list = [["w7 mechanic 1 placeholder"], ["w7 mechanic 2 placeholder"], ["w7 mechanic 3 placeholder"]]
    #w8list = [["w8 mechanic 1 placeholder"], ["w8 mechanic 2 placeholder"], ["w8 mechanic 3 placeholder"]]
    biggoleProgressionTiersDict = {
        Placements.COMBAT_LEVELS: section_combatLevels.pinchy_rating,
        Placements.STAMPS: stamps_AdviceSection.pinchy_rating,
        Placements.BRIBES: bribes_AdviceSection.pinchy_rating,
        Placements.SMITHING: smithing_AdviceSection.pinchy_rating,
        Placements.BUBBLES: alchBubbles_AdviceSection.pinchy_rating,
        Placements.VIALS: alchVials_AdviceSection.pinchy_rating,
        Placements.P2W: alchP2W_AdviceSection.pinchy_rating,
        Placements.REFINERY: refinery_AdviceSection.pinchy_rating,
        Placements.SALT_LICK: saltlick_AdviceSection.pinchy_rating,
        Placements.DEATH_NOTE: deathnote_AdviceSection.pinchy_rating,
        Placements.PRAYERS: prayers_AdviceSection.pinchy_rating
        }
    pinchy = idleon_Pinchy.generatePinchyWorld(parsedJSON, playerCount, biggoleProgressionTiersDict)
    generalReview = AdviceWorld(
        name=WorldName.GENERAL,
        sections=[section_combatLevels, section_maestro, *section_consumables, section_gemShop, *sections_quest_gstacks, section_regular_gstacks, section_cards],
        banner="general_banner.jpg"
    )

    w1Review = AdviceWorld(
        name=WorldName.WORLD1,
        sections=[stamps_AdviceSection, bribes_AdviceSection, smithing_AdviceSection],
        banner="w1banner.png"
    )
    w2Review = AdviceWorld(
        name=WorldName.WORLD2,
        sections=[alchBubbles_AdviceSection, alchVials_AdviceSection, alchP2W_AdviceSection],
        banner="w2banner.png"
    )
    w3Review = AdviceWorld(
        name=WorldName.WORLD3,
        sections=[refinery_AdviceSection, buildings_AdviceSection, saltlick_AdviceSection, deathnote_AdviceSection, prayers_AdviceSection, trapping_AdviceSection],
        banner="w3banner.png"
    )
    w4Review = AdviceWorld(
        name=WorldName.WORLD4,
        sections=[breeding_AdviceSection],
        banner="w4banner.png"
    )
    w5Review = AdviceWorld(
        name=WorldName.WORLD5,
        sections=[],
        banner="w5banner.png"
    )

    biggoleAdviceList = [w5Review, w4Review, w3Review, w2Review, w1Review, generalReview, pinchy, headerData]

    if runType == "consoleTest":
        return "Pass"
    else:
        return biggoleAdviceList
