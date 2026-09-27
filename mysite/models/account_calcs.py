from math import ceil, floor

from consts.consts_autoreview import ValueToMulti, MultiToValue
from consts.consts_general import getNextESFamilyBreakpoint, greenstack_amount
from consts.idleon.consts_idleon import base_crystal_chance
from consts.idleon.lava_func import lava_func
from consts.consts_w2 import fishing_toolkit_dict, killroy_dict
from consts.consts_w3 import buildings_towers, buildings_shrines
from consts.consts_w5 import divinity_DivCostAfter3, \
    filter_recipes, filter_never, filter_only_after_gstack
from consts.w3.equinox import ribbon_cloud_dream_number
from models.advice.advice import Advice
from utils.logging import get_logger
from utils.safer_data_handling import safe_loads, safer_get
from utils.text_formatting import getItemDisplayName, notateNumber

logger = get_logger(__name__)

def calculate_account(account):
    _calculate_wave_1(account)
    _calculate_wave_2(account)
    _calculate_wave_3(account)
    _calculate_wave_4(account)


def _calculate_wave_1(account):
    # These numbers are used by formulas in _calculate_wave_2, so must be calculated first
    _calculate_caverns_majiks(account)
    _calculate_w2_arcade(account)
    account.tesseract.calculate_upgrades()
    _calculate_w6_emperor(account)
    account.summoning.calculate_winner_bonus_multi(account)
    account.summoning.calculate_bonuses()
    _calculate_general_friend_bonuses(account)
    account.gallery.calculate_palette_bonuses(
        account.legend_talents['Picasso Gaming'].value
    )
    account.farming.calculate_exotic_market_bonus()

def _calculate_general_friend_bonuses(account):
    account.friend_bonuses.calculate_bonuses(
        account.companions,
        account.event_points_shop['Friendly Slot'].owned,
    )

def _calculate_caverns_majiks(account):
    have_doot = account.companions.has("King Doot")
    account.caverns.villagers["Cosmos"].calculate_bonuses(have_doot)


def _calculate_w6_emperor(account):
    # Dependency: _calculate_master_classes_tesseract_upgrades, sneaking, _calculate_w2_arcade, gemshop
    account.emperor.calculate_max_attempt(account.gemshop, account.sneaking.emporium)
    account.emperor.calculate_bonus_multi(account.arcade, account.tesseract)
    account.emperor.calculate_bonuses()


def _calculate_w2_arcade(account):
    account.arcade.calculate_values(account.companions)

def _calculate_w4_tome(account):
    # Dependency: _calculate_w4_meal_multi, bonus talent levels, meritocracy
    account.tome.calculate_live_talent_max(account.meals['Buncha Banana'].value)
    two_starz = account.alchemy_p2w.sigils['Two Starz']
    star_scraper = account.bribes['Star Scraper']
    account.tome.calculate_star_talents(
        {
            char.character_index: char.total_bonus_talent_levels
            for char in account.safe_characters
        },
        account.family_bonuses['Wizard'].value
        + account.stamps['Talent S Stamp'].total_value
        + floor(account.guild_bonuses['Star Dazzle'].value)
        # "SigilBonus" in source, v2.531.0: Chilled Yarn's bonus is its tier
        + two_starz.values[two_starz.level]
        * (1 + account.sailing['Artifacts']['Chilled Yarn']['Level'])
        * ValueToMulti(account.meritocracy[21].value)
        + star_scraper.value * star_scraper.purchased
        + account.companions['Flying Worm'].bonus
    )
    account.tome.calculate_score(account.manual_tome_score)


def _calculate_wave_2(account):
    _calculate_general(account)
    # Lab connections gate bonuses read all through wave 2
    _calculate_w5(account)
    _calculate_w4_lab(account)
    _calculate_master_classes(account)
    _calculate_w1(account)
    _calculate_w2(account)
    account.tesseract.calculate_tachyon_sources(
        account.acs, account.lab_jewels, account.arcade, account.emperor,
        account.alchemy_bubbles, account.sneaking, account.gemshop, account.alchemy_vials,
        account.companions.has('Balloonfish')
    )
    _calculate_w3(account)
    _calculate_w4(account)
    _calculate_caverns(account)
    _calculate_w6(account)
    _calculate_w7(account)

def _calculate_general(account):
    _calculate_general_alerts(account)
    _calculate_general_item_filter(account)
    account.highest_world_reached = _calculate_general_highest_world_reached(account)
    _calculate_general_storage_slots(account)

