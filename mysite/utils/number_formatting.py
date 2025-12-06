from consts.consts_autoreview import default_huge_number_replacement
from utils.logging import get_consts_logger

logger = get_consts_logger(__name__)


def parse_number(number: str | int | float, default=default_huge_number_replacement) -> int | float:
    """
    Parses a string to a number. Simplifies to an int if possible. Otherwise, it returns a float
    """
    try:
        num = float(number)
        return int(num) if int(num) == num else num
    except:
        logger.exception(f"An error occurred during parse_number. Replacing with default: {default}")
        return int(float(default))
