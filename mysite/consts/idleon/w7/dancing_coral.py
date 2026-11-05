from consts.idleon.w3.construction import ShrineInfo
from consts.idleon.w7.spelunk import Spelunky
from utils.number_formatting import parse_number

dancing_coral_base_costs = Spelunky[22]
dancing_coral_description_templates = Spelunky[23]
dancing_coral_bonus_base_values = Spelunky[24]

# `"Reef_Coral;Vibrant_Coral;...` and `"(Generated_Daily_in_Town);...` in source
# (Dancing Coral UI). Last updated in v2.550
dancing_coral_cost_names = "Reef_Coral;Vibrant_Coral;Glowing_Coral;Char_Coral;Neon_Coral;Aegean_Coral;Gilded_Coral;Twisted_Coral;Eternal_Coral;".split(";")  # fmt: skip # noqa
dancing_coral_cost_sources = "(Generated_Daily_in_Town);(Dropped_by_Shellslugs);(Dropped_by_Litterfish);(Dropped_by_Coralcave_Crab);(Dropped_by_Eggroll);(Dropped_by_Ancientfish);(Dropped_by_Magni_Pufferfin);(Dropped_by_RIPtide);(Dropped_by_RIPtide)".split(";")  # fmt: skip # noqa

dancing_coral_bonus_data = []
for index, (base_cost, description_template, base_value) in enumerate(zip(dancing_coral_base_costs, dancing_coral_description_templates, dancing_coral_bonus_base_values)):
    if "who_knows" in description_template:
        continue
    dancing_coral_bonus_data.append({
        "Base Cost": parse_number(base_cost),
        "Description Template": description_template.replace("_", " ").replace("潤", "&"),
        "Base Value": parse_number(base_value),
        "Target Shrine Name": ShrineInfo[index][0].replace("_", " "),
        "Cost Name": dancing_coral_cost_names[index].replace("_", " "),
        "Cost Source": dancing_coral_cost_sources[index].replace("_", " "),
    })
