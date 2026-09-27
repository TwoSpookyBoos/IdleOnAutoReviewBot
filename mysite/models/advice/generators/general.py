from models.advice.advice import Advice
from models.general.session_data import session_data


def get_upgrade_vault_advice(upgrade_name: str, link_to_section: bool = True, additional_info_text: str = "") -> Advice:
    upgrade = session_data.account.vault.upgrades[upgrade_name]
    return upgrade.get_advice(session_data.account.vault.total_upgrades, link_to_section, additional_info_text)
