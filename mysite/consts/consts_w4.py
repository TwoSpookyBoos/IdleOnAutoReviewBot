import math
from consts.consts_idleon import NinjaInfo
from utils.safer_data_handling import safer_math_pow
from utils.number_formatting import parse_number
from utils.text_formatting import kebab
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)

tomepct = {
    95: 1015,
    90: 1447,
    80: 2532,
    70: 4132,
    60: 7884,
    50: 12726,
    25: 28707,
    10: 37451,
    5: 39670,
    1: 42116,
    0.5: 42698,
    0.1: 43425,
}

#`Tome = function ()` in source. Last updated in v2.46 Nov 29
tome_challenges = ["Stamp_Total_LV 10000 0 1000 filler Your_Tome_Score_of_#_PTS_is_in_the_Top_$_of_all_players_in_IdleOn!_@___@_If_you_can_reach_~_PTS,_you'll_be_in_the_Top_`_of_all_players!".split(" "), "Statue_Total_LV 2300 0 600 filler filler".split(" "), "Cards_Total_LV 1344 2 1000 filler filler".split(" "), "Total_Talent_Max_LV_膛_(Tap_for_more_info) 12000 0 600 filler For_each_talent,_the_tome_counts_the_highest_Max_LV_out_of_all_your_players.".split(" "), "Unique_Quests_Completed_膛 323 2 500 filler Doing_the_same_quest_on_multiple_players_doesn't_count_for_this.".split(" "), "Account_LV 7000 0 1500 filler filler".split(" "), "Total_Tasks_Completed 470 2 470 filler filler".split(" "), "Total_Achievements_Completed 266 2 850 filler filler".split(" "), "Most_Money_held_in_Storage 25 1 500 filler filler".split(" "), "Most_Spore_Caps_held_in_Inventory_at_once 9 1 200 filler filler".split(" "), "Trophies_Found 22 2 700 filler filler".split(" "), "Account_Skills_LV 18000 0 1200 filler filler".split(" "), "Best_Spiketrap_Surprise_round 13 2 100 filler filler".split(" "), "Total_AFK_Hours_claimed 2000000 0 350 filler filler".split(" "), "DPS_Record_on_Shimmer_Island 20 1 350 filler filler".split(" "), "Star_Talent_Points_Owned 2500 0 200 filler filler".split(" "), "Average_kills_for_a_Crystal_Spawn_膛 30 3 350 filler This_tracks_your_Crystal_Mob_spawn_chance!_While_this_is_capped_at_1_in_100,_you_get_BONUS_Exp_and_Drops_if_your_Crystal_Spawn_is_better!_For_example,_if_your_average_kills_is_20,_you're_getting_5x_Exp_and_Drops_from_Crystals!".split(" "), "Dungeon_Rank 30 0 250 filler filler".split(" "), "Highest_Drop_Rarity_Multi 40 0 350 1 filler".split(" "), "Constellations_Completed 49 2 300 filler filler".split(" "), "Most_DMG_Dealt_to_Gravestone_in_a_Weekly_Battle_膛 300000 0 200 filler Gravestone_appears_when_you_defeat_all_weekly_bosses._This_is_the_negative_number_shown_after.".split(" "), "Unique_Obols_Found 107 2 250 filler filler".split(" "), "Total_Bubble_LV 200000 0 1200 filler filler".split(" "), "Total_Vial_LV 962 2 500 filler filler".split(" "), "Total_Sigil_LV 72 2 250 filler filler".split(" "), "Jackpots_Hit_in_Arcade 1 0 50 filler filler".split(" "), "Post_Office_PO_Boxes_Earned 20000 0 300 filler filler".split(" "), "Highest_Killroy_Score_on_a_Warrior 3000 0 200 filler filler".split(" "), "Highest_Killroy_Score_on_an_Archer 3000 0 200 filler filler".split(" "), "Highest_Killroy_Score_on_a_Mage 3000 0 200 filler filler".split(" "), "Fastest_Time_to_kill_Chaotic_Efaunt_(in_Seconds) 10 3 200 filler filler".split(" "), "Largest_Oak_Log_Printer_Sample 9 1 400 filler filler".split(" "), "Largest_Copper_Ore_Printer_Sample 9 1 400 filler filler".split(" "), "Largest_Spore_Cap_Printer_Sample 9 1 300 filler filler".split(" "), "Largest_Goldfish_Printer_Sample 9 1 300 filler filler".split(" "), "Largest_Fly_Printer_Sample 9 1 300 filler filler".split(" "), "Best_Non_Duplicate_Goblin_Gorefest_Wave_膛 120 0 200 filler Non_Duplicate_means_you_can_only_place_1_of_each_Wizard_Type,_2_or_more_invalidates_the_attempt.".split(" "), "Total_Best_Wave_in_Worship 1000 0 300 filler filler".split(" "), "Total_Digits_of_all_Deathnote_Kills_膛 700 0 600 filler For_example,_1,520_kills_would_be_4_digits,_and_this_is_for_all_monster_types.".split(" "), "Equinox_Clouds_Completed 31 2 750 filler filler".split(" "), "Total_Refinery_Rank 120 0 450 filler filler".split(" "), "Total_Atom_Upgrade_LV 150 0 400 filler filler".split(" "), "Total_Construct_Buildings_LV 4000 0 900 filler filler".split(" "), "Most_Tottoise_in_Storage_膛 5 1 150 filler Tottoise_is_the_11th_Shiny_Critter_unlocked_from_the_Jade_Emporium_in_World_6".split(" "), "Most_Greenstacks_in_Storage_膛 150 0 600 filler Greenstack_is_when_you_have_10,000,000_or_more_of_a_single_item_in_your_Storage_Chest.".split(" "), "Rift_Levels_Completed 49 2 500 filler filler".split(" "), "Highest_Power_Pet 5 1 150 filler filler".split(" "), "Fastest_Time_reaching_Round_100_Arena_(in_Seconds) 50 3 180 filler filler".split(" "), "Total_Kitchen_Upgrade_LV 8000 0 200 filler filler".split(" "), "Total_Shiny_Pet_LV 750 0 250 filler filler".split(" "), "Total_Cooking_Meals_LV 5400 0 750 filler filler".split(" "), "Total_Pet_Breedability_LV 500 2 200 filler filler".split(" "), "Total_Lab_Chips_Owned 100 0 150 filler filler".split(" "), "Total_Colosseum_Score 10 1 200 filler filler".split(" "), "Most_Giants_Killed_in_a_Single_Week 25 0 250 filler filler".split(" "), "Total_Onyx_Statues 28 2 450 filler filler".split(" "), "Fastest_Time_to_Kill_200_Tremor_Wurms_(in_Seconds) 30 3 150 filler filler".split(" "), "Total_Boat_Upgrade_LV 10000 0 200 filler filler".split(" "), "God_Rank_in_Divinity 10 0 200 filler filler".split(" "), "Total_Gaming_Plants_Evolved 100000 0 200 filler filler".split(" "), "Total_Artifacts_Found_膛 185 2 1000 filler Rarer_versions_of_an_artifact_count_for_more,_so_Ancient_would_count_as_2_Artifacts.".split(" "), "Gold_Bar_Sailing_Treasure_Owned 14 1 200 filler filler".split(" "), "Highest_Captain_LV 25 0 150 filler filler".split(" "), "Highest_Immortal_Snail_LV 50 2 300 filler filler".split(" "), "Best_Gold_Nugget 9 1 200 filler filler".split(" "), "Items_Found 1800 2 1300 filler filler".split(" "), "Most_Gaming_Bits_Owned 80 1 400 filler filler".split(" "), "Highest_Crop_OG 6 1 200 filler filler".split(" "), "Total_Crops_Discovered 120 2 350 filler filler".split(" "), "Total_Golden_Food_Beanstacks_膛 30 2 400 filler Supersized_Gold_Food_Beanstacks_count_as_2_Beanstacks!".split(" "), "Total_Summoning_Upgrades_LV 10000 0 200 filler filler".split(" "), "Total_Career_Summoning_Wins_膛 160 0 500 filler Rack_up_those_wins!_Endless_Summoning_wins_count_for_this_too,_of_course!".split(" "), "Ninja_Floors_Unlocked 12 2 250 filler filler".split(" "), "Familiars_Owned_in_Summoning_膛 600 0 150 filler Measured_in_terms_of_Grey_Slime,_so_a_Vrumbi_would_count_as_3,_Bloomy_as_12,_and_so_on.".split(" "), "Jade_Emporium_Upgrades_Purchased 50 2 700 filler filler".split(" "), "Total_Minigame_Highscore_膛 450 2 100 filler This_is_Choppin_game,_Mining_Cart_game,_Fishing_game,_Catching_Hoops_game,_and_Trapping_game".split(" "), "Total_Prayer_Upgrade_LV 673 2 200 filler filler".split(" "), "Total_Land_Rank_膛 5000 0 200 filler Land_Ranks_are_from_the_Farming_skill,_in_World_6._Unlocked_from_the_Night_Market!".split(" "), "Largest_Magic_Bean_Trade 1000 0 200 filler filler".split(" "), "Most_Balls_earned_from_LBoFaF_膛 1000 0 150 filler LBoFaF_means_Lava's_Ballpit_of_Fire_and_Fury,_the_bonus_round_in_Arcade".split(" "), "Total_Arcade_Gold_Ball_Shop_Upgrade_LV 3800 2 800 filler filler".split(" "), "Vault_Upgrade_bonus_LV 500 2 500 filler filler".split(" "), "Total_Gambit_Time_(in_Seconds)_膛 3600 0 400 filler Gambit_is_the_14th_Cavern_in_The_Hole.".split(" "), "Total_Digits_of_all_Cavern_Resources_膛 500 0 750 filler For_example,_if_you_had_1273_gravel_and_422_gold_dust,_thats_7_Digits._If_you_then_got_23_quaver_notes_from_harp,_thats_another_2_digits,_making_your_total_9_Digits.".split(" "), "Total_LV_of_Cavern_Villagers 200 0 350 filler filler".split(" "), "Megafeathers_Earned_from_Orion 12 0 250 filler filler".split(" "), "Megafish_Earned_from_Poppy 12 0 250 filler filler".split(" "), "Best_Bravery_Monument_Round_膛 50 0 250 filler Bravery_Monument_is_the_4th_Cavern_in_The_Hole._The_Hole_is_found_in_World_5.".split(" "), "Best_Justice_Monument_Round_膛 200 0 250 filler Justice_Monument_is_the_10th_Cavern_in_The_Hole._'Best_Round'_here_means_your_highest_Court_Case_reached_in_a_run.".split(" "), "Best_Wisdom_Monument_Round_膛 18 2 250 filler Wisdom_Monument_is_the_13th_Cavern_in_The_Hole.".split(" "), "Best_Deathbringer_Max_Damage_in_Wraith_Mode_膛 10 1 400 filler Deathbringer_is_the_Blood_Berserker's_Master_Class,_given_by_Masterius_NPC_in_World_6._You_need_to_open_your_grimoire_to_register_damage.".split(" "), "Best_Dawg_Den_score_膛 7 1 250 filler The_Dawg_Den_is_the_3rd_Cavern_in_The_Hole._The_Hole_is_found_in_World_5.".split(" "), "Total_Resource_Layers_Destroyed_膛 150 0 350 filler Destroying_Layers_includes_the_following_caverns..._Motherlode,_Eternal_Hive,_and_Evertree_Cavern,_with_more_added_later!".split(" "), "Total_Opals_Found 500 0 400 filler filler".split(" "), "Best_Pure_Memory_Round_Reached_膛 13 2 50 filler Yea_nah,_I_aint_snitchin'._This_is_a_SECRET_mode.".split(" "), "Spirited_Valley_Emperor_Boss_Kills_膛 100 2 400 filler This_counts_your_current_Showdown_for_the_Emperor_boss_in_World_6,_not_the_total_amount_of_kills.".split(" "), "Total_Summoning_Boss_Stone_victories_膛 28 0 300 filler This_is_the_TOTAL_wins_you_have_against_all_Summoning_Bosses_combined._These_are_the_bossfights_from_the_stones,_like_the_one_next_to_Tribal_Shaman_NPC!".split(" "), "Total_Coral_Reef_upgrades_膛 37 2 400 filler The_Coral_Reef_is_a_feature_in_World_7_town,_unlocked_by_rescuing_Humble_Hugh's_missing_Fishies!".split(" "), "Deepest_Depth_reached_in_a_single_Delve_膛 100 0 300 filler This_is_for_the_Spelunking_skill,_it's_just_the_deepest_you've_gone_in_a_single_attempt.".split(" "), "Total_Ninja_Knowledge_Upgrades_LV_膛 5000 0 500 filler Ninja_Knowledge_is_the_upgrade_tree_accessed_within_Sneaking._This_includes_mini_knowledge_upgrades,_but_you'll_unlock_those_later...".split(" "), "Best_Windwalker_Max_Damage_in_Tempest_Mode_膛 10 1 400 filler Windwalker_is_the_Beast_Masters's_Master_Class,_given_by_Masterius_NPC_in_World_6._You_need_to_open_your_Compass_to_register_damage.".split(" "), "Best_Arcane_Cultist_Max_Damage_in_Arcanist_Mode_膛 10 1 400 filler Arcane_Cultist_is_the_Bubonic_Conjuror's_Master_Class,_given_by_Masterius_NPC_in_World_6._You_need_to_open_your_Tesseract_to_register_damage.".split(" "), "Biggest_Haul_in_a_single_Delve_膛 25 1 300 filler This_is_for_the_Spelunking_skill,_it's_just_the_most_amount_of_Amber_you've_gotten_in_a_single_attempt.".split(" "), "Total_Spelunk_Shop_Upgrades_LV 2000 0 500 filler filler".split(" "), "Total_Spelunk_Discoveries_made_膛 76 2 300 filler A_Discovery_is_when_you_destroy_a_rock_for_the_first_time_in_a_cave._It's_basically_how_many_unique_'things'_you've_encountered_while_spelunking!".split(" "), "Highest_leveled_Spelunker_膛 200 0 200 filler In_other_words,_this_is_the_Spelunking_LV_of_the_highest_leveled_spelunker_in_your_account.".split(" "), "Lava_Dev_Streams_watched_膛 10 2 250 filler Hey_this_one's_about_me!_In_order_to_get_credit_for_watching_one_of_my_streams,_you_need_to_get_a_gem_drop_from_me_while_I'm_live_on_twitch_at_____Twitch.tv/_lava贫flame2".split(" "), "Nametags_Found_膛 20 2 700 filler This_only_counts_the_amount_of_unique_nametags_you_found..._but_don't_throw_away_your_duplicate_nametags!_You'll_need_them_for_The_Gallery_in_World_7!".split(" ")]
tome_challenges_count = len(tome_challenges)
# Formula pulled from `if ("TomeLvReq" == e)` under `_customBlock_Summoning = function`. Last updated in v2.46 Nov 29
def get_final_combat_level_required_for_tome() -> int:
    #return 40 * t + (5 * Math.max(0, t - 35) + (10 * Math.max(0, t - 60) + (10 * Math.max(0, t - 80) + 15 * Math.max(0, t - 100)))) + 350;
    result = (
        40 * tome_challenges_count
        + (5 * max(0, tome_challenges_count - 35))
        + (10 * max(0, tome_challenges_count - 60))
        + (10 * max(0, tome_challenges_count - 80))
        + (15 * max(0, tome_challenges_count - 100))
        + 350
    )
    return result


