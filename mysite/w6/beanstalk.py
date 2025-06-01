from consts.consts_autoreview import break_you_best
from consts.consts_w6 import gfood_codes, BEANSTACK_GOAL, SUPER_BEANSTACK_GOAL
from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, Advice, AdviceGroup
from utils.text_formatting import getItemDisplayName
from flask import g as session_data


def getProgressionTiersAdviceSections():
    beanstalk_Advices = {}

    optional_tiers = 0
    true_max = true_max_tiers['Beanstalk']
    max_tier = true_max - optional_tiers

    super_beanstack_bought = session_data.account.sneaking['JadeEmporium']['Supersized Gold Beanstacking']['Obtained']

    # Assets contains totals from Storage and inventories
    gold_foods = dict.fromkeys(gfood_codes, 0)
    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.all_assets.get(gfood).amount

    foods_ready_to_deposit = []  # Food ready to deposit, including a tag in the name for 10k or 100k
    foods_to_beanstack = []  # If food is not already Beanstacked and player has less than required amount (10k)
    foods_to_deposit_for_beanstack = []  # If food is not already Beanstacked and player has enough to do so
    for food_name, food_values_dict in session_data.account.sneaking['Beanstalk'].items():
        if not food_values_dict['Beanstacked']:
            if gold_foods[food_name] < BEANSTACK_GOAL:
                foods_to_beanstack.append(food_name)
            else:
                foods_ready_to_deposit.append(f"{getItemDisplayName(food_name)}: 10k Beanstack")
                foods_to_deposit_for_beanstack.append(food_name)

    super_beanstack_progress: dict[str, int] = dict()
    for gold_food_code, total_owned in gold_foods.items():
        # Remove 10k from the amount of gold food owned if the first 10k hasn't been deposited yet
        adjusted_total_owned = (
            total_owned
            if session_data.account.sneaking['Beanstalk'][gold_food_code]['Beanstacked']
            else total_owned - BEANSTACK_GOAL
        )

        # mark progress as 0% if less than 10k is owned
        super_beanstack_progress[gold_food_code] = max(0, adjusted_total_owned)

    foods_to_super_beanstack = []  # If food is not already Beanstacked and player has less than required amount (10k)
    for food_name, food_values_dict in session_data.account.sneaking['Beanstalk'].items():
        if not food_values_dict['SuperBeanstacked']:
            if super_beanstack_progress[food_name] < SUPER_BEANSTACK_GOAL:
                foods_to_super_beanstack.append(food_name)
            else:
                foods_ready_to_deposit.append(f"{getItemDisplayName(food_name)}: 100k Super Beanstack")

    foods_finished = sum([v['Beanstacked'] + v['SuperBeanstacked'] for v in session_data.account.sneaking['Beanstalk'].values()])

    beanstalk_Advices['Ready for Deposit'] = [
        Advice(
            label=food_name,
            picture_class=food_name.split(":")[0],
            completed=False
        )
        for food_name in foods_ready_to_deposit
    ]
    if len(foods_ready_to_deposit) > 0:
        session_data.account.alerts_Advices['World 6'].append(Advice(
            label=f"Golden Food ready for {{{{Beanstalk|#beanstalk}}}}",
            picture_class="beanstalk",
            unrated=True
        ))

    beanstalk_Advices['Beanstack'] = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / BEANSTACK_GOAL :.02%}",
            goal='100%'
        )
        for codename in foods_to_beanstack
    ]

    beanstalk_Advices['Super Beanstack'] = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(super_beanstack_progress[codename]) / SUPER_BEANSTACK_GOAL :.02%}",
            goal='100%'
        )
        for codename in foods_to_super_beanstack
    ]

    #Generate AdviceGroups
    beanstalk_AdviceGroupDict = {}
    if not super_beanstack_bought:
        beanstalk_AdviceGroupDict['Upgrade'] = AdviceGroup(
            tier='',
            pre_string='Upgrade the Beanstalk to enhance Golden Food beanstacks further',
            advices=[
                Advice(
                    label='Buy "Supersized Gold Beanstacking" from the {{ Jade Emporium|#sneaking }}',
                    picture_class='supersized-gold-beanstacking',
                )
            ],
            informational=False,
            completed=False
        )
    beanstalk_AdviceGroupDict['Ready for Deposit'] = AdviceGroup(
        tier='',
        pre_string='Golden Foods ready for deposit',
        advices=beanstalk_Advices['Ready for Deposit'],
        informational=True,
        completed=False
    )

    beanstalk_AdviceGroupDict['Beanstack'] = AdviceGroup(
        tier='',
        pre_string='Collect 10,000 of these Golden Foods',
        advices=beanstalk_Advices['Beanstack'],
        informational=True,
    )
    beanstalk_AdviceGroupDict['Beanstack'].sort_advices(True)

    if super_beanstack_bought:
        beanstalk_AdviceGroupDict['Super Beanstack'] = AdviceGroup(
            tier='',
            pre_string='Collect another 100,000 of these Golden Foods',
            advices=beanstalk_Advices['Super Beanstack'],
            informational=True,
        )
        beanstalk_AdviceGroupDict['Super Beanstack'].sort_advices(True)

    overall_SectionTier = min(true_max, foods_finished)
    return beanstalk_AdviceGroupDict, overall_SectionTier, max_tier, true_max

def getBeanstalkAdviceSection() -> AdviceSection:
    if not session_data.account.sneaking['JadeEmporium']["Gold Food Beanstalk"]['Obtained']:
        return AdviceSection(
            name='Beanstalk',
            tier='',
            header="Come back after unlocking \"Gold Food Beanstalk\" from the Jade Emporium",
            picture='Jade_Vendor.gif',
            unreached=True,
            unrated=True
        )
    #Generate AdviceGroups
    beanstalk_AdviceGroups, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceSections()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    beanstalk_AdviceSection = AdviceSection(
        name='Beanstalk',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=(
            f"You have upgraded the Beanstalk {tier_section} times" if overall_SectionTier < max_tier
            else f"Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯{break_you_best}"
        ),
        picture='Beanstalk.png',
        groups=beanstalk_AdviceGroups.values(),
        unrated=True,
    )

    return beanstalk_AdviceSection
