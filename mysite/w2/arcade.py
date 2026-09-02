from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.general import get_companion_advice

from utils.logging import get_logger


logger = get_logger(__name__)

def getArcadeBonusesAdviceGroup() -> AdviceGroup:
    arcade_Advices = {
        'Currency': [],
        'Bonuses': []
    }
    arcade_Advices['Currency'] = session_data.account.arcade.get_currency_advice()

    _, reindeer_advice = get_companion_advice('Spirit Reindeer')
    arcade_Advices['Bonuses'] = [reindeer_advice] + [
        upgrade.get_advice(False) for upgrade in session_data.account.arcade.values()
    ]

    for subgroup in arcade_Advices:
        for advice in arcade_Advices[subgroup]:
            advice.mark_advice_completed()

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
