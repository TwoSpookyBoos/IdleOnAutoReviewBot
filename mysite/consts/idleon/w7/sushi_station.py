from consts.idleon.w7.research import Research
from utils.number_formatting import parse_number

# `ab.SushiUPG` in source. Last updated in v2.527 Aug 2026
SushiUPG = ["Sushi_Slot 50 3.50 1 0 Adds_a_new_slot_for_your_Sushi_Station!".split(" "), "Fuel_Capacity_I 9999 1.08 50 0 +{_max_Fuel_Capacity!".split(" "), "Fuel_Capacity_II 9999 1.10 200 0 +{_max_Fuel_Capacity,_and_a_unique_@_$x_Fuel_Cap_bonus!".split(" "), "Fuel_Capacity_III 9999 1.12 1500 0 +{_max_Fuel_Capacity,_and_a_unique_@_$x_Fuel_Cap_bonus!".split(" "), "Fuel_Capacity_IV 9999 1.13 10000 0 +{_max_Fuel_Capacity,_and_a_unique_@_$x_Fuel_Cap_bonus!".split(" "), "Fuel_Capacity_V 9999 1.15 50000 0 +{_max_Fuel_Capacity,_and_a_unique_@_$x_Fuel_Cap_bonus!".split(" "), "Superior_Sushi_Skillz 35 3.80 1 .20 You_can_now_click_the_Sushi_on_your_fuel_bar_to_change_which_sushi_you_cook,_up_to_Tier_$._This_also_increases_fuel_cost.".split(" "), "Quality_Freshness 25 6.50 1 0 {%_chance_for_freshly_cooked_Sushi_to_be_+1_higher_Tier!_Cook_T1,_get_T2!".split(" "), "Fastburn_Fuel_I 9999 1.10 15 0 +{%_faster_Fuel_generation!_@_Your_current_rate_is_$".split(" "), "Fastburn_Fuel_II 9999 1.12 100 0 +{%_faster_Fuel_generation,_and_a_unique_@_$x_Fuel_Generation_multi_bonus!".split(" "), "Fastburn_Fuel_III 9999 1.14 750 0 +{%_faster_Fuel_generation,_and_a_unique_@_$x_Fuel_Generation_multi_bonus!".split(" "), "Fastburn_Fuel_IV 9999 1.16 5000 0 +{%_faster_Fuel_generation,_and_a_unique_@_$x_Fuel_Generation_multi_bonus!".split(" "), "Fastburn_Fuel_V 9999 1.17 25000 0 +{%_faster_Fuel_generation,_and_a_unique_@_$x_Fuel_Generation_multi_bonus!".split(" "), "Seared_Knowledge 1 1.10 1 1.5 Whenever_a_sushi_is_created_in_any_way,_that_sushi_type_gains_+1_EXP._Level_up_sushi_for_unique_knowledge_bonuses!".split(" "), "Hot_Slot 20 20.0 1 0 Adds_a_new_SPECIAL_slot_for_your_Sushi_Station..._the_Hot_Plate!_Sushi_on_these_slots_generate_$x_more_Bucks!".split(" "), "Cold_Slot 8 150 1 0 Adds_a_new_SPECIAL_slot_for_your_Sushi_Station..._the_Cold_Plate!_Sushi_on_these_slots_generate_+$_EXP/day_for_ALL_sushi_lower_tiered_than_this_one!".split(" "), "Milktoast_Slot 12 70.0 1 0 Adds_a_new_SPECIAL_slot_for_your_Sushi_Station..._the_Milktoast_Plate!_Sushi_on_these_slots_generate_+$_EXP/day".split(" "), "Salt_Shaker 1 1.10 1 2 Click_to_use_once_per_day._When_used,_all_sushi_have_a_chance_of_getting_a_Tier_Up!_By_default,_you_get_+1_shaker_use_every_day,_just_sayin'.".split(" "), "Pepper_Shaker 1 1.10 1 3 Click_to_use_once_per_day._When_used,_all_sushi_have_a_chance_to_be_Perfecto'd,_which_means_its_Knowledge_Bonus_is_2x_bigger!".split(" "), "Saffron_Shaker 1 1.10 1 4 Click_to_use_once_per_day._When_used,_all_sushi_generate_1_hour's_worth_of_Bucks!".split(" "), "Shake_N'_Bake 10 100.0 1 0 Whenever_you_use_any_Shaker,_you_instantly_generate_1_hour's_worth_of_Fuel!_Also,_{%_chance_to_get_10_hour's_worth_instead!".split(" "), "Bottomless_Shakers 20 12.0 1 0 Whenever_you_use_any_Shaker,_there's_a_{%_chance_to_get_another_usage!_Free_use,_basically...".split(" "), "Sasaphrax_Saffron 23 11.0 1 0 Saffron_Shaker_now_generates_$_hour's_worth_of_Bucks,_not_just_1_hour!".split(" "), "Charcoal_Fireplace 15 40.0 1 0 Unlock_a_new_Fireplace!_This_default_red_charcoal_fire_increases_Fuel_generation_by_+1%_per_Tier_of_Sushi_in_the_column_above_it.".split(" "), "Copper_Firelighter 1 1.10 1 3 Fireplaces_can_be_changed_to_blue._Sushi_above_blue_fires_have_a_{%_chance_of_getting_+2_tiers_instead_of_+1,_so_long_as_it's_not_your_highest_tier.".split(" "), "Potassium_Firelighter 1 1.10 1 5 Fireplaces_can_be_changed_to_purple,_which_each_give_+1_energy/sec_@_$".split(" "), "Lithium_Firelighter 1 1.10 1 4 Fireplaces_can_be_changed_to_pink._Sushi_above_pink_fires_generate_$x_more_Knowledge_EXP_by_all_methods_and_means_of_doing_so!_Think_about_it.".split(" "), "Barium_Firelighter 1 1.10 1 2 Fireplaces_can_be_changed_to_green._Sushi_above_green_fires_generate_$x_more_Bucks.".split(" "), "Overtuned_Fuel 1 1.10 1 0 When_you_generate_fuel_while_at_max_capacity,_you_get_+1_bonus_@_$".split(" "), "Heat_of_the_East_Wind 1 1.10 1 0 When_a_sushi_is_combined,_it_tiers-up_the_sushi_to_its_right,_but_only_if_that_sushi_is_lower_tiered._@_This_only_works_on_sushi_Tier_$_and_lower.".split(" "), "Customer_Surcharge_I 9999 1.14 2 0 All_your_sushi_generate_Bucks_based_on_their_tier._Higher_tier_sushi_generate_way_more!_@_This_upgrade_boosts_all_Bucks_generated_by_+{%".split(" "), "Customer_Surcharge_II 9999 1.16 3 0 All_your_sushi_generate_+{%_more_Bucks!_Also,_each_unique_sushi_you_create_gives_a_1.10x_multiplicative_bonus_to_Bucks_generated,_did_you_know_that?".split(" "), "Customer_Surcharge_III 9999 1.17 5 0 All_your_sushi_generate_+{%_more_Bucks!".split(" "), "Customer_Surcharge_IV 9999 1.19 10 0 All_your_sushi_generate_+{%_more_Bucks!".split(" "), "Customer_Surcharge_V 9999 1.20 20 0 All_your_sushi_generate_+{%_more_Bucks!".split(" "), "Quickpay_Fee 120 2.00 1 0 When_a_sushi_is_created,_it_instantly_generates_{_minute's_worth_of_Bucks!".split(" "), "Wholesale_Pricing 9999 1.15 1 0 All_upgrades_are_$%_cheaper,_now_and_forever!".split(" "), "2nd_Degree_Searing 9999 1.35 1 0 Newly_created_Sushi_generate_+$_exp,_instead_of_just_+1_EXP._This_is_of_course_multiplied_by_all_knowledge_EXP_multi's".split(" "), "3rd_Degree_Searing 9999 1.15 1 0 Boosts_all_Sushi_EXP_gained_from_all_sources_by_+{%._That_includes_newly_created_Sushi_and_EXP_from_Cold_and_Milktoast_plates.".split(" "), "Rift_Guy's_Upgrade 0 1.10 1 0 I've_got_my_hands_in_everything!_Minehead,_farming,_the_rift..._so_yea,_of_course_I'm_in_the_Sushi_biz_too,_don't_be_so_shocked.".split(" "), "No_Tax_on_Tips 9999 1.20 2 0 Multiplies_all_Bucks_earned_by_}x".split(" "), "Hourly_Wage_Meter 9999 1.08 1 0 Adds_a_display_to_the_Top_Right_of_the_Sushi_Station_which_shows_total_Hourly_Bucks_generated_by_all_your_sushi._@_Also,_+{%_total_Bucks_generated_by_all_sushi!".split(" "), "Movement_Mittens 1 1.10 1 .3 Adds_the_MOVE_button._Enabling_this_option_lets_you_drag_the_SLOTS_themselves_around_your_Sushi_Station,_instead_of_the_sushi.".split(" "), "Sushi_Tier_Vision 9999 1.20 2 0 Adds_a_toggle_button_to_the_Top_Left_of_the_Sushi_Station._Click_it_to_show_Sushi_Tiers_numerically,_can_be_turned_off_any_time._@_Also,_+{%_total_Bucks_generated_by_all_sushi!".split(" "), "Sushi_Service_Bonuses 1 1.10 1 0 Creating_a_new_sushi_type_gives_a_new_IdleOn_bonus_for_the_REST_of_the_game!_Check_them_out_in_the_BONUS_tap,_top_right_corner.".split(" ")]

