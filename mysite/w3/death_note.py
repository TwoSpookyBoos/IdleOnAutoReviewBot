from math import floor
from consts.consts_autoreview import break_you_best
from consts.idleon.consts_idleon import current_world
from consts.consts_w3 import apoc_names_list, apoc_difficulty_name_list, dn_delays, dn_skull_value_to_name_dict, getDNKillRequirement
from consts.progression_tiers import deathNote_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.text_formatting import pl, notateNumber
from utils.logging import get_logger


logger = get_logger(__name__)

def getAllKillsDisplaySubgroupedByWorldAdviceGroup():
    advices = {}
    ags = []
    apoc_name = apoc_names_list[-1]  #This is the Unfiltered placeholder that stores just kill_count without any goal
    difficulty_name = apoc_difficulty_name_list[-2]
    #logger.debug(f"apocCharactersIndexList: {session_data.account.death_note.apoc_character_indexes}")
    for character_index in session_data.account.death_note.apoc_character_indexes:
        char = session_data.account.all_characters[character_index]
        #logger.debug(f"Generating AdviceGroup for: {char.character_name}")
        advices[char.character_name] = {
            "Scattered Extras": [],
            "World 1": [],
            "World 2": [],
            "World 3": [],
            "World 4": [],
            "World 5": [],
            "World 6": [],
            "World 7": [],
            #"World 8": [],
        }
        for unmet in char.apocalypses[apoc_name].unmet[difficulty_name]:
            subgroupName = f'World {unmet.world}' if unmet.world != 0 else 'Scattered Extras'
            advices[char.character_name][subgroupName].append(Advice(
                label=f"{unmet.monster_name} in {unmet.map_name}",
                picture_class=unmet.monster_image,
                goal=f"{unmet.kills_short:,}"
            ))
    for toon_name, toon_advice_list in advices.items():
        ags.append(AdviceGroup(
            tier='',
            pre_string=f'All kills for {toon_name} without a filter. Have fun',
            advices=toon_advice_list,
            informational=True,
            completed=True
        ))
    return ags

