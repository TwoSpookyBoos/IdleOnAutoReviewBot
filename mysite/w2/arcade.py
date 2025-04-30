from consts import arcade_max_level
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getArcadeBonusesAdviceGroup() -> AdviceGroup:
    arcade_advice = {
        'Currency': [],
        'Bonuses': []
    }
    arcade_advice['Currency'] = [
        Advice(
            label=f"{currency_name} owned: {currency_amount:,}",
            picture_class=f'arcade-{currency_name[:-1]}',
            completed=True,
            informational=True
        ) for currency_name, currency_amount in session_data.account.arcade_currency.items()
    ]

    arcade_advice['Bonuses'] = [
        Advice(
            label=f"Bonus {bonus_name}: {bonus_details['Display']}",
            picture_class=bonus_details['Image'],
            progression=bonus_details['Level'],
            goal=arcade_max_level+1,
            resource=bonus_details['Material'],
        ) for bonus_name, bonus_details in session_data.account.arcade.items()
    ]
    arcade_advice['Bonuses'].insert(0, Advice(
        label=f"Reindeer Companion: {max(1, 2 * session_data.account.companions['Reindeer'])}/2x bonuses"
              f"{'<br>Note: Could be inaccurate: Companion data not found!' if not session_data.account.companions['Companion Data Present'] else ''}",
        picture_class='spirit-reindeer',
        progression=int(session_data.account.companions['Reindeer']),
        goal=1

    ))


    for subgroup in arcade_advice:
        for advice in arcade_advice[subgroup]:
            mark_advice_completed(advice)

    arcade_ag = AdviceGroup(
        tier='',
        pre_string="Arcade Shop Currency and Bonuses",
        advices=arcade_advice
    )
    return arcade_ag

def getArcadeAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    arcade_AdviceGroupDict = {}
    arcade_AdviceGroupDict['Shop'] = getArcadeBonusesAdviceGroup()

    #Generate AdviceSection
    #tier_section = f"{overall_SectionTier}/{max_tier}"
    arcade_AdviceSection = AdviceSection(
        name="Arcade",
        tier='0/0',
        pinchy_rating=0,
        header="Arcade",
        picture="wiki/Arcade_Gold_Ball.png",
        groups=arcade_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return arcade_AdviceSection
