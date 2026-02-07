from consts.idleon.consts_idleon import NinjaInfo

from utils.number_formatting import parse_number

raw_merit_bonus = NinjaInfo[41]
merit_bonus = [
    {
        "Bonus": raw_merit_bonus[index].replace("_", " "),
        "Value": parse_number(raw_merit_bonus[index + 1]),
    }
    for index in range(0, len(raw_merit_bonus), 3)
]