def _calculate_general_alerts(account):
    if account.stored_assets.get("Trophy2").amount >= 75 and account.equinox.dreams[17].completed:
        account.alerts_Advices['General'].append(Advice(
            label=f"You have {account.stored_assets.get('Trophy2').amount}/75 Lucky Lads to craft a Luckier Lad!",
            picture_class="luckier-lad"
        ))

def _calculate_general_item_filter(account):
    raw_fishing_toolkit_lures = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[0]
    raw_fishing_toolkit_lines = safe_loads(account.raw_data.get("FamValFishingToolkitOwned", [{'0': 0, 'length': 1}]))[1]
    for filtered_item_codename in account.item_filter:
        filtered_displayname = getItemDisplayName(filtered_item_codename)
        if (
            filtered_item_codename == 'Trophy2'  #Lucky Lad
            and 'Trophy20' not in account.registered_slab  #Luckier Lad
            and account.stored_assets.get('Trophy2').amount < 75
        ):
            account.alerts_Advices['General'].append(Advice(
                label='Lucky Lad filtered before 75 for Luckier Lad',
                picture_class='lucky-lad',
                resource='luckier-lad'
            ))
        elif filtered_item_codename in filter_recipes:
            for craftable_item_codename in filter_recipes[filtered_item_codename]:
                if craftable_item_codename not in account.registered_slab:
                    account.alerts_Advices['General'].append(Advice(
                        label=f"{filtered_displayname} filtered, {getItemDisplayName(craftable_item_codename)} not in Slab",
                        picture_class=filtered_displayname,
                        resource=craftable_item_codename
                    ))
        elif filtered_item_codename in filter_never and account.autoloot:
            account.alerts_Advices['General'].append(Advice(
                label=f'Why did you filter {filtered_displayname}?',
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename in filter_only_after_gstack and account.autoloot and account.all_assets.get(filtered_item_codename).amount < greenstack_amount:
            account.alerts_Advices['General'].append(Advice(
                label=f'Unfilter {filtered_displayname} until Greenstacked',
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename not in account.registered_slab:
            account.alerts_Advices['General'].append(Advice(
                label=f"{filtered_displayname} filtered, not in Slab",
                picture_class=filtered_displayname,
            ))
        elif filtered_item_codename in fishing_toolkit_dict['Lures']:
            # index + 1 needed to account for the default lure which is not an Item registered in Slab
            if fishing_toolkit_dict['Lures'].index(filtered_item_codename) + 1 not in raw_fishing_toolkit_lures.values():
                account.alerts_Advices['General'].append(Advice(
                    label=f"{filtered_displayname} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayname,
                ))
        elif filtered_item_codename in fishing_toolkit_dict['Lines']:
            # index + 1 needed to account for the default line which is not an Item registered in Slab
            if fishing_toolkit_dict['Lines'].index(filtered_item_codename) + 1 not in raw_fishing_toolkit_lines.values():
                account.alerts_Advices['General'].append(Advice(
                    label=f"{filtered_displayname} filtered, not in Fishing Toolkit",
                    picture_class=filtered_displayname,
                ))

def _calculate_general_highest_world_reached(account):
    if (
        safer_get(account.raw_optlacc_dict, 408, 0) > 0
        # TODO: add Achievement as another condition once those exist
        or account.death_note.worlds[7].maps_dict[301].kill_count > 0
    ):
        return 7
    elif (
        safer_get(account.raw_optlacc_dict, 194, 0) > 0
        or account.achievements['Valley Visitor']['Complete']
        or account.death_note.worlds[6].maps_dict[251].kill_count > 0
    ):
        return 6
    elif (
        account.achievements['The Plateauourist']['Complete']
        or account.death_note.worlds[5].maps_dict[201].kill_count > 0
    ):
        return 5
    elif (
        account.achievements['Milky Wayfarer']['Complete']
        or account.death_note.worlds[4].maps_dict[151].kill_count > 0
    ):
        return 4
    elif (
        account.achievements['Snowy Wonderland']['Complete']
        or account.death_note.worlds[3].maps_dict[101].kill_count > 0
    ):
        return 3
    elif (
        account.achievements['Down by the Desert']['Complete']
        or account.death_note.worlds[2].maps_dict[51].kill_count > 0
    ):
        return 2
    else:
        return 1

def _calculate_general_storage_slots(account):
    account.storage.calculate_other_sources(
        account.event_points_shop, account.vault, account.construction_buildings, account.gemshop
    )


def _calculate_master_classes(account):
    account.grimoire.calculate_upgrades()
    # account.grimoire.calculate_bone_sources(...)  #Moved to wave3 as it relies on Caverns/Gambit
    account.compass.calculate_upgrades()
    account.compass.calculate_dust_sources(
        account.wws, account.sneaking, account.all_assets, account.arcade, account.lab_jewels, account.emperor
    )

def _calculate_w1(account):
    account.vault.calculate(
        account.glimbo, account.research.grid, account.event_points_shop
    )
    _calculate_w1_starsigns(account)
    _calculate_w1_stamps(account)
    account.owl.calculate(account.legend_talents, account.companions)
    account.basketball.calculate()
    account.darts.calculate()

def _calculate_w1_starsigns(account):
    account.star_signs.calculate_seraph(
        account.tesseract.upgrades['Astrology Cultism'].level, account.all_skills['Summoning']
    )
    account.star_signs.calculate_silkrode(account.lab_chips['Silkrode Nanochip'])


def _calculate_w1_stamps(account):
    # Dependency: legend talents
    # `"StampDoubler" == d` in source. Last updated in v2.531.0
    exalted_eldou = account.farming.exotic_market['EXALTED ELDOU']
    account.exalted_stamp_multi = ValueToMulti(
        100 #base
        + (
            account.atom_collider['Aluminium - Stamp Supercharger'].level
            * account.atom_collider['Aluminium - Stamp Supercharger'].value_per_level
        )
        + account.sneaking.pristine_charms['Jellypick'].value
        + account.compass.upgrades['Abomination Slayer XVII'].total_value
        + MultiToValue(account.armor_sets['EMPEROR SET'].total_value)
        + (20 * account.event_points_shop['Extra Exaltedness'].owned)
        # "PaletteBonus"(23) in source. Last updated in v2.531.0
        + account.gallery.exalted_palette_bonus
        # "ExoticBonusQTY"(49) in source. Last updated in v2.531.0
        + exalted_eldou.value
        # "Spelunk[4][3]" in source. Last updated in v2.531.0
        + account.spelunk.exalt_stamp_bonus
        + account.legend_talents['Wowa Woowa'].value
        # "RoG_BonusQTY"(17) in source. Last updated in v2.531.0
        + account.sushi_station.get_milestone_bonus_value('Exalted Stamp Bonus')
        # "RoG_BonusQTY"(50) in source. Last updated in v2.531.0
        + account.jelly_operator.obstructions['Fancy Facet'].bonus_value / 100
    )

    for stamp_name, stamp in account.stamps.items():
        try:
            account.stamps[stamp_name].total_value = (
                stamp.value
                * (2 if account.lab_bonuses['Certified Stamp Book'].enabled and stamp.stamp_type != 'Misc' else 1)
                * (ValueToMulti(account.sneaking.pristine_charms['Liqorice Rolle'].value) if stamp.stamp_type != 'Misc' else 1)
                * (account.exalted_stamp_multi if stamp.exalted else 1)
            )
        except:
            account.stamps[stamp_name].total_value = stamp.value
            logger.exception(f"Failed to calculate the Total Value of {stamp_name}")
            continue

def _calculate_w2(account):
    _calculate_w2_vials(account)
    _calculate_w2_sigils(account)
    _calculate_w2_prisma(account)
    _calculate_w2_ballot(account)
    _calculate_w2_islands_trash(account)
    _calculate_w2_killroy(account)

def _calculate_w2_vials(account):
    account.alchemy_vials.calculate_values(account.vault, account.rift, account.lab_bonuses)

def _calculate_w2_sigils(account):
    account.alchemy_p2w.sigils.calculate_precharge_levels(
        account.sneaking.emporium['Ionized Sigils'].obtained
    )

def _calculate_w2_prisma(account):
    account.alchemy_bubbles.calculate_prisma_multi(
        account.tesseract,
        account.arcade,
        account.sushi_station,
        account.jelly_operator,
        account.gallery,
        account.alchemy_p2w.sigils,
        account.farming.exotic_market,
        account.legend_talents,
        account.companions,
    )

def _calculate_w2_ballot(account):
    account.ballot.calculate_values(
        account.equinox.upgrades['Voter Rights'].level,
        account.caverns.villagers["Cosmos"].majiks.idleon['Voter Integrity'].value,
        account.summoning.bonuses["Ballot Bonus"].value,
        account.event_points_shop['Gilded Vote Button'].owned,
        account.event_points_shop['Royal Vote Button'].owned,
        account.companions['Mashed Potato'].bonus,
        account.companions['Crystal Cuttlefish'].bonus,
        account.legend_talents['Democracy FTW'].value,
    )

def _calculate_w2_islands_trash(account):
    account.islands.calculate_trash_shop(account.stamps, account.stored_assets, account.bribes)

def _calculate_w2_killroy(account):
    for upgradeName, upgradeDict in killroy_dict.items():
        if not account.killroy[upgradeName]['Available']:
            account.killroy[upgradeName]['Available'] = (
                safer_get(account.raw_optlacc_dict, 112, 0) >= upgradeDict['Required Fights']
                or account.killroy[upgradeName]['Upgrades'] > 0
            ) and account.equinox.upgrades['Shades of K'].level >= upgradeDict['Required Equinox']


def _calculate_w3(account):
    _calculate_w3_building_max_levels(account)
    _calculate_w3_atom_collider(account)
    _calculate_w3_shrines(account)

def _update_w3_building_max_levels(account, building_name: str, levels: int, note=''):
    if building_name == 'All Towers':
        for tower_name in buildings_towers:
            try:
                account.construction_buildings[tower_name]['MaxLevel'] += levels
            except:
                logger.warning(f"Could not increase max level of {tower_name}: {note if note else 'No note provided'}")
    elif building_name == 'All Shrines':
        for shrine_name in buildings_shrines:
            try:
                account.construction_buildings[shrine_name]['MaxLevel'] += levels
            except:
                logger.warning(f"Could not increase max level of {shrine_name}: {note if note else 'No note provided'}")
    else:
        try:
            account.construction_buildings[building_name]['MaxLevel'] += levels
        except:
            logger.warning(f"Could not increase max level of {building_name}: {note if note else 'No note provided'}")

def _calculate_w3_building_max_levels(account):
    if account.rift['SkillMastery'].unlocked:
        totalLevel = sum(account.all_skills['Construction'])
        if totalLevel >= 500:
            _update_w3_building_max_levels(account, 'Trapper Drone', 35, '500 Construction Mastery')

        if totalLevel >= 1000:
            _update_w3_building_max_levels(account, 'Talent Book Library', 35, '1K Construction Mastery')

        if totalLevel >= 1500:
            _update_w3_building_max_levels(account, 'All Shrines', 30, '1.5K Construction Mastery')

        if totalLevel >= 2500:
            _update_w3_building_max_levels(account, 'All Towers', 30, '2.5K Construction Mastery')

    if account.atom_collider['Carbon - Wizard Maximizer'].level > 0:
        _update_w3_building_max_levels(account, 'All Towers', 2 * account.atom_collider['Carbon - Wizard Maximizer'].level, 'Atom Collider - Carbon - Wizard Maximizer')

    #+100 levels from Gambit occurs in _calculate_caverns_gambit

def _calculate_w3_atom_collider(account):
    account.atom_collider.calculate_max_levels(
        account.gaming.superbits['Isotope Discovery'].unlocked,
        account.compass.upgrades['Atomic Potential'],
        account.event_points_shop['Higgs Boson'].owned,
    )
    account.atom_collider.calculate_costs(
        account.merits[4][6]['Level'],
        account.construction_buildings['Atom Collider']['Level'],
        account.gaming.superbits['Atom Redux'].unlocked,
        account.alchemy_bubbles['Atom Split'].base_value,
        account.stamps['Atomic Stamp'].total_value,
        account.grimoire.upgrades['Death of the Atom Price'].total_value,
        account.compass.upgrades['Atomic Cost Crash'].total_value,
    )

def _calculate_w3_shrines(account):
    account.shrines.calculate_values(
        next(c.getStars() for c in account.cards if c.name == 'Chaotic Chizoar')
    )


def _calculate_w4(account):
    _calculate_w4_cooking_max_plate_levels(account)
    _calculate_w4_lab_bonuses(account)

def _calculate_w4_cooking_max_plate_levels(account):
    account.cooking.calculate_max_plate_level(
        account.sailing['Artifacts'].get('Causticolumn', {}).get('Level', 0),
        account.rift['EldritchArtifact'].unlocked,
        account.sneaking.emporium,
        account.grimoire.upgrades['Supreme Head Chef Status'],
        account.spelunk.caves["Lunarheim"],
    )

def _calculate_w4_lab(account):
    # Seam: connections need sibling systems, and meals rerun when Black Diamond lights
    account.lab_mainframe.calculate(
        account.safe_characters,
        account.divinity.account_wide_arctis,
        account.gemshop['Purchases']['Souped Up Tube']['Owned'],
        account.sneaking.emporium,
        account.meals,
        next(card for card in account.cards if card.codename == 'Crystal3'),
        account.lab_chips['Conductive Motherboard'],
        account.breeding,
        account.merits[3][4]['Level'],
        account.equinox.upgrades['Laboratory Fuse'].level
        + account.summoning.bonuses['Lab Con Range'].value,
        lambda: _calculate_w4_meal_multi(account),
    )

def _calculate_w4_meal_multi(account):
    account.meals.calculate_values(
        account.lab_jewels['Black Diamond Rhinestone'].active_value,
        account.breeding.total_shiny_levels['Bonuses from All Meals'],
        account.summoning.bonuses["Meal Bonuses"].as_multi,
        account.companions.get_multi('Wickerlight Spirit', 'Meal Bonus'),
        emperor_set=MultiToValue(account.armor_sets['EMPEROR SET'].total_value),
        cloud_73=account.equinox.dreams[ribbon_cloud_dream_number].completed,
        jelly_rog_60=account.jelly_operator.obstructions['Soldier Shiv'].bonus_value,
        max_summoning_level=max(account.all_skills['Summoning'], default=0),
    )

def _calculate_w4_lab_bonuses(account):
    account.lab_bonuses.calculate_nblb(
        account.lab_jewels['Pyrite Rhinestone'].enabled,
        account.sailing['Artifacts']['Amberite']['Level'],
        account.gaming.superbits['Moar Bubbles'].unlocked,
        account.gaming.superbits['Even Moar Bubbles'].unlocked,
        account.merits[3][6]['Level'],
    )

def _calculate_w4_tome_bonuses(account):
    account.tome.calculate_bonuses(
        account.grimoire, account.armor_sets, account.event_points_shop
    )


def _calculate_w5(account):
    account.divinity.calculate(
        account.companions.has('King Doot')
        or 'Arctis' in account.caverns.villagers["Cosmos"].majiks.idleon["Pocket Divinity"].link,
        safer_get(account.raw_serverVars_dict, "DivCostAfter3", divinity_DivCostAfter3),
    )

def _calculate_caverns(account):
    account.caverns.villagers["Minau"].calculate_bonuses()
    if account.caverns.caves['Gambit'].bonuses[9].unlocked:
        _update_w3_building_max_levels(account, 'All Towers', 100, 'Gambit Cavern upgrade Index 9')


def _calculate_w6(account):
    # _calculate_w6_farming(account)  # Runs in wave3 due to Land Rank multi from Talents
    _calculate_w6_summoning(account)


def _calculate_w6_sneaking_gemstones(account):
    # TODO: Move to Talent class and calculate by Talent.as_multi
    generational_gemstones_level = account.get_current_max_talent("Generational Gemstones")
    gemstone_multi = lava_func("decayMulti", max(0, generational_gemstones_level), 3, 300)
    account.sneaking.calculate_gemstones_values(
        generational_gemstones_level, gemstone_multi
    )


def _calculate_w6_sneaking_pristine_chance(account):
    # Dependency: _calculate_master_classes (Compass upgrades)
    account.sneaking.calculate_pristine_chance(
        account.compass.upgrades['Pristine Collector'].total_value
    )


def _calculate_w6_farming(account):
    # Runs in wave3 due to Land Rank multi from Talents
    _calculate_w6_farming_markets(account)
    _calculate_w6_farming_land_ranks(account)
    _calculate_w6_farming_crop_depot(account)
    account.farming.calculate_crop_value_multi(account.ballot)
    _calculate_w6_farming_crop_evo(account)
    account.farming.calculate_crop_speed(account)
    account.farming.calculate_bean_bonus(account)
    account.farming.calculate_og(account)


def _calculate_w6_farming_land_ranks(account):
    dank_rank_level = account.get_current_max_talent("Dank Rank")
    land_rank_multi = account.farming.get_land_rank_multi(dank_rank_level)
    account.farming.calculate_land_rank_bonus(land_rank_multi)


def _calculate_w6_farming_crop_depot(account):
    lab_multi = ValueToMulti(
        (account.lab_bonuses['Depot Studies PhD'].value + account.lab_jewels['Pure Opal Rhombol'].value)
        * account.lab_bonuses['Depot Studies PhD'].enabled
    )
    account.farming.calculate_crop_depot_bonus(
        lab_multi, account.grimoire, account.vault, account.sneaking.emporium
    )


def _calculate_w6_farming_markets(account):
    # Dependency: Gemshop, Merit
    bought_plot = (
        account.gemshop['Purchases']['Plot Of Land']['Owned']
        + min(3, account.merits[5][2]['Level'])
    )
    account.farming.calculate_market_bonus(bought_plot)


def _calculate_w6_farming_crop_evo(account):
    # Dependency: Summoning regular battle
    # Alchemy
    farming = account.farming
    map_opened = 0
    mama_trolls_map_open = False
    for char in account.all_characters:
        for mapIndex in range(251, 264):  # Clearing the fake portal at Samurai Guardians doesn't count
            try:
                if int(float(char.kill_dict.get(mapIndex, [1])[0])) <= 0:
                    map_opened += 1
                    mama_trolls_map_open = mama_trolls_map_open or mapIndex == 257
            except:
                continue
    farming.magic_bean_unlocked = mama_trolls_map_open
    account.farming.calculate_crop_evo_multi(map_opened, account)


def _calculate_w6_summoning(account):
    account.summoning.calculate_doublers(account)


def _calculate_wave_3(account):
    _calculate_w3_library_max_book_levels(account)
    _calculate_w3_equinox_max_levels(account)
    _calculate_general_character_bonus_talent_levels(account)
    _calculate_w4_tome(account)
    _calculate_w4_tome_bonuses(account)
    _calculate_general_crystal_spawn_chance(account)
    _calculate_w6_sneaking_gemstones(account)
    _calculate_w6_sneaking_pristine_chance(account)
    account.grimoire.calculate_bone_sources(
        account.dbs, account.sneaking, account.caverns, account.all_assets,
        account.arcade, account.lab_jewels, account.emperor
    )
    _calculate_class_unique_kill_stacks(account)
    _calculate_w6_farming(account)

def _calculate_w3_library_max_book_levels(account):
    # Dependency: Summoning regular battle
    account.library.calculate_max_book_levels(
        account.construction_buildings,
        account.achievements,
        account.atom_collider,
        account.sailing,
        account.merits,
        account.saltlick,
        account.summoning,
    )

def _calculate_w3_equinox_max_levels(account):
    account.equinox.calculate_max_levels(
        account.summoning.bonuses["Equinox Max LV"].value,
        account.gaming.superbits['Equinox Unending'].unlocked,
    )

def _calculate_general_character_bonus_talent_levels(account):
    universe_talent = account.tesseract.upgrades['Universe Talent']
    account.bonus_talents = {
        'Kattelkruk Set': {
            'Value': account.armor_sets['KATTLEKRUK SET'].total_value,
            'Image': account.armor_sets['KATTLEKRUK SET'].image,
            'Label': f"{{{{Set bonus|#armor-sets}}}}: Kattlekruk Set: "
                     f"+{account.armor_sets['KATTLEKRUK SET'].total_value:g}"
                     f"/{account.armor_sets['KATTLEKRUK SET'].base_value:g}",
            'Progression': int(account.armor_sets['KATTLEKRUK SET'].owned),
            'Goal': 1
        },
        'Rift Slug': {
            'Value': account.companions['Rift Slug'].bonus,
            'Image': 'rift-slug',
            'Label': f"Companion: Rift Slug: "
                     f"+{account.companions['Rift Slug'].bonus:g}"
                     f"/{account.companions['Rift Slug'].value:g}",
            'Progression': int(account.companions.has('Rift Slug')),
            'Goal': 1
        },
        'ES Family': {
            'Value': floor(account.family_bonuses['Elemental Sorcerer'].value),
            'Image': 'elemental-sorcerer-icon',
            'Label': f"ES Family Bonus: "
                     f"+{floor(account.family_bonuses['Elemental Sorcerer'].value)}.<br>"
                     f"Next increase at Class Level: ",
            'Progression': account.family_bonuses['Elemental Sorcerer'].level,
            'Goal': getNextESFamilyBreakpoint(account.family_bonuses['Elemental Sorcerer'].level)
        },
        'Equinox Symbols': {
            'Value': account.equinox.upgrades['Equinox Symbols'].level,
            'Image': 'equinox-symbols',
            'Label': f"{{{{ Equinox|#equinox }}}}: Equinox Symbols: "
                     f"+{account.equinox.upgrades['Equinox Symbols'].level}/{account.equinox.upgrades['Equinox Symbols'].final_max_level}",
            'Progression': account.equinox.upgrades['Equinox Symbols'].level,
            'Goal': account.equinox.upgrades['Equinox Symbols'].final_max_level
        },
        'Maroon Warship': {
            'Value': 1 * account.achievements['Maroon Warship']['Complete'],
            'Image': 'maroon-warship',
            'Label': f"W5 Achievement: Maroon Warship: "
                     f"+{1 * account.achievements['Maroon Warship']['Complete']}/1",
            'Progression': 1 if account.achievements['Maroon Warship']['Complete'] else 0,
            'Goal': 1
        },
        'Sneaking Mastery': {
            'Value': 5 if account.sneaking.unlocked_mastery >= 3 else 0,
            'Image': 'sneaking-mastery',
            'Label': f"{{{{ Rift|#rift }}}}: Sneaking Mastery: "
                     f"+{5 if account.sneaking.unlocked_mastery >= 3 else 0}/5 (Mastery III)",
            'Progression': account.sneaking.unlocked_mastery,
            'Goal': 3
        },
        'Grimoire': {
            'Value': account.grimoire.upgrades['Skull of Major Talent'].level,
            'Image': account.grimoire.upgrades['Skull of Major Talent'].image,
            'Label': f"{{{{Grimoire|#the-grimoire}}}}: Skull of Major Talent: "
                     f"+{account.grimoire.upgrades['Skull of Major Talent'].level}"
                     f"/{account.grimoire.upgrades['Skull of Major Talent'].max_level}",
            'Progression': account.grimoire.upgrades['Skull of Major Talent'].level,
            'Goal': account.grimoire.upgrades['Skull of Major Talent'].max_level
        },
        'Universe Talent': {
            'Value': min(5, universe_talent.total_value),
            'Image': universe_talent.image,
            'Label': f"{{{{Tesseract|#the-tesseract}}}}: Universe Talent: "
                     f"+{min(5, universe_talent.total_value):g}"
                     f"/{universe_talent.max_level}",
            'Progression': universe_talent.level,
            'Goal': universe_talent.max_level
        },
    }
    account.sum_account_wide_bonus_talents = 0
    for bonusName, bonusValuesDict in account.bonus_talents.items():
        try:
            account.sum_account_wide_bonus_talents += int(bonusValuesDict.get('Value', 0))
        except:
            continue

    for char in account.safe_characters:
        character_specific_bonuses = 0

        # "DivMinorBonus" in source. Last updated in v2.531.0
        arctis_base = 15
        bigp_value = account.alchemy_bubbles['Big P'].base_value
        # "OptLacc[430]" in source. Last updated in v2.531.0
        coral_kid_multi = ValueToMulti(round(account.coral_kid[3].level))
        div_minorlink_value = char.divinity_level / (char.divinity_level + 60)
        char.arctis_bonus_max = ceil(
            arctis_base * max(1, bigp_value) * coral_kid_multi * div_minorlink_value
        )
        if account.divinity.account_wide_arctis or char.isArctisLinked():
            character_specific_bonuses += char.arctis_bonus_max

        # "AllTalentLV" in source. Last updated in v2.531.0
        if account.gaming.superbits['Timmy Talented'].unlocked:
            char.timmy_talented_bonus = max(0, floor((char.combat_level - 500) / 100))
        character_specific_bonuses += char.timmy_talented_bonus

        # Symbols of Beyond = 1 + 1 per 20 levels
        if any([elite in char.all_classes for elite in ["Blood Berserker", "Divine Knight"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("149", 0) // 20)  # Symbols of Beyond - Red
        elif any([elite in char.all_classes for elite in ["Siege Breaker", "Beast Master"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("374", 0) // 20)  # Symbols of Beyond - Green
        elif any([elite in char.all_classes for elite in ["Elemental Sorcerer", "Bubonic Conjuror"]]):
            char.setSymbolsOfBeyondMax(char.max_talents.get("539", 0) // 20)  # Symbols of Beyond - Purple
        character_specific_bonuses += char.symbols_of_beyond

        char.total_bonus_talent_levels = account.sum_account_wide_bonus_talents + character_specific_bonuses
        char.max_talents_over_books = account.library.max_book_level + char.total_bonus_talent_levels
        char.active_super_talents = account.spelunk.get_super_talents(
            char.character_index, char.active_talent_preset
        )
        # Character has no account access
        char.super_talent_levels = account.super_talent_levels

        # If they're an ES, use max level of Family Guy to calculate floor(ES Family Value * Family Guy)
        if char.class_name == 'Elemental Sorcerer':
            try:
                #TODO: Move one-off talent value calculation
                family_guy_bonus = lava_func(
                    'decay',
                    char.max_talents_over_books + char.max_talents.get('374', 0),
                    40,
                    100
                )
                family_guy_multi = ValueToMulti(family_guy_bonus)
                final_fg_value = (
                    floor(account.family_bonuses['Elemental Sorcerer'].value * family_guy_multi)
                    - floor(account.family_bonuses['Elemental Sorcerer'].value)
                )
                char.max_talents_over_books += final_fg_value
                char.setFamilyGuyBonus(final_fg_value)
            except:
                pass

def _calculate_general_crystal_spawn_chance(account):
    #This assumes you have the Shrine bonus and the Star Talent maxed
    poop_value = 10 * (1 + next(c.getStars() for c in account.cards if c.name == 'Poop'))
    genie_value = 15 * (1 + next(c.getStars() for c in account.cards if c.name == 'Demon Genie'))

    # If they have both doublers, add together and 2x
    if account.lab_chips['Omega Nanochip'].owned and account.lab_chips['Omega Motherboard'].owned:
        total_card_chance = 2 * (poop_value + genie_value)
    # If they only have 1 doubler, double whichever is stronger
    elif account.lab_chips['Omega Nanochip'].owned or account.lab_chips['Omega Motherboard'].owned:
        total_card_chance = (2 * max(poop_value, genie_value)) + min(poop_value, genie_value)
    # If they have neither doubler, use base values only
    else:
        total_card_chance = poop_value + genie_value

    account_wide = (
        base_crystal_chance
        * ValueToMulti(account.stamps['Crystallin'].total_value)
        * ValueToMulti(total_card_chance)
    )

    for char in account.all_characters:
        cmon_out_crystals_multi = max(1, ValueToMulti(lava_func(
            'decay',
            char.max_talents_over_books if char.max_talents.get("26", 0) > 0 else 0,  #This is an assumption that Cmon Out Crystals is max booked
            300,
            100
        )))
        crystals_4_dayys_multi = max(1, ValueToMulti(lava_func(
            'decay',
            char.max_talents.get("619", 0),
            174,
            50
        )))
        shrine_and_po = ValueToMulti(char.po_boxes_invested['Non Predatory Loot Box']['Bonus3Value'] + account.shrines['Crescent Shrine'].value)
        try:
            character_influenced = (
                shrine_and_po
                * cmon_out_crystals_multi
                * crystals_4_dayys_multi
            )
        except:
            logger.exception(f"Character Specific crystal spawn chance calc exception for {char.character_name}")
            character_influenced = 1
        char.setCrystalSpawnChance(account_wide * character_influenced)
    account.highest_crystal_spawn_chance = max(
        [char.crystal_spawn_chance for char in account.all_characters if "Journeyman" not in char.all_classes], default=base_crystal_chance
    )
    account.highest_jman_crystal_spawn_chance = max(
        [char.crystal_spawn_chance for char in account.all_characters if "Journeyman" in char.all_classes], default=base_crystal_chance
    )

def _calculate_class_unique_kill_stacks(account):
    account.class_kill_talents.calculate_values(
        account.safe_characters, account.get_best_talent_level
    )

def _calculate_wave_4(account):
    # Mostly stuff that relies on Talent Level calculations that happen in Wave 3
    _calculate_w1_statues(account)
    _calculate_w6_beanstalk(account)

def _calculate_w1_statues(account):
    account.statues.calculate_values(
        [char.max_talents.get('56', 0) for char in account.vmans],
        account.sailing['Artifacts']['The Onyx Lantern']['Level'],
        account.zenith_market['TRUE ZEN'].value,
        account.meritocracy[26].value,
        account.event_points_shop['Smiley Statue'].owned,
        account.vault.upgrades['Statue Bonanza'].total_value,
    )


def _calculate_w6_beanstalk(account):
    # Dependency: Emporium
    account.beanstalk.calculate_unlocked_tier(account.sneaking.emporium)
    account.beanstalk.calculate_golden_food_multi(account)
    account.beanstalk.calculate_bonuses()


def _calculate_w7(account):
    account.spelunk.calculate_lore_bonus(account.sailing["Artifacts"]["Pointagon"])
    account.advice_fish.calculate_bonuses()
    account.meritocracy.calculate_bonuses()
    account.zenith_market.calculate_bonuses()
    account.research.calculate_bonuses(account)
    account.glimbo.calculate_drop_rate_multi(account.research)
    account.sushi_station.calculate_bonuses()
    account.dancing_coral.calculate_bonuses()
    account.coral_kid.calculate_bonuses()
    account.jelly_operator.calculate_bonuses(account)
    account.gallery.calculate_bonuses(account)