max_cooking_tables = 10  # Last updated in v2.46 Nov 29
max_meal_level = 150  # Last updated in v2.46 Nov 29
max_cooking_ribbon = 23  # Last updated in v2.46 Nov 29
cooking_close_enough = 300  # Last updated in v2.46 Nov 29
#`MealINFO = function ()` in source. Last updated in v2.46 Nov 29
MealINFO = ["Turkey_a_la_Thank 10 2 +{%_Total_Damage Do_I_smell_gratitude?_Oh,_no,_that's_colonialization... TotDmg".split(" "), "Egg 15 5 +{%_Meal_Cooking_Speed It's_just_an_egg. Mcook".split(" "), "Salad 25 3 +{%_Cash_from_Monsters Yea_uhm,_could_I_get_a_burger,_but_hold_the_meat_and_buns? Cash".split(" "), "Pie 40 5 +{%_New_Recipe_Cooking_Speed Cartoon_characters_with_a_fear_of_levitation_HATE_the_smell_of_this! Rcook".split(" "), "Frenk_Fries 60 5 +{%_New_Pet_Breeding_Odds You're_breeding_pets_in_outer_space,_don't_be_shocked_that_there's_no_France! Npet".split(" "), "Spaghetti 90 4 +{%_Breeding_EXP Your_mom_made_this._It's_her_spaghetti. BrExp".split(" "), "Corn 125 2 +{%_Skill_Efficiency To_think_the_government_is_subsidizing_this..._its_bonus_is_terrible!!! Seff".split(" "), "Garlic_Bread 175 4 +{%_VIP_Library_Membership The_letter_H_ain't_lookin'_so_good_after_eating_a_few_of_these... VIP".split(" "), "Garlicless_Bread 250 2 +{%_Lab_EXP Many_revolutions_in_the_world_originate_from_an_increase_in_the_price_of_bread Lexp".split(" "), "Pizza 350 9 +{%_New_Pet_Breeding_Odds Mama_mia_mahhh_piiiiiiiizzza!!!_Wait_I_already_did_that_joke,_replace_this_one Npet".split(" "), "Apple 500 5 +{_Base_DEF Aw_jeez_Richard,_I_sure_am_hungry_for_apples! Def".split(" "), "Pancakes 700 2 +{Px_Line_Width_in_Lab_Mainframe Ohhh,_they're_called_'pan'cakes_because_they're_like_cakes_made_in_a_pan_haha PxLine".split(" "), "Corndog 1000 12 +{%_Meal_Cooking_Speed Ohhh,_they're_called_'corn'dogs_because..._wait,_why_are_they_called_corndogs? Mcook".split(" "), "Cabbage 1400 5 +{%_Cooking_Spd_per_10_Kitchen_LVs More_speed_every_10_total_kitchen_upgrade_LVs!_That's_one_IMPORTANT_vegetable! KitchenEff".split(" "), "Potato_Pea_Pastry 2000 1 +{%_Lower_Egg_Incubator_Time Yuhhhh_it's_that_Triple_P_threat!_Look_out_for_them_P's_bro! TimeEgg".split(" "), "Dango 3000 2 +{%_Lower_Kitchen_Upgrade_Costs Look,_I'm_not_sure_what_these_are_either,_just_go_with_it. KitchC".split(" "), "Sourish_Fish 4000 4 +{%_VIP_Library_Membership Shhh_stop_saying_they're_sweet,_you're_gonna_get_me_in_trouble! VIP".split(" "), "Octoplop 5000 2 +{%_Total_Damage They_really_did_just_plop_an_octopus_on_a_plate_and_call_it_a_day. TotDmg".split(" "), "Croissant 8000 1 +{%_Pet_Fighting_Damage Carl_loves_these! PetDmg".split(" "), "Canopy 12500 10 +{%_New_Recipe_Cooking_Speed ...oh,_you_said_'Can_of_Pea's._You_know,_that_does_make_a_lot_more_sense. Rcook".split(" "), "Cannoli 20000 1 +{%_Points_earned_in_Tower_Defence Ain't_got_no_joke_for_this_one,_it's_existence_is_enough_of_a_joke. TDpts".split(" "), "Cheese 35000 5 +{%_Cooking_EXP Sourced_organically,_straight_from_the_moon! CookExp".split(" "), "Sawdust 50000 5 +{%_Lab_EXP 'Id_rather_starve_than_eat_that'_-_Angie,_2021 Lexp".split(" "), "Eggplant 75000 5 +{%_Pet_Breedability_Speed Idk_what_you_Zoomers_are_up_to_with_those_eggplant_emojis,_but_I_don't_like_it... Breed".split(" "), "Cheesy_Bread 110000 1 +{%_Total_Accuracy Another_bread_meal?_Wow_so_unoriginal,_I'm_glad_I_already_left_a_1_star_rating. TotAcc".split(" "), "Wild_Boar 200000 2 +{Px_Line_Width_in_Lab_Mainframe It's_not_really_wild_anymore_is_it,_it_looks_kinda_dead_and_roasted. PxLine".split(" "), "Donut 300000 15 +{%_New_Pet_Breeding_Odds Mmmmm..._doooooooonut... Npet".split(" "), "Riceball 500000 3 +{%_Skill_Efficiency Dude_it's_just_a_ball_of_rice,_like_what_do_you_want_me_to_say_about_it? Seff".split(" "), "Cauliflower 750000 1 +{%_Basic_Atk_Speed The_white_part_is_called_Curd!_Hmm,_time_to_recategorize_this_as_an_educational_game! AtkSpd".split(" "), "Durian_Fruit 1000000 6 +{%_Lower_Kitchen_Upgrade_costs This_must_have_been_in_the_room_when_Kurt_said_it_smelled_like_'teen_spirit'... KitchC".split(" "), "Orange 1500000 3 +{%_VIP_Library_Membership The_true_arch-nemesis_of_rappers_and_poets_alike. VIP".split(" "), "Bunt_Cake 3000000 7 +{%_Cash_from_Monsters Bunt_cake_more_like_Punt_cake_because_I'm_kicking_this_trash_straight_to_the_garbage. Cash".split(" "), "Chocolate_Truffle 5000000 25 +{%_New_Pet_Breeding_Odds I_mean_it's_got_a_bite_taken_out_of_it,_pretty_gross. Npet".split(" "), "Leek 8000000 2 +{%_skilling_prowess Prowess_lowers_the_efficiency_needed_when_efficiency_bar_is_orange_in_AFK_info Sprow".split(" "), "Fortune_Cookie 12000000 4 +{%_Faster_Library_checkout_Speed It_reads:_'Salvation_lies_not_within_enjoying_video_games,_but_from_gitting_gud_at_them' Lib".split(" "), "Pretzel 20000000 7 +{%_Lab_EXP I_love_pretzels,_people_really_be_sleepin'_on_the_versatility_they_bring_to_the_table! Lexp".split(" "), "Sea_Urchin 30000000 1 +{%_Critters_from_traps At_least_one_person_reading_this_has_eating_one_of_these._Oh,_it's_you?_Good_for_you. Critter".split(" "), "Mashed_Potato 40000000 6 +{%_Cooking_EXP This_nutritious_meal_reminds_me_of_the_potato_monster_from_that_IdleOn_video_game! CookExp".split(" "), "Mutton 90000000 1 +{%_Crit_Chance Yeap_I_tell_you_hwat_Bobby,_this_is_a_real_man's_meal_right_here! Crit".split(" "), "Wedding_Cake 135000000 2 +{%_Pet_Fighting_Damage Imagine_getting_married_lol_so_cringe_haha_am_I_right??!?!_High-five,_fellow_kids! PetDmg".split(" "), "Eel 200000000 1 +{%_Line_Width_in_Lab_Mainframe The_younger_sibling_of_the_Loch_Ness_Monster._He's_real,_but_no_one_really_cares. LinePct".split(" "), "Whipped_Cocoa 300000000 4 +{%_Skill_Efficiency Why_is_this_being_served_on_a_plate?_Was_the_cup_not_good_enough_for_you?? Seff".split(" "), "Onion 500000000 3 +{%_Total_Damage No,_I'm_not_crying,_this_onion_is_just_stimulating_the_lachrymal_glands_in_my_eyes. TotDmg".split(" "), "Soda 700000000 20 +{%_Meal_Cooking_Speed Yea_those_red_marks_are_grill_marks,_our_chef_doesn't_know_what_he's_doing. Mcook".split(" "), "Sushi_Roll 900000000 7 +{%_VIP_Library_Membership For_something_called_a_'sushi_roll',_it_isn't_moving_around_very_much. VIP".split(" "), "Buncha_Banana 1250000000.0 4 +{_Max_LVs_for_TP_Pete_Star_Talent Straight_from_the_island_of_Karjama!_Or_something_like_that,_starts_with_a_K_at_least. TPpete".split(" "), "Pumpkin 1700000000.0 2 +{%_Liquid_Cap_for_liquids_1_and_2 According_to_the_author_of_the_Iliad,_its_value_should_peak_right_around_January... Liquid12".split(" "), "Cotton_Candy 4000000000.0 2 +{%_Divinity_EXP The_most_exquisite_of_fairground_cuisine! DivExp".split(" "), "Massive_Fig 7000000000.0 3 +{%_Total_Damage This_thing_has_gotta_weigh_at_least_30! TotDmg".split(" "), "Head_Chef_Geustloaf 10000000000.0 4 +{%_Bits_Gained_in_Gaming How_DARE_you_question_the_honorable_Chef_Geustloaf's_cooking_abilities! GamingBits".split(" "), "Kiwi_Fruit 14000000000.0 2 +{%_Liquid_Cap_for_liquids_3_and_4 Is_there_a_reason_these_are_so_hard_to_cook?_Aren't_you_just_like..._cutting_it_in_half? Liquid34".split(" "), "Popped_Corn 20000000000.0 2 +{%_Sailing_Speed Effectively_no_different_than_a_normal_bowl_of_popcorn,_but_it's_still_impressive! Sailing".split(" "), "Double_Cherry 32000000000.0 30 +{%_Meal_Cooking_Speed So_like..._why_did_the_yellow_circle_want_these_again?_This_bonus_is_pretty_bad. Mcook".split(" "), "Ratatouey 52000000000.0 8 +{%_Lower_Kitchen_Upgrade_costs Hey_cmon_man_how_should_I_know_how_to_spell_Ratatouille,_there's_no_France_remember? KitchC".split(" "), "Giant_Tomato 90000000000.0 5 +{%_Gaming_EXP It's_big,_it's_large,_it's_round,_it's_red,_and_it'll_fill_you_up_thats_for_sure! GamingExp".split(" "), "Wrath_Grapes 130000000000.0 4 +{%_Divinity_EXP I'd_be_angry_too_if_I_were_a_grape. DivExp".split(" "), "Sausy_Sausage 225000000000.0 6 +{%_Bits_Gained_in_Gaming Plump_innit!_Would_go_great_with_some_momey_milk! GamingBits".split(" "), "Seasoned_Marrow 350000000000.0 3 +{%_Farming_EXP You_ate_all_the_edible_stuff_around_the_bone?_Why_not_try_the_stuff_inside_the_bone! zFarmExp".split(" "), "Sticky_Bun 700000000000.0 5 +{%_All_Summoning_Essence_Gain This_frosting_better_be_made_of_superglue_or_I'm_suing_for_false_advertising. zSumEss".split(" "), "Frazzleberry 1000000000000.0 2 +{%_Sneaking_EXP Big._Blue._Beautiful._Boing._Boat._Broom._Balls._Backgammon._Bort. zSneakExp".split(" "), "Misterloin_Steak 1700000000000.0 6 +{%_Jade_gain_from_Sneaking Make_sure_to_paint_on_the_grill_marks_to_really_give_it_that_extra_taste! zJade".split(" "), "Large_Pohayoh 6000000000000.0 2 +{%_Summoning_EXP Aye_lad_if_thah_ain't_tha_larjes'_fookin'_poh'ay'oh_eyev_evah_seen_wih_me_own_eyes! zSummonExp".split(" "), "Bill_Jack_Pepper 35000000000000.0 5 +{%_Crop_Evolution_Chance It's_Him. zCropEvo".split(" "), "Burned_Marshmallow 90000000000000.0 40 +{%_Meal_Cooking_Speed IMPORTANT,_this_bonus_DOUBLES_at_Farming_Lv_50._Triples_at_Farming_Lv_100,_and_so_on! zMealFarm".split(" "), "Yumi_Peachring 800000000000000.0 2 +{%_All_Golden_Food_bonus Don't_disrespect_the_ring._All_hail_the_ring. zGoldFood".split(" "), "Plumpcakes 6000000000000000.0 6 +{%_Total_Damage Ohhh,_they're_called_'plump'cakes_because_they're_dummy_thicc_can_I_get_an_amen! TotDmg".split(" "), "Nyanborgir 50000000000000000.0 9 +{%_Crop_Evolution_Chance It's_the_greatest_meal_ever!_Bonus_DOUBLES_at_Summoning_Lv_50,_Triples_at_100,_etc zCropEvoSumm".split(" "), "Tempura_Shrimp 25000000000000000000000000000000000000000000.0 0.07 +{%_Spelunking_EXP Ah_yes,_the_Chicken_Wings_of_the_sea..._Shrimply_delicious. SplkExp".split(" "), "Woahtermelon 5000000000000000000000000000000000000000000000000.0 0.03 +{%_cheaper_Spelunking_Upgrades IMPORTANT,_this_bonus_DOUBLES_once_your_first_character_reaches_Lv_50_Spelunking! SplkUpg".split(" "), "Cookies 888880000000000000000000000000000000000000000000000000.0 0.30 +{%_Total_Spelunking_POW They're_pipin'_hot,_fresh_outta_the_oven..._wait,_what_oven? SplkPOW".split(" "), "Singing_Seed 100000000000000000000000000000000000000000000000000000000000.0 0.20 +{%_Amber_gain_from_Spelunking You're_asking_me_will_my_love_grow?_Pistachioooooh_ohhh,_Pishaaaaaaachio!!! SplkAmb".split(" ")]
cooking_meal_dict = {
    index: {
        'Name': name.replace('_', ' '),
        'BaseCost': parse_number(basecost),
        'BaseValue': parse_number(basevalue),
        'Effect': effect.replace('_', ' '),
        'Description': description.replace('_', ' '),
        'Image': f"{kebab(name.replace('_', ' '))}-meal"
    }
    for index, (name, basecost, basevalue, effect, description, _) in enumerate(MealINFO)
}
max_meal_count = len(cooking_meal_dict)

