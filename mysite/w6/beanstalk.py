from collections import defaultdict

from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.consts_w6 import gfood_codes, BEANSTACK_GOAL, SUPER_BEANSTACK_GOAL
from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, Advice, AdviceGroup
from utils.text_formatting import getItemDisplayName
from flask import g as session_data


def getProgressionTiersAdviceSections():
    beanstalk_advice = {
        "Tiers": defaultdict(list)
    }

    optional_tiers = 1
    true_max = true_max_tiers['Beanstalk']
    max_tier = true_max - optional_tiers
    overall_section_tier = 0

    food_sources = {
        "Golden Peanut": "Smithing",
        "Golden Jam": "W1 Colo (efficient) or W6 Colo (fast)",
        "Golden Kebabs": "W2 Colo (efficient) or W6 Colo (fast)",
        "Golden Meat Pie": "W2 Crystals",
        "Golden Nomwich": "W1 Crystals",
        "Golden Ham": "W3 Crystals",
        "Golden Bread": "W3 Colo (efficient) or W5 Colo (fast)",
        "Golden Ribs": "W4 Crystals",
        "Golden Cheese": "W3 Crystals",
        "Golden Grilled Cheese Nomwich": "W5 Crystals",
        "Golden Hampter Gummy Candy": "W5 Crystals",
        "Golden Nigiri": "W6 Crystals",
        "Golden Dumpling": "W6 Crystals",
        "Golden Cake": "Smithing",
        "Butter Bar": "Catching Butterflies"
    }

    def get_food_advice_label(food_code):
        food_name = getItemDisplayName(food_code)
        return f"{food_name}: {food_sources[food_name]}"

    super_beanstack_bought = session_data.account.sneaking['JadeEmporium']['Supersized Gold Beanstacking']['Obtained']
    # Assets contains totals from Storage and inventories
    gold_foods = dict.fromkeys(gfood_codes, 0)
    optional_gold_foods = ["ButterBar", "FoodG4"]
    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.all_assets.get(gfood).amount

    gold_food_levels = dict.fromkeys(gfood_codes, 0)
    for golden_food, data in session_data.account.sneaking["Beanstalk"].items():
        if data["Beanstacked"]:
            gold_food_levels[golden_food] += 1
        if data["SuperBeanstacked"]:
            gold_food_levels[golden_food] += 1

    # Reach Tier 1: 10k for all non-optional
    tier_0_foods = [golden_food for golden_food, tier in gold_food_levels.items() if golden_food not in optional_gold_foods and tier == 0]
    if len(tier_0_foods) == 0:
        overall_section_tier = 1

    beanstalk_advice["Tiers"][build_subgroup_label(1, max_tier) + ": Collect 10,000 of these Golden Foods"] = sorted([
        Advice(
            label=get_food_advice_label(golden_food_code),
            picture_class=getItemDisplayName(golden_food_code),
            progression=f"{int(gold_foods[golden_food_code]) / BEANSTACK_GOAL :.02%}",
            goal="100%",
        ) for golden_food_code in tier_0_foods],
        key=lambda advice: float(advice.progression.strip("%")),
        reverse=True
    )

    # Reach Tier 2 (Practical Max): 100k for all non-optional
    tier_1_foods = [golden_food for golden_food, tier in gold_food_levels.items() if golden_food not in optional_gold_foods and tier == 1]
    if len(tier_0_foods) == 0 and len(tier_1_foods) == 0:
        overall_section_tier = 2

    buy_jade_emporium_upgrade_advice = [Advice(
        label='Buy "Supersized Gold Beanstacking" from the {{ Jade Emporium|#sneaking }}',
        picture_class='supersized-gold-beanstacking',
    )] if not super_beanstack_bought else []

    beanstalk_advice["Tiers"][build_subgroup_label(2, max_tier) + ": Collect 100,000 of these Golden Foods"] = buy_jade_emporium_upgrade_advice + sorted([
        Advice(
            label=get_food_advice_label(golden_food_code),
            picture_class=getItemDisplayName(golden_food_code),
            progression=f"{int(gold_foods[golden_food_code]) / SUPER_BEANSTACK_GOAL :.02%}",
            goal="100%",
        ) for golden_food_code in tier_1_foods],
        key=lambda advice: float(advice.progression.strip("%")),
        reverse=True
    )

    # Reach Tier 3 (True Max): 10k/100k for optional foods
    optional_tier_0_foods = [golden_food for golden_food, tier in gold_food_levels.items() if golden_food in optional_gold_foods and tier == 0]
    optional_tier_1_foods = [golden_food for golden_food, tier in gold_food_levels.items() if golden_food in optional_gold_foods and tier <= 1]
    if len(tier_0_foods) == 0 and len(tier_1_foods) == 0 and len(optional_tier_1_foods) == 0:
        overall_section_tier = 3

    optional_food_advices = []
    optional_food_advices += [
        Advice(
            label=get_food_advice_label(golden_food_code) + " (10k)",
            picture_class=getItemDisplayName(golden_food_code),
            progression=f"{int(gold_foods[golden_food_code]) / BEANSTACK_GOAL :.02%}",
            goal="100%",
        ) for golden_food_code in optional_tier_0_foods
    ]
    optional_food_advices += [
        Advice(
            label=get_food_advice_label(golden_food_code) + " (100k)",
            picture_class=getItemDisplayName(golden_food_code),
            progression=f"{int(gold_foods[golden_food_code]) / SUPER_BEANSTACK_GOAL :.02%}",
            goal="100%",
        ) for golden_food_code in optional_tier_1_foods
    ]

    beanstalk_advice["Tiers"][build_subgroup_label(3, max_tier)] = sorted(
        optional_food_advices,
        key=lambda advice: float(advice.progression.strip("%")),
        reverse=True
    )

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
        header=(
            f"Best Beanstalk tier met: {tier_section}" if overall_SectionTier < max_tier
            else f"Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯{break_you_best}"
        ),
        picture='Beanstalk.png',
        groups=beanstalk_AdviceGroups.values(),
    )

    return beanstalk_AdviceSection
