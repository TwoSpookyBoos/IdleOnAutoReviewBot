from pathlib import Path

import yaml
from flask import g as session_data

import models.account_calcs
import models.account_parser
from config import app
from consts.consts_autoreview import versions_patches
from models.custom_exceptions import UsernameBanned
from models.models import AdviceWorld, WorldName, Account
from utils.data_formatting import getJSONfromAPI, getJSONfromText, HeaderData
from utils.logging import get_logger
from utils.text_formatting import is_username
from general import combat_levels, greenstacks, pinchy, cards, secret_path, consumables, gem_shop, active, achievements, event_shop, drop_rate
from master_classes import grimoire, compass
from w1 import upgrade_vault, stamps, bribes, smithing, statues, starsigns, owl
from w2 import alchemy_vials, alchemy_bubbles, alchemy_p2w, alchemy_sigils, post_office, killroy, islands, arcade, bonus_ballot
from w3 import trapping, refinery, death_note, worship, salt_lick, buildings, equinox, library, sampling, atom_collider, armor_sets
from w4 import breeding, cooking, rift
from w5 import slab, divinity, sailing, gaming
from caverns import villagers, shallow_caverns, glowshroom_tunnels, underground_overgrowth
from w6 import beanstalk, sneaking, farming, summoning, emperor

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

def get_or_parse_json(inputData, source_string, runType):
    if is_username(inputData):
        return getJSONfromAPI(runType, inputData, source_string)

    return getJSONfromText(runType, inputData)