#`RiftStuff = function ()` [1] in source. Last updated in v2.46 Nov 29
rift_rewards_dict = {
    5: {'Name': 'Trap Box Vacuum', 'Shorthand': "TrapBoxVacuum"},
    10: {'Name': 'Infinite Stars', 'Shorthand': "InfiniteStars"},
    15: {'Name': 'Skill Mastery', 'Shorthand': "SkillMastery"},
    20: {'Name': 'Eclipse Skulls', 'Shorthand': "EclipseSkulls"},
    25: {'Name': 'Stamp Mastery', 'Shorthand': "StampMastery"},
    30: {'Name': 'Eldritch Artifact', 'Shorthand': "EldritchArtifacts"},
    35: {'Name': 'Vial Mastery', 'Shorthand': "VialMastery"},
    40: {'Name': 'Construct Mastery', 'Shorthand': "ConstructionMastery"},
    45: {'Name': 'Ruby Cards', 'Shorthand': "RubyCards"},
    50: {'Name': 'Killroy Prime', 'Shorthand': "KillroyPrime"},
    55: {'Name': 'Sneaking Mastery', 'Shorthand': "SneakingMastery"},
}

#`ChipDesc = function ()` in source. Last updated in v2.47 Nov 29
ChipDesc = ["Grounded_Nanochip +{%_Total_Defence Boosts_total_defence Copper 20000 Meal0 100 Spice0 100 0 def 10".split(" "), "Grounded_Motherboard +{%_Move_Speed_if_total_is_less_than_170% Boosts_total_movement_speed OakTree 30000 Meal1 100 Spice0 100 0 move 30".split(" "), "Grounded_Software +{%_Total_Accuracy Boosts_total_accuracy Fish1 20000 Meal3 100 Spice1 100 0 acc 10".split(" "), "Grounded_Processor +{%_Drop_Rate_if_total_is_less_than_5.00x Boosts_total_drop_rate DesertA1 10000 Meal4 100 Spice1 100 0 dr 60".split(" "), "Potato_Chip +{%_Basic_Attack_spd._*Can_Only_Equip_1_per_player* Boosts_attack_speed Bug1 20000 Meal6 100 Spice2 100 1 atkspd 20".split(" "), "Conductive_Nanochip +{%_Lab_EXP_Gain Boosts_lab_exp_gain StumpTree 100000 Meal9 100 Spice3 100 0 labexp 30".split(" "), "Conductive_Motherboard +{%_Line_Width_within_Mainframe Boosts_mainframe_line_width Gold 100000 Meal12 100 Spice4 100 0 linewidth 12".split(" "), "Conductive_Software +{%_Fighting_AFK_Gain_Rate_*Can_Only_Equip_1_per_player* Boosts_Fighting_AFK_gain_rate Critter2 10000 Meal15 100 Spice4 100 1 fafk 15".split(" "), "Conductive_Processor +{%_Skilling_AFK_Gain_Rate_*Can_Only_Equip_1_per_player* Boosts_Skilling_AFK_gain_Rate Bug5 100000 Meal18 100 Spice5 100 1 safk 15".split(" "), "Chocolatey_Chip {%_chance_to_spawn_a_crystal_mob_when_one_dies._*Can_Only_Equip_1_per_player* Chance_for_Crystal_Mob_revival CraftMat8 200000 Meal21 100 Spice6 100 1 crys 75".split(" "), "Galvanic_Nanochip +{%_Monster_Respawn_Rate Boosts_Mob_respawn_rate SnowC1 100000 Meal24 100 Spice7 100 0 resp 10".split(" "), "Galvanic_Motherboard +{%_Total_Skilling_Efficiency_for_all_skills Boosts_skilling_efficiency Fish5 250000 Meal27 100 Spice8 100 0 toteff 20".split(" "), "Galvanic_Software +{%_Total_Damage Boosts_total_damage Dementia 300000 Meal29 100 Spice9 100 0 dmg 10".split(" "), "Galvanic_Processor +{_Base_Efficiency_for_all_skills Boosts_base_skilling_efficiency GalaxyB2 100000 Meal31 100 Spice10 100 0 eff 250".split(" "), "Wood_Chip +{%_Multikill_per_Damage_Tier_for_all_worlds Boosts_multikill Tree8 250000 Meal33 100 Spice11 100 0 mkill 15".split(" "), "Silkrode_Nanochip Doubles_the_bonuses_of_all_active_Star_Signs._*Can_Only_Equip_1_per_player* Bolsters_active_star_signs CraftMat10 2000000 Meal35 100 Spice12 100 1 star 1".split(" "), "Silkrode_Motherboard Doubles_MISC_bonuses_of_currently_equipped_Trophy._*Can_Only_Equip_1_per_player* Bolsters_equipped_trophy Soul5 2000000 Meal37 100 Spice13 100 1 troph 1".split(" "), "Silkrode_Software Doubles_MISC_bonuses_of_keychain_equipped_in_the_upper_keychain_slot._*Can_Only_Equip_1_per_player* Bolsters_equipped_keychain Bug8 2000000 Meal39 100 Spice13 100 1 key1 1".split(" "), "Silkrode_Processor Doubles_MISC_bonuses_of_currently_equipped_Pendant._*Can_Only_Equip_1_per_player* Bolsters_equipped_pendant Critter10 2000000 Meal41 100 Spice14 100 1 pend 1".split(" "), "Poker_Chip Your_weapon_gives_1.{x_more_Weapon_Power._*Can_Only_Equip_1_per_player* Bolsters_equipped_Weapon CraftMat14 2000000 Meal43 100 Spice14 100 1 weppow 25".split(" "), "Omega_Nanochip Doubles_bonus_of_card_equipped_in_top_left_slot._*Can_Only_Equip_1_per_player* Bolsters_an_equipped_card Bug8 10000000 Meal45 100 Spice15 100 1 card1 1".split(" "), "Omega_Motherboard Doubles_bonus_of_card_equipped_in_bottom_right_slot._*Can_Only_Equip_1_per_player* Bolsters_an_equipped_card Fish8 10000000 Meal47 100 Spice16 100 1 card2 1".split(" ")]
lab_chips_dict = {
    index: {
        'Name': name.replace('_', ' ').title(),
        'Description': description.replace('_', ' '),
        'Effect': effect.replace('_', ' '),
        'BaseValue': parse_number(basevalue)
    }
    for index, (name, effect, description, _, _, _, _, _, _, _, _, basevalue) in enumerate(ChipDesc)
}

