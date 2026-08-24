from consts.idleon.caverns.cavern import HolesInfo

jar_rupies = [
    "Red",
    "Green",
    "Blue",
    "Yellow",
    "Magenta",
    "Turquoise",
    "Orange",
    "Ultramarine",
    "Purple",
    "Master",
    "White",
    "Dark",
]
max_jar_rupies = len(jar_rupies)

jar_types = [
    "Simple",
    "Tall",
    "Ornate",
    "Great",
    "Enchanted",
    "Artisan",
    "Epic",
    "Gilded",
    "Ceremony",
    "Heirloom",
]
max_jar_types = len(jar_types)

# rupie_index -> (source jar_types index, unlock threshold, threshold display text).
# Threshold is None when the Rupie always drops from that Jar type; otherwise it's
# unlocked once you own that many of the *previous* Rupie (jar_rupies[rupie_index - 1]).
jar_rupie_sources = {
    0: (0, None, None),
    1: (0, 100, "100"),
    2: (0, 1e3, "1K"),
    3: (3, None, None),
    4: (3, 1e4, "10K"),
    5: (3, 5e5, "500K"),
    6: (6, None, None),
    7: (6, 6e6, "6M"),
    8: (6, 5e7, "50M"),
    9: (9, None, None),
    10: (5, None, None),
    11: (8, None, None),
}

jar_collectibles = [
    {
        "Name": name.title().replace("_", " "),
        "ScalingValue": int(scaling_value),
        "Description": description.replace("_", " "),
    }
    for name, scaling_value, _filler, description in (
        entry.split("|") for entry in HolesInfo[67]
    )
]
max_jar_collectibles = len(jar_collectibles)
