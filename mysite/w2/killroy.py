import math

from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import break_you_best, killroy_only_1_level  # killroy_progressionTiers,
from utils.text_formatting import pl

logger = get_logger(__name__)

def getKillroyCurrentUpgradesAdviceGroup():
    current_advices = []
    for upgradeName, upgradeDict in session_data.account.killroy.items():
        #logger.debug(f"{upgradeName} available? {upgradeDict['Available']}")
        current_advices.append(Advice(
            label=f"{upgradeName}"
                  f"{'<br>Complete ' if not upgradeDict['Available'] else ''}"
                  f"{upgradeDict['Remaining'] if not upgradeDict['Available'] else ''}"
                  f"{' more Killroy fights to unlock this upgrade' if not upgradeDict['Available'] else ''}",
            picture_class=upgradeDict['Image'],
            progression=upgradeDict['Upgrades']
        ))
    current_ag = AdviceGroup(
        tier="",
        pre_string="Informational- Current upgrades",
        advices=current_advices
    )

    return current_ag

def getKillroyUpgradeRecommendationsAdviceGroup():
    ratio_label = '2 Skulls to 3 Timer Ratio'
    only_1_label = 'Only 1 level needed'

    future_advices = {
        ratio_label: [],
        only_1_label: [],
    }

    player_skull_ratio = session_data.account.killroy['Skulls']['Upgrades'] / max(1, session_data.account.killroy['Timer']['Upgrades'])
    desired_skull_ratio = 2/3
    desired_timer_ratio = 3/2
    skull_goal = min(900, max(1, math.ceil(session_data.account.killroy['Timer']['Upgrades'] * desired_skull_ratio)))
    timer_goal = max(1, math.ceil(session_data.account.killroy['Skulls']['Upgrades'] * desired_timer_ratio))
    #logger.debug(f"skull_ratio: {player_skull_ratio}")

    future_advices[ratio_label].append(Advice(
        label=f"Current Skull Ratio",
        picture_class='killroy-skull',
        progression=f"{player_skull_ratio:.2%}",
        goal=f"{desired_skull_ratio:.2%}",
    ))

    if player_skull_ratio < desired_skull_ratio:
        if session_data.account.killroy['Skulls']['Available'] and session_data.account.killroy['Skulls']['Upgrades'] < skull_goal:
            future_advices[ratio_label].append(Advice(
                label=f"Level Skulls to {skull_goal} to meet desired ratio",
                picture_class='killroy-skulls',
                progression=session_data.account.killroy['Skulls']['Upgrades'],
                goal=skull_goal
            ))
            future_advices[ratio_label].append(Advice(
                label=f"Keep Timer as-is for now",
                picture_class='killroy-timer',
                progression=session_data.account.killroy['Timer']['Upgrades'],
                #goal=timer_goal
            ))
        else:
            future_advices[ratio_label].append(Advice(
                label=f"Level Timer until you unlock Skulls upgrade",
                picture_class='killroy-timer',
                progression=session_data.account.killroy['Timer']['Upgrades'],
                goal=min(15, session_data.account.killroy['Timer']['Upgrades'] + session_data.account.killroy['Skulls']['Remaining'])
            ))
    else:
        future_advices[ratio_label].append(Advice(
            label=f"Level Timer to {timer_goal} to meet desired ratio",
            picture_class='killroy-timer',
            progression=session_data.account.killroy['Timer']['Upgrades'],
            goal=timer_goal
        ))
        future_advices[ratio_label].append(Advice(
            label=f"{'Keep Skulls as - is for now' if session_data.account.killroy['Skulls']['Upgrades'] < skull_goal else 'Skulls hardcapped at 900. Time to stop!'}",
            picture_class='killroy-skulls',
            progression=session_data.account.killroy['Skulls']['Upgrades'],
            #goal=skull_goal
        ))

    for upgradeName, upgradeDict in session_data.account.killroy.items():
        if upgradeName in killroy_only_1_level:
            if upgradeDict['Upgrades'] >= 1:
                label = f"{'🛑 ' if upgradeDict['Upgrades'] > 1 else ''}Do not level {upgradeName} any further!"
            else:
                label = f"⚠️ Grab ONLY 1 level in {upgradeName}{' once available' if not upgradeDict['Available'] else ''}"
            future_advices[only_1_label].append(Advice(
                label=label,
                picture_class=upgradeDict['Image'],
                progression=upgradeDict['Upgrades'],
                goal=1
            ))
        # else:
        #     future_advices[ratio_label].append(Advice(
        #         label=f"Continue leveling {upgradeName}",
        #         picture_class=upgradeDict['Image'],
        #         progression=upgradeDict['Upgrades'],
        #         goal=900 if upgradeName == 'Skulls' else ''
        #     ))

    future_ag = AdviceGroup(
        tier="",
        pre_string="Informational- Future upgrades",
        advices=future_advices
    )

    return future_ag

def setKillroyProgressionTier():
    killroy_AdviceDict = {
    }
    killroy_AdviceGroupDict = {}
    killroy_AdviceSection = AdviceSection(
        name="Killroy",
        tier="0",
        pinchy_rating=0,
        header="Best Killroy tier met: Not Yet Evaluated",
        picture="wiki/Killroy.gif",
        complete=False
    )
    # highestKillroySkillLevel = max(session_data.account.all_skills["KillroySkill"])
    # if highestKillroySkillLevel < 1:
    #     killroy_AdviceSection.header = "Come back after unlocking Killroy!"
    #     return killroy_AdviceSection

    infoTiers = 0
    max_tier = 0 #max(killroy_progressionTiers.keys(), default=0) - infoTiers
    tier_Killroy = 0

    killroy_AdviceGroupDict['Future'] = getKillroyUpgradeRecommendationsAdviceGroup()
    killroy_AdviceGroupDict['Current'] = getKillroyCurrentUpgradesAdviceGroup()

    overall_KillroyTier = min(max_tier + infoTiers, tier_Killroy)
    tier_section = f"{overall_KillroyTier}/{max_tier}"
    killroy_AdviceSection.pinchy_rating = overall_KillroyTier
    killroy_AdviceSection.tier = tier_section
    killroy_AdviceSection.groups = killroy_AdviceGroupDict.values()
    if overall_KillroyTier >= max_tier:
        killroy_AdviceSection.header = f"Best Killroy tier met: {tier_section}{break_you_best}️"
        killroy_AdviceSection.complete = True
    else:
        killroy_AdviceSection.header = f"Best Killroy tier met: {tier_section}"

    return killroy_AdviceSection
