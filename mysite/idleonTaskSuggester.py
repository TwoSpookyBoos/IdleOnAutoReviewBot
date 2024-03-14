#idleonTaskSuggester.py
import datetime
import copy
from flask import g as session_data

import idleon_Rift
from data_formatting import getJSONfromAPI, getJSONfromText, getLastUpdatedTime, getCharacterDetails, HeaderData
#general stuff that makes this file too big if I include directly
from models import AdviceWorld, WorldName, Account, Character

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
import idleon_Rift
from utils import get_logger


logger = get_logger(__name__)


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
        headerData.data_source = headerData.PUBLIC
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
        headerData.data_source = HeaderData.JSON
        if runType == "web":
            print("~~~~~~~~~~~~~~~ Starting up PROD main at", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "for direct web JSON input.~~~~~~~~~~~~~~~")
        parsedJSON = getJSONfromText(runType, inputData)

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
    session_data.account = Account(parsedJSON)

    #Step 3: Send that data off to all the different analyzers
    for name in session_data.account.names:
        #print("Checking for name in bannedAccountsList:", name.lower(),  (name.lower() in bannedAccountsList))
        if name.lower() in bannedAccountsList:
            if runType == "web":
                print("idleonTaskSuggester~ WARNING! PETTY BITCH MODE ACTIVATED. Banned name entered:", name)
                return bannedListofLists
            elif runType == "consoleTest":
                return "Banned"
    roastworthyBool = getRoastableStatus(session_data.account.names)

    if headerData.data_source == HeaderData.JSON:
        if session_data.account.names[0] == "Character1":
            headerData.json_error = "NO SORTED LIST OF CHARACTER NAMES FOUND IN DATA. REPLACING WITH GENERIC NUMBER ORDER."
        else:
            headerData.first_name = session_data.account.names[0]

    #General
    getLastUpdatedTime(headerData)

    if runType == "web":
        logger.info(f'{headerData.last_update = }')

    section_combatLevels = idleon_CombatLevels.setCombatLevelsProgressionTier()
    section_consumables = idleon_Consumables.parseConsumables()
    section_gemShop = idleon_GemShop.setGemShopProgressionTier()
    sections_quest_gstacks, section_regular_gstacks = idleon_Greenstacks.setGStackProgressionTier()
    section_maestro = idleon_MaestroHands.getHandsStatus()
    section_cards = idleon_Cards.getCardSetReview()

    #World 1
    stamps_AdviceSection = idleon_Stamps.setStampProgressionTier()
    bribes_AdviceSection = idleon_Bribes.setBribesProgressionTier()
    smithing_AdviceSection = idleon_Smithing.setSmithingProgressionTier()

    #World 2
    alchBubbles_AdviceSection = idleon_Alchemy.setAlchemyBubblesProgressionTier()
    alchVials_AdviceSection = idleon_Alchemy.setAlchemyVialsProgressionTier()
    alchP2W_AdviceSection = idleon_Alchemy.setAlchemyP2W()
    #obols_AdviceSection = idleon_Obols.setObolsProgressionTier(parsedJSON, playerCount, progressionTiers['Obols'], fromPublicIEBool)

    #World 3
    refinery_AdviceSection = idleon_ConsRefinery.setConsRefineryProgressionTier()
    saltlick_AdviceSection = idleon_ConsSaltLick.setConsSaltLickProgressionTier()
    deathnote_AdviceSection = idleon_ConsDeathNote.setConsDeathNoteProgressionTier()
    buildings_AdviceSection = idleon_ConsBuildings.setConsBuildingsProgressionTier()
    prayers_AdviceSection = idleon_Worship.setWorshipPrayersProgressionTier()
    trapping_AdviceSection = idleon_Trapping.setTrappingProgressionTier()
    #collider_AdviceSection =
    #worship_AdviceSection =
    #printer_AdviceSection =

    #World 4
    breeding_AdviceSection = idleon_Breeding.setBreedingProgressionTier()
    #cooking_AdviceSection =
    #lab_AdviceSection =
    rift_AdviceSection = idleon_Rift.setRiftProgressionTier()

    #World 5
    #sailing_AdviceSection =
    #gaming_AdviceSection =
    #divinity_AdviceSection =

    #w6list = [["w6 mechanic 1 placeholder"], ["w6 mechanic 2 placeholder"], ["w6 mechanic 3 placeholder"]]
    #w7list = [["w7 mechanic 1 placeholder"], ["w7 mechanic 2 placeholder"], ["w7 mechanic 3 placeholder"]]
    #w8list = [["w8 mechanic 1 placeholder"], ["w8 mechanic 2 placeholder"], ["w8 mechanic 3 placeholder"]]
    all_sections = [
        section_combatLevels,
        stamps_AdviceSection, bribes_AdviceSection, smithing_AdviceSection,
        alchBubbles_AdviceSection, alchVials_AdviceSection, alchP2W_AdviceSection,
        refinery_AdviceSection, saltlick_AdviceSection, deathnote_AdviceSection, prayers_AdviceSection,
    ]
    pinchy_high, pinchy_low, pinchy_all = idleon_Pinchy.generatePinchyWorld(all_sections)

    pinchyReview = AdviceWorld(
        name=WorldName.PINCHY,
        sections=[pinchy_high, pinchy_low, pinchy_all],
        collapse=False,
        title="Pinchy AutoReview"
    )
    generalReview = AdviceWorld(
        name=WorldName.GENERAL,
        sections=[section_combatLevels, section_maestro, *section_consumables, section_gemShop, *sections_quest_gstacks, section_regular_gstacks, section_cards],
        banner="general_banner.jpg"
    )
    w1Review = AdviceWorld(
        name=WorldName.BLUNDER_HILLS,
        sections=[stamps_AdviceSection, bribes_AdviceSection, smithing_AdviceSection],
        banner="w1banner.png"
    )
    w2Review = AdviceWorld(
        name=WorldName.YUMYUM_DESERT,
        sections=[alchBubbles_AdviceSection, alchVials_AdviceSection, alchP2W_AdviceSection],
        banner="w2banner.png"
    )
    w3Review = AdviceWorld(
        name=WorldName.FROSTBITE_TUNDRA,
        sections=[refinery_AdviceSection, buildings_AdviceSection, saltlick_AdviceSection, deathnote_AdviceSection, prayers_AdviceSection, trapping_AdviceSection],
        banner="w3banner.png"
    )
    w4Review = AdviceWorld(
        name=WorldName.HYPERION_NEBULA,
        sections=[breeding_AdviceSection, rift_AdviceSection],
        banner="w4banner.png"
    )
    w5Review = AdviceWorld(
        name=WorldName.SMOLDERIN_PLATEAU,
        banner="w5banner.png"
    )

    reviews = [pinchyReview, generalReview, w1Review, w2Review, w3Review, w4Review, w5Review]

    if runType == "consoleTest":
        return "Pass"
    else:
        return reviews, headerData
