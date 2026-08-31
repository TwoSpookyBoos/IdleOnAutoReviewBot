from consts.idleon.w7.research import Research

# "Button_Bonuses" in source.
button_bonus_per_time = [2, 3, 2, 2, 4, 5, 4, 25, 5]

button_bonus_labels = [
    "Research EXP Multi", 
    "Minehead Currency Gain",  
    "Sushi Station Bucks Multi",  
    "Sailing Boat/Artifact Multi", 
    "All Masterclass Drop Rate",  
    "Farming Crop Evo Chance",  
    "Spelunking POW",  
    "Cooking Speed", 
    "Class EXP", 
]

# In-game art is buried on a sprite sheet and small anyway, re-using assets from elsewhere
button_bonus_picture_classes = [
    "research",
    "minehead-icon",
    "bucksio",
    "sailing",
    "meritocracy-25",
    "grimoire-upgrade-14",
    "spelunking-tool-0",
    "cooking",
    "meritocracy-27",
]

# "ButtonTasks" in source. Last updated in v2.527 Aug 2026: [Description, Base, FuncType, Coefficient, RoundResult]
ButtonTasks = [["Have_a_total_of_{_STR_or_more", "1000", "exponent", "1.045", "0"], ["Have_a_total_of_{_AGI_or_more", "1000", "exponent", "1.045", "0"], ["Have_a_total_of_{_WIS_or_more", "1000", "exponent", "1.045", "0"], ["Have_a_total_of_{_LUK_or_more", "400", "exponent", "1.040", "0"], ["Have_{_of_the_1st_type_of_Deathbringer_Bones_in_your_Grimoire", "5000", "exponent", "1.18", "0"], ["Have_{_of_the_2nd_type_of_Windwalker_Dust_in_your_Compass", "3000", "exponent", "1.16", "0"], ["Have_{_of_the_3rd_type_of_Arcane_Cultist_Tachyon_in_your_Tesseract", "1500", "exponent", "1.14", "0"], ["Have_{_of_the_4rd_type_of_Arcane_Cultist_Tachyon_in_your_Tesseract", "1000", "exponent", "1.12", "0"], ["Level_up_your_DRAGON_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_MINING_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_LUMBERBOB_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_OCEANMAN_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_OL_RELIABLE_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_BOX_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Level_up_your_TWOSOUL_Statue_to_at_least_LV_{", "100", "linear", "1.5", "1"], ["Have_a_{x_Class_EXP_multi_or_higher", "100", "exponent", "1.15", "0"], ["Have_a_{x_Drop_Rate_multi_or_higher", "25", "exponent", "1.031", "0"], ["Level_up_your_Crystallin_Stamp_to_at_least_LV_{", "25", "linear", "1.6", "1"], ["Level_up_your_Roid_Ragin_Bubble_to_at_least_LV_{", "200", "exponent", "1.035", "0"], ["Level_up_your_Swift_Steppin_Bubble_to_at_least_LV_{", "200", "exponent", "1.035", "0"], ["Level_up_your_Stable_Jenius_Bubble_to_at_least_LV_{", "200", "exponent", "1.035", "0"], ["Have_a_Construction_Build_Rate_of_at_least_{/hr", "50000000", "exponent", "1.13", "0"], ["Have_a_3d_Printer_sample_of_Copper_Ore_of_at_least_{/hr", "100000", "exponent", "1.15", "0"], ["Save_up_{_Feathers_for_your_pal_Orion", "1000000000", "exponent", "1.50", "0"], ["Have_a_total_of_{_Waves,_according_to_your_Miniature_Soul_Apparatus", "500", "linear", "3.5", "1"], ["Have_a_Breeding_Mob_with_at_least_{_power_in_your_1st_storage_slot", "25000", "exponent", "1.023", "0"], ["Have_a_Foraging_Speed_of_at_least_{_in_the_Desert_Oasis_Breeding_grounds", "100000", "exponent", "1.047", "0"], ["Put_a_Tier_{_or_better_Ribbon_on_Yumi_Peachring_in_Cooking", "5", "step", "20", "1"], ["Level_up_your_Sausy_Sausage_meal_to_at_least_LV_{", "25", "step", "2.5", "1"], ["Have_a_Tome_Score_of_at_least_{_PTS", "5000", "exponent", "1.011", "0"], ["Reach_Laboratory_LV_{_or_higher", "100", "linear", "3", "1"], ["Reach_Sneaking_LV_{_or_higher", "200", "linear", "4.3", "1"], ["Reach_Spelunking_LV_{_or_higher", "25", "linear", "1.30", "1"], ["Reach_Mining_LV_{_or_higher", "75", "step", "2", "1"], ["Reach_Choppin_LV_{_or_higher", "75", "step", "2", "1"], ["Reach_Divinity_LV_{_or_higher", "100", "linear", "2.5", "1"], ["Save_up_{_Divinity_PTS", "1000000", "exponent", "1.1", "0"], ["Save_up_{_bars_of_gold_in_Sailing", "1000000", "exponent", "1.13", "0"], ["Have_a_total_Artifact_Find_Chance_multi_of_{x_or_higher_in_Sailing", "1000", "exponent", "1.037", "0"], ["Save_up_{_Gaming_Bits", "1000000000", "exponent", "3.000", "0"], ["Evolve_a_total_of_{_Plants_in_Gaming,_as_shown_by_your_Elegant_Seashell", "1000", "exponent", "1.042", "0"], ["Have_a_total_Palette_Multi_of_{x_or_higher_in_Gaming", "10", "exponent", "1.021", "0"], ["Find_at_least_{_items,_as_shown_by_the_Slab", "500", "linear", "6", "1"], ["Save_up_{_White_Essence_in_Summoning", "1000000000", "exponent", "1.3", "0"], ["Reach_a_total_of_{_Total_Career_Wins_in_Summoning", "50", "linear", "2", "1"], ["Check_a_Crop_Transfer_Ticket_worth_at_least_{_Magic_Beans", "10000", "exponent", "1.060", "0"], ["Save_up_{_Jade_from_the_Ninja_Castle", "1000000", "exponent", "2.500", "0"], ["Have_a_total_of_{%_Golden_Food_Bonus,_as_shown_by_The_Beanstalk", "500", "linear", "100", "1"], ["Find_a_total_of_{_Crops,_as_shown_by_your_Crop_Scientist", "70", "linear", "1", "1"], ["Have_a_max_damage_range_of_{_crystal_damage,_as_shown_in_Player_Info", "100", "exponent", "1.090", "0"], ["Have_a_total_Spelunking_POW_of_{_or_more", "1000000000", "exponent", "1.220", "0"], ["Have_a_Best_Depth_of_at_least_{_in_Chucklemire", "40", "step", "2", "1"], ["Save_up_{_Coins_in_your_inventory..._like,_money,_those_coins", "1000000000", "exponent", "1.550", "0"], ["Reach_Showdown_{_or_higher_at_the_Emperor's_Castle_in_World_6", "25", "step", "2", "0"], ["Save_up_{_Bucks_at_your_Sushi_Station", "1000000", "exponent", "1.340", "0"], ["Save_up_{_Fish_for_your_pal_Poppy", "1000000000", "exponent", "1.280", "0"], ["Save_up_{_Meat_Slices_for_best_friend_Bubba", "1000000", "exponent", "1.150", "0"]]

button_tasks = [
    {
        "Description": description.replace("_", " "),
        "Base": float(base),
        "FuncType": func_type,
        "Coefficient": float(coefficient),
    }
    for description, base, func_type, coefficient, _round_result in ButtonTasks
]

# "Research[39]" in source: length-100 task-order shuffle
button_task_order = [int(value) for value in Research[39]]
