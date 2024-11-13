from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from flask import g as session_data
from consts import (
    break_you_best, infinity_string,
    #template_progressionTiers
)

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int]:
    template_AdviceDict = {
        'Tiers': {},
    }
    info_tiers = 0
    max_tier = 0  #max(template_progressionTiers.keys(), default=0) - info_tiers
    tier_Template = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Template,
        pre_string="Progression Tiers",
        advices=template_AdviceDict['Tiers']
    )
    overall_SectionTier = min(max_tier + info_tiers, tier_Template)
    return tiers_ag, overall_SectionTier, max_tier

def getTemplateAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    highestTemplateSkillLevel = max(session_data.account.all_skills["TemplateSkill"])
    if highestTemplateSkillLevel < 1:
        template_AdviceSection = AdviceSection(
            name="Template",
            tier="Not Yet Evaluated",
            header="Come back after unlocking Template!",
            picture="",
            unrated=None,
            unreached=True,
            completed=False
        )
        return template_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    template_AdviceGroupDict = {}
    template_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier = getProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    template_AdviceSection = AdviceSection(
        name="Template",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=f"Best Template tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="",
        groups=template_AdviceGroupDict.values(),
        completed=None,
        unrated=None,
    )

    return template_AdviceSection
