from consts import gfood_codes
from models.models import AdviceSection, Advice, AdviceGroup
from utils.text_formatting import getItemDisplayName
from flask import g as session_data

BEANSTACK_GOAL = 10**4
SUPER_BEANSTACK_GOAL = 10**5


def section_beanstalk():
    upgrade_bought = session_data.account.sneaking['JadeEmporium']["Supersized Gold Beanstacking"]['Obtained']

    if not session_data.account.sneaking['JadeEmporium']["Gold Food Beanstalk"]['Obtained']:
        return AdviceSection(
            name="Beanstalk",
            tier="",
            header="Come back once you've bought the \"Gold Food Beanstalk\" from the Jade Emporium",
            picture="Jade_Vendor.gif",
            collapse=True,
        )

    gold_foods = dict.fromkeys(gfood_codes, 0)

    # Assets contains totals from Storage and inventories
    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.assets.get(gfood).amount

    # Also include the amounts equipped on characters
    for toon in session_data.account.safe_characters:
        for food in toon.equipment.foods:
            if food.codename in gold_foods:
                gold_foods[food.codename] += food.amount

    foods_ready_to_deposit = []  # Food ready to deposit, including a tag in the name for 10k or 100k
    foods_to_beanstack = []  # If food is not already Beanstacked and player has less than required amount (10k)
    foods_to_deposit_for_beanstack = []  # If food is not already Beanstacked and player has enough to do so
    for foodName, foodValuesDict in session_data.account.sneaking['Beanstalk'].items():
        if not foodValuesDict['Beanstacked']:
            if gold_foods[foodName] < BEANSTACK_GOAL:
                foods_to_beanstack.append(foodName)
            else:
                foods_ready_to_deposit.append(f"{getItemDisplayName(foodName)}: 10k Beanstack")
                foods_to_deposit_for_beanstack.append(foodName)

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
    for foodName, foodValuesDict in session_data.account.sneaking['Beanstalk'].items():
        if not foodValuesDict['SuperBeanstacked']:
            if super_beanstack_progress[foodName] < SUPER_BEANSTACK_GOAL:
                foods_to_super_beanstack.append(foodName)
            else:
                foods_ready_to_deposit.append(f"{getItemDisplayName(foodName)}: 100k Super Beanstack")

    foods_finished = sum([v['Beanstacked'] + v['SuperBeanstacked'] for v in session_data.account.sneaking['Beanstalk'].values()])
    tier = f"{foods_finished}/{len(gold_foods)*2}"

    advice_deposit = [
        Advice(
            label=foodname,
            picture_class=foodname.split(":")[0],
        )
        for foodname in foods_ready_to_deposit
    ]

    advice_beanstack = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / BEANSTACK_GOAL:.02%}",
        )
        for codename in foods_to_beanstack
    ]

    advice_super_beanstack = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(super_beanstack_progress[codename]) / SUPER_BEANSTACK_GOAL:.02%}",
        )
        for codename in foods_to_super_beanstack
    ]

    group_upgrade = AdviceGroup(
        tier="",
        pre_string="Upgrade the Beanstalk to enhance Golden Food beanstacks further",
        advices=[
            Advice(
                label='Buy "Supersized Gold Beanstacking" from the {{ Jade Emporium|#sneaking }}',
                picture_class="supersized-gold-beanstacking",
            )
        ],
    )

    group_deposit = AdviceGroup(
        tier="",
        pre_string="Golden Foods ready for deposit",
        advices=advice_deposit,
    )

    group_beanstack = AdviceGroup(
        tier="",
        pre_string="Collect 10,000 of these Golden Foods",
        advices=advice_beanstack,
    )
    group_beanstack.sort_advices(True)

    group_super_beanstack = (
        AdviceGroup(
            tier="",
            pre_string="Collect another 100,000 of these Golden Foods",
            advices=advice_super_beanstack,
        )
        if upgrade_bought
        else None
    )
    if group_super_beanstack:
        group_super_beanstack.sort_advices(True)

    header = (
        "Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯"
        if foods_finished == len(gold_foods)
        else f"You have upgraded the Beanstalk {tier} times"
    )

    groups = [
        group_deposit,
        group_beanstack,
        (group_super_beanstack if upgrade_bought else group_upgrade),
    ]

    beanstalk_AdviceSection = AdviceSection(
        name="Beanstalk",
        tier=tier,
        header=header,
        picture="Beanstalk.png",
        groups=groups,
        complete=True if not groups else False
    )

    return beanstalk_AdviceSection
