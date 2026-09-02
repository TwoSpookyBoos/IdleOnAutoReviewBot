from models.advice.advice import Advice
from models.general.session_data import session_data


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
    upgrade = session_data.account.vault.upgrades[upgrade_name]
    return upgrade.get_advice(session_data.account.vault.total_upgrades, link_to_section, additional_info_text)


def get_companion_advice(companion_name: str, value_is_multi: bool = False) -> tuple[int | float, Advice]:
    return session_data.account.companions[companion_name].get_advice(value_is_multi)

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


