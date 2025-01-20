from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import rift_progressionTiers, break_you_best, riftRewardsDict

logger = get_logger(__name__)

def getRiftRewardFromLevel(inputLevel):
    return riftRewardsDict.get(inputLevel, {}).get('Name', f"UnknownRiftReward{inputLevel}")

def getRiftProgressionTiersAdviceGroup():
    rift_AdviceDict = {
        "UnlockRewards": [],
    }
    info_tiers = 0
    tier_RiftBonusesUnlocked = 0
    max_tier = max(rift_progressionTiers.keys()) - info_tiers

    for tier in rift_progressionTiers.keys():
        if session_data.account.rift_level >= rift_progressionTiers[tier][0]:
            tier_RiftBonusesUnlocked = tier
        else:
            rift_AdviceDict["UnlockRewards"].append(Advice(
                label=getRiftRewardFromLevel(rift_progressionTiers[tier][0]),
                picture_class=getRiftRewardFromLevel(rift_progressionTiers[tier][0]),
                progression=session_data.account.rift_level,
                goal=rift_progressionTiers[tier][0]
            ))
            rift_AdviceDict["UnlockRewards"].append(Advice(
                label=f"{rift_progressionTiers[tier][1]} max damage for Multikill",
                picture_class="damage"
            ))
            rift_AdviceDict["UnlockRewards"].append(Advice(
                label=f"{rift_progressionTiers[tier][2]}+ max level books recommended",
                picture_class="talent-book-library"
            ))
            break

    # Generate AdviceGroups
    rift_AdviceGroupDict = {}
    meowTheRiftAdvice = ""
    if session_data.account.rift_meowed == False and session_data.account.apocalypse_character_Index is not None:
        meowTheRiftAdvice = f"{session_data.account.all_characters[session_data.account.apocalypse_character_Index].character_name} has not completed a Super CHOW on the Rift yet!"
        rift_AdviceDict["UnlockRewards"].append(Advice(
            label=meowTheRiftAdvice,
            picture_class="blood-berserker-icon",
        ))
    if meowTheRiftAdvice != "" and tier_RiftBonusesUnlocked >= max_tier:
        group_pre_string = "One last thing..."
    else:
        group_pre_string = f"Unlock {pl(max_tier - tier_RiftBonusesUnlocked, 'the final Rift Bonus', 'more Rift bonuses')}"
    rift_AdviceGroupDict["UnlockRewards"] = AdviceGroup(
        tier=tier_RiftBonusesUnlocked,
        pre_string=group_pre_string,
        post_string="",
        advices=rift_AdviceDict["UnlockRewards"],
        informational=group_pre_string == "" or group_pre_string == "One last thing..."
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_RiftBonusesUnlocked)
    return rift_AdviceGroupDict, overall_SectionTier, max_tier

def getRiftAdviceSection() -> AdviceSection:
    if not session_data.account.rift['Unlocked']:
        rift_AdviceSection = AdviceSection(
            name="Rift",
            tier="Not Yet Evaluated",
            header="Come back after completing the Rift Ripper NPC's quest!",
            picture="Rift_Ripper.gif",
            unreached=True
        )
        return rift_AdviceSection

    #Generate AdviceGroups
    rift_AdviceGroupDict, overall_SectionTier, max_tier = getRiftProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    rift_AdviceSection = AdviceSection(
        name="Rift",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Rift tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="Rift_Ripper.gif",
        groups=rift_AdviceGroupDict.values()
    )
    return rift_AdviceSection
