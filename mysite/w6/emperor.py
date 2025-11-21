from consts.consts_autoreview import EmojiType
from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from flask import g as session_data
from utils.logging import get_logger

logger = get_logger(__name__)


def getBonusesAdviceGroup(player_emperor: dict) -> AdviceGroup:
    bonus_Advices = {
        'Currencies': [
            Advice(
                label=f"Daily Attempts: {player_emperor['Daily Attempts']}"
                      f"<br>Current Attempts: {player_emperor['Remaining Attempts']}/{player_emperor['Max Attempts']}",
                picture_class='lifetime-tickets',
                completed=True
            )
        ],
        'Bonuses': [
            Advice(
                label=f"{bonus_details['Description']}"
                      f"<br>{bonus_details['Scaling']}",
                picture_class=bonus_details['Image'],
                progression=bonus_details['Wins'],
                goal=EmojiType.INFINITY.value
            ) for bonus_name, bonus_details in player_emperor['Bonuses'].items()
        ]
    }

    for label in bonus_Advices:
        for advice in bonus_Advices[label]:
            advice.mark_advice_completed()

    bonus_ag = AdviceGroup(
        tier='',
        pre_string='Total Currencies and Bonuses',
        advices=bonus_Advices,
        informational=True,
        completed=True
    )
    bonus_ag.remove_empty_subgroups()
    return bonus_ag
def getShowdownsAdviceGroup(player_emperor: dict) -> AdviceGroup:

    sd_Advices = [
        Advice(
            label=f"Showdown {sd_number}"
                  f"<br>HP: {details[0]}"
                  f"<br>Reward: {details[1]}",
            picture_class=details[2],
            progression=session_data.account.emperor['Last Showdown'],
            goal=sd_number
        ) for sd_number, details in session_data.account.emperor['Upcoming'].items()
    ]

    for advice in sd_Advices:
        advice.mark_advice_completed()

    sd_ag = AdviceGroup(
        tier='',
        pre_string='Upcoming Showdowns',
        advices=sd_Advices,
        informational=True
    )
    sd_ag.remove_empty_subgroups()
    return sd_ag

def getProgressionTiersAdviceGroup(player_emperor: dict) -> tuple[AdviceGroup, int, int, int]:
    emperor_Advices = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Emperor']
    max_tier = true_max - optional_tiers
    tier_Emperor = 0

    #Assess Tiers
    # for tier_number, requirements in emperor_progressionTiers.items():
    #     subgroup_label = build_subgroup_label(tier_number, max_tier)
    #
    #     if subgroup_label not in emperor_Advices['Tiers'] and tier_Emperor == tier_number - 1:
    #         tier_ArmorSets = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_Emperor,
        pre_string='Progression Tiers',
        advices=emperor_Advices['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Emperor)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getEmperorAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    if session_data.account.highest_world_reached < 6:
        emperor_AdviceSection = AdviceSection(
            name='Emperor',
            tier='Not Yet Evaluated',
            header='Come back after unlocking Emperor!',
            picture='data/Boss6A.png',
            unrated=True,
            unreached=True,
            completed=False
        )
        return emperor_AdviceSection

    player_emperor = session_data.account.emperor

    #Generate Alert Advice

    #Generate AdviceGroups
    emperor_AdviceGroupDict = {}
    emperor_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup(player_emperor)
    emperor_AdviceGroupDict['Bonuses'] = getBonusesAdviceGroup(player_emperor)
    emperor_AdviceGroupDict['Upcoming'] = getShowdownsAdviceGroup(player_emperor)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    emperor_AdviceSection = AdviceSection(
        name='Emperor',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Emperor Showdown',  #f"Best Emperor tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='data/Boss6A.png',
        groups=emperor_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return emperor_AdviceSection