sushi_upgrades = [
    {
        "Name": values[0].replace("_", " "),
        "Max Level": parse_number(values[1]),
        "Cost Increment": float(values[2]),
        "Value Per Level": parse_number(values[3]),
        "Description": values[5].replace("_", " ").replace(" @ ", "<br>"),
    }
    for values in SushiUPG
]

# "MaxTier" in source -- highest cookable Sushi tier (0-indexed, so 63 possible tiers).
sushi_max_tier = 62

# "Research[32]" in source: real shop display order, not SushiUPG's declaration order
sushi_upgrade_shop_order = [int(value) for value in Research[32]]

# short stable names for each milestone
sushi_milestone_names = [
    "Research EXP Multi", "Minehead Upgrade Discount", "Research Daily Rolls",
    "Research Points", "Research AFK Gains", "Event Game Extra Play",
    "Spelunk Shop Discount", "Artifact Find Chance", "Research Magnifier",
    "Summoning Upgrade Discount", "Breeding Mob Damage", "Stamina Regen Multi",
    "Minehead Currency Multi", "Research Point (Flat)", "Ribbon Tier Up Chance",
    "Class EXP Multi", "Minehead Upgrade Discount II", "Exalted Stamp Bonus",
    "Monster Coin Drop", "Legend Talent Point", "Spelunking POW",
    "Grand Discovery Chance", "Minehead Atom Unlock", "Prisma Bubble Bonus",
    "Research AFK Gains II", "Burger Multi", "Sushi Station Upgrade Discount",
    "Spelunk Shop Discount II", "Spelunking Amber Gain", "Gaming Bits Gain",
    "Research Max Roll", "Rat King Crown Chance", "Ninja Twins Stealth",
    "Exotic Market Purchases", "Summoning Upgrade Discount II", "Farming Crop Evo Chance",
    "Hat Rack Multi", "Monster Coin Drop II", "Upgrade Vault Discount",
    "Bubba Meat Slice", "Tiny Cogs", "Sigil EXP Multi",
    "Gaming Palette Luck", "Laboratory EXP Multi", "Sushi Station Upgrade Discount II",
    "Sailing Captain EXP", "Divinity PTS Gain", "Upgrade Vault Discount II",
    "Drop Rate", "Total DMG", "Bonus Ballot Multi",
    "Meritocracy Bonus Multi", "Blue Chest Chance", "Research Upgrade Bonus Multi",
    "Gallery Bonus Multi", "Megacrop Growth Chance", "Villager Opals",
    "Sailing Chest Treasure", "Construction Shrine Build LV", "Royal Guardian Orblet Chance",
    "Royal Guardian Resource Rate", "Royal Guardian Regal Mobs", "Royal Guardian Marble Chance",
]

sushi_milestone_data = [
    {
        "Name": name,
        "Description": description.replace("_", " "),
        "Value": parse_number(value),
    }
    for name, description, value in zip(sushi_milestone_names, Research[36], Research[37])
]
