from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.models_util import get_event_shop_advice
from utils.logging import get_logger


logger = get_logger(__name__)

def getEventShopAdviceGroup() -> AdviceGroup:
    event_points_total = session_data.account.event_points_shop['Points Owned'] + session_data.account.all_assets.get("Quest89").amount
    event_shop_advice: list[Advice] = [
        get_event_shop_advice(bonus_name) for bonus_name in session_data.account.event_points_shop['Bonuses'].keys()
    ]

    event_shop_advice.insert(0, Advice(
        label=f"Event Points owned: {event_points_total}",
        picture_class='event-point',
        completed=True,
        informational=True
    ))
    for advice in event_shop_advice:
        if advice.resource == '':
            advice.mark_advice_completed()

    es_ag = AdviceGroup(
        tier='',
        pre_string='Seasonal Event Shop bonuses',
        advices=event_shop_advice,
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
