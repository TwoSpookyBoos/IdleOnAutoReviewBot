from pathlib import Path

import yaml
from flask import g as session_data

from config import app
from general import combatLevels, greenstacks, pinchy, cards, secretPath, consumables, gemShop
from models.custom_exceptions import UsernameBanned
from models.models import AdviceWorld, WorldName, Account
from utils.data_formatting import getJSONfromAPI, getJSONfromText, HeaderData
from utils.logging import get_logger
from utils.text_formatting import is_username
from w1 import stamps, bribes, smithing
from w2 import alchemy
from w3 import trapping, consRefinery, consDeathNote, worship, consSaltLick, consBuildings, equinox
from w4 import breeding, cooking, rift
from w5 import divinity
from w6 import beanstalk

logger = get_logger(__name__)


def maybe_ban(username, runType):
    bannedAccountsList = yaml.load(open(Path(app.static_folder) / "banned.yaml"), yaml.Loader)

    if username in bannedAccountsList:
        if runType == "consoleTest":
            return "Banned"

        raise UsernameBanned(username)


def getRoastableStatus(playerNames):
    roastworthyList = yaml.load(open(Path(app.static_folder) / "roastable.yaml"), yaml.Loader)
    return next((name.lower() in roastworthyList for name in playerNames), False)


def main(inputData, runType="web"):
    if is_username(inputData):
        maybe_ban(inputData, runType)

    # Step 1: Retrieve data from public IdleonEfficiency website or from file
    parsedJSON = get_or_parse_json(inputData, runType)

    # Step 2: Make account data available throughout the session
    session_data.account = Account(parsedJSON)

    for name in session_data.account.names:
        maybe_ban(name, runType)

    roastworthyBool = getRoastableStatus(session_data.account.names)

    # Step 3: Send that data off to all the different analyzers
    # General
    sections_general = [
        section_combatLevels := combatLevels.setCombatLevelsProgressionTier(),
        section_secretPath := secretPath.setSecretClassProgressionTier(),
        *(sections_consumables := consumables.parseConsumables()),
        section_gemShop := gemShop.setGemShopProgressionTier(),
        *(sections_gstacks := greenstacks.setGStackProgressionTier()),
        section_cards := cards.getCardSetReview(),
    ]
    # World 1
    sections_1 = [
        section_stamps := stamps.setStampProgressionTier(),
        section_bribes := bribes.setBribesProgressionTier(),
        section_smithing := smithing.setSmithingProgressionTier(),
    ]

    # World 2
    sections_2 = [
        section_alchBubbles := alchemy.setAlchemyBubblesProgressionTier(),
        section_alchVials := alchemy.setAlchemyVialsProgressionTier(),
        section_alchP2W := alchemy.setAlchemyP2W(),
        # section_obols := idleon_Obols.setObolsProgressionTier()
    ]

    # World 3
    sections_3 = [
        section_refinery := consRefinery.setConsRefineryProgressionTier(),
        section_saltlick := consSaltLick.setConsSaltLickProgressionTier(),
        section_deathnote := consDeathNote.setConsDeathNoteProgressionTier(),
        section_buildings := consBuildings.setConsBuildingsProgressionTier(),
        section_prayers := worship.setWorshipPrayersProgressionTier(),
        section_trapping := trapping.setTrappingProgressionTier(),
        section_equinox := equinox.setEquinoxProgressionTier(),
        # section_collider =
        # section_worship =
        # section_printer =
    ]
    # World 4
    sections_4 = [
        section_breeding := breeding.setBreedingProgressionTier(),
        section_cooking := cooking.setCookingProgressionTier(),
        # section_lab := ,
        section_rift := rift.setRiftProgressionTier(),
    ]
    # World 5
    sections_5 = [
        section_divinity := divinity.setDivinityProgressionTier(),
        # section_sailing =
        # section_gaming =
    ]
    # World 6
    sections_6 = [
        section_beanstalk := beanstalk.section_beanstalk(),
    ]

    pinchable_sections = [
        section_combatLevels, section_secretPath,
        section_stamps, section_bribes, section_smithing,
        section_alchBubbles, section_alchVials, section_alchP2W,
        section_refinery, section_saltlick, section_deathnote, section_prayers, section_equinox,
        section_breeding, section_cooking, section_rift,
        section_divinity
    ]
    sections_pinchy = pinchy.generatePinchyWorld(pinchable_sections)

    reviews = [
        AdviceWorld(name=WorldName.PINCHY, sections=sections_pinchy, title="Pinchy AutoReview", collapse=False),
        AdviceWorld(name=WorldName.GENERAL, sections=sections_general, banner="general_banner.jpg"),
        AdviceWorld(name=WorldName.BLUNDER_HILLS, sections=sections_1, banner="w1banner.png"),
        AdviceWorld(name=WorldName.YUMYUM_DESERT, sections=sections_2, banner="w2banner.png"),
        AdviceWorld(name=WorldName.FROSTBITE_TUNDRA, sections=sections_3, banner="w3banner.png"),
        AdviceWorld(name=WorldName.HYPERION_NEBULA, sections=sections_4, banner="w4banner.png"),
        AdviceWorld(name=WorldName.SMOLDERIN_PLATEAU, sections=sections_5, banner="w5banner.png"),
        AdviceWorld(name=WorldName.SPIRITED_VALLEY, sections=sections_6, banner="w6banner.png"),
    ]

    headerData = HeaderData(inputData)
    logger.info(f"{headerData.last_update = }")

    if runType == "consoleTest":
        return "Pass"
    else:
        return reviews, headerData


def get_or_parse_json(inputData, runType):
    if is_username(inputData):
        return getJSONfromAPI(runType, inputData)

    return getJSONfromText(runType, inputData)
