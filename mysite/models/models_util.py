# These functions will eventually be moved to their own respective models once we introduce more types/classes
from consts.consts_autoreview import EmojiType
from consts.consts_idleon import companions_data
from consts.consts_w5 import max_sailing_artifact_level
from models.models import Advice
from flask import g as session_data
from utils.misc.has_companion import has_companion
from utils.logging import get_logger
logger = get_logger(__name__)


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

def get_advice_for_money_advice(upgrade_name: str, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.advice_for_money['Upgrades'][upgrade_name]
    link_to_section_text = f'{{{{ Advice For Money|#advice-for-money }}}} - ' if link_to_section else ''
    return upgrade['Value'], Advice(
        label=f"{link_to_section_text}{upgrade_name}:"
              f"<br>{upgrade['Effect']}",
        picture_class=f"advice-for-money-{upgrade['Index']}",
        resource='coins',
        goal=EmojiType.INFINITY.value,
        progression=upgrade['Level']
    )

def get_spelunking_cavern_bonus_advice(bonus_index: int, link_to_section: bool = True) -> Advice:
    if bonus_index not in session_data.account.spelunk['Cave Bonuses']:
        logger.warning(f"bonus_index {bonus_index} not found in session_data.account.spelunk['Cave Bonuses']. Returning generic Advice.")

    bonus = session_data.account.spelunk['Cave Bonuses'].get(bonus_index, {})
    link_to_section_text = f'{{{{ Spelunking|#spelunking }}}} - ' if link_to_section else ''
    advice = Advice(
        label=f"{link_to_section_text}{bonus.get('CaveName', 'UnknownCave')}: {bonus.get('Description', f'UnknownBonus{bonus_index}')}",
        picture_class=bonus.get('Image', ''),
        progression=int(bonus.get('Owned', False)),
        goal=1,
        resource=bonus.get('Resource', ''),
    )
    return advice

def get_basketball_advice(upgrade_index: int, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.basketball['Upgrades'][upgrade_index]
    link_to_section_text = f'{{{{ Basketball|#basketball }}}} - ' if link_to_section else ''
    advice = Advice(
        label=f"{link_to_section_text}Upgrade {upgrade_index + 1}: {upgrade['Description']}",
        picture_class=upgrade['Image'],
        progression=upgrade['Level'],
        goal=EmojiType.INFINITY.value,
        resource='basketball-shop-currency',
    )
    return upgrade['Value'], advice

def get_darts_advice(upgrade_index: int, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.darts['Upgrades'][upgrade_index]
    link_to_section_text = f'{{{{ Darts|#darts }}}} - ' if link_to_section else ''
    advice = Advice(
        label=f"{link_to_section_text}Upgrade {upgrade_index + 1}: {upgrade['Description']}",
        picture_class=upgrade['Image'],
        progression=upgrade['Level'],
        goal=EmojiType.INFINITY.value,
        resource='darts-shop-currency',
    )
    return upgrade['Value'], advice

def get_sailing_artifact_advice(artifact_name: str, include_island_name: bool = False, link_to_section: bool = True) -> Advice:
    artifact = session_data.account.sailing['Artifacts'][artifact_name]
    link_to_section_text = f'{{{{ Artifact|#sailing }}}} - ' if link_to_section else ''
    island_text = f"{artifact['Island']} - " if include_island_name else ''
    advice = Advice(
        label=f"{link_to_section_text}{island_text}{artifact_name}"
              f"<br>{artifact['Description']}"
              f"<br>{artifact['Form']} Bonus: {artifact['FormBonus']}",
        picture_class=artifact['Image'],
        progression=artifact['Level'],
        goal=max_sailing_artifact_level
    )
    return advice

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
