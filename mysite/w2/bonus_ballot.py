import math
import time
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger


logger = get_logger(__name__)

def getBonusesAdviceGroup() -> AdviceGroup:
    ballot = session_data.account.ballot
    current_week = math.floor(time.time() / 604800)
    is_current_week = current_week == ballot.week
    bb_advice = {
        'Current Bonus': [
            buff.get_advice() for buff in ballot.values()
            if buff.index == ballot.current_buff and buff.index != 0
        ] if is_current_week else [],
        'On the Ballot': [
            buff.get_advice() for buff in ballot.values()
            if buff.index in ballot.on_the_ballot and buff.index != 0
        ] if is_current_week else [],
        'All Bonuses': [buff.get_advice() for buff in ballot.values()]
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
    voter_rights = session_data.account.equinox.upgrades['Voter Rights']
    summoning_bonus = session_data.account.summoning.bonuses["Ballot Bonus"]
    voter_integrity = session_data.account.caverns.villagers["Cosmos"].majiks.idleon['Voter Integrity']
    gvb = session_data.account.event_points_shop['Gilded Vote Button']
    rvb = session_data.account.event_points_shop['Royal Vote Button']
    _, mashed_potato_advice = session_data.account.companions['Mashed Potato'].get_advice()
    _, crystal_cuttlefish_advice = session_data.account.companions['Crystal Cuttlefish'].get_advice()
    multis_advice = {
        f"Total Multi: {session_data.account.ballot.bonus_multi:.2f}x": [
            voter_rights.get_bonus_advice(),
            voter_integrity.get_advice(),
            gvb.get_bonus_advice(),
            rvb.get_bonus_advice(),
            summoning_bonus.get_bonus_advice(),
            mashed_potato_advice,
            crystal_cuttlefish_advice,
            session_data.account.legend_talents['Democracy FTW'].get_advice()
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
