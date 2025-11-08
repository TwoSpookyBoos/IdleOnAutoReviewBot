from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_w6 import summoning_doubler_recommendations, summoning_stone_boss_damage_function, summoning_stone_boss_hp_function, summoning_stone_names, summoning_match_colors
from consts.consts_caverns import getSummoningDoublerPtsCost
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    summoning_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Summoning']
    max_tier = true_max - optional_tiers
    tier_Summoning = 0

    #Assess Tiers
    # for tier_number, requirements in summoning_progressionTiers.items():
    #     subgroup_name = f'To reach Tier {tier}'

    tiers_ag = AdviceGroup(
        tier=tier_Summoning,
        pre_string='Progression Tiers',
        advices=summoning_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Summoning)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getEndlessAdviceGroup() -> AdviceGroup:
    eb = session_data.account.summoning['BattleDetails']['Endless']

    endless_advice = [
        Advice(
            label=f"{battle_number}: {battle_details['Challenge']}"
                  f"<br>Reward: {battle_details['Description']}",
            picture_class=battle_details['Image'],
            progression=session_data.account.summoning['Battles']['Endless'],
            goal=battle_number
        ) for battle_number, battle_details in eb.items() if not battle_details['Defeated']
    ]

    endless_ag = AdviceGroup(
        tier='',
        pre_string='Upcoming Endless Rewards',
        advices=endless_advice,
        informational=True
    )
    endless_ag.remove_empty_subgroups()
    return endless_ag

def getUpgradesAdviceGroup() -> AdviceGroup:
    sources = 'Available Doublers and their Sources'
    doublers = 'Recommended Upgrades to Double for Matches'
    upgrades_advice = {
        sources: [],
        doublers: []
    }
    upgrades_advice.update({f"{k} Upgrades":[] for k in summoning_match_colors})

    summoning = session_data.account.summoning
    doublers_spent = summoning['Doubled Upgrades']
    doublers_owned = summoning['Total Doublers Owned']

    #Generate Alert
    if doublers_spent < doublers_owned:
        session_data.account.alerts_Advices['World 6'].append(Advice(
            label=f"{doublers_owned - doublers_spent} available {{{{ Summoning|#summoning }}}} Upgrade doublers",
            picture_class='summoning'
        ))

    #Sources
    next_doubler_cost = getSummoningDoublerPtsCost(session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value'])
    notated_next_doubler_cost = notateNumber('Basic', next_doubler_cost, decimals=3)
    notated_gambit_pts = notateNumber('Match', session_data.account.caverns['Caverns']['Gambit']['TotalPts'], 3,matchString=notated_next_doubler_cost)

    upgrades_advice[sources].append(Advice(
        label=f"{session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Name']} earned from {{{{ Gambit Cavern|#underground-overgrowth}}}}"
              f"<br>Next Doubler at {notated_next_doubler_cost} Total Gambit PTS ({next_doubler_cost - session_data.account.caverns['Caverns']['Gambit']['TotalPts']:,.0f} to go!)",
        picture_class=session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Image'],
        progression=notated_gambit_pts,
        goal=notated_next_doubler_cost
    ))
    upgrades_advice[sources].append(Advice(
        label=f"{10 * session_data.account.event_points_shop['Bonuses']['Summoning Star']['Owned']} earned from {{{{ Event Shop|#event-shop}}}}: Summoning Star",
        picture_class=session_data.account.event_points_shop['Bonuses']['Summoning Star']['Image'],
        progression=10 * session_data.account.event_points_shop['Bonuses']['Summoning Star']['Owned'],
        goal=10
    ))
    upgrades_advice[sources].append(Advice(
        label=f"{doublers_spent}/{doublers_owned} total doublers spent",
        picture_class='summoning',
        progression=doublers_spent,
        goal=doublers_owned
    ))

    #Doubler Recommendations
    for upgrade_name in summoning_doubler_recommendations:
        upgrades_advice[doublers].append(Advice(
            label=f"{summoning['Upgrades'][upgrade_name]['Color']}: {upgrade_name}: "
                  f"{'Not ' if not summoning['Upgrades'][upgrade_name]['Doubled'] else ''}Doubled",
            picture_class=summoning['Upgrades'][upgrade_name]['Image'],
            progression=int(summoning['Upgrades'][upgrade_name]['Doubled']),
            goal=1
        ))
    upgrades_advice[doublers].append(Advice(
        label=f"You're on your own now. You may consider:"
              f"<br>Essence Generation (Cyan, White, Purple, Blue, yolo)"
              f"<br>Cyan: Cost Deflation and Red: Cost Crashing for Cost Reduction"
              f"<br>Yellow: Unit Constitution (HP is circumstantial at best)",
        picture_class='rift-guy'
    ))

    #Normal Upgrades
    for upg_name, upg_details in summoning['Upgrades'].items():
        upgrades_advice[f"{upg_details['Color']} Upgrades"].append(Advice(
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
        pre_string='Doublers and Upgrades',
        advices=upgrades_advice,
        informational=True
    )
    return upgrades_ag

def getSummoningStoneAdviceGroup() -> AdviceGroup:
    summoning_stone_advice = []
    for index, (color, data) in enumerate(session_data.account.summoning['Summoning Stones'].items()):
        mult_text = f"<br>{data['Wins']} wins: {data['Wins'] + 1}x multi to {color} upgrades"
        summoning_stone_advice.append(Advice(
            label=f"{summoning_stone_names[color]} ({data['Location']})"
                  f"{mult_text}"
                  f"<br>DMG: {notateNumber('Basic', summoning_stone_boss_damage_function(data['Base DMG'], data['Wins'] + 1))}"
                  f"<br>HP: {notateNumber('Basic', summoning_stone_boss_hp_function(data['Base HP'], data['Wins'] + 1))}",
            picture_class=data['StoneImage'],
            resource=data['BossImage']
        ))
    return AdviceGroup(
        tier='',
        pre_string='Summoning Stones',
        advices=summoning_stone_advice,
        informational=True,
    )

def getSummoningAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    highest_summoning_level = max(session_data.account.all_skills['Summoning'])
    if highest_summoning_level < 1:
        summoning_AdviceSection = AdviceSection(
            name='Summoning',
            tier='0/0',
            header='Come back after unlocking Summoning!',
            picture='wiki/Summoner_Stone.png',
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
    summoning_AdviceGroupDict['Summoning Stones'] = getSummoningStoneAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    summoning_AdviceSection = AdviceSection(
        name='Summoning',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Summoning Information",  #Best Summoning tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='wiki/Summoner_Stone.png',
        groups=summoning_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )

    return summoning_AdviceSection
