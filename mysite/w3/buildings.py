import copy

from consts.consts_autoreview import EmojiType
from consts.progression_tiers import buildingsPostBuffs_progressionTiers, buildingsPreBuffs_progressionTiers, true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger


logger = get_logger(__name__)

def getInfluencers():
    honker_vial_level = session_data.account.alchemy_vials['Goosey Glug (Honker)']['Level']
    poisonic_level = session_data.account.construction_buildings['Poisonic Elder']['Level']
    cons_mastery = session_data.account.rift['ConstructionMastery']
    carbon_unlocked = session_data.account.atom_collider['Atoms']['Carbon - Wizard Maximizer']['Level'] >= 1
    results = [(cons_mastery or carbon_unlocked), honker_vial_level, poisonic_level]
    #logger.debug(f"Influencer results: EitherBuff: {results[0]}, Honker Vial Level: {results[1]}, Poisonic Tower Level: {results[2]}")
    return results

def generateShrineLevelingAlerts():
    has_shrine_world_order_bill = bool(session_data.account.legend_talents['Talents']['Shrine World Order Bill']['Level'])
    if has_shrine_world_order_bill: 
        return

    shrine_data = session_data.account.shrines
    unlocked_shrines = [value['Image'] for key, value in session_data.account.construction_buildings.items() if value['Type'] == 'Shrine' and value['Level'] > 0]
    unlocked_shrines_data = {key: {'map_index': shrine['MapIndex'], 'leveled_by': [], 'image': shrine['Image']} for key, shrine in shrine_data.items() if shrine['Image'] in unlocked_shrines}

    shrine_world_tour_active = session_data.account.labBonuses['Shrine World Tour']['Enabled']
    reached_world_6 = session_data.account.highest_world_reached >= 6
    has_collective_bargaining_agreement = session_data.account.sneaking.emporium['Shrine Collective Bargaining Agreement'].obtained
    xp_reset_warning = '' if reached_world_6 and has_collective_bargaining_agreement else f'<br>{EmojiType.WARNING.value} Moving this shrine will lose xp progress for the current level!'

    for char in session_data.account.safe_characters:
        char_current_map = char.current_map_index
        char_current_world = (char_current_map // 50) + 1
        for shrine_name, shrine_data in unlocked_shrines_data.items():
            shrine_current_map = shrine_data['map_index']
            shrine_current_world = (shrine_current_map // 50) + 1
            char_is_leveling = char_current_map == shrine_current_map or (shrine_world_tour_active and char_current_world == shrine_current_world)
            if char_is_leveling:
                unlocked_shrines_data[shrine_name]['leveled_by'].append(char)
    for shrine_name, shrine_data in unlocked_shrines_data.items():
        if len(shrine_data['leveled_by']) > 0:
            continue
        session_data.account.alerts_Advices['General'].append(Advice(
            label=f'Your {shrine_name} is not being leveled by anyone{xp_reset_warning}',
            picture_class=shrine_data['image']
        ))

def getProgressionTiersAdviceGroup():
    building_Advices = {}

    optional_tiers = 0
    true_max = true_max_tiers['Buildings']
    max_tier = true_max - optional_tiers

    progression_tiers_pre_buffs = copy.deepcopy(buildingsPreBuffs_progressionTiers)
    progression_tiers_post_buffs = copy.deepcopy(buildingsPostBuffs_progressionTiers)
    player_buildings = session_data.account.construction_buildings
    influencers = getInfluencers()
    hasBuffs = influencers[0]
    if hasBuffs:
        max_level_dict = {
            "3D Printer": 10, "Talent Book Library": 101, "Death Note": 51, "Salt Lick": 10, "Chest Space": 25,
            "Cost Cruncher": 60, "Trapper Drone": 20, "Automation Arm": 5, "Atom Collider": 200,
            "Pulse Mage": 70, "Fireball Lobber": 70, "Boulder Roller": 70, "Frozone Malone": 70, "Stormcaller": 90,
            "Party Starter": 70, "Kraken Cosplayer": 90, "Poisonic Elder": 90, "Voidinator": 40,
            "Woodular Shrine": 200, "Isaccian Shrine": 200, "Crystal Shrine": 200, "Pantheon Shrine": 200, "Clover Shrine": 200,
            "Summereading Shrine": 200, "Crescent Shrine": 200, "Undead Shrine": 200, "Primordial Shrine": 200
        }
    else:
        max_level_dict = {
            "3D Printer": 10, "Talent Book Library": 101, "Death Note": 51, "Salt Lick": 10, "Chest Space": 25,
            "Cost Cruncher": 60, "Trapper Drone": 15, "Automation Arm": 5, "Atom Collider": 200,
            "Pulse Mage": 50, "Fireball Lobber": 50, "Boulder Roller": 50, "Frozone Malone": 50, "Stormcaller": 50,
            "Party Starter": 50, "Kraken Cosplayer": 50, "Poisonic Elder": 50, "Voidinator": 40,
            "Woodular Shrine": 100, "Isaccian Shrine": 100, "Crystal Shrine": 100, "Pantheon Shrine": 100, "Clover Shrine": 100,
            "Summereading Shrine": 100, "Crescent Shrine": 100, "Undead Shrine": 100, "Primordial Shrine": 100
        }

    # Make adjustments to tiers based on other influencers
    # 1) If any building is level 0, it gets promoted to SS tier
    for building_name, building_level in max_level_dict.items():
        if player_buildings[building_name]['Level'] == 0:
            max_level_dict[building_name] = 1  # With a max recommended level of 1
            for tier in progression_tiers_post_buffs:
                if building_name in tier[2] and tier[1] != "SS":
                    tier[2].remove(building_name)  # Remove that building from any other non-SS tier.
                    progression_tiers_post_buffs[0][2].append(building_name)
                    # logger.debug(f"Level 0 building detected. Removing {building_name} from POSTBuff {tier[1]} and adding to SS with max level 1 instead.")
            for tier in progression_tiers_pre_buffs:
                if building_name in tier[2] and tier[1] != "SS":
                    tier[2].remove(building_name)  # Remove that building from any other non-SS tier.
                    progression_tiers_pre_buffs[0][2].append(building_name)
                    # logger.debug(f"Level 0 building detected. Removing {building_name} from PREBuff {tier[1]} and adding to SS with max level 1 instead.")

    # 2) Honker vial is 12+ OR Trapper Drone is 20+, drop Trapper Drone priority
    if influencers[1] >= 12 or player_buildings['Trapper Drone']['Level'] >= 20:
        try:
            progression_tiers_post_buffs[2][2].remove('Trapper Drone')  # Remove Trapper Drone from S Tier
            progression_tiers_post_buffs[5][2].insert(1, 'Trapper Drone')  # Add Trapper Drone to C tier
            if hasBuffs:
                max_level_dict['Trapper Drone'] = 50
            # logger.debug("Successfully moved Trapper Drone from PostBuff S to D tier and changed level from 20 to 50")
        except Exception as reason:
            logger.exception(f"Could not remove Trapper Drone from PostBuff S tier: {reason}")

    # 3) #Poisonic level 20+, drop Boulder Roller priority
    if influencers[2] >= 20:
        try:
            # PreBuffs
            progression_tiers_pre_buffs[2][2].remove("Boulder Roller")  # Remove Boulder Roller from S tier
            progression_tiers_pre_buffs[6][2].append("Boulder Roller")  # Add Boulder Roller to D tier
            # logger.debug("Successfully moved Boulder Roller from PreBuff S to D tier because Poisonic 20+")
            # PostBuffs
            progression_tiers_post_buffs[2][2].remove("Boulder Roller")  # Remove Boulder Roller from S tier
            progression_tiers_post_buffs[3][2].append("Boulder Roller")  # Add Boulder Roller to A tier
            # logger.debug("Successfully moved Boulder Roller from PostBuff S to A tier because Poisonic 20+")
        except Exception as reason:
            logger.exception(f"Could not move Boulder Roller from S tier in one or both tierlists: {reason}")

    # 4) Talent Library Book 101+, drop priority
    if player_buildings['Talent Book Library']['Level'] >= 101:
        try:
            progression_tiers_post_buffs[2][2].remove("Talent Book Library")  # Remove from S tier
            progression_tiers_post_buffs[5][2].insert(1, "Talent Book Library")  # Add to C tier
            if hasBuffs:
                max_level_dict["Talent Book Library"] = 201
            # logger.debug("Successfully moved 101+ Talent Library Book from PostBuff A to C tier.")
        except Exception as reason:
            logger.exception(f"Could not move 101+ Talent Library Book from PostBuff A tier to C tier: {reason}")

    # 5) #Basic Towers to 70, drop priority
    for tower_name in ['Frozone Malone', 'Party Starter', 'Pulse Mage', 'Fireball Lobber', 'Boulder Roller']:
        if player_buildings[tower_name]['Level'] >= 70:
            try:
                progression_tiers_post_buffs[3][2].remove(tower_name)  # Remove from A tier
                progression_tiers_post_buffs[5][2].insert(3, tower_name)  # Add to C tier
                if hasBuffs:
                    max_level_dict[tower_name] = 240
                # logger.info(f"Successfully moved 70+ basic tower from PostBuff A to C tier: {getBuildingNameFromIndex(towerIndex)})
            except Exception as reason:
                logger.exception(f"Could not move 70+ basic tower {tower_name} from PostBuff A tier to C tier: {reason}")

    # 6) Fancy Towers to 90, drop priority
    for tower_name in ['Kraken Cosplayer', 'Poisonic Elder', 'Stormcaller']:
        if player_buildings[tower_name]['Level'] >= 90:
            for tierIndex in range(0, len(progression_tiers_post_buffs)):
                if tower_name in progression_tiers_post_buffs[tierIndex][2]:
                    progression_tiers_post_buffs[tierIndex][2].remove(tower_name)  # Remove from any existing tier (S for Kraken and Poison, A for Stormcaller)
            progression_tiers_post_buffs[3][2].append(tower_name)  # Add to A tier
            if hasBuffs:
                max_level_dict[tower_name] = 240

    # 7) Voidinator to 40, drop priority
    if player_buildings['Voidinator']['Level'] >= 40:  # Voidinator scaling is very bad
        try:
            progression_tiers_pre_buffs[4][2].remove("Voidinator")  # Remove from PreBuff B tier
            progression_tiers_pre_buffs[5][2].insert(0, "Voidinator")  # Add to C tier
            progression_tiers_post_buffs[3][2].remove("Voidinator")  # Remove from PostBuff A tier
            progression_tiers_post_buffs[5][2].insert(0, "Voidinator")  # Add to C tier
            if hasBuffs:
                max_level_dict['Voidinator'] = 240
            # logger.debug("Successfully moved 30+ Voidinator from A/B to C tier in both tierlists")
        except Exception as reason:
            logger.exception(f"Could not move 30+ Voidinator from A/B to C tier in both tierlists: {reason}")

    # Decide which tierset to use
    if influencers[0] == True:  # Has either Construction Mastery or the Wizard atom
        progression_tiers_to_use = progression_tiers_post_buffs
        # logger.debug("Either Construction Mastery or Wizard Atom found. Setting ProgressionTiers to PostBuff.")
    else:
        progression_tiers_to_use = progression_tiers_pre_buffs
        # logger.debug("Setting ProgressionTiers to PreBuff.")

    # tier[0] = int tier
    # tier[1] = str Tier name
    # tier[2] = list of ints of tower indexes
    # tier[3] = str tower notes
    # tier[4] = str tier notes
    tier_names_list = []
    for counter in range(0, len(progression_tiers_to_use)):
        building_Advices[counter] = []
        tier_names_list.append(progression_tiers_to_use[counter][1])
        for building_name in progression_tiers_to_use[counter][2]:
            try:
                if max_level_dict.get(building_name, 999) > player_buildings.get(building_name, {}).get('Level', 0):
                    if progression_tiers_to_use[counter][1] == 'Unlock':
                        building_Advices[counter].append(Advice(
                            label=building_name,
                            picture_class=player_buildings.get(building_name, {}).get('Image', ''),
                            progression=0,
                            goal=1
                        ))
                    else:
                        building_Advices[counter].append(Advice(
                            label=building_name,
                            picture_class=player_buildings.get(building_name, {}).get('Image', ''),
                            progression=player_buildings.get(building_name, {}).get('Level', 0),
                            goal=max_level_dict.get(building_name, 999)
                        ))
            except:
                logger.exception(f"ProgressionTier evaluation error. Counter = {counter}, building_name = {building_name}")

    # Generate AdviceGroups
    building_AdviceGroups = {}
    tier_UnlockAllBuildings = int(all([building['Level'] > 0 for building in player_buildings.values()]))
    for tier_key in building_Advices.keys():
        if f"{tier_names_list[tier_key]}" == 'Unlock':
            building_AdviceGroups[tier_key] = AdviceGroup(
                tier=tier_UnlockAllBuildings,
                pre_string='Unlock All Buildings',
                advices=building_Advices[tier_key],
                informational=False
            )
        else:
            building_AdviceGroups[tier_key] = AdviceGroup(
                tier='',
                pre_string=f'{tier_names_list[tier_key]} Tier',
                advices=building_Advices[tier_key],
                informational=True
            )
    overall_SectionTier = min(true_max, tier_UnlockAllBuildings)
    return building_AdviceGroups, overall_SectionTier, max_tier, true_max

def getConsBuildingsAdviceSection() -> AdviceSection:
    highestConstructionLevel = max(session_data.account.all_skills["Construction"])
    if highestConstructionLevel < 1:
        building_AdviceSection = AdviceSection(
            name='Buildings',
            tier='0/0',
            header='Come back after unlocking the Construction skill in World 3!',
            picture='Construction_Table.gif',
            unrated=True,
            unreached=True
        )
        return building_AdviceSection

    # Generate Alerts
    generateShrineLevelingAlerts()

    #Generate AdviceGroups
    building_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    building_AdviceSection = AdviceSection(
        name='Buildings',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Priority Tiers for Trimmed Building Slots',
        picture='Construction_Table.gif',
        unrated=True,
        informational=True,
        groups=building_AdviceGroupDict.values(),
        note=(
            "Buildings shift around in Priority Tiers after reaching particular levels or notable account progression points."
            " The goal levels displayed are only for that particular tier and may be beyond your personal max level."
        )
    )
    return building_AdviceSection
