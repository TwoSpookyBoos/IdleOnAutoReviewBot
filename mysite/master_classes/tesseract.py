
from consts.consts_autoreview import EmojiType
from consts.consts_idleon import lavaFunc
from consts.consts_master_classes import tesseract_tachyon_list
from consts.progression_tiers import true_max_tiers

from models.models import AdviceSection, AdviceGroup, Advice, session_data
from models.advice.w2 import get_arcade_advice

from utils.all_talentsDict import all_talentsDict
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
    if tesseract["Arcane Rocks Enabled"]:
        currency_advices["Currencies"].append(
            Advice(
                label="Arcane Rocks Enabled! Collect 1 per full AFK hour while fighting on an Arcane Cultist. Maximize your /hr display "
                "within AFK Info screen before consuming!",
                picture_class="arcane-rock",
                progression=1,
                goal=1,
            )
        )
    else:
        currency_advices["Currencies"].append(
            Advice(
                label="Fight with Arcane Form enabled to collect 1,000 Arcane Fragments, then use the stack. "
                "This enables AFK Fighting on Arcane Cultists to produce 1 Arcane Rock per hour!",
                picture_class="arcane-fragment",
                progression=min(
                    1000, session_data.account.all_assets.get("Quest107").amount
                ),
                goal=1000,
            )
        )
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
    tesseract_talent_index = 586

    for arcane_cultist in session_data.account.acs:
        if arcane_cultist_index is None:
            arcane_cultist_index = arcane_cultist.character_index
        if arcane_cultist.current_preset_talents.get(str(tesseract_talent_index), 0) > tesseract_preset_level:
            arcane_cultist_index = arcane_cultist.character_index
            tesseract_preset_level = arcane_cultist.current_preset_talents.get(str(tesseract_talent_index), 0)
        if arcane_cultist.secondary_preset_talents.get(str(tesseract_talent_index), 0) > tesseract_preset_level:
            tesseract_preset_level = arcane_cultist.secondary_preset_talents.get(str(tesseract_talent_index), 0)


    mga_label = f"Tachyon Multi Group A: {tesseract['Tachyon Calc']['mga']:.2f}x"
    currency_advices[mga_label] = []

    ripple_in_spacetime = tesseract['Upgrades']['Ripple in Spacetime']
    currency_advices[mga_label].append(
        Advice(
            label=f"Tesseract Upgrade 'Ripple in Spacetime':"
                  f"<br>+{ripple_in_spacetime['Total Value']}% Tachyons",
            picture_class=ripple_in_spacetime['Image'],
            progression=ripple_in_spacetime['Level'],
            goal=ripple_in_spacetime['Max Level'],
            resource=ripple_in_spacetime['Tachyon Image']
        )
    )

    tesseract_talent_bonus_value = lavaFunc(
        funcType=all_talentsDict[tesseract_talent_index]['funcX'],
        level=tesseract_preset_level,
        x1=all_talentsDict[tesseract_talent_index]['x1'],
        x2=all_talentsDict[tesseract_talent_index]['x2'],
    )

    currency_advices[mga_label].append(
        Advice(
            label=f"Tesseract Talent: +{tesseract_talent_bonus_value:.2f}% Tachyons",
            picture_class='tesseract'
        )
    )

    verdon_hoarding = tesseract['Upgrades']['Verdon Hoarding']
    currency_advices[mga_label].append(
        Advice(
            label=f"Tesseract Upgrade 'Verdon Hoarding':"
                  f"<br>+{verdon_hoarding['Total Value']}% Tachyons",
            picture_class=verdon_hoarding['Image'],
            progression=verdon_hoarding['Level'],
            goal=verdon_hoarding['Max Level'],
            resource=verdon_hoarding['Tachyon Image']
        )
    )

    aurion_hoarding = tesseract['Upgrades']['Aurion Hoarding']
    currency_advices[mga_label].append(
        Advice(
            label=f"Tesseract Upgrade 'Aurion Hoarding':"
                  f"<br>+{aurion_hoarding['Total Value']}% Tachyons",
            picture_class=aurion_hoarding['Image'],
            progression=aurion_hoarding['Level'],
            goal=aurion_hoarding['Max Level'],
            resource=aurion_hoarding['Tachyon Image']
        )
    )

    # TODO: Tachyons from Equipment

    lab_jewel = session_data.account.labJewels['Eternal Energy Jewel']
    lab_jewel_active = lab_jewel['Enabled']
    currency_advices[mga_label].append(Advice(
        label=f"Lab Jewel 'Eternal Energy Jewel': +{lab_jewel['Value'] * lab_jewel_active}/{lab_jewel['Value']}% Tachyons",
        picture_class='deadly-wrath-jewel',
        progression=int(lab_jewel_active),
        goal=1
    ))

    currency_advices[mga_label].append(get_arcade_advice(50))

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

    mgc_label = f"Bone Multi Group C: {tesseract['Tachyon Calc']['mgc']:.2f}x"
    mystery_fizz = session_data.account.sneaking['PristineCharms']['Mystery Fizz']
    currency_advices[mgc_label] = [
        Advice(
            label=f"{{{{Sneaking|#sneaking}}}}: Pristine Charm: Mystery Fizz"
                  f"<br>{mystery_fizz['Bonus']}",
            picture_class=mystery_fizz['Image'],
            progression=int(mystery_fizz['Obtained']),
            goal=1
        )
    ]

    mgd_label = f"Tachyon Multi Group D: {tesseract['Tachyon Calc']['mgd']:.2f}x"
    currency_advices[mgd_label] = [
        Advice(
            label=f"Backup Energy Talent: {tesseract['Tachyon Calc']['mgd']:.2f}x Tachyons",
            picture_class='backup-energy',
        )
    ]

    mge_label = f"Tachyon Multi Group E: {tesseract['Tachyon Calc']['mge']:.2f}x"

    missing_bundle_data_txt = '<br>Note: Could be inaccurate. Bundle data not found!' if not session_data.account.gemshop['Bundle Data Present'] else ''
    missing_bundle_data = not session_data.account.gemshop['Bundle Data Present']
    has_arcanist_pack = session_data.account.gemshop['Bundles']['bun_x']['Owned']
    ac_pack_value = tesseract['Tachyon Calc']['mge']
    currency_advices[mge_label] = [Advice(
        label=f"Gemshop - Arcane Cultist Pack:"
              f"<br>{ac_pack_value}/1.2x Tachyons"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_arcanist_pack) if not missing_bundle_data else 'IDK',
        goal=1
    )]

    for subgroup in currency_advices:
        for advice in currency_advices[subgroup]:
            advice.mark_advice_completed()

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
            advice.mark_advice_completed()

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
