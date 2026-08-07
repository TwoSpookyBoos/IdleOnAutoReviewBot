# SaltLicks in source. Last updated in v2.523
SaltLicks = [
    "Refinery1 Samples_taken_for_the_3D_printer_are_+{%_bigger! 5 0.5 20 1.5".split(" "),
    "Refinery1 +4_Obol_storage_slots_per_upgrade!_Circle,_Square,_Hexagon,_then_Sparkle,_in_that_order. 10 1 8 2.3".split(" "),
    "Refinery2 +{%_Refinery_Speed_for_all_cycle_types._In_other_words,_cycles_take_less_time. 5 2 100 1.15".split(" "),
    "Refinery2 +{%_Class_EXP_and_Skill_EXP._Not_really_sure_what_those_blobulytes_do_with_these_souls... 10 .2 100 1.2".split(" "),
    "Refinery3 +{_Max_level_for_talent_books_from_the_library._RNG_be_with_you! 5 2 10 2.2".split(" "),
    "Refinery3 +{%_Liquid_rate_and_Capacity_for_all_liquids_in_Alchemy. 10 1 100 1.122".split(" "),
    "Refinery4 +{%_Points_Earned_during_Worship_Tower_Defense_from_killing_monsters. 5 5 10 2.1".split(" "),
    "Refinery4 +{%_Movement_Speed._Doesn't_work_if_you're_above_170%_move_speed_already. 10 .4 25 1.4".split(" "),
    "Refinery5 +{%_Multikill_Rate_for_all_worlds._All_of_them! 5 3 10 2.2".split(" "),
    "Refinery5 +{%_Total_Damage_dealt. 10 .1 250 1.04".split(" "),
    "Refinery6 +{%_Cooking_Mastery_EXP_gain,_a_feature_unlocked_via_Rift_61_deep_in_World_4. 100 1 100 1.22".split(" "),
]

salt_lick_name_list: list[str] = [
    'Printer Sample Size', 'Obol Storage', 'Refinery Speed', 'EXP', 'Max Book',
    'Alchemy Liquids', 'TD Points', 'Movespeed', 'Multikill', 'Damage', 'Cooking Mastery'
]

salt_lick_list = [
    {"name": salt_lick_name_list[index], "material": info[0]}
    for index, info in enumerate(SaltLicks)
]
