from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w6 import gfood_codes, BEANSTACK_GOAL, SUPER_BEANSTACK_GOAL, gfood_data
from consts.progression_tiers import true_max_tiers, beanstalk_progressionTiers
from models.models import AdviceSection, Advice, AdviceGroup
from utils.text_formatting import getItemDisplayName
from flask import g as session_data
from utils.logging import get_logger

logger = get_logger(__name__)


def get_food_advice_label(food_code):
    food_name = getItemDisplayName(food_code)
    return f"{food_name}: {gfood_data[food_name]["Source"]}"

def getProgressionTiersAdviceSections():
    beanstalk_advice = {
        'Tiers': {}
    }

    optional_tiers = 1
    true_max = true_max_tiers['Beanstalk']
    max_tier = true_max - optional_tiers
    tier_stacks = 0

    super_beanstack_bought = session_data.account.sneaking['JadeEmporium']['Supersized Gold Beanstacking']['Obtained']

    # Assets contains totals from Storage and inventories
    gold_foods = dict.fromkeys(gfood_codes, 0)
    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.all_assets.get(gfood).amount

    for tier_number, requirements in beanstalk_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        #10k
        for gold_food in requirements.get('10k', []):
            if not session_data.account.sneaking['Beanstalk'][gold_food]['Beanstacked']:
                if (
                    subgroup_label not in beanstalk_advice['Tiers']
                    and len(beanstalk_advice['Tiers']) < session_data.account.max_subgroups
                ):
                    beanstalk_advice['Tiers'][subgroup_label] = []
                if subgroup_label in beanstalk_advice['Tiers']:
                    beanstalk_advice['Tiers'][subgroup_label].append(Advice(
                        label=f"10k: {get_food_advice_label(gold_food)}",
                        picture_class=getItemDisplayName(gold_food),
                        progression=f"{min(1000, int(gold_foods[gold_food]) / BEANSTACK_GOAL) :.02%}",
                        goal="100%",
                        resource=gfood_data.get(getItemDisplayName(gold_food), {"Resource Image": ""})["Resource Image"]
                    ))

        #SuperBeanstack purchased
        if requirements.get('SuperBeanstack Purchased', False):
            if not super_beanstack_bought:
                if (
                    subgroup_label not in beanstalk_advice['Tiers']
                    and len(beanstalk_advice['Tiers']) < session_data.account.max_subgroups
                ):
                    beanstalk_advice['Tiers'][subgroup_label] = []
                if subgroup_label in beanstalk_advice['Tiers']:
                    beanstalk_advice['Tiers'][subgroup_label].append(Advice(
                        label=f"Purchase \"Supersized Gold Beanstacking\" from the Jade Emporium",
                        picture_class=session_data.account.sneaking['JadeEmporium']['Supersized Gold Beanstacking']['Image'],
                        progression=0,
                        goal=1
                    ))

        # 100k
        for gold_food in requirements.get('100k', []):
            if not session_data.account.sneaking['Beanstalk'][gold_food]['SuperBeanstacked']:
                if (
                    subgroup_label not in beanstalk_advice['Tiers']
                    and len(beanstalk_advice['Tiers']) < session_data.account.max_subgroups
                ):
                    beanstalk_advice['Tiers'][subgroup_label] = []
                if subgroup_label in beanstalk_advice['Tiers']:
                    beanstalk_advice['Tiers'][subgroup_label].append(Advice(
                        label=f"100k: {get_food_advice_label(gold_food)}",
                        picture_class=getItemDisplayName(gold_food),
                        progression=f"{min(1000, int(gold_foods[gold_food]) / SUPER_BEANSTACK_GOAL) :.02%}",
                        goal="100%",
                        resource=gfood_data.get(getItemDisplayName(gold_food), {"Resource Image": ""})["Resource Image"]
                    ))

        # Final tier check
        if subgroup_label not in beanstalk_advice['Tiers'] and tier_stacks == tier_number - 1:
            tier_stacks = tier_number

    overall_section_tier = min(true_max, tier_stacks)
    beanstalk_advice_group = {}
    tier_advice_group = AdviceGroup(
        tier=overall_section_tier,
        pre_string='Deposit Golden Foods to the Beanstalk',
        advices=beanstalk_advice['Tiers'],
    )
    tier_advice_group.remove_empty_subgroups()
    beanstalk_advice_group['Tiers'] = tier_advice_group
    return beanstalk_advice_group, overall_section_tier, max_tier, true_max


def getBeanstalkAdviceSection() -> AdviceSection:
    if not session_data.account.sneaking['JadeEmporium']["Gold Food Beanstalk"]['Obtained']:
        return AdviceSection(
            name='Beanstalk',
            tier='',
            header="Come back after unlocking \"Gold Food Beanstalk\" from the Jade Emporium",
            picture='Jade_Vendor.gif',
            unreached=True,
        )
    # Generate AdviceGroups
    beanstalk_AdviceGroups, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceSections()

    # Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    beanstalk_AdviceSection = AdviceSection(
        name='Beanstalk',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Beanstalk tier met: {tier_section}{break_you_best if overall_SectionTier >= max_tier else ''}",
        picture='Beanstalk.png',
        groups=beanstalk_AdviceGroups.values(),
    )

    return beanstalk_AdviceSection
