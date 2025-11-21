import json
import math
from consts.consts_autoreview import default_huge_number_replacement
from utils.logging import get_logger
logger = get_logger(__name__)


def safe_loads(data):
    return json.loads(data) if isinstance(data, str) else data


def safer_get(data, query, default):
    """
    Replace Nonetype result with default param if encountered.
    Also attempts to typecast the result to the same type as Default param.
    """
    try:
        result = data.get(query, default)
        if isinstance(result, type(default)):
            return result
        else:
            return safer_convert(result, default)
    except AttributeError:
        logger.exception(f"Could not .get() from provided {type(data)} data. Returning default.")
        return default
    except Exception as e:
        logger.exception(f"Something else went wrong lol: {e}")
        return default


def safer_convert(data, default):
    try:
        if data is None:
            return default
        elif isinstance(default, int):
            return int(float(data)) if data else default
        else:
            return type(default)(data)
    except (TypeError, ValueError):
        logger.exception(f"Could not convert [{type(data)}: {data}] to [{type(default)}: {default}]. Returning default.")
        return default
    except Exception as e:
        logger.exception(f"Something else went wrong lol: {e}")
        return default


def safer_math_pow(base, exponent, default=default_huge_number_replacement):
    try:
        return math.pow(base, exponent)
    except OverflowError:
        logger.error(f"OverflowError during math.pow() call given base {base} ^ {exponent}. Replacing with default: {default}")
        return default
    except:
        logger.exception(f"Some other error during math.pow() call. Replacing with default: {default}")
        return default


def safer_math_log(input_value, base):
    """
    :param input_value:
    :param base: Lava, lava, or 10 will all use Lava's pow10 estimate
    """
    if base == 'Lava' or base == 'lava' or base == 10:
        # When you see _customBlock_getLOG called in source code, use base='Lava' here
        return math.log(max(input_value, 1)) / 2.30259
    elif input_value <= 0:
        return 0
    else:
        return math.log(input_value, base)
