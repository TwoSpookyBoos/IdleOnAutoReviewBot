from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.logging import get_logger
from flask import g as session_data
from consts.consts_autoreview import break_you_best, build_subgroup_label

logger = get_logger(__name__)

def getProgressionTiersAdviceGroup() -> tuple[AdviceGroup, int, int, int]:
    template_Advices = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers.get('Template', 0)
    max_tier = true_max - optional_tiers
    tier_Template = 0

    #Assess Tiers
    for tier_number, requirements in template_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        if subgroup_label not in template_Advices['Tiers'] and tier_Template == tier_number - 1:
            tier_Template = tier_number

    tiers_ag = AdviceGroup(
        tier=tier_Template,
        pre_string='Progression Tiers',
        advices=template_Advices['Tiers']
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
    )

    return template_AdviceSection
