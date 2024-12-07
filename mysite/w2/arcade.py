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
            picture_class=f'arcade-bonus-{bonus_name}',
            progression=bonus_details['Level'],
            goal=arcade_max_level+1,
            resource='arcade-gold-ball' if bonus_details['Level'] < 100 else 'arcade-royale-ball' if bonus_details['Level'] == 100 else '',
        ) for bonus_name, bonus_details in session_data.account.arcade.items()
    ]

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
