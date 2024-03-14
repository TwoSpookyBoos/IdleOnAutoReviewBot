import json
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, progressionTiers

logger = get_logger(__name__)

def parseJSONtoLists():
    templateList = json.loads(session_data.account.raw_data["Template"])
    return templateList

def setTemplateProgressionTier():
    template_AdviceDict = {
    }
    template_AdviceGroupDict = {}
    template_AdviceSection = AdviceSection(
        name="Template",
        tier="Not Yet Evaluated",
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

