from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.general.session_data import session_data


def get_basketball_advice(upgrade_index: int, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.basketball.upgrades[upgrade_index]
    link_to_section_text = f'{{{{ Basketball|#basketball }}}} - ' if link_to_section else ''
    advice = Advice(
        label=f"{link_to_section_text}Upgrade {upgrade_index + 1}: {upgrade.description}",
        picture_class=upgrade.image,
        progression=upgrade.level,
        goal=EmojiType.INFINITY.value,
        resource='basketball-shop-currency',
    )
    return upgrade.value, advice


def get_darts_advice(upgrade_index: int, link_to_section: bool = True) -> tuple[int | float, Advice]:
    upgrade = session_data.account.darts.upgrades[upgrade_index]
    link_to_section_text = f'{{{{ Darts|#darts }}}} - ' if link_to_section else ''
    advice = Advice(
        label=f"{link_to_section_text}Upgrade {upgrade_index + 1}: {upgrade.description}",
        picture_class=upgrade.image,
        progression=upgrade.level,
        goal=EmojiType.INFINITY.value,
        resource='darts-shop-currency',
    )
    return upgrade.value, advice
