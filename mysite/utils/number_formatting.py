
def parse_number(number: str) -> int | float:
    """
    Parses a string to a number. Simplifies to an int if possible. Otherwise, it returns a float
    """
    num = float(number)
    return int(num) if int(num) == num else num