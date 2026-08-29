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
