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
