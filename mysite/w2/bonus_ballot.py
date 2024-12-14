import math
import time

from consts import ValueToMulti
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data

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
        pre_string="Info- All Ballot bonuses",
        advices=bb_advice
    )
    bb_ag.remove_empty_subgroups()

    return bb_ag


def getBallotMultiAdviceGroup():
    voter_integrity = session_data.account.caverns['Majiks']['Voter Integrity']
    gvb = session_data.account.event_points_shop['Bonuses']['Gilded Vote Button']
    multis_advice = {
        f"Total Multi: {session_data.account.event_points_shop['BonusMulti']:.2f}x": [
            Advice(
                label=f"{{{{ Equinox|#equinox}}}}: Voter Rights: {ValueToMulti(session_data.account.equinox_bonuses['Voter Rights']['CurrentLevel']):.2f}"
                      f"/1.{session_data.account.equinox_bonuses['Voter Rights']['FinalMaxLevel']}x to Weekly Ballot",
                picture_class="voter-rights",
                progression=session_data.account.equinox_bonuses['Voter Rights']['CurrentLevel'],
                goal=session_data.account.equinox_bonuses['Voter Rights']['FinalMaxLevel']
            ),
            Advice(
                label=f"Voter Integrity {{{{ Cavern Majik|#villagers }}}}: {voter_integrity['Description']}",
                picture_class=f"{voter_integrity['MajikType']}-majik-{'un' if voter_integrity['Level'] == 0 else ''}purchased",
                progression=voter_integrity['Level'],
                goal=voter_integrity['MaxLevel']
            ),
            Advice(
                label=f"{{{{Event Shop|#event-shop}}}}: Gilded Vote Button: {gvb['Description']}",
                picture_class=gvb['Image'],
                progression=int(gvb['Owned']),
                goal=1
            )
        ]
    }

    for subgroup in multis_advice:
        for advice in multis_advice[subgroup]:
            mark_advice_completed(advice)

    multis_ag = AdviceGroup(
        tier='',
        pre_string="Info- Sources of Bonus Ballot Multi",
        advices=multis_advice,
        informational=True
    )
    return multis_ag



def getBonus_BallotAdviceSection() -> AdviceSection:
    if session_data.account.highestWorldReached < 2:
        bonus_ballot_AdviceSection = AdviceSection(
            name="Bonus Ballot",
            tier='0/0',
            pinchy_rating=0,
            header="Come back after unlocking Bonus Ballot in W2 town!",
            picture="Bonus_Ballot.png",
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

    #Generate AdviceSection
    #tier_section = f"{overall_SectionTier}/{max_tier}"
    bonus_ballot_AdviceSection = AdviceSection(
        name="Bonus Ballot",
        tier='0/0',
        pinchy_rating=0,
        header="Bonus Ballot information",
        picture="wiki/Voter_Slime.gif",
        groups=bonus_ballot_AdviceGroupDict.values(),
        completed=None,
        informational=True,
        unrated=True,
    )

    return bonus_ballot_AdviceSection
