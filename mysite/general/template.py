from consts.progression_tiers_updater import true_max_tiers
from models.models import AdviceSection, AdviceGroup
from utils.logging import get_logger
from flask import g as session_data
from consts.consts import break_you_best

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    template_AdviceDict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Template']
    max_tier = true_max - optional_tiers
    tier_Template = 0

    #Assess Tiers

    tiers_ag = AdviceGroup(
        tier=tier_Template,
        pre_string='Progression Tiers',
        advices=template_AdviceDict['Tiers']
    )
    overall_SectionTier = min(true_max, tier_Template)
    return tiers_ag, overall_SectionTier, max_tier, true_max

def getTemplateAdviceSection() -> AdviceSection:
    #Check if player has reached this section
    highestTemplateSkillLevel = max(session_data.account.all_skills['TemplateSkill'])
    if highestTemplateSkillLevel < 1:
        template_AdviceSection = AdviceSection(
            name='Template',
            tier='Not Yet Evaluated',
            header='Come back after unlocking Template!',
            picture='',
            unrated=None,
            unreached=True,
            completed=False
        )
        return template_AdviceSection

    #Generate Alert Advice

    #Generate AdviceGroups
    template_AdviceGroupDict = {}
    template_AdviceGroupDict['Tiers'], overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceGroup()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    template_AdviceSection = AdviceSection(
        name="Template",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Template tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture="",
        groups=template_AdviceGroupDict.values(),
        completed=None,
        unrated=None,
    )

    return template_AdviceSection
