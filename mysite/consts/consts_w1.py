from math import ceil, e
from consts.consts_autoreview import ceilUpToBase
from consts.idleon.consts_idleon import NinjaInfo
from utils.safer_data_handling import safer_math_log, safer_math_pow
from utils.text_formatting import numberToLetter
from utils.number_formatting import parse_number
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

# Passive Starsigns do not consume an Infinite Star Sign point and are the 3 big signs you can't align to.
# Last updated in v2.43 Nov 10
passive_starsigns = ['Chronus_Cosmos', 'Hydron_Cosmos', 'Seraph_Cosmos']

# `StarSigns` in source. Last updated in v2.43 Nov 10
StarSigns = [["The_Buff_Guy", "+1%_Total_Damage", "+3_STR", "_"], ["Flexo_Bendo", "+2%_Movement_Speed", "+3_AGI", "_"], ["The_Book_Worm", "+1%_Class_EXP_Gain", "+3_WIS", "_"], ["The_Fuzzy_Dice", "+3_Talent_Points", "+3_LUK", "_"], ["Dwarfo_Beardus", "+5%_Mining_Efficency", "+20%_Multi-Ore_Chance", "_"], ["Hipster_Logger", "+5%_Chop_Efficiency", "+20%_Multi-Log_Chance", "_"], ["Pie_Seas", "+5%_Fishin_Efficency", "+20%_Multi-Fish_Odds", "_"], ["Shoe_Fly", "+5%_Catch_Efficiency", "+20%_Multi-Bug_Chance", "_"], ["Blue_Hedgehog", "+4%_Movement_Speed", "+0.0001%_Ring_Drop", "_"], ["Gum_Drop", "+15%_to_get_a_Time", "Candy_when_claiming", "8+_Hour_AFK_gains"], ["Activelius", "+15%_Class_EXP_when", "fighting_actively", "_"], ["Pack_Mule", "+10%_Carry_Cap", "_", "_"], ["Ned_Kelly", "+6%_Defence", "+2_Weapon_Power", "_"], ["Robinhood", "+4%_Accuracy", "+2%_Movement_Speed", "+1_Cant_Trade_GME"], ["Pirate_Booty", "+5%_Drop_Rate", "_", "_"], ["Muscle_Man", "+8_STR", "_", "_"], ["Fast_Frog", "+8_AGI", "_", "_"], ["Smart_Stooge", "+8_WIS", "_", "_"], ["Lucky_Larry", "+8_LUK", "_", "_"], ["Silly_Snoozer", "+2%_Fight_AFK_Gain", "_", "_"], ["The_Big_Comatose", "+2%_Skill_AFK_Gain", "_", "_"], ["Miniature_Game", "+30%_minigame_reward", "_", "_"], ["Mount_Eaterest", "+10%_chance_to_not", "consume_food", "+15%_All_Food_Effect"], ["Bob_Build_Guy", "+10%_Speed_in_Town", "Skills", "_"], ["The_Big_Brain", "+3%_Class_EXP_gain", "_", "_"], ["The_OG_Skiller", "+5%_Carry_Cap", "+1%_Skill_AFK_gain", "+2%_All_Skill_Prowess"], ["Grim_Reaper", "+2%_Mob_Respawn_rate", "_", "_"], ["The_Fallen_Titan", "+3%_Boss_Damage", "+4%_Crit_Chance", "_"], ["The_Forsaken", "-80%_Total_HP", "-50%_Defence", "+6%_Fight_AFK_Gain"], ["Mr_No_Sleep", "-6%_AFK_Gain", "+30%_Carry_Cap", "_"], ["Sir_Savvy", "+3%_Skill_EXP_gain", "_", "_"], ["All_Rounder", "+4_All_Stats", "_", "_"], ["Fatty_Doodoo", "-3%_Movement_Speed", "+5%_Defence", "+2%_Total_Damage"], ["Chronus_Cosmos", "All_characters_can", "now_align_with_2", "Star_Signs_at_once"], ["All_Rounderi", "+1%_All_Stat", "i.e._STR/AGI/WIS/LUK", "_"], ["Centaurii", "+10%_Accuracy", "_", "_"], ["Murmollio", "+10%_Defence", "_", "_"], ["Strandissi", "+3%_STR", "_", "_"], ["Agitagi", "+3%_AGI", "_", "_"], ["Wispommo", "+3%_WIS", "_", "_"], ["Lukiris", "+3%_LUK", "_", "_"], ["Pokaminni", "+15%_Card_Drop", "(Outside_of_Dungeons)", "_"], ["Gor_Bowzor", "+12%_Boss_Damage", "_", "_"], ["Hydron_Cosmos", "All_characters_can", "now_align_with_3", "Star_Signs_at_once"], ["Trapezoidburg", "+20%_Critters/Trap", "+10%_Trap_Efficiency", "_"], ["Sawsaw_Salala", "+25%_Construct_Exp", "_", "_"], ["Preys_Bea", "+15%_Worship_Efficiency", "+15%_Worship_EXP", "_"], ["Cullingo", "+15%_Total_Multikill", "_", "_"], ["Gum_Drop_Major", "+40%_to_get_a_Time", "Candy_when_claiming", "40+_Hour_AFK_gains"], ["Grim_Reaper_Major", "+4%_Mob_Respawn_rate", "(If_Lv&60)", "_"], ["Sir_Savvy_Major", "+6%_Skill_EXP_gain", "(If_Lv&70)", "_"], ["The_Bulwark", "+20%_Total_Damage", "-12%_Movement_Speed", "_"], ["Big_Brain_Major", "+6%_Class_EXP_gain", "(If_Lv&80)", "_"], ["The_Fiesty", "+6%_Total_Damage", "_", "_"], ["The_Overachiever", "+15%_Total_Damage", "-7%_Fight_AFK_Gain", "_"], ["Comatose_Major", "+4%_Skill_AFK_Gain", "(If_Lv&90)", "_"], ["S._Snoozer_Major", "+4%_Fight_AFK_Gain", "(If_Lv&100)", "_"], ["Breedabilli", "+35%_Breedable_Spd", "+15%_Shiny_Pet_LV_spd", "_"], ["Gordonius_Major", "+15%_Cooking_SPD", "(Multiplicative!)", "_"], ["Power_Bowower", "+30%_Pet_DMG_for", "Breeding_Skill", "_"], ["Scienscion", "+20%_Lab_EXP_Gain", "_", "_"], ["Artifosho", "+15%_Artifact_Find", "Chance", "(Multiplicative)"], ["Divividov", "+30%_Divinity_EXP", "_", "_"], ["C._Shanti_Minor", "+20%_Sailing_SPD", "_", "_"], ["Muscle_Magnus", "+50_STR", "_", "_"], ["Cropiovo_Minor", "+3%_Crop_Evo", "chance_per_Farming_LV", "_"], ["Fabarmi", "+20%_Farming_EXP", "_", "_"], ["O.G._Signalais", "+15%_OG_Chance", "_", "_"], ["Lightspeed_Frog", "+50_AGI", "_", "_"], ["Beanbie_Major", "+20%_Golden_Food", "bonuses", "_"], ["Damarian_Major", "+25%_Total_Damage", "_", "_"], ["Lotto_Larrinald", "+50_LUK", "_", "_"], ["Intellostooge", "+50_WIS", "_", "_"], ["S._Tealio", "+12%_Ninja_Twin", "Stealth", "_"], ["Sneekee_E._X.", "+15%_Sneaking_EXP", "_", "_"], ["Jadaciussi", "+10%_Jade_Gain", "(Multiplicative!)", "_"], ["Druipi_Major", "+12%_Drop_Rarity", "_", "_"], ["Sumo_Magno", "+20%_Summoning_EXP", "_", "_"], ["Killian_Maximus", "+3%_Multikill_Per_Tier", "_", "_"], ["Seraph_Cosmos", "All_characters_now_get", "1.10x_Star_Sign_bonuses", "per_20_Summoning_LV"], ["Glimmer_of_Beyond", "This_star_sign_is", "unreachable_for_now...", "_"], ["Fillerz48", "_", "_", "_"], ["Fillerz49", "_", "_", "_"], ["Fillerz50", "_", "_", "_"], ["Fillerz51", "_", "_", "_"], ["Fillerz52", "_", "_", "_"], ["Fillerz53", "_", "_", "_"], ["Fillerz54", "_", "_", "_"], ["Fillerz55", "_", "_", "_"], ["Fillerz56", "_", "_", "_"], ["Fillerz57", "_", "_", "_"], ["Fillerz58", "_", "_", "_"], ["Fillerz59", "_", "_", "_"], ["Fillerz32", "_", "_", "_"]]
starsigns_dict = {
    index: {
        'Name': name.replace('_', ' '),
        'Passive': name in passive_starsigns,
        'Bonus1': bonus1.replace('_', ' '),
        'Bonus2': bonus2.replace('_', ' '),
        'Bonus3': bonus3.replace('_', ' '),
    }
    for index, (name, bonus1, bonus2, bonus3) in enumerate(StarSigns) if not name.startswith("Fillerz")
}