#`LabMainBonus = function ()` in source. Last updated in v2.47 Nov 29
LabMainBonus = ["0 91 353 90 0 1 Animal_Farm +1%_Total_Damage_for_every_different_species_you_have_bred_within_Pet_Breeding._You_just_need_to_breed_the_pet_type_one_time_for_it_to_count!_@_-_@_Total_Bonus:_{%".split(" "), "1 250 310 90 1 2 Wired_In All_Uploaded_Players_print_2x_more_resources_from_their_section_of_the_3D_Printer._The_displayed_amount_will_NOT_appear_doubled,_just_to_avoid_confusion_as_to_what_your_actual_base_Sampling_Rate_is,_but_it_will_be_displayed_in_blue.".split(" "), "2 356 147 90 1 3 Gilded_Cyclical_Tubing All_refinery_cycles_occur_3x_faster._Faster_cycles_means_more_salts!".split(" "), "3 450 220 90 0 1 No_Bubble_Left_Behind Every_24_hours,_your_3_lowest_level_Alchemy_Bubbles_gets_+1_Lv._This_only_applies_to_bubbles_Lv_5_or_higher,_so_it's_more_like_'your_lowest_level_bubble_that_is_at_least_level_5'._ALSO,_it_only_works_on_the_first_15_bubbles_of_each_colour!_@_Doesn't_trigger_on_days_that_you_don't_login.".split(" "), "4 538 362 90 1 2 Killer's_Brightside All_monster_kills_count_for_2x_more_than_normal_for_things_like_opening_portals_and_Death_Note._Doesn't_increase_resource_drops_or_exp_gain.".split(" "), "5 651 200 90 0 1 Shrine_World_Tour If_a_shrine_is_placed_within_town,_instead_of_in_a_monster_map,_it_will_act_as_though_it_is_placed_in_EVERY_map_in_that_entire_world!".split(" "), "6 753 113 90 1 5 Viaduct_of_the_Gods All_alchemy_liquids_have_x5_higher_max_capacity._However,_you_regenerate_alchemy_liquids_-30%_slower.".split(" "), "7 824 377 90 1 2 Certified_Stamp_Book All_Stamps,_except_for_MISC_tab_stamps,_give_DOUBLE_the_bonus.".split(" "), "8 945 326 90 1 1.5 Spelunker_Obol 1.50x_higher_effects_from_all_active_Jewels_within_the_Mainframe,_and_gives_you_+50%_rememberance_of_the_game_Idle_Skilling._@_This_bonus_always_has_a_80px_connection_range_no_matter_what!".split(" "), "9 990 148 90 0 2 Fungi_Finger_Pocketer +2%_extra_cash_from_monsters_for_every_1_million_Green_Mushroom_kills_your_account_has,_which_can_be_viewed_at_Death_Note._@_-_@_Total_Bonus:_{%".split(" "), "10 1177 163 90 1 2 My_1st_Chemistry_Set All_Vials_in_Alchemy_give_DOUBLE_the_bonus._The_bonus_description_will_reflect_this_doubling.".split(" "), "11 1300 380 90 0 2 Unadulterated_Banking_Fury +2%_Total_Damage_for_each_'green_stack'_of_resources_in_your_bank._A_'green_stack'_is_a_stack_in_your_Storage_Chest_with_10_million_or_more_items,_since_the_number_turns_Green_after_10M!_@_-_@_Total_Bonus:_{%".split(" "), "12 400 390 90 0 1 Sigils_of_Olden_Alchemy Allows_you_to_level_up_Alchemy_Sigils_by_assigning_players_in_alchemy,_at_a_base_rate_of_1_sigil_xp_per_hour._@_Sigils_can_be_leveled_up_just_twice:_Once_to_unlock_their_bonus,_and_once_more_to_boost_their_bonus._Their_bonuses_are_passive,_and_apply_to_all_characters_always.".split(" "), "13 1430 265 90 0 50 Viral_Connection All_mainframe_bonuses_and_jewels_have_a_50%_larger_connection_range,_unless_it_states_otherwise._@_This_bonus_always_has_a_80px_connection_range_no_matter_what!".split(" ")]
lab_bonuses_dict = {
    index: {
        'Name': name.replace('_', ' '),
        'Description': description.replace('_', ' '),
        'BaseValue': parse_number(basevalue),
        'YCoord': parse_number(ycoord),
        'XCoord': parse_number(xcoord),
    }
    for index, (_, xcoord, _, ycoord, _, basevalue, name, description) in enumerate(LabMainBonus)
}
#Several additional lab bonuses unlocked through the Jade Emporium are tucked away in NinjaInfo
NinjaInfo_lab_bonuses = NinjaInfo[25:29]
for index, (_, xcoord, _, ycoord, _, basevalue, name, description) in enumerate(NinjaInfo_lab_bonuses):
    lab_bonuses_dict[len(LabMainBonus) + index + 1] = {
        'Name': name.replace('_', ' '),
        'Description': description.replace('_', ' '),
        'BaseValue': parse_number(basevalue),
        'YCoord': parse_number(ycoord),
        'XCoord': parse_number(xcoord),
    }

