from consts.consts_w2 import arcade_max_level
from models.general.session_data import session_data

from models.advice.advice import Advice

from utils.number_formatting import round_and_trim
from utils.logging import get_logger
logger = get_logger(__name__)

def get_arcade_advice(bonus_index: int, link_to_section: bool = True) -> Advice:
    bonus = session_data.account.arcade[bonus_index]
    label = ''
    if link_to_section:
        label += '{{Arcade|#arcade}} '
    if 'Display' not in bonus:
        display = f"Bonus {bonus_index}: +{round_and_trim(bonus['Value'])}"
        if bonus['Level'] < arcade_max_level:
            display += f"/{round_and_trim(bonus['MaxValue'])}"
        display += f"{bonus['Display Type']} {bonus['Stat']}"
        bonus['Display'] = display
    label += bonus['Display']
    return Advice(
        label=label,
        picture_class=bonus['Image'],
        progression=bonus['Level'],
        goal=arcade_max_level,
        resource=bonus['Material'],
    )
