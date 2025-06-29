import math

from consts.progression_tiers_updater import true_max_tiers
from consts.consts import EmojiType
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_w2 import killroy_only_1_level

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
    skull_goal = min(
        skull_hardcap,
        max(2 + session_data.account.killroy['Skulls']['Upgrades'], math.ceil(session_data.account.killroy['Timer']['Upgrades'] * desired_skull_ratio))
    )
    timer_goal = min(
        timer_softcap,
        max(3 + session_data.account.killroy['Timer']['Upgrades'], math.ceil(session_data.account.killroy['Skulls']['Upgrades'] * desired_timer_ratio))
    )

    future_advices[ratio_label].append(Advice(
        label='Current Skull Ratio',
        picture_class='killroy-skull',
        progression=f"{player_skull_ratio:.2%}",
        goal=f"{desired_skull_ratio:.2%}",
    ))

    #Skull and timer Advice
    if player_skull_ratio < desired_skull_ratio:
        if session_data.account.killroy['Skulls']['Upgrades'] < skull_hardcap:
            if session_data.account.killroy['Skulls']['Available']:
                skull_advice = Advice(
                    label=f'Level Skulls to {skull_goal} to meet desired ratio',
                    picture_class='killroy-skulls',
                    progression=session_data.account.killroy['Skulls']['Upgrades'],
                    goal=skull_goal
                )
                timer_advice = Advice(
                    label=f"Keep Timer as-is{' for now' if session_data.account.killroy['Timer']['Upgrades'] < timer_softcap else f'. You have reached the {timer_softcap} softcap.'}",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    goal=session_data.account.killroy['Timer']['Upgrades']
                )
            else:
                skull_advice = Advice(
                    label='Level up Skulls once unlocked',
                    picture_class='killroy-skulls',
                    completed=False
                )
                timer_advice = Advice(
                    label='Level Timer until you unlock Skulls upgrade',
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    goal=min(15, session_data.account.killroy['Timer']['Upgrades'] + session_data.account.killroy['Skulls']['Remaining'])
                )
        else:
            skull_advice = Advice(
                label=f'{EmojiType.STOP.value} Skulls drop chance is hardcapped at {skull_hardcap} upgrades. Do not level further!',
                picture_class='killroy-skulls',
                progression=session_data.account.killroy['Skulls']['Upgrades'],
                # goal=skull_goal
            )
            if session_data.account.killroy['Timer']['Upgrades'] < timer_softcap:
                timer_advice = Advice(
                    label=f'Level Timer to {timer_goal} to meet desired ratio',
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                    goal=timer_goal
                )
            else:
                timer_advice = Advice(
                    label=f"Bonus Killroy monsters stop spawning after {timer_softcap-30} Timer upgrades."
                          f" Timer at {timer_softcap} is typically enough time to kill all of those and the extra spawns they produce."
                          f" Timer after this point just allows more Basic spawns",
                    picture_class='killroy-timer',
                    progression=session_data.account.killroy['Timer']['Upgrades'],
                )
    else:
        skull_advice = Advice(
            label=f"'Keep Skulls as - is{' for now' if session_data.account.killroy['Skulls']['Upgrades'] < skull_hardcap else '. You have reached the hardcap!'}",
            picture_class='killroy-skulls',
            progression=session_data.account.killroy['Skulls']['Upgrades'],
            goal=session_data.account.killroy['Skulls']['Upgrades']
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
                label = f"{f'{EmojiType.STOP.value} ' if upgradeDict['Upgrades'] > 1 else ''}Do not level {upgradeName} any further!"
            else:
                label = f"{EmojiType.WARNING.value} Grab ONLY 1 level in {upgradeName}{' once available' if not upgradeDict['Available'] else ''}"
            future_advices[only_1_label].append(Advice(
                label=label,
                picture_class=upgradeDict['Image'],
                progression=upgradeDict['Upgrades'],
                goal=1,
                completed=upgradeDict['Upgrades'] >= 1
            ))

    future_ag = AdviceGroup(
        tier='',
        pre_string='Future upgrades',
        advices=future_advices,
        informational=True
    )

    return future_ag

def getKillroyAdviceSection() -> AdviceSection:
    if session_data.account.highest_world_reached < 2:
        killroy_AdviceSection = AdviceSection(
            name='Killroy',
            tier='0/0',
            pinchy_rating=0,
            header='Come back after unlocking Killroy in W2 town!',
            picture='wiki/Killroy.gif',
            unrated=True,
            unreached=True
        )
        return killroy_AdviceSection

    optional_tiers = 0
    true_max = true_max_tiers['Killroy']
    max_tier = 0 - optional_tiers
    tier_Killroy = 0

    #Generate AdviceGroup
    killroy_AdviceGroups = {}
    killroy_AdviceGroups['Future'] = getKillroyUpgradeRecommendationsAdviceGroup()

    #Generate AdviceSection
    overall_SectionTier = min(true_max, tier_Killroy)
    tier_section = f"{overall_SectionTier}/{max_tier}"
    killroy_AdviceSection = AdviceSection(
        name='Killroy',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header='Killroy Information',
        picture='wiki/Killroy.gif',
        groups=killroy_AdviceGroups.values(),
        unrated=True,
        informational=True
    )
    return killroy_AdviceSection
