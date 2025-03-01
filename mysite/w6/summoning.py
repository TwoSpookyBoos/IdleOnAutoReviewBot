from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string,
    #summoning_progressionTiers
)

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    summoning_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(summoning_progressionTiers.keys(), default=0) - info_tiers
    tier_Summoning = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Summoning,
        pre_string="Progression Tiers",
        advices=summoning_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Summoning)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + info_tiers


def getEndlessAdviceGroup():
    endless_advice = []
    eb = session_data.account.summoning['BattleDetails']['Endless']

    endless_advice = [
        Advice(
            label=f"{battle_number}: {battle_details['Description']}",
            picture_class=battle_details['Image'],
            progression=session_data.account.summoning['Battles']['Endless'],
            goal=battle_number
        ) for battle_number, battle_details in eb.items() if not battle_details['Defeated']
    ]

    endless_ag = AdviceGroup(
        tier='',
        pre_string='Informational- Upcoming Endless Rewards',
        advices=endless_advice
    )
    endless_ag.remove_empty_subgroups()
    return endless_ag


def getSummoningAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    highestSummoningSkillLevel = max(session_data.account.all_skills["Summoning"])
    if highestSummoningSkillLevel < 1:
        summoning_AdviceSection = AdviceSection(
            name="Summoning",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Summoning!",
            picture="",
            unrated=True,
            unreached=True,
            completed=False
        )
        return summoning_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    summoning_AdviceGroupDict = {}
    summoning_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()
    summoning_AdviceGroupDict['Endless'] = getEndlessAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    summoning_AdviceSection = AdviceSection(
        name="Summoning",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Summoning Information",  #Best Summoning tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="wiki/Summoner_Stone.png",
        groups=summoning_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return summoning_AdviceSection
