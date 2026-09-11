from consts.idleon.w7.coral_reef import CoralReef
from utils.number_formatting import parse_number

coral_reef_names = [
    "Brain Coral",
    "Carnation Coral",
    "Anemone Coral",
    "Pillar Coral",
    "Paragorgia Coral",
    "Staghorn Coral",
]

coral_reef_bonus_data = [
    {
        "Name": coral_reef_names[index],
        "Description": description.replace("_", " ")
        .replace("@", "")
        .replace("+{", "")
        .replace("+}", "")
        .replace("%", ""),
        "Max Level": parse_number(max_level, -1),
        "Image": f"coral-{index}",
        "Coefficient": parse_number(coefficient, 0),
        "Exponent Base": parse_number(exponent_base, 0),
    }
    # leftover `*_` parts seem to be coordinates used when rendering
    for index, (description, max_level, coefficient, exponent_base, *_) in enumerate(
        CoralReef
    )
]
