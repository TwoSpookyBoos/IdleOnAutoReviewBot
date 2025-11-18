# These functions will eventually be moved to their own respective models once we introduce more types/classes
from consts.consts_idleon import companions_data
from models.models import Advice
from flask import g as session_data
from utils.misc.has_companion import has_companion

def get_guild_bonus_advice(bonus_name: str) -> Advice:
    bonus = session_data.account.guild_bonuses[bonus_name]
    return Advice(
        label=f"Guild Bonus - {bonus_name}:"
              f"<br>{bonus['Description']}",
        picture_class=bonus['Image'],
        progression=bonus['Level'],
        goal=bonus['Max Level']
    )

def get_upgrade_vault_advice(upgrade_name: str, link_to_section: bool = True, additional_info_text: str = "") -> Advice:
    upgrade = session_data.account.vault['Upgrades'][upgrade_name]
    main_line = f"""{f"{{{{ Upgrade Vault|#upgrade-vault }}}} - {upgrade_name}" if link_to_section else upgrade_name}: {upgrade['Description']}"""
    unlock_line = f"<br>Requires {upgrade['Unlock Requirement'] - session_data.account.vault['Total Upgrades']} more Upgrades to unlock" if not upgrade['Unlocked'] else ""
    return Advice(
        label=main_line + unlock_line + additional_info_text,
        picture_class=upgrade['Image'],
        progression=upgrade['Level'],
        goal=upgrade['Max Level'],
    )

def get_companion_advice(companion_name: str) -> tuple[int | float, Advice]:
    companion_data_missing = not session_data.account.companions['Companion Data Present']
    missing_companion_data_txt = '<br>Note: Could be inaccurate. Companion data not found!' if companion_data_missing else ''
    companion = companions_data[companion_name]
    return companion['Value'] * has_companion(companion_name), Advice(
        label=f"Companions - {companion_name}:"
              f"<br>{companion['Description']}"
              f"{missing_companion_data_txt}",
        picture_class=companion['Image'],
        progression=int(has_companion(companion_name)) if not companion_data_missing else 'IDK',
        goal=1
    )


def get_advice_for_money_advice(upgrade_name, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.advice_for_money['Upgrades'][upgrade_name]
    link_to_section_text = f'{{{{ Advice For Money|#advice-for-money }}}} - ' if link_to_section else ''
    return upgrade['Value'], Advice(
        label=f"{link_to_section_text}{upgrade_name}:"
              f"<br>{upgrade['Effect']}",
        picture_class=f"advice-for-money-{upgrade['Index']}",
        resource='coins',
        progression=upgrade['Level']
    )
