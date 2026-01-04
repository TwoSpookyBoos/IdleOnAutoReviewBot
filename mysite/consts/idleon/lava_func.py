import math

from utils.safer_data_handling import safer_math_pow


def lava_func(funcType: str, level: int, x1: int | float, x2: int | float, roundResult=False):
    match funcType:
        case 'add':
            if x2 != 0:
                result = (((x1 + x2) / x2 + 0.5 * (level - 1)) / (x1/x2)) * level * x1
            else:
                result = level * x1
        case 'decay':
            result = (level * x1) / (level + x2)
        case 'intervalAdd':
            result = x1 + math.floor(level / x2)
        case 'decayMulti':
            result = 1 + (level * x1) / (level + x2)
        case 'bigBase':
            result = x1 + x2 * level
        case 'pow':
            result = safer_math_pow(x1, level)
        case _:
            result = 0
    if roundResult:
        return round(result)
    else:
        return result
