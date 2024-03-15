from pathlib import Path

import yaml
from flask import g as session_data

from config import app
from general import combatLevels, greenstacks, pinchy, cards, maestroHands, consumables, gemShop
from models.custom_exceptions import UsernameBanned
# general stuff that makes this file too big if I include directly
from models.models import AdviceWorld, WorldName, Account
from utils.data_formatting import (
    getJSONfromAPI,
    getJSONfromText,
    HeaderData,
)
from utils.logging import get_logger
from utils.text_formatting import is_username
from w1 import stamps, bribes, smithing
from w2 import alchemy
from w3 import trapping, consRefinery, consDeathNote, worship, consSaltLick, consBuildings
from w4 import breeding, rift


logger = get_logger(__name__)


def maybe_ban(username, runType):
    bannedAccountsList = yaml.load(
        open(Path(app.static_folder) / "banned.yaml"), yaml.Loader
    )

    if username in bannedAccountsList:
        if runType == "consoleTest":
            return "Banned"

        raise UsernameBanned(username)


def getRoastableStatus(playerNames):
    roastworthyList = ["scoli", "weebgasm", "herusx", "rashaken", "trickzbunny", "redpaaaaanda"]
    return next((name.lower() in roastworthyList for name in playerNames), False)


def main(inputData, runType="web"):
    if is_username(inputData):
        maybe_ban(inputData, runType)

    # Step 1: Retrieve data from public IdleonEfficiency website or from file
    parsedJSON = get_or_parse_json(inputData, runType)

    for name in session_data.account.names:
        maybe_ban(name, runType)

    # Step 2: Make account data available throughout the session
    session_data.account = Account(parsedJSON)

    # roastworthyBool = getRoastableStatus(session_data.account.names)

    headerData = HeaderData(inputData)
    logger.info(f"{headerData.last_update = }")


    # Step 3: Send that data off to all the different analyzers
    # General
    section_combatLevels = combatLevels.setCombatLevelsProgressionTier()
    sections_consumables = consumables.parseConsumables()
    section_gemShop = gemShop.setGemShopProgressionTier()
    sections_gstacks = greenstacks.setGStackProgressionTier()
    section_maestro = maestroHands.getHandsStatus()
    section_cards = cards.getCardSetReview()

    # World 1
    section_stamps = stamps.setStampProgressionTier()
    section_bribes = bribes.setBribesProgressionTier()
    section_smithing = smithing.setSmithingProgressionTier()

    # World 2
    section_alchBubbles = alchemy.setAlchemyBubblesProgressionTier()
    section_alchVials = alchemy.setAlchemyVialsProgressionTier()
    section_alchP2W = alchemy.setAlchemyP2W()
    # section_obols = idleon_Obols.setObolsProgressionTier(parsedJSON, playerCount, progressionTiers['Obols'], fromPublicIEBool)

    # World 3
    section_refinery = consRefinery.setConsRefineryProgressionTier()
    section_saltlick = consSaltLick.setConsSaltLickProgressionTier()
    section_deathnote = consDeathNote.setConsDeathNoteProgressionTier()
    section_buildings = consBuildings.setConsBuildingsProgressionTier()
    section_prayers = worship.setWorshipPrayersProgressionTier()
    section_trapping = trapping.setTrappingProgressionTier()
    # section_collider =
    # section_worship =
    # section_printer =

    # World 4
    section_breeding = breeding.setBreedingProgressionTier()
    # section_cooking =
    # section_lab =
    section_rift = rift.setRiftProgressionTier()

    # World 5
    # section_sailing =
    # section_gaming =
    # section_divinity =

    # w6list = [["w6 mechanic 1 placeholder"], ["w6 mechanic 2 placeholder"], ["w6 mechanic 3 placeholder"]]
    # w7list = [["w7 mechanic 1 placeholder"], ["w7 mechanic 2 placeholder"], ["w7 mechanic 3 placeholder"]]
    # w8list = [["w8 mechanic 1 placeholder"], ["w8 mechanic 2 placeholder"], ["w8 mechanic 3 placeholder"]]
    all_sections = [
        section_combatLevels,
        section_stamps, section_bribes, section_smithing,
        section_alchBubbles, section_alchVials, section_alchP2W,
        section_refinery, section_saltlick, section_deathnote, section_prayers,
        section_breeding, section_rift
    ]
    sections_pinchy = pinchy.generatePinchyWorld(all_sections)

    pinchyReview = AdviceWorld(
        name=WorldName.PINCHY,
        sections=sections_pinchy,
        collapse=False,
        title="Pinchy AutoReview"
    )
    generalReview = AdviceWorld(
        name=WorldName.GENERAL,
        sections=[section_combatLevels, section_maestro, *sections_consumables, section_gemShop, *sections_gstacks, section_cards],
        banner="general_banner.jpg"
    )
    w1Review = AdviceWorld(
        name=WorldName.BLUNDER_HILLS,
        sections=[section_stamps, section_bribes, section_smithing],
        banner="w1banner.png"
    )
    w2Review = AdviceWorld(
        name=WorldName.YUMYUM_DESERT,
        sections=[section_alchBubbles, section_alchVials, section_alchP2W],
        banner="w2banner.png"
    )
    w3Review = AdviceWorld(
        name=WorldName.FROSTBITE_TUNDRA,
        sections=[section_refinery, section_buildings, section_saltlick, section_deathnote, section_prayers, section_trapping],
        banner="w3banner.png"
    )
    w4Review = AdviceWorld(
        name=WorldName.HYPERION_NEBULA,
        sections=[section_breeding, section_rift],
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


def get_or_parse_json(inputData, runType):
    if is_username(inputData):
        parsedJSON = getJSONfromAPI(runType, inputData)
    else:
        parsedJSON = getJSONfromText(runType, inputData)
    return parsedJSON
