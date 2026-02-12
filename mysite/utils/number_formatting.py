from consts.consts_autoreview import default_huge_number_replacement
from utils.logging import get_consts_logger

logger = get_consts_logger(__name__)


def round_and_trim(number: int | float, places: int = 2) -> int | float:
    number_as_string = str(round(number, places))
    if int(number) != number:
        number_as_string = number_as_string.rstrip('0').rstrip('.')
    return parse_number(number_as_string)

def parse_number(number: str | int | float, default=default_huge_number_replacement) -> int | float:
    """
    Parses a string to a number. Simplifies to an int if possible. Otherwise, it returns a float
    """
    try:
        num = float(number)
        return int(num) if int(num) == num else num
    except:
        if not number.isalpha():
            logger.exception(f"An error occurred during parse_number. Replacing with default: {default}")
        return int(float(default))


def number_to_roman(num: int) -> str:
    # Mapping in descending order to handle largest values first
    roman_map = {
        1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
        100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
        10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'
    }
    result = ""
    for value, symbol in roman_map.items():
        count, num = divmod(num, value)
        result += symbol * count
        if num == 0:
            break
    return result
