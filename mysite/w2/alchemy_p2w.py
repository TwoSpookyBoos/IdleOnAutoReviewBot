from flask import g as session_data

from consts.consts_autoreview import break_you_best
from consts.progression_tiers import true_max_tiers
from models.models import Advice, AdviceGroup, AdviceSection


def getP2WProgressionTiersAdviceGroup(highest_alchemy_level):
    p2w_Advices = {
        'Pay2Win': []
    }
    p2w_AdviceGroupDict = {}
    optional_tiers = 0
    true_max = true_max_tiers['Pay2Win']
    max_tier = true_max - optional_tiers

    sum_liquid_cauldrons = 0
    liquid_cauldrons_unlocked = 1

    if highest_alchemy_level >= 80:
        liquid_cauldrons_unlocked = 4  # includes Toxic HG
    elif highest_alchemy_level >= 35:
        liquid_cauldrons_unlocked = 3  # includes Trench Seawater
    elif highest_alchemy_level >= 20:
        liquid_cauldrons_unlocked = 2  # includes Liquid Nitrogen

    bubble_cauldron_max = 4 * 375  # 4 cauldrons, 375 upgrades each
    liquid_cauldron_max = 180 * liquid_cauldrons_unlocked
    vials_max = 15 + 45  # 15 attempts, 45 RNG
    bubble_cauldron_sum = sum(session_data.account.alchemy_p2w['Cauldrons'])
    vials_sum = sum(session_data.account.alchemy_p2w['Vials'])
    player_sum = sum(session_data.account.alchemy_p2w['Player'])
    if isinstance(session_data.account.alchemy_p2w['Liquids'], list):
        # Liquids are different. Any locked liquid cauldrons are stored as -1 which would throw off a simple sum
        for liquid_entry in session_data.account.alchemy_p2w.get("Liquids"):
            if liquid_entry != -1:
                sum_liquid_cauldrons += liquid_entry

    p2w_sum = bubble_cauldron_sum + sum_liquid_cauldrons + vials_sum + player_sum
    p2w_max = bubble_cauldron_max + liquid_cauldron_max + vials_max + (highest_alchemy_level * 2)
    p2w_sum_without_player = bubble_cauldron_sum + sum_liquid_cauldrons + vials_sum
    p2w_max_without_player = bubble_cauldron_max + liquid_cauldron_max + vials_max

    tier_P2WUpgrades = int(p2w_sum_without_player >= p2w_max_without_player)

    if p2w_sum < p2w_max:
        if bubble_cauldron_sum < bubble_cauldron_max:
            p2w_Advices['Pay2Win'].append(Advice(
                label='Bubble Cauldron Upgrades',
                picture_class='cauldron-a',
                progression=bubble_cauldron_sum,
                goal=bubble_cauldron_max
            ))
        if sum_liquid_cauldrons < liquid_cauldron_max:
            p2w_Advices['Pay2Win'].append(Advice(
                label='Liquid Cauldron Upgrades',
                picture_class='bleach-liquid-cauldrons',
                progression=sum_liquid_cauldrons,
                goal=liquid_cauldron_max
            ))
        if vials_sum < vials_max:
            p2w_Advices['Pay2Win'].append(Advice(
                label='Vial Upgrades',
                picture_class='vials',
                progression=vials_sum,
                goal=vials_max
            ))
        if player_sum < highest_alchemy_level * 2:
            p2w_Advices['Pay2Win'].append(Advice(
                label='Player Upgrades',
                picture_class='p2w-player',
                progression=player_sum,
                goal=highest_alchemy_level * 2
            ))
            session_data.account.alerts_Advices['World 2'].append(Advice(
                label=f"{{{{ P2W|#pay2win }}}} Player upgrades can be leveled",
                picture_class='p2w-player',
            ))
    p2w_AdviceGroupDict['Pay2Win'] = AdviceGroup(
        tier=tier_P2WUpgrades,
        pre_string='Remaining Pay2Win upgrades to purchase',
        post_string='',
        advices=p2w_Advices['Pay2Win']
    )
    overall_SectionTier = min(true_max, tier_P2WUpgrades)
    return p2w_AdviceGroupDict, overall_SectionTier, max_tier, true_max, p2w_sum, p2w_max


def getAlchemyP2WAdviceSection() -> AdviceSection:
    highestAlchemyLevel = max(session_data.account.all_skills['Alchemy'])
    if highestAlchemyLevel < 1:
        p2w_AdviceSection = AdviceSection(
            name='Pay2Win',
            tier='Not Yet Evaluated',
            header='Come back after unlocking the Alchemy skill in World 2!',
            picture='pay2win.png',
            unreached=True
        )
        return p2w_AdviceSection

    #Generate AdviceGroups
    p2w_AdviceGroupDict, overall_SectionTier, max_tier, true_max, p2wSum, p2wMax = getP2WProgressionTiersAdviceGroup(highestAlchemyLevel)

    #Generate AdviceSection
    tier_section = f"{overall_SectionTier}/{max_tier}"
    header_upgrades = f"{p2wSum}/{p2wMax}"
    p2w_AdviceSection = AdviceSection(
        name='Pay2Win',
        tier=tier_section,
        pinchy_rating=overall_SectionTier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=(
            f"You've purchased all {p2wMax} upgrades in Alchemy's Pay 2 Win tab!{break_you_best}"
            if p2wSum >= p2wMax else
            f"You've purchased {header_upgrades} upgrades in Alchemy's Pay 2 Win tab."
            f"<br>Try to purchase the basic upgrades before Mid W5, and Player upgrades after each Alchemy level up!"
        ),
        picture='pay2win.png',
        groups=p2w_AdviceGroupDict.values()
    )
    return p2w_AdviceSection
