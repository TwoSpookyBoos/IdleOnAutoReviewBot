from pathlib import Path

import yaml
from flask import g as session_data

from config import app
from models.custom_exceptions import UsernameBanned
from models.models import AdviceWorld, WorldName, Account
from utils.data_formatting import getJSONfromAPI, getJSONfromText, HeaderData
from utils.logging import get_logger
from utils.text_formatting import is_username
from general import combatLevels, greenstacks, pinchy, cards, secretPath, consumables, gemShop, active, achievements
from w1 import stamps, bribes, smithing, statues, starsigns, owl
from w2 import alchemy, killroy, islands
from w3 import trapping, consRefinery, consDeathNote, worship, consSaltLick, consBuildings, equinox, library, sampling, collider
from w4 import breeding, cooking, rift
from w5 import slab, divinity, sailing
from w6 import beanstalk, sneaking, farming

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

    #roastworthyBool = getRoastableStatus(session_data.account.names)

    # Step 3: Send that data off to all the different analyzers
    # General
    sections_general = [
        section_combatLevels := combatLevels.setCombatLevelsProgressionTier(),
        section_secretPath := secretPath.setSecretClassProgressionTier(),
        section_active := active.setActiveProgressionTier(),
        section_achievements := achievements.setAchievementsProgressionTier(),
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
        section_statues := statues.setStatuesProgressionTier(),
        section_starsigns := starsigns.setStarsignsProgressionTier(),
        section_owl := owl.setOwlProgressionTier()
    ]
    # World 2
    sections_2 = [
        section_alchBubbles := alchemy.setAlchemyBubblesProgressionTier(),
        section_alchVials := alchemy.setAlchemyVialsProgressionTier(),
        section_alchP2W := alchemy.setAlchemyP2W(),
        section_alchSigils := alchemy.setAlchemySigilsProgressionTier(),
        # section_obols := idleon_Obols.setObolsProgressionTier(),
        section_killroy := killroy.setKillroyProgressionTier(),
        section_islands := islands.setIslandsProgressionTier()
    ]
    # World 3
    sections_3 = [
        section_refinery := consRefinery.setConsRefineryProgressionTier(),
        section_buildings := consBuildings.setConsBuildingsProgressionTier(),
        section_sampling := sampling.setSamplingProgressionTier(),
        section_library := library.setLibraryProgressionTier(),
        section_deathnote := consDeathNote.setConsDeathNoteProgressionTier(),
        section_saltlick := consSaltLick.setConsSaltLickProgressionTier(),
        section_collider := collider.setColliderProgressionTier(),
        # section_worship =
        section_prayers := worship.setWorshipPrayersProgressionTier(),
        section_trapping := trapping.setTrappingProgressionTier(),
        section_equinox := equinox.setEquinoxProgressionTier(),
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
        section_slab := slab.setSlabProgressionTier(),
        section_divinity := divinity.setDivinityProgressionTier(),
        section_sailing := sailing.setSailingProgressionTier()
        # section_gaming =
    ]
    # World 6
    sections_6 = [
        section_farming := farming.setFarmingProgressionTier(),
        section_sneaking := sneaking.setSneakingProgressionTier(),
        section_beanstalk := beanstalk.section_beanstalk(),
    ]

    #Sort sections into rated and unrated
    all_sections = [sections_general, sections_1, sections_2, sections_3, sections_4, sections_5, sections_6]
    unrated_sections = []
    pinchable_sections = []
    for section_list in all_sections:
        for section in section_list:
            if section.unrated:  # and not session_data.account.hide_unrated:
                unrated_sections.append(section)
            else:
                pinchable_sections.append(section)

    #Remove completed sections from Pinchy, if that setting is enabled
    completed_pinchable_sections = []
    # if session_data.account.hide_completed:
    #     completed_pinchable_sections = [section for section in pinchable_sections if section.complete]
    #     pinchable_sections = [section for section in pinchable_sections if not section.complete]
    #     #completed_unrated_sections = [section for section in unrated_sections if section.complete]
    #     unrated_sections = [section for section in unrated_sections if not section.complete]
    sections_pinchy = pinchy.generatePinchyWorld(pinchable_sections, unrated_sections, len(completed_pinchable_sections))

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
    for world in reviews:
        world.hide_unreached_sections()  # Feel free to comment this out while testing
        if session_data.account.hide_completed:
            world.hide_completed_sections()
            for section in world.sections:
                for group in section.groups:
                    group.remove_completed_advices()
                    group.remove_empty_subgroups()
        if session_data.account.hide_unrated:
            world.hide_unrated_sections()
    reviews = [world for world in reviews if len(world.sections) > 0]

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
