from flask import g as session_data

from consts.consts_autoreview import EmojiType
from consts.consts_master_classes import tesseract_tachyon_list
from consts.progression_tiers import true_max_tiers
from models.models import AdviceSection, AdviceGroup, Advice
from utils.data_formatting import mark_advice_completed
from utils.logging import get_logger
from utils.text_formatting import notateNumber

logger = get_logger(__name__)

def get_progression_tiers_advice_group() -> tuple[AdviceGroup, int, int, int]:
    tesseract_advice_dict = {
        'Tiers': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['Tesseract']
    max_tier = true_max - optional_tiers
    tier_tesseract = 0

    tiers_ag = AdviceGroup(
        tier=tier_tesseract,
        pre_string='Progression Tiers',
        advices=tesseract_advice_dict['Tiers']
    )
    overall_section_tier = min(true_max, tier_tesseract)
    return tiers_ag, overall_section_tier, max_tier, true_max


def get_tesseract_currencies_advice_group(tesseract) -> AdviceGroup:
    currency_advices = {
        'Currencies': [],
    }
    currency_advices['Currencies'].append(Advice(
        label=f"Total Tachyons Collected: {notateNumber('Basic', tesseract['Total Tachyons Collected'], 3)}",
        picture_class='tachion-truth'
    ))
    currency_advices['Currencies'] += [
        Advice(
            label=f"{tachyon_name}: {notateNumber('Basic', tesseract[f'Tachyon{tachyon_index}'], 3)}",
            picture_class=f'tesseract-tachyon-{tachyon_index-1}'
        ) for tachyon_index, tachyon_name in enumerate(tesseract_tachyon_list, start=1)
    ]

    #Tachyon Multi calculation groups
    currency_advices['Currencies'].append(Advice(
        label=f"Total Tachyon multi: {tesseract['Tachyon Calc']['Total']:.3f}x",
        picture_class='tesseract'
    ))

    arcane_cultist_index = None
    tesseract_preset_level = 100
    tesseract_talent_index = '586'

    for arcane_cultist in session_data.account.acs:
        if arcane_cultist_index is None:
            arcane_cultist_index = arcane_cultist.character_index
        if arcane_cultist.current_preset_talents.get(tesseract_talent_index, 0) > tesseract_preset_level:
            arcane_cultist_index = arcane_cultist.character_index
            tesseract_preset_level = arcane_cultist.current_preset_talents.get(tesseract_talent_index, 0)
        if arcane_cultist.secondary_preset_talents.get(tesseract_talent_index, 0) > tesseract_preset_level:
            tesseract_preset_level = arcane_cultist.secondary_preset_talents.get(tesseract_talent_index, 0)

    mgb_label = f"Tachyon Multi Group B: {tesseract['Tachyon Calc']['mgb']:.2f}x"

    emperor_tachyon_bonus = session_data.account.emperor['Bonuses'][6]
    currency_advices[mgb_label] = [
        Advice(
            label=f"{{{{Emperor Showdowns|#emperor}}}}: {emperor_tachyon_bonus['Description']}"
                  f"<br>{emperor_tachyon_bonus['Scaling']}",
            picture_class='the-emperor',
            progression=emperor_tachyon_bonus['Wins'],
            goal=EmojiType.INFINITY.value
        )
    ]

    mgd_label = f"Tachyon Multi Group D: {tesseract['Tachyon Calc']['mgd']:.2f}x"

    missing_bundle_data_txt = '<br>Note: Could be inaccurate. Bundle data not found!' if not session_data.account.gemshop['Bundle Data Present'] else ''
    missing_bundle_data = not session_data.account.gemshop['Bundle Data Present']
    has_arcanist_pack = session_data.account.gemshop['Bundles']['bun_x']['Owned']
    ac_pack_value = 1.2 if has_arcanist_pack else 1
    currency_advices[mgd_label] = [Advice(
        label=f"Gemshop - Arcane Cultist Pack:"
              f"<br>{ac_pack_value}/1.2x Extra Tachyons"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_arcanist_pack) if not missing_bundle_data else 'IDK',
        goal=1
    )]

    for subgroup in currency_advices:
        for advice in currency_advices[subgroup]:
            mark_advice_completed(advice)

    currency_ag = AdviceGroup(
        tier='',
        pre_string='Tesseract Currencies',
        advices=currency_advices,
        informational=True
    )
    # currency_ag.remove_empty_subgroups()
    return currency_ag

def get_tesseract_upgrades_advice_group(tesseract) -> AdviceGroup:
    upgrades_advice_dict = {
        'Upgrades': [Advice(
            label=f"Total Tesseract Upgrades: {tesseract['Total Upgrades']:,}",
            picture_class='tesseract'
        )]
    }

    #Upgrades
    upgrades_advice_dict['Upgrades'] += [
        Advice(
            label=(
                f"{upgrade_name}: {upgrade_details['Description']}"
                f"<br>Requires {upgrade_details['Unlock Requirement'] - tesseract['Total Upgrades']} more Upgrades to unlock"
                if not upgrade_details['Unlocked'] else
                f"{upgrade_name}: {upgrade_details['Description']}"
            ),
            picture_class=upgrade_details['Image'],
            progression=upgrade_details['Level'],
            goal=upgrade_details['Max Level'],
            resource=upgrade_details['Tachyon Image']
        ) for upgrade_name, upgrade_details in tesseract['Upgrades'].items()
    ]

    for subgroup in upgrades_advice_dict:
        for advice in upgrades_advice_dict[subgroup]:
            mark_advice_completed(advice)

    upgrades_ag = AdviceGroup(
        tier='',
        pre_string='Tesseract Upgrades',
        advices=upgrades_advice_dict,
        informational=True
    )
    upgrades_ag.remove_empty_subgroups()
    return upgrades_ag


def get_tesseract_advice_section() -> AdviceSection:
    #Check if player has reached this section
    if 'Arcane Cultist' not in session_data.account.classes:
        tesseract_advice_section = AdviceSection(
            name="The Tesseract",
            tier="Not Yet Evaluated",
            header="Come back after unlocking an Arcane Cultist in World 6!",
            picture='customized/Tesseract.gif',
            unrated=True,
            unreached=session_data.account.highest_world_reached < 6,
            completed=False
        )
        return tesseract_advice_section

    tesseract = session_data.account.tesseract

    #Generate AdviceGroups
    tesseract_advice_group_dict = {}
    tesseract_advice_group_dict['Tiers'], overall_section_tier, max_tier, true_max = get_progression_tiers_advice_group()
    tesseract_advice_group_dict['Currencies'] = get_tesseract_currencies_advice_group(tesseract)
    tesseract_advice_group_dict['Upgrades'] = get_tesseract_upgrades_advice_group(tesseract)

    #Generate AdviceSection
    tier_section = f"{overall_section_tier}/{max_tier}"
    tesseract_advice_section = AdviceSection(
        name='The Tesseract',
        tier=tier_section,
        pinchy_rating=overall_section_tier,
        header='Arcane Cultist and Tesseract Information',  #tier met: {tier_section}{break_you_best if overall_section_tier >= max_tier else ''}",
        picture='customized/Tesseract.gif',
        groups=tesseract_advice_group_dict.values(),
        completed=None,
        unrated=True,
    )

    return tesseract_advice_section
