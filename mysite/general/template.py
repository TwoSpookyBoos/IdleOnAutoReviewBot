import json
from models.models import AdviceSection
from utils.logging import get_logger
from flask import g as session_data
from consts import progressionTiers

logger = get_logger(__name__)

def parseJSONtoLists():
    rawTemplate = session_data.account.raw_data.get("Template", [])
    if isinstance(rawTemplate, str):
        rawCooking = json.loads(rawTemplate)
    return rawTemplate

def setTemplateProgressionTier():
    template_AdviceDict = {
    }
    template_AdviceGroupDict = {}
    template_AdviceSection = AdviceSection(
        name="Template",
        tier="0",
        pinchy_rating=0,
        header="Best Template tier met: Not Yet Evaluated",
        picture=""
    )
    highestTemplateSkillLevel = max(session_data.account.all_skills["TemplateSkill"])
    if highestTemplateSkillLevel < 1:
        template_AdviceSection.header = "Come back after unlocking Template!"
        return template_AdviceSection

    tier_Template = 0
    max_tier = progressionTiers["Template"][-1][0]
    overall_TemplateTier = min(max_tier, tier_Template)
