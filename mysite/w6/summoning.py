from consts.consts_autoreview import MultiToValue, EmojiType
from consts.consts_caverns import getSummoningDoublerPtsCost
from consts.progression_tiers import true_max_tiers
from consts.w6.summoning import (
    summoning_doubler_recommendations,
    summoning_regular_match_colors,
)

from models.advice.advice import Advice
from models.advice.advice_group import AdviceGroup
from models.advice.advice_section import AdviceSection
from models.advice.generators.general import get_gem_shop_purchase_advice
from models.advice.generators.w5 import get_sailing_artifact_advice
from models.general.session_data import session_data

from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.text_formatting import notateNumber

logger = get_logger(__name__)


def get_tiers() -> tuple[AdviceGroup, int, int, int]:
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


def get_next_endless_battles() -> AdviceGroup:
    endless_advice = [
        battle.get_info_advice(session_data.account.summoning.endless.total_win)
        for battle in session_data.account.summoning.endless.next_battle
    ]
    endless_ag = AdviceGroup(
        tier='',
        pre_string='Upcoming Endless Rewards',
        advices=endless_advice,
        informational=True
    )
    endless_ag.remove_empty_subgroups()
    return endless_ag


def get_regular_battles() -> AdviceGroup:
    rb_advices = {}
    regular_summoning = session_data.account.summoning.regular
    for color, battle_list in regular_summoning.battle.items():
        rb_advices[color] = [
            battle.get_info_advice(regular_summoning.win[color])
            for battle in battle_list
        ]
    rb_ag = AdviceGroup(
        tier="", pre_string="Regular Battles", advices=rb_advices, informational=True
    )
    rb_ag.remove_empty_subgroups()
    rb_ag.mark_advice_completed()
    return rb_ag


def get_bonuses() -> AdviceGroup:
    summoning = session_data.account.summoning
    bonuses_advices = {
        "Regular Battles Bonuses": [
            bonus.get_bonus_advice(False)
            for bonus in summoning.bonuses.values()
            if bonus.is_regular
        ],
        "Endless Battles Bonuses "
        f"{summoning.endless.total_win}/{EmojiType.INFINITY.value}": [
            bonus.get_bonus_advice(False)
            for bonus in summoning.bonuses.values()
            if not bonus.is_regular
        ],
    }
    bonuses_ag = AdviceGroup(
        tier="", pre_string="Bonuses", advices=bonuses_advices, informational=True
    )
    bonuses_ag.mark_advice_completed()
    return bonuses_ag


def get_bonuses_multi() -> AdviceGroup:
    account = session_data.account
    summoning = account.summoning
    player_group, max_group = summoning.multi["Bonuses"]["Group"]
    player_mga, player_mgb, player_mgc = player_group
    _, max_mgb, _ = max_group
    mga = f"Multi Group A: {round_and_trim(player_mga)}x"
    mgb = f"Multi Group B: {round_and_trim(player_mgb)}x"
    mgc = f"Multi Group C: {round_and_trim(player_mgc)}x"
    summary = "Summary"
    multi_advices = {summary: [], mga: [], mgb: [], mgc: []}
    # Multi Group A: Pristine Charm - Crystal Comb
    multi_advices[mga].append(
        account.sneaking.pristine_charms["Crystal Comb"].get_obtained_advice()
    )
    # Multi Group B: Gem Shop - King of all Winners
    multi_advices[mgb].append(
        get_gem_shop_purchase_advice(
            purchase_name="King Of All Winners",
            link_to_section=True,
            secondary_label=f": {round_and_trim(player_mgb)}/{round_and_trim(max_mgb)}x",
        )
    )
    # Multi Group C: Summoning Winner Bonuses, some of which apply only to certain upgrades
    multi_advices[mgc].append(
        account.emperor["Summoning Winner Bonuses"].get_bonus_advice()
    )
    multi_advices[mgc].append(
        summoning.bonuses["Winner Bonuses"].get_bonus_advice(False)
    )
    multi_advices[mgc].append(get_sailing_artifact_advice('The Winz Lantern'))
    multi_advices[mgc].append(Advice(
        label=f"W6 Larger Winner bonuses merit: "
              f"+{account.merits[5][4]['Level']}/{account.merits[5][4]['MaxLevel']}%",
        picture_class="merit-5-4",
        progression=account.merits[5][4]["Level"],
        goal=account.merits[5][4]["MaxLevel"]
    ))
    multi_advices[mgc].append(Advice(
        label=f"W6 Achievement: Spectre Stars: "
              f"+{int(account.achievements['Spectre Stars']['Complete'])}/1%",
        picture_class="spectre-stars",
        progression=int(account.achievements['Spectre Stars']['Complete']),
        goal=1
    ))
    multi_advices[mgc].append(Advice(
        label=f"W6 Achievement: Regalis My Beloved: "
              f"+{int(account.achievements['Regalis My Beloved']['Complete'])}/1%",
        picture_class="regalis-my-beloved",
        progression=summoning.sanctuary_count if not account.achievements['Regalis My Beloved']['Complete'] else 360,
        goal=360
    ))
    multi_advices[mgc].append(Advice(
        label=f"{{{{Armor Set|#armor-sets}}}}: Godshard Set: "
              f"+{round(MultiToValue(account.armor_sets['Sets']['GODSHARD SET']['Total Value']), 1):g}"
              f"/{round(account.armor_sets['Sets']['GODSHARD SET']['Base Value'], 1):g}%",
        picture_class=account.armor_sets['Sets']['GODSHARD SET']['Image'],
        progression=int(account.armor_sets['Sets']['GODSHARD SET']['Owned']),
        goal=1
    ))
    # Summary
    total = round_and_trim(summoning.multi["Bonuses"]["Value"])
    library_total = round_and_trim(summoning.multi["Library"]["Value"])
    multi_advices[summary].append(Advice(
        label=f"Regular Battles Bonuses Multi: {total}x",
        picture_class='summoning'
    ))
    multi_advices[summary].append(Advice(
        label=f"Library Max Bonus Multi: {library_total}x",
        picture_class='library'
    ))
    multi_ag = AdviceGroup(
        tier="",
        pre_string="Sources of Bonuses Multi",
        advices=multi_advices,
        informational=True,
    )
    multi_ag.mark_advice_completed()
    return multi_ag


