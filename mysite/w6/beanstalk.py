import json

from consts import jade_emporium
from models.models import Account, AdviceSection, Advice, AdviceGroup
from utils.data_formatting import safe_loads
from utils.text_formatting import getItemDisplayName, numberToLetter
from flask import g as session_data

TEN_K = 1
HUNNIT_K = 2


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

    foods_to_10k = [
        k for k, v in beanstalk_status.items() if v < TEN_K and gold_foods[k] < 10**4
    ]
    foods_to_deposit_10k = [
        k for k, v in beanstalk_status.items() if v < TEN_K and k not in foods_to_10k
    ]

    foods_to_100k = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and gold_foods[k] < 10**5
    ]
    foods_to_deposit_100k = [
        k for k, v in beanstalk_status.items() if v < HUNNIT_K and k not in foods_to_100k
    ]

    foods_to_deposit = foods_to_deposit_10k + foods_to_deposit_100k * upgrade_bought

    foods_finished = sum(beanstalk_status.values())
    tier = f"{foods_finished}/{len(gold_foods)*2}"

    advice_deposit = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
        )
        for codename in foods_to_deposit
    ]

    advice_10k = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / 10**4:.02%}",
        )
        for codename in foods_to_10k
    ]

    advice_100k = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / 10**5:.02%}",
        )
        for codename in foods_to_100k
    ]

    group_upgrade = AdviceGroup(
        tier="",
        pre_string="Upgrade the Beanstalk to upgrade foods further",
        advices=[
            Advice(
                label="Buy \"Supersized Gold Beanstacking\" from the Jade Emporium",
                picture_class="jade-vendor"
            )
        ]
    )

    group_deposit = AdviceGroup(
        tier="",
        pre_string="Deposit these golden foods",
        advices=advice_deposit,
    )

    group_10k = AdviceGroup(
        tier="",
        pre_string="Get 10,000 of these golden foods",
        advices=advice_10k,
    )

    group_100k = AdviceGroup(
        tier="",
        pre_string="Get 100,000 of these golden foods",
        advices=advice_100k,
    ) if upgrade_bought else None

    if foods_finished == len(gold_foods):
        header = "Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯"
    else:
        header = f"You have upgraded the Beanstalk {tier} times"

    groups = [
        group_deposit,
        group_10k,
        (group_upgrade if not upgrade_bought else group_100k),
    ]

    return AdviceSection(
        name="Giant Beanstalk",
        tier=tier,
        header=header,
        picture="Beanstalk.png",
        groups=groups
    )
