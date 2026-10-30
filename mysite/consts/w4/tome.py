from consts.consts_general import card_raw_data
from consts.consts_w4 import (
    get_tome_level_required,
    tome_challenges,
)
from consts.idleon.consts_idleon import (
    DeathNoteMobs,
    MapAFKtarget,
    MapDetails,
    NinjaInfo,
    RANDOlist,
)
from consts.w4.breeding import pet_species

tome_challenge_details = [
    {
        "Name": challenge[0]
        .replace("_(Tap_for_more_info)", "")
        .replace("_膛", "")
        .replace("_", " "),
        "Target": float(challenge[1]),
        "Type": int(challenge[2]),
        "Max Points": int(challenge[3]),
        "Level Required": get_tome_level_required(NinjaInfo[32].index(str(index))),
    }
    for index, challenge in enumerate(tome_challenges)
]

tome_card_requirements = {
    card[0]: float(card[2]) for cardset in card_raw_data for card in cardset
}

tome_deathnote_maps = [
    (MapAFKtarget.index(mob), float(MapDetails[MapAFKtarget.index(mob)][0][0]))
    for world in DeathNoteMobs
    for mob in world
    if mob in MapAFKtarget
]

# `PetStats` worlds, which the save indexes from 0
tome_breeding_species = [
    (world, index)
    for world, pets in enumerate(pet_species)
    for index in range(len(pets))
]

# Toilet Paper Postage
tome_live_talent_max_index = "625"

# Star Player, Supernova Player, Calm Basics pts, Special pts
tome_star_talent_indexes = [8, 17, 275, 622]

# "ShinyBonusS" in source. Last updated in v2.531.0
tome_star_shiny_bonus_index = 14
tome_star_shiny_pets = [
    (world, index)
    for world, pets in enumerate(pet_species)
    for index, pet in enumerate(pets)
    if pet["Shiny Bonus"] == "Star Talent Pts"
]
tome_star_shiny_per_level = float(RANDOlist[92][tome_star_shiny_bonus_index])
