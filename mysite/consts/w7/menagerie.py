from consts.idleon.w7.research import Research
from utils.misc.clean_game_text import clean_game_text
from utils.number_formatting import parse_number

# "Research"[52..55] in source: mission description, goal per completion, base goal,
# progress label. Last updated in v2.550.0
menagerie_missions = [
    {
        "Description": clean_game_text(description),
        "Goal Increment": parse_number(increment),
        "Goal Base": parse_number(base),
        "Progress Label": clean_game_text(label),
    }
    for description, increment, base, label in zip(
        Research[52], Research[53], Research[54], Research[55]
    )
]

# "Research"[56] and [62] in source: unlock description and tooltip.
# "膛" is the trailing "more info" icon. Last updated in v2.550.0
menagerie_unlocks = [
    {
        "Description": clean_game_text(description, drop_glyphs="膛"),
        "Tooltip": clean_game_text(tooltip),
    }
    for description, tooltip in zip(Research[56], Research[62])
]

# "Research"[57] and [58] in source: boost description and "BoostQTY" per level.
# Last updated in v2.550.0
menagerie_boosts = [
    {
        "Description": clean_game_text(description),
        "Value Per Level": parse_number(value),
    }
    for description, value in zip(Research[57], Research[58])
]

# "SideJellyUnlocked" in source: jellyfish N (1..6) needs this Menagerie unlock.
# Jellyfish 0 is the Menagerie itself and is always there. Last updated in v2.550.0
menagerie_jellyfish = [
    {"Name": "Menagerie Jellyfish", "Unlock Index": None},
    {"Name": "Pink Jellyfish", "Unlock Index": 3},
    {"Name": "Blue Jellyfish", "Unlock Index": 5},
    {"Name": "Red Jellyfish", "Unlock Index": 7},
    {"Name": "Silver Jellyfish", "Unlock Index": 10},
    {"Name": "Yellow Jellyfish", "Unlock Index": 12},
    {"Name": "Green Jellyfish", "Unlock Index": 23},
]

# "ConstBuildBONUSES" in source: Yellow Jellyfish buildings, Menagerie[0][11..14].
# Names come from what each bonus feeds ("ExtraBuildSPDmulti", "ExtraConEXPmulti",
# "ExtraFlaggyRatemulti", "LumiGainRate"). Last updated in v2.550.0
yellow_jelly_buildings = [
    {"Name": "Build Speed", "Value Per Level": 25, "Multiplicative": True},
    {"Name": "Construction EXP", "Value Per Level": 15, "Multiplicative": True},
    {"Name": "Flaggy Rate", "Value Per Level": 10, "Multiplicative": True},
    {"Name": "Lumi Gain", "Value Per Level": 3, "Multiplicative": False},
]

# "Spelunk"[17][28] in source: Top 0.1% nametags the Green Jellyfish wants
green_jelly_nametags_required = 12
# Silver Jellyfish max LVs (Menagerie[0][9], [0][10]), from the jelly UI "maxed" check
silver_jelly_max_levels = (100, 190)
