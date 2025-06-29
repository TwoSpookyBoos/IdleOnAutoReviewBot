from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import break_you_best
from consts.consts_w4 import rift_rewards_dict
from consts.progression_tiers import rift_progressionTiers, true_max_tiers

logger = get_logger(__name__)

def getRiftRewardFromLevel(input_level):
    return rift_rewards_dict.get(input_level, {}).get('Name', f'UnknownRiftReward-{input_level}')

def getRiftProgressionTiersAdviceGroup():
    rift_Advices = {
        'UnlockRewards': [],
    }
    optional_tiers = 0
    tier_RiftBonusesUnlocked = 0
    true_max = true_max_tiers['Rift']
    max_tier = true_max - optional_tiers

    for tier_number, requirements in rift_progressionTiers.items():
        if session_data.account.rift_level >= requirements[0]:
            tier_RiftBonusesUnlocked = tier_number
        else:
            rift_Advices['UnlockRewards'].append(Advice(
                label=getRiftRewardFromLevel(requirements[0]),
                picture_class=getRiftRewardFromLevel(requirements[0]),
                progression=session_data.account.rift_level,
                goal=requirements[0]
            ))
            rift_Advices['UnlockRewards'].append(Advice(
                label=f'{requirements[1]} max damage for Multikill',
                picture_class='damage'
            ))
            rift_Advices['UnlockRewards'].append(Advice(
                label=f'{requirements[2]}+ max level books recommended',
                picture_class='talent-book-library'
            ))
            break

    # Generate AdviceGroups
    rift_AdviceGroupDict = {}
    meowTheRiftAdvice = ''
    if session_data.account.rift_meowed == False and session_data.account.apocalypse_character_index is not None:
        meowTheRiftAdvice = (
            f"{session_data.account.all_characters[session_data.account.apocalypse_character_index].character_name}"
            f" has not completed a Super CHOW on the Rift yet!"
        )
        rift_Advices["UnlockRewards"].append(Advice(
            label=meowTheRiftAdvice,
            picture_class="blood-berserker-icon",
        ))
    if meowTheRiftAdvice != '' and tier_RiftBonusesUnlocked >= max_tier:
        group_pre_string = 'One last thing...'
    else:
        group_pre_string = f"Unlock {pl(max_tier - tier_RiftBonusesUnlocked, 'the final Rift Bonus', 'more Rift bonuses')}"
    rift_AdviceGroupDict['UnlockRewards'] = AdviceGroup(
        tier=tier_RiftBonusesUnlocked,
        pre_string=group_pre_string,
        advices=rift_Advices['UnlockRewards'],
    )
    overall_SectionTier = min(true_max, tier_RiftBonusesUnlocked)
    return rift_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getRiftAdviceSection() -> AdviceSection:
    if not session_data.account.rift['Unlocked']:
        rift_AdviceSection = AdviceSection(
            name='Rift',
            tier='0/0',
            header="Come back after completing the Rift Ripper NPC's quest!",
            picture='Rift_Ripper.gif',
            unreached=True
        )
        return rift_AdviceSection

    #Generate AdviceGroups
    rift_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getRiftProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    rift_AdviceSection = AdviceSection(
        name='Rift',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Rift tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Rift_Ripper.gif',
        groups=rift_AdviceGroupDict.values()
    )
    return rift_AdviceSection
