# EmperorBon in source. Last update v2.48 Jan 04 2026
EmperorBon = ["}x_Ninja_Stealth }x_Deathbringer_Extra_Bones $%_cheaper_Farming_Upgrades +{_Opals }x_Windwalker_Extra_Dust +{%_Equinox_Bar_Fill_Rate }x_Arcane_Cultist_Extra_Tachyons }x_Gaming_Bit_gain }x_Summoning_Winner_Bonuses +{%_something_World_7ish +{%_something_World_7ish +{%_Drop_Rate".split(" "), "30 5 20 1 5 15 5 50 1 5 5 10".split(" "), "0 1 0 2 1 4 0 2 4 3 1 0 2 4 5 0 1 2 4 0 6 5 4 2 7 0 1 3 5 4 11 8 0 7 6 9 2 1 7 10 4 5 7 6 0 2 11 1".split(" ")]

emperor_bonus_description = [
    (display_template := value.replace("_", " "), display_template.split(" ", 1))
    for value in EmperorBon[0]
]
emperor_bonus_values = [int(value) for value in EmperorBon[1]]
emperor_fight_bonus_index = [int(value) for value in EmperorBon[2]]
