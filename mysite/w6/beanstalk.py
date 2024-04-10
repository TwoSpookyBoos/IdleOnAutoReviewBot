import json

from consts import jade_emporium
from models.models import Account, AdviceSection, Advice, AdviceGroup
from utils.data_formatting import safe_loads

from utils.text_formatting import getItemDisplayName, numberToLetter


TEN_K = 1
HUNNIT_K = 2


def __get_ninja_section(raw):
    default = "[]"
    return safe_loads(raw.get("Ninja", default))


def __get_beanstalk_data(raw):
    if ninja_section := __get_ninja_section(raw):
        return ninja_section[-4]
    return None


def __beanstalk_bought(raw):
    if not (ninja_section := __get_ninja_section(raw)):
        return False, False

    jade_emporium_bought = ninja_section[-6][9]

    name_base = "Gold Food Beanstalk"
    name_upgrade = "Supersized Gold Beanstacking"

    upgrades_bought: list[bool] = list()

    for name in [name_base, name_upgrade]:
        index = next(i for i, upgrade in enumerate(jade_emporium) if upgrade["name"] == name)
        letter = numberToLetter(index)
        upgrades_bought.append(letter in jade_emporium_bought)

    return upgrades_bought


def section_beanstalk():
    account = Account()
    raw = account.raw_data
    beanstalk_bought, upgrade_bought = __beanstalk_bought(raw)

    beanstalk_data = __get_beanstalk_data(raw)

    if not (beanstalk_bought or beanstalk_data):
        return AdviceSection(name="beanstalk", tier="", header="")

    gfood_codes = ["PeanutG", "ButterBar", *[f"FoodG{i}" for i in range(1, 14)]]
    gold_foods = dict.fromkeys(gfood_codes, 0)
    beanstalk_status = dict(zip(gfood_codes, beanstalk_data))

    for gfood in gfood_codes:
        gold_foods[gfood] += account.assets.get(gfood).amount

    for toon in account.safe_characters:
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
                label="Buy Supersized Gold Beanstacking from the Jade Emporium",
                picture_class=""
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
