from collections.abc import Callable
from math import ceil

from consts.general.common import percent_break_point


def next_break_point_tooltip(
    value: float,
    max_value: float,
    half_level: float,
    format_bonus: Callable[[float], str],
    start_value: float = 0.0,
    curve_max: float | None = None,
) -> str:
    """Tooltip HTML with the first break point above `value`.

    For a bonus of start + (curve_max - start) * level / (level + half_level).
    `curve_max` is what the formula tends to, given when the bonus is capped below
    it by `max_value`. The break points are percents of `max_value`, the ones not
    above `start_value` are skipped. `format_bonus` turns a break point bonus into
    the displayed text. Empty once the last one is reached.
    """
    if curve_max is None:
        curve_max = max_value
    percents = percent_break_point
    if curve_max > max_value:
        # A cap below the curve is reached at some level, unlike the curve itself
        percents = [*percent_break_point, 1]
    for percent in percents:
        bonus = max_value * percent
        if bonus <= max(value, start_value):
            continue
        growth = (bonus - start_value) / (curve_max - start_value)
        # round() drops float noise, e.g. 18999.999... for 95%
        level = ceil(round(half_level * growth / (1 - growth), 6))
        return (
            f"<p>{percent:.0%} at level {level:,} with bonus {format_bonus(bonus)}</p>"
        )
    return ""
