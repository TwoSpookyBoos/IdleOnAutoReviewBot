from consts.idleon.w2.killroy import SkullShopDesc

# Permanent Skull Shop upgrades, by "KillroyBonuses" index in source: the shop slot
# (`SkullShopDesc` row), the OptLacc index counting purchases and the bonus
# Base + Scale * purchases / (Half Purchases + purchases). Last updated in v2.561
skull_shop_bonuses = [
    {
        "Name": name,
        "Slot": slot,
        "Purchases Index": purchases_index,
        "Base": base,
        "Scale": scale,
        "Half Purchases": half_purchases,
        "Description": SkullShopDesc[slot][0].replace("|", " ").replace("_", " "),
        "Cost": int(SkullShopDesc[slot][1]),
    }
    for name, slot, purchases_index, base, scale, half_purchases in [
        ("Artifact Find", 11, 228, 1, 1, 300),
        ("Crop Evolution", 13, 229, 1, 9, 300),
        ("Jade Gain", 14, 230, 1, 2, 300),
        ("Gallery", 15, 467, 0, 10, 200),
        ("Masterclass Drops", 16, 468, 1, 1.3, 200),
        ("W7 Skill EXP", 17, 469, 1, 0.8, 150),
        ("Daily Coral", 18, 470, 0, 25, 250),
        ("Something", 19, 471, 1, 2, 200),
    ]
]