def getDeathNoteProgressionTiersAdviceGroup():
    deathnote_AdviceDict = {
        'W1': [],
        'W2': [],
        'W3': [],
        'W4': [],
        'W5': [],
        'W6': [],
        'W7': [],
        'ZOW': {},
        'CHOW': {},
        'MEOW': {},
        'WOW': {}
    }
    deathnote_failed_skull_type = {
        'W1': '',
        'W2': '',
        'W3': '',
        'W4': '',
        'W5': '',
        'W6': '',
        'W7': '',
    }
    optional_tiers = 3
    true_max = true_max_tiers['Death Note']
    max_tier = true_max - optional_tiers
    world_indexes = []
    tier_combo = {}
    for number in range(1, current_world + 1):
        world_indexes.append(number)
        tier_combo[number] = 0
    tier_combo['ZOW'] = 0
    tier_combo['CHOW'] = 0
    tier_combo['MEOW'] = 0
    tier_combo['WOW'] = 0
    apoc_to_next_tier = {
        'ZOW': 0,
        'CHOW': 0,
        'MEOW': 0,
        'WOW': 0
    }
    zows_for_next_tier = 0
    chows_for_next_tier = 0
    meows_for_next_tier = 0
    wows_for_next_tier = 0

    # Just shortening the paths
    apoc_characters_index_list = session_data.account.death_note.apoc_character_indexes
    apocalypse_character_Index = session_data.account.death_note.apocalypse_character_index
    full_death_note_dict = session_data.account.death_note.worlds

    highest_zow_count = 0
    highest_zow_count_index = None
    highest_chow_count = 0
    highest_chow_count_index = None
    for barb_index in apoc_characters_index_list:
        if highest_zow_count_index is None:
            highest_zow_count_index = barb_index
        if highest_chow_count_index is None:
            highest_chow_count_index = barb_index
        if session_data.account.all_characters[barb_index].apocalypses['ZOW'].total > highest_zow_count:
            highest_zow_count = session_data.account.all_characters[barb_index].apocalypses['ZOW'].total
            highest_zow_count_index = barb_index
        if session_data.account.all_characters[barb_index].apocalypses['CHOW'].total > highest_chow_count:
            highest_chow_count = session_data.account.all_characters[barb_index].apocalypses['CHOW'].total
            highest_chow_count_index = barb_index

    # Assess Tiers
    for tier in deathNote_progressionTiers:
        # tier[0] = int tier_number
        # tier[1] = int w1LowestSkull
        # tier[2] = int w2LowestSkull
        # tier[3] = int w3LowestSkull
        # tier[4] = int w4LowestSkull
        # tier[5] = int w5LowestSkull
        # tier[6] = int w6LowestSkull
        # tier[7] = int w7LowestSkull
        # tier[8] = int w8LowestSkull
        # tier[9] = int zowCount
        # tier[10] = int chowCount
        # tier[11] = int meowCount
        # tier[12] = int wowCount
        # tier[13] = str Notes

        # Basic Worlds
        for world_index in world_indexes:
            if tier_combo[world_index] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
                if full_death_note_dict[world_index].lowest_skull_value >= tier[world_index]:
                    tier_combo[world_index] = tier[0]
                else:
                    required_kills = getDNKillRequirement(skull_value=tier[world_index])
                    for skull_value in full_death_note_dict[world_index].maps_by_skull:
                        skull_name = dn_skull_value_to_name_dict[skull_value]
                        if skull_value < tier[world_index]:
                            # Looking for previously skipped enemy requirements where {skull_value} < {tier[world_index]}
                            # I promise this should be < not <=. You'll get negative amounts remaining if you use <=
                            for enemy in full_death_note_dict[world_index].maps_by_skull[skull_value]:
                                if (
                                    tier[world_index] < dn_delays.get(enemy.map_name, {}).get('DelayUntilSkull', 0)
                                    or tier[0] < dn_delays.get(enemy.map_name, {}).get('DelayUntilTier', 0)
                                ):
                                    # Skip certain maps until particular Skull values or Tier number
                                    continue
                                else:
                                    if deathnote_failed_skull_type[f'W{world_index}'] == '':
                                        # Store the type of skull failed to be used in the AG header
                                        deathnote_failed_skull_type[f'W{world_index}'] = dn_skull_value_to_name_dict[tier[world_index]]
                                    try:
                                        deathnote_AdviceDict[f'W{world_index}'].append(Advice(
                                            label=(
                                                f"{enemy.monster_name} in {enemy.map_name} ({notateNumber('Basic', required_kills - enemy.kill_count, 0)} remaining)"
                                            ),
                                            picture_class=enemy.monster_image,
                                            progression=min(99, floor(round(enemy.kill_count/required_kills * 100))),
                                            goal=100,
                                            unit='%',
                                            resource=skull_name
                                        ))
                                    except:
                                        logger.exception(f"Failed to find enemy name for W{world_index} {enemy.map_name}")
                    # If all failed requirements were delayed, be sure to increase the Tier as this counts as a Pass
                    if len(deathnote_AdviceDict[f'W{world_index}']) == 0:
                        tier_combo[world_index] = tier[0]

        # ZOW
        if tier_combo['ZOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highest_zow_count >= tier[9]:
                tier_combo['ZOW'] = tier[0]
            else:
                zows_for_next_tier = f"({highest_zow_count}/{tier[9]})"
                if highest_zow_count_index is not None:
                    apoc_to_next_tier['ZOW'] = tier[9] - highest_zow_count
                    for difficultyName in apoc_difficulty_name_list:
                        if len(session_data.account.all_characters[highest_zow_count_index].apocalypses['ZOW'].unmet[difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['ZOW']:
                                deathnote_AdviceDict['ZOW'][difficultyName] = []
                            deathnote_AdviceDict["ZOW"][difficultyName].extend(
                                unmet.get_advice()
                                for unmet in session_data.account.all_characters[highest_zow_count_index].apocalypses['ZOW'].unmet[difficultyName]
                            )
                else:
                    deathnote_AdviceDict['ZOW'] = [
                        Advice(
                            label='Create a Barbarian',
                            picture_class='barbarian-icon',
                            progression=0,
                            goal=1
                        )
                    ]

        # CHOW
        if tier_combo['CHOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if highest_chow_count >= tier[10]:
                tier_combo['CHOW'] = tier[0]
            else:
                chows_for_next_tier = f"({highest_chow_count}/{tier[10]})"
                if highest_chow_count_index is not None:
                    apoc_to_next_tier['CHOW'] = tier[10] - highest_chow_count
                    for difficultyName in apoc_difficulty_name_list:
                        if len(session_data.account.all_characters[highest_chow_count_index].apocalypses['CHOW'].unmet[difficultyName]) > 0:
                            if difficultyName not in deathnote_AdviceDict['CHOW']:
                                deathnote_AdviceDict['CHOW'][difficultyName] = []
                            deathnote_AdviceDict["CHOW"][difficultyName].extend(
                                unmet.get_advice()
                                for unmet in session_data.account.all_characters[highest_chow_count_index].apocalypses['CHOW'].unmet[difficultyName]
                            )
                else:
                    deathnote_AdviceDict['CHOW'] = [
                        Advice(
                            label='Create a Blood Berserker',
                            picture_class='blood-berserker-icon',
                            progression=0,
                            goal=1
                        )
                    ]

        # MEOW
        if tier_combo['MEOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if tier[11] == 0:
                tier_combo['MEOW'] = tier[0]
            else:
                if apocalypse_character_Index is not None:
                    if session_data.account.all_characters[apocalypse_character_Index].apocalypses['MEOW'].total >= tier[11]:
                        tier_combo['MEOW'] = tier[0]
                    else:
                        meows_for_next_tier = f"({session_data.account.all_characters[apocalypse_character_Index].apocalypses['MEOW'].total}/{tier[11]})"
                        apoc_to_next_tier['MEOW'] = tier[11] - session_data.account.all_characters[apocalypse_character_Index].apocalypses['MEOW'].total
                        for difficultyName in apoc_difficulty_name_list:
                            if len(session_data.account.all_characters[apocalypse_character_Index].apocalypses['MEOW'].unmet[difficultyName]) > 0:
                                if difficultyName not in deathnote_AdviceDict['MEOW']:
                                    deathnote_AdviceDict['MEOW'][difficultyName] = []
                                deathnote_AdviceDict["MEOW"][difficultyName].extend(
                                    unmet.get_advice()
                                    for unmet in session_data.account.all_characters[apocalypse_character_Index].apocalypses['MEOW'].unmet[difficultyName]
                                )
                else:
                    deathnote_AdviceDict['MEOW'] = [
                        Advice(
                            label='Create a Blood Berserker',
                            picture_class='blood-berserker-icon',
                            progression=0,
                            goal=1
                        )
                    ]

        # WOW
        if tier_combo['WOW'] >= (tier[0] - 1):  # Only evaluate if they already met the previous tier's requirement
            if tier[12] == 0:
                tier_combo['WOW'] = tier[0]
            else:
                if apocalypse_character_Index is not None:
                    if session_data.account.all_characters[apocalypse_character_Index].apocalypses['WOW'].total >= tier[12]:
                        tier_combo['WOW'] = tier[0]
                    else:
                        wows_for_next_tier = f"({session_data.account.all_characters[apocalypse_character_Index].apocalypses['WOW'].total}/{tier[12]})"
                        apoc_to_next_tier['WOW'] = tier[12] - session_data.account.all_characters[apocalypse_character_Index].apocalypses['WOW'].total
                        for difficulty_name in apoc_difficulty_name_list:
                            if len(session_data.account.all_characters[apocalypse_character_Index].apocalypses['WOW'].unmet[difficulty_name]) > 0:
                                if difficulty_name not in deathnote_AdviceDict['WOW']:
                                    deathnote_AdviceDict['WOW'][difficulty_name] = []
                                deathnote_AdviceDict['WOW'][difficulty_name].extend(
                                    unmet.get_advice()
                                    for unmet in session_data.account.all_characters[apocalypse_character_Index].apocalypses['WOW'].unmet[difficulty_name]
                                )

                else:
                    deathnote_AdviceDict['WOW'] = [
                        Advice(
                            label='Create a Death Bringer',
                            picture_class='death-bringer-icon',
                            progression=0,
                            goal=1
                        )
                    ]

    # Generate Advice Groups
    deathnote_AdviceGroups = {}
    # Basic Worlds
    for world_index in world_indexes:
        deathnote_AdviceGroups[f'W{world_index}'] = AdviceGroup(
            tier=tier_combo[world_index],
            pre_string=(
                f"Complete a minimum of {deathnote_failed_skull_type[f'W{world_index}']} "
                f"({notateNumber('Basic', getDNKillRequirement(skull_name=deathnote_failed_skull_type[f'W{world_index}']), 0)})"
                f" in W{world_index}"
            ),
            advices=deathnote_AdviceDict[f'W{world_index}'],
        )

    # ZOW
    if highest_zow_count_index is not None:
        deathnote_AdviceGroups['ZOW'] = AdviceGroup(
            tier=tier_combo['ZOW'],
            pre_string=f"{'You could complete' if tier_combo['ZOW'] >= max_tier else 'Complete'} "
                       f"{apoc_to_next_tier['ZOW']} more ZOW{pl(apoc_to_next_tier['ZOW'])} with "
                       f"{session_data.account.all_characters[highest_zow_count_index].character_name} {zows_for_next_tier}",
            advices=deathnote_AdviceDict['ZOW'],
            post_string="Aim for 12hrs or less (8k+ KPH) per enemy",
        )
    else:
        deathnote_AdviceGroups['ZOW'] = AdviceGroup(
            tier=tier_combo['ZOW'],
            pre_string='ZOW Progress unavailable until a Barbarian is found in your account',
            advices=deathnote_AdviceDict['ZOW'],
        )

    # CHOW
    if highest_chow_count_index is not None:
        deathnote_AdviceGroups['CHOW'] = AdviceGroup(
            tier=tier_combo['CHOW'],
            pre_string=f"{'You could complete' if tier_combo['CHOW'] >= max_tier else 'Complete'} "
                       f"{apoc_to_next_tier['CHOW']} more CHOW{pl(apoc_to_next_tier['CHOW'])} with "
                       f"{session_data.account.all_characters[highest_chow_count_index].character_name} {chows_for_next_tier}",
            advices=deathnote_AdviceDict['CHOW'],
            post_string="Aim for 12hrs or less (83k+ KPH) per enemy",
        )
    else:
        deathnote_AdviceGroups['CHOW'] = AdviceGroup(
            tier=tier_combo['CHOW'],
            pre_string='CHOW Progress unavailable until a Blood Berserker is found in your account',
            advices=deathnote_AdviceDict['CHOW'],
        )

    # MEOW
    if apocalypse_character_Index is not None:
        deathnote_AdviceGroups['MEOW'] = AdviceGroup(
            tier=tier_combo['MEOW'],
            pre_string=f"{'You could complete' if tier_combo['MEOW'] >= max_tier else 'Complete'} "
                       f"{apoc_to_next_tier['MEOW']} more Super CHOW{pl(apoc_to_next_tier['MEOW'])} with "
                       f"{session_data.account.all_characters[apocalypse_character_Index].character_name} {meows_for_next_tier}",
            advices=deathnote_AdviceDict['MEOW'],
            post_string=f"Aim for 24hrs or less (4m+ KPH) per enemy",
        )
    else:
        deathnote_AdviceGroups['MEOW'] = AdviceGroup(
            tier=tier_combo['MEOW'],
            pre_string='Super CHOW Progress unavailable until a Blood Berserker is found in your account',
            advices=deathnote_AdviceDict['MEOW'],
        )

    # WOW
    if apocalypse_character_Index is not None:
        deathnote_AdviceGroups['WOW'] = AdviceGroup(
            tier=tier_combo['WOW'],
            pre_string=f"{'You could complete' if tier_combo['WOW'] >= max_tier else 'Complete'} "
                       f"{apoc_to_next_tier['WOW']} more WOW{pl(apoc_to_next_tier['WOW'])} with "
                       f"{session_data.account.all_characters[apocalypse_character_Index].character_name} {wows_for_next_tier}",
            advices=deathnote_AdviceDict['WOW'],
            post_string='Aim for 10m+ KPH per enemy',
        )
    else:
        deathnote_AdviceGroups['WOW'] = AdviceGroup(
            tier=tier_combo['WOW'],
            pre_string='Super CHOW Progress unavailable until a Blood Berserker is found in your account',
            advices=deathnote_AdviceDict['WOW'],
        )

    if apocalypse_character_Index is not None:
        all_kills_ags = getAllKillsDisplaySubgroupedByWorldAdviceGroup()
        for ag in all_kills_ags:
            deathnote_AdviceGroups[ag.pre_string] = ag

    overall_SectionTier = min(true_max, min(tier_combo.values()))
    return deathnote_AdviceGroups, overall_SectionTier, max_tier, true_max


def getDeathNoteAdviceSection() -> AdviceSection:
    if session_data.account.construction_buildings['Death Note'].level < 1:
        deathnote_AdviceSection = AdviceSection(
            name='Death Note',
            tier='0/0',
            header=f'Come back after unlocking the Death Note within the Construction skill in World 3!',
            picture='Construction_Death_Note.png',
            unreached=True
        )
        return deathnote_AdviceSection

    #Generate AdviceGroups
    deathnote_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getDeathNoteProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    deathnote_AdviceSection = AdviceSection(
        name='Death Note',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Death Note tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Construction_Death_Note.png',
        groups=deathnote_AdviceGroupDict.values(),
        note=(
            "Important! Since you already have 2+ Blood Berserkers, you must complete Super CHOWs and WOWs"
            " with the last one in your character roster, regardless of the platform you play on."
        ) if len(session_data.account.death_note.bb_character_indexes) > 1 else ''
    )

    return deathnote_AdviceSection
