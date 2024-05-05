from consts import sneakingGemstonesMaxValueDict
from models.models import AdviceSection, AdviceGroup, Advice
from utils.text_formatting import pl
from utils.logging import get_logger
from flask import g as session_data

logger = get_logger(__name__)

def setSneakingProgressionTier():
    sneaking_AdviceDict = {
        "Gemstones": []
    }
    sneaking_AdviceGroupDict = {}
    sneaking_AdviceSection = AdviceSection(
        name="Sneaking",
        tier="0",
        pinchy_rating=0,
        header="Best Sneaking tier met: Not Yet Evaluated",
        picture="Dojo_Ghost.gif"
    )
    highestSneakingSkillLevel = max(session_data.account.all_skills.get("Sneaking", [0]))
    if highestSneakingSkillLevel < 1:
        sneaking_AdviceSection.header = "Come back after unlocking the Sneaking skill in W6!"
        return sneaking_AdviceSection

    tier_Sneaking = 0
    max_tier = 0
    #Assess Gemstones
    for gemstoneName, gemstoneLevel in session_data.account.sneaking["Gemstones"].items():
        sneaking_AdviceDict["Gemstones"].append(Advice(
            label=f"{gemstoneName} (Level {session_data.account.sneaking.get('Gemstones', {}).get(gemstoneName, {}).get('Level', 0)}: {session_data.account.sneaking.get('Gemstones', {}).get(gemstoneName, {}).get('Value', 0):.2f} {session_data.account.sneaking.get('Gemstones', {}).get(gemstoneName, {}).get('Stat', '')})",
            picture_class=gemstoneName,
            progression=f"{session_data.account.sneaking.get('Gemstones', {}).get(gemstoneName, {}).get('Percent', 0):.2f}",
            goal=100,
            unit="%"
        ))
    # Generate AdviceGroups
    sneaking_AdviceGroupDict["Gemstones"] = AdviceGroup(
        tier="",
        pre_string="Percentage of Gemstone values",
        post_string="Formulas thanks to merlinthewizard1313",
        advices=sneaking_AdviceDict["Gemstones"]
    )

    # Generate AdviceSection
    overall_SneakingTier = min(max_tier, tier_Sneaking)
    tier_section = f"{overall_SneakingTier}/{max_tier}"
    sneaking_AdviceSection.tier = tier_section
    sneaking_AdviceSection.pinchy_rating = overall_SneakingTier
    sneaking_AdviceSection.groups = sneaking_AdviceGroupDict.values()
    if overall_SneakingTier == max_tier:
        sneaking_AdviceSection.header = f"Best Sneaking tier met: {tier_section}<br>You best ❤️"
    else:
        sneaking_AdviceSection.header = f"Best Sneaking tier met: {tier_section}"

    return sneaking_AdviceSection
