from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def getEventShopAdviceGroup() -> AdviceGroup:
    event_points_total = session_data.account.event_points_shop['Points Owned'] + session_data.account.all_assets.get("Quest89").amount
    es_advice = [
        Advice(
            label=f"{bonus_name}: {bonus_details['Description']}",
            picture_class=bonus_details['Image'],
            progression=1 if bonus_details['Owned'] else event_points_total,
            goal=1 if bonus_details['Owned'] else bonus_details['Cost'],
            resource='event-point' if not bonus_details['Owned'] else '',
        ) for bonus_name, bonus_details in session_data.account.event_points_shop['Bonuses'].items()
    ]

    es_advice.insert(0, Advice(
        label=f"Event Points owned: {event_points_total}",
        picture_class='event-point',
        completed=True,
        informational=True
    ))
    for advice in es_advice:
        if advice.resource == '':
            mark_advice_completed(advice)

    es_ag = AdviceGroup(
        tier='',
        pre_string='Seasonal Event Shop bonuses',
        advices=es_advice,
        informational=True
    )
    return es_ag

def getEvent_ShopAdviceSection() -> AdviceSection:
    #Generate AdviceGroups
    event_shop_AdviceGroupDict = {}
    event_shop_AdviceGroupDict['Shop'] = getEventShopAdviceGroup()

    overall_SectionTier = 0
    optional_tiers = 0
    true_max = 0  #true_max_tiers['Event Shop']
    max_tier = true_max - optional_tiers

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    event_shop_AdviceSection = AdviceSection(
        name="Event Shop",
        tier=tier_section,
        pinchy_rating=0,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Seasonal Event Points Shop',
        picture='Event_Shop.png',
        groups=event_shop_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return event_shop_AdviceSection
