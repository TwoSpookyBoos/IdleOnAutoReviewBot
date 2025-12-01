from consts.consts_autoreview import ValueToMulti
from utils.number_formatting import parse_number
from utils.text_formatting import getItemDisplayName
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

max_printer_sample_rate = 90
arbitrary_shrine_goal = 32  # Last updated in v2.46 Nov 19
arbitrary_shrine_note = f"Shrines have no Max level. Goal of {arbitrary_shrine_goal} is arbitrary"
max_implemented_dreams = 36  # Last verified as of v2.30
max_possible_dreams = 35  # Last verified as of v2.30. The dream to complete Killroy Prime is impossible
dreams_that_unlock_new_bonuses = [1, 3, 6, 8, 11, 14, 18, 21, 24, 29, 32]
#`DreamUpg = function ()` in source. Last updated in v2.46 Nov 19
equinox_bonuses_dict = {
    2: {'Name': 'Equinox Dreams', 'BaseLevel': 5, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 5, 'Category': 'Recommended', 'SummoningExpands': False},
    3: {'Name': 'Equinox Resources', 'BaseLevel': 4, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 4, 'Category': 'Recommended', 'SummoningExpands': False},
    4: {'Name': 'Shades of K', 'BaseLevel': 3, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 3, 'Category': 'Optional', 'SummoningExpands': False},
    5: {'Name': 'Liquidvestment', 'BaseLevel': 4, 'MaxLevelIncreases': {7: 3, 16: 4}, 'FinalMaxLevel': 11, 'Category': 'Recommended',
        'SummoningExpands': False},
    6: {'Name': 'Matching Scims', 'BaseLevel': 8, 'MaxLevelIncreases': {13: 5, 19: 10, 35: 10}, 'FinalMaxLevel': 33, 'Category': 'Recommended',
        'SummoningExpands': True},
    7: {'Name': 'Slow Roast Wiz', 'BaseLevel': 5, 'MaxLevelIncreases': {33: 6}, 'FinalMaxLevel': 11, 'Category': 'Recommended', 'SummoningExpands': True},
    8: {'Name': 'Laboratory Fuse', 'BaseLevel': 10, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 10, 'Category': 'Optional', 'SummoningExpands': False},
    9: {'Name': 'Metal Detector', 'BaseLevel': 6, 'MaxLevelIncreases': {}, 'FinalMaxLevel': 6, 'Category': 'Recommended', 'SummoningExpands': True},
    10: {'Name': 'Faux Jewels', 'BaseLevel': 6, 'MaxLevelIncreases': {22: 5, 27: 10}, 'FinalMaxLevel': 21, 'Category': 'Recommended', 'SummoningExpands': True},
    11: {'Name': 'Food Lust', 'BaseLevel': 10, 'MaxLevelIncreases': {26: 4}, 'FinalMaxLevel': 14, 'Category': 'Optional', 'SummoningExpands': True},
    12: {'Name': 'Equinox Symbols', 'BaseLevel': 5, 'MaxLevelIncreases': {31: 4}, 'FinalMaxLevel': 9, 'Category': 'Recommended', 'SummoningExpands': True},
    13: {'Name': 'Voter Rights', 'BaseLevel': 15, 'MaxLevelIncreases': {36: 15}, 'FinalMaxLevel': 30, 'Category': 'Recommended', 'SummoningExpands': True},
}
#`RefineryInfo = function` in source holds the material cost, if we ever want to care about that.
refinery_dict = {
    # 'salt': [json index, advice image name, cycles per Synth cycle, consumption of previous salt, next salt consumption, next salt cycles per Synth cycle]
    'Red': [3, 'redox-salts', 4, 0, 2, 4],
    'Orange': [4, 'explosive-salts', 4, 2, 2, 4],
    'Blue': [5, 'spontaneity-salts', 4, 2, 1, 1],
    'Green': [6, 'dioxide-synthesis', 1, 1, 2, 1],
    'Purple': [7, 'purple-salt', 1, 2, 2, 1],
    'Nullo': [8, 'nullo-salt', 1, 2, 0, 0]
}
#`TowerInfo = function ()` in source. Last updated in v2.46 Nov 29
#"3D_Printer Using_the_new_Star_Talent_(on_the_2nd_tab_of_Star_Talents),_you_can_collect_samples_to_start_printing_resources!_@_Current_Bonuses:_@_$_Player_Slots_Unlocked 1 30 Refinery1 Blank 3 0 10 1 10".split(" ")
#[0] = name, [1] = description,
#[2] = ?, [3] = ?, [4] = 1st required material. 2 and 3 are probably cost / scaling
#[5] = 2nd required material, [6] = ?, [7] = ?. 6 and 7 are probably cost / scaling
#[7] = default max level, [8] = ?, [9] = final max level after various upgrades
buildings_dict = {
    # Buildings
    0: {'Name': '3D Printer', 'Image': 'x3d-printer', 'BaseMaxLevel': 10, 'Type': 'Utility'},
    1: {'Name': 'Talent Book Library', 'Image': 'talent-book-library', 'BaseMaxLevel': 101, 'Type': 'Utility'},
    2: {'Name': 'Death Note', 'Image': 'death-note', 'BaseMaxLevel': 51, 'Type': 'Utility'},
    3: {'Name': 'Salt Lick', 'Image': 'salt-lick', 'BaseMaxLevel': 10, 'Type': 'Utility'},
    4: {'Name': 'Chest Space', 'Image': 'chest-space', 'BaseMaxLevel': 25, 'Type': 'Utility'},
    5: {'Name': 'Cost Cruncher', 'Image': 'cost-cruncher', 'BaseMaxLevel': 60, 'Type': 'Utility'},
    6: {'Name': 'Trapper Drone', 'Image': 'critter-drone', 'BaseMaxLevel': 15, 'Type': 'Utility'},
    7: {'Name': 'Automation Arm', 'Image': 'automation-arm', 'BaseMaxLevel': 5, 'Type': 'Utility'},
    8: {'Name': 'Atom Collider', 'Image': 'atom-collider', 'BaseMaxLevel': 200, 'Type': 'Utility'},
    # TD Towers
    9: {'Name': 'Pulse Mage', 'Image': 'pulse-mage', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    10: {'Name': 'Fireball Lobber', 'Image': 'fireball-lobber', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    11: {'Name': 'Boulder Roller', 'Image': 'boulder-roller', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    12: {'Name': 'Frozone Malone', 'Image': 'frozone-malone', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    13: {'Name': 'Stormcaller', 'Image': 'stormcaller', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    14: {'Name': 'Party Starter', 'Image': 'party-starter', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    15: {'Name': 'Kraken Cosplayer', 'Image': 'kraken-cosplayer', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    16: {'Name': 'Poisonic Elder', 'Image': 'poisonic-elder', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    17: {'Name': 'Voidinator', 'Image': 'voidinator', 'BaseMaxLevel': 50, 'Type': 'Tower'},
    # Shrines
    # ShrineInfo = function ()
    18: {'Name': 'Woodular Shrine', 'Image': 'woodular-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 12, 'ValueIncrement': 3},
    19: {'Name': 'Isaccian Shrine', 'Image': 'isaccian-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 12, 'ValueIncrement': 3},
    20: {'Name': 'Crystal Shrine', 'Image': 'crystal-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 20, 'ValueIncrement': 4},
    21: {'Name': 'Pantheon Shrine', 'Image': 'pantheon-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 10, 'ValueIncrement': 2},
    22: {'Name': 'Clover Shrine', 'Image': 'clover-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 15, 'ValueIncrement': 3},
    23: {'Name': 'Summereading Shrine', 'Image': 'summereading-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 6, 'ValueIncrement': 1},
    24: {'Name': 'Crescent Shrine', 'Image': 'crescent-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 50, 'ValueIncrement': 7.5},
    25: {'Name': 'Undead Shrine', 'Image': 'undead-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 5, 'ValueIncrement': 1},
    26: {'Name': 'Primordial Shrine', 'Image': 'primordial-shrine', 'BaseMaxLevel': 100, 'Type': 'Shrine', 'ValueBase': 1, 'ValueIncrement': 0.1},
}
# buildings_utilities = [buildingValuesDict['Name'] for buildingName, buildingValuesDict in buildings_dict.items() if buildingValuesDict['Type'] == 'Utility']

buildings_towers = [buildingValuesDict['Name'] for buildingName, buildingValuesDict in buildings_dict.items() if buildingValuesDict['Type'] == 'Tower']
# Last updated in v2.46 Nov 29
buildings_tower_max_level = (
    50  # Base
    + 30  # 2.5 Cons Mastery
    + 100  # 2 per level times 50 max levels of Atom Collider - Carbon
           # (including 20 max levels from WW Compass Atomic Potential)
    + 100  # Cavern 14 - Gambit - Bonus Index 9
)
buildings_shrines: list[str] = [buildingValuesDict['Name'] for buildingName, buildingValuesDict in buildings_dict.items() if
                                buildingValuesDict['Type'] == 'Shrine']

#`AtomInfo = function ()` in source. Last updated in v2.46 Nov 29
AtomInfo = ["Hydrogen_-_Stamp_Decreaser 1 1.35 2 1 Every_day_you_log_in,_the_resource_cost_to_upgrade_a_stamp's_max_lv_decreases_by_{%_up_to_a_max_of_90%._This_reduction_resets_back_to_0%_when_upgrading_any_stamp_max_lv.".split(" "), "Helium_-_Talent_Power_Stacker 0 10 10 1 All_talents_that_give_more_bonus_per_'Power_of_10_resources_you_own'_will_count_+{_more_powers_of_10_than_you_actually_own_when_giving_the_bonus.".split(" "), "Lithium_-_Bubble_Insta_Expander 10 1.25 25 1 No_Bubble_Left_Behind_bonus_now_has_a_15%_chance_to_level_up_the_lowest_bubble_out_of_ALL_bubbles,_not_just_the_first_15_of_each_colour._Also,_+{%_chance_to_give_+1_additional_Lv.".split(" "), "Beryllium_-_Post_Office_Penner 20 1.26 75 7 Every_day,_1_silver_pen_from_your_Post_Office_will_instantly_convert_into_1_PO_Box_for_all_characters._This_conversion_happens_{_times_per_day.".split(" "), "Boron_-_Particle_Upgrader 70 1.37 175 2 When_a_bubble_has_a_cost_of_100M_or_more_to_upgrade,_you_can_instead_spend_particles._However,_you_can_only_do_this_{_times_a_day,_after_which_the_cost_will_return_to_resources.".split(" "), "Carbon_-_Wizard_Maximizer 250 1.27 500 2 All_wizard_towers_in_construction_get_+{_max_levels._Also,_all_wizards_get_a_+2%_damage_bonus_for_each_wizard_tower_level_above_50_in_construction._Total_bonus:_}%_wizard_dmg.".split(" "), "Nitrogen_-_Construction_Trimmer 500 1.25 1000 15 Gold_trimmed_construction_slots_give_+{%_more_build_rate_than_before._Also,_you_now_have_1_additional_trimmed_slot.".split(" "), "Oxygen_-_Library_Booker 1000 1.24 3250 2 Increases_the_Checkout_Refresh_Speed_of_the_Talent_Library_by_+{%._Also,_the_Minimum_Talent_LV_is_increased_by_+<,_and_the_Maximum_Talent_LV_is_increased_by_+10.".split(" "), "Fluoride_-_Void_Plate_Chef 2500 1.23 2500 1 Multiplies_your_cooking_speed_by_+{%_for_every_meal_at_Lv_30+._In_other_words,_every_plate_with_a_studded_black_void_plate._Total_bonus:_>%_cooking_speed".split(" "), "Neon_-_Damage_N'_Cheapener 5000 1.22 5000 1 Increases_your_total_damage_by_+{%._Also,_reduces_the_cost_of_all_atom_upgrades_by_{%_too.".split(" "), "Sodium_-_Snail_Kryptonite 12000 2 12000 5 When_you_fail_a_snail_upgrade,_it's_LV_gets_reset_to_the_nearest_5_(Up_to_Lv_{)_instead_of_back_to_0,_like_failing_at_Lv_7_will_reset_to_Lv_5.".split(" "), "Magnesium_-_Trap_Compounder 30000 1.6 30000 1 Every_day,_critters_gained_from_traps_increases_by_+{%._This_bonus_is_capped_at_60_days,_and_resets_back_to_+0%_when_a_new_trap_is_placed.".split(" "), "Aluminium_-_Stamp_Supercharger 200000 1.45 200000 1 Stamp_Doublers_give_an_extra_+{%_MORE_bonus_than_the_normal_+100%_they_give!".split(" ")]
atoms_list = [
    [
        name.replace('_', ' '),
        parse_number(pos1),
        parse_number(pos2),
        parse_number(pos3),
        parse_number(valueperlevel),
        description.replace('_', ' ')
    ]
    for name, pos1, pos2, pos3, valueperlevel, description in AtomInfo
]
collider_storage_limit_list = [15, 25, 100, 250, 1050]

#Names and the soul costs to level the prayers are in `PrayerInfo = function ()` in source. Last updated in v2.46 Nov 29
#The numbers for the bonus and curse functions are elsewhere, so this remains handwritten for now. Pretty sure I stole formulas from Wiki
prayers_dict = {
    0: {"Name": "Big Brain Time", "Material": "Forest Soul", "Display": "Big Brain Time (Forest Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Class EXP', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 225, 'curse_x2': 25, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    1: {"Name": "Skilled Dimwit", "Material": "Forest Soul", "Display": "Skilled Dimwit (Forest Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Skill Efficiency', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'Skill EXP Gain', 'curse_pre': '-', 'curse_post': '%'},
    2: {"Name": "Unending Energy", "Material": "Forest Soul", "Display": "Unending Energy (Forest Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 22.5, 'bonus_x2': 2.5, 'bonus_stat': 'Class and Skill EXP', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 1, 'curse_x2': 0, 'curse_stat': 'Max AFK time is now 10 hours. Use with caution', 'curse_pre': '',
        'curse_post': ''},
    3: {"Name": "Shiny Snitch", "Material": "Forest Soul", "Display": "Shiny Snitch (Forest Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Shiny Critters per trap', 'bonus_pre': '+', 'bonus_post': '',
        "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'lower', 'curse_pre': 'Your Shiny chance is now ', 'curse_post': 'x'},
    4: {"Name": "Zerg Rushogen", "Material": "Forest Soul", "Display": "Zerg Rushogen (Forest Soul)", "MaxLevel": 20,
        "bonus_funcType": 'bigBase', 'bonus_x1': 4.5, 'bonus_x2': 0.5, 'bonus_stat': 'All AFK Gain Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 10.8, 'curse_x2': 1.2, 'curse_stat': 'Carry Capacity', 'curse_pre': '-', 'curse_post': '%'},
    5: {"Name": "Tachion of the Titans", "Material": "Dune Soul", "Display": "Tachion of the Titans (Dune Soul)", "MaxLevel": 2,
        "bonus_funcType": 'bigBase', 'bonus_x1': 1, 'bonus_x2': 0, 'bonus_stat': 'Giant Monsters can now spawn on Monster Kill', 'bonus_pre': '',
        'bonus_post': '',
        "curse_funcType": 'bigBase', 'curse_x1': 1, 'curse_x2': 0, 'curse_stat': 'Giant Monsters can now spawn...', 'curse_pre': '', 'curse_post': ''},
    6: {"Name": "Balance of Precision", "Material": "Dune Soul", "Display": "Balance of Precision (Dune Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Total Accuracy', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 4.5, 'curse_x2': 0.5, 'curse_stat': 'Total Damage', 'curse_pre': '-', 'curse_post': '%'},
    7: {"Name": "Midas Minded", "Material": "Dune Soul", "Display": "Midas Minded (Dune Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Drop Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 225, 'curse_x2': 2.5, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    8: {"Name": "Jawbreaker", "Material": "Dune Soul", "Display": "Jawbreaker (Dune Soul)", "MaxLevel": 50,
        "bonus_funcType": 'bigBase', 'bonus_x1': 36, 'bonus_x2': 4, 'bonus_stat': 'Coins from Monsters', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 180, 'curse_x2': 20, 'curse_stat': 'Max HP for all monsters', 'curse_pre': '+', 'curse_post': '%'},
    9: {"Name": "The Royal Sampler", "Material": "Rooted Soul", "Display": "The Royal Sampler (Rooted Soul)", "MaxLevel": 20,
        "bonus_funcType": 'bigBase', 'bonus_x1': 13.5, 'bonus_x2': 1.5, 'bonus_stat': 'Printer Sample Rate', 'bonus_pre': '+', 'bonus_post': '%',
        "curse_funcType": 'bigBase', 'curse_x1': 27, 'curse_x2': 3, 'curse_stat': 'All EXP gain. Remove all samples on this character to Unequip.',
        'curse_pre': '-', 'curse_post': '%'},
    10: {"Name": "Antifun Spirit", "Material": "Rooted Soul", "Display": "Antifun Spirit (Rooted Soul)", "MaxLevel": 10,
         "bonus_funcType": 'bigBase', 'bonus_x1': 630, 'bonus_x2': 70, 'bonus_stat': 'Minigame Reward Multi', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 8.1, 'curse_x2': 0.9, 'curse_stat': 'plays per attempt', 'curse_pre': 'Minigames cost ', 'curse_post': ''},
    11: {"Name": "Circular Criticals", "Material": "Rooted Soul", "Display": "Circular Criticals (Rooted Soul)", "MaxLevel": 20,
         "bonus_funcType": 'bigBase', 'bonus_x1': 9, 'bonus_x2': 1, 'bonus_stat': 'Critical Hit Chance', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Critical Damage', 'curse_pre': '-', 'curse_post': '%'},
    12: {"Name": "Ruck Sack", "Material": "Rooted Soul", "Display": "Ruck Sack (Rooted Soul)", "MaxLevel": 50,
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Carry Capacity', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'All AFK Gain Rate', 'curse_pre': '-', 'curse_post': '%'},
    13: {"Name": "Fibers of Absence", "Material": "Frigid Soul", "Display": "Fibers of Absence (Frigid Soul)", "MaxLevel": 50,
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Kills for Deathnote and opening portals', 'bonus_pre': '+',
         'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Total Damage', 'curse_pre': '-', 'curse_post': '%'},
    14: {"Name": "Vacuous Tissue", "Material": "Frigid Soul", "Display": "Vacuous Tissue (Frigid Soul)", "MaxLevel": 1,
         "bonus_funcType": 'bigBase', 'bonus_x1': 100, 'bonus_x2': 0, 'bonus_stat': 'Dungeon Credits and Flurbos from Boosted Runs', 'bonus_pre': '+',
         'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 2, 'curse_x2': 0, 'curse_stat': 'Dungeon Passes per run', 'curse_pre': 'Use ', 'curse_post': 'x'},
    15: {"Name": "Beefy For Real", "Material": "Frigid Soul", "Display": "Beefy For Real (Frigid Soul)", "MaxLevel": 40,
         "bonus_funcType": 'bigBase', 'bonus_x1': 18, 'bonus_x2': 2, 'bonus_stat': 'Total Damage', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 9, 'curse_x2': 1, 'curse_stat': 'Total Defence and Accuracy', 'curse_pre': '-', 'curse_post': '%'},
    16: {"Name": "Balance of Pain", "Material": "Squishy Soul", "Display": "Balance of Pain (Squishy Soul)", "MaxLevel": 30,
         "bonus_funcType": 'bigBase', 'bonus_x1': 7.2, 'bonus_x2': 0.8, 'bonus_stat': 'Multikill per Damage Tier', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 13.5, 'curse_x2': 1.5, 'curse_stat': 'Total Defence and Accuracy', 'curse_pre': '-', 'curse_post': '%'},
    17: {"Name": "Balance of Proficiency", "Material": "Squishy Soul", "Display": "Balance of Proficiency (Squishy Soul)", "MaxLevel": 50,
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'Skill EXP Gain', 'bonus_pre': '+', 'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'Skill Efficiency', 'curse_pre': '-', 'curse_post': '%'},
    18: {"Name": "Glitterbug", "Material": "Squishy Soul", "Display": "Glitterbug (Squishy Soul)", "MaxLevel": 30,
         "bonus_funcType": 'bigBase', 'bonus_x1': 27, 'bonus_x2': 3, 'bonus_stat': 'chance for Giant Mobs to summon 2 Crystal Mobs', 'bonus_pre': '+',
         'bonus_post': '%',
         "curse_funcType": 'bigBase', 'curse_x1': 18, 'curse_x2': 2, 'curse_stat': 'less likely to spawn', 'curse_pre': 'Giant Mobs are ', 'curse_post': '%'},
}
prayers_list: list[str] = [details['Display']for details in prayers_dict.values()]
conditional_prayers = {'Unending Energy': 50, 'Big Brain Time': 50, 'Antifun Spirit': 10, 'Fibers of Absence': 50, 'Beefy For Real': 40, 'Glitterbug': 25}
ignorable_prayers = {'Tachion of the Titans': 1, 'Balance of Precision': 1, 'Circular Criticals': 1, 'Vacuous Tissue': 1}
salt_lick_list: list[str] = [
    'Printer Sample Size', 'Obol Storage', 'Refinery Speed', 'EXP', 'Max Book',
    'Alchemy Liquids', 'TD Points', 'Movespeed', 'Multikill', 'Damage',
]

totems_max_wave = 300
totems_list = [
    'Goblin Gorefest',
    'Wakawaka War',
    'Acorn Assault',
    'Frosty Firefight',
    'Clash of Cans',
    'Citric Conflict',
    'Breezy Battle'
]

# TODO: W7 has added more sources
max_static_book_levels = (
    25  #Construction Building: Talent Level Library
    + 5  #W3 Achievement: Checkout Takeout
    + 125  #Sailing Artifact: Fury Relic. 25 per tier * 5 tiers
    + 10  #Atom Collider: Oxygen (level 1 gives all 10 levels)
    # 165 total last updated in v2.46 Nov 29
)
max_scaling_book_levels = (
    20  #Salt Lick
    + 10  #World 3 Merit Shop
    # 30 total last updated in v2.46 Nov 29
)
max_summoning_book_levels = round(
    (10.5  #Summoning Battle: Cyan 14
     + 3.5  #Summoning Battle: Teal 9
     )
    * ValueToMulti(50)  #Gem Shop: King of all Winners
    * ValueToMulti(30)  #Pristine Charm: Crystal Comb
    * ValueToMulti(
        1       #Achievement: Spectre Stars
        + 10    #World 6 Merit Shop
        + 15    #Armor Set bonus: Godshard Set
        + 125   #Sailing Artifact: Winz Lantern. 25 per tier * 5 tiers
    )
    #69 total last updated in v2.46 Nov 29
)
max_overall_book_levels = 100 + max_static_book_levels + max_scaling_book_levels + max_summoning_book_levels
hardcap_symbols = (max_overall_book_levels // 20) * 20

# see `TalentEnhDisp` in source (Amount of bonuses * 25). Last updated in v2.43 Nov 6
hardcap_enhancement_eclipse = 10 * 25
library_subgroup_tiers = [
    'Account Wide Priorities', 'Skilling - High Priority', 'Skilling - Medium Priority', 'Skilling - Low Priority', 'Skilling - Lowest Priority',
    'Combat - High Priority', 'Combat - Medium Priority', 'Combat - Low Priority', 'ALL Unmaxed Talents', 'VIP'
]  # Used in the Group by Priority function
old_library_subgroup_tiers = [
    '', 'Skilling - High Priority', 'Skilling - Medium Priority', 'Skilling - Low Priority', 'Skilling - Lowest Priority',
    'Combat - High Priority', 'Combat - Medium Priority', 'Combat - Low Priority', 'ALL Unmaxed Talents'
]  # Used in the Group by Character function
skill_talentsDict = {
    # Optimal is an optional list for calculating library.getJeapordyGoal
    # [0] = the starting level
    # [1] = the interval of levels after the starting level which provide a bonus
    # [2] = does this talent benefit from bonuses over the max book level, True of False]
    # Example: Symbols of Beyond gives a benefit every 20 levels and does NOT benefit from bonuses like Rift Slug of Arctis
    # 2nd example: Apocalypse ZOW gives a bonus every 33 and DOES benefit from bonuses

    # Wisdom Skills
    "Chopping": {
        "High": {
            460: {"Name": "Log on Logs", "Tab": "Tab 2"},
            445: {"Name": "Smart Efficiency", "Tab": "Tab 1"},
            462: {"Name": "Deforesting All Doubt", "Tab": "Tab 2"},
            461: {"Name": "Leaf Thief", "Tab": "Tab 2"},
            539: {"Name": "Symbols of Beyond P", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            532: {"Name": "Skill Wiz", "Tab": "Tab 4"},
        },
        "Medium": {
            533: {"Name": "Utmost Intellect", "Tab": "Tab 4"},
            456: {"Name": "Unt'WIS'ted Robes", "Tab": "Tab 2"},
            459: {"Name": "Individual Insight", "Tab": "Tab 2"},
            488: {"Name": "Wis Wumbo", "Tab": "Tab 3"},
            449: {"Name": "Active Afk'er", "Tab": "Tab 1"},
        },
        "Low": {
            452: {"Name": "Mana Overdrive", "Tab": "Tab 2"},
            472: {"Name": "Staring Statues", "Tab": "Tab 3"},
            487: {"Name": "Stupendous Statues", "Tab": "Tab 3"},
            1: {"Name": "Mana Booster", "Tab": "Tab 1"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            486: {"Name": "Occult Obols", "Tab": "Tab 3"},
        },
        "Lowest": {
            464: {"Name": "Inner Peace", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Alchemy": {
        "Medium": {
            492: {"Name": "Bubble Breakthrough", "Tab": "Tab 3"},
        },
        "Low": {
            493: {"Name": "Sharing Some Smarts", "Tab": "Tab 3"},  # Account-wide EXP bumped to Low
        },
    },
    "Laboratory": {
        "Low": {
            538: {"Name": "Upload Squared", "Tab": "Tab 4"},
            537: {"Name": "Essence Transferral", "Tab": "Tab 4"},
            536: {"Name": "Green Tube", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    "Worship": {
        "High": {
            476: {"Name": "Sooouls", "Tab": "Tab 3"},
        },
        "Medium": {
            303: {"Name": "Stop Right There", "Tab": "Tab 3"},
        },
        "Low": {
            478: {"Name": "Nearby Outlet", "Tab": "Tab 3"},
            475: {"Name": "Charge Syphon", "Tab": "Tab 3", 'Hardcap': 200},
        },
        "Lowest": {
            477: {"Name": "Bless Up", "Tab": "Tab 3"},
        },
    },
    "Divinity": {
        "Medium": {
            505: {"Name": "Polytheism", "Tab": "Tab 4"},  # Account-wide divinity points
            506: {"Name": "Shared Beliefs", "Tab": "Tab 4"},  # Account-wide EXP bumped to Medium because Divinity extra important
        },
    },
    # Strength Skills
    'Farming': {
        'High': {
            207: {'Name': 'Dank Ranks', 'Tab': 'Tab 5'}
        },
        'Medium': {
            205: {'Name': 'Mass Irrigation', 'Tab': 'Tab 5'}
        },
        'Low': {
            206: {'Name': "Agricultural 'Preciation", 'Tab': 'Tab 5'}
        },
    },
    "Cooking": {
        "High": {
            148: {"Name": "Overflowing Ladle", "Tab": "Tab 4"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
        },
        "Medium": {
            146: {"Name": "Apocalypse Chow", "Tab": "Tab 4"},
        },
        "Low": {
            147: {"Name": "Waiting to Cool", "Tab": "Tab 4"},
        },
    },
    "Fishing": {
        "High": {
            115: {"Name": "Worming Undercover", "Tab": "Tab 3"},
            85: {"Name": "Brute Efficiency", "Tab": "Tab 1"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Tab 4"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Tab 2"},
            143: {"Name": "Overblown Testosterone", "Tab": "Tab 4"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Tab 2"},
            94: {"Name": "Firmly Grasp It", "Tab": "Tab 2"},
            98: {"Name": "Absolute Unit", "Tab": "Tab 2"},
            81: {"Name": "Str Summore", "Tab": "Tab 3"},
            89: {"Name": "Idle Skilling", "Tab": "Tab 1"},
            118: {"Name": "Catching Some Zzz's", "Tab": "Tab 3"},
        },
        "Low": {
            112: {"Name": "Strongest Statues", "Tab": "Tab 3"},
            116: {"Name": "Bobbin' Bobbers", "Tab": "Tab 3", 'Hardcap': 200},
            111: {"Name": "Fistful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            117: {"Name": "All Fish Diet", "Tab": "Tab 3"},
        },
    },
    "Mining": {
        "High": {
            100: {"Name": "Big Pick", "Tab": "Tab 2"},
            85: {"Name": "Brute Efficiency", "Tab": "Tab 1"},
            103: {"Name": "Tool Proficiency", "Tab": "Tab 2"},
            101: {"Name": "Copper Collector", "Tab": "Tab 2"},
            149: {"Name": "Symbols of Beyond R", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            142: {"Name": "Skill Strengthen", "Tab": "Tab 4"},
        },
        "Medium": {
            99: {"Name": "Haungry for Gold", "Tab": "Tab 2"},
            203: {'Name': 'Built Different', 'Tab': 'Tab 5'},
            143: {"Name": "Overblown Testosterone", "Tab": "Tab 4"},
            96: {"Name": "'STR'ess Tested Garb", "Tab": "Tab 2"},
            94: {"Name": "Firmly Grasp It", "Tab": "Tab 2"},
            98: {"Name": "Absolute Unit", "Tab": "Tab 2"},
            81: {"Name": "Str Summore", "Tab": "Tab 3"},
            89: {"Name": "Idle Skilling", "Tab": "Tab 1"},
        },
        "Low": {
            92: {"Name": "Health Overdrive", "Tab": "Tab 2"},
            127: {"Name": "Shieldiest Statues", "Tab": "Tab 3"},
            112: {"Name": "Strongest Statues", "Tab": "Tab 3"},
            95: {"Name": "Strength in Numbers", "Tab": "Tab 2"},
            0: {"Name": "Health Booster", "Tab": "Tab 1"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            111: {"Name": "Fistful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            104: {"Name": "Tempestuous Emotions", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Construction": {
        "Medium": {
            131: {"Name": "Redox Rates", "Tab": "Tab 3"},
        },
        "Low": {
            130: {"Name": "Refinery Throttle", "Tab": "Tab 3", "Optimal": [0, 8, True]},
        },
        "Lowest": {
            132: {"Name": "Sharper Saws", "Tab": "Tab 3", 'Hardap': 160},
        },
    },
    "Gaming": {
        "Medium": {
            177: {"Name": "Bitty Litty", "Tab": "Tab 4"},
        },
        "Low": {
            175: {"Name": "Undying Passion", "Tab": "Tab 4"},
            176: {"Name": "1000 Hours Played", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    # Agility Skills
    "Smithing": {
        "High": {},
        "Medium": {},
        "Low": {
            269: {"Name": "Broken Time", "Tab": "Tab 1"},
            281: {"Name": "Acme Anvil", "Tab": "Tab 2"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
    "Catching": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Tab 1"},
            295: {"Name": "Teleki-net-ic Logs", "Tab": "Tab 3"},
            296: {"Name": "Briar Patch Runner", "Tab": "Tab 3"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Tab 4"},
        },
        "Medium": {
            298: {"Name": "Sunset on the Hives", "Tab": "Tab 3"},
            368: {"Name": "Adaptation Revelation", "Tab": "Tab 4"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Tab 2"},
            428: {'Name': 'Unreal Agility', 'Tab': 'Tab 5'},
            278: {"Name": "Sanic Speed", "Tab": "Tab 2"},
            293: {"Name": "Agi Again", "Tab": "Tab 3"},
        },
        "Low": {
            292: {"Name": "Shwifty Statues", "Tab": "Tab 3"},
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            291: {"Name": "Shoeful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
            297: {"Name": "Bug Enthusiast", "Tab": "Tab 3"},
        },
    },
    "Sailing": {
        "Low": {
            326: {"Name": "Expertly Sailed", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
            327: {"Name": "Captain Peptalk", "Tab": "Tab 4"},  # Account-wide Captain EXP bumped to low
        },
    },
    "Trapping": {
        "High": {
            263: {"Name": "Elusive Efficiency", "Tab": "Tab 1"},
            311: {"Name": "Invasive Species", "Tab": "Tab 3"},
            310: {"Name": "Eagle Eye", "Tab": "Tab 3"},
            374: {"Name": "Symbols of Beyond G", "Tab": "Tab 4", "Optimal": [0, 20, False], 'Hardcap': hardcap_symbols},
            367: {"Name": "Skill Ambidexterity", "Tab": "Tab 4"},
        },
        "Medium": {
            368: {"Name": "Adaptation Revelation", "Tab": "Tab 4"},
            276: {"Name": "Garb of Un'AGI'ng Quality", "Tab": "Tab 2"},
            428: {'Name': 'Unreal Agility', 'Tab': 'Tab 5'},
            278: {"Name": "Sanic Speed", "Tab": "Tab 2"},
            293: {"Name": "Agi Again", "Tab": "Tab 3"},
        },
        "Low": {
            144: {"Name": "The Family Guy", "Tab": "Tab 4"},
            291: {"Name": "Shoeful of Obol", "Tab": "Tab 3"},
        },
        "Lowest": {
            282: {"Name": "Yea I Already Know", "Tab": "Tab 2"},
            265: {"Name": "Focused Soul", "Tab": "Tab 2"},
        },
    },
    "Breeding": {
        "High": {
            373: {"Name": "Curviture Of The Paw", "Tab": "Tab 4"},
        },
        "Low": {
            372: {"Name": "Shining Beacon of Egg", "Tab": "Tab 4"},  # Account-wide EXP bumped to Low
        },
    },
    'Sneaking': {
        'High': {
            432: {'Name': 'Generational Gemstones', 'Tab': 'Tab 5'},
            430: {'Name': 'Price Recession', 'Tab': 'Tab 5'},
        },
        'Medium': {
            431: {'Name': 'Sneaky Skilling', 'Tab': 'Tab 5'},  # Account-wide EXP bumped to Medium
        }
    },
    # Utility is talents that apply to multiple skills at a bottom-of-the-group priority (Mostly Jman stuff + Drop Rate)
    "Utility": {
        "High": {
            43: {"Name": "Right Hand of Action", "Tab": "Tab 3"},
            32: {"Name": "Printer Go Brrr", "Tab": "Tab 3", "Optimal": [0, 40, True]},
            34: {"Name": "One Step Ahead", "Tab": "Tab 3"},
            59: {"Name": "Blood Marrow", "Tab": "Tab 4"},
            57: {"Name": "Species Epoch", "Tab": "Tab 4"},
            49: {"Name": "Enhancement Eclipse", "Tab": "Tab 4", "Optimal": [0, 25, False], 'Hardcap': hardcap_enhancement_eclipse},
            53: {"Name": "Eternal WIS", "Tab": "Tab 4"},
            51: {"Name": "Eternal STR", "Tab": "Tab 4"},
            52: {"Name": "Eternal AGI", "Tab": "Tab 4"},
        },
        "Medium": {
            41: {"Name": "Crystal Countdown", "Tab": "Tab 3"},
            28: {"Name": "Cards Galore", "Tab": "Tab 2"},
            29: {"Name": "Rares Everywhere", "Tab": "Tab 2"},
            24: {"Name": "Curse of Mr Looty Booty", "Tab": "Tab 2"},
            56: {"Name": "Voodoo Statufication", "Tab": "Tab 4"},
            78: {"Name": "Extra Bags", "Tab": "Tab 1"},
            39: {"Name": "Colloquial Containers", "Tab": "Tab 3"},
        },
        "Low": {
            279: {"Name": "Robbinghood", "Tab": "Tab 2"},
            37: {"Name": "Skilliest Statue", "Tab": "Tab 3"},
            27: {"Name": "Reroll Pls", "Tab": "Tab 2"},
        },
        "Lowest": {
            42: {"Name": "Left Hand of Learning", "Tab": "Tab 3"},
            40: {"Name": "Maestro Transfusion", "Tab": "Tab 3"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            17: {'Name': 'Supernova Player', "Tab": "Tab 2"},
            8: {'Name': 'Star Player', "Tab": "Tab 1"}
        },
    },
}
combat_talentsDict = {
    # Talents here are unique from the skill_talentsDict above
    # Warriors
    "Death Bringer": {
        "High": {
            198: {'Name': 'Graveyard Shift', 'Tab': 'Tab 5'},
            196: {'Name': 'Grimoire', 'Tab': 'Tab 5'},
            199: {'Name': 'Detonation', 'Tab': 'Tab 5'},
            200: {'Name': 'Marauder Style', 'Tab': 'Tab 5'},
            197: {'Name': 'Sentinel Axes', 'Tab': 'Tab 5'},

        },
        "Medium": {
            195: {'Name': 'Wraith Form', 'Tab': 'Tab 5'},
            202: {'Name': "Famine O' Fish", 'Tab': 'Tab 5'},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            140: {"Name": "Tough Steaks", "Tab": "Tab 4"},
        },
    },
    "Blood Berserker": {
        "High": {},
        "Medium": {
            108: {"Name": "No Pain No Gain", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            140: {"Name": "Tough Steaks", "Tab": "Tab 4"},
        },
    },
    "Barbarian": {
        "High": {},
        "Medium": {
            108: {"Name": "No Pain No Gain", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            110: {"Name": "Apocalypse Zow", "Tab": "Tab 3"},
        },
    },
    "Divine Knight": {
        "High": {
            168: {"Name": "Orb of Remembrance", "Tab": "Tab 4"},
            120: {"Name": "Shockwave Slash", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            165: {"Name": "Knightly Disciple", "Tab": "Tab 4"},  # Inconsistent levels for extra attacks per Stark. Idk, just max book it and deal with it
            169: {"Name": "Imbued Shockwaves", "Tab": "Tab 4"},
            121: {"Name": "Daggerang", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            166: {"Name": "Mega Mongorang", "Tab": "Tab 4"},
        },
        "Medium": {
            178: {"Name": "King of the Remembered", "Tab": "Tab 4"},
            129: {"Name": "Blocky Bottles", "Tab": "Tab 3"},
            125: {"Name": "Precision Power", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            141: {"Name": "Charred Skulls", "Tab": "Tab 4"},
            170: {"Name": "Gamer Strength", "Tab": "Tab 4"},
        },
    },
    "Squire": {
        "High": {
            120: {"Name": "Shockwave Slash", "Tab": "Tab 3", "Optimal": [0, 30, True]},
            121: {"Name": "Daggerang", "Tab": "Tab 3", "Optimal": [0, 30, True]}, },
        "Medium": {
            129: {"Name": "Blocky Bottles", "Tab": "Tab 3"},
            125: {"Name": "Precision Power", "Tab": "Tab 3"},
            97: {"Name": "Carry a Big Stick", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            88: {"Name": "Idle Brawling", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },

    # Mages
    "Bubonic Conjuror": {
        "High": {
            490: {"Name": "Cranium Cooking", "Tab": "Tab 3"},
            481: {"Name": "Auspicious Aura", "Tab": "Tab 3"},
            483: {"Name": "Tenteyecle", "Tab": "Tab 3"},
            529: {"Name": "Raise Dead", "Tab": "Tab 4", 'Hardcap': 200},
            526: {"Name": "Flatulent Spirit", "Tab": "Tab 4"},
            525: {"Name": "Chemical Warfare", "Tab": "Tab 4"},
        },
        "Medium": {
            485: {"Name": "Virile Vials", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            531: {"Name": "Memorial Skulls", "Tab": "Tab 4"},
            530: {"Name": "Wired In Power", "Tab": "Tab 4"},
        },
    },
    "Shaman": {
        "High": {
            490: {"Name": "Cranium Cooking", "Tab": "Tab 3"},
            481: {"Name": "Auspicious Aura", "Tab": "Tab 3"},
            483: {"Name": "Tenteyecle", "Tab": "Tab 3"},
        },
        "Medium": {
            485: {"Name": "Virile Vials", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },
    "Elemental Sorcerer": {
        "High": {
            469: {"Name": "Mana Is Life", "Tab": "Tab 3"},
            496: {"Name": "Lightning Barrage", "Tab": "Tab 4"},
            497: {"Name": "Radiant Chainbolt", "Tab": "Tab 4"},
            467: {"Name": "Tornado", "Tab": "Tab 3"},
            466: {"Name": "Floor Is Lava", "Tab": "Tab 3"},
            498: {"Name": "Dimensional Wormhole", "Tab": "Tab 4"},
        },
        "Medium": {
            508: {"Name": "Wormhole Emperor", "Tab": "Tab 4"},
            474: {"Name": "Fuscia Flasks", "Tab": "Tab 3"},
            470: {"Name": "Paperwork, Great", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            507: {"Name": "Gods Chosen Children", "Tab": "Tab 4"},
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            531: {"Name": "Memorial Skulls", "Tab": "Tab 4"},
            463: {"Name": "Choppin It Up Ez", "Tab": "Tab 2"},
            451: {"Name": "Mini Fireball", "Tab": "Tab 2"},
            500: {"Name": "Believer Strength", "Tab": "Tab 4"},
        },
    },
    "Wizard": {
        "High": {
            469: {"Name": "Mana Is Life", "Tab": "Tab 3"},
            467: {"Name": "Tornado", "Tab": "Tab 3"},
            466: {"Name": "Floor Is Lava", "Tab": "Tab 3"},
        },
        "Medium": {
            474: {"Name": "Fuscia Flasks", "Tab": "Tab 3"},
            470: {"Name": "Paperwork, Great", "Tab": "Tab 3"},
            455: {"Name": "Knowledge Is Power", "Tab": "Tab 2"},
            457: {"Name": "Power Overwhelming", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            448: {"Name": "Idle Casting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            463: {"Name": "Choppin It Up Ez", "Tab": "Tab 2"},
            451: {"Name": "Mini Fireball", "Tab": "Tab 2"},
        },
    },

    # Archers
    "Siege Breaker": {
        "High": {
            318: {"Name": "Pirate Flag", "Tab": "Tab 4"},
            319: {"Name": "Plunder Ye Deceased", "Tab": "Tab 4"},
            316: {"Name": "Suppressing Fire", "Tab": "Tab 4", 'Optimal': [0, 33, True]},
            317: {"Name": "Firebomb", "Tab": "Tab 4", 'Optimal': [0, 50, True]},
            315: {"Name": "Cannonball", "Tab": "Tab 4"},
            285: {"Name": "Homing Arrows", "Tab": "Tab 3", 'Optimal': [0, 15, True]},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            289: {"Name": "Woah, That Was Fast", "Tab": "Tab 3"},
            286: {"Name": "Magic Shortbow", "Tab": "Tab 3", 'Optimal': [0, 20, True]},
            328: {"Name": "Archlord Of The Pirates", "Tab": "Tab 4"},
            290: {"Name": "Speedna", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            366: {"Name": "Stacked Skulls", "Tab": "Tab 4"},
            320: {"Name": "Crew Rowing Strength", "Tab": "Tab 4"},
        },
    },
    "Bowman": {
        "High": {
            285: {"Name": "Homing Arrows", "Tab": "Tab 3", 'Optimal': [0, 15, True]},
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            289: {"Name": "Woah, That Was Fast", "Tab": "Tab 3"},
            286: {"Name": "Magic Shortbow", "Tab": "Tab 3", 'Optimal': [0, 20, True]},
            290: {"Name": "Speedna", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },
    'Wind Walker': {
        "High": {
            424: {'Name': 'Some Commandments', 'Tab': 'Tab 5'},
            422: {'Name': 'Spirit Ballista', 'Tab': 'Tab 5'},
            423: {'Name': 'Eternal Hunt', 'Tab': 'Tab 5'},
            421: {'Name': 'Compass', 'Tab': 'Tab 5'},
            425: {'Name': 'Windborne', 'Tab': 'Tab 5'},
            426: {'Name': 'Elemental Mayhem', 'Tab': 'Tab 5'},
            362: {"Name": "Whale Wallop", "Tab": "Tab 4", 'Optimal': [0, 17, True]},
            301: {"Name": "Bear Trap", "Tab": "Tab 3", 'Optimal': [0, 30, True]},
            300: {"Name": "360 Noscope", "Tab": "Tab 3", },
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
            361: {"Name": "Boar Rush", "Tab": "Tab 4", 'Optimal': [0, 20, True]},
        },
        "Medium": {
            363: {"Name": "Nacho Party", "Tab": "Tab 4", 'Optimal': [0, 13, True]},
            305: {"Name": "Looty Mc Shooty", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            433: {'Name': 'Dustwalker', 'Tab': 'Tab 5'},
            434: {'Name': 'Slayer Abominator', 'Tab': 'Tab 5'},
            427: {'Name': "Pumpin' Power", 'Tab': 'Tab 5'},
            420: {'Name': 'Tempest Form', 'Tab': 'Tab 5'},
            428: {'Name': 'Shiny Medallions', 'Tab': 'Tab 5'},
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            366: {"Name": "Stacked Skulls", "Tab": "Tab 4"},
            365: {"Name": "Animalistic Ferocity", "Tab": "Tab 4"},
        },
    },
    "Beast Master": {
        "High": {
            362: {"Name": "Whale Wallop", "Tab": "Tab 4", 'Optimal': [0, 17, True]},
            301: {"Name": "Bear Trap", "Tab": "Tab 3", 'Optimal': [0, 30, True]},
            300: {"Name": "360 Noscope", "Tab": "Tab 3", },
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
            363: {"Name": "Nacho Party", "Tab": "Tab 4", 'Optimal': [0, 13, True]},
            361: {"Name": "Boar Rush", "Tab": "Tab 4", 'Optimal': [0, 20, True]},
        },
        "Medium": {
            305: {"Name": "Looty Mc Shooty", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            366: {"Name": "Stacked Skulls", "Tab": "Tab 4"},
            365: {"Name": "Animalistic Ferocity", "Tab": "Tab 4"},
        },
    },
    "Hunter": {
        "High": {
            301: {"Name": "Bear Trap", "Tab": "Tab 3", 'Optimal': [0, 30, True]},
            300: {"Name": "Three-Sixty Noscope", "Tab": "Tab 3", },
            270: {"Name": "Piercing Arrow", "Tab": "Tab 2", 'Optimal': [0, 40, True]},
        },
        "Medium": {
            305: {"Name": "Looty Mc Shooty", "Tab": "Tab 3"},
            273: {"Name": "Strafe", "Tab": "Tab 2"},
            284: {"Name": "Veins of the Infernal", "Tab": "Tab 2"},
            277: {"Name": "High Polymer Limbs", "Tab": "Tab 2"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            268: {"Name": "Idle Shooting", "Tab": "Tab 1"},
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
        },
    },

    # Secret Class
    "Voidwalker": {
        "High": {
            19: {"Name": "Gimme Gimme", "Tab": "Tab 2"},
            26: {"Name": "Cmon Out Crystals", "Tab": "Tab 2"},
            46: {"Name": "Void Radius", "Tab": "Tab 4"},
            45: {"Name": "Void Trial Rerun", "Tab": "Tab 4"},
            47: {"Name": "Bossing Vain", "Tab": "Tab 4"},
            58: {"Name": "Master of the System", "Tab": "Tab 4"},
        },
        "Medium": {
            50: {"Name": "Power Orb", "Tab": "Tab 4"},
            48: {"Name": "Quad Jab", "Tab": "Tab 4"},
            33: {"Name": "Triple Jab", "Tab": "Tab 3"},
            18: {"Name": "Two Punch Man", "Tab": "Tab 2"},
            31: {"Name": "Skillage Damage", "Tab": "Tab 3"},
            20: {"Name": "Lucky Hit", "Tab": "Tab 2"},
            54: {"Name": "Eternal Luk", "Tab": "Tab 4"},
            21: {"Name": "F'LUK'ey Fabrics", "Tab": "Tab 2"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            36: {"Name": "Clever Clover Obols", "Tab": "Tab 3"},
        }
    },
    "Maestro": {
        "High": {
            19: {"Name": "Gimme Gimme", "Tab": "Tab 2"},
            26: {"Name": "Cmon Out Crystals", "Tab": "Tab 2"},
        },
        "Medium": {
            33: {"Name": "Triple Jab", "Tab": "Tab 3"},
            18: {"Name": "Two Punch Man", "Tab": "Tab 2"},
            31: {"Name": "Skillage Damage", "Tab": "Tab 3"},
            20: {"Name": "Lucky Hit", "Tab": "Tab 2"},
            21: {"Name": "F'LUK'ey Fabrics", "Tab": "Tab 2"},
            38: {"Name": "Bliss N Chips", "Tab": "Tab 3"},
            6: {"Name": "Gilded Sword", "Tab": "Tab 1"},
        },
        "Low": {
            5: {"Name": "Sharpened Axe", "Tab": "Tab 1"},
            36: {"Name": "Clever Clover Obols", "Tab": "Tab 3"},
        }
    },
}
unbookable_talents_list = [
    10, 11, 12,  # Tab 1 STR, AGI, WIS
    75, 79,  # Beginner tab1 Happy Dude and Sleepin' on the Job
    23,  # Journeyman Lucky Horseshoe
    86, 87,  # Warrior tab1 Meat Shank and Critikill
    266, 267,  # Archer tab1 Featherweight and I See You
    446, 447,  # Mage tab1 Overclocked Energy and Farsight
]
approx_max_talent_level_star_talents = (
    max_overall_book_levels
    + 30  # Grimoire
    + 60  # Equinox last updated in v2.46 Nov 29, including +10 from Gaming: Duper Bits: Equinox Unending
    + 25  # Companion: Rift Slug
    + 32  # Arctis last updated in v2.46 Nov 29
    + (1 + hardcap_symbols // 20)  # Symbols of Beyond last updated in v2.46 Nov 29 
    + 15  # ES Family Bonus (Note: Not Family Guy!)
    + 5  # Sneak Mastery III
    + 5  # Kattlekruk Set
    + 1  # Maroon Warship achievement
)
approx_max_talent_level_non_es_non_star = (
    approx_max_talent_level_star_talents
    + 50  # Super Talent Points 1/1. Last updated in v2.46 Nov 29
    + 50  # Super Duper Talents 5/5. Last updated in v2.46 Nov 29
    + 25  # Zenith Super Dupers 25/25. Last updated in v2.46 Nov 29
)
approx_max_talent_level_es = approx_max_talent_level_non_es_non_star + 6  # Family Guy, last updated in v2.46 Nov 29


dn_skull_requirement_list = [0, 25000, 100000, 250000, 500000, 1000000, 5000000, 100000000, 1000000000]
dn_miniboss_skull_requirement_list = [0, 100, 250, 1000, 5000, 25000, 100000, 1000000, 1000000000]
dn_skull_value_list = [0, 1, 2, 3, 4, 5, 7, 10, 20]
dn_skull_names = [
    'None',
    'Normal Skull',
    'Copper Skull',
    'Iron Skull',
    'Gold Skull',
    'Platinum Skull',
    'Dementia Skull',
    'Lava Skull',
    'Eclipse Skull',
]
dn_skull_value_to_name_dict = dict(zip(dn_skull_value_list, dn_skull_names))
dn_skull_name_to_requirement_normal = dict(zip(dn_skull_names, dn_skull_requirement_list))
dn_skull_name_to_requirement_miniboss = dict(zip(dn_skull_names, dn_miniboss_skull_requirement_list))
dn_miniboss_names = [
    'Glunko The Massive', 'Dr Defecaus', 'Baba Yaga', 'Biggie Hours', 'King Doot',
    'Dilapidated Slush', 'Mutated Mush', 'Domeo Magmus', 'Demented Spiritlord'
]
reversed_dn_skull_requirement_list = dn_skull_requirement_list[::-1]
reversed_dn_skull_value_list = dn_skull_value_list[::-1]

apocable_map_index_dict = {
    0: [30, 9, 38, 69, 120, 166],  # Barbarian only, not in regular DeathNote
    1: [1, 2, 14, 17, 16, 13, 18, 19, 24, 26, 27, 28, 8, 15, 31],
    2: [51, 52, 53, 57, 58, 59, 60, 62, 63, 64, 65],
    3: [101, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 116, 117],
    4: [151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163],
    5: [201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213],
    6: [251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264],
    7: [301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312]
}
dn_basic_maps_count = sum([len(v) for k, v in apocable_map_index_dict.items() if k > 0])
dn_all_apoc_maps_count = dn_basic_maps_count + len(apocable_map_index_dict[0])
apoc_amounts_list = [100000, 1000000, 100000000, 1000000000, 1000000000000]
apoc_names_list = ["ZOW", "CHOW", "MEOW", "WOW", "Unfiltered"]
apoc_difficulty_name_list = [
    'Basic W1 Enemies', 'Basic W2 Enemies', 'Basic W3 Enemies', 'Basic W4 Enemies', 'Basic W5 Enemies', 'Basic W6 Enemies',
    'Easy Extras', 'Medium Extras', 'Difficult Extras', 'Insane', 'Impossible'
]
dn_delays = {
    # DelayUntilTier allows a monster map to be skipped until a particular tier
    # DelayUntilSkull allows a monster map to be skipped until the tier requires a particular Skull value, i.e. 20 for Eclipse Skull
    #W1
    'Where the Branches End': {'DelayUntilTier': 22},
    #W6
    'Yolkrock Basin': {'DelayUntilSkull': dn_skull_value_list[7]},
    'Chieftain Stairway': {'DelayUntilSkull': dn_skull_value_list[7]},
    "Emperor's Castle Doorstep": {'DelayUntilSkull': dn_skull_value_list[8]}
}

max_trapping_critter_types = 12
trapping_quests_requirement_list = [
    {"QuestName": "Frogecoin to the MOON!", 'RequiredItems': {"Critter1": 100, "Critter1A": 1}},
    {"QuestName": "Yet another Cartoon Reference", 'RequiredItems': {"Critter2": 250, "Critter2A": 1}},
    {"QuestName": "Small Stingers, Big Owie", 'RequiredItems': {"Critter3": 500, "Critter3A": 2}},
    {"QuestName": "The Mouse n the Molerat", 'RequiredItems': {"Critter4": 1000, "Critter4A": 2}},
    {"QuestName": "Happy Tree Friend", 'RequiredItems': {"Critter5": 1500, "Critter5A": 3}},
    {"QuestName": "Noot Noot!", 'RequiredItems': {"Critter6": 2500, "Critter6A": 4}},
    {"QuestName": "Bunny you Should Say That!", 'RequiredItems': {"Critter7": 4000, "Critter7A": 6}},
    {"QuestName": "Rollin' Thunder", 'RequiredItems': {"Critter8": 8000, "Critter8A": 10}},
    {"QuestName": "Glitter Critter", 'RequiredItems': {"Critter8A": 30, "Critter6A": 60, "Critter3A": 200}}
]
trapset_images = {
    0: 'cardboard-traps',
    1: 'silkskin-traps',
    2: 'wooden-traps',
    3: 'natural-traps',
    4: 'steel-traps',
    5: 'meaty-traps',
    6: 'royal-traps',
    7: 'egalitarian-traps',
    8: 'forbidden-traps',
    9: 'containment-of-the-zrgyios'
}


def getSkullNames(mkValue: int) -> str:
    try:
        return dn_skull_value_to_name_dict.get(mkValue, f"UnknownSkull{mkValue}")
    except Exception as reason:
        return f"Unexpected Input '{mkValue}' received: {reason}"


def getNextSkullNames(mkValue: int) -> str:
    if mkValue == dn_skull_value_list[-1]:
        return "Finished!"
    else:
        try:
            return dn_skull_names[dn_skull_value_list.index(mkValue) + 1]
        except Exception as reason:
            return f"Unexpected Input '{mkValue}' received: {reason}"


def getEnemyNameFromMap(inputMap: str) -> str:
    mapNametoEnemyNameDict = {
        # W1 Maps
        "Spore Meadows": "Green Mushroom",
        "Froggy Fields": "Frog",
        "Valley of the Beans": "Bored Bean",
        "Birch Enclave": "Red Mushroom",
        "Jungle Perimeter": "Slime",
        "The Base of the Bark": "Stick",
        "Hollowed Trunk": "Nutto",
        "Where the Branches End": "Wood Mushroom",
        "Winding Willows": "Baby Boa",
        "Vegetable Patch": "Carrotman",
        "Forest Outskirts": "Glublin",
        "Encroaching Forest Villa": "Wode Board",
        "Tucked Away": "Gigafrog",
        "Poopy Sewers": "Poop",
        "Rats Nest": "Rat",
        "The Roots": "Special - Single Nutto at WorshipTD map",
        "The Office": "Special - Poops surrounding Dr.Def",
        "Meel's Crypt": "Special- Boop",

        # W2 Maps
        "Jar Bridge": "Sandy Pot",
        "The Mimic Hole": "Mimic",
        "Dessert Dunes": "Crabcake",
        "The Grandioso Canyon": "Mafioso",
        "Shifty Sandbox": "Sand Castle",
        "Pincer Plateau": "Pincermin",
        "Slamabam Straightaway": "Mashed Potato",
        "The Ring": "Tyson",
        "Up Up Down Down": "Moonmoon",
        "Sands of Time": "Sand Giant",
        "Djonnuttown": "Snelbie",
        "Mummy Memorial": "Special- Invisible Green Mushroom inside King Doot's map",

        # W3 Maps
        "Steep Sheep Ledge": "Sheepie",
        "Snowfield Outskirts": "Frost Flake",
        "The Stache Split": "Sir Stache",
        "Refrigeration Station": "Bloque",
        "Mamooooth Mountain": "Mamooth",
        "Rollin' Tundra": "Snowmen",
        "Signature Slopes": "Penguin",
        "Thermonuclear Climb": "Thermister",
        "Waterlogged Entrance": "Quenchie",
        "Cryo Catacombs": "Cryosnake",
        "Overpass of Sound": "Bop Box",
        "Crystal Basecamp": "Neyeptune",
        "Wam Wonderland": "Dedotated Ram",
        "Hell Hath Frozen Over": "Bloodbone",
        "Equinox Valley": "Special- AFK only Dedotated Ram",

        # W4 Maps
        "Spaceway Raceway": "Purp Mushroom",
        "TV Outpost": "TV",
        "Donut Drive-In": "Donut",
        "Outskirts of Fallstar Isle": "Demon Genie",
        "Mountainous Deugh": "Soda Can",
        "Wurm Highway": "Flying Worm",
        "Jelly Cube Bridge": "Gelatinous Cuboid",
        "Cocoa Tunnel": "Choccie",
        "Standstill Plains": "Biggole Wurm",
        "Shelled Shores": "Clammie",
        "The Untraveled Octopath": "Octodar",
        "Flamboyant Bayou": "Flombeige",
        "Enclave of Eyes": "Stilted Seeker",
        "The Rift": "Rift Monsters",

        # W5 Maps
        "Naut Sake Perimeter": "Suggma",
        "Niagrilled Falls": "Maccie",
        "The Killer Roundabout": "Mister Brightside",
        "Cracker Jack Lake": "Cheese Nub",
        "The Great Molehill": "Stiltmole",
        "Erruption River": "Molti",
        "Mount Doomish": "Purgatory Stalker",
        "OJ Bay": "Citringe",
        "Lampar Lake": "Lampar",
        "Spitfire River": "Fire Spirit",
        "Miner Mole Outskirts": "Biggole Mole",
        "Crawly Catacombs": "Crawler",
        "The Worm Nest": "Tremor Wurm",

        # W6 Maps
        "Gooble Goop Creek": "Sprout Spirit",
        "Picnic Bridgeways": "Ricecake",
        "Irrigation Station": "River Spirit",
        "Troll Playground": "Baby Troll",
        "Edge of the Valley": "Woodlin Spirit",
        "Bamboo Laboredge": "Bamboo Spirit",
        "Lightway Path": "Lantern Spirit",
        "Troll Broodnest": "Mama Troll",
        "Above the Clouds": "Leek Spirit",
        "Sleepy Skyline": "Ceramic Spirit",
        "Dozey Dogpark": "Skydoggie Spirit",
        "Yolkrock Basin": "Royal Egg",
        "Chieftain Stairway": "Minichief Spirit",
        "Emperor's Castle Doorstep": "Samurai Guardian",
    }
    try:
        return mapNametoEnemyNameDict.get(inputMap, f"UnknownMap:{inputMap}")
    except Exception as reason:
        return f"Unexpected Input received: {reason}"


def getDNKillRequirement(miniboss=False, skull_value=None, skull_name=''):
    required_kills = 0
    if skull_value is not None:
        required_kills = (
            dn_skull_requirement_list[dn_skull_value_list.index(skull_value)]
            if miniboss is False else
            dn_miniboss_skull_requirement_list[dn_skull_value_list.index(skull_value)]
        )
    elif skull_name != '':
        required_kills = (
            dn_skull_name_to_requirement_normal[skull_name]
            if miniboss is False else
            dn_skull_name_to_requirement_miniboss[skull_name]
        )
    return required_kills


printer_indexes_being_printed_by_character_index = [
    [5, 6],  # Character Index 0
    [12, 13],
    [19, 20],
    [26, 27],
    [33, 34],
    [40, 41],  # Character Index 5
    [47, 48],
    [54, 55],
    [61, 62],
    [68, 69],  # Character Index 9
]
# This flattens the above list of lists. Nested list comprehension sucks to read
printer_all_indexes_being_printed = [index for character_index in printer_indexes_being_printed_by_character_index for index in character_index]

#`EquipmentSets = function ()` in source. Last updated in v2.46 Nov 29
equipment_sets_dict = {
    'COPPER_SET': [
        ["EquipmentHats17", "EquipmentShirts11", "EquipmentPants2"],
        "EquipmentTools2 EquipmentToolsHatchet3 FishingRod2 CatchingNet2 TrapBoxSet2 WorshipSkull2".split(" "),
        ["none"],
        ["1", "0", "60", "+{%_Mining_and|Chopping_Efficiency", "+{%_Mining_and_Chopping|Efficiency"]
    ],
    'IRON_SET': [
        ["EquipmentHats18", "EquipmentShirts12", "EquipmentPants3"],
        ["EquipmentTools3", "EquipmentToolsHatchet1", "FishingRod3", "CatchingNet3", "WorshipSkull2"],
        ["none"],
        ["1", "0", "25", "+{%_Class_EXP_Gain", "+{%_Class_EXP_Gain"]
    ],
    'AMAROK_SET': [
        ["EquipmentHats22", "EquipmentShirts18", "EquipmentPants17", "EquipmentShoes20"],
        ["none"],
        ["none"],
        ["0", "0", "40", "+{%_Accuracy_and|Defence", "+{%_Accuracy_and_Defence"]
    ],
    'GOLD_SET': [
        ["EquipmentHats28", "EquipmentShirts13", "EquipmentPants4", "EquipmentShoes3"],
        ["EquipmentTools5", "EquipmentToolsHatchet2", "FishingRod4", "CatchingNet4", "WorshipSkull2"],
        ["EquipmentPunching3", "TestObj3", "EquipmentBows5", "EquipmentWands5"],
        ["1", "1", "50", "}x_Coins_Dropped|by_Monsters", "}x_Coins_Dropped_by_Monsters"]
    ],
    'PLATINUM_SET': [
        ["EquipmentHats19", "EquipmentShirts14", "EquipmentPants5", "EquipmentShoes4"],
        "EquipmentTools6 EquipmentToolsHatchet4 FishingRod5 CatchingNet5 TrapBoxSet3 WorshipSkull3".split(" "),
        ["EquipmentSword1", "EquipmentBows6", "EquipmentWands6"],
        ["1", "1", "60", "+{%_Fishing_and|Catching_Efficiency", "+{%_Fishing_and_Catching|Efficiency"]
    ],
    'EFAUNT_SET': [
        ["EquipmentHats52", "EquipmentShirts26", "EquipmentPants20", "EquipmentShoes21"],
        ["none"],
        ["none"],
        ["0", "0", "25", "+{%_Drop_Rate", "+{%_Drop_Rate"]
    ],
    'DEMENTIA_SET': [
        ["EquipmentHats53", "EquipmentShirts15", "EquipmentPants6", "EquipmentShoes5"],
        "EquipmentTools7 EquipmentToolsHatchet5 FishingRod6 CatchingNet6 TrapBoxSet4 WorshipSkull4".split(" "),
        ["EquipmentPunching4", "EquipmentSword2", "EquipmentBows7", "EquipmentWands3"],
        ["2", "1", "50", "+{%_Critters_and|Souls_gained", "+{%_Critters_and_Souls_gained"]
    ],
    'VOID_SET': [
        ["EquipmentHats54", "EquipmentShirts27", "EquipmentPants21", "EquipmentShoes22"],
        "EquipmentTools11 EquipmentToolsHatchet7 FishingRod7 CatchingNet7 TrapBoxSet5 WorshipSkull5".split(" "),
        ["EquipmentPunching5", "EquipmentSword3", "EquipmentBows8", "EquipmentWands7"],
        ["2", "1", "10", "+{%_AFK_Gains", "+{%_AFK_Gains"]
    ],
    'CHIZOAR_SET': [
        ["EquipmentHats68", "EquipmentShirts6", "EquipmentPants9", "EquipmentShoes23"],
        ["none"],
        ["none"],
        ["0", "0", "40", "+{%_All_Skill_EXP|Gain", "+{%_All_Skill_EXP_Gain"]
    ],
    'LUSTRE_SET': [
        ["EquipmentHats70", "EquipmentShirts32", "EquipmentPants24", "EquipmentShoes24"],
        "EquipmentTools8 EquipmentToolsHatchet6 FishingRod8 CatchingNet8 TrapBoxSet6 WorshipSkull6".split(" "),
        ["EquipmentPunching6", "EquipmentSword4", "EquipmentBows9", "EquipmentWands8"],
        ["2", "1", "75", "+{%_Total_Damage", "+{%_Total_Damage"]
    ],
    'DIABOLICAL_SET': [
        ["EquipmentHats71", "EquipmentShirts33", "EquipmentPants25", "EquipmentShoes25"],
        "EquipmentTools12 EquipmentToolsHatchet8 FishingRod9 CatchingNet9 TrapBoxSet7 WorshipSkull7".split(" "),
        ["EquipmentPunching7", "EquipmentSword5", "EquipmentBows10", "EquipmentWands9"],
        ["2", "1", "20", "+{%_Faster_Monster|Respawning", "+{%_Faster_Monster_Respawning"]
    ],
    'TROLL_SET': [
        ["EquipmentHats74", "EquipmentShirts34", "EquipmentPants8", "EquipmentShoes34"],
        ["none"],
        ["none"],
        ["0", "0", "25", "}x_Higher_Bonuses|from_Tome", "}x_Higher_Bonuses_from_Tome"]
    ],
    'MAGMA_SET': [
        ["EquipmentHats77", "EquipmentShirts35", "EquipmentPants26", "EquipmentShoes35"],
        "EquipmentTools9 EquipmentToolsHatchet9 FishingRod10 CatchingNet10 TrapBoxSet8 WorshipSkull9".split(" "),
        ["EquipmentPunching8", "EquipmentSword6", "EquipmentBows11", "EquipmentWands10"],
        ["3", "1", "100", "+{%_Lab_and|Divinity_EXP_Gain", "+{%_Lab_and_Divinity_EXP_Gain"]
    ],
    'KATTLEKRUK_SET': [
        ["EquipmentHats83", "EquipmentShirts36", "EquipmentPants27", "EquipmentShoes36", "EquipmentCape13"],
        ["none"],
        ["EquipmentPunching9", "EquipmentSword7", "EquipmentBows12", "EquipmentWands11"],
        ["0", "1", "5", "+{_LV_for_all_Talents", "+{_LV_for_all_Talents"]
    ],
    'MARBIGLASS_SET': [
        ["EquipmentHats105", "EquipmentShirts37", "EquipmentPants29", "EquipmentShoes37"],
        "EquipmentTools14 EquipmentToolsHatchet12 FishingRod11 CatchingNet11 TrapBoxSet9 WorshipSkull10".split(" "),
        ["EquipmentPunching10", "EquipmentSword8", "EquipmentBows13", "EquipmentWands12"],
        ["4", "1", "10", "+{%_All_Stat", "+{%_All_Stat"]
    ],
    'GODSHARD_SET': [
        ["EquipmentHats106", "EquipmentShirts38", "EquipmentPants30", "EquipmentShoes38"],
        "EquipmentTools15 EquipmentToolsHatchet10 FishingRod12 CatchingNet12 TrapBoxSet10 WorshipSkull11".split(" "),
        ["EquipmentPunching11", "EquipmentSword9", "EquipmentBows14", "EquipmentWands13"],
        ["6", "1", "15", "}x_Higher_Winners|Bonuses_from_Summoning", "}x_Higher_Winners_Bonuses_from|Summoning"]
    ],
    'EMPEROR_SET': [
        "EquipmentHats119 EquipmentShirts39 EquipmentPants31 EquipmentShoes40 EquipmentRings36 EquipmentCape17".split(" "),
        ["none"],
        ["none"],
        ["0", "0", "20", "Ribbons_and_Exalted|Stamps_give_}x_more_multi", "Ribbons_and_Exalted_Stamps|give_}x_more_multi"]
    ],
    'PREHISTORIC_SET': [
        ["EquipmentHats123", "EquipmentShirts41", "EquipmentPants32", "EquipmentShoes41"],
        "EquipmentTools16 EquipmentToolsHatchet13 FishingRod13 CatchingNet13 TrapBoxSet11 WorshipSkull12".split(" "),
        ["EquipmentPunching12", "EquipmentSword10", "EquipmentBows15", "EquipmentWands14"],
        ["6", "1", "100", "}x_EXP_Gain_in_all|World_7_Skills", "}x_EXP_Gain_in_all_World_7|Skills"]
    ],
    'SECRET_SET': [
        ["EquipmentHats61", "EquipmentPunching11", "EquipmentShirts31", "Trophy3", "EquipmentNametag4"],
        ["none"],
        ["none"],
        ["0", "0", "25", "}x_Gold_Food|effect", "}x_Gold_Food_effect"]
    ],
}
