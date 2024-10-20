from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts import template_progressionTiers, break_you_best

logger = get_logger(__name__)

def setTemplateProgressionTier():
    template_AdviceDict = {
    }
    template_AdviceGroupDict = {}
    template_AdviceSection = AdviceSection(
        name="Template",
        tier="0",
        pinchy_rating=0,
        header="Best Template tier met: Not Yet Evaluated",
        picture="",
        complete=False,
        unrated=False,
    )
    highestTemplateSkillLevel = max(session_data.account.all_skills["TemplateSkill"])
    if highestTemplateSkillLevel < 1:
        template_AdviceSection.header = "Come back after unlocking Template!"
        return template_AdviceSection

    infoTiers = 0
    max_tier = max(template_progressionTiers.keys(), default=0) - infoTiers
    tier_Template = 0

    overall_TemplateTier = min(max_tier + infoTiers, tier_Template)
    tier_section = f"{overall_TemplateTier}/{max_tier}"
    template_AdviceSection.pinchy_rating = overall_TemplateTier
    template_AdviceSection.tier = tier_section
    template_AdviceSection.groups = template_AdviceGroupDict.values()
    if overall_TemplateTier >= max_tier:
        template_AdviceSection.header = f"Best Template tier met: {tier_section}{break_you_best}️"
        template_AdviceSection.complete = True
    else:
        template_AdviceSection.header = f"Best Template tier met: {tier_section}"

    return template_AdviceSection
