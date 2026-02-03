from consts.idleon.w7.spelunk import Spelunky

from utils.number_formatting import parse_number

advice_fish_upgrade_data = []
for upgrade_data in Spelunky[18]:
    name, description_bonus, max_value, cost_coefficient, _ = upgrade_data.split(",")
    description, bonus = description_bonus.split("_@_")
    advice_fish_upgrade_data.append(
        {
            "Name": name.replace("_", " "),
            "Description": description.replace("_", " "),
            "Bonus": bonus.replace("_", " "),
            "MaxValue": parse_number(max_value),
            "CostCoefficient": parse_number(cost_coefficient),
        }
    )
