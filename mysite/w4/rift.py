import json
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data
from consts import rift_progressionTiers

logger = get_logger(__name__)
riftRewardsDict = {
    5: 'Trap Box Vacuum',
    10: 'Infinite Stars',
    15: 'Skill Mastery',
    20: 'Eclipse Skulls',
    25: 'Stamp Mastery',
    30: 'Eldritch Artifact',
    35: 'Vial Mastery',
    40: 'Construct Mastery',
    45: 'Ruby Cards'}

def getRiftRewardFromLevel(inputLevel):
    return riftRewardsDict.get(inputLevel, f"UnknownRiftReward{inputLevel}")

def parseJSONtoLists():
    templateList = json.loads(session_data.account.raw_data.get("Rift", "[0,0,'',0,0,0,0,0,0,0]"))
    return templateList

def setRiftProgressionTier():
    rift_AdviceDict = {
        "UnlockRewards": [],
    }
    rift_AdviceGroupDict = {}
    rift_AdviceSection = AdviceSection(
        name="Rift",
        tier="Not Yet Evaluated",
        header="Best Rift tier met: Not Yet Evaluated",
        picture="Rift_Ripper.gif"
    )
    if not session_data.account.rift_unlocked:
        rift_AdviceSection.header = "Come back after completing the Rift Ripper NPC's quest!"
        return rift_AdviceSection

    tier_RiftBonusesUnlocked = 0
    max_tier = max(rift_progressionTiers.keys())

    for tier in rift_progressionTiers.keys():
        if session_data.account.rift_level >= rift_progressionTiers[tier][0]:
            tier_RiftBonusesUnlocked = tier
        else:
            rift_AdviceDict["UnlockRewards"].append(
                Advice(
                    label=getRiftRewardFromLevel(rift_progressionTiers[tier][0]),
                    picture_class=getRiftRewardFromLevel(rift_progressionTiers[tier][0]),
                    progression=session_data.account.rift_level,
                    goal=rift_progressionTiers[tier][0])
            )
            rift_AdviceDict["UnlockRewards"].append(
                Advice(
                    label=f"{rift_progressionTiers[tier][1]} max damage for Multikill",
                    picture_class="damage")
            )
            rift_AdviceDict["UnlockRewards"].append(
                Advice(
                    label=f"{rift_progressionTiers[tier][2]}+ max level books recommended",
                    picture_class="talent-book-library")
            )
            break
    #Generate AdviceGroups
        rift_AdviceGroupDict["UnlockRewards"] = AdviceGroup(
            tier=str(tier_RiftBonusesUnlocked),
            pre_string=f"Unlock {pl(max_tier - tier_RiftBonusesUnlocked, 'the final Rift Bonus', 'more Rift bonuses')}",
            post_string="",
            advices=rift_AdviceDict.get("UnlockRewards", [])
        )
    #Generate AdviceSection
    overall_RiftTier = min(max_tier, tier_RiftBonusesUnlocked)
    tier_section = f"{overall_RiftTier}/{max_tier}"
    rift_AdviceSection.tier = tier_section
    rift_AdviceSection.pinchy_rating = overall_RiftTier
    rift_AdviceSection.groups = rift_AdviceGroupDict.values()
    if overall_RiftTier == max_tier:
        rift_AdviceSection.header = f"Best Rift tier met: {tier_section}<br>You best ❤️"
    else:
        rift_AdviceSection.header = f"Best Rift tier met: {tier_section}"

    return rift_AdviceSection