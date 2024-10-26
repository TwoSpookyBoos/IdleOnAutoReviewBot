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
        section_combatLevels := combatLevels.getCombatLevelsAdviceSection(),
        section_secretPath := secretPath.getSecretClassAdviceSection(),
        section_active := active.getActiveAdviceSection(),
        section_achievements := achievements.getAchievementsAdviceSection(),
        *(sections_consumables := consumables.getConsumablesAdviceSections()),
        section_gemShop := gemShop.getGemShopAdviceSection(),
        *(sections_gstacks := greenstacks.getGStackAdviceSections()),
        section_cards := cards.getCardsAdviceSection(),
    ]
    # World 1
    sections_1 = [
        section_stamps := stamps.getStampAdviceSection(),
        section_bribes := bribes.getBribesAdviceSection(),
        section_smithing := smithing.getSmithingAdviceSection(),
        section_statues := statues.getStatuesAdviceSection(),
        section_starsigns := starsigns.getStarsignsAdviceSection(),
        section_owl := owl.getOwlAdviceSection()
    ]
    # World 2
    sections_2 = [
        section_alchBubbles := alchemy.getAlchemyBubblesAdviceSection(),
        section_alchVials := alchemy.getAlchemyVialsAdviceSection(),
        section_alchP2W := alchemy.getAlchemyP2WAdviceSection(),
        section_alchSigils := alchemy.getAlchemySigilsAdviceSection(),
        # section_obols := idleon_Obols.setObolsProgressionTier(),
        section_killroy := killroy.getKillroyAdviceSection(),
        section_islands := islands.getIslandsAdviceSection()
    ]
    # World 3
    sections_3 = [
        section_refinery := consRefinery.getConsRefineryAdviceSection(),
        section_buildings := consBuildings.getConsBuildingsAdviceSection(),
        section_sampling := sampling.getSamplingAdviceSection(),
        section_library := library.getLibraryAdviceSection(),
        section_deathnote := consDeathNote.getDeathNoteAdviceSection(),
        section_saltlick := consSaltLick.getSaltLickAdviceSection(),
        section_collider := collider.getColliderAdviceSection(),
        # section_worship =
        section_prayers := worship.getPrayersAdviceSection(),
        section_trapping := trapping.getTrappingAdviceSection(),
        section_equinox := equinox.getEquinoxAdviceSection(),
    ]
    # World 4
    sections_4 = [
        section_breeding := breeding.getBreedingAdviceSection(),
        section_cooking := cooking.getCookingAdviceSection(),
        # section_lab := ,
        section_rift := rift.getRiftAdviceSection(),
    ]
    # World 5
    sections_5 = [
        section_slab := slab.getSlabAdviceSection(),
        section_divinity := divinity.getDivinityAdviceSection(),
        section_sailing := sailing.getSailingAdviceSection()
        # section_gaming =
    ]
    # World 6
    sections_6 = [
        section_farming := farming.setFarmingProgressionTier(),
        section_sneaking := sneaking.getSneakingAdviceSection(),
        section_beanstalk := beanstalk.getBeanstalkAdviceSection(),
    ]

    #Sort sections into rated and unrated, as well as checking for completeness
    all_sections = [sections_general, sections_1, sections_2, sections_3, sections_4, sections_5, sections_6]
    unrated_sections = []
    pinchable_sections = []
    for section_list in all_sections:
        for section in section_list:
            for group in section.groups:
                group.check_for_completeness()
            section.check_for_completeness()
            section.check_for_informationalness()
            logger.debug(
                (f"{section} {section.tier}: "
                 f"Unreached={section.unreached}, "
                 f"Unrated={section.unrated}, "
                 f"Complete={section.complete}, "
                 f"Info={section.informational}"
                 )
            )
            if section.unrated:
                unrated_sections.append(section)
            else:
                pinchable_sections.append(section)

    #Pinchy Evaluation
    sections_pinchy = pinchy.generatePinchyWorld(pinchable_sections, unrated_sections)
    for section in sections_pinchy:
        for group in section.groups:
            group.check_for_completeness()
        section.check_for_completeness()
        section.check_for_informationalness()
        #logger.debug(f"{section}: Unreached={section.unreached}, Complete={section.complete}, Info={section.informational}, Unrated={section.unrated}")

    #Build Worlds
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
        logger.debug(f"{world}: Unrated={world.unrated}, Complete={world.complete}, Info={world.informational}")
        continue

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