#`JewelDesc = function ()` in source. Last updated in v2.47 Nov 29
JewelDesc = ["76 134 90 Meal_cooking_is_}x_faster._This_bonus_is_applied_TWICE_if_all_3_purple_jewels_are_active. Boosts_Meal_Cooking_speed Quest66 5 Meal1 2000 Spice0 200 Amethyst_Rhinestone 1.5".split(" "), "164 412 90 'Animal_Farm'_mainframe_bonus_gives_an_additional_+}%_per_species._If_Animal_Farm_is_not_active,_then_this_does_nothing. Bolsters_'Animal_Farm' Quest35 5 Meal3 2000 Spice1 200 Purple_Navette 0.5".split(" "), "163 218 90 All_players_get_+}%_Lab_EXP_gain. Boosts_Lab_EXP_gain Timecandy1 10 Meal5 2000 Spice2 200 Purple_Rhombol 40".split(" "), "246 110 90 Construction_slot_1_is_now_trimmed_up,_and_has_}x_building_Speed._Also_trims_slot_2_if_all_4_blue_jewels_are_active. Trims_up_a_construction_slot Quest15 10 Meal7 5000 Spice3 400 Sapphire_Rhinestone 3".split(" "), "277 394 90 All_players_get_+}%_All_Stat._STR,_AGI,_WIS,_and_LUCK_to_boot. Boosts_all_stats TreeInterior1b 25 Meal9 5000 Spice4 400 Sapphire_Navette 3".split(" "), "470 294 90 Even_if_this_jewel_is_off,_all_players_within_a_150px_radius_of_this_jewel,_shown_by_the_circle,_have_+25%_Line_Width._@_Also_gives_+}%_Breeding_EXP,_but_only_when_active. Emits_a_'Line_Width'_Aura Sewers1b 30 Meal11 5000 Spice5 400 Sapphire_Rhombol 25".split(" "), "490 112 90 Every_24_hours,_the_}_lowest_level_Kitchen_Upgrades_across_all_owned_kitchens_gain_+1_Lv. Automatically_levels_up_kitchens Quest38 2 Meal13 5000 Spice6 400 Sapphire_Pyramite 2".split(" "), "552 163 90 'No_Bubble_Left_Behind'_mainframe_bonus_gives_+}_levels_instead_of_+1,_and_does_so_for_the_lowest_4_bubbles_instead_of_3. Bolsters_'No_Bubble_Left_Behind' DesertA1b 50 Meal15 10000 Spice7 1500 Pyrite_Rhinestone 2".split(" "), "646 407 90 All_players_get_}x_'non-consume'_chance,_and_raises_the_max_chance_from_90%_to_98%,_allowing_for_longer_AFK_with_food. Boosts_'non-consume'_chance EquipmentPants19 2 Meal17 10000 Spice8 1500 Pyrite_Navette 3".split(" "), "680 319 90 All_mainframe_bonuses_and_jewels_have_a_}%_larger_connection_range,_except_for_this_jewel._This_jewel_has_an_80px_connection_range_no_matter_what! Boosts_mainframe_connection_range DesertA3b 50 Meal19 10000 Spice9 1500 Pyrite_Rhombol 30".split(" "), "847 105 90 All_players_deal_1.}x_more_damage._This_bonus_is_applied_TWICE_if_all_4_Orange_Jewels_are_active. Boosts_player_damage DesertC2b 50 Meal21 10000 Spice10 1500 Pyrite_Pyramite 10".split(" "), "998 404 90 }%_reduced_incubation_egg_time._Mo_eggs_mo_problems_tho,_fo_sho. Reduces_egg_incubation_time BabaYagaETC 1 Meal23 25000 Spice11 5000 Emerald_Rhinestone 28".split(" "), "1079 233 90 All_players_have_}_higher_base_efficiency_in_all_skills,_and_+10%_skill_action_speed._This_bonus_is_applied_TWICE_if_all_5_Green_Jewels_are_active. Boosts_player_efficiency SnowA2a 80 Meal25 25000 Spice12 5000 Emerald_Navette 200".split(" "), "1085 121 90 'Fungi_Finger_Pocketer'_mainframe_bonus_gives_an_additional_+}%_cash_bonus_per_million_mushroom_kills Bolsters_'Fungi_Finger_Pocketer' SnowB2a 120 Meal27 25000 Spice13 5000 Emerald_Rhombol 1".split(" "), "1167 390 90 Meal_cooking_is_}%_faster_for_every_25_total_upgrade_levels_across_all_kitchens._@_Total_Bonus:_{%_speed Boosts_Meal_Cooking_speed SnowC4a 150 Meal29 25000 Spice14 5000 Emerald_Pyramite 1".split(" "), "1300 208 90 Special_Pets_in_the_Fenceyard_level_up_their_Passive_Bonuses_+}%_faster Boosts_Pet_Passive_level_up_rate GalaxyA2b 200 Meal31 25000 Spice15 5000 Emerald_Ulthurite 30".split(" "), "1365 100 90 All_meals_now_give_a_1.}x_higher_bonus!_Go_ahead_and_check_it_out_at_the_Dinner_Menu!_@_Doesn't_apply_to_the_meal_that_gives_Line_Width_bonus. Bolsters_meals GalaxyC1b 300 Meal33 100000 Spice15 10000 Black_Diamond_Rhinestone 16".split(" "), "1389 408 90 'Unadulterated_Banking_Fury'_gives_an_additional_+}%_Total_Damage_per_greened_stack. Bolsters_'Unadulterated_Banking_Fury' Critter10A 10000 Meal35 100000 Spice16 10000 Black_Diamond_Ulthurite 1".split(" "), "1619 203 90 'Slab_Sovereignty'_gives_an_additional_}%_boost_to_all_Slab_Bonuses! Bolsters_'Slab_Sovereignty' SpiA1 3000000 Meal53 1000000 Spice20 10000 Pure_Opal_Rhinestone 20".split(" "), "1846 410 80 +}%_higher_effects_from_all_active_bonuses_and_jewels_within_the_Mainframe,_except_for_Spelunker_Obol._@_This_is_a_multiplier,_so_+10%_would_be_1.10x,_ya_feel_me?_@_This_bonus_always_has_a_80px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Pure_Opal_Navette 10".split(" "), "2040 96 90 'Depot_Studies_PhD'_gives_an_additional_}%_boost_to_all_Crop_Depot_bonuses! Bolsters_'Depot_Studies_PhD' Critter11A 5000 Meal62 100000000 Spice22 10000 Pure_Opal_Rhombol 10".split(" "), "1815 96 100 +}%_extra_Deathbringer_Bones._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Deadly_Wrath_Jewel 50".split(" "), "1728 421 100 +}%_extra_Windwalker_Dust._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 North_Winds_Jewel 50".split(" "), "2042 410 100 +}%_extra_Arcane_Cultist_Tachyons._@_This_bonus_always_has_a_100px_connection_range_no_matter_what! Boosts_entire_Lab SpiB2b 1000 Meal58 10000000 Spice21 10000 Eternal_Energy_Jewel 50".split(" ")]
lab_jewels_dict = {
    index: {
        'Name': data[11].replace('_', ' '),
        'Description': data[3].replace('_', ' '),
        'BaseValue': parse_number(data[12])
    }
    for index, data in enumerate(JewelDesc)
}