# The formula including this is buried. Search for `Seraph_Cosmos` and pray
seraph_max = 5  #Last updated in v2.46 Dec 8

def get_seraph_cosmos_max_summ_level_goal(astrology_cultism_level: int) -> int:
    # Returns the highest summoning level needed to reach seraph_max based on astrology_cultism levels
    try:
        result = 20 * ceil(safer_math_log(seraph_max, e) / safer_math_log(1.1 + min(0.01 * astrology_cultism_level, 0.10), e))
        return result
    except:
        logger.exception(f"Something went wrong. Returning max as if they have no astrology cultism.")
        result = 20 * ceil(safer_math_log(seraph_max, e) / safer_math_log(1.1, e))
        return result

def get_seraph_cosmos_summ_level_goal(astrology_cultism_level: int, character_summoning_level: int | None = None, all_summoning_levels: list | None = None) -> int:
    max_summ_level_goal = get_seraph_cosmos_max_summ_level_goal(astrology_cultism_level)
    if character_summoning_level is not None:
        result = min(max_summ_level_goal, ceilUpToBase(character_summoning_level, 20))
        return result
    elif all_summoning_levels is not None:
        result = min(max_summ_level_goal, ceilUpToBase(max(all_summoning_levels, default=0), 20))
        return result
    else:
        logger.error(
            f"get_seraph_cosmos_summ_level_goal() was called with no summoning level type goal. Please submit "
            f"character_summoning_level to calculate an individual character's goal, "
            f"or all_summoning_levels to find the account-wide goal based on the character with the highest level summoning."
        )
        result = max_summ_level_goal
        return result

