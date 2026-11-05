from consts.generated.monster_data import monster_data
from consts.idleon.consts_idleon import RANDOlist
from consts.idleon.w4.breeding import PetGenes, PetStats
from utils.misc.clean_game_text import clean_game_text

# "PetGenes" in source, without the trailing "GeneName" filler rows.
# Last updated in v2.550.0
breeding_genetics = [gene[0] for gene in PetGenes if gene[0] != "GeneName"]

# "RANDOlist"[91] in source: shiny bonus descriptions, "{" is the value.
# The name is the description without the value. Last updated in v2.550.0
shiny_bonus_names = [
    clean_game_text(description.removeprefix("+{").removeprefix("%"))
    for description in RANDOlist[91]
]

# "PetStats" in source: breedable pets per world, [0] is the monster and [5] the
# species index. The genetic is "RANDOlist"[55][species - 1] into "PetGenes".
# "ShinyBonusS": "RANDOlist"[90][species] is the shiny bonus index into
# "RANDOlist"[91] (description) and [92] (value per Shiny LV). Worlds past the
# breedable ones are "_" placeholders or have no column 5. Last updated in v2.550.0
pet_species = [
    [
        {
            "Name": monster_data[pet[0]]["Name"],
            "Genetic": breeding_genetics[int(RANDOlist[55][int(pet[5]) - 1])],
            "Shiny Bonus": shiny_bonus_names[bonus],
            "Shiny Description": clean_game_text(RANDOlist[91][bonus]),
            "Shiny Value Per Level": int(RANDOlist[92][bonus]),
        }
        for pet, bonus in ((pet, int(RANDOlist[90][int(pet[5])])) for pet in world)
    ]
    for world in PetStats
    if len(world[0]) > 5 and world[0][0] != "_"
]
breeding_total_pets = sum(len(world) for world in pet_species)

# "SpecialPassives" "Lv" in source: Menagerie Unlock 11 raises it by 10.
# Last updated in v2.550.0
shiny_base_max_level = 20

# Shiny bonuses the progression tiers may skip, depending on the account
shiny_bonus_exclusions = [
    "Infinite Star Signs",
    "Lower Minimum Travel Time for Sailing",
    "Higher Artifact Find Chance",
    "Base Critters per Trap",
    "Faster Shiny Mob Lv Up Rate",
]

# Shiny bonuses grouped by how much leveling them is worth, for progression tiers
shiny_bonus_tier = {
    "Important": [
        "Bonuses from All Meals",
        "Drop Rate",
        "Summoning EXP gain",
        "Base Efficiency for All Skills",
        "Multikill Per Tier",
        "Faster Refinery Speed",
    ],
    "Useful": [
        "Farming EXP gain",
        "Lower Minimum Travel Time for Sailing",
        "Sail Captain EXP Gain",
        "Higher Artifact Find Chance",
        "Skill EXP",
        "Base Critters per Trap",
    ],
    "Other": [
        "Faster Shiny Mob Lv Up Rate",
        "Base WIS",
        "Base STR",
        "Base AGI",
        "Base LUK",
        "Infinite Star Signs",
        "Total Damage",
        "Tab 4 Talent Pts",
        "Tab 3 Talent Pts",
        "Tab 2 Talent Pts",
        "Tab 1 Talent Pts",
        "Class EXP",
        "Line Width in Lab",
        "Star Talent Pts",
    ],
}
