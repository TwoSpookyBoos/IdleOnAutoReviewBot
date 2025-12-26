import math
import time
from consts.progression_tiers import true_max_tiers
from consts.consts_autoreview import EmojiType

from models.models import AdviceSection, AdviceGroup, Advice, session_data
from models.models_util import get_companion_advice, get_summoning_bonus_advice, get_legend_talent_advice
from utils.logging import get_logger


logger = get_logger(__name__)

def getBonusesAdviceGroup() -> AdviceGroup:
    bb = session_data.account.ballot['Buffs']
    current_week = math.floor(time.time() / 604800)
    bb_advice = {
        'Current Bonus': [
            Advice(
                label=f"Bonus {bonus_index}: {bonus_details['Description']}",
                picture_class=bonus_details['Image'],
            ) for bonus_index, bonus_details in bb.items() if bonus_index == session_data.account.ballot['CurrentBuff'] and bonus_index != 0
        ] if current_week == session_data.account.ballot['Week'] else [],
        'On the Ballot': [
            Advice(
                label=f"Bonus {bonus_index}: {bonus_details['Description']}",
                picture_class=bonus_details['Image'],
            ) for bonus_index, bonus_details in bb.items() if bonus_index in session_data.account.ballot['OnTheBallot'] and bonus_index != 0
        ] if current_week == session_data.account.ballot['Week'] else [],
        'All Bonuses': [
            Advice(
                label=f"Bonus {bonus_index}: {bonus_details['Description']}",
                picture_class=bonus_details['Image'],
            ) for bonus_index, bonus_details in bb.items()
        ]
    }

    bb_ag = AdviceGroup(
        tier='',
        pre_string='All Ballot bonuses',
        advices=bb_advice,
        informational=True
    )
    bb_ag.remove_empty_subgroups()

    return bb_ag

def getBallotMultiAdviceGroup():
    e_vr = session_data.account.equinox_bonuses['Voter Rights']
    endless = session_data.account.summoning['Endless Bonuses']['+{% Ballot Bonus']
    voter_integrity = session_data.account.caverns['Majiks']['Voter Integrity']
    gvb = session_data.account.event_points_shop['Bonuses']['Gilded Vote Button']
    rvb = session_data.account.event_points_shop['Bonuses']['Royal Vote Button']
    _, mashed_potato_advice = get_companion_advice('Mashed Potato')
    _, crystal_cuttlefish_advice = get_companion_advice('Crystal Cuttlefish')
    multis_advice = {
        f"Total Multi: {session_data.account.ballot['BonusMulti']:.2f}x": [
            Advice(
                label=f"{{{{ Equinox|#equinox}}}}: Voter Rights: +{e_vr['CurrentLevel']}/{e_vr['FinalMaxLevel']}%",
                picture_class="voter-rights",
                progression=e_vr['CurrentLevel'],
                goal=e_vr['FinalMaxLevel']
            ),
            Advice(
                label=f"Voter Integrity {{{{ Majik|#villagers }}}}: +{voter_integrity['Description']}",
                picture_class=f"{voter_integrity['MajikType']}-majik-{'un' if voter_integrity['Level'] == 0 else ''}purchased",
                progression=voter_integrity['Level'],
                goal=voter_integrity['MaxLevel']
            ),
            Advice(
                label=f"{{{{Event Shop|#event-shop}}}}: Gilded Vote Button: {gvb['Description']}",
                picture_class=gvb['Image'],
                progression=int(gvb['Owned']),
                goal=1
            ),
            Advice(
                label=f"{{{{Event Shop|#event-shop}}}}: Royal Vote Button: {rvb['Description']}",
                picture_class=rvb['Image'],
                progression=int(rvb['Owned']),
                goal=1
            ),
            get_summoning_bonus_advice('+{% Ballot Bonus', endless=True),
            mashed_potato_advice,
            crystal_cuttlefish_advice,
            get_legend_talent_advice('Democracy FTW')
        ]
    }

    for subgroup in multis_advice:
        for advice in multis_advice[subgroup]:
            advice.mark_advice_completed()

    multis_ag = AdviceGroup(
        tier='',
        pre_string='Sources of Bonus Ballot Multi',
        advices=multis_advice,
        informational=True
    )
    return multis_ag

def getBonus_BallotAdviceSection() -> AdviceSection:
    if session_data.account.highest_world_reached < 2:
        bonus_ballot_AdviceSection = AdviceSection(
            name="Bonus Ballot",
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking Bonus Ballot in W2 town!',
            picture='Bonus_Ballot.png',
            completed=False,
            unrated=True,
            unreached=True
        )
        return bonus_ballot_AdviceSection

    #Generate AdviceGroups
    bonus_ballot_AdviceGroupDict = {
        'Bonuses': getBonusesAdviceGroup(),
        'Multi': getBallotMultiAdviceGroup()
    }

    overall_SectionTier = 0
    optional_tiers = 0
    true_max = true_max_tiers['Bonus Ballot']
    max_tier = true_max - optional_tiers

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    bonus_ballot_AdviceSection = AdviceSection(
        name='Bonus Ballot',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header="Bonus Ballot information",
        picture="wiki/Voter_Slime.gif",
        groups=bonus_ballot_AdviceGroupDict.values(),
        completed=None,
        informational=True,
        unrated=True,
    )

    return bonus_ballot_AdviceSection
