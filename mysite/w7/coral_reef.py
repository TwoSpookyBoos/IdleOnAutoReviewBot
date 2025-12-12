from consts.consts_autoreview import ValueToMulti, EmojiType
from consts.consts_w1 import stamp_maxes
from consts.consts_w2 import max_vial_level
from models.models import AdviceSection, AdviceGroup, Advice, Card
from flask import g as session_data

from models.models_util import get_coral_reef_advice, get_companion_advice, get_gem_shop_purchase_advice


def get_corals_info_group() -> AdviceGroup:
    coral_advice: list[Advice] = [
        Advice(
            label=f"Town Corals: {int(session_data.account.coral_reef['Town Corals'])}",
            picture_class="coral"
        ), *[get_coral_reef_advice(name) for name in session_data.account.coral_reef['Reef Corals'].keys()]
    ]
    return AdviceGroup(
        pre_string='Corals',
        advices=coral_advice,
        tier='',
        informational=True
    )

def get_sources_of_coral_info_group() -> AdviceGroup:
    # `"ReefDayGains" == e` in source. Last updated in v2.46 Dec 7

    # Base
    base_daily_corals = 10

    # Mult A
    shellslug_multi, shellslug_advice = get_companion_advice('Shellslug')

    # Mult B
    coolral = session_data.account.event_points_shop['Bonuses']['Coolral']
    coolral_multi = 1 + 0.3 * coolral['Owned']
    coolral_advice = Advice(
        label=f'{{{{ Event Shop|#event-shop }}}} - Coolral: x{coolral_multi}/x1.3 Daily Corals',
        resource='event-point',
        picture_class='event-shop-25',
        progression = int(coolral['Owned']),
        goal = 1,
    )

    # Mult C
    more_coral = 'More Coral'
    more_coral_data = session_data.account.gemshop['Purchases'][more_coral]
    more_coral_multi = 1 + 0.2 * more_coral_data['Owned']
    more_coral_advice = get_gem_shop_purchase_advice(purchase_name=more_coral, secondary_label=f": x{more_coral_multi}/x3.0 Daily Corals")


    # Mult D
    multi_group_d_value = 0
    multi_group_d_advice: list[Advice] = []

    # TODO: Coral Kid upgrade
    coral_kid_advice = Advice(
        label="Coral Kid Upgrade (WIP)",
        picture_class="coming-soon"
    )
    multi_group_d_advice.append(coral_kid_advice)

    # TODO: Dancing Coral bonus
    dancing_coral_advice = Advice(
        label="Dancing Coral Bonus (WIP)",
        picture_class="coming-soon"
    )
    multi_group_d_advice.append(dancing_coral_advice )

    # TODO: Clamwork bonus
    clamwork_advice = Advice(
        label="Clamwork Bonus (WIP)",
        picture_class="coming-soon"
    )
    multi_group_d_advice.append(clamwork_advice )

    # TODO: Killroy bonus
    killroy_advice = Advice(
        label="Killroy Bonus (WIP)",
        picture_class="coming-soon"
    )
    multi_group_d_advice.append(killroy_advice )

    corale_stamp = session_data.account.stamps['Corale Stamp']
    corale_stamp_value = corale_stamp['Total Value']
    corale_stamp_advice = Advice(
        label=f"{{{{ Stamps|#stamps }}}} - Corale: +{round(corale_stamp_value, 1):g}% Daily Corals",
        picture_class='corale-stamp',
        progression=corale_stamp['Level'],
        resource=corale_stamp['Material'],
        goal=stamp_maxes['Corale Stamp'] if corale_stamp['Delivered'] else 1
    )
    multi_group_d_advice.append(corale_stamp_advice)
    multi_group_d_value += corale_stamp_value

    scale_on_ice = session_data.account.alchemy_vials['Scale On Ice (Scaled Fragment)']
    scale_on_ice_value = scale_on_ice['Value']
    scale_on_ice_advice = Advice(
        label=f"{{{{ Vial|#vials }}}}: Scale On Ice: +{scale_on_ice['Value']:.2f}% Daily Corals",
        picture_class='scaled-fragment',
        progression=scale_on_ice['Level'],
        resource='scaled-fragment',
        goal=max_vial_level
    )
    multi_group_d_advice.append(scale_on_ice_advice)
    multi_group_d_value += scale_on_ice_value

    # TODO: Legend Talent
    legend_talent_advice = Advice(
        label="Legend Talent (WIP)",
        picture_class="coming-soon"
    )
    multi_group_d_advice.append(legend_talent_advice )

    coral_arcade = session_data.account.arcade[57]
    coral_arcade_value = coral_arcade['Value']
    coral_arcade_advice = Advice(
        label=f"{{{{ Arcade|#arcade }}}} - Daily Corals: +{coral_arcade_value:.2f}/{coral_arcade['MaxValue']:g}%",
        picture_class=coral_arcade['Image'],
        progression=coral_arcade['Level'],
        resource='arcade-gold-ball',
        goal=101,
    )
    multi_group_d_advice.append(coral_arcade_advice)
    multi_group_d_value += coral_arcade_value

    coral_conservationism = session_data.account.sneaking['JadeEmporium']['Coral Conservationism']
    coral_conservationism_value = 20 * int(coral_conservationism['Obtained'])
    coral_conservationism_advice = Advice(
        label=f'{{{{ Jade Emporium|#jade-emporium }}}} Upgrade \"Coral Conservationism\": +{coral_conservationism_value}/20% Daily Corals',
        picture_class=coral_conservationism['Image'],
        progression=int(coral_conservationism['Obtained']),
        resource='jade-coin',
        goal=1
    )
    multi_group_d_advice.append(coral_conservationism_advice)
    multi_group_d_value += coral_conservationism_value

    demonblub_card: Card = next(card for card in session_data.account.cards if card.name == 'Demonblub')
    demonblub_card_value = demonblub_card.getCurrentValue()
    demonblub_advice = demonblub_card.getAdvice()
    multi_group_d_advice.append(demonblub_advice)
    multi_group_d_value += demonblub_card_value

    coral_statue = session_data.account.statues['Coral Statue']
    coral_statue_value = coral_statue['Value']
    coral_statue_advice = Advice(
        label=f"Level {coral_statue['Level']} Coral Statue: +{coral_statue_value:.2f}% {'(must be at least gold)' if coral_statue['Type'] == 'Normal' else ''}",
        picture_class=coral_statue['Image'],
        progression=coral_statue['Level'],
        goal=EmojiType.INFINITY.value,
    )
    multi_group_d_advice.append(coral_statue_advice)
    multi_group_d_value += coral_statue_value

    multi_group_d_mult = round(ValueToMulti(multi_group_d_value), 2)

    # Total
    total_daily_corals = base_daily_corals * shellslug_multi * coolral_multi * more_coral_multi

    coral_sources: dict[str, list[Advice]] = {
        f'Total daily corals: {total_daily_corals}': [],
        f'Base: {base_daily_corals}': [Advice(
           label=f'Base daily corals: {base_daily_corals}',
            picture_class='coral',
            completed=True,
        )],
        f'Multi Group A: x{shellslug_multi}': [shellslug_advice],
        f'Multi Group B: x{coolral_multi}': [coolral_advice],
        f'Multi Group C: x{more_coral_multi}': [more_coral_advice],
        f'Multi Group D: x{multi_group_d_mult}': multi_group_d_advice,
    }

    for subgroup in coral_sources.values():
        for advice in subgroup:
            advice.mark_advice_completed()

    return AdviceGroup(
        pre_string='Sources of daily Corals',
        advices=coral_sources,
        tier='',
        informational=True
    )

def get_coral_reef_section():
    # Check if player has reached this section
    if session_data.account.highest_world_reached < 7:
        reef_AdviceSection = AdviceSection(
            name='Coral Reef',
            tier='Not Yet Evaluated',
            header='Come back after unlocking W7!',
            picture='',
            unreached=True,
        )
        return reef_AdviceSection

    groups = [get_corals_info_group(), get_sources_of_coral_info_group()]
    return AdviceSection(
        name='Coral Reef',
        tier='',
        header='Coral Reef',
        picture='extracted_sprites/HumbleHugh0.png',
        groups=groups,
        informational=True,
        unrated=True,
    )
