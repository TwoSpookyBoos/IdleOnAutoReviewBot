from consts.idleon.w5.divinity import (
    DivPerHrEXP,
    DivPTSPerHr,
    DivStyle,
    GodsInfo,
    OfferingOdds,
)

# Blessing currency is hardcoded per god in source (the Divinity altar click handler):
# Gaming bits for 0/2/4/8, Sailing treasure for 1, coins for 3/6, particles otherwise.
# The colour of the bits is only our image choice. Last updated in v2.561.0
_blessing_materials = [
    "green-bits",
    "sailing-treasure-0",
    "red-bits",
    "coins",
    "red-bits",
    "particles",
    "coins",
    "particles",
    "purple-bits",
    "particles",
]
# Indexed like `GodsInfo`: Snehebatu = 0
divinity_gods = [
    {
        "Name": info[0],
        # "DivMinorBonus" in source: `GodsInfo[GodsInfo[god][13]][3]`
        "MinorBaseValue": int(GodsInfo[int(info[13])][3]),
        "BlessingPerLevel": int(info[14]),
        "BlessingMaterial": _blessing_materials[index],
    }
    for index, info in enumerate(GodsInfo)
]

# "StyleLvReq" in source:
# 5i + 5 * floor(i / 4) + 10 * floor(i / 5) + max(0, 15 * (i - 5)).
# Last updated in v2.561.0
_style_unlock_levels = [0, 5, 10, 15, 25, 40, 60, 80]
_style_notes = {3: "(To all characters)", 5: "(Even when not Meditating)"}
# Indexed like `DivStyle`
divinity_styles = [
    {
        "Name": info[0],
        "UnlockLevel": _style_unlock_levels[index],
        "Points": DivPTSPerHr[index],
        "Exp": DivPerHrEXP[index],
        "Notes": _style_notes.get(index, ""),
    }
    for index, info in enumerate(DivStyle)
]

# Indexed like `OfferingOdds`; names and images are not in source
_offering_names = [
    "Olive Branch",
    "Incense",
    "Giftbox",
    "Tithe",
    "Hearty Meal",
    "Sacrifice",
]
divinity_offerings = [
    {
        "Name": _offering_names[index],
        "Image": f"offering-{round(100 * odds)}",
        "Odds": odds,
    }
    for index, odds in enumerate(OfferingOdds)
]

# Server variable `DivCostAfter3` read by "OfferingCost" in source: % offering cost
# increase per god after the third. Used when the save has no server variables.
# Last verified as of v2.12 Ballot
default_offering_cost_after_3 = 40

divinity_level_reasons = {
    0: "",
    2: "to activate Doot",
    40: "to unlock the TranQi Style.",
    50: "to unlock the Multitool Stamp from Poigu's quest.",
}
divinity_arctis_breakpoints = {
    12: {60: 841, 61: 602, 62: 467, 63: 380, 64: 319, 65: 275, 66: 241},
    13: {72: 841, 73: 647, 74: 525, 75: 441, 76: 379, 77: 332, 78: 295},
    14: {85: 1331, 86: 986, 87: 782, 88: 648, 89: 522, 90: 481, 91: 425, 92: 381},
    15: {
        102: 1641,
        103: 1246,
        104: 1004,
        105: 841,
        106: 722,
        107: 633,
        108: 564,
        109: 508,
        110: 462,
    },
    16: {
        122: 3601,
        123: 2401,
        124: 1801,
        125: 1441,
        126: 1201,
        127: 1029,
        128: 901,
        129: 801,
        130: 721,
    },
    17: {
        150: 4441,
        151: 3101,
        152: 2383,
        153: 1936,
        154: 1631,
        155: 1409,
        156: 1241,
        157: 1002,
    },
    18: {
        188: 5983,
        189: 4302,
        190: 3361,
        191: 2759,
        192: 2341,
        193: 2033,
        194: 1798,
        195: 1612,
    },
    19: {244: 6041, 245: 4841, 246: 4041, 247: 3469, 248: 3041, 249: 2707, 250: 2441},
    20: {332: 6731, 333: 5817, 334: 5123, 335: 4579, 336: 4141, 337: 3780, 338: 3478},
}
