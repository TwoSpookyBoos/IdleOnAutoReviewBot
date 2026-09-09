from consts.consts_autoreview import EmojiType, break_you_best, build_subgroup_label
from consts.idleon.master_classes.tesseract import tesseract_tachyon_list
from consts.consts_w2 import max_NBLB, max_vial_level
from consts.progression_tiers import true_max_tiers, tesseract_progressionTiers
from models.general.session_data import session_data
from models.advice.advice import Advice
from models.advice.advice_section import AdviceSection
from models.advice.advice_group import AdviceGroup
from models.advice.generators.w2 import get_arcade_advice
from utils.misc.add_subgroup_if_available_slot import add_subgroup_if_available_slot
from utils.logging import get_logger
from utils.number_formatting import round_and_trim
from utils.text_formatting import notateNumber, pl

logger = get_logger(__name__)

def find_enemy_map(world_number: int, map_name: str):
    #Look up the account's EnemyMap data for a zone by name, if it's been parsed
    world = session_data.account.enemy_worlds.get(world_number)
    if not world:
        return None
    return next((enemy_map for enemy_map in world.maps_dict.values() if enemy_map.map_name == map_name), None)

def get_progression_tiers_advice_group(tesseract) -> tuple[dict[str, AdviceGroup], int, int, int]:
    tesseract_advices = {
        'Total Upgrades': {},
        'Specific Upgrades': {},
        'Highest Map': {},
    }
    optional_tiers = 0
    true_max = true_max_tiers['The Tesseract']
    max_tier = true_max - optional_tiers
    tier_total_upgrades = 0
    tier_specific_upgrades = 0
    tier_highest_map = 0

    #Assess Tiers
    for tier_number, requirements in tesseract_progressionTiers.items():
        subgroup_label = build_subgroup_label(tier_number, max_tier)

        #Total Upgrades
        if tesseract.total_upgrades < requirements.get('Total Upgrades', 0):
            add_subgroup_if_available_slot(tesseract_advices['Total Upgrades'], subgroup_label)
            if subgroup_label in tesseract_advices['Total Upgrades']:
                tesseract_advices['Total Upgrades'][subgroup_label].append(Advice(
                    label="Total Tesseract Upgrades",
                    picture_class='tesseract',
                    progression=tesseract.total_upgrades,
                    goal=requirements.get('Total Upgrades', 0)
                ))
        if subgroup_label not in tesseract_advices['Total Upgrades'] and tier_total_upgrades == tier_number - 1:
            tier_total_upgrades = tier_number

        #Specific Upgrades - account-wide talents
        for upgrade_name, required_level in requirements.get('Specific Upgrades', {}).items():
            upgrade_details = tesseract.upgrades.get(upgrade_name)
            current_level = upgrade_details.level if upgrade_details else 0
            if current_level < required_level:
                add_subgroup_if_available_slot(tesseract_advices['Specific Upgrades'], subgroup_label)
                if subgroup_label in tesseract_advices['Specific Upgrades']:
                    tesseract_advices['Specific Upgrades'][subgroup_label].append(
                        upgrade_details.get_tier_advice(required_level) if upgrade_details else Advice(
                            label=upgrade_name,
                            picture_class='tesseract',
                            progression=current_level,
                            goal=required_level
                        )
                    )
        if subgroup_label not in tesseract_advices['Specific Upgrades'] and tier_specific_upgrades == tier_number - 1:
            tier_specific_upgrades = tier_number

        #Highest Map
        map_requirement = requirements.get('Highest Map')
        if map_requirement:
            target_map = find_enemy_map(map_requirement['World'], map_requirement['Map Name'])
            map_opened = bool(target_map and target_map.kill_count > 0)
            if not map_opened:
                add_subgroup_if_available_slot(tesseract_advices['Highest Map'], subgroup_label)
                if subgroup_label in tesseract_advices['Highest Map']:
                    tesseract_advices['Highest Map'][subgroup_label].append(Advice(
                        label=f"Reach {map_requirement['Map Name']} (World {map_requirement['World']})",
                        picture_class=target_map.monster_image if target_map else 'tesseract',
                        progression=int(map_opened),
                        goal=1
                    ))
        if subgroup_label not in tesseract_advices['Highest Map'] and tier_highest_map == tier_number - 1:
            tier_highest_map = tier_number

    #Generate AdviceGroups
    tesseract_advice_group_dict = {}
    tesseract_advice_group_dict['Total Upgrades'] = AdviceGroup(
        tier=tier_total_upgrades,
        pre_string='Purchase more Total Tesseract Upgrades',
        advices=tesseract_advices['Total Upgrades'],
    )
    tesseract_advice_group_dict['Specific Upgrades'] = AdviceGroup(
        tier=tier_specific_upgrades,
        pre_string=f"Level up the following account-wide Tesseract Upgrade{pl(tesseract_advices['Specific Upgrades'])}",
        advices=tesseract_advices['Specific Upgrades'],
    )
    tesseract_advice_group_dict['Highest Map'] = AdviceGroup(
        tier=tier_highest_map,
        pre_string='Reach the following zones',
        advices=tesseract_advices['Highest Map'],
    )

    overall_section_tier = min(true_max, tier_total_upgrades, tier_specific_upgrades, tier_highest_map)
    return tesseract_advice_group_dict, overall_section_tier, max_tier, true_max


