from consts.idleon.caverns.cavern import HolesInfo
from utils.safer_data_handling import safer_convert, safer_math_pow

gambit_challenge_names = [
    "King's Gambit",
    "Horsey's Gambit",
    "Bishop's Gambit",
    "Queen's Gambit",
    "Rook's Gambit",
    "Noob's Gambit",
]
schematics_unlocking_gambit_challenges = [
    None,
    "Horsey Gambit",
    "Bishop Gambit",
    "Queen Gambit",
    "Castle Gambit",
    "Noob Gambit",
]
max_gambit_challenges = len(gambit_challenge_names)
# Index into raw_caverns_list[11] where challenge times start.
# Taken from `_customBlock_Holes2."GambitPts"` in source.
gambit_challenge_time_offset = 65


def _parse_gambit_bonus(index: int, entry: str) -> dict:
    scaling_value, scales_with_pts, description, name = entry.split("|")
    clean_name = (
        name.replace("_", " ")
        .replace("梦", "")
        .replace("(TAP ME)", "")
        .replace("而", "x")
        .strip()
        .strip("'")
    )
    clean_description = description.replace("_", " ").strip().strip("'")
    if clean_description == "no":
        clean_description = ""
    # `_customBlock_Holes "GambitPtsREQ"` in source. Last updated in v2.523
    pts_required = 2e3 + 1e3 * (index + 1) * (1 + index / 5) * safer_math_pow(
        1.26, index
    )
    return {
        "ScalingValue": safer_convert(scaling_value, 0),
        "ScalesWithPts": safer_convert(scales_with_pts, False),
        "Description": clean_description,
        "Name": clean_name,
        "PtsRequired": pts_required,
    }


gambit_pts_bonuses = [
    _parse_gambit_bonus(index, entry) for index, entry in enumerate(HolesInfo[71])
]

gambit_pts_for_doublers = [
    0,
    1,
    206,
    351,
    598,
    1018,
    1735,
    2956,
    5036,
    8579,
    14615,
    24899,
    42419,
    72267,
    123118,
    209749,
    357336,
    608773,
    1037131,
    1766899,
    3010163,
    5128238,
    8736680,
    14884170,
    25357290,
    43199731,
    73596854,
    125382655,
    213607095,
    363909914,
    619972035,
    1056210093,
    1799403358,
    3065538252,
    5222578214,
    8897401031,
    15157981722,
    25823766860,
    43994441151,
    74950756128,
    127689219300,
    217536654301,
    370604474083,
    631377165616,
    1075640347430,
    1832505545065,
    3121932512775,
    5318653818304,
    9061079418982,
    15436831018131,
    26298826096055,
]
