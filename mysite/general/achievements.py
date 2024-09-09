from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import break_you_best, achievements_progressionTiers, achievement_categories

logger = get_logger(__name__)

def setAchievementsProgressionTier():
    achievements_AdviceDict = {category: {} for category in achievement_categories}
    achievements_AdviceGroupDict = {}
    achievements_AdviceSection = AdviceSection(
        name="Achievements",
        tier="0",
        pinchy_rating=0,
        header="Best Achievements tier met: Not Yet Evaluated",
        picture="Grasslands_Gary.gif",
        complete=False
    )

    infoTiers = 0
    max_tier = max(achievements_progressionTiers.keys(), default=0) - infoTiers
    tiers = {category: 0 for category in achievement_categories}

    #Assess tiers
    for tierNumber, tierRequirements in achievements_progressionTiers.items():
        subgroupName = f"To reach Tier {tierNumber}"
        for categoryName, categoryAchievementsDict in tierRequirements.items():
            for achievementName, achievementDetailsDict in categoryAchievementsDict.items():
                    if not session_data.account.achievements.get(achievementName):
                        if subgroupName not in achievements_AdviceDict[categoryName]:
                            achievements_AdviceDict[categoryName][subgroupName] = []
                        achievements_AdviceDict[categoryName][subgroupName].append(Advice(
                            label=f"W{achievementDetailsDict['World']} {achievementName}: {achievementDetailsDict['Reward']}",
                            picture_class=achievementName,
                        ))
            if subgroupName not in achievements_AdviceDict[categoryName] and tiers[categoryName] == tierNumber - 1:
                tiers[categoryName] = tierNumber

    #Advice Group
    for category in achievement_categories:
        achievements_AdviceGroupDict[category] = AdviceGroup(
            tier=tiers[categoryName],
            pre_string=f"Complete achievements for {category}",
            advices=achievements_AdviceDict[category]
        )

    #Advice Section
    overall_AchievementsTier = min(max_tier + infoTiers, min(tiers.values()))
    tier_section = f"{overall_AchievementsTier}/{max_tier}"
    achievements_AdviceSection.pinchy_rating = overall_AchievementsTier
    achievements_AdviceSection.tier = tier_section
    achievements_AdviceSection.groups = achievements_AdviceGroupDict.values()
    if overall_AchievementsTier >= max_tier:
        achievements_AdviceSection.header = f"Best Achievements tier met: {tier_section}{break_you_best}️"
        achievements_AdviceSection.complete = True
    else:
        achievements_AdviceSection.header = f"Best Achievements tier met: {tier_section}"

    return achievements_AdviceSection