max_nblb_bubbles = 10  # Last updated in v2.46 Nov 29
max_breeding_territories = 25  # Last updated in v2.46 Nov 29
breeding_last_arena_bonus_unlock_wave = 200
index_first_territory_assigned_pet = 28
slot_unlock_waves_list = [2, 15, 50, 125]
territory_names = [
    "", "Grasslands", "Jungle", "Encroaching Forest", "Tree Interior", "Stinky Sewers",
    "Desert Oasis", "Beach Docks", "Coarse Mountains", "Twilight Desert", "The Crypt",
    "Frosty Peaks", "Tundra Outback", "Crystal Caverns", "Pristalle Lake",
    "Nebulon Mantle", "Starfield Skies", "Shores of Eternity",
    "Molten Bay", "Smokey Lake", "Wurm Catacombs",
    "Spirit Fields", "Bamboo Forest", "Lullaby Airways", "Dharma Mesa",
    'The Doodling School',
]
#`PetUpgradeINFO = function ()` in source. Last updated in v2.46 Nov 30
PetUpgradeINFO = ["No_Upgrade_Selected Filler PetDeadCell Blank 6 1.08 0 1.15 100 TAP_AN_UPGRADE_ABOVE!_Also,_as_a_reward_for_reading_this,_I'll_let_you_know_that_upgrading_this_'nothing'_bonus_actually_boosts_breeding_exp_gain_1%_per_LV_lmao _ 0".split(" "), "Gene_Splicing_}_Helps_unlock_next_pet_type Filler PetDeadCell 0 6 1.1 3 2.5 20 Unlocks_Gene_Boosting,_which_increases_chance_to_breed_new_pets._Use_the_DNA_Splicer_tool_from_the_Town_Shop_to_get_Genes. -}%_Gene_Boost_Cost 4".split(" "), "Egg_Capacity Filler PetDeadCell 3 20 1.5 10 100 5 Increases_the_maximum_number_of_eggs_your_incubator_can_hold._The_more_eggs_you_currently_hold,_the_rarer_it_is_to_get_a_new_one. +}_Egg_Max 1".split(" "), "Breedability_Pets Filler PetDeadCell 6 5 1.25 10 7 10 Unlocks_Breedability,_which_increases_chance_to_breed_new_pets._Put_a_'pink'_pets_in_the_Fenceyard_to_increase_their_multiplier. +}%_Breedability_Spd 25".split(" "), "Fence_Extension Filler PetDeadCell 11 30 1.16 10 4 10 Increases_the_number_of_slots_in_your_Fence_Yard,_allowing_for_more_pets_to_roam_around,_free_range_style! +}_Fenceyard_Slots 1".split(" "), "Rarity_of_the_Egg Filler PetDeadCell 14 35 1.25 10 9 10 Unlocks_the_3rd_Multi,_Egg_Rarity._When_the_egg_incubator_is_full,_theres_a_chance_to_increase_the_rarity_of_another_egg! }x_Chance 1".split(" "), "Blooming_Axe Filler PetDeadCell 20 40 1.25 10 10 10 All_pets_do_more_damage_in_battle! +}%_Pet_Damage 6".split(" "), "Pastpresent_Brood Filler PetDeadCell 25 45 1.6 10 130 5 Unlocks_the_4th_Breeding_Multi,_Pastpres._This_increases_based_on_the_number_of_different_pets_discovered_from_the_previous_world. }x_Bigger_Multi 0.15".split(" "), "Paint_Bucket Filler PetDeadCell 30 50 1.05 10 1.35 100 Unlocks_Shiny_Pet_Breeding._Shiny_Pets_come_in_1_of_5_colours,_and_boost_their_Special_Passive_bonus_when_in_the_Fenceyard. +}%_Base_Shiny_Chance 2".split(" "), "Overwhelmed_Golden_Egg Filler PetDeadCell 35 55 1.6 10 5 20 Your_New_Pet_Chance_is_multiplied_for_every_100_kitchen_upgrade_levels_across_all_kitchens!_So_200_Lvs_would_apply_it_twice!! }x_Multiplier_every_100_Upg 0.02".split(" "), "Failsafe_Restitution_Cloud Filler PetDeadCell 40 60 1.08 10 3.88 25 Unlocks_the_5th_Breeding_Multiplier,_Failure._This_increases_every_time_you_fail_to_get_a_new/shiny_pet,_up_to_a_max,_and_depletes_when_you_succeed. }_Maximum_Times 10".split(" "), "Shattershell_Iteration Filler PetDeadCell 45 65 1.25 10 34 10 Every_time_you_use_up_your_last_incubator_egg,_there_is_a_chance_to_produce_2_more_eggs_immediately. }%_Chance 8".split(" "), "Grand_Martial_of_Shinytown Filler PetDeadCell 62 3 1.01 1000 2.85 300 Boosts_the_rate_at_which_shiny_pets_level_up_from_being_in_the_fenceyard._This_will_help_you_rack_up_those_100+_Day_requirements! +}%_Shiny_Pet_LV_Up_Rate 5".split(" ")]
#Need to find where these levels are established in source.
breeding_upgrade_unlock_levels = [1, 1, 5, 10, 15, 20, 25, 30, 40, 50, 60, 70, 80]
breeding_upgrades_dict = {
    index: {
        'Name': name.replace('_', ' '),
        'BonusText': bonustext.replace('_', ' '),
        'BonusValue': parse_number(bonusvalue),
        'MaxLevel': parse_number(maxlevel),
        'UnlockLevel': breeding_upgrade_unlock_levels[index]
    }
    for index, (name, _, _, _, _, _, _, _, maxlevel, bonustext, _, bonusvalue) in enumerate(PetUpgradeINFO)
}
breeding_genetics_list: list[str] = [
    "Fighter", "Defender", "Forager", "Fleeter", "Breeder", "Special", "Mercenary", "Boomer",
    "Sniper", "Amplifier", "Tsar", "Rattler", "Cursory", "Fastidious", "Flashy", "Opticular",
    "Monolithic", "Alchemic", "Badumdum", "Defstone", "Targeter", "Looter", "Refiller", "Eggshell",
    "Lazarus", "Trasher", "Miasma", "Converter", "Heavyweight", "Fastihoop", "Ninja",
    "Superboomer", "Peapeapod", "Borger"
]
breeding_shiny_bonus_list: list[str] = [
    "Faster Shiny Pet Lv Up Rate",  #0
    "Infinite Star Signs",
    "Total Damage",  #2
    "Drop Rate",
    "Base Efficiency for All Skills",  #4
    "Base WIS",
    "Base STR",  #6
    "Base AGI",
    "Base LUK",  #8
    "Class EXP",
    "Skill EXP",  #10
    "Tab 1 Talent Pts",
    "Tab 2 Talent Pts",  #12
    "Tab 3 Talent Pts",
    "Tab 4 Talent Pts",  #14
    "Star Talent Pts",
    "Faster Refinery Speed",  #16
    "Base Critter Per Trap",
    "Multikill Per Tier",  #18
    "Bonuses from All Meals",
    "Line Width in Lab",  #20
    "Higher Artifact Find Chance",
    "Sail Captain EXP Gain",  #22
    "Lower Minimum Travel Time for Sailing",
    "Farming EXP",  #24
    "Summoning EXP"
]
breeding_species_dict: dict[int, dict] = {
    #Built using references to Genetics and ShinyBonus lists because I kept making typos + Wiki isn't consistent to copy/paste from
    1: {
        0: {
            'Name': 'Green Mushroom',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate,
        },
        1: {
            'Name': 'Squirrel',
            'Genetic': breeding_genetics_list[2],  #Forager
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        2: {
            'Name': 'Frog',
            'Genetic': breeding_genetics_list[7],  #Boomer
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        3: {
            'Name': 'Bored Bean',
            'Genetic': breeding_genetics_list[3],  #Fleeter
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Red Mushroom',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[19],  #Bonuses from All Meals
        },
        5: {
            'Name': 'Slime',
            'Genetic': breeding_genetics_list[12],  #Cursory
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        6: {
            'Name': 'Piggo',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        7: {
            'Name': 'Baby Boa',
            'Genetic': breeding_genetics_list[20],  #Targeter
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        8: {
            'Name': 'Carrotman',
            'Genetic': breeding_genetics_list[6],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        9: {
            'Name': 'Glublin',
            'Genetic': breeding_genetics_list[22],  #Refiller
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        10: {
            'Name': 'Wode Board',
            'Genetic': breeding_genetics_list[26],  #Miasma
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        11: {
            'Name': 'Gigafrog',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Wild Boar',
            'Genetic': breeding_genetics_list[28],  #Heavyweight
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        13: {
            'Name': 'Walking Stick',
            'Genetic': breeding_genetics_list[22],  #Refiller
            'ShinyBonus': breeding_shiny_bonus_list[17],  #Base Critter Per Trap
        },
        14: {
            'Name': 'Nutto',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        15: {
            'Name': 'Poop',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        16: {
            'Name': 'Rat',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
    },
    2: {
        0: {
            'Name': 'Sandy Pot',
            'Genetic': breeding_genetics_list[21],  #Looter
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        1: {
            'Name': 'Mimic',
            'Genetic': breeding_genetics_list[1],  #Defender
            'ShinyBonus': breeding_shiny_bonus_list[11],  #Tab 1 Talent Pts
        },
        2: {
            'Name': 'Crabcake',
            'Genetic': breeding_genetics_list[3],  #Fleeter
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        3: {
            'Name': 'Mafioso',
            'Genetic': breeding_genetics_list[2],  #Forager
            'ShinyBonus': breeding_shiny_bonus_list[12],  #Tab 2 Talent Pts
        },
        4: {
            'Name': 'Mallay',
            'Genetic': breeding_genetics_list[15],  #Opticular
            'ShinyBonus': breeding_shiny_bonus_list[20],  #Line Width in Lab
        },
        5: {
            'Name': 'Sand Castle',
            'Genetic': breeding_genetics_list[19],  #Defstone
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        6: {
            'Name': 'Pincermin',
            'Genetic': breeding_genetics_list[0],  #Fighter
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        7: {
            'Name': 'Mashed Potato',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        8: {
            'Name': 'Tyson',
            'Genetic': breeding_genetics_list[13],  #Fastidious
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        9: {
            'Name': 'Whale',
            'Genetic': breeding_genetics_list[18],  #Badumdum
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        10: {
            'Name': 'Moonmoon',
            'Genetic': breeding_genetics_list[7],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[5],  #Base WIS
        },
        11: {
            'Name': 'Sand Giant',
            'Genetic': breeding_genetics_list[11],  #Rattler
            'ShinyBonus': breeding_shiny_bonus_list[4],  #Base Efficiency for All Skills
        },
        12: {
            'Name': 'Snelbie',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[14],  #Tab 4 Talent Pts
        },
        13: {
            'Name': 'Dig Doug',
            'Genetic': breeding_genetics_list[24],  #Lazarus
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        14: {
            'Name': 'Beefie',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
        15: {
            'Name': 'Crescent Spud',
            'Genetic': breeding_genetics_list[16],  #Monolithic
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        16: {
            'Name': 'Chippy',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[25],  #Summoning EXP
        },
    },
    3: {
        0: {
            'Name': 'Sheepie',
            'Genetic': breeding_genetics_list[8],  #Sniper
            'ShinyBonus': breeding_shiny_bonus_list[19],  #Bonuses from All Meals
        },
        1: {
            'Name': 'Frost Flake',
            'Genetic': breeding_genetics_list[30],  #Ninja
            'ShinyBonus': breeding_shiny_bonus_list[13],  #Tab 3 Talent Pts
        },
        2: {
            'Name': 'Sir Stache',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        3: {
            'Name': 'Xylobone',
            'Genetic': breeding_genetics_list[15],  #Opticular
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        4: {
            'Name': 'Bunny',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
        5: {
            'Name': 'Bloque',
            'Genetic': breeding_genetics_list[17],  #Alchemic
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        6: {
            'Name': 'Mamooth',
            'Genetic': breeding_genetics_list[21],  #Looter
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        7: {
            'Name': 'Snowman',
            'Genetic': breeding_genetics_list[19],  #Defstone
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        8: {
            'Name': 'Penguin',
            'Genetic': breeding_genetics_list[13],  #Fastidious
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        9: {
            'Name': 'Thermister',
            'Genetic': breeding_genetics_list[8],  #Sniper
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        10: {
            'Name': 'Quenchie',
            'Genetic': breeding_genetics_list[7],  #Boomer
            'ShinyBonus': breeding_shiny_bonus_list[0],  #Faster Shiny Pet Lv Up Rate
        },
        11: {
            'Name': 'Cryosnake',
            'Genetic': breeding_genetics_list[23],  #Eggshell
            'ShinyBonus': breeding_shiny_bonus_list[15],  #Star Talent Pts
        },
        12: {
            'Name': 'Mecho Mouse',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        13: {
            'Name': 'Bop Box',
            'Genetic': breeding_genetics_list[27],  #Converter
            'ShinyBonus': breeding_shiny_bonus_list[1],  #Infinite Star Signs
        },
        14: {
            'Name': 'Neyeptune',
            'Genetic': breeding_genetics_list[24],  #Lazarus
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        15: {
            'Name': 'Dedotated Ram',
            'Genetic': breeding_genetics_list[9],  #Amplifier
            'ShinyBonus': breeding_shiny_bonus_list[18],  #Multikill Per Tier
        },
        16: {
            'Name': 'Bloodbone',
            'Genetic': breeding_genetics_list[20],  #Targeter
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        17: {
            'Name': 'Panda',
            'Genetic': breeding_genetics_list[27],  #Converter
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
    },
    4: {
        0: {
            'Name': 'Purp Mushroom',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[24],  #Farming EXP
        },
        1: {
            'Name': 'TV',
            'Genetic': breeding_genetics_list[11],  #Rattler
            'ShinyBonus': breeding_shiny_bonus_list[22],  #Sail Captain EXP Gain
        },
        2: {
            'Name': 'Donut',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[25],  #Summoning EXP
        },
        3: {
            'Name': 'Demon Genie',
            'Genetic': breeding_genetics_list[31],  #Superboomer
            'ShinyBonus': breeding_shiny_bonus_list[16],  #Faster Refinery Speed
        },
        4: {
            'Name': 'Flying Worm',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        5: {
            'Name': 'Dog',
            'Genetic': breeding_genetics_list[32],  #Peapeapod
            'ShinyBonus': breeding_shiny_bonus_list[23],  #Lower Minimum Travel Time for Sailing
        },
        6: {
            'Name': 'Soda Can',
            'Genetic': breeding_genetics_list[29],  #Fastihoop
            'ShinyBonus': breeding_shiny_bonus_list[21],  #Higher Artifact Find Chance
        },
        7: {
            'Name': 'Gelatinous Cuboid',
            'Genetic': breeding_genetics_list[14],  #Flashy
            'ShinyBonus': breeding_shiny_bonus_list[2],  #Total Damage
        },
        8: {
            'Name': 'Choccie',
            'Genetic': breeding_genetics_list[31],  #Superboomer
            'ShinyBonus': breeding_shiny_bonus_list[3],  #Drop Rate
        },
        9: {
            'Name': 'Biggole Wurm',
            'Genetic': breeding_genetics_list[10],  #Tsar
            'ShinyBonus': breeding_shiny_bonus_list[9],  #Class EXP
        },
        10: {
            'Name': 'Cool Bird',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[6],  #Base STR
        },
        11: {
            'Name': 'Clammie',
            'Genetic': breeding_genetics_list[6],  #Mercenary
            'ShinyBonus': breeding_shiny_bonus_list[10],  #Skill EXP
        },
        12: {
            'Name': 'Octodar',
            'Genetic': breeding_genetics_list[12],  #Cursory
            'ShinyBonus': breeding_shiny_bonus_list[17],  #Base Critter Per Trap
        },
        13: {
            'Name': 'Flombeige',
            'Genetic': breeding_genetics_list[25],  #Trasher
            'ShinyBonus': breeding_shiny_bonus_list[7],  #Base AGI
        },
        14: {
            'Name': 'Stilted Seeker',
            'Genetic': breeding_genetics_list[33],  #Borger
            'ShinyBonus': breeding_shiny_bonus_list[5],  #Base WIS
        },
        15: {
            'Name': 'Hedgehog',
            'Genetic': breeding_genetics_list[32],  #Peapeapod
            'ShinyBonus': breeding_shiny_bonus_list[8],  #Base LUK
        },
    },
}
breeding_total_pets = sum([len(petValues) for worldIndex, petValues in breeding_species_dict.items()])
shiny_days_list = [
    0, 3, 11, 33, 85,
    200, 448, 964, 2013, 4107,
    8227, 16234, 31633, 60989, 116522,
    220874, 415802, 778022, 1447955, 2681786,
]


def getShinyLevelFromDays(days: float) -> int:
    shinyLevel = 0
    for requirement in shiny_days_list:
        if float(days) > requirement:
            shinyLevel += 1
        else:
            break
    return shinyLevel


def getDaysToNextShinyLevel(days: float) -> float:
    shinyLevel = getShinyLevelFromDays(days)
    if shinyLevel >= len(shiny_days_list):
        return 0
    else:
        try:
            daysRemaining = shiny_days_list[shinyLevel] - float(days)
            return daysRemaining
        except Exception as reason:
            logger.warning(f"With shinyLevel of {shinyLevel}, Defaulting Shiny days Remaining to 0. Reason: {reason}")
            return 0


breedabilityDaysList = [
    0.0000,
    2.9722,
    25.5910,
    230.7881,
    2445.8520,
    30113.1432,
    421857.0285,
    6615176.2308,
    114686626.8729,
    2177232407.5082,
]
breedabilityHearts = [1 + safer_math_pow(x, 1.25) for x in range(0, 10)]


def getBreedabilityMultiFromDays(days: float) -> float:
    if not isinstance(days, float):
        try:
            days = float(days)
        except:
            logger.warning(f"Expected days to be float type, got {type(days)}: {days}. Using 0 days instead.")
            days = 0
    result = 1 + math.log(max(1, safer_math_pow(days+1, 0.725)))
    #logger.debug(f"getBreedabilityMultiFromDays: Given {days} days, Breedability Multi = {result}")
    return result


def getBreedabilityHeartFromMulti(multi: float) -> str:
    result = 0
    for reqIndex, requirement in enumerate(breedabilityHearts):
        if multi >= requirement:
            result += 1
        else:
            break
    return f"breedability-heart-{result}"
