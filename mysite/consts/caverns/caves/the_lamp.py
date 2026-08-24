from consts.idleon.caverns.caves.the_lamp import LampWishes
from utils.number_formatting import parse_number
from utils.safer_data_handling import safer_convert

lamp_wishes_description_overrides = {
    # Replace flavor text to shorten/clarify the descriptions
    "More_Wishes": "Unlock the next Wish Type",
    "Another_Try": (
        "Reset investments for Opals, Conjuror PTS, "
        "Jar Collectible Enhancements, or Summoning Doublers"
    ),
    "1000000_Opals": "+1 Opal",
    "Bring_Them_Back": "+12 AFK Hours to any unlocked Monument",
    "World_4_Stuff": (
        "+{% Cooking Speed, +}% Shiny Pet LV Up & Breedability Rate, +~% Lab EXP gain"
    ),
    "A_Moderate_Discount": "15% discount on the next Engineer Schematic creation",
    "World_5_Things": "+{% Sailing Loot Value, +}% Bits gain, +~% Divinity Pts gain",
    "Infinite_Resources": "Well, Harp, and Jar cavern resource gain",
    "World_6_Majigers": (
        "+{% Next Crop chance, +}% Stealth for Ninja twins, +~% All Essence gain"
    ),
    # 'Knowledge_of_Future' intentionally left out for when he implements it in future
    "World_7_Watsinames": LampWishes[10][4].split("_like_")[1].replace("_", " "),
    # 'World_8_Stuff' intentionally left out for when he implements it in the future
}
lamp_wishes = [
    {
        "Name": entry[0].replace("_", " "),
        "BaseCost": parse_number(entry[1]),
        "CostIncreaser": parse_number(entry[2]),
        "DoesCostIncrease": safer_convert(parse_number(entry[3]), True),
        "Description": lamp_wishes_description_overrides.get(
            entry[0], entry[4].replace("_", " ")
        ),
    }
    for entry in LampWishes
]
