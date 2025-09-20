from utils.logging import get_logger

logger = get_logger(__name__)


def parse_number(number: str, default=1e100) -> int | float:
    """
    Parses a string to a number. Simplifies to an int if possible. Otherwise, it returns a float
    """
    try:
        num = float(number)
        return int(num) if int(num) == num else num
    except:
        logger.exception(f"An error occurred during parse_number. Replacing with default: {default}")
        return int(float(default))