def main(inputData, source_string, runType="web"):
    if is_username(inputData):
        maybe_ban(inputData, runType)

    # Step 1: Retrieve data from public IdleonEfficiency website or from file
    parsedJSON, verified_source_string = get_or_parse_json(inputData, source_string, runType)

    # Step 2: Make account data available throughout the session
    session_data.account = Account(parsedJSON, source_string)

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
    # finalize_progression_tiers()
    all_sections = {
        WorldName.GENERAL: [
            combat_levels.getCombatLevelsAdviceSection(),
            secret_path.getSecretClassAdviceSection(),
            active.getActiveAdviceSection(),
            drop_rate.get_drop_rate_advice_section(),
            achievements.getAchievementsAdviceSection(),
            *(consumables.getConsumablesAdviceSections()),
            gem_shop.getGemShopAdviceSection(),
            *(greenstacks.getGStackAdviceSections()),
            cards.getCardsAdviceSection(),
            event_shop.getEvent_ShopAdviceSection(),
        ],
        WorldName.MASTER_CLASSES: [
            grimoire.getGrimoireAdviceSection(),
            compass.getCompassAdviceSection()
        ],
        WorldName.BLUNDER_HILLS: [
            upgrade_vault.getVaultAdviceSection(),
            stamps.getStampAdviceSection(),
            bribes.getBribesAdviceSection(),
            smithing.getSmithingAdviceSection(),
            statues.getStatuesAdviceSection(),
            starsigns.getStarsignsAdviceSection(),
            owl.getOwlAdviceSection()
        ],
        WorldName.YUM_YUM_DESERT: [
            alchemy_bubbles.getAlchemyBubblesAdviceSection(),
            alchemy_vials.getAlchemyVialsAdviceSection(),
            alchemy_p2w.getAlchemyP2WAdviceSection(),
            alchemy_sigils.getAlchemySigilsAdviceSection(),
            post_office.getPostOfficeAdviceSection(),
            killroy.getKillroyAdviceSection(),
            islands.getIslandsAdviceSection(),
            arcade.getArcadeAdviceSection(),
            bonus_ballot.getBonus_BallotAdviceSection()
        ],
        WorldName.FROSTBITE_TUNDRA: [
            armor_sets.getArmorSetsAdviceSection(),
            refinery.getConsRefineryAdviceSection(),
            buildings.getConsBuildingsAdviceSection(),
            sampling.getSamplingAdviceSection(),
            library.getLibraryAdviceSection(),
            death_note.getDeathNoteAdviceSection(),
            salt_lick.getSaltLickAdviceSection(),
            atom_collider.getColliderAdviceSection(),
            worship.getPrayersAdviceSection(),
            trapping.getTrappingAdviceSection(),
            equinox.getEquinoxAdviceSection(),
        ],
        WorldName.HYPERION_NEBULA: [
            breeding.getBreedingAdviceSection(),
            cooking.getCookingAdviceSection(),
            rift.getRiftAdviceSection(),
        ],
        WorldName.SMOLDERIN__PLATEAU: [
            slab.getSlabAdviceSection(),
            divinity.getDivinityAdviceSection(),
            sailing.getSailingAdviceSection(),
            gaming.getGamingAdviceSection(),
        ],
        WorldName.CAVERNS: [
            villagers.getVillagersAdviceSection(),
            shallow_caverns.getShallowCavernsAdviceSection(),
            glowshroom_tunnels.getGlowshroomTunnelsAdviceSection(),
            underground_overgrowth.getUndergroundOvergrowthAdviceSection()
        ],
        WorldName.SPIRITED_VALLEY: [
            farming.getFarmingAdviceSection(),
            summoning.getSummoningAdviceSection(),
            sneaking.getSneakingAdviceSection(),
            beanstalk.getBeanstalkAdviceSection(),
            emperor.getEmperorAdviceSection()
        ],
    }

    #Sort sections into rated and unrated, as well as checking for completeness
    unrated_sections = []
    pinchable_sections = []
    for world_name, section_list in all_sections.items():
        for section in section_list:
            section.world_name = world_name
            for group in section.groups:
                group.check_for_completeness()
            section.check_for_completeness()
            section.check_for_informationalness()
            section.check_for_optional()
            # logger.debug(
            #     (f"{section} {section.tier}: "
            #      f"Unreached={section.unreached}, "
            #      f"Unrated={section.unrated}, "
            #      f"Completed={section.completed}, "
            #      f"Info={section.informational}"
            #      )
            # )
            if section.unrated:
                unrated_sections.append((world_name, section))
            else:
                pinchable_sections.append((world_name, section))

    #Pinchy Evaluation
    sections_pinchy = pinchy.generatePinchyWorld(pinchable_sections, unrated_sections)
    for section in sections_pinchy:
        for group in section.groups:
            group.check_for_completeness()
        section.check_for_completeness()
        section.check_for_informationalness()
        section.check_for_optional()
        #logger.debug(f"{section}: Unreached={section.unreached}, Completed={section.completed}, Info={section.informational}, Unrated={section.unrated}")

    #Remove the later-rated sections if Overwhelmed mode is on
    # if session_data.overwhelmed:
    placements_count = 0
    sections_to_keep = []
    for section in sections_pinchy:
        if section.name == 'Pinchy all':
            for group in section.groups:
                # Skip the Alerts group, if it exists
                if group.pre_string == 'Alerts':
                    continue
                placements_count += 1
                for advice in group.advices['default']:
                    if placements_count >= session_data.account.max_subgroups + 1:
                        # Currently this should break after 2
                        advice.overwhelming = True
                    else:
                        advice.overwhelming = False
                        sections_to_keep.append(advice.label)

        #Remove all the later-rated Sections
        # sections_general = [section for section in sections_general if section.name in sections_to_keep]
        # sections_master_classes = [section for section in sections_master_classes if section.name in sections_to_keep]
        # sections_blunder_hills = [section for section in sections_blunder_hills if section.name in sections_to_keep]
        # sections_yum_yum_desert = [section for section in sections_yum_yum_desert if section.name in sections_to_keep]
        # sections_frostbite_tundra = [section for section in sections_frostbite_tundra if section.name in sections_to_keep]
        # sections_hyperion_nebula = [section for section in sections_hyperion_nebula if section.name in sections_to_keep]
        # sections_smolderin__plateau = [section for section in sections_smolderin__plateau if section.name in sections_to_keep]
        # sections_caverns = [section for section in sections_caverns if section.name in sections_to_keep]
        # sections_spirited_valley = [section for section in sections_spirited_valley if section.name in sections_to_keep]

        #Remove later-rated Groups within the remaining Sections
        for section_list in all_sections.values():
            for s in section_list:
                s.set_overwhelming(s.name not in sections_to_keep)
                # logger.debug(f"{s.name} started with {len(s.groups)}")
                # s.groups = [group for group in s.groups if safer_convert(group.tier, 0) <= s.pinchy_rating and not group.informational]
                # logger.debug(f"{s.name} ended with {len(s.groups)}")

    #Build Worlds
    reviews = [
        AdviceWorld(name=WorldName.PINCHY, sections=sections_pinchy, title='Pinchy AutoReview', collapse=False,
                    complete=False, optional=False, informational=False, unrated=False),
        AdviceWorld(name=WorldName.GENERAL, sections=all_sections[WorldName.GENERAL], banner=['generalbanner.jpg', 'generalbannertext.png']),
        AdviceWorld(name=WorldName.MASTER_CLASSES, sections=all_sections[WorldName.MASTER_CLASSES], banner=['master_classes_banner.png', 'master_classes_banner_text.png']),
        AdviceWorld(name=WorldName.BLUNDER_HILLS, sections=all_sections[WorldName.BLUNDER_HILLS], banner=['w1banner.png', 'w1bannertext.png']),
        AdviceWorld(name=WorldName.YUM_YUM_DESERT, sections=all_sections[WorldName.YUM_YUM_DESERT], banner=['w2banner.png', 'w2bannertext.png']),
        AdviceWorld(name=WorldName.FROSTBITE_TUNDRA, sections=all_sections[WorldName.FROSTBITE_TUNDRA], banner=['w3banner.png', 'w3bannertext.png']),
        AdviceWorld(name=WorldName.HYPERION_NEBULA, sections=all_sections[WorldName.HYPERION_NEBULA], banner=['w4banner.png', 'w4bannertext.png']),
        AdviceWorld(name=WorldName.SMOLDERIN__PLATEAU, sections=all_sections[WorldName.SMOLDERIN__PLATEAU], banner=['w5banner.png', 'w5bannertext.png']),
        AdviceWorld(name=WorldName.CAVERNS, sections=all_sections[WorldName.CAVERNS], banner=['cavernsbanner.png', 'cavernsbannertext.png']),
        AdviceWorld(name=WorldName.SPIRITED_VALLEY, sections=all_sections[WorldName.SPIRITED_VALLEY], banner=['w6banner.png', 'w6bannertext.png']),
    ]

    for world in reviews:
        world.hide_unreached_sections()  # Feel free to comment this out while testing
        world.check_for_overwhelming()
        world.check_for_informationalness()
        world.check_for_optional()
        #logger.debug(f"{world}: Unrated={world.unrated}, Complete={world.completed}, Info={world.informational}, Overwhelming={world.overwhelming}")
        continue

    reviews = [world for world in reviews if len(world.sections) > 0]

    headerData = HeaderData(inputData, verified_source_string)
    logger.info(f"{headerData.last_update = }")

    if runType == 'consoleTest':
        return 'Pass'
    else:
        return reviews, headerData
