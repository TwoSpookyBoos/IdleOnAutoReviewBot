from consts.idleon.w7.legend_talents import LegendTalents
from consts.idleon.w7.spelunk import Spelunky
from utils.number_formatting import parse_number

legend_talents_order = Spelunky[26]
legend_talents_bonuses = {
    name.replace("_", " "): {
        "Max Level": parse_number(max_level, -1),
        "Base Value": parse_number(base_value, 0),
        "Bonus": bonus.replace("_", " "),
        "Description": description.replace("_", " ").replace("@ ", ""),
        "Image": f"legend-talent-{legend_talents_order.index(str(index))}",
        "Display Order": legend_talents_order.index(str(index)),
    }
    for index, (name, max_level, base_value, _, bonus, description) in enumerate(
        LegendTalents
    )
    if name.lower() != "filler"
}

# "LegendTalent_MaxLV" in source: Research Grid squares adding their raw level to the
# max LV of these talents (by `LegendTalents` index). Last updated in v2.561.0
legend_talents_grid_max_level_bonuses = {
    "Legendary Yellow Fever": (2, 13, 3, 18, 5),
    "Legendary Red Fever": (9, 23, 33, 1, 16),
    "Legendary Brown Fever": (20, 31, 19, 27, 8),
    "Legendary Green Fever": (34, 30, 29, 6, 26),
}
# Menagerie Unlock 20 gives +3 max LV to these talents
legend_talents_menagerie_max_level_indexes = (35, 33, 36, 0, 20, 31, 15, 32, 6)
