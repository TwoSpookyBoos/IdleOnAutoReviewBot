from consts.idleon.consts_idleon import companions_data
from models.advice.advice import Advice
from models.general.session_data import session_data
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


def get_gem_shop_purchase_advice(
        purchase_name: str,
        link_to_section: bool = True,
        override_goal: int | None = None,
        secondary_label: str | None = None
) -> Advice:
    gsp = session_data.account.gemshop['Purchases'][purchase_name]
    link_to_section_text = f'{{{{ Gem Shop|#gem-shop }}}} - ' if link_to_section else ''
    secondary_label_text = f'{secondary_label}' if secondary_label is not None else ''
    advice = Advice(
        label=f"{link_to_section_text}{purchase_name} ({gsp['Subsection']}){secondary_label_text}",
        picture_class=purchase_name,
        progression=gsp['Owned'],
        goal=(
            override_goal if override_goal is not None
            else int(gsp['MaxLevel']) if isinstance(gsp['MaxLevel'], float)
            else gsp['MaxLevel']
        ),
    )
    advice.resource = 'gem' if advice.percent < 100 else ''
    return advice


