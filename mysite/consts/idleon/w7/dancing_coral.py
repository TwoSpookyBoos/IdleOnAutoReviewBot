from consts.idleon.w3.construction import ShrineInfo
from consts.idleon.w7.spelunk import Spelunky
from utils.number_formatting import parse_number

dancing_coral_base_costs = Spelunky[22]
dancing_coral_description_templates = Spelunky[23]
dancing_coral_bonus_base_values = Spelunky[24]

dancing_coral_bonus_data = []
for index, (base_cost, description_template, base_value) in enumerate(zip(dancing_coral_base_costs, dancing_coral_description_templates, dancing_coral_bonus_base_values)):
    if "who_knows" in description_template:
        continue
    dancing_coral_bonus_data.append({
        "Base Cost": parse_number(base_cost),
        "Description Template": description_template.replace("_", " "),
        "Base Value": parse_number(base_value),
        "Target Shrine Name": ShrineInfo[index][0].replace("_", " ")
    })
