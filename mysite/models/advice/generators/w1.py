from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.general.session_data import session_data


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


def get_event_shop_advice(bonus_name: str) -> Advice:
    # TODO: add "Value" field to Event Shop Items so we can use this in other sections. Currently this generator is only useful for the Event Shop section
    event_points_total = session_data.account.event_points_shop['Points Owned'] + session_data.account.all_assets.get("Quest89").amount
    bonus = session_data.account.event_points_shop['Bonuses'][bonus_name]
    return Advice(
        label=f"{bonus_name}: {bonus['Description']}",
        picture_class=bonus['Image'],
        progression=1 if bonus['Owned'] else event_points_total,
        goal=1 if bonus['Owned'] else bonus['Cost'],
        resource='event-point' if not bonus['Owned'] else '',
    )
