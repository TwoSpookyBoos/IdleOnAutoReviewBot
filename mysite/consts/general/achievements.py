from consts.progression_tiers import achievements_progressionTiers

# World and Reward are authored per achievement in the tier list
achievement_tier_info: dict[str, dict] = {
    name: info
    for tier in achievements_progressionTiers.values()
    for category in tier.values()
    for name, info in category.items()
}