def get_seraph_cosmos_multi(astrology_cultism_level: int, character_summoning_level: int | None = None, all_summoning_levels: list | None = None) -> float:
    # This formula is kind of buried. Search for `Seraph_Cosmos` and pray
    # if (t = a.engine.getGameAttribute("StarSignsUnlocked"), Object.prototype.hasOwnProperty.call(t.h, "Seraph_Cosmos"))
    # Math.min(5, Math.pow(1.1 + Math.min(c.asNumber(a.engine.getGameAttribute("Arcane")[40]), 10) / 100, Math.ceil((c.asNumber(a.engine.getGameAttribute("Lv0")[18]) + 1) / 20)))
    if character_summoning_level is not None:
        result = min(seraph_max, safer_math_pow(
            1.1 + min(0.01 * astrology_cultism_level, 0.10),
            ceil(character_summoning_level + 1) / 20)
        )
        return result
    elif all_summoning_levels is not None:
        result = min(seraph_max, safer_math_pow(
            1.1 + min(0.01 * astrology_cultism_level, 0.10),
            ceil(max(all_summoning_levels, default=0) + 1) / 20)
        )
        return result
    else:
        logger.error(
            f"get_seraph_cosmos_summ_level_goal() was called with no summoning level type goal. Please submit "
            f"character_summoning_level to calculate an individual character's goal, "
            f"or all_summoning_levels to find the account-wide goal based on the character with the highest level summoning."
        )
        result = 1
        return result

def get_seraph_stacks(summoning_level) -> int:
    result = ceil((summoning_level + 1) / 20)
    return result


