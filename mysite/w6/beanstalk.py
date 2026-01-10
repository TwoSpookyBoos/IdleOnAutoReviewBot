from consts.consts_autoreview import break_you_best, build_subgroup_label
from consts.progression_tiers import true_max_tiers, beanstalk_progressionTiers
from models.general.session_data import session_data

from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup

from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.text_formatting import getItemCodeName

from utils.logging import get_logger

logger = get_logger(__name__)


def getProgressionTiersAdviceSections():
    optional_tiers = 2
    true_max = true_max_tiers['Beanstalk']
    max_tier = true_max - optional_tiers
    tier_stacks = 0

    beanstalk = session_data.account.beanstalk
    deposit_tier_advice = {}
    alert = set()

    for tier_number, requirements in beanstalk_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        # 10k
        process_progression_deposit_tier(
            requirements.get('10k', []), 0, deposit_tier_advice, subgroup_label, alert
        )

        # SuperBeanstack purchased
        if requirements.get('Tier Unlocked', 0) == 2 and beanstalk.unlocked_tier < 2:
            add_subgroup_if_available_slot(deposit_tier_advice, subgroup_label)
            if subgroup_label in deposit_tier_advice:
                deposit_tier_advice[subgroup_label].append(Advice(
                    label="Purchase \"Supersized Gold Beanstacking\" from the Jade Emporium",
                    picture_class=session_data.account.sneaking['JadeEmporium']['Supersized Gold Beanstacking']['Image'],
                    progression=0,
                    goal=1
                ))

        # 100k
        process_progression_deposit_tier(
            requirements.get('100k', []), 1, deposit_tier_advice, subgroup_label, alert
        )

        # Upgrade from Urie Quest
        if requirements.get('Tier Unlocked', 0) == 3 and beanstalk.unlocked_tier < 3:
            add_subgroup_if_available_slot(deposit_tier_advice, subgroup_label)
            if subgroup_label in deposit_tier_advice:
                deposit_tier_advice[subgroup_label].append(Advice(
                    label='Complete Urie quest in World 7 and upgrade Beanstalk',
                    picture_class='urie',
                    progression=0,
                    goal=1
                ))

        # 1M
        process_progression_deposit_tier(
            requirements.get('1M', []), 2, deposit_tier_advice, subgroup_label, alert
        )

        # Final tier check
        if subgroup_label not in deposit_tier_advice and tier_stacks == tier_number - 1:
            tier_stacks = tier_number

    session_data.account.add_alert_list('World 6', alert)

    overall_section_tier = min(true_max, tier_stacks)
    beanstalk_advice_group = {}
    tier_advice_group = AdviceGroup(
        tier=overall_section_tier,
        pre_string='Deposit Golden Foods to the Beanstalk',
        advices=deposit_tier_advice,
    )
    tier_advice_group.remove_empty_subgroups()
    beanstalk_advice_group['Tiers'] = tier_advice_group
    return beanstalk_advice_group, overall_section_tier, max_tier, true_max


def process_progression_deposit_tier(
    requirement, current_tier, advice_group, subgroup_label, alert
):
    # Assets contains totals from Storage and inventories
    account_items = session_data.account.all_assets
    beanstalk = session_data.account.beanstalk
    for golden_food_name in requirement:
        deposited = beanstalk[golden_food_name]
        if deposited.tier == current_tier:
            add_subgroup_if_available_slot(advice_group, subgroup_label)
            if subgroup_label in advice_group:
                golden_food_code = getItemCodeName(golden_food_name)
                # TODO: change account_items to use name instead code
                account_amount = account_items.get(golden_food_code).amount
                advice_group[subgroup_label].append(
                    deposited.next_tier_progress_advice(account_amount))
                alert.add(deposited.alert_advice(account_amount))


def getGoldFoodBonusAdviceSections() -> AdviceGroup:
    food_list_advice = [
        deposited.get_bonus_advice(False)
        for deposited in session_data.account.beanstalk.values()
    ]
    for advice in food_list_advice:
        advice.mark_advice_completed()
    return AdviceGroup(
        tier='',
        pre_string='Golden Food Bonus',
        advices=food_list_advice,
        informational=True
    )


def getBeanstalkAdviceSection() -> AdviceSection:
    if session_data.account.beanstalk.unlocked_tier < 1:
        return AdviceSection(
            name='Beanstalk',
            tier='',
            header="Come back after unlocking \"Gold Food Beanstalk\" from the Jade Emporium",
            picture='Jade_Vendor.gif',
            unreached=True,
        )
    # Generate AdviceGroups
    beanstalk_AdviceGroups, overall_SectionTier, max_tier, true_max = getProgressionTiersAdviceSections()
    beanstalk_AdviceGroups['Gold Food'] = getGoldFoodBonusAdviceSections()

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
