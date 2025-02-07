from pathlib import Path

import yaml
from flask import g as session_data

import models.account_calcs
import models.account_parser
from config import app
from consts import versions_patches
from models.custom_exceptions import UsernameBanned
from models.models import AdviceWorld, WorldName, Account
from utils.data_formatting import getJSONfromAPI, getJSONfromText, HeaderData, safer_convert
from utils.logging import get_logger
from utils.text_formatting import is_username
from general import combatLevels, greenstacks, pinchy, cards, secretPath, consumables, gemShop, active, achievements, eventShop, grimoire
from w1 import upgrade_vault, stamps, bribes, smithing, statues, starsigns, owl
from w2 import alchemy, post_office, killroy, islands, arcade, bonus_ballot
from w3 import trapping, consRefinery, consDeathNote, worship, consSaltLick, consBuildings, equinox, library, sampling, collider
from w4 import breeding, cooking, rift
from w5 import slab, divinity, sailing
from caverns import villagers, shallow_caverns, glowshroom_tunnels
from w6 import beanstalk, sneaking, farming, summoning

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

    patch_guess = ''
    for version in versions_patches:
        if session_data.account.version > version:
            patch_guess = versions_patches[version]
    logger.info(f"Data version {session_data.account.version}: {patch_guess} or later")
    models.account_parser.parse_account(session_data.account, runType)
    models.account_calcs.calculate_account(session_data.account)

    for name in session_data.account.names:
        maybe_ban(name, runType)

    #roastworthyBool = getRoastableStatus(session_data.account.names)

    # Step 3: Send that data off to all the different analyzers
    all_sections = [
        sections_general := [
            combatLevels.getCombatLevelsAdviceSection(),
            secretPath.getSecretClassAdviceSection(),
            active.getActiveAdviceSection(),
            achievements.getAchievementsAdviceSection(),
            *(consumables.getConsumablesAdviceSections()),
            gemShop.getGemShopAdviceSection(),
            *(greenstacks.getGStackAdviceSections()),
            cards.getCardsAdviceSection(),
            eventShop.getEvent_ShopAdviceSection(),
            grimoire.getGrimoireAdviceSection()
        ],
        sections_1 := [
            upgrade_vault.getVaultAdviceSection(),
            stamps.getStampAdviceSection(),
            bribes.getBribesAdviceSection(),
            smithing.getSmithingAdviceSection(),
            statues.getStatuesAdviceSection(),
            starsigns.getStarsignsAdviceSection(),
            owl.getOwlAdviceSection()
        ],
        sections_2 := [
            alchemy.getAlchemyBubblesAdviceSection(),
            alchemy.getAlchemyVialsAdviceSection(),
            alchemy.getAlchemyP2WAdviceSection(),
            alchemy.getAlchemySigilsAdviceSection(),
            post_office.getPostOfficeAdviceSection(),
            killroy.getKillroyAdviceSection(),
            islands.getIslandsAdviceSection(),
            arcade.getArcadeAdviceSection(),
            bonus_ballot.getBonus_BallotAdviceSection()
        ],
        sections_3 := [
            consRefinery.getConsRefineryAdviceSection(),
            consBuildings.getConsBuildingsAdviceSection(),
            sampling.getSamplingAdviceSection(),
            library.getLibraryAdviceSection(),
            consDeathNote.getDeathNoteAdviceSection(),
            consSaltLick.getSaltLickAdviceSection(),
            collider.getColliderAdviceSection(),
            worship.getPrayersAdviceSection(),
            trapping.getTrappingAdviceSection(),
            equinox.getEquinoxAdviceSection(),
        ],
        sections_4 := [
            breeding.getBreedingAdviceSection(),
            cooking.getCookingAdviceSection(),
            rift.getRiftAdviceSection(),
        ],
        sections_5 := [
            slab.getSlabAdviceSection(),
            divinity.getDivinityAdviceSection(),
            sailing.getSailingAdviceSection(),
        ],
        sections_caverns := [
            villagers.getVillagersAdviceSection(),
            shallow_caverns.getShallowCavernsAdviceSection(),
            glowshroom_tunnels.getGlowshroomTunnelsAdviceSection()
        ],
        sections_6 := [
            farming.setFarmingProgressionTier(),
            summoning.getSummoningAdviceSection(),
            sneaking.getSneakingAdviceSection(),
            beanstalk.getBeanstalkAdviceSection(),
        ],
    ]

    #Sort sections into rated and unrated, as well as checking for completeness
    unrated_sections = []
    pinchable_sections = []
    for section_list in all_sections:
        for section in section_list:
            for group in section.groups:
                group.check_for_completeness()
            section.check_for_completeness()
            section.check_for_informationalness()
            # logger.debug(
            #     (f"{section} {section.tier}: "
            #      f"Unreached={section.unreached}, "
            #      f"Unrated={section.unrated}, "
            #      f"Completed={section.completed}, "
            #      f"Info={section.informational}"
            #      )
            # )
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
        #logger.debug(f"{section}: Unreached={section.unreached}, Completed={section.completed}, Info={section.informational}, Unrated={section.unrated}")

    #Remove the later-rated sections if Overwhelmed mode is on
    if session_data.overwhelmed:
        sections_to_keep = []
        for section in sections_pinchy:
            if section.name == 'Pinchy all':
                for group in section.groups:
                    # Skip the Alerts group, if it exists
                    if group.pre_string == 'Alerts':
                        continue
                    for advice in group.advices['default']:
                        sections_to_keep.append(advice.label)
                    break

        #Remove all the later-rated Sections
        sections_general = [section for section in sections_general if section.name in sections_to_keep]
        sections_1 = [section for section in sections_1 if section.name in sections_to_keep]
        sections_2 = [section for section in sections_2 if section.name in sections_to_keep]
        sections_3 = [section for section in sections_3 if section.name in sections_to_keep]
        sections_4 = [section for section in sections_4 if section.name in sections_to_keep]
        sections_5 = [section for section in sections_5 if section.name in sections_to_keep]
        sections_caverns = [section for section in sections_caverns if section.name in sections_to_keep]
        sections_6 = [section for section in sections_6 if section.name in sections_to_keep]

        #Remove later-rated Groups within the remaining Sections
        for section_list in [sections_general, sections_1, sections_2, sections_3, sections_4, sections_5, sections_caverns, sections_6]:
            for s in section_list:
                #logger.debug(f"{s.name} started with {len(s.groups)}")
                s.groups = [group for group in s.groups if safer_convert(group.tier, 0) <= s.pinchy_rating and not group.informational]
                #logger.debug(f"{s.name} ended with {len(s.groups)}")

    #Build Worlds
    reviews = [
        AdviceWorld(name=WorldName.PINCHY, sections=sections_pinchy, title="Pinchy AutoReview", collapse=False, complete=False),
        AdviceWorld(name=WorldName.GENERAL, sections=sections_general, banner=["generalbanner.jpg", "generalbannertext.png"]),
        AdviceWorld(name=WorldName.BLUNDER_HILLS, sections=sections_1, banner=["w1banner.png", "w1bannertext.png"]),
        AdviceWorld(name=WorldName.YUMYUM_DESERT, sections=sections_2, banner=["w2banner.png", "w2bannertext.png"]),
        AdviceWorld(name=WorldName.FROSTBITE_TUNDRA, sections=sections_3, banner=["w3banner.png", "w3bannertext.png"]),
        AdviceWorld(name=WorldName.HYPERION_NEBULA, sections=sections_4, banner=["w4banner.png", "w4bannertext.png"]),
        AdviceWorld(name=WorldName.SMOLDERIN_PLATEAU, sections=sections_5, banner=["w5banner.png", "w5bannertext.png"]),
        AdviceWorld(name=WorldName.CAVERNS, sections=sections_caverns, banner=["cavernsbanner.png", "cavernsbannertext.png"]),
        AdviceWorld(name=WorldName.SPIRITED_VALLEY, sections=sections_6, banner=["w6banner.png", "w6bannertext.png"]),
    ]

    for world in reviews:
        world.hide_unreached_sections()  # Feel free to comment this out while testing
        #logger.debug(f"{world}: Unrated={world.unrated}, Complete={world.complete}, Info={world.informational}")
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
