from consts import gfood_codes, break_you_best
from models.models import AdviceSection, Advice, AdviceGroup
from utils.text_formatting import getItemDisplayName
from flask import g as session_data

BEANSTACK_GOAL = 10**4
SUPER_BEANSTACK_GOAL = 10**5

def getProgressionTiersAdviceSections():
    beanstalk_AdviceDict = {}
    gold_foods = dict.fromkeys(gfood_codes, 0)
    info_tiers = 0
    max_tier = len(gold_foods) * 2


    upgrade_bought = session_data.account.sneaking['JadeEmporium']["Supersized Gold Beanstacking"]['Obtained']

    # Assets contains totals from Storage and inventories
    for gfood in gfood_codes:
        gold_foods[gfood] += session_data.account.all_assets.get(gfood).amount

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

    beanstalk_AdviceDict['Ready for Deposit'] = [
        Advice(
            label=foodname,
            picture_class=foodname.split(":")[0],
        )
        for foodname in foods_ready_to_deposit
    ]
    if len(foods_ready_to_deposit) > 0 and not session_data.account.hide_unrated:
        session_data.account.alerts_AdviceDict['World 6'].append(Advice(
            label=f"Golden Food ready for {{{{Beanstalk|#beanstalk}}}}",
            picture_class="beanstalk"
        ))

    beanstalk_AdviceDict['Beanstack'] = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(gold_foods[codename]) / BEANSTACK_GOAL:.02%}",
            goal='100%'
        )
        for codename in foods_to_beanstack
    ]

    beanstalk_AdviceDict['Super Beanstack'] = [
        Advice(
            label=getItemDisplayName(codename),
            picture_class=getItemDisplayName(codename),
            progression=f"{int(super_beanstack_progress[codename]) / SUPER_BEANSTACK_GOAL:.02%}",
            goal='100%'
        )
        for codename in foods_to_super_beanstack
    ]

    #Generate AdviceGroups
    beanstalk_AdviceGroupDict = {}
    if not upgrade_bought:
        beanstalk_AdviceGroupDict['Upgrade'] = AdviceGroup(
            tier="",
            pre_string="Upgrade the Beanstalk to enhance Golden Food beanstacks further",
            advices=[
                Advice(
                    label='Buy "Supersized Gold Beanstacking" from the {{ Jade Emporium|#sneaking }}',
                    picture_class="supersized-gold-beanstacking",
                )
            ],
            informational=False,
            completed=False
        )
    beanstalk_AdviceGroupDict['Ready for Deposit'] = AdviceGroup(
        tier="",
        pre_string="Golden Foods ready for deposit",
        advices=beanstalk_AdviceDict['Ready for Deposit'],
        informational=False,
    )

    beanstalk_AdviceGroupDict['Beanstack'] = AdviceGroup(
        tier="",
        pre_string="Collect 10,000 of these Golden Foods",
        advices=beanstalk_AdviceDict['Beanstack'],
        informational=True,
    )
    beanstalk_AdviceGroupDict['Beanstack'].sort_advices(True)

    if upgrade_bought:
        beanstalk_AdviceGroupDict['Super Beanstack'] = AdviceGroup(
                tier="",
                pre_string="Collect another 100,000 of these Golden Foods",
                advices=beanstalk_AdviceDict['Super Beanstack'],
                informational=True,
        )
        beanstalk_AdviceGroupDict['Super Beanstack'].sort_advices(True)

    overall_SectionTier = min(max_tier + info_tiers, foods_finished)
    return beanstalk_AdviceGroupDict, overall_SectionTier, max_tier

def getBeanstalkAdviceSection() -> AdviceSection:
    if not session_data.account.sneaking['JadeEmporium']["Gold Food Beanstalk"]['Obtained']:
        return AdviceSection(
            name="Beanstalk",
            tier="",
            header="Come back after unlocking \"Gold Food Beanstalk\" from the Jade Emporium",
            picture="Jade_Vendor.gif",
            unreached=True,
            unrated=True
        )
    #Generate AdviceGroups
    beanstalk_AdviceGroupDict, overall_SectionTier, max_tier = getProgressionTiersAdviceSections()

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    beanstalk_AdviceSection = AdviceSection(
        name="Beanstalk",
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        header=(
            f"You have upgraded the Beanstalk {tier_section} times" if overall_SectionTier < max_tier
            else f"Well done, Jack! The Golden Goose took an enviably massive dump in your lap. Go pay the giants off! 🍯{break_you_best}"
        ),
        picture="Beanstalk.png",
        groups=beanstalk_AdviceGroupDict.values(),
        unrated=True,
    )

    return beanstalk_AdviceSection
