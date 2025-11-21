from utils.data_formatting import logger
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_convert
from utils.text_formatting import getItemDisplayName
from utils.logging import get_logger
logger = get_logger(__name__)

# `AlchemyDescription` in source. Last updated in v2.43 Nov 10
# [0]=Orange, [1]=Green, [2]=Purple, [3]=Yellow bubbles,
# [4]=Vials, [5]=Water Shop
alchemy_description = [["ROID_RAGIN 1 0 add 0 Copper Liquid1 Blank Blank +{_Total_STR_for_all_players,_always. 0 1 2 0 0 TotalSTR".split(" "), "WARRIORS_RULE 2 50 decayMulti 0 Grasslands1 Liquid1 Blank Blank All_Orange_Passive_Bubbles,_which_are_the_smaller_sized_ones,_give_a_{x_higher_bonus_to_your_warrior-based_classes. 0 3 2 0 0 Opassz".split(" "), "HEARTY_DIGGY 50 100 decay 0 JungleTree Liquid1 Blank Blank +{%_mining_efficiency_per_power_of_10_max_HP_that_your_character_has._The_perfect_bonus_for_miners_with_infinite_HP! 0 5 2 0 0 MinEff".split(" "), "WYOMING_BLOOD 23.5 1.5 bigBase 0 Bug1 Liquid1 Blank Blank +{%_chance_for_Multiple_Ores_while_Mining,_and_the_max_is_now_300%,_not_100%._Big_bubbles_like_this_must_be_equipped_to_give_bonus. 1 10 3 0 0 MiningACTIVE".split(" "), "REELY_SMART 100 80 decay 0 CraftMat6 Liquid1 Blank Blank +{%_Mining_and_Fishing_EXP_gain._Y'know_what,_I'll_even_DOUBLE_that_bonus_for_whichever_skill_has_the_lower_level! 0 20 3 0 0 MinFishEXP".split(" "), "BIG_MEATY_CLAWS 4 0 add 0 DesertB2 Liquid1 Blank Blank Increases_base_damage_by_+$._This_bonus_increases_based_on_how_much_Max_HP_you_have_above_250. 0 200 4 0 0 bdmgHP".split(" "), "SPLOOSH_SPLOOSH 23.5 1.5 bigBase 0 Fish2 Liquid1 Blank Blank Multi-Fish_fishing_chance_is_increased_by_+{%,_and_your_max_Multi-Fish_chance_is_300%_instead_of_100%. 1 100 4 0 0 FishingACTIVE".split(" "), "STRONK_TOOLS 65 70 decay 0 Plat Liquid1 Blank Blank The_following_tools_give_+{%_more_skilling_Power_than_normal:_$ 0 60 4 0 0 ToolW".split(" "), "FMJ 0.5 0 add 0 Bug4 Liquid1 Blank Blank +{%_more_defence_from_Equipment._Also,_+1_base_Def_per_Class_LV,_up_to_+{. 0 50 5 0 0 DefPct".split(" "), "BAPPITY_BOOPITY 35 100 decay 0 CraftMat8 Liquid1 Blank Blank +{%_critical_Damage._Badabing,_badaboom!_Or_in_Italian,_Babadabinga,_babadaboomahh! 0 100 5 0 0 critDMG".split(" "), "BRITTLEY_SPEARS 40 50 decay 0 Critter1 Liquid2 Blank Blank +{%_Total_damage._This_multiplies_with_other_damage_bonuses,_but_adds_with_the_other_'+%_Total_Damage'_bubbles. 0 10 3 0 0 pctDmg1".split(" "), "CALL_ME_BOB 25 2.5 bigBase 0 SnowA3 Liquid2 Blank Blank +{%_Construction_EXP_Gain._Also_gives_+50%_Bug-Fixing_speed_if_your_username_is_LavaFlame2. 1 120 3 0 0 conEXPACTIVE".split(" "), "CARPENTER 5 50 decay 0 Refinery2 Liquid2 Blank Blank +{%_Build_Speed_per_Construction_Level._Not_affected_by_'Warriors_Rule'_bubble. 0 3 4 0 0 Construction".split(" "), "BUFF_BOI_TALENT 5 1 bigBase 0 Critter4 Liquid2 Blank Blank +{_Talent_Points_for_EACH_tab!_But_it's_just_for_warriors,_don't_tell_the_other_classes!!_NOTE:_Doesn't_affect_Master_Class 0 50 2 0 0 TalWarrior".split(" "), "ORANGE_BARGAIN 40 12 decay 0 Soul4 Liquid2 Blank Blank The_material_costs_of_ALL_orange_bubbles_are_{%_lower 0 30 3 0 0 BubbleCostOr".split(" "), "PENNY_OF_STRENGTH 18 30 decay 0 Fish5 Liquid3 Blank Blank +{%_Cash_from_Monsters_for_every_250_STR._The_pennies_reflect_your_strength_in_themselves,_thus_making_them_more_valuable! 0 200 3 0 0 CashSTR".split(" "), "MULTORANGE 1.4 30 decayMulti 0 GalaxyA3 Liquid3 Blank Blank The_following_orange_bubbles_give_{x_higher_bonus_than_displayed:_1st,_3rd,_5th,_8th,_15th 0 250 3 0 0 MultiOr".split(" "), "DREAM_OF_IRONFISH 12 30 decay 0 CraftMat13 Liquid3 Blank Blank +{%_Mining_and_Fishing_AFK_GAINS_rate._Wow,_how_bias_can_you_get..._giving_the_warrior's_bubble_TWO_afk_gain_bonuses. 0 200 4 0 0 MinFshAFK".split(" "), "SHIMMERON 80 40 decay 0 CraftMat14 Liquid3 Blank Blank +{%_Gold_Food_Effect._Go_on,_its_ok,_I_won't_be_offended._No_seriously,_go_upgrade_something_else,_I_know_I'm_not_a_good_upgrade... 0 300 4 0 0 GFoodz".split(" "), "BITE_BUT_NOT_CHEW 50 40 decay 0 GalaxyC4 Liquid3 Blank Blank +{%_Food_Non-Consume_chance._Also,_if_your_capped_Non-Consume_chance_happens_to_be_98%,_this_changes_it_to_99%! 1 200 5 0 0 nonFoodACTIVE".split(" "), "SPEAR_POWAH 40 60 decay 0 Bits Liquid3 Blank Blank +{%_more_Weapon_Power_from_your_weapon,_but_only_if_its_a_Spear! 0 10000 5 0 0 W1".split(" "), "SLABI_OREFISH 3 60 decay 0 Soul6 Liquid3 Blank Blank +{_Mining_and_Fishing_Power_per_100_items_found,_shown_on_The_Slab! 0 150 5 0 0 W2".split(" "), "GAMER_AT_HEART 20 60 decay 0 SailTr9 Liquid3 Blank Blank When_claiming_AFK_Gains,_+{%_chance_to_gain_an_equal_amount_of_time_for_Gaming_progress! 1 100 6 0 0 W3ACTIVE".split(" "), "SLABI_STRENGTH 25 60 decay 0 LavaB3b Liquid3 Blank Blank +{_Base_STR_per_100_items_found,_shown_on_The_Slab! 0 2 6 0 0 W4".split(" "), "POWER_TRIONE 23 50 decay 0 SailTr20 Liquid3 Blank Blank +{%_Total_Damage_per_250_STR,_but_only_for_warriors!_No_triple_dipping_into_AGI_and_WIS!_Also_this,_but_for_beginners_with_LUK! 0 150 6 0 0 W5".split(" "), "FARQUAD_FORCE 30 60 decay 0 W6item1 Liquid3 Blank Blank The_effect_STR_has_on_Damage_is_increased_by_+{% 0 100 5 0 0 W6".split(" "), "ENDGAME_EFF_I 3 60 decay 0 SpiA2b Liquid3 Blank Blank +{_Mining_and_Fishing_Power._This_bonus_increases_based_on_every_10_Class_LVs_you_are_above_500. 0 150 5 0 0 W7".split(" "), "TOME_STRENGTH 2.5 60 decay 0 W6item8 Liquid4 Blank Blank +{%_STR_for_every_2000_Tome_Completion_Points_over_5000._So_you'd_get_one_stack_of_this_at_7000_pts,_two_at_9000,_etc 0 500 6 0 0 W8".split(" "), "ESSENCE_BOOST 50 60 decay 0 Tree13 Liquid4 Blank Blank +{%_Red_Essence_Gain,_this_bonus_increases_based_on_the_total_level_of_ALL_your_warriors! 0 200 6 0 0 W9AllCharz".split(" "), "CROP_CHAPTER 12 50 decay 0 W6item10 Liquid4 Blank Blank +{%_Crop_Evolution_chance_for_every_2000_Tome_Completion_Points_above_5000. 0 1500 6 0 0 W10AllCharz".split(" "), "DOUBLE_PAGEY 30 130 decay 0 w7A1 Liquid4 Blank Blank +{%_Multi_Page_chance_for_active_Spelunking!_Now_you_can_not_read_things_TWICE_as_much!!_Who_am_I_even_talking_to!!! 0 4000 7 0 0 W11".split(" "), "DMG_OF_THE_SUN 4000 300 decay 0 W7item0 Liquid4 Blank Blank +{%_Total_Damage._This_is_additive,_so_the_better_you_are_the_less_you'll_even_notice_this_bonus. 0 10 8 0 0 W12".split(" "), "BONE_BUBBLE 200 500 decay 0 Bug15 Liquid4 Blank Blank +{%_Extra_Dust_for_Deathbringers._Wait_I_meant_Bones,_since_Dust_is_for_Arcane_Cultists._Wait_I_meant_Windwalkers. 0 1000 9 0 0 W13".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 W14".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 W15".split(" ")], ["SWIFT_STEPPIN 1 0 add 0 DesertA1 Liquid1 Blank Blank +{_Total_AGI_for_all_players,_always. 0 1 2 0 0 TotalAGI".split(" "), "ARCHER_OR_BUST 2 50 decayMulti 0 Grasslands1 Liquid1 Blank Blank All_Green_Passive_Bonuses,_which_are_the_smaller_sized_ones,_give_{x_more_bonuses_to_your_archer-based_characters. 0 3 2 0 0 Gpassz".split(" "), "HAMMER_HAMMER 23 2 bigBase 0 Iron Liquid1 Blank Blank Lets_you_produce_two_items_at_once_in_the_anvil,_and_gives_+{%_production_speed._Big_bubbles_like_this_must_be_equipped_to_give_bonus. 1 5 2 0 0 AnvilACTIVE".split(" "), "LIL_BIG_DAMAGE 20 100 decay 0 Fish1 Liquid1 Blank Blank +{%_Mastery._Mastery_is_your_stat_that_boosts_minimum_damage._Just_like_in_Maplest..._err,_just_like_how_I_thought_it_up_myself! 0 10 3 0 0 Mastery".split(" "), "ANVILNOMICS 40 100 decay 0 ForestTree Liquid1 Blank Blank Costs_for_buying_Anvil_Production_Points_is_reduced_by_{%._This_is_just_like_a_tax_cut,_so_remember_me_as_a_hero! 0 20 3 0 0 AnvilProdCost".split(" "), "QUICK_SLAP 4 0 add 0 DesertB1 Liquid1 Blank Blank Increases_base_damage_by_+$._This_bonus_increases_based_on_how_much_Movement_Speed_you_have_above_110%. 0 90 4 0 0 bdmgSPD".split(" "), "SANIC_TOOLS 65 70 decay 0 Jungle1 Liquid1 Blank Blank The_following_tools_give_+{%_more_skilling_Power_than_normal:_$ 0 130 4 0 0 ToolA".split(" "), "BUG] 23.5 1.5 bigBase 0 Bug3 Liquid1 Blank Blank Multi-Bug_catching_chance_is_increased_by_+{%,_and_your_max_Multi-Bug_chance_is_300%_instead_of_100%. 1 70 4 0 0 CatchingACTIVE".split(" "), "SHAQURACY 1 0 add 0 Fish4 Liquid1 Blank Blank Your_secondary_stat_(WIS_for_warrior,_STR_for_archer,_AGI_for_mage)_gives_+{%_more_Accuracy_than_normal. 0 65 5 0 0 AccPct".split(" "), "CHEAP_SHOT 7 100 decay 0 Bug5 Liquid1 Blank Blank +{%_critical_Chance,_as_it_increases_the_chance_for_your_attack_to_hit_the_monster's_privates,_and_for_the_monster_to_be_male. 0 35 5 0 0 CritChance".split(" "), "BOW_JACK 40 50 decay 0 Soul1 Liquid2 Blank Blank +{%_Total_damage._This_multiplies_with_other_damage_bonuses,_but_adds_with_the_other_'+%_Total_Damage'_bubbles. 0 5 3 0 0 pctDmg2".split(" "), "CALL_ME_ASH 25 2 bigBase 0 SaharanFoal Liquid2 Blank Blank +{%_Trapping_Efficiency_when_this_bubble_is_equipped._Also,_+1_Placeable_Trap_ALWAYS,_even_when_this_isn't_equipped! 1 100 3 0 0 TrapACTIVE".split(" "), "CUZ_I_CATCH_EM_ALL 3 100 decayMulti 0 Soul3 Liquid2 Blank Blank {x_more_likely_to_catch_shiny_critters_when_opening_a_trap. 0 25 4 0 0 CritShiny".split(" "), "FAST_BOI_TALENT 5 1 bigBase 0 Bug6 Liquid2 Blank Blank +{_Talent_Points_for_EACH_tab,_but_just_for_Archers!_Oh,_and_also_for_the_SECRET_class..._NOTE:_Doesn't_affect_Master_Class 0 120 2 0 0 TalArchers".split(" "), "GREEN_BARGAIN 40 12 decay 0 Critter5 Liquid2 Blank Blank The_material_costs_of_ALL_green_bubbles_are_{%_lower 0 200 3 0 0 BubbleCostGr".split(" "), "DOLLAR_OF_AGILITY 18 30 decay 0 CraftMat11 Liquid3 Blank Blank +{%_Cash_from_Monsters_for_every_250_AGI._The_extra_agility_allows_the_dollars_to_stretch_in_size_and_increase_in_value! 0 250 3 0 0 CashAGI".split(" "), "PREMIGREEN 1.4 30 decayMulti 0 Critter8 Liquid3 Blank Blank The_following_green_bubbles_give_{x_higher_bonus_than_displayed:_1st,_7th,_10th,_13th,_15th 0 150 3 0 0 MultiGr".split(" "), "FLY_IN_MIND 12 40 decay 0 Bug7 Liquid3 Blank Blank +{%_Catching_AFK_Gains_Rate._Now_you_too_can_dream_about_bugs_in_your_sleep,_just_like_I_do_all_the_time!!!! 0 350 4 0 0 CatchinAFK".split(" "), "KILL_PER_KILL 70 40 decay 0 Refinery4 Liquid3 Blank Blank +{%_extra_Kills_for_Deathnote_and_opening_portals_to_new_maps._Shoutout_to_my_Idle_Skilling_players_who_remember_'Kill_Per_Kill'! 1 6 4 0 0 kpkACTIVE".split(" "), "AFK_EXPEXP 40 40 decay 0 Bug8 Liquid3 Blank Blank +{%_chance_for_Double_EXP_when_claiming_AFK_gains._You'll_know_this_happens_because_it_literally_tells_you_it_happened! 0 300 5 0 0 DubEXP".split(" "), "BOW_POWER 40 60 decay 0 Bits Liquid3 Blank Blank +{%_more_Weapon_Power_from_your_weapon,_but_only_if_its_a_Bow! 0 10000 5 0 0 A1".split(" "), "SLABO_CRITTERBUG 3 60 decay 0 Tree9 Liquid3 Blank Blank +{_Catching_and_Trapping_Power_per_100_items_found,_shown_on_The_Slab! 0 500 5 0 0 A2".split(" "), "SAILOR_AT_HEART 16 60 decay 0 SailTr11 Liquid3 Blank Blank When_claiming_AFK_Gains,_+{%_chance_to_gain_an_equal_amount_of_time_for_Sailing_progress! 1 100 6 0 0 A3ACTIVE".split(" "), "SLABO_AGILITY 25 60 decay 0 LavaB6 Liquid3 Blank Blank +{_Base_AGI_and_LUK_per_100_items_found,_shown_on_The_Slab!_Woah_cool_this_is_like_a_Archer_Beginner_crossover_bubble! 0 250 6 0 0 A4".split(" "), "POWER_TRITWO 23 50 decay 0 SailTr24 Liquid3 Blank Blank +{%_Total_Damage_per_250_AGI,_but_only_for_archers!_No_triple_dipping_into_STR_and_WIS! 0 150 6 0 0 A5".split(" "), "QUICKDRAW_QUIVER 40 60 decay 0 W6item0 Liquid3 Blank Blank The_effect_AGI_has_on_Damage_is_increased_by_+{% 0 25000 5 0 0 A6".split(" "), "ESSENCE_BOOST 50 60 decay 0 Tree12 Liquid3 Blank Blank +{%_Green_Essence_Gain,_this_bonus_increases_based_on_the_total_level_of_ALL_your_archers! 0 500 5 0 0 A7AllCharz".split(" "), "ENDGAME_EFF_II 3 60 decay 0 W6item3 Liquid4 Blank Blank +{_Catching_and_Trapping_Power._This_bonus_increases_based_on_every_10_Class_LVs_you_are_above_500. 0 150 6 0 0 A8".split(" "), "TOME_AGILITY 2.5 60 decay 0 Bug13 Liquid4 Blank Blank +{%_AGI_for_every_2000_Tome_Completion_Points_over_5000._So_you'd_get_one_stack_of_this_at_7000_pts,_two_at_9000,_etc 0 750 6 0 0 A9".split(" "), "STEALTH_CHAPTER 10 50 decay 0 W6item5 Liquid4 Blank Blank +{%_Stealth_(the_stat_that_lowers_detection_rate_in_Sneaking)_for_every_2000_Tome_Completion_Points_above_5000. 0 250 6 0 0 A10AllCharz".split(" "), "SPAPUNKIE 400 150 decay 0 w7A2 Liquid4 Blank Blank +{%_Spelunking_Efficiency._You_yearn_that_much_more_for_the_tiny_gaps_in_caverns_that_man_was_not_meant_to_venture... 0 4000 7 0 0 A11".split(" "), "DMG_OF_THE_MOON 4000 300 decay 0 Spelunking1 Liquid4 Blank Blank +{%_Total_Damage._This_is_additive,_so_the_better_you_are_the_less_you'll_even_notice_this_bonus. 0 100 8 0 0 A12".split(" "), "DUST_BUBBLE 200 500 decay 0 Soul8 Liquid4 Blank Blank +{%_Extra_Dust_for_Windwalkers. 0 300 9 0 0 A13".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 A14".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 A15".split(" ")], ["STABLE_JENIUS 1 0 add 0 OakTree Liquid1 Blank Blank +{_Total_WIS_for_all_players,_always. 0 1 2 0 0 TotalWIS".split(" "), "MAGE_IS_BEST 2 50 decayMulti 0 Grasslands1 Liquid1 Blank Blank All_Purple_Passive_Bonuses,_which_are_the_smaller_sized_ones,_give_{x_more_bonuses_to_your_mage-based_characters. 0 3 2 0 0 Ppassz".split(" "), "HOCUS_CHOPPUS 50 100 decay 0 CraftMat5 Liquid1 Blank Blank +{%_choppin_efficiency_per_power_of_10_max_MP_that_your_character_has._Super_diaper!_Err,_duper. 0 5 2 0 0 ChopEff".split(" "), "MOLTO_LOGGO 23.5 1.5 bigBase 0 IronBar Liquid1 Blank Blank +{%_chance_for_Multiple_Logs_while_Choppin,_and_the_max_is_now_300%,_not_100%._Big_bubbles_like_this_must_be_equipped_to_give_bonus. 1 10 3 0 0 MultiLogACTIVE".split(" "), "NOODUBBLE 100 60 decay 0 CraftMat7 Liquid1 Blank Blank +{%_Choppin'_and_Alchemy_EXP_gain._Y'know_what,_I'll_even..._actually,_never_mind. 0 20 3 0 0 ChopAlchEXP".split(" "), "NAME_I_GUESS 4 0 add 0 Gold Liquid1 Blank Blank Increases_base_damage_by_+$._This_bonus_increases_based_on_how_much_Max_MP_you_have_above_150. 0 40 4 0 0 bdmgMP".split(" "), "LE_BRAIN_TOOLS 65 70 decay 0 Bug3 Liquid1 Blank Blank The_following_tools_give_+{%_more_skilling_Power_than_normal:_$ 0 55 4 0 0 ToolM".split(" "), "COOKIN_ROADKILL 120 70 decay 0 ToiletTree Liquid1 Blank Blank Cranium_Cooking_lasts_{%_longer,_gives_{%_more_progress_per_kill,_and_has_a_{%_lower_cooldown._Also_+{%_Alchemy_EXP! 1 75 4 0 0 AlchemyACTIVE".split(" "), "BREWSTACHIO 50 100 decay 0 DesertC1 Liquid1 Blank Blank +{%_Brew_Speed._This_a_multiplicative_bonus,_which_means_its_ultra_powerful,_all_the_time!_Even_on_Mondays,_the_worst_day! 0 150 5 0 0 BrewSpd".split(" "), "ALL_FOR_KILL 40 100 decay 0 StumpTree Liquid1 Blank Blank Attack_Talents_give_+{%_higher_bonuses_to_Offline_Gains_than_they_normally_do._So_you_might_as_well_just_AFK_forever,_bye! 0 100 5 0 0 AttackAfk".split(" "), "MATTY_STAFFORD 40 50 decay 0 Refinery1 Liquid2 Blank Blank +{%_Total_damage._This_multiplies_with_other_damage_bonuses,_but_adds_with_the_other_'+%_Total_Damage'_bubbles. 0 3 3 0 0 pctDmg3".split(" "), "CALL_ME_POPE 2.4 70 decayMulti 0 Critter2 Liquid2 Blank Blank {x_Worship_Charge_rate_per_hour._Also,_{x_Max_Worship_Charge!_You_bouta_go_super_with_all_that_charge..._just_sayin' 1 25 3 0 0 worshipACTIVE".split(" "), "GOSPEL_LEADER 60 30 decay 0 Bug5 Liquid2 Blank Blank +{%_Max_Charge_per_10_Worship_levels._I_guess_you_could_say_this_upgrade_doesn't_come_Free_of_Charge! 0 150 4 0 0 maxCharge".split(" "), "SMART_BOI_TALENT 5 1 bigBase 0 SnowC1 Liquid2 Blank Blank Sorry,_mages_don't_get_anything..._Ok_fine,_you_can_have_+{_Talent_Points_for_each_tab._NOTE:_Doesn't_affect_Master_Class 0 150 2 0 0 TalWiz".split(" "), "PURPLE_BARGAIN 40 12 decay 0 Soul1 Liquid2 Blank Blank The_material_costs_of_ALL_purple_bubbles_are_{%_lower 0 500 3 0 0 BubbleCostPu".split(" "), "NICKEL_OF_WISDOM 18 30 decay 0 AlienTree Liquid3 Blank Blank +{%_Cash_from_Monsters_for_every_250_WIS._Wisdom_allows_the_nickel_to_trick_others_into_thinking_its_a_Dime,_increasing_its_value! 0 150 3 0 0 CashWIS".split(" "), "SEVERAPURPLE 1.4 30 decayMulti 0 Void Liquid3 Blank Blank The_following_purple_bubbles_give_{x_higher_bonus_than_displayed:_1st,_3rd,_5th,_13th,_15th 0 175 3 0 0 MultiPu".split(" "), "TREE_SLEEPER 12 40 decay 0 Soul5 Liquid3 Blank Blank +{%_Choppin'_AFK_Gains_Rate._Ain't_nothin'_like_sittin'_down_at_the_ol'_tree_and_havin'_a_snooze_n'_a_sleep! 0 60 4 0 0 ChoppinAFK".split(" "), "HYPERSWIFT 30 30 decay 0 Fish7 Liquid3 Blank Blank +{%_Basic_Attack_Speed._Just_like_all_other_Basic_Attack_Speed_bonuses,_this_boosts_AFK_kills/hr_if_you_do_enough_dmg! 0 250 4 0 0 BAspd".split(" "), "MATRIX_EVOLVED 60 40 decay 0 Tree8 Liquid3 Blank Blank +{%_Lab_EXP_Gain._Also_+{%_ineptitude_to_face_the_reality_of_what's_REALLY_going_on_behind_the_scenes... 1 250 5 0 0 LabXpACTIVE".split(" "), "WAND_PAWUR 40 60 decay 0 Bits Liquid3 Blank Blank +{%_more_Weapon_Power_from_your_weapon,_but_only_if_its_a_Wand!_Or_a_fisticuff_I_guess... 0 10000 5 0 0 M1".split(" "), "SLABE_LOGSOUL 3 60 decay 0 Bug9 Liquid3 Blank Blank +{_Choppin_and_Worship_Power_per_100_items_found,_shown_on_The_Slab! 0 250 5 0 0 M2".split(" "), "PIOUS_AT_HEART 300 100 decay 0 SailTr13 Liquid3 Blank Blank +{%_Divinity_EXP_Gain 1 15 6 0 0 M3ACTIVE".split(" "), "SLABE_WISDOM 25 60 decay 0 LavaC1 Liquid3 Blank Blank +{_Base_WIS_per_100_items_found,_shown_on_The_Slab! 0 200 6 0 0 M4".split(" "), "POWER_TRITHREE 23 50 decay 0 SailTr28 Liquid3 Blank Blank +{%_Total_Damage_per_250_WIS,_but_only_for_mages!_No_triple_dipping_into_STR_and_AGI! 0 200 6 0 0 M5".split(" "), "SMARTER_SPELLS 25 60 decay 0 W6item6 Liquid3 Blank Blank The_effect_WIS_has_on_Damage_is_increased_by_+{% 0 500 5 0 0 M6".split(" "), "ENDGAME_EFF_III 3 60 decay 0 W6item7 Liquid3 Blank Blank +{_Choppin_and_Worship_Power._This_bonus_increases_based_on_every_10_Class_LVs_you_are_above_500. 0 950 5 0 0 M7".split(" "), "ESSENCE_BOOST 50 100 decay 0 Soul7 Liquid4 Blank Blank +{%_Purple_Essence_Gain,_this_bonus_increases_based_on_the_total_level_of_ALL_your_mages! 0 250 6 0 0 M8AllCharz".split(" "), "TOME_WISDOM 2.5 60 decay 0 W6item4 Liquid4 Blank Blank +{%_WIS_for_every_2000_Tome_Completion_Points_over_5000._So_you'd_get_one_stack_of_this_at_7000_pts,_two_at_9000,_etc 0 150 6 0 0 M9".split(" "), "ESSENCE_CHAPTER 15 50 decay 0 W6item0 Liquid4 Blank Blank +{%_All_Essence_Gain_for_every_2000_Tome_Completion_Points_above_5000. 0 250000 6 0 0 M10AllCharz".split(" "), "DEEP_DEPTH 8 200 decay 0 Prehistrium Liquid4 Blank Blank +{%_chance_to_find_the_rope_'n_hole_to_the_next_Depth_in_Speluking_Delves. 0 1000 7 0 0 M11".split(" "), "DMG_OF_THE_SOUL 4000 300 decay 0 w7A4 Liquid4 Blank Blank +{%_Total_Damage._This_is_additive,_so_the_better_you_are_the_less_you'll_even_notice_this_bonus. 0 4000 8 0 0 M12".split(" "), "TACHYON_BUBBLE 250 500 decay 0 w7A8 Liquid4 Blank Blank +{%_Extra_Tachyons_for_Arcane_Cultist. 0 4000 9 0 0 M13".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 M14".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 M14".split(" ")], ["LOTTO_SKILLS 1 0 add 0 CraftMat1 Liquid1 Blank Blank +{_LUK_for_all_players,_always. 0 1 2 0 0 TotalLUK".split(" "), "DROPPIN_LOADS 40 70 decay 0 Fish1 Liquid1 Blank Blank +{%_Drop_Rate._Thanks_to_this_upgrade,_you_can_get_even_MORE_angry_when_you_keep_not_getting_that_rare_item_you're_grinding_for! 0 3 2 0 0 DropRate".split(" "), "STARTUE_EXP 25 60 decay 0 BirchTree Liquid1 Blank Blank Leveling_up_a_statue_resets_it's_exp_bar_down_to_{%,_instead_of_0%._Staturrific!_Yea..._the_jokes_are_only_gonna_go_downhill_from_here_lol 0 5 2 0 0 StatueStartEXP".split(" "), "LEVEL_UP_GIFT 100 30 decay 0 DesertA3 Liquid1 Blank Blank {%_chance_for_a_gift_to_drop_when_leveling_up,_like_a_gem_or_an_EXP_Balloon!_Big_bubbles_like_this_must_be_equipped_to_give_bonus. 1 10 2 0 0 LevelUpACTIVE".split(" "), "PROWESESSARY 1.5 60 decayMulti 0 ToiletTree Liquid1 Blank Blank The_Prowess_Bonus_for_every_skill_is_multiplied_by_{._Prowess_lowers_the_Efficiency_needed_to_get_multiple_QTY_per_drop_from_resources. 0 20 3 0 0 ProwessMulti".split(" "), "STAMP_TRAMP 1 0 add 0 Bug2 Liquid1 Blank Blank Increases_the_Max_Lv_of_the_'Toilet_Paper_Postage'_Talent_to_{._You_unlock_this_talent_by_typing_'More_like_Poopy_Pete'_near_Pete. 0 45 4 0 0 TPpostage".split(" "), "UNDEVELOPED_COSTS 40 70 decay 0 Fish3 Liquid1 Blank Blank Reduces_the_material_costs_of_all_Alchemy_Bubbles_by_{%._They_are_just_bubbles_though,_how_much_could_they_even_cost?_10_dollars? 0 65 6 0 0 BubbleCost".split(" "), "DA_DAILY_DRIP 30 100 decay 0 CraftMat9 Liquid1 Blank Blank Increases_the_Max_Cap_for_every_liquid_by_+$._This_bonus_increases_based_on_the_combined_Alchemy_LV_of_all_your_characters! 0 125 8 0 0 LqdCap".split(" "), "GRIND_TIME 9.7 .3 bigBase 0 Liquid1 Liquid2 Blank Blank +{%_Class_EXP._The_go-to_active_bubble_for_anyone_who_wants_to_reach_max_level_faster_and_finally_start_playing_the_game! 1 50 25 0 0 expACTIVE".split(" "), "LAAARRRRYYYY 120 100 decay 0 Dementia Liquid2 Blank Blank Every_time_you_upgrade_an_Alchemy_bubble,_there's_a_{%_chance_it'll_upgrade_2_times,_for_no_extra_cost!_Two_fer_one,_getter_dun! 0 50 4 0 0 DoubleBubbleUpg".split(" "), "COGS_FOR_HANDS 4 0 add 0 SnowA2 Liquid2 Blank Blank +{%_Cog_Production_speed._Cogs_are_great._I_really_really_like_cogs._I_guess_you_could_say_I_think_they're_pretty_Coggers... 0 50 3 0 0 CogMakeSpd".split(" "), "SAMPLE_IT 12 40 decay 0 Soul2 Liquid2 Blank Blank +{%_Sample_Size_when_taking_samples_for_the_3d_printer._Finally,_your_statisitcal_analysis_will_be_accurate! 0 15 3 0 0 SampleSize".split(" "), "BIG_GAME_HUNTER 60 30 decay 0 Critter3 Liquid2 Blank Blank Killing_a_Giant_Monster_has_a_{%_chance_to_not_decrease_the_Giant_Mob_Spawn_Odds,_which_reset_at_the_end_of_each_week. 1 40 4 0 0 GiantsACTIVE".split(" "), "IGNORE_OVERDUES 100 60 decay 0 Tree7 Liquid2 Blank Blank +{%_Book_Checkout_speed,_all_thanks_to_this_one_little_bubble_that_librarians_do_NOT_want_you_to_know_about! 0 120 2 0 0 booksSpeed".split(" "), "YELLOW_BARGAIN 40 12 decay 0 Critter6 Liquid2 Blank Blank The_material_costs_of_ALL_yellow_bubbles_are_{%_lower. 0 250 3 0 0 BubbleCostYe".split(" "), "MR_MASSACRE 90 50 decay 0 Refinery3 Liquid3 Blank Blank +{%_Multikill_per_damage_tier._Remember,_damage_tier_is_shown_by_the_Purple_Bar_in_AFK_info,_and_multikill_is_bigtime_for_resources 1 8 3 0 0 MKtierACTIVE".split(" "), "EGG_INK 40 40 decay 0 Spice0 Liquid3 Blank Blank +{%_faster_Egg_Incubation_Time_in_the_Pet_Nest._This_will_be_an_absolutely_VITAL_upgrade_once_you_unlock_pet_egg_rarity! 0 100 4 0 0 EggInc".split(" "), "DIAMOND_CHEF 0.3 13 decayMulti 0 Spice6 Liquid3 Blank Blank {x_faster_Meal_and_Fire_Kitchen_Speeds_for_every_Meal_at_Lv_11+._This_is_when_the_meal_plate_becomes_Diamond_Blue,_just_so_you_know! 0 100 4 0 0 MealSpdz".split(" "), "CARD_CHAMP 100 40 decay 0 Spice9 Liquid3 Blank Blank +{%_Card_Drop_Chance_for_all_card_types,_even_Party_Dungeon_cards! 0 100 5 0 0 CardDropz".split(" "), "PETTING_THE_RIFT 15 50 decay 0 Critter10 Liquid3 Blank Blank +{%_Shiny_Pet_Chance_for_every_new_Rift_level_you_reach._Go_find_the_Rift_Ripper,_above_the_Octodars_in_World_4. 0 100 5 0 0 NewPetRift".split(" "), "BOATY_BUBBLE 135 70 decay 0 Bits Liquid3 Blank Blank +{%_Sailing_Speed_for_all_boats 0 5000 5 0 0 Y1".split(" "), "BIG_P 0.5 60 decayMulti 0 SailTr1 Liquid3 Blank Blank {x_higher_bonus_than_displayed_from_the_Minor_Link_bonus_of_the_deity_you're_linked_to_in_Divinity._AKA_bigger_god_passive! 1 50 5 0 0 Y2ACTIVE".split(" "), "BIT_BY_BIT 50 70 decay 0 Tree10 Liquid3 Blank Blank +{%_more_bits_earned_in_gaming_per_plant_found,_as_shown_in_the_Log_Book_found_in_the_top_right_of_the_gaming_garden! 0 200 5 0 0 Y3".split(" "), "GIFTS_ABOUND 40 60 decay 0 Bug10 Liquid3 Blank Blank +{%_chance_to_not_use_up_Divinity_points_when_offering_a_gift! 0 200 6 0 0 Y4".split(" "), "ATOM_SPLIT 14 40 decay 0 LavaC2 Liquid3 Blank Blank +{%_lower_particle_cost_for_upgrading_all_atoms_ 0 250 6 0 0 Y5".split(" "), "CROPIUS_MAPPER 5 70 decay 0 SpiA5 Liquid3 Blank Blank +{%_Crop_Evolution_chance_for_EVERY_map_you_unlock_in_world_6,_across_all_characters!_Total_bonus:_$ 0 1000 5 0 0 Y6".split(" "), "ESSENCE_BOOST 50 60 decay 0 Bug12 Liquid3 Blank Blank +{%_Yellow_Essence_Gain._This_bonus_doesn't_increase_based_on_anything! 0 1500 5 0 0 Y7".split(" "), "HINGE_BUSTER 100 70 decay 0 W6item2 Liquid4 Blank Blank Your_ninja_twins_do_+{%_more_damage_to_doors!_Knock_knock,_let_'em_in,_let_'em_in! 0 120 5 0 0 Y8".split(" "), "NINJA_LOOTER 0.3 60 decayMulti 0 W6item9 Liquid4 Blank Blank {x_Item_Find_chance_for_your_ninja_twin_while_sneaking! 1 1200 6 0 0 Y9ACTIVE".split(" "), "LO_COST_MO_JADE 99 40 decay 0 SpiD1 Liquid4 Blank Blank The_Jade_Cost_of_'Currency_Conduit'_scales_{%_slower,_making_it_cheaper,_allowing_you_to_buy_it_more_and_get_more_JADE! 0 2500 6 0 0 Y10".split(" "), "FASTER_NRG 20 100 decay 0 Tree14 Liquid4 Blank Blank +{%_faster_Stamina_Regeneration_for_Spelunking._Delve_fast,_delve_often. 0 1000 7 0 0 Y11".split(" "), "KATTLE_DA_GOAT 40 300 decay 0 W7item1 Liquid4 Blank Blank Kattlekruk,_who_took_literally_2.5yrs_after_being_released_to_let_you_have_his_bonus,_now_gives_+{%_more_Bubble_LVs_per_day. 0 10 8 0 0 Y12".split(" "), "CODFREY_RULZ_OK 5 500 decay 0 W7item2 Liquid4 Blank Blank +{%_higher_Gallery_Bonus_Multi._This_boosts_the_bonuses_from_both_Trophies_and_Nametags,_incase_you_didn't_know. 0 20 9 0 0 Y13".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 Y14".split(" "), "BUBBLE 99 40 decay 0 FillerMaterial Liquid4 Blank Blank It's_just_a_normal_bubble._It_doesn't_have_a_bonus_yet,_it_just_floats_and_is_round. 0 2500 6 0 0 Y15".split(" ")], ["COPPER_CORONA 3 0 add 0 Copper Liquid1 Blank Blank Orange_bubble_cauldron_brew_speed_is_increased_by_+{% 0 OrangeBrew".split(" "), "SIPPY_SPLINTERS 3 0 add 0 OakTree Liquid1 Blank Blank Green_bubble_cauldron_brew_speed_is_increased_by_+{% 1 GreenBrew".split(" "), "MUSHROOM_SOUP 3 0 add 0 Grasslands1 Liquid1 Blank Blank Yellow_cauldron_brew_speed_is_increased_by_+{% 3 YellowBrew".split(" "), "SPOOL_SPRITE 3 0 add 0 CraftMat1 Liquid1 Blank Blank Purple_cauldron_brew_speed_is_increased_by_+{% 2 PurpleBrew".split(" "), "BARIUM_MIXTURE 3 0 add 0 CopperBar Liquid1 Blank Blank +{_Water_Droplet_max_capacity._Thats_the_1st_liquid_type_in_Alchemy,_btw. 0 Liquid1Cap".split(" "), "DIETER_DRINK 1 0 add 0 Grasslands3 Liquid1 Blank Blank Monsters_drop_+{%_more_money. 1 MonsterCash".split(" "), "SKINNY_0_CAL 2.5 0 add 0 Jungle2 Liquid1 Blank Blank +{%_chance_to_get_double_points_when_depositing_statues._So_like..._if_you_deposit_one_statue,_it_might_count_as_one!_Or_two. 1 StatueDouble".split(" "), "THUMB_POW 1 0 add 0 CraftMat5 Liquid1 Blank Blank When_converting_Skill_EXP_into_Class_EXP_using_the_'EXP_CONVERTER'_star_talent,_you'll_get_{%_more_Class_EXP_than_you_usually_do. 0 ClassEXPconvert".split(" "), "JUNGLE_JUICE 1 0 add 0 JungleTree Liquid1 Blank Blank +{%_liquid_regen_rate_for_all_liquid_cauldrons._Yes,_even_the_secret_one! 4 LiquidRegen".split(" "), "BARLEY_BREW 1 0 add 0 IronBar Liquid1 Blank Blank Alchemy_bubble_upgrade_costs_are_{%_lower_for_all_bubbles!_Even_the_giraffe_bubbles_that_look_strangely_like_elephants! 4 AlchBubbleCost".split(" "), "ANEARFUL 2 0 add 0 Forest1 Liquid1 Blank Blank +{%_Card_drop_rate._Even_works_offline,_just_like_it_always_has!_What_do_you_mean_this_used_to_say_something_different...? 1 CardDrop".split(" "), "TEA_WITH_PEA 3 0 add 0 ToiletTree Liquid1 Blank Blank +{_Liquid_Nitrogen_max_capacity._Thats_the_2nd_liquid_type_in_Alchemy,_btw. 3 Liquid2Cap".split(" "), "GOLD_GUZZLE 1 0 add 0 Gold Liquid1 Blank Blank +{%_Shop_sell_price. 3 ShopSell".split(" "), "RAMIFICOCTION 1 0 add 0 Forest3 Liquid1 Blank Blank +{_Talent_Points_for_Tab_1._Shout_out_to_that_1_person_who'll_make_it_this_far_without_knowing_what_talents_are,_you're_my_hero! 3 Tab1Pts".split(" "), "SEAWATER 1 0 add 0 Fish1 Liquid1 Blank Blank +{%_chance_for_1_kill_to_count_for_2_when_trying_to_open_new_portals,_but_only_while_actively_playing._One,_two,_buckle_my_shoe. 3 MultiKillPlay".split(" "), "TAIL_TIME 0.5 0 add 0 Sewers2 Liquid1 Blank Blank +{_Weapon_Power._This_is_gonna_be_OP_in_later_worlds_I_can_already_tell. 0 WeaponPOW".split(" "), "FLY_IN_MY_DRINK 3 0 add 0 Bug1 Liquid1 Blank Blank Eww_go_get_me_another_one,_I_can't_drink_this!_...what,_why_are_you_looking_at_me_like_that?_OH_right,_uh,_this_gives_+{_base_Accuracy. 2 baseACC".split(" "), "MIMICRAUGHT 1 0 add 0 DesertA2 Liquid1 Blank Blank +{%_EXP_from_monsters._Sorry,_I_know_this_is_a_lame_bonus._Send_me_an_email_if_you_want_me_change_it_to_+{%_NPC_dialogue_talking_speed. 3 MonsterEXP".split(" "), "BLUE_FLAV 30 7 decay 0 Plat Liquid1 Blank Blank -{%_material_cost_for_stamps._You_know_how_it's_hard_to_increase_stamps_max_levels?_Well_this_kinda_makes_that_a_bit_less_factual! 4 MatCostStamp".split(" "), "SLUG_SLURP 2 0 add 0 Fish2 Liquid1 Blank Blank +{_Post_Office_Box_Points_for_every_character,_and_easily_the_best_bonus_in_the_game._A_box_will_never_abandon_you! 4 BoxPoints".split(" "), "PICKLE_JAR 50 0 add 0 BobJoePickle Liquid2 Blank Blank +{%_Nothing._Absolutely_nothing,_now_and_forever._It's_a_darn_pickle,_what_were_you_expecting? 1 Nothing".split(" "), "FUR_REFRESHER 2 0 add 0 SnowA1 Liquid2 Blank Blank +{%_higher_Shiny_Critter_chance._This_is_a_multiplier,_so_+1%_from_this_vial_means_1.01x,_so_5%_shiny_chance_would_go_to_5.05%. 0 Shiny1".split(" "), "SIPPY_SOUL 1 0 add 0 Soul1 Liquid2 Blank Blank +{_Talent_Points_for_Tab_2. 1 Tab2Pts".split(" "), "CRAB_JUICE 4 0 add 0 Critter2 Liquid2 Blank Blank +{_Starting_points_in_Worship_Tower_Defence._Of_course,_a_true_balloon_monkey_wouldn't_accept_handouts_like_this. 0 TDpts".split(" "), "VOID_VIAL 1 0 add 0 Void Liquid2 Blank Blank +{%_Mining_Efficiency. 0 MinEff".split(" "), "RED_MALT 1 0 add 0 Refinery1 Liquid2 Blank Blank +{%_Refinery_Cycle_Speed._I_just_want_to_see_you_squirm_a_bit_more_as_you_decide_where_to_spend_your_precious_salts_hahahaha!! 0 RefSpd".split(" "), "EW_GROSS_GROSS 1 0 add 0 Bug5 Liquid2 Blank Blank +{%_Catching_Efficiency. 4 CatchEff".split(" "), "THE_SPANISH_SAHARA 1 0 add 0 SaharanFoal Liquid2 Blank Blank +{%_Choppin_Efficiency. 4 ChopEff".split(" "), "POISON_TINCTURE 3 0 add 0 Critter1A Liquid2 Blank Blank Eagle_Eye_Trap-O-Vision_gives_+{%_more_critters. 2 TrapOvision".split(" "), "ETRUSCAN_LAGER 1 0 add 0 SnowB2 Liquid2 Blank Blank +{%_Fishing_Efficiency. 4 FishEff".split(" "), "CHONKER_CHUG 1 0 add 0 Soul2 Liquid2 Blank Blank +{%_Talent_Book_Library_checkout_speed. 3 TalBookSpd".split(" "), "BUBONIC_BURP 1 0 add 0 Critter4 Liquid3 Blank Blank +{_Cog_Inventory_spaces._DONT_PANIC!!!_I_KNOW_ITS_ALARMING_THAT_A_VIAL_FINALLY_GIVES_A_USEFUL_BONUS,_BUT_STAY_CALM! 4 CogInv".split(" "), "VISIBLE_INK 1 0 add 0 SnowB3 Liquid3 Blank Blank +{%_Construction_Exp_gain. 4 ConsExp".split(" "), "ORANGE_MALT 5 0 add 0 Refinery2 Liquid3 Blank Blank +{%_higher_Shiny_Critter_chance._This_stacks_with_the_shiny_chance_from_the_Fur_Refresher_vial._You_see,_they_have_the_same_shaped_vial. 0 Shiny2".split(" "), "SNOW_SLURRY 0.5 0 add 0 SnowB5 Liquid3 Blank Blank +{%_Printer_sample_size._My_my_there_are_a_lot_of_these_'sample_size'_bonuses_in_the_game..._too_many... 4 SampleSize".split(" "), "SLOWERGY_DRINK 1 0 add 0 Soul4 Liquid3 Blank Blank +{%_Base_Multikill_per_Multikill_Tier_for_all_worlds._Stack_them_skulls! 4 Overkill".split(" "), "SIPPY_CUP 1 0 add 0 SnowC1 Liquid3 Blank Blank +{%_Cog_production_speed. 4 CogSpd".split(" "), "BUNNY_BREW 1 0 add 0 Critter7 Liquid3 Blank Blank +{_Talent_Points_for_Tab_3. 2 Tab3Pts".split(" "), "40-40_PURITY 1 0 add 0 SnowC4 Liquid3 Blank Blank +{_Trench_Seawater_max_capacity._Thats_the_3rd_liquid_type_in_Alchemy,_btw. 4 Liquid3Cap".split(" "), "SHAVED_ICE 1 0 add 0 Refinery5 Liquid3 Blank Blank +{%_base_Giant_Monster_spawn_rate. 4 GiantMob".split(" "), "GOOSEY_GLUG 1 0 add 0 Critter9 Liquid3 Blank Blank +{_base_critter_per_trap._This_is_a_sHONKingly_good_bonus,_the_aren't_many_others_of_its_kind! 4 CritterBASED".split(" "), "BALL_PICKLE_JAR 25 0 add 0 BallJoePickle Liquid1 Blank Blank +{%_arcade_ball_gain_rate,_and_those_are_balls_blessed_by_Balljoepickle_himself,_so_you_know_they're_extra_lucky! 3 arcadeBALLZ".split(" "), "CAPACHINO 4 0 add 0 GalaxyA1 Liquid3 Blank Blank +{%_Breeding_EXP_gain 2 BreedXP".split(" "), "DONUT_DRINK 5 0 add 0 GalaxyA3 Liquid3 Blank Blank +{%_Chance_to_breed_a_new_pet._Multiplicative,_so_+5%_here_would_change_a_1_in_100_to_1_in_95_chance. 2 NewPet".split(" "), "LONG_ISLAND_TEA 6 0 add 0 Fish6 Liquid3 Blank Blank +{%_Meal_Cooking_Speed 3 MealCook".split(" "), "SPOOK_PINT 5 0 add 0 Soul5 Liquid3 Blank Blank +{%_New_Recipe_Cooking_Speed 2 RecCook".split(" "), "CALCIUM_CARBONATE 11 0 add 0 GalaxyB3 Liquid3 Blank Blank +{_Starting_Worship_Pts. 2 TDpts".split(" "), "BLOAT_DRAFT 3 0 add 0 Critter10 Liquid3 Blank Blank +{%_Lab_EXP_gain._Strange,_you'd_think_someone_dumb_enough_to_drink_a_bloated_blobfish_drink_wouldn't_get_bonus_lab_exp_at_all... 2 LabXP".split(" "), "CHOCO_MILKSHAKE 50 7 decay 0 GalaxyB4 Liquid3 Blank Blank -{%_Kitchen_Upgrading_Cost. 2 Kcosts".split(" "), "PEARL_SELTZER 0.5 0 add 0 GalaxyC1b Liquid3 Blank Blank +{%_All_Stats._If_you_don't_know_what_all_stats_means_by_now,_you've_prolly_got_bigger_problems_than_not_knowing_what_all_stats_means. 2 AllStatPCT".split(" "), "KRAKENADE 1 0 add 0 Fish8 Liquid3 Blank Blank +{_Weapon_Power._Unleash_the_kraken... 3 WeaponPOW".split(" "), "ELECTROLYTE 2 0 add 0 GalaxyC4 Liquid3 Blank Blank +{%_Pet_Team_Damage 2 PetDmg".split(" "), "ASH_AGUA 2 0 add 0 LavaA1 Liquid3 Blank Blank +{_Talent_Points_for_Tab_4 0 Tab4Pts".split(" "), "MAPLE_SYRUP 2 0 add 0 Tree9 Liquid3 Blank Blank +{%_Divinity_EXP._Maple_syrup_helps_you_keep_calm_and_meditate_with_the_divine..._No_wonder_those_Canadians_are_so_nice! 0 DivXP".split(" "), "HAMPTER_DRIPPY 2 0 add 0 LavaA5b Liquid3 Blank Blank +{%_Sailing_EXP_gain._Doesn't_help_level_up_captains,_only_yourself._So_yea,_I'm_basically_saying_you're_a_crappy_captain_lol 3 SailXP".split(" "), "DREADNOG 2 0 add 0 DreadloBar Liquid3 Blank Blank +{%_Cooking_Speed_for_meals._No,_MEALS,_not_meel,_dont_cook_him!!_Stop!!_STOP!!!! 0 MealCook".split(" "), "DUSTED_DRINK 2 0 add 0 Bug10 Liquid3 Blank Blank +{%_Gaming_EXP._Cool. 2 GameXP".split(" "), "OJ_JOOCE 2 0 add 0 LavaB3 Liquid3 Blank Blank +{%_Sailing_Speed._If_only_there_was_a_way_to_also_lower_the_minimum_sailing_time..._I'm_sure_you'll_find_it_eventually... 0 SailSpd".split(" "), "OOZIE_OOBLEK 2 0 add 0 Soul6 Liquid3 Blank Blank +{%_Bits_gained_in_Gaming._Cool. 0 GameBits".split(" "), "VENISON_MALT 2 0 add 0 LavaC2 Liquid3 Blank Blank -{%_material_cost_for_stamps._Have_at_it_endgamers! 2 MatCostStamp".split(" "), "MARBLE_MOCHA 5 0 add 0 Marble Liquid3 Blank Blank +{%_Faster_Equinox_Bar_Fill_Rate 3 EqBar".split(" "), "WILLOW_SIPPY 4 0 add 0 Tree11 Liquid3 Blank Blank +{%_Faster_Sigil_Charge_Rate 3 SigSpd".split(" "), "SHINYFIN_STEW 7 0 add 0 Fish13 Liquid3 Blank Blank +{%_Construction_Build_Rate,_so_you_can_hit_all_those_boosted_max_levels_you_keep_unlocking 3 Contspd".split(" "), "DREAMY_DRINK 3.5 0 add 0 Bug11 Liquid3 Blank Blank Shrines_charge_+{%_faster,_so_this_way_they_charge_faster,_compared_to_like_if_bonus_this_wasn't_oven_you_of_out_hot_eat_the_food. 3 ShrineSpd".split(" "), "RICECAKORADE 2 0 add 0 SpiA2 Liquid4 Blank Blank +{%_Farming_Speed,_so_the_plants_grow_faster._Makes_sense,_plants_do_get_energy_from_the_dumbest_things... 0 6FarmSpd".split(" "), "LADYBUG_SERUM 4 0 add 0 Bug12 Liquid4 Blank Blank +{%_White_Essence_gain,_and_before_you_make_an_angry_rant,_male_ladybugs_were_also_used_to_flavor_this_vial! 0 6WhiteEss".split(" "), "FLAVORGIL 7 0 add 0 Fish12 Liquid4 Blank Blank +{%_Farming_Crop_Evolution_chance._I_guess_like,_the_fishbits_mutate_with_the_crops?_Idk_I'm_not_a_planterman. 1 6FarmEvo".split(" "), "GREENLEAF_TEA 1.5 0 add 0 SpiB1 Liquid4 Blank Blank +{%_Ninja_Untying_rate._I_wonder_if_bomb_diffusers_drink_tea_before_going_to_work? 1 6Untie".split(" "), "FIREFLY_GROG 5 0 add 0 Bug13 Liquid4 Blank Blank +{%_Cooking_Speed,_but_multiplicative_so_it_stacks_big_time_with_the_other_892,314_cooking_bonuses_you_have! 0 6CookSpd".split(" "), "DABAR_SPECIAL 4 0 add 0 GodshardBar Liquid4 Blank Blank +{%_Total_Skill_efficiency,_but_not_multiplicative_so_that_it_drowns_in_the_sea_of_bonuses_you_already_have. 4 6SkillEff".split(" "), "REFRESHMENT 2 0 add 0 Soul7 Liquid4 Blank Blank +{%_Sneaking_EXP_gain._Something_about_it_makes_you_feel_light_on_your_feet,_as_if_u_just_wanna_fly... 0 6SneakEXP".split(" "), "GIBBED_DRINK 3.5 0 add 0 SpiC2 Liquid4 Blank Blank +{%_Summoning_EXP_gain._No,_the_horn_doesn't_contribute_to_the_flavor,_just_the_fleshy_bits_inside. 3 6SummEXP".split(" "), "DED_SAP 3.5 0 add 0 Tree13 Liquid4 Blank Blank +{%_Farming_EXP_gain,_but_dont_drink_too_much_since_Eucalyptus_oil_is_toxic_IRL_no_joke_fr_fr_search_it_or_just_take_my_word. 4 6FarmEXP".split(" "), "ROYALE_COLA 3.5 0 add 0 SpiD3 Liquid4 Blank Blank +{%_Jade_Gain_in_Sneaking._Congratulations_btw_on_trekking_through_World_6_like_that,_what_a_journey! 0 6Jade".split(" "), "TURTLE_TISANE 4 0 add 0 Critter11 Liquid4 Blank Blank +{%_Artifact_find_chance,_Sigil_SPD,_Cooking_SPD,_and_Construction_Build_rate._All_MULTIPLICATIVE!_A_very_special_vial_indeed... 0 6turtle".split(" "), "CHAPTER_CHUG 1 0 add 0 Spelunking0 Liquid4 Blank Blank +{%_Total_Damage_MULTIPLIER!_Yesss_multi_yeeeesss_I_know_how_it_is_I'm_chill_with_it 3 7dmg".split(" "), "SIPPY_SEAWEED 0.5 0 add 0 Tree14 Liquid4 Blank Blank +{%_faster_Spelunking_Speed..._like,_for_finding_chapter_pages_and_leveling_up! 1 7spelunkspd".split(" "), "WRIGGLE_WATER 1 0 add 0 w7A3 Liquid4 Blank Blank +{%_Spelunking_Amber_gain 1 7amber".split(" "), "ROCKY_BOBA 10 0 add 0 Prehistrium Liquid4 Blank Blank +{%_Gaming_Bits_multiplier!_Wait,_bits?_Gaming??_That's_not_very_World_7_of_you_mister_Prehistrium,_not_very_W7_of_you_at_all... 4 7bits".split(" "), "OCTOSODA 0.4 0 add 0 Soul8 Liquid4 Blank Blank +{%_AFK_Gains_rate_for_all_World_7_skills 2 7skillw7afk".split(" "), "PAPER_PINT 1 0 add 0 Spelunking2 Liquid4 Blank Blank +{%_extra_Masterclass_drops,_specifically_DB's_Bones,_WW's_Dust,_and_AC's_Tachyons!_We_love_our_acronyms_don't_we! 4 7masta".split(" "), "SCALE_ON_ICE 0.1 0 add 0 w7A5 Liquid4 Blank Blank +{%_daily_Coral_for_the_Coral_Reef!_I'm_a_bit_of_a_miserly_vial,_so_you'll_be_lucky_to_get_even_a_few_percent_from_me! 0 7corale".split(" "), "TRASH_DRANK 2 0 add 0 Bug15 Liquid4 Blank Blank +{%_Spelunking_Efficiency,_so_you_can_find_more_chapter_pages_and_help_solve_the_illiteracy_problem_that_plagues_our_community! 1 7spelunkeff".split(" "), "CRABOMAYSE 0.5 0 add 0 w7A12 Liquid4 Blank Blank +{%_Class_EXP_gain_MULTIPLIER!_What?_No,_don't_thank_Lava,_thank_ME!!!_I'm_the_one_giving_you_my_bonus! 0 7classexp".split(" ")], ["MEDIOCRE_OBOLS 1 1 0 2.2 Liquid1 Blank Blank Blank 1_random_low-quality_Obol._Sure,_it'll_probably_be_a_crappy_bronze_Obol,_but_that's_not_bad_considering_youre_paying_with_water! 0 10 0 0 0 1 1".split(" "), "WEAK_UPG_STONE 1 1 0 2.1 Liquid1 Blank Blank Blank `Slaps_roof_of_car`_This_bad_boy_can_upgrade_so_many_equipm..._wait,_how'd_a_car_get_in_here?_Gives_1_random_low-quality_Upgrade_Stone. 0 5 0 0 0 0 1".split(" "), "DISTILLED_WATER 1 1 0 1.37 Liquid1 Blank Blank Blank This_distilled_water_was_double-purified_by_running_it_through_thousands_of_diamonds!_So_yea,_it's_just_regular_water,_but_more_expensive. 4 1 0 0 0 0 1".split(" "), "ONE_MEASLY_GEM 1 1 0 7.5 Liquid1 Blank Blank Blank 1_Gem._Perfect_for_buying_things_in_the_Gem_Shop!_Sponsored_by_LavaFlame2's_Gem_Shop!' 4 5 0 0 0 0 1".split(" "), "STAR_BOOK 1 1 0 1.3 Liquid1 Blank Blank Blank Gives_you_a_Star-Book!_It's_always_the_same_one,_but_it_comes_with_a_random_Max_Lv,_so_keep_buying_it_until_you_get_one_with_a_100_Lv_Max! 3 50 0 0 0 0 1".split(" "), "EXP_BALLOON 1 1 0 2.8 Liquid1 Blank Blank Blank A_small_exp_balloon._They_give_you_exp_in_whatever_skill_you're_currently_training!_Using_them_in_town_will_give_EXP_in_the_town_skill! 1 15 0 0 0 0 1".split(" "), "SMALL_DONATION 1 0 1 2 Liquid1 Blank Blank Blank Your_donation_helps_starving_orphan_monsters._They_asked_for_food,_but_beggars_can't_be_choosers!_You_wont_get_anything_for_doing_this. 0 1 0 0 0 0 0".split(" "), "DECENT_OBOLS 1 1 0 2.5 Liquid1 Liquid2 Blank Blank 1_random_low-quality_Obol,_except_this_time_the_'low'_was_rated_by_someone_with_higher_standards,_so_it's_more_like_medium_quality! 4 20 3 0 0 1 1".split(" "), "TALENT_POINT;1;1;1;1.3;Liquid1;Liquid2;Blank;Blank;Gives_a_redeemable_talent_point_for_the_2nd_Talent Tab._Applies_to_all_characters._Also,_this_item's_cost_will_never_reset,_never_ever_ever!;1;3;1;0;0;0;0".split(";"), "GRAND_OBOLS 1 1 0 2.2 Liquid2 Liquid3 Blank Blank 1_random_Obol._It_could_be_a_super_rare_gold_obol,_but_it's_most_likely_gonna_be_a_bronze_obol. 3 5 3 0 0 1 1".split(" "), "BARGAIN_TAG 1 1 0 1.19 Liquid2 Liquid3 Blank Blank Lowers_the_cost_of_the_next_bubble_you_upgrade_by_25%!_Can_stack_multiple_times,_but_max_is_90%_off. 3 1 1 0 0 0 1".split(" "), "DENSE_WATER 1 1 0 1.37 Liquid3 Blank Blank Blank Sourced_from_the_bottom_of_the_Great_Trench,_dont_drink_this_or_you'll_become_dummy_thicc_or_whatever! 2 1 0 0 0 0 1".split(" "), "A_PAIR_OF_GEMS 1 2 0 8.5 Liquid3 Blank Blank Blank 2_Gems._Thats_two_steps_closer_to_buying_everything_in_Gem_Shop!_Sure_are_a_lot_of_steps_for_that_one_though... 4 5 0 0 0 0 1".split(" "), "EMPTY_SPACE 1 0 0 1 Liquid3 Blank Blank Blank There's_nothing_here_buddy,_but_that_ain't_gon_stop_me_from_selling_it_to_ya! 0 1 0 0 0 0 1".split(" "), "EMPTY_SPACE 1 0 0 1 Liquid3 Blank Blank Blank This_is_EXTRA_rare_nothing,_sure_ain't_going_for_cheap! 0 10 0 0 0 0 1".split(" "), "EMPTY_SPACE 1 0 0 1 Liquid3 Blank Blank Blank There's_nothing_here_buddy,_but_that_ain't_gon_stop_me_from_selling_it_to_ya! 0 1 0 0 0 0 1".split(" "), "EMPTY_SPACE 1 0 0 1 Liquid3 Blank Blank Blank There's_nothing_here_buddy,_but_that_ain't_gon_stop_me_from_selling_it_to_ya! 0 1 0 0 0 0 1".split(" "), "TALENT_POINT;1;1;1;1.27;Liquid3;Blank;Blank;Blank;Gives_a_redeemable_talent_point_for_the_3rd_Talent Tab._Applies_to_all_characters._This_item's_cost_will_reset_every_50,000,000_years.;4;3;0;0;0;0;0".split(";")]]

vials_dict = {
    index: {
        'Name': name.replace('_', ' ').title(),
        'Material': material,
        'x1': parse_number(x1),
        'x2': parse_number(x2),
        'funcType': funcType
    }
    for index, (name, x1, x2, funcType, pos4, material, liquid, pos7, pos8, description, pos10, codename) in enumerate(alchemy_description[4])
}
max_index_of_vials = len(vials_dict)
vials_considered_unmaxable = ['Poison Froge', 'Purple Salt', 'Pearler Shell', 'Hampter', 'BobJoePickle', 'BallJoePickle']
max_maxable_vials = max_index_of_vials - len(vials_considered_unmaxable)

# `AlchemyVialQTYreq` in source (though we don't actually copy that array because it's weirdly formatted and has more entries than possible levels).
# Last updated in v2.43 Nov 6
# Set the first element (Level 0) to 1 so we can set it as a `goal` in Advices
vial_costs = [1, 100, 1000, 2500, 10e3, 50e3, 100e3, 500e3, 1e6, 5e6, 25e6, 100e6, 1e9]
max_vial_level = len(vial_costs)

def getReadableVialNames(inputNumber):
    try:
        return f"{vials_dict[int(inputNumber)]['Name']} ({getItemDisplayName(vials_dict[int(inputNumber)]['Material'])})"
    except:
        return f"Unknown Vial {inputNumber}"


critter_vials_list = [
    getReadableVialNames(23),  #Crabbo
    getReadableVialNames(31),  #Mousey
    getReadableVialNames(37),  #Bunny
    getReadableVialNames(40),  #Honker
    getReadableVialNames(47),  #Blobfish
    getReadableVialNames(74),  #Tuttle
]

# `SigilDesc` in source. Last updated in v2.43 Nov 9
sigils_data = ["BIG_MUSCLE 2 100 10 20 filler Boosts_base_STR_by_+{ 50000 40 250000 100".split(" "), "PUMPED_KICKS 3 150 10 20 filler Boosts_base_AGI_by_+{ 60000 40 300000 100".split(" "), "ODD_LITEARTURE 5 200 10 20 filler Boosts_base_WIS_by_+{ 70000 40 400000 100".split(" "), "GOOD_FORTUNE 8 300 10 20 filler Boosts_base_LUK_by_+{ 90000 40 500000 100".split(" "), "PLUNGING_SWORD 15 700 75 225 filler Boosts_base_damage_by_+{ 100000 1000 600000 5000".split(" "), "WIZARDLY_HAT 24 1250 10 20 filler Boosts_Mana_Regeneration_by_+{%_both_inside_and_outside_of_dungeon 130000 30 700000 50".split(" "), "ENVELOPE_PILE 60 2500 12 25 filler Decreases_the_cost_of_upgrading_stamp_MAX_LEVELS_by_-{% 160000 40 1000000 65".split(" "), "SHINY_BEACON 120 4000 1 2 filler The_first_{_monster_kills_every_day_will_spawn_a_Crystal_Mob 200000 5 1400000 10".split(" "), "METAL_EXTERIOR 250 7000 6 12 filler Boosts_defence_by_nothing._Also_gives_+{%_Class_EXP 240000 20 1700000 50".split(" "), "TWO_STARZ 500 10000 10 25 filler Gives_+{_Star_Talent_points_to_spend_as_you_wish 280000 45 2200000 100".split(" "), "PIPE_GAUGE 700 12000 10 20 filler Increases_the_speed_of_refinery_cycles_by_+{% 320000 30 2600000 60".split(" "), "TROVE 1300 14000 10 20 filler Boosts_drop_rate_by_+{% 400000 30 3000000 100".split(" "), "PEA_POD 2100 15000 25 50 filler All_sigils_charge_{%_faster_than_normal 420000 100 3500000 450".split(" "), "TUFT_OF_HAIR 3000 25000 3 6 filler Boosts_movement_speed_by_+{%_if_under_175% 450000 10 4300000 15".split(" "), "EMOJI_VEGGIE 4500 33000 10 25 filler Boosts_the_bonus_of_all_golden_food_by_+{% 480000 40 5500000 60".split(" "), "VIP_PARCHMENT 6300 42000 10 25 filler Boosts_VIP_Membership_in_the_library_by_+{% 520000 50 6700000 100".split(" "), "DREAM_CATCHER 7000 50000 1 2 filler Boosts_all_Skill_AFK_gain_rates_by_+{% 560000 4 8200000 10".split(" "), "DUSTER_STUDS 8000 60000 3 7 filler Boosts_weapon_power_by_+{ 600000 15 10000000 25".split(" "), "GARLIC_GLOVE 9000 70000 15 35 filler Decreases_the_cost_of_all_kitchen_upgrades_by_-{% 650000 60 12000000 90".split(" "), "LAB_TESSTUBE 12000 80000 8 20 filler Boosts_Lab_EXP_gain_by_+{% 700000 35 14000000 70".split(" "), "PECULIAR_VIAL 17000 120000 15 25 filler Boosts_the_regeneration_rate_of_all_alchemy_liquids_by_+{% 750000 35 15000000 50".split(" "), "LOOT_PILE 23000 160000 10 20 filler All_sailing_treasure_chests_give_+{%_more_treasure! 900000 30 16000000 60".split(" "), "DIV_SPIRAL 26000 200000 10 30 filler Boosts_Divinity_EXP_gain_by_+{% 1200000 50 17000000 100".split(" "), "COOL_COIN 30000 250000 20 50 filler Boosts_Jade_Coin_gain_in_Sneaking_by_+{% 2000000 100 20000000 250".split(" ")]
sigil_name_overrides = {
    "VIP_PARCHMENT": "VIP Parchment" # .title() turns it to "Vip", but it's an acronym so we keep it uppercase
}
sigils_dict = {
    sigil_name_overrides.get(name, name.replace("_", " ").title()): {
        "Index": index * 2, # this is later used to parse player hours and player level from `raw_p2w_list`
        "PlayerHours": 0,
        "Level": 0,
        "PrechargeLevel": 0,
        "Requirements": [int(req1), int(req2), int(req3), int(req4)],
        "Values": [0, int(bon1), int(bon2), int(bon3), int(bon4)],
        "Description": description.replace("_", " ")
    }
    for index, (name, req1, req2, bon1, bon2, _, description, req3, bon3, req4, bon4) in enumerate(sigils_data)
}
max_sigil_level = len(list(sigils_dict.values())[0]['Values']) - 1

bubble_cauldron_color_list = ['Orange', 'Green', 'Purple', 'Yellow']
alchemy_liquids_list = ['Water Droplets', 'Liquid Nitrogen', 'Trench Seawater', 'Toxic Mercury']
alchemy_jobs_list = bubble_cauldron_color_list + alchemy_liquids_list + [k for k in sigils_dict.keys()]
min_NBLB = 2
max_NBLB = 1500
nblb_max_index = 24
nblb_skippable = [
    'Reely Smart', 'Bappity Boopity', 'Orange Bargain', 'Bite But Not Chew',  #Orange
    'Lil Big Damage', 'Anvilnomics', 'Cheap Shot', 'Green Bargain', 'Kill Per Kill',  #Green
    'Noodubble', 'Purple Bargain', 'Matrix Evolved',  #Purple
    'Yellow Bargain', 'Petting The Rift',  #Yellow
]
bubble_name_overrides = {
    0: {
        'FMJ': 'FMJ',
        'ESSENCE_BOOST': 'Essence Boost-Orange'
    },
    1: {
        'BUG]': 'Bug^2',
        'ESSENCE_BOOST': 'Essence Boost-Green',
        'ENDGAME_EFF_II': 'Endgame Eff II',
    },
    2: {
        'ESSENCE_BOOST': 'Essence Boost-Purple',
        'ENDGAME_EFF_III': 'Endgame Eff III',
    },
    3: {
        'ESSENCE_BOOST': 'Essence Boost-Yellow'
    }
}
bubbles_dict = {
    cauldron_index: {
        index: {
            'Name': bubble_name_overrides[cauldron_index].get(name, name.replace('_', ' ').title()),
            'Material': material,
            'x1': parse_number(x1),
            'x2': parse_number(x2),
            'funcType': funcType
        }
        for index, (name, x1, x2, funcType, pos4, material, liquid, pos7, pos8, description, pos10, pos11, pos12, pos13, pos14, codename)
        in enumerate(alchemy_description[cauldron_index]) if name != 'BUBBLE'  #exclude placeholders
    }
    for cauldron_index in range(0, len(bubble_cauldron_color_list))  #exclude vials and the water shop
}
max_implemented_bubble_index = max(bubbles_dict[0].keys())

def getReadableBubbleNames(inputNumber, color):
    try:
        return bubbles_dict[bubble_cauldron_color_list.index(color)][inputNumber]
    except:
        return f"Unknown {color} Bubble {inputNumber}"


at_risk_basic_bubbles = [
    "Roid Ragin",
    "Hearty Diggy",
    "Wyoming Blood",
    "Sploosh Sploosh",
    "Stronk Tools",
    "FMJ",
    "Swift Steppin",
    "Hammer Hammer",
    "Lil Big Damage",
    "Anvilnomics",
    "Bug^2",
    "Shaquracy",
    "Cheap Shot",
    "Call Me Ash",
    "Fast Boi Talent",
    "Stable Jenius",
    "Name I Guess",
    "Le Brain Tools",
    "Cookin Roadkill",
    "All For Kill",
    "Gospel Leader",
    "Droppin Loads",
    "Prowesessary",
    "Stamp Tramp",
    "Undeveloped Costs",
    "Laaarrrryyyy",
    "Ignore Overdues",
]  #Standard log, ore, fish, bug prints in W1-W3 bubbles
atrisk_advanced_bubbles = [
    'Warriors Rule', 'Big Meaty Claws', 'Call Me Bob', 'Brittley Spears', 'Buff Boi Talent', 'Orange Bargain',
    'Archer Or Bust', 'Quick Slap', 'Sanic Tools', 'Bow Jack', 'Cuz I Catch Em All', 'Green Bargain',
    'Mage Is Best', 'Hocus Choppus', 'Molto Loggo', 'Brewstachio', 'Call Me Pope', 'Smart Boi Talent', 'Purple Bargain',
    'Lotto Skills', 'Startue Exp', 'Level Up Gift', 'Grind Time', 'Cogs For Hands', 'Sample It', 'Big Game Hunter', 'Yellow Bargain',
]  #Advanced being anvil mats, monster mats, critters, souls in W1-W3 bubbles
atrisk_lithium_bubbles = [
    'Penny Of Strength',
    'Fly In Mind', 'Afk Expexp', 'Slabo Critterbug',
    'Nickel Of Wisdom', 'Severapurple', 'Hyperswift', 'Matrix Evolved', 'Slabe Logsoul',
    'Bit By Bit', 'Gifts Abound',
]  #Standard log, ore, fish, bug prints in W4+ bubbles
atrisk_lithium_advanced_bubbles = [
    'Multorange', 'Bite But Not Chew', 'Slabi Orefish', 'Gamer At Heart',
    'Premigreen', 'Sailor At Heart', 'Slabo Agility',
    'Tree Sleeper', 'Pious At Heart', 'Slabe Wisdom', 'Essence Boost-Purple',
    'Petting The Rift', 'Big P', 'Atom Split'
]  #Advanced being anvil mats, monster mats, critters, souls, sailing treasures in W4+ bubbles

# `ArcadeShopInfo` in source. Last updated in v2.43 Nov 6
arcade_shop_info = ["+{_Base_Damage 1 0 add _ +{_Dmg -1".split(" "), "+{_Base_Defence 0.2 0 add _ +{_Def -1".split(" "), "+{%_Total_Accuracy 60 100 decay _ +{%_Acc -1".split(" "), "+{%_Mining_EXP_gain 60 100 decay % +{%_Min_EXP -1".split(" "), "+{%_Fishing_EXP_gain 60 100 decay % +{%_Fish_EXP -1".split(" "), "+{%_Sample_Size 4 100 decay % +{%_Size -1".split(" "), "+{%_AFK_Gains_Rate 4 100 decay % +{%_Rate -1".split(" "), "+{_Cap_for_all_Liquids 25 100 decay % +{_Cap -1".split(" "), "+{%_Multikill_per_Tier 10 100 decay % +{%_Multikill -1".split(" "), "+{%_Catching_EXP_gain 50 100 decay % +{%_Catch_EXP -1".split(" "), "+{%_Cash_from_Mobs 20 100 decay % +{%_Cash -1".split(" "), "+{%_Cash_from_Mobs 30 100 decay % +{%_Cash -1".split(" "), "+{%_Class_EXP_gain 20 100 decay % +{%_EXP -1".split(" "), "+{%_Shiny_Chance 100 100 decay % +{%_Chance -1".split(" "), "+{%_Trapping_EXP 50 100 decay % +{%_Trap_EXP -1".split(" "), "+{_Starting_TD_Pts 1 0 add _ +{_Worship_Pts -1".split(" "), "+{_Tab_1_Talent_Pt 1 10 intervalAdd _ +1_Pt_per_10_LVs -1".split(" "), "+{_Weapon_Power 0.07 0 add _ +{_Wep_POW -1".split(" "), "+{%_Skill_EXP_gain 20 100 decay % +{%_EXP -1".split(" "), "+{_Base_STR 1 0 add _ +{_STR -1".split(" "), "+{_Base_AGI 1 0 add _ +{_AGI -1".split(" "), "+{_Base_WIS 1 0 add _ +{_WIS -1".split(" "), "+{_Base_LUK 1 0 add _ +{_LUK -1".split(" "), "+{%_Trapping_Critters 30 100 decay % +{%_Critters -1".split(" "), "+{%_Worship_Souls 30 100 decay % +{%_Souls -1".split(" "), "+{%_Refinery_Speed 30 100 decay % +{%_Speed -1".split(" "), "+{%_Forge_Capacity 100 100 decay % +{%_Cap -1".split(" "), "+{%_Drop_Rate 30 100 decay % +{%_Drop -1".split(" "), "+{%_Cook_SPD_multi 40 100 decay % +{%_SPD -1".split(" "), "+{%_Lab_EXP_gain 30 100 decay % +{%_EXP -1".split(" "), "+{%_Breed_Pet_DMG 40 100 decay % +{%_DMG -1".split(" "), "+{%_Nugget_Regen 30 100 decay % +{%_Regen -1".split(" "), "+{%_Artifact_Find 50 100 decay % +{%_Chance -1".split(" "), "+{%_Sailing_Loot 30 100 decay % +{%_Loot -1".split(" "), "+{%_W_Ess_gain 40 100 decay % +{%_W_Ess -1".split(" "), "+{%_Jade_gain 50 100 decay % +{%_Jade -1".split(" "), "+{%_Farming_EXP 30 100 decay % +{%_EXP -1".split(" "), "+{%_Divinity_EXP 40 100 decay % +{%_EXP -1".split(" "), "+{%_Villager_XP_multi 40 100 decay % +{%_XP_multi -1".split(" "), "+{%_Gold_Ball_Gain 1 0 add % +{%_Balls -1".split(" "), "+{%_Deathbringer_Bones 1 0 add % +{%_Bones -1".split(" "), "+{%_Equinox_Fill_Rate .75 0 add % +{%_Fill_Rate -1".split(" "), "+{%_Monument_AFK .5 0 add % +{%_AFK -1".split(" "), "+{%_Sigil_Speed 1 0 add % +{%_Speed -1".split(" "), "+{%_Construction_Build 2 0 add % +{%_Build_Rate -1".split(" "), "+{%_Burger 1 0 add % +{%_Burger -1".split(" "), "+{%_Total_Damage 2 0 add % +{%_Damage -1".split(" "), "+{%_Windwalker_Dust 1 0 add % +{%_Dust -1".split(" "), "+{%_Medallion_Chance 0.5 0 add % +{%_Chance -1".split(" "), "+{%_Breedability_Rate 100 100 decay % +{%_Breed_Rate -1".split(" "), "+{%_Arcane_Tachyons 1 0 add % +{%_Tachyons 17".split(" "), "+{%_Emperor_Bonuses 0.2 0 add % +{%_Bonus 42".split(" "), "+{%_Sneaking_XP_multi 100 100 decay % +{%_XP_multi 29".split(" "), "+{%_Summon_XP_multi 100 100 decay % +{%_XP_multi 23".split(" "), "+{%_Prisma_Bonuses 10 100 decay % +{%_Bonus 21".split(" "), "+{%_Spelunking_Amber 50 100 decay % +{%_Amber 28".split(" "), "+{%_Spelunk_XP_multi 30 100 decay % +{%_XP_multi 39".split(" "), "+{%_Daily_Coral 10 100 decay % +{%_Coral 41".split(" "), "+{%_Palette_Luck 50 100 decay % +{%_Luck 42".split(" "), "+{%_Meritocracy_Bonus 10 100 decay % +{%_Bonus 31".split(" "), "+{%_Class_XP_multi 50 100 decay % +{%_XP_multi 31".split(" "), "+{%_Kruk_Bubble_LVs 40 100 decay % +{%_Bubble_LV 22".split(" ")]
arcade_stat_name_overrides = {
    'Shiny Chance': 'Shiny Critter Chance',
    'Cook SPD multi': 'Cooking Speed multi',
    'Breed Pet DMG': 'Breeding Pet DMG',
    'Nugget Regen': 'Nugget Generation',
    'Artifact Find': 'Artifact Find Chance',
    'W Ess gain': 'White Essence gain',
    'Gold Ball Gain': 'Gold Ball gain',
    'Deathbringer Bones': 'Death Bringer Bones',
    'Construction Build': 'Construction Build Rate',
    'Burger': 'Burger (does nothing atm)',
    'Windwalker Dust': 'Wind Walker Dust',
    'Arcane Tachyons': 'Arcane Cultist Tachyons',
    'Summon XP multi': 'Summoning XP multi',
    'Prisma Bonuses': 'Prisma Bubble Bonus',
}
arcade_bonuses = {
    index: {
        'Stat': arcade_stat_name_overrides.get(" ".join(stat_code.split("_")[1:]), " ".join(stat_code.split("_")[1:])),
        'x1': parse_number(x1),
        'x2': parse_number(x2),
        'funcType': func_type,
        'displayType': '%' if stat_code.split("_")[0][-1] == '%' else ''
    } for index, [stat_code, x1, x2, func_type, _, _, _] in enumerate(arcade_shop_info)
}
arcade_max_level = 100
post_office_tabs = ["Bob's Boxes", "Charlie's Crates"]
#po_box_dict last taken from code in 2.09: #PostOffUpgradeInfo = function ()
#Translate using the Post Office tab in AR spreadsheet
po_box_dict = {
    0: {
        'Name': 'Civil War Memory Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 1, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Damage',
        '2_funcType': 'decay', '2_x1': 13, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Fight AFK Gains', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 10, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critical Chance', '3_minCount': 100,
    },
    1: {
        'Name': 'Locally Sourced Organs', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 2, '1_pre': '', '1_post': '', '1_stat': 'Base Max HP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max HP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Respawns', '3_minCount': 100,
    },
    2: {
        'Name': 'Magician Starterpack', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'intervalAdd', '1_x1': 1, '1_x2': 3, '1_pre': '', '1_post': '', '1_stat': 'Base Max MP',
        '2_funcType': 'add', '2_x1': 0.1, '2_x2': 0, '2_pre': '', '2_post': '%', '2_stat': 'Max MP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 17, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Faster Cooldowns', '3_minCount': 100,
    },
    3: {
        'Name': 'Box of Unwanted Stats', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Base Accuracy',
        '2_funcType': 'add', '2_x1': 0.3, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'Base Defence', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 29, '3_x2': 170, '3_pre': '', '3_post': '%', '3_stat': 'Monster EXP', '3_minCount': 100,
    },
    4: {
        'Name': 'Dwarven Supplies', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Mining Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Mining AFK Gain', '3_minCount': 100,
    },
    5: {
        'Name': 'Blacksmith Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Smithing EXP',
        '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Production Speed', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 150, '3_pre': '', '3_post': '%', '3_stat': 'to Craft +1 Slot', '3_minCount': 100,
    },
    6: {
        'Name': 'Taped Up Timber', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Choppin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Choppin AFK Gain', '3_minCount': 100,
    },
    7: {
        'Name': 'Carepack From Mum', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 23, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Not Consume Food',
        '2_funcType': 'decay', '2_x1': 30, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Health Food Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Boost Food Effect', '3_minCount': 100,
    },
    8: {
        'Name': 'Sealed Fishheads', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Fishin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Fishin AFK Gain', '3_minCount': 100,
    },
    9: {
        'Name': 'Potion Package', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 70, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Brewing Speed',
        '2_funcType': 'decay', '2_x1': 60, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Alchemy EXP', '2_minCount': 25,
        '3_funcType': 'add', '3_x1': 0.1, '3_x2': 0, '3_pre': '', '3_post': '', '3_stat': 'Cranium Cook Time', '3_minCount': 100,
    },
    10: {
        'Name': 'Bug Hunting Supplies', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Catchin Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Prowess Effect', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 175, '3_pre': '', '3_post': '%', '3_stat': 'Catchin AFK Gain', '3_minCount': 100,
    },
    11: {
        'Name': 'Non Predatory Loot Box', 'Tab': post_office_tabs[0], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Drop Rarity',
        '2_funcType': 'add', '2_x1': 0.25, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'LUK', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 65, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Crystal Mob Spawn', '3_minCount': 100,
    },
    12: {
        'Name': 'Deaths Storage Unit', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 22, '1_x2': 200, '1_pre': '', '1_post': '', '1_stat': 'Weapon Power',
        '2_funcType': 'decay', '2_x1': 15, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Basic Atk Speed', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 15, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 100,
    },
    13: {
        'Name': 'Utilitarian Capsule', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 5, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Printer Sample Size',
        '2_funcType': 'decay', '2_x1': 15, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Multikill per Tier', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 39, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Cash from Mobs', '3_minCount': 100,
    },
    14: {
        'Name': 'Lazzzy Lootcrate', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 30, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': '2X AFK XP chance',
        '2_funcType': 'decay', '2_x1': 35, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'AFK exp if 36hr+', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 35, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'AFK Cash if 36hr+', '3_minCount': 100,
    },
    15: {
        'Name': 'Science Spare Parts', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Lab Efficiency',
        '2_funcType': 'decay', '2_x1': 40, '2_x2': 150, '2_pre': '', '2_post': '%', '2_stat': 'Lab EXP gain', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Base LUK', '3_minCount': 100,
    },
    16: {
        'Name': 'Trapping Lockbox', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Trapping Efficiency',
        '2_funcType': 'decay', '2_x1': 50, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Trapping EXP', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 45, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'Critters Trapped', '3_minCount': 100,
    },
    17: {
        'Name': 'Construction Container', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 0.25, '1_x2': 0, '1_pre': '', '1_post': '%', '1_stat': 'Base Build Rate',
        '2_funcType': 'decay', '2_x1': 75, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Shrine Charge Rate', '2_minCount': 25,
        '3_funcType': 'add', '3_x1': 0.5, '3_x2': 0, '3_pre': '', '3_post': '%', '3_stat': 'Construction EXP', '3_minCount': 100,
    },
    18: {
        'Name': 'Crate of the Creator', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'decay', '1_x1': 50, '1_x2': 200, '1_pre': '', '1_post': '%', '1_stat': 'Worship Efficiency',
        '2_funcType': 'decay', '2_x1': 200, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Max Charge', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 90, '3_x2': 200, '3_pre': '', '3_post': '', '3_stat': 'Starting Worship Pts', '3_minCount': 100,
    },
    19: {
        'Name': 'Chefs Essentials', 'Tab': post_office_tabs[1], 'Max Level': 400,
        '1_funcType': 'add', '1_x1': 4, '1_x2': 0, '1_pre': '', '1_post': '', '1_stat': 'Cooking Efficiency',
        '2_funcType': 'decay', '2_x1': 60, '2_x2': 200, '2_pre': '', '2_post': '%', '2_stat': 'Cooking EXP gain', '2_minCount': 25,
        '3_funcType': 'decay', '3_x1': 88, '3_x2': 200, '3_pre': '', '3_post': '%', '3_stat': 'for 2x Ladle Drop', '3_minCount': 100,
    },
    20: {
        'Name': 'Myriad Crate', 'Tab': post_office_tabs[1], 'Max Level': 100000,
        '1_funcType': 'decay', '1_x1': 400, '1_x2': 20000, '1_pre': '', '1_post': '', '1_stat': 'Base All Stat',
        '2_funcType': 'decay', '2_x1': 1000, '2_x2': 20000, '2_pre': '', '2_post': '', '2_stat': 'Base All Efficiency', '2_minCount': 100,
        '3_funcType': 'decay', '3_x1': 100, '3_x2': 20000, '3_pre': '', '3_post': '%', '3_stat': 'All Skills exp', '3_minCount': 300,
    },
    21: {
        'Name': "Scurvy C'arr'ate", 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 8, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for sailing',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'AGI', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200,
    },
    22: {
        'Name': 'Box of Gosh', 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 75, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'Divinity EXP',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'WIS', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 30, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Divinity Gain', '3_minCount': 200,
    },
    23: {
        'Name': 'Gaming Lootcrate', 'Tab': post_office_tabs[1], 'Max Level': 800,
        '1_funcType': 'decay', '1_x1': 14, '1_x2': 400, '1_pre': '', '1_post': '%', '1_stat': 'afk counts for gaming',
        '2_funcType': 'add', '2_x1': 0.2, '2_x2': 0, '2_pre': '', '2_post': '', '2_stat': 'STR', '2_minCount': 50,
        '3_funcType': 'decay', '3_x1': 25, '3_x2': 400, '3_pre': '', '3_post': '%', '3_stat': 'Total Damage', '3_minCount': 200,
    },
}
max_po_box_before_myriad = sum([v['Max Level'] for v in po_box_dict.values() if v['Name'] != 'Myriad Crate'])
max_po_box_after_myriad = max_po_box_before_myriad + po_box_dict[20]['Max Level']
ballot_dict = {
    0:  {'BaseValue': 25, 'Description': "All your characters deal }x more damage to enemies", 'Image': "ballot-1"},
    1:  {'BaseValue': 25, 'Description': "All your characters deal }x more damage to enemies", 'Image': "ballot-1"},
    2:  {'BaseValue': 15, 'Description': "Increases STR AGI WIS and LUK for all characters by {%", 'Image': "ballot-2"},
    3:  {'BaseValue': 30, 'Description': "Increases Defence and Accuracy by +{% for all characters", 'Image': "ballot-3"},
    4:  {'BaseValue': 30, 'Description': "Logging in each day gives +{ more GP to your guild than you normally do", 'Image': "ballot-4"},
    5:  {'BaseValue': 20, 'Description': "}x Kill per Kill, making monster kills worth more for portals and deathnote", 'Image': "ballot-5"},
    6:  {'BaseValue': 15, 'Description': "{% AFK gain for both fighting and skills for all characters", 'Image': "ballot-6"},
    7:  {'BaseValue': 42, 'Description': "Boosts all Mining EXP gain and Mining Efficiency by +{%", 'Image': "ballot-7"},
    8:  {'BaseValue': 50, 'Description': "Boosts all Fishing EXP gain and Fishing Efficiency by +{%", 'Image': "ballot-8"},
    9:  {'BaseValue': 38, 'Description': "Boosts all Chopping' EXP gain and Choppin' Efficiency by +{%", 'Image': "ballot-9"},
    10: {'BaseValue': 46, 'Description': "Boosts all Catching EXP gain and Catching Efficiency by +{%", 'Image': "ballot-10"},
    11: {'BaseValue': 20, 'Description': "Increases the amount of resources produced by the 3D printer by }x", 'Image': "ballot-11"},
    12: {'BaseValue': 25, 'Description': "Boosts liquid generation rate for all Alchemy liquids by +{%", 'Image': "ballot-12"},
    13: {'BaseValue': 63, 'Description': "Boosts all Cooking EXP gain and Cooking speed by +{%", 'Image': "ballot-13"},
    14: {'BaseValue': 50, 'Description': "Boosts Dungeon Credit and Dungeon Flurbo gain by }x", 'Image': "ballot-14"},
    15: {'BaseValue': 60, 'Description': "All your characters gain +{% more class EXP from monsters", 'Image': "ballot-15"},
    16: {'BaseValue': 50, 'Description': "Speeds up Egg incubation and Breeding EXP gain by +{%", 'Image': "ballot-16"},
    17: {'BaseValue': 80, 'Description': "Boosts Sigil EXP gain by }x, still requires Sigils active in Lab", 'Image': "ballot-17"},
    18: {'BaseValue': 40, 'Description': "Boosts Construction Build Rate and Construction EXP gain by +{%", 'Image': "ballot-18"},
    19: {'BaseValue': 53, 'Description': "Boosts Shrine EXP gain by a staggering }x", 'Image': "ballot-19"},
    20: {'BaseValue': 31, 'Description': "Boosts Artifact Find Chance in Sailing by }x", 'Image': "ballot-20"},
    21: {'BaseValue': 80, 'Description': "Boosts New Species chance when using DNA in gaming by }x", 'Image': "ballot-21"},
    22: {'BaseValue': 75, 'Description': "Find +{% more gold Nuggets when digging with the shovel in gaming", 'Image': "ballot-22"},
    23: {'BaseValue': 60, 'Description': "Boosts Divinity PTS gain by }x and Divinity EXP gain by +{%", 'Image': "ballot-23"},
    24: {'BaseValue': 50, 'Description': "Boosts Sailing Captain EXP gain and Sailing Speed by }x", 'Image': "ballot-24"},
    25: {'BaseValue': 65, 'Description': "Boosts Sneaking Stealth by }x and EXP gain by +{% for all your Ninja Twins", 'Image': "ballot-25"},
    26: {'BaseValue': 30, 'Description': "Boosts bonuses from all Golden food by +{%", 'Image': "ballot-26"},
    27: {'BaseValue': 38, 'Description': "Increases Drop Rate for all your characters by +{%", 'Image': "ballot-27"},
    28: {'BaseValue': 40, 'Description': "Boosts Summoning EXP gain by +40% and all Essence gained by }x", 'Image': "ballot-28"},
    29: {'BaseValue': 40, 'Description': "Boosts Crop Value, and Farming EXP gain, AND Next Crop Chance by +{%", 'Image': "ballot-29"},
    30: {'BaseValue': 45, 'Description': "Increases Trapping EXP gain and Worship EXP gain by +{%", 'Image': "ballot-30"},
    31: {'BaseValue': 90, 'Description': "Increases Lab EXP gain by +{%", 'Image': "ballot-31"},
    32: {'BaseValue': 40, 'Description': "Boosts Equinox Bar Fill rate by }x", 'Image': "ballot-32"},
    33: {'BaseValue': 50, 'Description': "Boosts Refinery Cycle Speed by +{%", 'Image': "ballot-33"},
    34: {'BaseValue': 52, 'Description': "Increases cash earned from monsters by +{%", 'Image': "ballot-34"},
}
fishing_toolkit_dict = {
    'Lures': [f"Weight{i}" for i in range(1, 15)],
    'Lines': [f"Line{i}" for i in range(1, 15)]
}
obols_dict = {
    #Drop Rate
    "ObolBronzePop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolBronzePop"), 'Base': {'LUK': 1, 'DEF': 1, '%_DROP_CHANCE': 2}},
    "ObolSilverPop":    {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverPop"), 'Base': {'LUK': 3, 'DEF': 2, '%_DROP_CHANCE': 3}},
    "ObolHyper0":       {"Shape": "Circle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0"), 'Base': {'WP': 1, '%_DROP_CHANCE': 4}},
    "ObolSilverLuck":   {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolSilverLuck"), 'Base': {'LUK': 2, '%_DROP_CHANCE': 5}},
    "ObolGoldLuck":     {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolGoldLuck"), 'Base': {'LUK': 3, '%_DROP_CHANCE': 7}},
    "ObolKnight":       {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolKnight"), 'Base': {'WP': 2, 'STR': 3, 'AGI': 3, 'WIS': 3, 'LUK': 3, 'DEF': 5, '%_DROP_CHANCE': 8}},
    "ObolHyperB0":      {"Shape": "Square", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolHyper0"), 'Base': {'WP': 5, '%_DROP_CHANCE': 10}},
    "ObolPlatinumLuck": {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPlatinumLuck"), 'Base': {'LUK': 5, '%_DROP_CHANCE': 10}},
    "ObolLava":         {"Shape": "Hexagon", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolLava"), 'Base': {'LUK': 10, '%_DROP_CHANCE': 14}},
    "ObolPinkLuck":     {"Shape": "Sparkle", "Bonus": "Drop Rate", "DisplayName": getItemDisplayName("ObolPinkLuck"), 'Base': {'LUK': 7, '%_DROP_CHANCE': 15}},

    #Card Drop Chance
    "ObolBronzeCard":   {"Shape":"Circle", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolBronzeCard"), "Base": {"%_CARD_DROP_CHANCE": 1}},
    "ObolSilverCard":   {"Shape": "Square", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolSilverCard"), "Base": {"%_CARD_DROP_CHANCE": 3, "STR": 1, "AGI": 1, "WIS": 1}},
    "ObolGoldCard":     {"Shape": "Hexagon", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolGoldCard"), "Base": {"%_CARD_DROP_CHANCE": 5, "STR": 2, "AGI": 2, "WIS": 2}},
    "ObolPlatinumCard": {"Shape": "Hexagon", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolPlatinumCard"), "Base": {"%_CARD_DROP_CHANCE": 7, "STR": 3, "AGI": 3, "WIS": 3}},
    "ObolPinkCard":     {"Shape": "Sparkle", "Bonus": "Card Drop Chance", "DisplayName": getItemDisplayName("ObolPinkCard"), "Base": {"%_CARD_DROP_CHANCE": 10, "STR": 5, "AGI": 5, "WIS": 5, "WP": 1}},
}
obols_max_bonuses_dict = {
    'PlayerDropRatePractical': 134,         #12*4=48% circles, 6*8=48% squares,  2*11=22% hex, 1*16=16% sparkle
    'PlayerDropRateTrue': 172,              #12*5=60% circles, 6*11=66% squares, 2*15=30% hex, 1*16=16% sparkle
    'FamilyDropRatePractical': 188,         #12*4=48% circles, 4*8=32% squares,  4*11=44% hex, 4*16=64% sparkle
    'FamilyDropRateTrue': 228,              #12*5=60% circles, 4*11=44% squares, 4*15=60% hex, 4*16=64% sparkle

    'PlayerCardDropChancePractical': 75,    #12*2=24% circles, 6*4=24% square, 2*8=16% hex, 1*11=11% sparkle
    'PlayerCardDropChanceTrue': 75 ,        #12*2=24% circles, 6*4=24% square, 2*8=16% hex, 1*11=11% sparkle
    'FamilyCardDropChancePractical': 116,   #12*2=24% circles, 4*4=16% square, 4*8=32% hex, 4*11=44% sparkle
    'FamilyCardDropChanceTrue': 116         #12*2=24% circles, 4*4=16% square, 4*8=32% hex, 4*11=44% sparkle
}
ignorable_obols_list = [
    'Blank', 'LockedInvSpace', 'ObolLocked1', 'ObolLocked2', 'ObolLocked3', 'ObolLocked4',
]
islands_dict = {
    'Trash Island':     {'Code': '_', 'Description': 'Trade garbage that washs up each day for items',},
    'Rando Island':     {'Code': 'a', 'Description': 'Guaranteed Random Event once a week',},
    'Crystal Island':   {'Code': 'b', 'Description': 'Fight daily giant crystal mobs that drop candy',},
    'Seasalt Island':   {'Code': 'c', 'Description': 'Catch legendary fish for crafting World 6 equips',},
    'Shimmer Island':   {'Code': 'd', 'Description': 'Do Weekly Challenges for Shimmer Upgrades',},
    'Fractal Island':   {'Code': 'e', 'Description': 'Dump your time candy here for... nothing...?',},
}
islands_trash_shop_costs = {
    'Skelefish Stamp': 20,
    'Amplestample Stamp': 40,
    'Golden Sixes Stamp': 80,
    'Stat Wallstreet Stamp': 300,
    'Unlock New Bribe Set': 135,
    'Filthy Damage Special Talent Book': 450,
    'Trash Tuna Nametag': 1500
}
islands_fractal_rewards_dict = {
    24: {'Reward': '1 in 100000 chance for Master of Nothing Trophy per hour of Nothing AFK', 'Image': 'master-of-nothing'},
    200: {'Reward': '1.25x Dungeon Credits and Flurbos gained', 'Image': 'ballot-14'},
    750: {'Reward': '-30% Kitchen Upgrade Costs', 'Image': 'cooking-table'},
    2500: {'Reward': '1.20x Chance to find Sailing Artifacts', 'Image': 'artifact-find-chance'},
    10e3: {'Reward': 'Dirty Shovel digs up +25% more Gold Nuggets', 'Image': 'dirty-shovel'},
    20e3: {'Reward': '+100 Star Talent Pts', 'Image': 'star-talent-icon'},
    40e3: {'Reward': 'All Ninja twins get +2% Stealth per Sneaking level', 'Image': 'sneaking'},
    60e3: {'Reward': 'World 7 Bonus... I wonder what it will be...', 'Image': 'rift-tbd'},
}
killroy_dict = {
    'Timer': {
        'Required Fights': 0,
        'Required Equinox': 0,
        'UpgradesIndex': 106,
        'Image': 'killroy-timer'
    },
    'Talent Points': {
        'Required Fights': 2,
        'Required Equinox': 0,
        'UpgradesIndex': 107,
        'Image': 'killroy-talent-points'},
    'Skulls': {
        'Required Fights': 16,
        'Required Equinox': 0,
        'UpgradesIndex': 108,
        'Image': 'killroy-skulls'
    },
    'Respawn': {
        'Required Fights': 36,
        'Required Equinox': 1,
        'UpgradesIndex': 109,
        'Image': 'killroy-respawn'
    },
    'Dungeon Credits': {
        'Required Fights': 64,
        'Required Equinox': 2,
        'UpgradesIndex': 110,
        'Image': 'killroy-dungeon-credits'
    },
    'Pearls': {
        'Required Fights': 100,
        'Required Equinox': 3,
        'UpgradesIndex': 111,
        'Image': 'killroy-pearls'
    },
        }
killroy_only_1_level = ['Talent Points', 'Dungeon Credits', 'Pearls']

# This returns incomplete data, since the obols_dict currently only contains DR obols
# Despite this, the function is written to work with whatever data is added to the obols_dict
def get_obol_totals(obol_list, obol_upgrade_dict) -> dict:
    obols_totals = {}
    for obol_index, obol_name in enumerate(obol_list):
        obol_index = str(obol_index)
        # Adds the base values for each equipped obol
        for obol_base_name, obol_base_value in obols_dict.get(obol_name, {}).get('Base', {}).items():
            obols_totals[f"Total{obol_base_name}"] = obols_totals.get(f"Total{obol_base_name}", 0) + obol_base_value
        # Adds any upgrade value for each equipped obol
        if obol_index in obol_upgrade_dict.keys():
            if 'UQ1txt' in obol_upgrade_dict[obol_index] and obol_upgrade_dict[obol_index]['UQ1txt'] != 0:
                try:
                    obols_totals[f"Total{obol_upgrade_dict[obol_index]['UQ1txt']}"] = (
                            obols_totals.get(f"Total{obol_upgrade_dict[obol_index]['UQ1txt']}", 0)
                            + safer_convert(obol_upgrade_dict[obol_index]['UQ1val'], 0)
                    )
                except:
                    logger.exception(f"Could not parse Obol UQ1txt at {obol_index}: {obol_upgrade_dict[obol_index]}")
            if 'UQ2txt' in obol_upgrade_dict[obol_index] and obol_upgrade_dict[obol_index]['UQ2txt'] != 0:
                try:
                    obols_totals[f"Total{obol_upgrade_dict[obol_index]['UQ2txt']}"] = (
                            obols_totals.get(f"Total{obol_upgrade_dict[obol_index]['UQ2txt']}", 0)
                            + safer_convert(obol_upgrade_dict[obol_index]['UQ2val'], 0)
                    )
                except:
                    logger.exception(f"Could not parse Obol UQ2txt at {obol_index}: {obol_upgrade_dict[obol_index]}")
            for upgrade_val in ['STR', 'AGI', 'WIS', 'LUK', 'Defence', 'Weapon_Power', 'Reach', 'Speed']:
                obols_totals[f"Total{upgrade_val}"] = obols_totals.get(f"Total{upgrade_val}", 0) + obol_upgrade_dict.get(upgrade_val, 0)
    return obols_totals
