from models.advice.advice import Advice
from models.general.session_data import session_data
from utils.logging import get_logger
logger = get_logger(__name__)


def get_coral_reef_advice(coral_name: str) -> Advice:
    upgrade = session_data.account.coral_reef['Reef Corals'][coral_name]
    unlock_or_upgrade_text = 'Level up' if upgrade['Unlocked'] else "Unlock"
    next_level_cost_text = f"<br>Next level costs {upgrade['Next Cost']} corals" if upgrade['Unlocked'] and upgrade['Level'] < upgrade['Max Level'] else ''
    advice = Advice(
        label=f"{unlock_or_upgrade_text} {coral_name}: {upgrade['Description']}{next_level_cost_text}",
        picture_class=upgrade['Image'],
        progression=upgrade['Level'],
        goal=upgrade['Max Level'],
        resource='coral',
    )
    return advice
