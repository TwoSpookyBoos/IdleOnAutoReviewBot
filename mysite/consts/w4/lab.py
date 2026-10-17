from consts.idleon.consts_idleon import RANDOlist

# `"EmporiumBonus",Math.round(8+i)` in lab init. Last updated in v2.531.0
lab_bonus_emporium_unlocks = {
    "Artifact Attraction": "The Artifact Matrix",
    "Slab Sovereignty": "The Slab Matrix",
    "Spiritual Growth": "The Spirit Matrix",
    "Depot Studies PhD": "The Crop Matrix",
}

# Mainframe connections, `_customEvent_Lab2` "d" trigger in source.
# Last updated in v2.531.0
lab_prism_coords = (43, 229)
lab_base_connection_range = 80
# `"Dist"==e` in source: these ignore every range bonus
lab_bonus_fixed_ranges = {"Spelunker Obol": 80, "Viral Connection": 80}
lab_jewel_fixed_ranges = {
    "Pyrite Rhombol": 80,
    "Pure Opal Navette": 80,
    "Deadly Wrath Jewel": 100,
    "North Winds Jewel": 100,
    "Eternal Energy Jewel": 100,
}
# TaskShopDesc[3][4][11] in source: a stray space in the row shifts this to 1
lab_merit_range_per_level = 1
lab_base_line_width = 50
lab_line_width_per_level = 2
lab_line_width_card_cap = 50
lab_souped_tube_line_width = 30
lab_sapphire_rhombol_aura_range = 150
lab_sapphire_rhombol_aura_multi = 1.25
lab_arena_line_width = 20
lab_arena_bonus_wave = int(RANDOlist[53][13])
lab_shiny_line_width_per_level = int(RANDOlist[92][19])
# Laboratory Bling grants these jewels at total Lab levels
lab_bling_jewel_levels = {
    "Pure Opal Rhinestone": 700,
    "Pure Opal Navette": 1400,
    "Pure Opal Rhombol": 2100,
}
