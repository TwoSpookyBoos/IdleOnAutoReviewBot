from collections import defaultdict
from decimal import Decimal
from consts.consts_monster_data import decode_monster_name
from utils.number_formatting import parse_number
from utils.text_formatting import kebab
from utils.logging import get_consts_logger
logger = get_consts_logger(__name__)


summoning_sanctuary_counts = [1]
for multi in range(3, 16):  #(3, 16) produces length of 14
    summoning_sanctuary_counts.append(multi * summoning_sanctuary_counts[-1])
#summoning_sanctuary_counts = [1, 3, 12, 60, 360, 2520, 20160, 181440, 1814400, 19958400, 239500800, 3113510400, 43589145600, 653837184000]
#`SummonUPG = function ()` in source. Last updated in v2.46 Nov Dec 2
summoning_upgrades = ["427 171 0 White_Essence_Champ 10 1.12 5 0 9999 -1 1 +{%_White_Essence_generated_per_hour_for_each_win_across_all_colours._@_Total_bonus:_+}%".split(" "), "374 158 0 Unit_Health 10 1.3 1 0 9999 0 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "479 145 0 Familiar 100 10 1 0 25 0 0 Summons_a_slime_familiar_to_chill_in_your_sanctuary,_generating_10_Summoning_EXP_every_hour._@_Cost_resets_in_|".split(" "), "391 113 0 Unit_Damage 20 1.35 1 0 9999 1 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "389 59 0 Green_Summoning 4000 1.2 10 0 9999 3 1 Unlocks_the_Green_Summoning_Stone,_and_begins_generating_Green_Essence._@_Also,_+{%_Green_Essence_per_hour".split(" "), "449 80 0 Mana_Generation 40 1.35 2 0 9999 3 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "536 126 0 Familiar_Merging 2500 1.2 1 0 1 9 0 3_Slime_Familiars_merge_into_a_Vrumbi_Familiar_which_gives_4x_Summoning_Exp._4_Vrumbies_then_merge_and_give_5x_exp._This_repeats_many_times.".split(" "), "499 58 0 Dodge_Roll 80 1.3 1 0 30 5 0 All_your_units_get_a_+{%_chance_to_dodge_damage_when_colliding_with_an_enemy".split(" "), "554 66 0 Multi-Number_Cards 7500 1.5 1 0 1 7 0 There's_a_chance_cards_can_played_multiple_times,_indicated_by_the_number_in_the_top-left_corner._These_cards_also_come_with_a_smaller_cost!".split(" "), "356 226 1 Vrumbi 10 7.5 5 0 10 4 0 7%_chance_to_draw_a_Vrumbi_during_competition._They_have_1.5x_SPD,_2.0x_DMG,_and_+{%_Dodge_Chance".split(" "), "301 209 1 Unit_Wellness 25 1.3 2 0 9999 9 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "306 154 1 Green_Essence_Victor 50 1.12 1 0 9999 10 1 +{%_Green_Essence_generated_per_hour_for_each_Green_circuit_win._@_Total_bonus:_+}%".split(" "), "252 137 1 Powerful_Units 70 1.35 2 0 9999 11 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "274 86 1 Yellow_Summoning 15000 1.2 10 0 9999 12 1 Unlocks_the_Yellow_Summoning_Stone,_and_begins_generating_Yellow_Essence._@_Also,_+{%_Yellow_Essence_per_hour".split(" "), "200 152 1 Mana_Overflow 4000 1.5 1 0 1 12 0 During_competition,_when_your_mana_pool_is_full,_expand_max_mana_by_1.5x_and_boost_mana_generation_by_+15%".split(" "), "215 94 1 Spiked_Placement 250 1.4 4 0 9999 12 1 When_summoning_any_unit,_deal_{_damage_to_all_enemies_within_100_pixels_of_where_you_click..._You_don't_have_to_click_in_your_spawn!".split(" "), "169 62 1 Starting_Mana_frfr 750 1.6 1 0 9999 15 1 Start_each_competition_with_+{_more_mana".split(" "), "509 201 2 Bloomy 20 25 5 0 10 13 0 4%_chance_to_draw_a_Bloomy_during_competition._They_sit_in_the_backline_and_give_+{%_Mana_Generation_while_alive.".split(" "), "566 188 2 Yellow_Essence_Winnin' 50 1.12 5 0 9999 17 1 +{%_Yellow_Essence_generated_per_hour_for_each_Yellow_circuit_win._@_Total_bonus:_+}%".split(" "), "622 159 2 Luck_of_the_Draw 130 3 2 0 10 18 0 All_special_units_are_>x_more_likely_to_be_drawn_instead_of_slime.".split(" "), "607 106 2 Unit_Constitution 250 1.3 5 0 9999 19 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{%".split(" "), "661 70 2 Stronger_Units 525 1.35 4 0 9999 20 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "714 89 2 Slime_Cellsplit 900 1.15 1 0 30 21 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "747 137 2 Blue_Summoning 50000 1.2 10 0 9999 22 1 Unlocks_the_Blue_Summoning_Stone,_and_begins_generating_Blue_Essence._@_Also,_+{%_Blue_Essence_per_hour".split(" "), "769 78 2 Re-Draw 2000 5 1 0 3 22 1 Unlocks_the_Re-Draw_button,_allowing_you_to_instantly_redraw_all_your_cards_for_a_cost..._but_you_get_the_first_{_for_free!".split(" "), "826 88 2 Another_Slot 10000 1.5 1 0 1 24 0 Adds_+1_Card_Slot,_letting_you_hold_more_cards_at_once!".split(" "), "367 295 3 Tonka 30 1.85 10 0 20 23 0 5%_chance_to_draw_a_Tonka_during_competition._They_have_0.75x_SPD,_0.75x_DMG,_and_8.0x_HP._Your_upgrades_here_boost_its_HP_by_a_further_+{%.".split(" "), "312 285 3 Blue_Essence_Ballin' 70 1.12 5 0 9999 26 1 +{%_Blue_Essence_generated_per_hour_for_each_Blue_circuit_win._@_Total_bonus:_+}%".split(" "), "258 300 3 Slime_Mitosis 200 1.5 1 0 30 27 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "207 275 3 Manaranarr 450 1.5 2 0 9999 28 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "220 224 3 Blue_Knowledge 750 1.15 1 0 9999 29 1 +{%_Blue_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "168 214 3 Beefier_Units 1500 1.35 6 0 9999 30 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{".split(" "), "117 183 3 Jeweled_Cards 6000 170 6 0 3 31 1 {%_chance_to_draw_a_Jeweled_variant_of_any_card,_which_costs_2x_Mana_but_spawns_4x_Units!".split(" "), "62 208 3 Purple_Summoning 250000 1.2 10 0 9999 32 1 Unlocks_the_Purple_Summoning_Stone,_and_begins_generating_Purple_Essence._@_Also,_+{%_Purple_Essence_per_hour".split(" "), "78 129 3 Another_Slot 15000 1.5 1 0 1 32 0 Adds_+1_Card_Slot!_Or_as_an_AI_might_say,_this_upgrade_further_substantiates_the_incremental_improvement_to_the_quantity_of_cards_you_hold_by_1".split(" "), "58 77 3 Unit_Ache_Pea 5000 1.3 9 0 9999 34 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "530 263 4 Regalis 50 1.7 1 0 30 33 0 3%_chance_to_draw_a_Regalis_during_competition._They_spawn_a_Slime_Unit_every_1_sec._Upgrading_this_boosts_slime_unit_spawn_rate_by_+{%".split(" "), "588 238 4 Unit_Hitpoints 100 1.25 13 0 9999 36 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{".split(" "), "644 228 4 Purp_Essence_Pumpin' 250 1.12 5 0 9999 37 1 +{%_Purple_Essence_generated_per_hour_for_each_Purple_circuit_win._@_Total_bonus:_+}%".split(" "), "693 256 4 Familiar_Skipping 600 1.25 1 0 100 38 0 When_summoning_a_Slime_Familiar,_there's_a_1_in_8_to_get_a_Vrumbi_instead_of_Slime,_and_1_in_50_to_get_a_Bloomy._Upgrading_this_boosts_this_chance_by_+{%".split(" "), "747 262 4 Purple_Knowledge 1000 1.15 1 0 9999 39 1 +{%_Purple_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "705 207 4 Final_Card 2000 2500 1 0 3 38 1 If_you_play_every_card_in_your_hand,_get_+{%_Mana_Regen_per_card_played._Playing_Multi-Number_cards_counts_multiple_times_for_this!".split(" "), "764 204 4 Mana_Dividends 4500 1.5 2 0 9999 41 1 During_competition,_mana_generation_is_+{%_higher_than_normal.".split(" "), "821 165 4 Brutal_Units 9000 1.25 5 0 9999 42 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{%".split(" "), "875 186 4 Red_Summoning 1000000 1.2 10 0 9999 43 1 Unlocks_the_Red_Summoning_Stone,_and_begins_generating_Red_Essence._@_Also,_+{%_Red_Essence_per_hour".split(" "), "404 353 5 Sparkie 75 1.75 5 0 30 44 0 5%_chance_to_draw_a_Sparkie_during_competition._They_have_3.0X_DMG_and_explode_on_death._Your_upgrades_here_boost_it's_DMG_by_a_further_+{%.".split(" "), "349 391 5 Red_Essence_Ragin' 200 1.15 5 0 9999 45 1 +{%_Red_Essence_generated_per_hour_for_each_Red_circuit_win._@_Total_bonus:_+}%".split(" "), "293 362 5 Seeing_Red 750 1.8 1 0 10 46 1 When_an_enemy_crosses_your_line_and_damages_you,_all_units_get_{%_DMG_for_the_rest_of_the_fight._This_stacks_every_time_an_enemy_crosses_your_line.".split(" "), "230 370 5 Slime_Duplication 2000 1.5 1 0 40 47 0 When_spawning_any_unit_during_competition,_+{%_chance_to_also_spawn_an_exact_duplicate,_free_of_charge!".split(" "), "164 377 5 Cost_Crashing 4000 1.25 1 0 9999 48 1 All_Summoning_upgrades_cost_}%_less_Essence.".split(" "), "146 322 5 Unit_Blood 8000 1.4 10 0 9999 49 1 Increases_the_HP_of_all_summoned_units_in_competition_by_a_brand_new_multiplier_of_+{%".split(" "), "100 276 5 Merciless_Units 15000 1.41 8 0 9999 50 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_a_brand_new_multiplier_of_+{%".split(" "), "48 302 5 Red_Knowledge 30000 1.52 1 0 9999 51 1 +{%_Red_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "108 391 5 Cyan_Summoning 3000000 1.21 10 0 9999 49 1 Unlocks_the_Cyan_Summoning_Stone,_and_begins_generating_Cyan_Essence._@_Also,_+{%_Cyan_Essence_per_hour".split(" "), "477 374 6 Cyan_Essence_King 150 1.15 5 0 9999 69 1 +{%_Cyan_Essence_generated_per_hour_for_each_Cyan_circuit_win._@_Total_bonus:_+}%".split(" "), "534 384 6 I_Frames 400 1.5 1 0 30 54 0 All_your_units_get_a_+{%_chance_to_dodge_damage_when_colliding_with_an_enemy".split(" "), "598 390 6 Units_of_Destruction 2000 1.43 10 0 9999 55 1 Increases_the_DMG_of_all_summoned_units_in_competition_by_+{%".split(" "), "574 322 6 Cost_Deflation 1200 1.21 2 0 9999 69 1 All_Summoning_upgrades_cost_}%_less_Essence.".split(" "), "630 339 6 Cyan_Knowledge 5000 1.55 1 0 9999 57 1 +{%_Cyan_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "683 373 6 Undying_Units 10000 1.41 14 0 9999 58 1 Increases_the_HP_of_all_summoned_units_in_competition_by_+{%".split(" "), "739 385 6 DMG_Laundering 20000 1.79 1 0 9999 59 1 Boosts_the_DMG_of_all_summoned_units_by_+{%_for_every_100_total_summoning_upgrades_purchased._@_Total_bonus:_+}%".split(" "), "795 394 6 HP_Laundering 50000 1.78 1 0 9999 60 1 Boosts_the_HP_of_all_summoned_units_by_+{%_for_every_100_total_summoning_upgrades_purchased._@_Total_bonus:_+}%".split(" "), "736 320 6 Infinite_Essence 100000 1.35 5 0 9999 70 1 The_generation_of_all_essence_colours_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "792 312 6 Infinite_Health 300000 1.38 2 0 9999 62 1 The_HP_of_all_summoned_units_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "834 266 6 Infinite_Damage 600000 1.41 2 0 9999 63 1 The_DMG_of_all_summoned_units_is_increased_by_+{%_for_every_Endless_Summoning_victory_you_have._@_Total_bonus:_+}%".split(" "), "340 76 0 White_Knowledge 1500 1.15 1 0 9999 4 1 +{%_White_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "148 109 1 Green_Knowledge 1200 1.15 1 0 9999 16 1 +{%_Green_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "678 153 2 Yellow_Knowledge 300 1.15 1 0 9999 19 1 +{%_Yellow_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "874 122 2 Sharpened_Spikes 12000 1.65 1 0 20 25 1 Spike_damage_is_increased_by_{%_of_your_base_unit_damage._@_Total_Bonus_Spike_DMG:_+}".split(" "), "514 327 6 Guardio 100 3.5 8 0 30 53 0 4%_chance_to_draw_a_Guardio!_They_sit_in_midfield,_do_0_DMG,_have_12x_HP,_and_aren't_knocked_back._Your_upgrades_here_boost_its_HP_by_a_further_+{%.".split(" "), "680 315 6 Endless_Summoning 2500 1.55 1 0 1 58 0 Unlocks_the_Endless_Summoning_feature,_accessed_in_the_Top_Right_when_selecting_an_opponent!_Go_to_the_Summoner's_Table,_you_can't_miss_it!".split(" "), "408 344 7 Muddah 100000 1.55 1 0 1 71 0 2%_chance_to_draw_a_Muddah_during_competition._They_have_25x_HP,_5x_DMG,_and_spawn_2_to_3_random_units_on_death.".split(" "), "395 392 7 Sell_Sell_Sell 500000 1.20 3 0 9999 71 1 All_Summoning_upgrades_cost_}%_less_Essence.".split(" "), "349 360 7 Teal_Tirade 1000000 1.15 5 0 9999 72 1 +{%_Teal_Essence_generated_per_hour_for_each_Teal_circuit_win._@_Total_bonus:_+}%".split(" "), "298 387 7 Unit_Obliteration 5000000 1.40 50 0 9999 73 1 Increases_the_DMG_of_all_summoned_units_in_compeition_by_+{%".split(" "), "247 369 7 Cost_Laundering 10000000 50000 1 0 9999 74 1 Reduces_the_cost_of_all_Summoning_Upgrades_by_+{%_for_every_100_total_summoning_upgrades_purchased._@_Total_bonus:_}%_cost_reduction".split(" "), "198 398 7 Hundredaire 40000000 2.80 1 0 9999 75 1 If_you_have_100x_the_mana_cost_of_a_unit_when_summoned,_you'll_multiply_Unit_Damage_by_+{%_for_the_rest_of_the_match!".split(" "), "177 348 7 Serrated_Spikes 90000000 1.35 1 0 9999 76 1 Spike_damage_is_increased_by_{%".split(" "), "129 384 7 Allstar 200000000 170 1 0 50 77 0 Hey_now,_all_your_Summoning_Doublers_give_+{%_Extra_multiplier_to_their_attached_bonuses!".split(" "), "109 335 7 Whims_of_the_Tide 550000000 12 2 0 250 78 0 +{%_Total_pla..._player_damage?_Am_I_looking_at_this_right...?_Seems_like_it!_@_+{%_Total_Player_Damage_Multiplier!".split(" "), "51 332 7 Teal_Knowledge 1000000000 1.15 1 0 9999 79 1 +{%_Teal_Essence_generation_per_Summoning_LV_you_have._@_Total_bonus:_+}%".split(" "), "48 388 7 Glombolic_Units 2000000000 1.42 100 0 9999 80 1 Embiggens_your_units,_glombolicizing_their_health_by_a_homogonic_+{%_emulcified_pediatrician.".split(" ")]
max_summoning_upgrades = len(summoning_upgrades)
summoning_doubler_recommendations = [
    'Brutal Units', 'DMG Laundering', 'Seeing Red', 'Sharpened Spikes',  #Unique damage multis
    'Final Card', 'Jeweled Cards',
    'Infinite Damage',  #90% of Group C
    'Mana Generation', 'Manaranarr', 'Mana Dividends',  #Mana Generation in battle
    'Beefier Units', 'Stronger Units', 'Powerful Units', 'Unit Damage',  #Rest of the base damage group
    'Units of Destruction', 'Merciless Units',  #Rest of Group C
    'Re-Draw', 'Starting Mana frfr', 'Infinite Essence'
]

#`SummonEnemies = function ()` in source. Last updated in v2.46 Dec 2
SummonEnemies = ["mushG frogG Copper Iron poopSmall Plat Void Starfire branch beanG ratB slimeG mushR acorn snakeG carrotO goblinG plank frogBIG mushW poopD jarSand mimicA crabcake coconut sandcastle pincermin potato steak moonman sandgiant snailZ sheep flake stache bloque mamoth snowball penguin thermostat glass snakeB speaker eye ram skele2 mushP w4a2 w4a3 demonP w4b2 w4b1 w4b3 w4b4 w4b5 w4c1 w4c2 w4c3 w4c4 w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2 w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3 Pet1 Pet2 Pet3 Pet0 Pet4 Pet6 Pet5 Pet10 Pet11 rift1 rift2 rift3 rift4 rift5 Crystal1 Crystal2 Crystal3 Crystal4 Crystal0 Crystal5 babaMummy slimeB mini6a mini3a mini4a mini5a Boss6 babayaga babayaga w7a1 w7a2 w7a3 w7a4 w7a5 w7a6 w7a7 w7a8 w7a9 w7a10 w7a11 w7a12".split(" "), "26 27 20 21 26 20 19 18 32 47 31 23 20 42 33 42 38 44 56 26 27 31 33 35 49 32 39 57 55 27 50 42 32 35 30 40 37 33 52 43 35 31 30 39 37 33 33 31 37 53 28 19 36 46 37 26 19 33 66 24 20 43 30 32 20 22 23 28 31 34 21 34 22 27 35 33 36 46 25 36 45 29 38 23 27 42 29 25 23 28 30 34 26 30 34 40 35 48 36 54 35 35 36 35 44 30 83 50 61 42 84 30 61 0 0 19 31 39 38 50 32 36 29 38 34 31 58".split(" "), "41 18 21 17 19 17 17 17 31 32 19 15 38 25 24 22 34 21 33 37 21 20 30 43 25 17 54 58 37 29 21 26 31 28 19 27 22 26 24 39 27 18 38 23 42 31 32 36 37 34 29 23 36 32 33 26 24 30 39 20 28 36 27 32 27 27 24 30 31 37 22 25 25 34 39 27 35 36 29 33 34 27 33 24 31 41 24 26 22 23 25 21 29 38 30 37 59 34 37 39 42 35 38 35 44 30 0 7 -12 -30 3 10 45 0 0 17 29 29 25 47 31 29 28 25 37 31 42".split(" "), "8 9 10 11 11 10 11 10 20 16 13 10 13 17 14 24 16 21 22 13 14 12 16 21 14 17 26 28 23 22 23 25 14 14 14 12 14 20 22 25 15 14 21 18 21 30 16 23 21 31 18 10 22 28 30 14 10 24 30 10 12 29 18 28 11 18 18 24 28 23 11 22 16 19 27 22 29 34 22 26 31 19 27 14 16 32 12 12 17 12 18 18 14 15 16 24 18 28 22 32 20 15 20 30 22 23 90 90 90 90 90 90 90 90 90 14 22 18 20 41 20 17 22 22 15 22 31".split(" "), "Jonesy_and_his_Lil_Mushies Lex_and_her_Hoppy_Frogs _ _ TP_Pete_Jr_and_his_Battle_Poops _ _ _ Kyle_and_his_Branch_Brigade Bongo_and_his_Lazy_Beans Michael_and_his_Rodents Sam_and_his_Goopy_Slimes Walter_and_his_Lil_Shrooms Aaron_and_his_Aacorn_Gang Mika_and_his_Itty_Bitty_Baby_Boas Guy_Montag_and_his_Walking_Veggies Gork_and_his_Ugly_Glublins Ed_and_his_Stolen_Planks Gigachad_and_his_Awesome_Gigafrogs Kip_and_his_Lil_Fungi Bob_and_his_Boops_of_Death Karen_and_her_Pots Jimmy_and_his_Enthusiastic_Mimics Eugene_and_his_Frosted_Crabs Nobby_and_his_Gang_of_Nuts Tiny_Tim_and_his_Cool_Castles Tira_and_her_Shrewd_Pincermen Misha_and_her_Super_Spuds Wlad_and_his_Rootin'_Tootin'_Tysons Mac_and_his_Many_Moonmoons Sir_Reginald_and_his_Gentlemen_Giants Shelby_and_her_Shelled_Snelbies Paulie_and_his_Sheepie_Herd Dirk_and_his_Celsius_Flakes Mr_Harrison_and_his_Mighty_Staches Gibby_and_his_Bloque_Offensive Esther_and_her_Trampler_Mamooths Frosty_and_his_Relatives The_Accountant_and_his_Trusty_Penguins Fermi_and_his_Thermies Kristen_and_her_Chill_Quenchies Rob_and_his_Ice_Cold_Killer_Snakes Lil_Plump_and_his_Dope_Bops Nadia_and_her_All_Seeing_Eyes Shepherd_and_his_Flock_of_Rams Brody_and_his_Infamous_Bloodbones ProXD_and_his_Mushrooms_of_Mischief Tallie_and_her_Rambunctious_TVs Homer_and_his_Epic_Donuts Nostalgo_and_his_Genies_of_Olde Dalia_and_her_Hyperactive_Drinks Werm_and_his_Worms JelloL0ver87_and_his_Beloved_Gel_Cubes Megacorp_Representative_and_his_Product Werm's_Stepsister_and_her_Worms DQ_and_their_abandoned_Clammies Dee_and_her_'dars Gordon_and_his_Eloquent_Flombeiges Giuseppe_and_his_Power_Tools Jawz_and_his_Hot_Smokin_Suggmas Macdonald_and_his_Homemade_Maccies Brandon_and_his_Iconic_Brightsides Lola_and_her_Crazy_Crackers Mr_M_and_his_Holey_Moleys The_Don's_Molto_Bene_Moltis Smoggy_Shaman_and_their_Scary_Bones Thomas_and_his_Halftime_Breakforce Larry_and_his_Lava_Lamps OwO_and_their_Spirit_Army Briggs_and_his_Mole_Workforce Krepe_and_his_Crawlies Grinder23_and_his_Favorite_Mobs Spiffy_Jr_and_their_Whelming_Liquids iFarm_and_their_0cal_Units Spiffy_Sr_and_his_Bigtime_Liquids Bart_and_his_Trollsquad Grunkle_and_their_Rooted_Whimsy Barb_and_her_Overworked_Blobs Lumi_and_her_Bright_Lights Marge_and_her_Troll_Patrol Lief_and_his_Overzealous_Leeks Seru_and_their_Ceramic_Entities Mr_Walker_and_his_Untiring_Doggies Duke_of_Yolk_and_his_Subjects Sorel_and_her_Esteemed_Sludge Shinji_and_his_Inevitable_Army Pablo_and_his_Plump_Piggies Gam3rPr0digy_and_their_Boar_Stampede Donald_and_his_Quacky_Ducks Sandy_and_her_Nutty_Squirrels Popo_and_their_Largest_of_Mammalians Little_Susie_and_her_Bunny_Family MovieFan84_and_his_Famous_Nacho_Batallion Ronaldo_and_his_Cool_Freakin'_Birdz Master_Oogman_and_his_Speedy_Hedgehogs ENIGMA_INFINITE_and_their_Rift_Spookers ENIGMA_INFINITE_and_their_Rift_Slugs ENIGMA_INFINITE_and_their_Rift_Jocunds ENIGMA_INFINITE_and_their_Rift_Hiveminds ENIGMA_INFINITE_and_their_Rift_Stalkers King's_Gambit Horsey's_Gambit Bishop's_Gambit Queen's_Gambit Castle's_Gambit Noob's_Gambit The_Aetherdoot The_Grover_Glunko The_Shimmerlord The_Freezerslush The_Hexermush The_Cinderdomeo The_Zephyeror W7_boss W8_boss Danny_and_his_Shiny_Fishies Monty_and_his_Dastardly_Doodlefish Rhea_and_her_Eccentric_Eels Clarence_and_his_Slug_Entourage Nina_and_her_Birthday_Balloonfish Karl_and_his_Downtrodden_Clamrades Jojo_and_his_Bizarre_Recyclables Penny_and_her_Lane_of_Puffers Bill_and_his_Spiky_Balls_of_Pain Maple_and_her_Nostalgic_Spearfish Mr._K_and_his_Crusty_Crabs Frankton_and_his_Crab_Army_of_Doom".split(" "), "1 2 _ _ 6 _ _ _ 3 1 4 5 7 6 2 3 4 8 5 1 6 9 7 10 2 8 7 3 5 11 4 1 12 9 6 1 8 13 2 4 10 14 15 7 5 11 16 9 1 3 12 6 8 13 1 2 4 10 14 17 15 1 5 11 16 7 18 9 3 6 4 10 19 2 8 12 14 13 1 16 5 15 17 3 18 20 1 2 3 6 4 2 1 5 3 20 20 20 20 20 20 20 20 20 20 20 0 0 0 0 0 0 0 0 0 1 4 10 12 1 17 4 14 20 1 4 11".split(" "), "<x_Total_DMG <x_Jade_Gain <x_Farming_SPD <x_Artifact_Find +{_Lab_Con_Range <x_All_Essence <x_Sneak_EXP <x_Sigil_SPD <x_Farming_EXP +{%_Drop_Rate <x_Crop_EVO +{%_AFK_Gains +{%_Skill_EXP <x_Construct_SPD <x_Skill_Effncy. <x_Cooking_SPD <x_Gaming_Bits <x_Shiny_EXP +{%_All_Stat +{_Library_Max +{_Stamp_LV/day +{%_Villager_EXP +{%_Ballot_Bonus +{%_Class_EXP +{_Equinox_Max_LV +{%_Monument_AFK <x_Meal_Bonuses <x_Spelunk_POW <x_Amber_Gain +{%_for_World_7 +{%_for_World_7 <x_Winner_Bonuses".split(" "), "15 30 _ _ 15 _ _ _ 4 16 15 0.3 10 20 35 5 20 10 0.3 19 25 5 15 2 40 15 25 6 0.3 10 20 25 1 10 30 30 15 10 50 20 3 30 10 30 0.3 15 50 15 35 6 2 35 20 15 50 75 25 5 60 30 10 40 0.3 25 90 30 25 25 7 25 15 10 3 50 20 2 80 20 60 120 0.3 20 50 8 70 3 8 15 3 7 15 25 12 0.3 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 250 17 5 3 350 250 20 300 1 500 23 90".split(" "), "4 6 _ _ 25 _ _ _ 31 8 28 10 5 39 12 15 17 19 21 50 _ 9 11 14 16 18 22 26 30 34 45 60 20 23 27 29 32 35 38 41 46 49 51 54 65 74 33 36 37 42 43 47 52 56 61 62 66 70 78 44 48 53 55 57 59 63 69 71 75 79 82 84 58 64 67 68 72 73 76 77 80 81 83 85 86 87 0 1 2 3 5 7 13 24 40 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 20 95 120 150 180 220 206 300 320 350 400 450 500".split(" "), "21 22 23 24 25 27 23 22 24 29 25 26 24 23 22 32 30 31 25 24 26 29 24 22 21 23 31 28 27 24 26 22 30 25 29 28 23 26 24 32".split(" "), "1 3 1 12 1 7 2 4 15 3 1 4 18 2 4 3 2 2 2 20 5 4 24 4 1 2 3 5 9 26 5 5 3 1 5 8 2 6 30 3".split(" "), "4 5 1 6 4 0 5 6 7 8 3 10 2 9 7 1 6 5 2 8 3 4 10 6 1 7 2 0 6 3 5 8 9 4 6 2 1 5 10 8".split(" "), "Slow_Motion|All_units,_both_yours_and_my|own,_move_at_60%_speed. Fast_Forward|All_of_our_units,_yours_and|mine,_move_at_170%_speed. Glass_Cannon|You_have_but_a_single_health|point,_as_do_I. Zerg_Surprise|You_best_be_ready,_I'm_playing_all|my_minions_on_turn_1! Extra_Time|I've_doubled_our_health_points_so|we_can_play_longer. Fair_Play|No_lane_stacking!_When_you_hurt_me,|all_your_units_in_that_lane|take_damage. Invincibility|Just_let_me_play_my_units,_I_will|forfeit_one_health_each_time,_but|you_must_deal_the_final_blow. Offsides_Rule|When_you_hurt_me,_all_your_minions|beyond_the_midfield_perish. Triple_Overtime|Ten_times_the_health_points._I_wanna|see_your_deck's_lategame_viability. Truce|No_mods,_no_effects,_no_tricks.|I_want_a_proper_match_this_time. Uno_Draw_7|You're_playing_with_a_7_card_hand.|It's_more_fun_this_way,_trust|me_you'll_love_it!".split(" "), "2000 5000 1000000 75000 20000 300000 5000000 100000000 100000000".split(" "), "250000 1000000 150000000 10000000 4000000 40000000 500000000 2000000000 12000000000.0".split(" ")]

# Maps to the RewardID, 1 indexed because Lava, so placeholder made for [0]
summoningRewards = ['Unknown'] + [entry.replace('_', ' ') for entry in SummonEnemies[6]]
# Replace two '+{% for World 7' with uniq name
index = summoningRewards.index('+{% for World 7')
summoningRewards[index] = '+{% for World 7 #1'
index = summoningRewards.index('+{% for World 7')
summoningRewards[index] = '+{% for World 7 #2'
# summoningRewards = [
#     "Unknown",
#     # Normal Rewards
#     "x Total DMG", "x Jade Gain", "x Farming SPD", "x Artifact Find",
#     " Lab Con Range", "x All Essence", "x Sneak EXP", "x Sigil SPD",
#     "x Farming EXP", "% Drop Rate", "x Crop EVO", "% AFK Gains",
#     "% Skill EXP", "x Construct SPD", "x Skill Effncy.", "x Cooking SPD",
#     "x Gaming Bits", "x Shiny EXP", "% All Stat", " Library Max",
#     # Endless Rewards
#     "+ Stamp LV/day", "% Villager EXP", "% Ballot Bonus", "% Class EXP",
#     "+ Equinox Max LV", "% Monument AFK", "x Meal Bonuses", "% for World 7 (Placeholder 1)", "% for World 7 (Placeholder 2)",
#     "% for World 7 (Placeholder 3)", "% for World 7 (Placeholder 4)", "x Winner Bonuses"
# ]
summoning_rewards_that_dont_multiply_base_value = [
    summoningRewards[0],   #Placeholder
    summoningRewards[21],  #Stamp Levels
    summoningRewards[23],  #Ballot Bonus
    summoningRewards[25],  #Equinox Levels
    summoningRewards[32],  #Winner Bonuses
]

summoning_regular_match_colors = ['White', 'Green', 'Yellow', 'Blue', 'Purple', 'Red', 'Cyan', 'Teal']
#TODO: update everything below when the Teal Summoning Stone exists
summoning_stone_names = {
    'White': 'Aether',
    'Green': 'Grover',
    'Yellow': 'Shimmer',
    'Blue': 'Freezer',
    'Purple': 'Hexer',
    'Red': 'Cinder',
    'Cyan': 'Zephyer',
    'Teal': 'TBD'
}
summoning_stone_locations = ['Bamboo Laboredge', 'Lightway Path', 'Yolkrock Basin', 'Equinox Valley', 'Jelly Cube Bridge', 'Crawly Catacombs', 'Emperor\'s Castle Doorstep']
summoning_stone_stone_images = ['white-summoning-stone', 'green-summoning-stone', 'yellow-summoning-stone', 'blue-summoning-stone', 'purple-summoning-stone', 'red-summoning-stone', 'cyan-summoning-stone']
summoning_stone_boss_images = ['king-doot', 'glunko-the-massive', 'demented-spiritlord', 'dilapidated-slush', 'mutated-mush', 'domeo-magmus', 'the-emperor']
summoning_stone_fight_codenames = ['babaMummy', 'slimeB', 'mini6a', 'mini3a', 'mini4a', 'mini5a', 'Boss6', 'babayaga', 'babayaga']

summoning_stone_boss_base_hp = "250000 1000000 150000000 10000000 4000000 40000000 500000000 2000000000 12000000000".split(" ")
summoning_stone_boss_hp_function = lambda base_hp, boss_round: 2 * base_hp * (4000 ** (boss_round - 1))

summoning_stone_boss_base_damage = "2000 5000 1000000 75000 20000 300000 5000000 100000000 100000000".split(" ")
summoning_stone_boss_damage_function = lambda base_damage, boss_round: Decimal(0.8) * base_damage * (4000 ** (boss_round - 1))

# This is built by manually splitting the list in SummonEnemies[0]
summoning_matches_per_color_dict = {
    'White': "Pet1 Pet2 Pet3 Pet0 Pet4 Pet6 Pet5 Pet10 Pet11".split(" "),
    'Green': "mushG frogG poopSmall branch beanG ratB slimeG mushR acorn snakeG carrotO goblinG plank frogBIG mushW".split(" "),
    'Yellow': "jarSand mimicA crabcake coconut sandcastle pincermin potato steak moonman sandgiant snailZ".split(" "),
    'Blue': "sheep flake stache bloque mamoth snowball penguin thermostat glass snakeB speaker eye ram skele2".split(" "),
    'Purple': "mushP w4a2 w4a3 demonP w4b2 w4b1 w4b3 w4b4 w4b5 w4c1 w4c2 w4c3 w4c4".split(" "),
    'Red': "w5a1 w5a2 w5a3 w5a4 w5a5 w5b1 w5b2 w5b3 w5b4 w5b5 w5b6 w5c1 w5c2".split(" "),
    'Cyan': "w6a1 w6a2 w6a3 w6a4 w6a5 w6b1 w6b2 w6b3 w6b4 w6c1 w6c2 w6d1 w6d2 w6d3".split(" "),
    'Teal': "w7a1 w7a2 w7a3 w7a4 w7a5 w7a6 w7a7 w7a8 w7a9 w7a10 w7a11 w7a12".split(" "),
    'Endless': "rift1 rift2 rift3 rift4 rift5".split(" "),
    'Gambit': "Crystal1 Crystal2 Crystal3 Crystal4 Crystal0 Crystal5".split(" "),
    'Stones': "babaMummy slimeB mini6a mini3a mini4a mini5a Boss6 babayaga babayaga".split(" "),
}
summoning_unimplemented_matches = ['Copper', 'Iron', 'Plat', 'Void', 'Starfire', 'poopD']
#To verify we aren't missing any summoning enemies, we check for any new entries that aren't in the unimplemented matches list
summoning_unassigned_enemy_names = [
    enemy_name for enemy_name in SummonEnemies[0]
    if enemy_name not in [summon for summons in summoning_matches_per_color_dict.values() for summon in summons]
    and enemy_name not in summoning_unimplemented_matches
]
if len(summoning_unassigned_enemy_names) > 0:
    logger.error(f"Unplaced summoning matches found: {summoning_unassigned_enemy_names}. Add them to the proper color in summoning_matches_per_color_dict.")

summoning_regular_battles = []
for color, battles in summoning_matches_per_color_dict.items():
    if color in summoning_regular_match_colors:
        summoning_regular_battles += battles

def get_summoning_battle_color(enemy_id) -> str:
    for color, battles in summoning_matches_per_color_dict.items():
        if enemy_id in battles:
            return color
    return f'Unknown-{enemy_id}'

def get_summoning_battle_type(enemy_id) -> str:
    color = get_summoning_battle_color(enemy_id)
    match color:
        case 'Endless' | 'Gambit' | 'Stones':
            return color
        case _:
            return 'Regular'

summoning_dict = defaultdict(dict)
for match_index in range(0, len(SummonEnemies[0])):
    if SummonEnemies[5][match_index] != '_' and SummonEnemies[0][match_index] not in summoning_unimplemented_matches:
        enemy_codename = SummonEnemies[0][match_index]
        enemy_displayname = decode_monster_name(enemy_codename, False)
        color = get_summoning_battle_color(enemy_codename)
        summoning_dict[color][len(summoning_dict[color])] = {
            'EnemyID': enemy_codename,
            'OpponentName': SummonEnemies[4][match_index].replace('_', ' '),
            'RewardID': summoningRewards[parse_number(SummonEnemies[5][match_index])],
            'RewardQTY': parse_number(SummonEnemies[7][match_index]),
            'Color': color,
            'BattleType': get_summoning_battle_type(enemy_codename),
            'Image': kebab(enemy_displayname),
        }

# summoning_endless_challenge_types = SummonEnemies[12]
summoning_endless_challenge_types = [
    "Slow Motion (60% speed)", "Fast Forward (170% speed)", "Glass Cannon (1 HP)",
    "Zerg Surprise", "Extra Time (2x HP)", "Fair Play (No lane stacking)",
    "Invincibility", "Offsides Rule", "Triple Overtime (10x HP)",
    "Truce (No Mods)", "Uno Draw 7"
]
if len(SummonEnemies[12]) > len(summoning_endless_challenge_types):
    logger.warning(f"Endless Summoning Challenge Types out of sync.")
summoning_endlessDict = {}
summoning_endless_reward_index = [int(i) for i in SummonEnemies[9]]
summoning_endless_reward_qty = [int(i) for i in SummonEnemies[10]]
summoning_endless_challenge_index = [int(i) for i in SummonEnemies[11]]
for index in range(0, 40):
    summoning_endlessDict[index] = {
        'RewardID': summoningRewards[summoning_endless_reward_index[index]],
        'RewardQTY': summoning_endless_reward_qty[index],
        'Challenge': summoning_endless_challenge_types[summoning_endless_challenge_index[index]]
    }
summoning_battle_counts_dict = {k: len(v) for k, v in summoning_dict.items()}
summoning_battle_counts_dict['Normal'] = sum(summoning_battle_counts_dict.values())
summoning_bonus_img = {
    # Regular
    '<x Total DMG': 'summoning-total-dmg',
    '<x Jade Gain': 'summoning-jade',
    '<x All Essence': 'summoning',
    '<x Farming SPD': 'farming',
    '<x Artifact Find': 'sailing',
    '+{ Lab Con Range': 'laboratory',
    '<x Sneak EXP': 'sneaking',
    '<x Sigil SPD': 'sigils',
    '<x Farming EXP': 'farming',
    '+{% Drop Rate': 'vault-upgrade-18',
    '<x Crop EVO': 'farming',
    '+{% AFK Gains': 'summoning-afk',
    '+{% Skill EXP': 'summoning-skill-exp',
    '<x Construct SPD': 'construction',
    '<x Skill Effncy.': 'summoning-skill-eff',
    '<x Cooking SPD': 'cooking',
    '<x Gaming Bits': 'gaming',
    '<x Shiny EXP': 'breeding',
    '+{% All Stat': 'summoning-all-stat',
    '+{ Library Max': 'library',
    # Endless
    '+{ Stamp LV/day': 'summoning-stamp',
    '+{% Villager EXP': 'summoning-village-exp',
    '+{% Ballot Bonus': 'summoning-ballot',
    '+{% Class EXP': 'summoning-class-exp',
    '+{ Equinox Max LV': 'equinox',
    '<x Meal Bonuses': 'cooking',
    '<x Amber Gain': 'summoning-amber',
    '+{% Monument AFK': 'summoning-monument-afk',
    '<x Winner Bonuses': 'endless-summoning',
    '+{% for World 7 #1': 'placeholder',
    '+{% for World 7 #2': 'placeholder',
    '<x Spelunk POW': 'summoning-spelunking-pow'
}