forge_upgrades_dict = {
    0: {
        "UpgradeName": "New Forge Slot",
        "Purchased": 0,
        "MaxPurchases": 16
    },
    1: {
        "UpgradeName": "Ore Capacity Boost",
        "Purchased": 0,
        "MaxPurchases": 50
    },
    2: {
        "UpgradeName": "Forge Speed",
        "Purchased": 0,
        "MaxPurchases": 90
    },
    3: {
        "UpgradeName": "Forge EXP Gain (Does Nothing!)",
        "Purchased": 0,
        "MaxPurchases": 85
    },
    4: {
        "UpgradeName": "Bar Bonanza",
        "Purchased": 0,
        "MaxPurchases": 75
    },
    5: {
        "UpgradeName": "Puff Puff Go",
        "Purchased": 0,
        "MaxPurchases": 60
    }
}

# `StatueInfo` in source. Last updated in v2.43 Nov 10
StatueInfo = [["POWER", "@BASE_DAMAGE", "30", "3"], ["SPEED", "%@MOVE_SPEED", "65", "0.1"], ["MINING", "@MINING_POWER", "280", "0.3"], ["FEASTY", "%@FOOD_EFFECT", "320", "1"], ["HEALTH", "@BASE_HEALTH", "0", "3"], ["KACHOW", "%@CRIT_DAMAGE", "-15", "0.4"], ["LUMBERBOB", "@CHOPPIN_POWER", "90", "0.3"], ["THICC_SKIN", "@BASE_DEFENCE", "210", "1"], ["OCEANMAN", "@FISHING_POWER", "115", "0.3"], ["OL_RELIABLE", "@CATCHIN_POWER", "45", "0.3"], ["EXP", "%@CLASS_EXP", "0", "0.1"], ["ANVIL", "%@PRODUCT_SPD", "165", "0.5"], ["CAULDRON", "%@ALCHEMY_EXP", "280", "0.5"], ["BEHOLDER", "%@CRIT_CHANCE", "300", "0.2"], ["BULLSEYE", "%@ACCURACY", "110", "0.8"], ["BOX", "@TRAPPIN_POWER", "180", "0.3"], ["TWOSOUL", "@WORSHIP_POWER", "260", "0.3"], ["EHEXPEE", "%@SKILL_EXP", "69", "0.1"], ["SEESAW", "%@CONS_EXP", "13", "0.5"], ["PECUNIA", "%@COINS", "50", "1"], ["MUTTON", "%@COOKING_EXP", "0", "0.3"], ["EGG", "%@BREEDING_EXP", "25", "0.4"], ["BATTLEAXE", "%@DAMAGE", "300", "0.2"], ["SPIRAL", "%@DIVINITY_EXP", "70", "1"], ["BOAT", "%@SAILING_SPD", "210", "0.5"], ["COMPOST", "%@FARMING_EXP", "75", "0.4"], ["STEALTH", "%@STEALTH", "185", "0.3"], ["ESSENCE", "%@WHITE_ESS", "160", "0.6"], ["VILLAGER", "%@VILLAGER_EXP", "120", "0.3"], ["DRAGON", "%@STATUES_BONUS", "270", "0.2"], ["SPELUNKY", "%@SPELUNK_EXP", "43", "0.2"], ["CORAL", "%@DAILY_CORAL", "181", "0.02"]]
statue_farming = {
    0:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    1:  {"Farmer": "W1-W3 Crystals with DK", "Resource": "w1-w3-crystals"},
    2:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    3:  {"Farmer": "W1-W3 Crystals with DK", "Resource": "w1-w3-crystals"},
    4:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    5:  {"Farmer": "Monolith Quest on All characters", "Resource": "monolith"},
    6:  {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    7:  {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    8:  {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},  #v2.45 moved statues from Skilling nodes to Crystals
    9:  {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    10: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    11: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    12: {"Farmer": "Crystals with DK at Sandy Pot or Tyson", "Resource": "crystal-crabal"},
    13: {"Farmer": "Crystals with DK at Beans", "Resource": "bored-bean"},
    14: {"Farmer": "Active ES at Wood Mushroom or Candy at Nutto", "Resource": "wood-mushroom"},
    15: {"Farmer": "Candy or Active ES at Penguins", "Resource": "penguin"},
    16: {"Farmer": "Candy or Active ES at Quenchies", "Resource": "quenchie"},
    17: {"Farmer": "Crystals with DK at Bloodbones", "Resource": "bloodbone"},
    18: {"Farmer": "Candy or Active ES at Cryosnakes", "Resource": "cryosnake"},
    19: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    20: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    21: {"Farmer": "Crystals with DK at Clammies", "Resource": "clammie"},
    22: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    23: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    24: {"Farmer": "Crystals with DK at Tremor Wurms", "Resource": "tremor-wurm"},
    25: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    26: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    27: {"Farmer": "Crystals with DK at Minichiefs", "Resource": "minichief-spirit"},
    28: {"Farmer": "AFK {{Cavern 9|#villagers}}", "Resource": "gloomie-mushroom"},
    29: {"Farmer": "AFK {{Cavern 15|#villagers}}", "Resource": "ancient-golem"},
    30: {"Farmer": "W7 Crystals with DK", "Resource": ""},
    31: {"Farmer": "W7 Crystals with DK", "Resource": ""}
}
statues_dict = {
    index: {
        'Name': f"{name.replace('_', ' ').title()} Statue",
        'ItemName': f"EquipmentStatues{index+1}",
        'Effect': effect.replace('@', ' ').replace('_', ' ').strip().title(),
        'BaseValue': parse_number(basevalue),
        'Farmer': statue_farming.get(index, {}).get('Farmer', ''),
        'Resource': statue_farming.get(index, {}).get('Resource', ''),
    }
    for index, (name, effect, pos2, basevalue) in enumerate(StatueInfo)
}
statue_type_dict = {0: 'Normal', 1: 'Gold', 2: 'Onyx', 3: 'Zenith'}
statue_type_count = sum([isinstance(k, int) for k in statue_type_dict.keys()])
statue_count = len(statues_dict.keys())
statue_onyx_stack_size = 20000
statue_zenith_stack_size = 1000000

def get_statue_type_index_from_name(statue_type_name: str) -> int:
    statue_type_index = next((k for k, v in statue_type_dict.items() if v == statue_type_name), 0)
    return statue_type_index


# Found near end of `NinjaInfo` in source. Last updated in v2.43 Nov10
NinjaInfo_event_shop = NinjaInfo[39]
event_points_shop_dict = {}
event_points_shop_duplicate_name_overrides = {
    'Extra Page': 'Extra Page #2',
    'Plain Showcase': 'The Scroll'
}
for index in range(0, len(NinjaInfo_event_shop), 2):
    name = NinjaInfo_event_shop[index].split('@')[0].replace('_', ' ').strip()
    if name in event_points_shop_dict:
        override_name = event_points_shop_duplicate_name_overrides.get(name, 'UNKNOWN')
        if override_name == 'UNKNOWN':
            logger.warning(f"Found duplicate Event Shop item name '{name}' without override at index {index}")
            name = f"{name} #{index}"
        else:
            name = override_name
    event_points_shop_dict[name] = {
        'Cost': NinjaInfo_event_shop[index+1],
        'Code': numberToLetter(int(index/2)),
        'Image': f'event-shop-{int(index/2)}',
        'Description': NinjaInfo_event_shop[index].split('@')[1].replace('_', ' ').strip()
    }

# unnamed arrays in source. Last updated in v2.45 Nov 16
# search for any of these string, they're unique enough to find quickly
basketball_upgrade_descriptions = ["Select_an_upgrade,_these_bonuses_are_permanent_and_affect_the_rest_of_the_game!", "+{%_Damage_to_Monsters", "+{%_Coins_dropped_by_monsters", "+{%_Class_EXP_when_killing_monsters", "+{%_Efficiency_for_all_Skills,_like_Mining_and_Choppin!"]
darts_upgrade_descriptions = ["Select_an_upgrade,_these_bonuses_are_permanent_and_affect_the_rest_of_the_game!", "+{%_Extra_Damage_against_Monsters!", "+{_Talent_PTS_for_the_first_page!", "All_Vault_upgrades_are_}x_Cheaper!", "+{%_Movement_Speed,_so_you_can_run_faster!"]