def get_tesseract_currencies_advice_group(tesseract) -> AdviceGroup:
    currency_advices = {
        'Currencies': [],
    }
    currency_advices['Currencies'].append(Advice(
        label=f"Total Tachyons Collected: {notateNumber('Basic', tesseract.total_tachyons_collected, 3)}",
        picture_class='tachion-truth'
    ))
    if tesseract.arcane_rocks_enabled:
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
            label=f"{tachyon_name}: {notateNumber('Basic', tesseract.tachyons[tachyon_index], 3)}",
            picture_class=f'tesseract-tachyon-{tachyon_index}'
        ) for tachyon_index, tachyon_name in enumerate(tesseract_tachyon_list)
    ]

    #Tachyon Multi calculation groups
    currency_advices['Currencies'].append(Advice(
        label=f"Total Tachyon multi: {tesseract.tachyon_calc['Total']:.3f}x",
        picture_class='tesseract'
    ))

    mga_label = f"Tachyon Multi Group A: {tesseract.tachyon_calc['mga']:.2f}x"
    currency_advices[mga_label] = []

    currency_advices[mga_label].append(tesseract.upgrades['Ripple in Spacetime'].get_bonus_advice())
    currency_advices[mga_label].append(tesseract.get_tesseract_talent_advice())
    currency_advices[mga_label].append(tesseract.upgrades['Verdon Hoarding'].get_bonus_advice())
    currency_advices[mga_label].append(tesseract.upgrades['Aurion Hoarding'].get_bonus_advice())

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

    mgb_label = f"Tachyon Multi Group B: {tesseract.tachyon_calc['mgb']:.2f}x"

    emperor_tachyon_bonus = session_data.account.emperor["Arcane Cultist Extra Tachyons"]
    tachyon_bubble = session_data.account.alchemy_bubbles['Tachyon Bubble']

    currency_advices[mgb_label] = [
        emperor_tachyon_bonus.get_bonus_advice(),
        Advice(
            label=f"{{{{ Alchemy Bubbles|#bubbles }}}} - Tachyon Bubble: +{round_and_trim(tachyon_bubble['BaseValue'])}/250%",
            picture_class='tachyon-bubble',
            resource=tachyon_bubble['Material'],
            progression=tachyon_bubble['Level'],
            goal=max_NBLB
        )
    ]

    mgc_label = f"Bone Multi Group C: {tesseract.tachyon_calc['mgc']:.2f}x"
    currency_advices[mgc_label] = [
        session_data.account.sneaking.pristine_charms[
            'Mystery Fizz'
        ].get_obtained_advice()
    ]

    mgd_label = f"Tachyon Multi Group D: {tesseract.tachyon_calc['mgd']:.2f}x"
    currency_advices[mgd_label] = [tesseract.get_backup_energy_advice()]

    mge_label = f"Tachyon Multi Group E: {tesseract.tachyon_calc['mge']:.2f}x"

    missing_bundle_data_txt = '<br>Note: Could be inaccurate. Bundle data not found!' if not session_data.account.gemshop['Bundle Data Present'] else ''
    missing_bundle_data = not session_data.account.gemshop['Bundle Data Present']
    has_arcanist_pack = session_data.account.gemshop['Bundles']['bun_x']['Owned']
    ac_pack_value = tesseract.tachyon_calc['mge']
    currency_advices[mge_label] = [Advice(
        label=f"Gemshop - Arcane Cultist Pack:"
              f"<br>{ac_pack_value}/1.2x Tachyons"
              f"{missing_bundle_data_txt}",
        picture_class='gem',
        progression=int(has_arcanist_pack) if not missing_bundle_data else 'IDK',
        goal=1
    )]

    mgf_label = f"Tachyon Multi Group F: {round_and_trim(tesseract.tachyon_calc['mgf'])}x"
    vial = session_data.account.alchemy_vials["Paper Pint (Chapter Three 'This is Gospel')"]
    currency_advices[mgf_label] = [Advice(
        label=f"{{{{ Vial|#vials }}}}: Paper Pint: +{round_and_trim(vial['Value'])}%",
        picture_class='spelunking-chapter-3',
        progression=vial['Level'],
        goal=max_vial_level
    )]

    mgg_label = f"Tachyon Multi Group G: {round_and_trim(tesseract.tachyon_calc['mgg'])}x"
    _, ballonfish_advice = session_data.account.companions['Balloonfish'].get_advice()
    currency_advices[mgg_label] = [ballonfish_advice]

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
            label=f"Total Tesseract Upgrades: {tesseract.total_upgrades:,}",
            picture_class='tesseract'
        )]
    }

    #Upgrades
    upgrades_advice_dict['Upgrades'] += [
        upgrade_details.get_advice(tesseract.total_upgrades) for upgrade_details in tesseract.upgrades.values()
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
    tesseract_advice_group_dict, overall_section_tier, max_tier, true_max = get_progression_tiers_advice_group(tesseract)
    tesseract_advice_group_dict['Currencies'] = get_tesseract_currencies_advice_group(tesseract)
    tesseract_advice_group_dict['Upgrades'] = get_tesseract_upgrades_advice_group(tesseract)

    #Generate AdviceSection
    tier_section = f"{overall_section_tier}/{max_tier}"
    tesseract_advice_section = AdviceSection(
        name='The Tesseract',
        tier=tier_section,
        pinchy_rating=overall_section_tier,
        max_tier=max_tier,
        true_max_tier=true_max,
        header=f"Best Tesseract tier met: {tier_section}{break_you_best if overall_section_tier >= max_tier else ''}",
        picture='customized/Tesseract.gif',
        groups=tesseract_advice_group_dict.values(),
        completed=None,
    )

    return tesseract_advice_section
