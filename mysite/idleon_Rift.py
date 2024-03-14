import json
from models import AdviceSection, AdviceGroup, Advice
from utils import pl, get_logger
from flask import g as session_data
from consts import maxTiersPerGroup, progressionTiers

logger = get_logger(__name__)

def parseJSONtoLists():
    templateList = json.loads(session_data.account.raw_data["Rift"])
    return templateList

def setRiftProgressionTier():
    rift_AdviceDict = {
    }
    rift_AdviceGroupDict = {}
    rift_AdviceSection = AdviceSection(
        name="Rift",
        tier="Not Yet Evaluated",
        header="Best Rift tier met: Not Yet Evaluated",
        picture=""
    )
    highestTemplateSkillLevel = max(session_data.account.all_skills["TemplateSkill"])
    if highestTemplateSkillLevel < 1:
        rift_AdviceSection.header = "Come back after unlocking Template!"
        return rift_AdviceSection

    tier_Template = 0
    max_tier = progressionTiers["Template"][-1][0]
    overall_TemplateTier = min(max_tier, tier_Template)
