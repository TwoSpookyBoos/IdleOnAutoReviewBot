from consts.consts_autoreview import EmojiType
from models.advice.advice import Advice
from models.general.session_data import session_data
from utils.logging import get_logger
logger = get_logger(__name__)

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


def get_legend_talent_advice(talent_name: str, link_to_section: bool = True) -> Advice:
    talent = session_data.account.legend_talents['Talents'][talent_name]
    link_to_section_text = f'{{{{ Legend Talent|#legend-talents }}}} - ' if link_to_section else ''
    next_level_text = f"<br>Next Lv: {talent['Bonus']}" if talent['Level'] < talent['Max Level'] else ''
    advice = Advice(
        label=f"{link_to_section_text}{talent_name}: {talent['Description']}{next_level_text}",
        picture_class=talent['Image'],
        progression=talent['Level'],
        goal=talent['Max Level'],
    )
    return advice
