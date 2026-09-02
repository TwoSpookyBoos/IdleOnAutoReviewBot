from models.general.session_data import session_data

from models.advice.advice import Advice

def get_arcade_advice(bonus_index: int, link_to_section: bool = True) -> Advice:
    return session_data.account.arcade[bonus_index].get_advice(link_to_section)
