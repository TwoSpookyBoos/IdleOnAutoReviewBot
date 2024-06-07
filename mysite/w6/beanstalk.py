from models.models import AdviceSection, Advice, AdviceGroup
from utils.data_formatting import safe_loads
from utils.text_formatting import getItemDisplayName
from flask import g as session_data

TEN_K = 1
HUNNIT_K = 2

BEANSTACK_GOAL = 10**4
SUPER_BEANSTACK_GOAL = 10**5


def __get_ninja_section(raw):
    default = "[]"
    return safe_loads(raw.get("Ninja", default))


def __get_beanstalk_data(raw):
    if ninja_section := __get_ninja_section(raw):
        return ninja_section[-4]
    else:
        return []


def section_beanstalk():
    beanstalk_bought = "Gold Food Beanstalk" in session_data.account.jade_emporium_purchases
    upgrade_bought = "Supersized Gold Beanstacking" in session_data.account.jade_emporium_purchases
    beanstalk_data = __get_beanstalk_data(session_data.account.raw_data)

    if not (beanstalk_bought and beanstalk_data):
        return AdviceSection(
            name="Giant Beanstalk",
            tier="",
            header="Come back once you've bought the \"Gold Food Beanstalk\" from the Jade Emporium",
            picture="Jade_Vendor.gif",
            collapse=False,
        )

    gfood_codes = ["PeanutG", "ButterBar", *[f"FoodG{i}" for i in range(1, 14)]]
    gold_foods = dict.fromkeys(gfood_codes, 0)
    beanstalk_status = dict(zip(gfood_codes, beanstalk_data))

    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.assets.get(gfood).amount

    for toon in session_data.account.safe_characters:
        for food in toon.equipment.foods:
            if food.codename not in beanstalk_status:
                continue

            gold_foods[food.codename] += food.amount

    foods_to_beanstack = [k for k, v in beanstalk_status.items() if v < TEN_K and gold_foods[k] < BEANSTACK_GOAL]
    foods_to_deposit_for_beanstack = [
        k for k, v in beanstalk_status.items() if v < TEN_K and k not in foods_to_beanstack
    ]

    super_beanstack_progress: dict[str, int] = dict()
    for gold_food_code in gold_foods:
        total_owned = gold_foods[gold_food_code]

        # remove 10k from the amount of gold food owned if the first 10k hasn't been collected or deposited yet
        adjusted_total_owned = (
            total_owned
            if gold_food_code not in (foods_to_deposit_for_beanstack + foods_to_beanstack)
            else total_owned - BEANSTACK_GOAL
        )

        # mark progress as 0% if less than 10k is owned
        super_beanstack_progress[gold_food_code] = max(0, adjusted_total_owned)

    foods_to_super_beanstack = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and super_beanstack_progress[k] < SUPER_BEANSTACK_GOAL
    ]
    foods_to_deposit_for_super_beanstack = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and k not in foods_to_super_beanstack
    ]

    foods_to_deposit = foods_to_deposit_for_beanstack + foods_to_deposit_for_super_beanstack * upgrade_bought

    foods_finished = sum(beanstalk_status.values())
    tier = f"{foods_finished}/{len(gold_foods)*2}"

    advice_deposit = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
        )
        for codename in foods_to_deposit
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
        pre_string="Upgrade the Beanstalk to upgrade foods further",
        advices=[
            Advice(
                label='Buy "Supersized Gold Beanstacking" from the Jade Emporium',
                picture_class="supersized-gold-beanstacking",
            )
        ],
    )

    group_deposit = AdviceGroup(
        tier="",
        pre_string="Deposit these golden foods",
        advices=advice_deposit,
    )

    group_beanstack = AdviceGroup(
        tier="",
        pre_string="Get 10,000 of these golden foods",
        advices=advice_beanstack,
    )

    group_super_beanstack = (
        AdviceGroup(
            tier="",
            pre_string="Get another 100,000 of these golden foods",
            advices=advice_super_beanstack,
        )
        if upgrade_bought
        else None
    )

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

    return AdviceSection(
        name="Giant Beanstalk",
        tier=tier,
        header=header,
        picture="Beanstalk.png",
        groups=groups,
    )
