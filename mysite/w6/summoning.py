from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string, summoningDict, summoning_doubler_recommendations, getSummoningDoublerPtsCost,
    # summoning_progressionTiers
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
    # for tier, requirements in summoning_progressionTiers.items():
    #     subgroup_name = f'To reach Tier {tier}'

    tiers_ag = AdviceGroup(
        tier=tier_Summoning,
        pre_string="Progression Tiers",
        advices=summoning_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Summoning)
    return tiers_ag, overall_SectionTier, max_tier, max_tier + info_tiers

def getEndlessAdviceGroup() -> AdviceGroup:
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

def getUpgradesAdviceGroup() -> AdviceGroup:
    doublers = 'Recommended Upgrades to Double for Matches'
    upgrades_advice = {
        doublers: []
    }
    upgrades_advice.update({k:[] for k in summoningDict.keys()})

    summoning = session_data.account.summoning

    #Generate Alert
    if summoning['Doubled Upgrades'] < session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value']:
        avail = session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value'] - summoning['Doubled Upgrades']
        session_data.account.alerts_AdviceDict['World 6'].append(Advice(
            label=f"{avail} available {{{{ Summoning|#summoning }}}} Upgrade doublers",
            picture_class='summoning'
        ))

    next_doubler = getSummoningDoublerPtsCost(session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value'])

    upgrades_advice[doublers].append(Advice(
        label=f"{summoning['Doubled Upgrades']}/{session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Name']} "
              f"from {{{{ Gambit Cavern|#underground-overgrowth}}}} spent"
              f"<br>Next Doubler at {next_doubler:,} Total Gambit PTS ({next_doubler - session_data.account.caverns['Caverns']['Gambit']['TotalPts']:,.0f} to go!)",
        picture_class=session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Image'],
        progression=summoning['Doubled Upgrades'],
        goal=session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value']
    ))

    for upgrade_name in summoning_doubler_recommendations:
        upgrades_advice[doublers].append(Advice(
            label=f"{summoning['Upgrades'][upgrade_name]['Color']}: {upgrade_name}: "
                  f"{'Not ' if not summoning['Upgrades'][upgrade_name]['Doubled'] else ''}Doubled",
            picture_class=summoning['Upgrades'][upgrade_name]['Image'],
            progression=int(summoning['Upgrades'][upgrade_name]['Doubled']),
            goal=1
        ))

    for upg_name, upg_details in summoning['Upgrades'].items():
        upgrades_advice[upg_details['Color']].append(Advice(
            label=(
                f"{upg_name}"
                if upg_details['Unlocked'] else
                f"{upg_name}: Unlocked after 1 level into {upg_details['LockedBehindName']}"
            ),
            picture_class=upg_details['Image'],
            progression=upg_details['Level'],
            goal=upg_details['MaxLevel']
        ))

    for subgroup in upgrades_advice:
        for advice in upgrades_advice[subgroup]:
            mark_advice_completed(advice)

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Informational- Doublers and Upgrades',
        advices=upgrades_advice
    )
    return upgrades_ag

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
    summoning_AdviceGroupDict['Upgrades'] = getUpgradesAdviceGroup()
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
