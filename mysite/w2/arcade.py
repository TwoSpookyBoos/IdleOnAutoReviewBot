from consts.consts_w2 import arcade_max_level
from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from utils.misc.has_companion import has_companion

logger = get_logger(__name__)

def getArcadeBonusesAdviceGroup() -> AdviceGroup:
    arcade_Advices = {
        'Currency': [],
        'Bonuses': []
    }
    arcade_Advices['Currency'] = [
        Advice(
            label=f"{currency_name} owned: {currency_amount:,}",
            picture_class=f'arcade-{currency_name[:-1]}',
            completed=True,
            informational=True
        ) for currency_name, currency_amount in session_data.account.arcade_currency.items()
    ]

    comp_present = session_data.account.companions['Companion Data Present']
    not_present_note = '<br>Note: Could be inaccurate: Companion data not found!' if not comp_present else ''

    arcade_Advices['Bonuses'] = [
        Advice(
            label=f"Bonus {bonus_name}: {bonus_details['Display']}",
            picture_class=bonus_details['Image'],
            progression=bonus_details['Level'],
            goal=arcade_max_level+1,
            resource=bonus_details['Material'],
        ) for bonus_name, bonus_details in session_data.account.arcade.items()
    ]
    arcade_Advices['Bonuses'].insert(0, Advice(
        label=f"Reindeer Companion: {max(1, 2 * has_companion('Reindeer'))}/2x bonuses{not_present_note}",
        picture_class='spirit-reindeer',
        progression=int(has_companion('Reindeer')),
        goal=1
    ))

    for subgroup in arcade_Advices:
        for advice in arcade_Advices[subgroup]:
            mark_advice_completed(advice)

    arcade_ag = AdviceGroup(
        tier='',
        pre_string='Arcade Shop Currency and Bonuses',
        advices=arcade_Advices,
        informational=True
    )
    return arcade_ag

def getArcadeAdviceSection() -> AdviceSection:
    overall_SectionTier = 0
    optional_tiers = 0
    true_max = true_max_tiers['Arcade']
    max_tier = true_max - optional_tiers

    #Generate AdviceGroups
    arcade_AdviceGroupDict = {}
    arcade_AdviceGroupDict['Shop'] = getArcadeBonusesAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    arcade_AdviceSection = AdviceSection(
        name='Arcade',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Arcade',
        picture='wiki/Arcade_Gold_Ball.png',
        groups=arcade_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return arcade_AdviceSection