def get_upgrades() -> AdviceGroup:
    summoning = session_data.account.summoning
    sources = 'Available Doublers and their Sources'
    doublers = 'Recommended Upgrades to Double for Matches'
    total = f"Total Doublers: {summoning.doubler.own}"
    upgrades_advice = {
        total: [],
        sources: [],
        doublers: []
    }
    upgrades_advice.update({f"{k} Upgrades": [] for k in summoning_regular_match_colors})
    # Sources
    next_doubler_cost = getSummoningDoublerPtsCost(session_data.account.caverns['Caverns']['Gambit']['Bonuses'][0]['Value'])
    notated_next_doubler_cost = notateNumber('Basic', next_doubler_cost, decimals=3)
    notated_gambit_pts = notateNumber('Match', session_data.account.caverns['Caverns']['Gambit']['TotalPts'], 3, matchString=notated_next_doubler_cost)
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
    upgrades_advice[sources].append(summoning.get_doubler_spent_advice())
    # Doubler Recommendations
    for upgrade_name in summoning_doubler_recommendations:
        upgrades_advice[doublers].append(
            summoning.upgrades[upgrade_name].get_doubler_advice()
        )
    upgrades_advice[doublers].append(Advice(
        label=f"You're on your own now. You may consider:"
              f"<br>Essence Generation (Cyan, White, Purple, Blue, yolo)"
              f"<br>Cyan: Cost Deflation and Red: Cost Crashing for Cost Reduction"
              f"<br>Yellow: Unit Constitution (HP is circumstantial at best)",
        picture_class='rift-guy'
    ))
    # Normal Upgrades
    for upgrade in summoning.upgrades.values():
        upgrades_advice[f"{upgrade.color} Upgrades"].append(upgrade.get_bonus_advice())
    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Doublers and Upgrades',
        advices=upgrades_advice,
        informational=True
    )
    upgrades_ag.mark_advice_completed()
    return upgrades_ag


def get_bosses() -> AdviceGroup:
    return AdviceGroup(
        tier="",
        pre_string="Summoning Stones",
        advices=[
            boss.get_info_advice()
            for boss in session_data.account.summoning.bosses.values()
        ],
        informational=True,
    )


def get_section() -> AdviceSection:
    # Check if player has reached this section
    highest_summoning_level = max(session_data.account.all_skills["Summoning"])
    if highest_summoning_level < 1:
        return AdviceSection(
            name="Summoning",
            tier="0/0",
            header="Come back after unlocking Summoning!",
            picture="wiki/Summoner_Stone.png",
            unrated=True,
            unreached=True,
            completed=False
        )
    # Generate Alert
    session_data.account.add_alert_list(
        "World 6", [session_data.account.summoning.get_doubler_alert()]
    )
    # Generate AdviceGroups
    summoning_AdviceGroupDict = {}
    summoning_AdviceGroupDict["Tiers"], overall_tier, max_tier, true_max = get_tiers()
    summoning_AdviceGroupDict["Regular"] = get_regular_battles()
    summoning_AdviceGroupDict["Endless"] = get_next_endless_battles()
    summoning_AdviceGroupDict["Bonuses"] = get_bonuses()
    summoning_AdviceGroupDict["Bonuses Multi"] = get_bonuses_multi()
    summoning_AdviceGroupDict["Summoning Stones"] = get_bosses()
    summoning_AdviceGroupDict["Upgrades"] = get_upgrades()
    # Generate AdviceSection
    return AdviceSection(
        name="Summoning",
        tier=f"{overall_tier}/{max_tier}",
        pinchy_rating=overall_tier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="Summoning Information",
        picture="wiki/Summoner_Stone.png",
        groups=summoning_AdviceGroupDict.values(),
        completed=None,
        unrated=True,
    )
