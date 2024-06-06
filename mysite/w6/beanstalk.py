from models.models import AdviceSection, Advice, AdviceGroup
from utils.data_formatting import safe_loads
from utils.text_formatting import getItemDisplayName
from flask import g as session_data

TEN_K = 1
HUNNIT_K = 2

TIER_1_GOAL = 10**4
BASE_TIER_2_GOAL = 10**5
COMBINED_TIER_2_GOAL = TIER_1_GOAL + BASE_TIER_2_GOAL


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

    if not (beanstalk_bought or beanstalk_data):
        return AdviceSection(
            name="Giant Beanstalk",
            tier="",
            header="Come back once you've bought the \"Gold Food Beanstalk\" from the Jade Emporium",
            picture="Jade_Vendor.gif",
            collapse=False
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

    foods_to_tier_1 = [
        k for k, v in beanstalk_status.items() if v < TEN_K and gold_foods[k] < 10**4
    ]
    foods_to_deposit_tier_1 = [
        k for k, v in beanstalk_status.items() if v < TEN_K and k not in foods_to_tier_1
    ]

    tier_2_amount_needed_by_golden_food_code: dict[str, int] = dict()
    for golden_food_code in gold_foods:
        # if the golden food's tier 1 goal isn't deposited yet, then use the combined tier 2 goal
        tier_2_goal = COMBINED_TIER_2_GOAL \
            if golden_food_code in foods_to_deposit_tier_1 \
            else BASE_TIER_2_GOAL

        tier_2_amount_needed_by_golden_food_code[golden_food_code] = tier_2_goal

    foods_to_tier_2 = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and gold_foods[k] < tier_2_amount_needed_by_golden_food_code[k]
    ]
    foods_to_deposit_tier_2 = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and k not in foods_to_tier_2
    ]

    foods_to_deposit = foods_to_deposit_tier_1 + foods_to_deposit_tier_2 * upgrade_bought

    foods_finished = sum(beanstalk_status.values())
    tier = f"{foods_finished}/{len(gold_foods)*2}"

    advice_deposit = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
        )
        for codename in foods_to_deposit
    ]

    advice_tier_1 = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / TIER_1_GOAL:.02%}",
        )
        for codename in foods_to_tier_1
    ]

    advice_tier_2 = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / tier_2_amount_needed_by_golden_food_code[codename]:.02%}",
        )
        for codename in foods_to_tier_2
    ]

    group_upgrade = AdviceGroup(
        tier="",
        pre_string="Upgrade the Beanstalk to upgrade foods further",
        advices=[
            Advice(
                label="Buy \"Supersized Gold Beanstacking\" from the Jade Emporium",
                picture_class="supersized-gold-beanstacking"
            )
        ]
    )

    group_deposit = AdviceGroup(
        tier="",
        pre_string="Deposit these golden foods",
        advices=advice_deposit,
    )

    group_tier_1 = AdviceGroup(
        tier="",
        pre_string="Get 10,000 of these golden foods",
        advices=advice_tier_1,
    )

    group_tier_2 = AdviceGroup(
        tier="",
        pre_string="Get another 100,000 of these golden foods",
        advices=advice_tier_2,
    ) if upgrade_bought else None

    if foods_finished == len(gold_foods):
        header = "Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯"
    else:
        header = f"You have upgraded the Beanstalk {tier} times"

    groups = [
        group_deposit,
        group_tier_1,
        (group_tier_2 if upgrade_bought else group_upgrade),
    ]

    return AdviceSection(
        name="Giant Beanstalk",
        tier=tier,
        header=header,
        picture="Beanstalk.png",
        groups=groups
    )
