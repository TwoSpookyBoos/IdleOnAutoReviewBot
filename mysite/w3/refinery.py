
from consts.consts_autoreview import break_keep_it_up, EmojiType
from consts.consts_w3 import refinery_max_powerpercycle, refinery_max_rank_panda, refinery_max_rank_no_panda
from consts.progression_tiers import true_max_tiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from utils.logging import get_logger

logger = get_logger(__name__)

def getRefineryProgressionTierAdviceGroups():
    refinery_AdviceDict = {
        'AutoRefine': [],
        'Merits': [],
        'ExcessAndDeficits': [],
        'Tab1Ranks': [],
        'Tab2Ranks': [],
    }
    refinery_AdviceGroupDict = {}
    optional_tiers = 0
    true_max = true_max_tiers['Refinery']
    max_tier = true_max - optional_tiers
    tier_AutoRefine = 1
    tier_W3Merits = 1
    refinery = session_data.account.refinery

    # AutoRefine and On/Off Advice
    if not refinery['Red'].running:
        if refinery['Red'].rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{refinery['Red'].name} Production: Off",
                picture_class=refinery['Red'].image,
                progression='Off',
                goal='On'
            ))
            session_data.account.alerts_Advices['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} is not producing",
                picture_class=refinery['Red'].image
            ))
    if refinery['Red'].auto_refine != 0:
        if refinery['Red'].rank < 100:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{refinery['Red'].name} Auto Refine: ON",
                picture_class=refinery['Red'].image,
                progression='ON',
                goal='OFF'
            ))
            session_data.account.alerts_Advices['World 3'].append(Advice(
                label=f"{{{{ Red Salt|#refinery }}}} is set to Auto Refine: ON. Recommended to reach Rank 100+ before enabling Auto Refine.",
                picture_class=refinery['Red'].image
            ))

    if not refinery['Green'].running:
        if refinery['Green'].rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{refinery['Green'].name} Production: Off",
                picture_class=refinery['Green'].image,
                progression='Off',
                goal='On'
            ))
            session_data.account.alerts_Advices['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} is not producing",
                picture_class=refinery['Green'].image
            ))
    if refinery['Green'].auto_refine != 0:
        if refinery['Green'].rank < 30:
            tier_AutoRefine = 0
            refinery_AdviceDict['AutoRefine'].append(Advice(
                label=f"{refinery['Green'].name} Auto Refine: ON",
                picture_class=refinery['Green'].image,
                progression='ON',
                goal='OFF'
            ))
            session_data.account.alerts_Advices['World 3'].append(Advice(
                label=f"{{{{ Green Salt|#refinery }}}} is set to Auto Refine: ON. Recommended to reach Rank 30+ before enabling Auto Refine.",
                picture_class=refinery['Green'].image
            ))

    # W3Merits Advice
    sum_salts_rank2_plus = 0
    if refinery['Orange'].rank >= 2:
        sum_salts_rank2_plus += 1
    if refinery['Blue'].rank >= 2:
        sum_salts_rank2_plus += 1
    if refinery['Green'].rank >= 2:
        sum_salts_rank2_plus += 1
    if refinery['Purple'].rank >= 2:
        sum_salts_rank2_plus += 1
    if refinery['Nullo'].rank >= 2:
        sum_salts_rank2_plus += 1
    if session_data.account.merits[2][6].level < sum_salts_rank2_plus:
        tier_W3Merits = 0
        refinery_AdviceDict['Merits'].append(Advice(
                label='W3 Taskboard Merits Purchased',
                picture_class='iceland-irwin',
                progression=session_data.account.merits[2][6].level,
                goal=sum_salts_rank2_plus
        ))

    # Excess and Deficits Advice
    for salt in refinery.values():
        output_maxed_note = (
            f"<br>Power Per Cycle max of {int(refinery_max_powerpercycle):,} has been reached! "
            f"Ranking up won't create any more Salts per cycle."
            if salt.output_maxed
            else ''
        )
        refinery_AdviceDict['ExcessAndDeficits'].append(Advice(
            label=f"Rank {salt.rank} {salt.name} Salt: {salt.excess_or_deficit}"
                  f"{output_maxed_note}",
            picture_class=salt.image,
            goal=f"{salt.excess_amount:,}"
        ))

    # Ranks Advice
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Red Salt',
        picture_class=refinery['Red'].image,
        progression=refinery['Red'].rank,
        goal=(
            refinery['Red'].rank if refinery['Red'].output_maxed
            else refinery_max_rank_panda if session_data.account.companions.has('Panda')
            else refinery_max_rank_no_panda
        )
    ))
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Orange Salt',
        picture_class=refinery['Orange'].image,
        progression=refinery['Orange'].rank,
        goal=refinery['Orange'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab1Ranks'].append(Advice(
        label='Blue Salt',
        picture_class=refinery['Blue'].image,
        progression=refinery['Blue'].rank,
        goal=refinery['Blue'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Green Salt',
        picture_class=refinery['Green'].image,
        progression=refinery['Green'].rank,
        goal=(
            refinery['Green'].rank if refinery['Green'].output_maxed
            else refinery_max_rank_panda if session_data.account.companions.has('Panda')
            else refinery_max_rank_no_panda
        )
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Purple Salt',
        picture_class=refinery['Purple'].image,
        progression=refinery['Purple'].rank,
        goal=refinery['Purple'].max_rank_with_excess
    ))
    refinery_AdviceDict['Tab2Ranks'].append(Advice(
        label='Nullo Salt',
        picture_class=refinery['Nullo'].image,
        progression=refinery['Nullo'].rank,
        goal=refinery['Nullo'].max_rank_with_excess
    ))

    # Generate AdviceGroups
    refinery_AdviceGroupDict['AutoRefine'] = AdviceGroup(
        tier=tier_AutoRefine,
        pre_string="Red and Green Salts should be ENABLED and set to Auto Refine: OFF to allow ranking up",
        advices=refinery_AdviceDict['AutoRefine']
    )
    refinery_AdviceGroupDict['Merits'] = AdviceGroup(
        tier=tier_W3Merits,
        pre_string='W3 Salt Merits Purchased',
        advices=refinery_AdviceDict['Merits'],
        post_string='Leveling this Merit would immediately decrease salt consumption.'
    )
    refinery_AdviceGroupDict['ExcessAndDeficits'] = AdviceGroup(
        tier='',
        pre_string='Salt Excess/Deficit per Synthesis Cycle',
        advices=refinery_AdviceDict['ExcessAndDeficits'],
        informational=True,
        completed=all([int(advice.goal.replace(',', '')) >= 0 for advice in refinery_AdviceDict['ExcessAndDeficits']])
    )
    refinery_AdviceGroupDict['Tab1Ranks'] = AdviceGroup(
        tier='',
        pre_string='Max Tab1 Ranks without causing a Salt Deficit',
        advices=refinery_AdviceDict['Tab1Ranks'],
        post_string=f"Or just YOLO rank up everything if balancing is too much of a pain {EmojiType.WIDE_SHRUG.value}",
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab1Ranks']])
    )
    refinery_AdviceGroupDict['Tab2Ranks'] = AdviceGroup(
        tier='',
        pre_string='Max Tab2 Ranks without causing a Salt Deficit',
        advices=refinery_AdviceDict['Tab2Ranks'],
        post_string='',
        informational=True,
        completed=all([advice.progression >= advice.goal for advice in refinery_AdviceDict['Tab2Ranks']])
    )
    overall_SectionTier = min(true_max, tier_AutoRefine, tier_W3Merits)
    return refinery_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getConsRefineryAdviceSection() -> AdviceSection:
    highest_construction_level = max(session_data.account.characters.all_skills['Construction'])
    if highest_construction_level < 1:
        return AdviceSection(
            name='Refinery',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Construction skill in World 3!',
            picture='Construction_Refinery.gif',
            unreached=True
        )

    #Generate AdviceGroups
    refinery_AdviceGroupDict, overall_SectionTier, max_tier, true_max = getRefineryProgressionTierAdviceGroups()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    return AdviceSection(
        name='Refinery',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Refinery tier met: {tier_section}{break_keep_it_up if overall_SectionTier >= max_tier else ''}",
        picture='Construction_Refinery.gif',
        groups=refinery_AdviceGroupDict.values(),
        collapse=False
    )
