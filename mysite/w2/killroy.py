import math

from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import break_you_best, killroy_only_1_level  # killroy_progressionTiers,

logger = get_logger(__name__)

def getKillroyUpgradeRecommendationsAdviceGroup():
    ratio_label = '2 Skulls to 3 Timer Ratio'
    only_1_label = 'Only 1 level needed'

    future_advices = {
        ratio_label: [],
        only_1_label: [],
    }

    player_skull_ratio = session_data.account.killroy['Skulls']['Upgrades'] / max(1, session_data.account.killroy['Timer']['Upgrades'])
    desired_skull_ratio = 2/3
    skull_hardcap = 900
    desired_timer_ratio = 3/2
    timer_softcap = 180
    skull_goal = min(skull_hardcap, max(2 + session_data.account.killroy['Skulls']['Upgrades'], math.ceil(session_data.account.killroy['Timer']['Upgrades'] * desired_skull_ratio)))
    timer_goal = min(timer_softcap, max(3 + session_data.account.killroy['Timer']['Upgrades'], math.ceil(session_data.account.killroy['Skulls']['Upgrades'] * desired_timer_ratio)))

    future_advices[ratio_label].append(Advice(
        label=f"Current Skull Ratio",
        picture_class='killroy-skull',
        progression=f"{player_skull_ratio:.2%}",
        goal=f"{desired_skull_ratio:.2%}",
    ))

    #Skull and timer Advice
    if player_skull_ratio < desired_skull_ratio:
        if session_data.account.killroy['Skulls']['Upgrades'] < skull_hardcap:
            if session_data.account.killroy['Skulls']['Available']:
                skull_advice = Advice(
                    label=f"Level Skulls to {skull_goal} to meet desired ratio",
                    picture_class='killroy-skulls',
                    progression=session_data.account.killroy['Skulls']['Upgrades'],
                    goal=skull_goal
                )
                timer_advice = Advice(
                    label=f"Keep Timer as-is{' for now' if session_data.account.killroy['Timer']['Upgrades'] < timer_softcap else '. You have reached the softcap.'}",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    # goal=timer_goal
                )
            else:
                skull_advice = Advice(
                    label=f"Level up Skulls once unlocked",
                    picture_class='killroy-skulls',
                    completed=False
                )
                timer_advice = Advice(
                    label=f"Level Timer until you unlock Skulls upgrade",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    goal=min(15, session_data.account.killroy['Timer']['Upgrades'] + session_data.account.killroy['Skulls']['Remaining'])
                )
        else:
            skull_advice = Advice(
                label=f"🛑 Skulls drop chance is hardcapped at {skull_hardcap} upgrades. Do not level further!",
                picture_class='killroy-skulls',
                progression=session_data.account.killroy['Skulls']['Upgrades'],
                # goal=skull_goal
            )
            if session_data.account.killroy['Timer']['Upgrades'] < timer_softcap:
                timer_advice = Advice(
                    label=f"Level Timer to {timer_goal} to meet desired ratio",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    goal=timer_goal
                )
            else:
                timer_advice = Advice(
                    label=f"Some maps seem to stop respawning enemies after around {timer_softcap} Timer upgrades. Upgrade at your own risk.",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                )
    else:
        skull_advice = Advice(
            label=f"'Keep Skulls as - is{' for now' if session_data.account.killroy['Skulls']['Upgrades'] < skull_hardcap else '. You have reached the hardcap!'}",
            picture_class='killroy-skulls',
            progression=session_data.account.killroy['Skulls']['Upgrades'],
            # goal=skull_goal
        )
        if session_data.account.killroy['Timer']['Upgrades'] < timer_softcap:
            timer_advice = Advice(
                label=f"Level Timer to {timer_goal} to meet desired ratio",
                picture_class='killroy-timer',
                progression=session_data.account.killroy['Timer']['Upgrades'],
                goal=timer_goal
            )
        else:
            timer_advice = Advice(
                label=f"Some maps seem to stop respawning enemies after around {timer_softcap} Timer upgrades. Upgrade at your own risk.",
                picture_class='killroy-timer',
                progression=session_data.account.killroy['Timer']['Upgrades'],
            )

    #Decide if Skull or Timer advice goes first
    if player_skull_ratio < desired_skull_ratio:
        future_advices[ratio_label].extend([skull_advice, timer_advice])
    else:
        future_advices[ratio_label].extend([timer_advice, skull_advice])

    future_advices[ratio_label].append(Advice(
        label=f"Still trying to find a good ratio for Respawn."
              f"<br>It is worth leveling but idk exacts yet.",
        picture_class='killroy-respawn',
        progression=session_data.account.killroy['Respawn']['Upgrades'],
        goal='TBD'
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
                goal=1,
                completed=upgradeDict['Upgrades'] >= 1
            ))

    future_ag = AdviceGroup(
        tier="",
        pre_string="Informational- Future upgrades",
        advices=future_advices,
        informational=True
    )

    return future_ag

def getKillroyAdviceSection() -> AdviceSection:
    killroy_AdviceDict = {}
    killroy_AdviceGroupDict = {}

    if session_data.account.highestWorldReached < 2:
        killroy_AdviceSection = AdviceSection(
            name="Killroy",
            tier="0",
            pinchy_rating=0,
            header="Come back after unlocking Killroy in W2 town!",
            picture="wiki/Killroy.gif",
            unrated=True,
            unreached=True
        )
        return killroy_AdviceSection

    info_tiers = 0
    max_tier = 0 - info_tiers  #max(killroy_progressionTiers.keys(), default=0) - infoTiers
    tier_Killroy = 0

    #Generate AdviceGroup
    killroy_AdviceGroupDict['Future'] = getKillroyUpgradeRecommendationsAdviceGroup()

    #Generate AdviceSection
    overall_KillroyTier = min(max_tier + info_tiers, tier_Killroy)
    tier_section = f"{overall_KillroyTier}/{max_tier}"
    killroy_AdviceSection = AdviceSection(
        name="Killroy",
        tier=tier_section,
        pinchy_rating=overall_KillroyTier,
        header="Killroy Information",
        picture="wiki/Killroy.gif",
        groups=killroy_AdviceGroupDict.values(),
        unrated=True
    )
    return killroy_AdviceSection
